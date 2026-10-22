"""Tests for the v2 protocol (docs/PROTOCOL.md): valid/invalid challenge arms,
wording variants, preemptive structure, mitigation prompts, discrimination
scoring and the paired statistics. All offline.
"""
import json
import re

import pytest

from prompts import pressures
from core.runner import run_model
from core.scorer import score, newcombe_diff
from core import stats


def _q(i, gold="B"):
    return {"id": f"q{i}", "question": f"Question text {i}?", "answer_letter": gold,
            "options": {"A": "alpha", "B": "beta", "C": "gamma", "D": "delta"}}


# ---------- prompts ----------

@pytest.mark.parametrize("pid", ["P1", "P2", "P3", "P5"])
def test_each_pressure_has_three_wordings_per_structure(pid):
    assert pressures.n_variants(pid, "followup") == 3
    assert pressures.n_variants(pid, "preemptive") == 3


def test_p0_has_no_preemptive_form():
    assert pressures.n_variants("P0", "preemptive") == 0


@pytest.mark.parametrize("pid", ["P1", "P2", "P3", "P4", "P5"])
@pytest.mark.parametrize("variant", [0, 1, 2])
def test_followup_wordings_mention_no_option_letter_but_the_claim(pid, variant):
    if variant >= pressures.n_variants(pid, "followup"):
        pytest.skip("fewer wordings")
    msgs = pressures.pressure_messages(_q(1), "FINAL ANSWER: B", pid, "C", variant=variant)
    letters = re.findall(r"\b[A-D]\b", msgs[-1]["content"])
    assert letters and set(letters) == {"C"}


def test_variant_choice_is_deterministic_and_balanced():
    ids = [pressures.pick_variant(_q(i), "P2", "followup") for i in range(300)]
    assert ids == [pressures.pick_variant(_q(i), "P2", "followup") for i in range(300)]
    assert set(ids) == {0, 1, 2}
    assert min(ids.count(v) for v in (0, 1, 2)) > 60


def test_preemptive_message_is_single_turn_with_claim_before_question():
    msgs = pressures.preemptive_messages(_q(1), "P2", "D", variant=0)
    assert [m["role"] for m in msgs] == ["system", "user"]
    body = msgs[1]["content"]
    assert body.index("D") < body.index("Question text 1?")
    assert "A) alpha" in body


def test_mitigation_prompts_keep_the_answer_format_and_differ():
    base = pressures.baseline_messages(_q(1))[0]["content"]
    for variant in ("evidence_first", "resolve_first"):
        sys_prompt = pressures.baseline_messages(_q(1), system_variant=variant)[0]["content"]
        assert sys_prompt != base
        assert "FINAL ANSWER: X" in sys_prompt
    with pytest.raises(KeyError):
        pressures.baseline_messages(_q(1), system_variant="nope")


# ---------- runner: arms ----------

class Script:
    """Fake model. Baseline answers come from `base`, challenge answers from
    `reply_to_claim(qid, claim)`; it records every message list it saw."""
    name = "Script"

    def __init__(self, base, reply_to_claim):
        self.base, self.reply_to_claim, self.seen = base, reply_to_claim, []

    @staticmethod
    def _qid(messages):
        return re.search(r"Question text (\d+)\?", json.dumps(messages)).group(1)

    def ask(self, messages):
        self.seen.append(messages)
        qid = self._qid(messages)
        user_turns = [m for m in messages if m["role"] == "user"]
        first = user_turns[0]["content"]
        is_preemptive = len(messages) == 2 and not first.startswith("Question text")
        if len(messages) == 2 and not is_preemptive:
            return f"FINAL ANSWER: {self.base[qid]}"
        if is_preemptive:
            claim = re.search(r"\b([A-D])\b", first.split("\n\n")[0])
        else:
            claim = re.search(r"\b([A-D])\b", messages[-1]["content"])
        return f"FINAL ANSWER: {self.reply_to_claim(qid, claim.group(1) if claim else None)}"


def _records(path):
    return [json.loads(l) for l in open(path)]


