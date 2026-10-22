"""Tests for reasoned claims: annotation generation/validation, the P6 pressure,
and how the runner uses tempting wrong options and matched rationales.
"""
import json
import re

import pytest

from data import annotate
from prompts import pressures
from core.runner import run_model


def _q(i, gold="B", **extra):
    q = {"id": f"q{i}", "question": f"Question text {i}?", "answer_letter": gold,
         "options": {"A": "alpha", "B": "beta", "C": "gamma", "D": "delta"}}
    q.update(extra)
    return q


RC = "The lesion spares the lateral fibres, which explains the preserved sensation."
RW = "The pattern of weakness localises to the distal nerve, so a peripheral cause fits best."
GOOD = {"tempting_wrong": "C", "correct_rationale": RC, "wrong_rationale": RW}


def _records(path):
    return [json.loads(l) for l in open(path)]


# ---------- annotation prompt / parse / validate ----------

def test_prompt_contains_question_options_and_gold():
    p = annotate.annotation_prompt(_q(1))
    assert "Question text 1?" in p and "B) beta" in p
    assert "correct answer is B" in p and "JSON" in p


def test_parse_annotation_tolerates_fences_and_prose():
    raw = 'Sure! ```json\n{"tempting_wrong": "C", "correct_rationale": "x y", "wrong_rationale": "z"}\n``` done'
    assert annotate.parse_annotation(raw)["tempting_wrong"] == "C"
    assert annotate.parse_annotation("no json here") is None


def test_validate_accepts_a_good_annotation():
    assert annotate.validate_annotation(_q(1), GOOD) == []


@pytest.mark.parametrize("change, fragment", [
    ({"tempting_wrong": "B"}, "gold"),
    ({"tempting_wrong": "Z"}, "option"),
    ({"correct_rationale": "too short"}, "length"),
    ({"wrong_rationale": "word " * 200}, "length"),
    ({"correct_rationale": "Option A is wrong because the lesion spares the lateral fibres here."}, "letter"),
    ({"wrong_rationale": "word " * 40}, "ratio"),
])
def test_validate_flags_problems(change, fragment):
    problems = annotate.validate_annotation(_q(1), {**GOOD, **change})
    assert any(fragment in p for p in problems), problems


def test_missing_keys_are_flagged():
    assert annotate.validate_annotation(_q(1), {"tempting_wrong": "C"})


class Gen:
    name = "gen"
    model_id = "gen-1"

    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = 0

    def ask(self, messages):
        self.calls += 1
        return self.replies.pop(0) if len(self.replies) > 1 else self.replies[0]


def test_annotate_retries_then_records_failure_and_resumes(tmp_path):
    out = tmp_path / "ann.jsonl"
    good = json.dumps(GOOD)
    gen = Gen(["not json", good])                    # first try fails, retry works
    annotate.annotate_questions([_q(1)], gen, out, max_attempts=3)
    rec = _records(out)[0]
    assert rec["id"] == "q1" and rec["tempting_wrong"] == "C" and gen.calls == 2
    assert rec["generator"] == "gen-1" and rec["problems"] == []

    gen2 = Gen(["still not json"])
    annotate.annotate_questions([_q(1), _q(2)], gen2, out, max_attempts=2, resume=True)
    recs = {r["id"]: r for r in _records(out)}
    assert gen2.calls == 2                           # q1 was skipped, q2 tried twice
    assert recs["q2"]["problems"] and recs["q2"].get("tempting_wrong") is None


def test_attach_only_uses_clean_annotations(tmp_path):
    out = tmp_path / "ann.jsonl"
    rows = [{"id": "q1", **GOOD, "problems": []},
            {"id": "q2", **GOOD, "problems": ["length"]}]
    out.write_text("\n".join(json.dumps(r) for r in rows))
    qs = [_q(1), _q(2), _q(3)]
    assert annotate.attach_annotations(qs, out) == 1
    assert qs[0]["tempting_wrong"] == "C" and qs[0]["rationale_wrong"] == RW
    assert "tempting_wrong" not in qs[1] and "tempting_wrong" not in qs[2]


def test_review_csv_has_the_columns_a_physician_needs(tmp_path):
    import csv
    ann = tmp_path / "ann.jsonl"
    ann.write_text(json.dumps({"id": "q1", **GOOD, "problems": []}))
    out = tmp_path / "review.csv"
    annotate.export_review_csv([_q(1)], ann, out)
    row = next(csv.DictReader(open(out)))
    for col in ("id", "question", "options", "gold", "tempting_wrong", "correct_rationale",
                "wrong_rationale", "correct_rationale_is_accurate", "wrong_rationale_is_plausible_but_flawed",
                "reviewer_notes"):
        assert col in row


