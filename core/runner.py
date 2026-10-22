"""
core/runner.py
--------------
The experiment loop (docs/PROTOCOL.md). For one model over a list of questions:

  For each question:
    1. Ask the BASELINE (no pressure). Parse the letter.
    2. Assign an ARM from the model's own baseline answer:
         correct -> "invalid" arm: the user claims a WRONG letter
         wrong   -> "valid"   arm: the user claims the CORRECT letter
       (a baseline that errored or cannot be parsed gets no arm: we do not
       know what the model believed, so we do not challenge it.)
    3. Apply each chosen pressure (P0..P4), for each chosen structure, in a
       fresh conversation, parse the new letter, and record whether the model
       adopted the claim.

Matched wording across arms is what lets us separate "responds to the truth of
the claim" from "responds to the social force of the claim".

Every interaction is written to a jsonl file so the run is fully auditable and
reproducible (and so you can pull qualitative examples later).
"""

from __future__ import annotations
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Optional, Sequence
from pathlib import Path

from prompts import pressures
from core.parser import extract_letter


class _Streak:
    """Shared count of consecutive failed calls; trips `stop` at the limit."""

    def __init__(self, limit: int):
        self.limit, self.n, self.last, self.tripped_n = limit, 0, None, 0
        self.lock, self.stop = threading.Lock(), threading.Event()

    def record(self, error) -> None:
        with self.lock:
            self.n = self.n + 1 if error else 0
            if error:
                self.last = error
            if self.n >= self.limit and not self.stop.is_set():
                self.tripped_n = self.n
                self.stop.set()


def _run_question(adapter, q, i, pressure_ids, structures, system_variant,
                  strict_parse, sleep, streak, baseline_samples=1) -> Optional[List[Dict]]:
    """All records for one question (baseline plus challenges), in order.

    Returns None if the run was told to stop part-way, so a half-finished
    question is never written (and a resumed run redoes it from scratch).
    """
    recs: List[Dict] = []
    qid = q.get("id", str(i))
    gold = q["answer_letter"]

    def call(msgs):
        if streak.stop.is_set():
            return None, "skipped"
        try:
            reply, err = adapter.ask(msgs), None
        except Exception as e:  # network/model error: log and continue
            reply, err = "", str(e)
        streak.record(err)
        if sleep:
            time.sleep(sleep)
        return reply, err

    # ---- 1. Baseline: k independent samples of the same unpressured question ----
    # One sample is not a stable measurement of what the model "knows": at
    # temperature 0 the answer still changes between identical calls for ~10%
    # of questions. We keep only questions that are answered the same way,
    # correctly or wrongly, on every sample.
    base_msgs = pressures.baseline_messages(q, system_variant)
    samples = []
    for k in range(max(1, baseline_samples)):
        reply, err = call(base_msgs)
        if err == "skipped":
            return None
        letter, method = extract_letter(reply, strict=strict_parse)
        samples.append((reply, err, letter))
        recs.append({
            "model": adapter.name, "qid": qid, "phase": "baseline", "sample": k,
            "system_variant": system_variant, "pressure": None, "gold": gold,
            "predicted": letter, "parse_method": method,
            "correct": letter == gold, "flipped": None, "error": err,
            "reply": reply,
        })

    base_reply, base_error, base_letter = samples[0]
    letters = [x[2] for x in samples]
    # No arm unless every sample was readable and they agree on correctness.
    if any(x[1] for x in samples) or any(l is None for l in letters):
        return recs
    correct_flags = {l == gold for l in letters}
    if len(correct_flags) != 1:
        return recs                      # unstable item: excluded from both arms
    base_correct = correct_flags.pop()

    # ---- 2. Arm ----
    if base_correct:
        arm, claim = "invalid", pressures.pick_wrong_claim(q)
    else:
        arm, claim = "valid", gold

    def challenge(structure, pid, arm_, prior, claim_):
        """Ask one challenge; returns False if the run was told to stop."""
        variant = pressures.pick_variant(q, pid, structure)
        claim_letter = None if pid == "P0" else claim_
        rationale = pressures.claim_rationale(q, claim_letter) if pid == "P6" else None
        if structure == "preemptive":
            msgs = pressures.preemptive_messages(q, pid, claim_letter, variant, system_variant,
                                                 rationale=rationale)
        else:
            reply = pressures.planted_reply(prior) if structure == "prefilled" else base_reply
            msgs = pressures.pressure_messages(q, reply, pid, claim_letter, variant, system_variant,
                                               rationale=rationale)
        p_reply, p_error = call(msgs)
        if p_error == "skipped":
            return False
        p_letter, p_method = extract_letter(p_reply, strict=strict_parse)
        p_correct = (p_letter == gold)
        # followed = adopted the user's claim (None for the claim-free
        # control or a failed call). flipped = legacy: a readable
        # answer that is not the gold letter.
        followed = None if (p_error or claim_letter is None) else (p_letter == claim_letter)
        flipped = None if p_error else ((p_letter is not None) and (not p_correct))
        rec = {
            "model": adapter.name, "qid": qid, "phase": "pressure",
            "arm": arm_, "structure": structure, "variant": variant,
            "system_variant": system_variant, "pressure": pid,
            "pushed": claim_letter, "gold": gold,
            "baseline_predicted": base_letter,
            "predicted": p_letter, "parse_method": p_method,
            "correct": p_correct, "followed": followed,
            "flipped": flipped, "error": p_error, "reply": p_reply,
            "claim_kind": ("none" if claim_letter is None else "gold" if claim_letter == gold
                           else "tempting" if q.get("tempting_wrong") == claim_letter else "arbitrary"),
        }
        if structure == "prefilled":
            rec["prior"] = prior
        recs.append(rec)
        return True

    # ---- 3. Challenges ----
    for structure in structures:
        for pid in pressure_ids:
            if pressures.n_variants(pid, structure) == 0:
                continue            # e.g. P0 has no preemptive form
            if pid == "P6" and pressures.claim_rationale(q, claim if structure != "prefilled" else gold) is None:
                continue            # reasoned claims need this question's annotation
            if structure == "prefilled":
                if not base_correct:
                    continue        # only questions the model demonstrably knows
                wrong = pressures.pick_wrong_claim(q)
                # Same wrong letter on both sides: invalid = gold answer challenged by
                # the wrong claim; valid = the wrong answer challenged by the gold claim.
                for arm_, prior, claim_ in (("invalid", gold, wrong), ("valid", wrong, gold)):
                    if not challenge(structure, pid, arm_, prior, claim_):
                        return None
            elif not challenge(structure, pid, arm, None, claim):
                return None
    return recs


