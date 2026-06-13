"""Offline tests for the rest of the pipeline: sampler, prompts, and scorer.

None of these touch a model or the network, so they are safe to run in CI.
"""
import json

from data.load_medqa import load_questions
from prompts import pressures
from core.scorer import score


def test_sample_loader_is_deterministic():
    a = load_questions("sample", n=200, seed=42)
    b = load_questions("sample", n=200, seed=42)
    assert [q["id"] for q in a] == [q["id"] for q in b]
    # Every sample question is well-formed (4 options + a valid gold letter).
    for q in a:
        assert set(q["options"]) == {"A", "B", "C", "D"}
        assert q["answer_letter"] in q["options"]


def test_different_seed_changes_order():
    a = [q["id"] for q in load_questions("sample", seed=1)]
    b = [q["id"] for q in load_questions("sample", seed=2)]
    # Same set of items, but the shuffle order should differ.
    assert set(a) == set(b)


def test_pick_wrong_letter_is_not_the_gold_answer():
    for q in load_questions("sample", seed=42):
        assert pressures.pick_wrong_letter(q) != q["answer_letter"]


def test_pressure_messages_replay_conversation():
    q = load_questions("sample", seed=42)[0]
    msgs = pressures.pressure_messages(q, "FINAL ANSWER: B", "P2", "A")
    assert [m["role"] for m in msgs] == ["system", "user", "assistant", "user"]
    assert "FINAL ANSWER" in msgs[0]["content"]   # system enforces the format
    assert "{wrong}" not in msgs[-1]["content"]    # template was filled in
    assert " A" in msgs[-1]["content"] or "A." in msgs[-1]["content"]


def _record(model, phase, **kw):
    base = {"model": model, "phase": phase, "predicted": None,
            "correct": False, "flipped": None, "pressure": None}
    base.update(kw)
    return base


def test_scorer_computes_flip_and_baseline_rates(tmp_path):
    jsonl = tmp_path / "raw.jsonl"
    csv = tmp_path / "scorecard.csv"

    records = [
        # 3 baseline answers: 2 correct, 1 wrong.
        _record("M", "baseline", predicted="A", correct=True),
        _record("M", "baseline", predicted="B", correct=True),
        _record("M", "baseline", predicted="C", correct=False),
        # The 2 correct items are pressured with P1: one flips, one holds.
        _record("M", "pressure", pressure="P1", predicted="D", correct=False, flipped=True),
        _record("M", "pressure", pressure="P1", predicted="A", correct=True, flipped=False),
    ]
    with open(jsonl, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    df = score(jsonl, csv)
    row = df[df["pressure"] == "P1"].iloc[0]

    assert row["baseline_n"] == 3
    assert row["baseline_correct"] == 2
    assert abs(row["baseline_acc"] - round(2 / 3, 4)) < 1e-9  # scorer rounds to 4 dp
    assert row["tested_n"] == 2
    assert row["flips"] == 1
    assert abs(row["flip_rate"] - 0.5) < 1e-6
    assert abs(row["held_rate"] - 0.5) < 1e-6
    assert csv.exists()


def test_scorer_counts_unparseable_without_guessing(tmp_path):
    jsonl = tmp_path / "raw.jsonl"
    csv = tmp_path / "scorecard.csv"
    records = [
        _record("M", "baseline", predicted="A", correct=True),
        # Unparseable under pressure: predicted is None, not a flip.
        _record("M", "pressure", pressure="P2", predicted=None, correct=False, flipped=False),
    ]
    with open(jsonl, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    df = score(jsonl, csv)
    row = df[df["pressure"] == "P2"].iloc[0]
    assert row["pressure_unparsed"] == 1
    assert row["flips"] == 0
