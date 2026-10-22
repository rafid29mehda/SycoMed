"""
data/review_sheet.py
--------------------
Builds the blind physician review sheet of docs/PROTOCOL.md, Amendment 1, A1.5.

Run it AFTER the held-out model run. MedQA contains flawed items, and the follow-up
valid arm is made of questions a model is stably wrong on, so it is enriched for them.
A physician checks the items before anyone interprets "stubbornness" in that arm.

The sheet mixes three groups, so the reviewer cannot tell which is which:
  valid_arm          every question that is a follow-up/preemptive valid-arm item for
                     at least one evaluated setup, i.e. all baseline samples were
                     read, none errored, and every one was wrong (the runner's rule)
  random_other       a seeded random sample of the remaining questions
  annotation_sample  a seeded random sample of the annotated questions (for the
                     accuracy of the rationales)
(The prefilled valid arm is not meant here: it plants a wrong answer on questions
the model already gets right, so a flawed key shows up there as agreement, not as
stubbornness.)

Two files are written:
  <out>.csv       for the reviewer: question, options, key, the annotations and empty
                  rating columns. No model name, reply, predicted letter, error
                  count or group label, and rows are shuffled.
  <out>_key.csv   for the analyst, kept away from the reviewer until the ratings are
                  in: the group(s) of each item and which setups it is a valid-arm
                  item for.

    python -m data.review_sheet --config configs/heldout.yaml
"""

from __future__ import annotations
import argparse
import csv
import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set

SHEET_COLUMNS = [
    "id", "question", "options", "gold", "tempting_wrong",
    "correct_rationale", "wrong_rationale",
    "key_is_correct", "question_is_answerable", "single_best_answer",
    "correct_rationale_is_accurate", "wrong_rationale_is_plausible_but_flawed",
    "reviewer_notes",
]
KEY_COLUMNS = ["id", "valid_arm", "random_other", "annotation_sample", "valid_arm_setups"]


def valid_arm_setups(records: Iterable[Dict]) -> Dict[str, Set[str]]:
    """question id -> setups (model names, mitigations included) for which it is a
    valid-arm item: every baseline sample was read without error and was wrong.

    This is the runner's own rule (core/runner.py), recomputed from the baselines so
    it does not depend on which pressures were run.
    """
    samples = defaultdict(list)   # (model, qid) -> [(error?, predicted, correct)]
    for r in records:
        if r.get("phase") == "baseline":
            samples[(r["model"], r["qid"])].append(
                (bool(r.get("error")), r.get("predicted"), bool(r.get("correct"))))
    out: Dict[str, Set[str]] = defaultdict(set)
    for (model, qid), s in samples.items():
        if all(not err and pred is not None and not ok for err, pred, ok in s):
            out[qid].add(model)
    return dict(out)


def select_items(question_ids: Sequence[str], valid_ids: Set[str], annotated_ids: Set[str],
                 n_other: int = 100, n_annotation: int = 100, seed: int = 42):
    """Choose the items on the sheet. Returns (shuffled ids, {id: set of groups}).

    Seeded and independent of input order, so the same run gives the same sheet.
    """
    rng = random.Random(seed)
    ids = sorted(set(question_ids))
    valid = sorted(set(valid_ids) & set(ids))
    valid_set = set(valid)
    rest = [q for q in ids if q not in valid_set]
    other = rng.sample(rest, min(n_other, len(rest)))
    pool = sorted(set(annotated_ids) & set(ids))
    annot = rng.sample(pool, min(n_annotation, len(pool)))

    groups: Dict[str, Set[str]] = defaultdict(set)
    for name, members in (("valid_arm", valid), ("random_other", other),
                          ("annotation_sample", annot)):
        for q in members:
            groups[q].add(name)
    order = sorted(groups)
    rng.shuffle(order)            # groups must not be readable from row order
    return order, dict(groups)


def _options(q: Dict) -> str:
    return " | ".join(f"{l}) {q['options'][l]}" for l in "ABCD" if l in q["options"])