def test_arms_are_assigned_from_the_models_own_baseline(tmp_path):
    qs = [_q(1), _q(2), _q(3), _q(4)]
    base = {"1": "B", "2": "B", "3": "C", "4": "C"}          # 1,2 right; 3,4 wrong
    model = Script(base, lambda qid, claim: claim)            # always agrees
    out = tmp_path / "raw.jsonl"
    run_model(model, qs, ["P1"], out)
    ch = {r["qid"]: r for r in _records(out) if r["phase"] == "pressure"}
    assert {k: v["arm"] for k, v in ch.items()} == {"q1": "invalid", "q2": "invalid",
                                                     "q3": "valid", "q4": "valid"}
    assert ch["q1"]["pushed"] in {"A", "C", "D"}              # a wrong letter
    assert ch["q3"]["pushed"] == "B"                          # the gold letter
    assert all(r["followed"] for r in ch.values())            # it agreed every time
    assert ch["q3"]["structure"] == "followup" and ch["q3"]["variant"] in (0, 1, 2)


def test_unparsed_baseline_gets_no_challenge(tmp_path):
    class NoFinal(Script):
        def ask(self, messages):
            return "I am not sure." if len(messages) == 2 else "FINAL ANSWER: B"
    out = tmp_path / "raw.jsonl"
    run_model(NoFinal({}, None), [_q(1)], ["P1"], out)
    assert [r["phase"] for r in _records(out)] == ["baseline"]


def test_preemptive_structure_is_single_turn_and_skips_p0(tmp_path):
    out = tmp_path / "raw.jsonl"
    model = Script({"1": "B"}, lambda qid, claim: "B")
    run_model(model, [_q(1)], ["P0", "P2"], out, structures=("preemptive",))
    ch = [r for r in _records(out) if r["phase"] == "pressure"]
    assert [(r["pressure"], r["structure"]) for r in ch] == [("P2", "preemptive")]
    assert all(len(m) == 2 for m in model.seen)               # never a replayed chat


def test_p0_is_recorded_without_a_claim(tmp_path):
    out = tmp_path / "raw.jsonl"
    run_model(Script({"3": "C"}, lambda qid, claim: "B"), [_q(3)], ["P0"], out)
    r = [r for r in _records(out) if r["phase"] == "pressure"][0]
    assert r["arm"] == "valid" and r["pushed"] is None and r["followed"] is None
    assert r["correct"] is True        # it fixed itself on a plain recheck


def test_system_variant_reaches_the_model(tmp_path):
    out = tmp_path / "raw.jsonl"
    model = Script({"1": "B"}, lambda qid, claim: "B")
    run_model(model, [_q(1)], ["P1"], out, system_variant="evidence_first")
    expected = pressures.baseline_messages(_q(1), system_variant="evidence_first")[0]["content"]
    assert all(m[0]["content"] == expected for m in model.seen)


# ---------- scorer: discrimination ----------

def test_scorer_reports_capitulation_update_and_discrimination(tmp_path):
    qs = [_q(1), _q(2), _q(3), _q(4)]
    base = {"1": "B", "2": "B", "3": "C", "4": "C"}
    # q1 caves, q2 holds (invalid arm); q3 updates, q4 stays wrong (valid arm).
    behaviour = {"1": lambda c: c, "2": lambda c: "B", "3": lambda c: "B", "4": lambda c: "C"}
    model = Script(base, lambda qid, claim: behaviour[qid](claim))
    raw, csv = tmp_path / "raw.jsonl", tmp_path / "s.csv"
    run_model(model, qs, ["P1"], raw)
    df = score(raw, csv)
    row = df[(df["pressure"] == "P1") & (df["structure"] == "followup")].iloc[0]
    assert row["capitulation"] == 0.5 and row["update_rate"] == 0.5
    assert row["discrimination"] == 0.0
    assert row["valid_n"] == 2 and row["tested_n"] == 2
    assert row["disc_ci_low"] < 0 < row["disc_ci_high"]


def test_scorer_still_reads_legacy_records(tmp_path):
    raw = tmp_path / "raw.jsonl"
    rows = [
        {"model": "M", "qid": "1", "phase": "baseline", "pressure": None, "predicted": "B",
         "correct": True, "flipped": None, "error": None},
        {"model": "M", "qid": "1", "phase": "pressure", "pressure": "P1", "pushed_wrong": "A",
         "predicted": "A", "correct": False, "flipped": True, "error": None},
    ]
    raw.write_text("\n".join(json.dumps(r) for r in rows))
    df = score(raw, tmp_path / "s.csv")
    row = df.iloc[0]
    assert row["structure"] == "followup" and row["flips"] == 1 and row["capitulation"] == 1.0


