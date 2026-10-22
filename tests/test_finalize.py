"""Tests for the 'finalize the tool' pass: stable baselines (k samples),
resumable runs, run metadata, call estimates, plots.
"""
import json
import re

import pytest

from core.runner import run_model
from core.scorer import score
from prompts import pressures


def _q(i, gold="B"):
    return {"id": f"q{i}", "question": f"Question text {i}?", "answer_letter": gold,
            "options": {"A": "alpha", "B": "beta", "C": "gamma", "D": "delta"}}


def _records(path):
    return [json.loads(l) for l in open(path)]


class Scripted:
    """Baseline answers per question are a list consumed one call at a time."""
    name = "S"

    def __init__(self, baselines, challenge="B"):
        self.baselines = {k: list(v) for k, v in baselines.items()}
        self.challenge = challenge
        self.calls = 0

    def ask(self, messages):
        self.calls += 1
        qid = re.search(r"Question text (\d+)\?", json.dumps(messages)).group(1)
        if len(messages) == 2:
            seq = self.baselines[qid]
            return f"FINAL ANSWER: {seq.pop(0) if len(seq) > 1 else seq[0]}"
        return f"FINAL ANSWER: {self.challenge}"


# ---------- stable baselines ----------

def test_arms_need_a_stable_baseline_across_samples(tmp_path):
    qs = [_q(1), _q(2), _q(3)]
    model = Scripted({"1": ["B", "B", "B"],      # known
                      "2": ["C", "C", "C"],      # stably wrong
                      "3": ["B", "C", "B"]})     # unstable -> no arm
    out = tmp_path / "raw.jsonl"
    run_model(model, qs, ["P1"], out, baseline_samples=3)
    recs = _records(out)
    base = [r for r in recs if r["phase"] == "baseline"]
    assert len(base) == 9 and sorted({r["sample"] for r in base}) == [0, 1, 2]
    arms = {r["qid"]: r["arm"] for r in recs if r["phase"] == "pressure"}
    assert arms == {"q1": "invalid", "q2": "valid"}          # q3 excluded


def test_scorer_reports_unstable_baselines(tmp_path):
    qs = [_q(1), _q(2), _q(3)]
    model = Scripted({"1": ["B"], "2": ["C"], "3": ["B", "C", "B"]})
    raw = tmp_path / "raw.jsonl"
    run_model(model, qs, ["P1"], raw, baseline_samples=3)
    df = score(raw, tmp_path / "s.csv")
    row = df.iloc[0]
    assert row["baseline_questions"] == 3 and row["baseline_unstable"] == 1
    assert row["baseline_n"] == 9                     # every sample is an observation
    assert row["baseline_acc"] == pytest.approx(5 / 9, abs=1e-3)


def test_single_sample_mode_is_unchanged(tmp_path):
    out = tmp_path / "raw.jsonl"
    run_model(Scripted({"1": ["B"]}), [_q(1)], ["P1"], out)
    assert len([r for r in _records(out) if r["phase"] == "baseline"]) == 1


# ---------- resume ----------

class Flaky(Scripted):
    def __init__(self, *a, bad_qid=None, **k):
        super().__init__(*a, **k)
        self.bad_qid = bad_qid

    def ask(self, messages):
        qid = re.search(r"Question text (\d+)\?", json.dumps(messages)).group(1)
        if qid == self.bad_qid:
            self.calls += 1
            raise RuntimeError("429")
        return super().ask(messages)


def test_resume_skips_finished_questions_and_retries_failed_ones(tmp_path):
    qs = [_q(1), _q(2)]
    out = tmp_path / "raw.jsonl"
    first = Flaky({"1": ["B"], "2": ["B"]}, bad_qid="2")
    run_model(first, qs, ["P1"], out)
    assert any(r["error"] for r in _records(out))

    second = Scripted({"1": ["B"], "2": ["B"]})
    run_model(second, qs, ["P1"], out, resume=True)
    recs = _records(out)
    assert not any(r["error"] for r in recs)
    assert second.calls == 2                       # only q2 (baseline + one challenge)
    by_q = {}
    for r in recs:
        by_q.setdefault(r["qid"], []).append(r)
    assert len(by_q["q1"]) == 2 and len(by_q["q2"]) == 2   # no duplicates