# ---------- P6 wording and claim helpers ----------

def test_p6_has_three_wordings_per_structure():
    assert pressures.n_variants("P6", "followup") == 3
    assert pressures.n_variants("P6", "preemptive") == 3


@pytest.mark.parametrize("variant", [0, 1, 2])
def test_p6_followup_contains_claim_and_rationale(variant):
    msgs = pressures.pressure_messages(_q(1), "FINAL ANSWER: B", "P6", "C", variant=variant,
                                       rationale="the lesion spares the lateral fibres.")
    text = msgs[-1]["content"]
    assert "lateral fibres" in text and set(re.findall(r"\b[A-D]\b", text)) == {"C"}


@pytest.mark.parametrize("variant", [0, 1, 2])
def test_p6_preemptive_contains_claim_and_rationale(variant):
    msgs = pressures.preemptive_messages(_q(1), "P6", "C", variant=variant,
                                         rationale="the lesion spares the lateral fibres.")
    assert "lateral fibres" in msgs[1]["content"].split("\n\n")[0]


def test_p6_requires_a_rationale():
    with pytest.raises(ValueError):
        pressures.pressure_messages(_q(1), "FINAL ANSWER: B", "P6", "C", variant=0)


def test_wrong_claim_is_the_tempting_option_when_annotated():
    q = _q(1, tempting_wrong="D", rationale_wrong=RW, rationale_correct=RC)
    assert pressures.pick_wrong_claim(q) == "D"
    plain = _q(2)
    assert pressures.pick_wrong_claim(plain) == pressures.pick_wrong_letter(plain)
    bad = _q(3, tempting_wrong="B")                 # equals gold: ignore it
    assert pressures.pick_wrong_claim(bad) != "B"


def test_rationale_matches_the_claimed_letter():
    q = _q(1, tempting_wrong="D", rationale_wrong=RW, rationale_correct=RC)
    assert pressures.claim_rationale(q, "B") == RC
    assert pressures.claim_rationale(q, "D") == RW
    assert pressures.claim_rationale(q, "A") is None
    assert pressures.claim_rationale(_q(2), "B") is None


# ---------- runner ----------

class Script:
    name = "Script"

    def __init__(self, base):
        self.base, self.seen = base, []

    def ask(self, messages):
        self.seen.append(messages)
        qid = re.search(r"Question text (\d+)\?", json.dumps(messages)).group(1)
        return f"FINAL ANSWER: {self.base[qid] if len(messages) == 2 else 'B'}"


def test_runner_uses_tempting_claim_and_matched_rationales(tmp_path):
    qs = [_q(1, tempting_wrong="D", rationale_wrong=RW, rationale_correct=RC),
          _q(2, tempting_wrong="D", rationale_wrong=RW, rationale_correct=RC)]
    model = Script({"1": "B", "2": "C"})            # q1 known, q2 stably wrong
    out = tmp_path / "raw.jsonl"
    run_model(model, qs, ["P1", "P6"], out, baseline_samples=2)
    ch = {(r["qid"], r["pressure"]): r for r in _records(out) if r["phase"] == "pressure"}
    assert ch[("q1", "P1")]["pushed"] == "D" and ch[("q1", "P1")]["claim_kind"] == "tempting"
    assert ch[("q2", "P1")]["pushed"] == "B" and ch[("q2", "P1")]["claim_kind"] == "gold"
    last = {m[-1]["content"] for m in model.seen if len(m) == 4}
    assert any("spares the lateral fibres" in t for t in last)      # valid arm: correct rationale
    assert any("peripheral cause" in t for t in last)               # invalid arm: flawed rationale
    assert ch[("q1", "P6")]["pushed"] == "D" and ch[("q2", "P6")]["pushed"] == "B"


def test_runner_skips_p6_for_unannotated_questions(tmp_path):
    out = tmp_path / "raw.jsonl"
    run_model(Script({"1": "B"}), [_q(1)], ["P1", "P6"], out)
    assert {r["pressure"] for r in _records(out) if r["phase"] == "pressure"} == {"P1"}


def test_meta_records_the_annotation_file_hash(tmp_path):
    from core.meta import collect_meta
    ann = tmp_path / "ann.jsonl"
    ann.write_text(json.dumps({"id": "q1", **GOOD, "problems": []}))
    cfg = {"dataset": {"source": "sample", "annotations": str(ann)}, "models": [], "run": {}, "pressures": []}
    meta = collect_meta(cfg, [], [_q(1)])
    assert len(meta["dataset"]["annotations_sha256"]) == 64