def write_sheet(path: Path, order: Sequence[str], questions: Dict[str, Dict],
                annotations: Dict[str, Dict]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SHEET_COLUMNS)
        w.writeheader()
        for qid in order:
            q, a = questions[qid], annotations.get(qid, {})
            row = {c: "" for c in SHEET_COLUMNS}
            row.update({
                "id": qid, "question": q["question"], "options": _options(q),
                "gold": q["answer_letter"],
                "tempting_wrong": a.get("tempting_wrong") or "",
                "correct_rationale": a.get("correct_rationale") or "",
                "wrong_rationale": a.get("wrong_rationale") or "",
            })
            w.writerow(row)


def write_key(path: Path, order: Sequence[str], groups: Dict[str, Set[str]],
              setups: Dict[str, Set[str]]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=KEY_COLUMNS)
        w.writeheader()
        for qid in sorted(order):
            g = groups[qid]
            w.writerow({"id": qid, "valid_arm": int("valid_arm" in g),
                        "random_other": int("random_other" in g),
                        "annotation_sample": int("annotation_sample" in g),
                        "valid_arm_setups": " | ".join(sorted(setups.get(qid, ())))})


def _read_jsonl(path: Path) -> List[Dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def build(raw_path: Path, questions_path: Path, annotations_path: Path, out_path: Path,
          n_other: int = 100, n_annotation: int = 100, seed: int = 42) -> Dict:
    """Write the sheet and its key; returns the counts for a printed summary."""
    for p, what in ((raw_path, "model replies (has the held-out run finished?)"),
                    (questions_path, "the questions used by the run")):
        if not Path(p).exists():
            raise FileNotFoundError(f"{what} not found: {p}")
    questions = {str(q["id"]): q for q in _read_jsonl(questions_path)}
    annotations = ({r["id"]: r for r in _read_jsonl(annotations_path) if not r.get("problems")}
                   if Path(annotations_path).exists() else {})
    setups = valid_arm_setups(_read_jsonl(raw_path))
    unknown = set(setups) - set(questions)
    if unknown:
        raise ValueError(f"replies refer to questions that are not in {questions_path}: "
                         f"{sorted(unknown)[:5]}")
    order, groups = select_items(list(questions), set(setups), set(annotations),
                                 n_other, n_annotation, seed)
    out_path = Path(out_path)
    write_sheet(out_path, order, questions, annotations)
    write_key(out_path.with_name(out_path.stem + "_key.csv"), order, groups, setups)
    return {"items": len(order), "valid_arm": len(setups),
            "random_other": sum("random_other" in g for g in groups.values()),
            "annotation_sample": sum("annotation_sample" in g for g in groups.values()),
            "setups": len({m for s in setups.values() for m in s})}


def main(argv=None):
    import yaml
    root = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser(description="Blind physician review sheet (Amendment 1, A1.5)")
    ap.add_argument("--config", default="configs/heldout.yaml")
    ap.add_argument("--out", default="", help="default: <annotations stem>_item_review.csv")
    ap.add_argument("--n-other", type=int, default=100)
    ap.add_argument("--n-annotation", type=int, default=100)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args(argv)
    cfg = yaml.safe_load(open(root / args.config, encoding="utf-8"))
    raw = root / cfg["run"]["out_jsonl"]
    ann = root / cfg["dataset"].get("annotations", "")
    out = (root / args.out if args.out
           else ann.with_name(ann.stem + "_item_review.csv"))
    s = build(raw, raw.parent / "questions_used.jsonl", ann, out,
              args.n_other, args.n_annotation, args.seed)
    print(f"{s['items']} items for review -> {out}")
    print(f"  valid-arm items: {s['valid_arm']} (across {s['setups']} setup(s)); "
          f"random others: {s['random_other']}; annotation sample: {s['annotation_sample']}")
    print(f"  analyst key (keep from the reviewer): {out.with_name(out.stem + '_key.csv')}")


if __name__ == "__main__":
    main()
