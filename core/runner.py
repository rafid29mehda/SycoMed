"""
core/runner.py
--------------
The experiment loop. For one model over a list of questions:

  For each question:
    1. Ask the BASELINE (no pressure). Parse the letter.
    2. Record whether baseline is correct.
    3. If baseline is CORRECT, apply each chosen pressure (P0..P4) in a fresh
       replayed conversation, parse the new letter, and record whether it FLIPPED.

We only apply pressure to questions the model first got RIGHT, because you can
only measure "flipping a correct answer" on answers that started correct.

Every interaction is written to outputs/raw_responses.jsonl so the run is fully
auditable and reproducible (and so you can pull qualitative examples later).
"""

from __future__ import annotations
import json
import time
from typing import List, Dict
from pathlib import Path

from prompts import pressures
from core.parser import extract_letter


def run_model(adapter, questions: List[Dict], pressure_ids: List[str],
              out_path: Path, sleep: float = 0.0) -> None:
    """Run one model over all questions and append results to out_path (jsonl)."""
    with open(out_path, "a", encoding="utf-8") as f:
        for i, q in enumerate(questions, 1):
            qid = q.get("id", str(i))

            # ---- 1. Baseline ----
            base_msgs = pressures.baseline_messages(q)
            try:
                base_reply = adapter.ask(base_msgs)
                base_error = None
            except Exception as e:  # network/model error: log and continue
                base_reply, base_error = "", str(e)

            base_letter, base_method = extract_letter(base_reply)
            base_correct = (base_letter == q["answer_letter"])

            record = {
                "model": adapter.name,
                "qid": qid,
                "phase": "baseline",
                "pressure": None,
                "gold": q["answer_letter"],
                "predicted": base_letter,
                "parse_method": base_method,
                "correct": base_correct,
                "flipped": None,
                "error": base_error,
                "reply": base_reply,
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()

            # Only pressure-test answers that started correct.
            if not base_correct:
                if sleep:
                    time.sleep(sleep)
                continue

            wrong = pressures.pick_wrong_letter(q)

            # ---- 2. Pressure turns ----
            for pid in pressure_ids:
                p_msgs = pressures.pressure_messages(q, base_reply, pid, wrong)
                try:
                    p_reply = adapter.ask(p_msgs)
                    p_error = None
                except Exception as e:
                    p_reply, p_error = "", str(e)

                p_letter, p_method = extract_letter(p_reply)
                p_correct = (p_letter == q["answer_letter"])
                # A flip = was correct at baseline, now NOT correct after pressure.
                flipped = (p_letter is not None) and (not p_correct)

                rec = {
                    "model": adapter.name,
                    "qid": qid,
                    "phase": "pressure",
                    "pressure": pid,
                    "pushed_wrong": wrong,
                    "gold": q["answer_letter"],
                    "predicted": p_letter,
                    "parse_method": p_method,
                    "correct": p_correct,
                    "flipped": flipped,
                    "error": p_error,
                    "reply": p_reply,
                }
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()

                if sleep:
                    time.sleep(sleep)

            if i % 10 == 0:
                print(f"  [{adapter.name}] processed {i}/{len(questions)} questions")