def _load_complete(out_path: Path, model: str):
    """Keep only questions of `model` that finished without errors.

    Rewrites the file without the unfinished ones (and returns the finished
    question ids), so resuming never leaves duplicates behind.
    """
    if not Path(out_path).exists():
        return set()
    by_q: Dict = {}
    other: List[str] = []
    with open(out_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            if r["model"] == model:
                by_q.setdefault(r["qid"], []).append(line)
            else:
                other.append(line)
    done = {qid for qid, lines in by_q.items()
            if not any(json.loads(l).get("error") for l in lines)}
    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(other)
        for qid in done:
            f.writelines(by_q[qid])
    return done


def run_model(adapter, questions: List[Dict], pressure_ids: List[str],
              out_path: Path, sleep: float = 0.0,
              max_consecutive_errors: int = 8, strict_parse: bool = True,
              structures: Sequence[str] = ("followup",),
              system_variant: str = "default", workers: int = 1,
              baseline_samples: int = 1, resume: bool = False) -> None:
    """Run one model over all questions and append results to out_path (jsonl).

    A call that raises is logged with its error and NOT scored as a wrong
    answer (the scorer excludes errored records). If `max_consecutive_errors`
    calls in a row fail (bad key, exhausted quota, model removed), the model is
    abandoned so the run does not burn time on a dead endpoint; a question that
    was cut off by the abort is not written at all.

    strict_parse (default): only a 'FINAL ANSWER: X' line counts as an answer.
    Anything else is recorded as unparsed and is never scored as a flip.

    structures: any of "followup" (answer, then challenged), "preemptive"
    (claim stated in the first message) and "prefilled" (planted prior answer,
    both arms on every known question). system_variant: "default" or a
    mitigation prompt from prompts/pressures.py. workers > 1 processes that many
    questions at once (mind the provider's rate limits); results are identical.

    baseline_samples: number of unpressured answers per question; a question
    enters an arm only if all samples agree on correctness (stable knowledge).

    resume: keep this model's finished, error-free questions already in
    out_path and only (re)run the rest. Needed for free-tier daily quotas.
    """
    done = _load_complete(out_path, adapter.name) if resume else set()
    todo = [(i, q) for i, q in enumerate(questions, 1)
            if str(q.get("id", i)) not in done]
    streak = _Streak(max_consecutive_errors)
    with open(out_path, "a", encoding="utf-8") as f, \
            ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = [pool.submit(_run_question, adapter, q, i, pressure_ids, structures,
                               system_variant, strict_parse, sleep, streak, baseline_samples)
                   for i, q in todo]
        for n, fut in enumerate(futures, 1):
            for rec in fut.result() or []:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            if n % 10 == 0 and not streak.stop.is_set():
                print(f"  [{adapter.name}] processed {n}/{len(todo)} questions")
    if streak.stop.is_set():
        print(f"  [{adapter.name}] ABORTED after {streak.tripped_n} consecutive errors: {streak.last}")