def test_aborted_run_leaves_no_half_finished_questions(tmp_path):
    class DiesAfter(Scripted):
        def ask(self, messages):
            self.calls += 1
            if self.calls > 3:
                raise RuntimeError("down")
            return super().ask(messages)
    out = tmp_path / "raw.jsonl"
    qs = [_q(i) for i in range(1, 6)]
    run_model(DiesAfter({str(i): ["B"] for i in range(1, 6)}), qs,
              ["P1", "P2", "P3"], out, max_consecutive_errors=2)
    for qid in {r["qid"] for r in _records(out)}:
        mine = [r for r in _records(out) if r["qid"] == qid]
        assert len([r for r in mine if r["phase"] == "pressure"]) == 3 or any(r["error"] for r in mine)


# ---------- metadata & estimates ----------

def test_estimate_calls_counts_samples_and_structures():
    from core.meta import estimate_calls
    cfg = {"pressures": ["P0", "P1", "P2"],
           "run": {"structures": ["followup", "preemptive", "prefilled"], "baseline_samples": 3},
           "models": [{"name": "m1"}, {"name": "m2"}]}
    est = estimate_calls(cfg, n_questions=10)
    # per question: 3 baseline + followup 3 + preemptive 2 (no P0) + prefilled 2x3 = 14 (upper bound)
    assert est["per_question"] == 14 and est["per_model"] == 140 and est["total"] == 280


def test_collect_meta_has_provenance_and_no_secrets(monkeypatch):
    from core.meta import collect_meta
    monkeypatch.setenv("OPENAI_API_KEY", "sk-secret-should-never-appear")
    class A:
        name = "m"; model_id = "gpt-x"; seen_models = {"gpt-x-2026-01-01"}
    cfg = {"dataset": {"source": "sample"}, "models": [{"name": "m", "api_key_env": "OPENAI_API_KEY"}],
           "run": {}, "pressures": ["P1"]}
    meta = collect_meta(cfg, [A()], [_q(1)])
    text = json.dumps(meta)
    assert "sk-secret" not in text
    for key in ("started_utc", "python", "packages", "git", "dataset", "config", "models"):
        assert key in meta
    assert meta["models"][0]["resolved_model_ids"] == ["gpt-x-2026-01-01"]
    assert meta["dataset"]["n_questions"] == 1 and len(meta["dataset"]["question_ids_sha256"]) == 64


# ---------- plots ----------

def test_plots_handle_multiple_structures(tmp_path):
    import pandas as pd
    from core.plots import make_plots
    rows = []
    for model in ("A", "B"):
        for structure in ("followup", "preemptive"):
            for p in ("P1", "P2"):
                rows.append({"model": model, "structure": structure, "pressure": p,
                             "capitulation": 0.2, "cap_ci_low": 0.1, "cap_ci_high": 0.3,
                             "update_rate": 0.7, "upd_ci_low": 0.5, "upd_ci_high": 0.8,
                             "discrimination": 0.5, "disc_ci_low": 0.3, "disc_ci_high": 0.7,
                             "flip_rate": 0.2})
    csv = tmp_path / "s.csv"
    pd.DataFrame(rows).to_csv(csv, index=False)
    make_plots(csv, tmp_path / "plots")
    assert (tmp_path / "plots" / "capitulation_vs_update.png").exists()
    assert (tmp_path / "plots" / "discrimination.png").exists()


def test_resumed_run_merges_metadata_instead_of_overwriting():
    from core.meta import merge_meta
    old = {"started_utc": "2026-10-09T10:00:00+00:00",
           "models": [{"name": "m", "model_id": "x", "resolved_model_ids": ["x-2026-01-01"]}]}
    new = {"started_utc": "2026-10-09T18:00:00+00:00",
           "models": [{"name": "m", "model_id": "x", "resolved_model_ids": []}]}
    merged = merge_meta(old, new)
    assert merged["started_utc"] == "2026-10-09T10:00:00+00:00"
    assert merged["resumed_utc"] == ["2026-10-09T18:00:00+00:00"]
    assert merged["models"][0]["resolved_model_ids"] == ["x-2026-01-01"]
    # and a second resume keeps appending
    again = merge_meta(merged, {"started_utc": "2026-10-10T09:00:00+00:00", "models": new["models"]})
    assert len(again["resumed_utc"]) == 2


# ---------- dev / held-out split ----------

def test_skip_gives_a_disjoint_heldout_slice():
    from data.load_medqa import load_questions, SAMPLE
    base = [q["id"] for q in load_questions("sample", n=0, seed=7)]       # whole shuffled set
    dev = [q["id"] for q in load_questions("sample", n=2, seed=7)]
    held = [q["id"] for q in load_questions("sample", n=2, seed=7, skip=2)]
    assert dev == base[:2] and held == base[2:4]
    assert not set(dev) & set(held)
    assert len(load_questions("sample", n=0, seed=7, skip=len(SAMPLE) + 5)) == 0