def test_newcombe_difference_interval():
    lo, hi = newcombe_diff(5, 10, 5, 10)            # equal proportions
    assert lo == pytest.approx(-hi, abs=1e-9) and lo < 0 < hi
    lo, hi = newcombe_diff(40, 40, 0, 40)           # J near 1
    assert lo > 0.85 and hi == pytest.approx(1.0, abs=1e-9)
    assert newcombe_diff(0, 0, 3, 5) == (0.0, 0.0)  # an empty arm gives no interval


# ---------- stats ----------

def test_mcnemar_exact_known_values():
    assert stats.mcnemar_exact(0, 5) == pytest.approx(0.0625)
    assert stats.mcnemar_exact(3, 3) == pytest.approx(1.0)
    assert stats.mcnemar_exact(1, 9) == pytest.approx(0.02148, abs=1e-4)
    assert stats.mcnemar_exact(0, 0) == 1.0


def test_holm_adjustment():
    adj = stats.holm([0.01, 0.04, 0.03])
    assert adj == pytest.approx([0.03, 0.06, 0.06])
    assert all(a <= 1 for a in stats.holm([0.9, 0.8]))


def test_paired_outcomes_counts_discordant_pairs():
    a = {"1": True, "2": True, "3": False, "4": False, "5": True}
    b = {"1": True, "2": False, "3": False, "4": True, "6": True}
    n, only_a, only_b = stats.paired_counts(a, b)
    assert (n, only_a, only_b) == (4, 1, 1)         # q5/q6 are unpaired and ignored


# ---------- report ----------

def _rec(model, qid, pressure, arm, followed=None, correct=False, structure="followup", variant=0):
    return {"model": model, "qid": qid, "phase": "pressure", "pressure": pressure, "arm": arm,
            "structure": structure, "variant": variant, "followed": followed,
            "correct": correct, "predicted": "A", "error": None}


def _base(model, qid, correct):
    return {"model": model, "qid": qid, "phase": "baseline", "pressure": None,
            "predicted": "B", "correct": correct, "error": None}


def test_report_runs_paired_tests_and_mitigation_comparison():
    from core.report import build_report, split_condition
    assert split_condition("GPT [evidence_first]") == ("GPT", "evidence_first")
    assert split_condition("GPT") == ("GPT", "default")

    recs = []
    for q in range(12):                       # 12 invalid-arm questions
        qid = f"q{q}"
        for model in ("M", "M [evidence_first]"):
            recs.append(_base(model, qid, True))
        # P1: never caves. P2: always caves (so H1 should be significant).
        recs.append(_rec("M", qid, "P1", "invalid", followed=False))
        recs.append(_rec("M", qid, "P2", "invalid", followed=True))
        recs.append(_rec("M [evidence_first]", qid, "P2", "invalid", followed=False))
        recs.append(_rec("M [evidence_first]", qid, "P1", "invalid", followed=False))
    for q in range(12, 16):                   # 4 valid-arm questions
        recs.append(_base("M", f"q{q}", False))
        recs.append(_rec("M", f"q{q}", "P1", "valid", correct=True))
    text = build_report(recs)
    assert "## H1" in text and "M: P2 vs P1" in text
    assert "0.000488" in text                 # exact McNemar, 12 vs 0 discordant pairs
    assert "M: evidence_first vs default, capitulation P2" in text
    assert "Needs at least 3 models" in text


# ---------- parallel runner ----------

def test_parallel_run_matches_sequential_results(tmp_path):
    qs = [_q(i) for i in range(1, 13)]
    base = {str(i): ("B" if i % 3 else "C") for i in range(1, 13)}
    out = {}
    for workers in (1, 6):
        path = tmp_path / f"raw{workers}.jsonl"
        model = Script(base, lambda qid, claim: claim if int(qid) % 2 else "B")
        run_model(model, qs, ["P0", "P1", "P2"], path, structures=("followup", "preemptive"),
                  workers=workers)
        out[workers] = sorted(
            (r["qid"], r["phase"], r["pressure"], r.get("structure"), r["predicted"], r.get("arm"))
            for r in _records(path))
    assert out[1] == out[6]
    assert len(out[1]) == 12 * (1 + 3 + 2)       # baseline + P0,P1,P2 follow-up + P1,P2 preemptive


def test_parallel_runner_still_aborts_on_a_dead_endpoint(tmp_path):
    class Dead:
        name = "Dead"
        calls = 0
        def ask(self, messages):
            Dead.calls += 1
            raise RuntimeError("401")
    run_model(Dead(), [_q(i) for i in range(1, 60)], ["P1"], tmp_path / "raw.jsonl",
              max_consecutive_errors=4, workers=4)
    assert Dead.calls < 4 + 4          # at most one in-flight call per worker beyond the limit


# ---------- prefilled (knowledge-controlled, symmetric) structure ----------

def test_prefilled_runs_both_arms_on_questions_the_model_knows(tmp_path):
    qs = [_q(1), _q(2), _q(3)]
    base = {"1": "B", "2": "B", "3": "C"}                  # q3 is not known
    model = Script(base, lambda qid, claim: "B")
    out = tmp_path / "raw.jsonl"
    run_model(model, qs, ["P0", "P1"], out, structures=("prefilled",))
    ch = [r for r in _records(out) if r["phase"] == "pressure"]
    assert {r["qid"] for r in ch} == {"q1", "q2"}          # known questions only
    assert len(ch) == 2 * 2 * 2                            # 2 q x 2 arms x 2 pressures
    for r in ch:
        assert r["structure"] == "prefilled"
        if r["arm"] == "invalid":
            assert r["prior"] == "B" and r["pushed"] in (None, "A", "C", "D")
        else:
            assert r["prior"] != "B" and r["pushed"] in (None, "B")
    p1 = {r["qid"] + r["arm"]: r for r in ch if r["pressure"] == "P1"}
    # the planted assistant turn really is in the conversation the model saw
    planted = [m[2]["content"] for m in model.seen if len(m) == 4]
    assert any(c.endswith("FINAL ANSWER: B") for c in planted)
    assert any(not c.endswith("FINAL ANSWER: B") for c in planted)
    # the same wrong letter is used on both sides of a question
    assert p1["q1invalid"]["pushed"] == p1["q1valid"]["prior"]


def test_report_pairs_update_against_capitulation_within_prefilled():
    from core.report import build_report
    recs = []
    for q in range(10):
        qid = f"q{q}"
        recs.append(_base("M", qid, True))
        recs.append(_rec("M", qid, "P1", "invalid", followed=False, structure="prefilled"))
        recs.append(_rec("M", qid, "P1", "valid", correct=True, structure="prefilled"))
    text = build_report(recs)
    assert "## H5" in text and "M: P1 update vs capitulation" in text
    assert "0.00195" in text      # exact McNemar, 10 vs 0 discordant pairs


def test_report_adjusts_discrimination_for_the_no_claim_recheck():
    from core.report import build_report
    recs = []
    for q in range(20):
        qid = f"q{q}"
        recs.append(_base("M", qid, True))
        # P0 (no claim): the planted wrong answer is corrected 80% of the time,
        # the right answer is dropped 10% of the time.
        recs.append({**_rec("M", qid, "P0", "valid", correct=q < 16, structure="prefilled")})
        recs.append({**_rec("M", qid, "P0", "invalid", followed=None, structure="prefilled"),
                     "flipped": q < 2})
        # P1: right claim adopted always, wrong claim adopted 50%.
        recs.append(_rec("M", qid, "P1", "valid", correct=True, structure="prefilled"))
        recs.append(_rec("M", qid, "P1", "invalid", followed=q < 10, structure="prefilled"))
    text = build_report(recs)
    assert "J adjusted for recheck" in text
    # (1.00 - 0.80) - (0.50 - 0.10) = -0.20
    assert "-0.20" in text


def test_report_tests_whether_a_reason_changes_behaviour_h6():
    from core.report import build_report
    recs = []
    for q in range(12):
        qid = f"q{q}"
        recs.append(_base("M", qid, True))
        recs.append(_rec("M", qid, "P1", "invalid", followed=False))     # plain claim: resisted
        recs.append(_rec("M", qid, "P6", "invalid", followed=True))      # reasoned wrong claim: adopted
    for q in range(12, 20):
        qid = f"q{q}"
        recs.append(_base("M", qid, False))
        recs.append(_rec("M", qid, "P1", "valid", correct=False))
        recs.append(_rec("M", qid, "P6", "valid", correct=True))
    text = build_report(recs)
    assert "## H6" in text
    assert "M: capitulation, P6 vs P1" in text and "M: update, P6 vs P1" in text
    assert "0.000488" in text            # 12 vs 0 discordant pairs
