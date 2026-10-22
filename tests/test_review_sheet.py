"""Tests for the blind physician review sheet (docs/PROTOCOL.md, Amendment 1, A1.5)."""

import csv
import json

import pytest
import yaml

from data import review_sheet as rs

SECRET_REPLY = "ZZ-SECRET-MODEL-REPLY"
SECRET_MODEL = "ZZ-Secret-Model"


def base(model, qid, k, predicted, gold="A", error=None):
    return {"model": model, "qid": qid, "phase": "baseline", "sample": k, "gold": gold,
            "predicted": predicted, "correct": predicted == gold, "error": error,
            "reply": SECRET_REPLY}


def wrong_all(model, qid, n=3):
    return [base(model, qid, k, "B") for k in range(n)]


def make_question(i):
    return {"id": f"q{i:03d}", "question": f"Question text {i}?",
            "options": {"A": "alpha", "B": "beta", "C": "gamma", "D": "delta"},
            "answer_letter": "A"}


def make_annotation(i):
    return {"id": f"q{i:03d}", "problems": [], "tempting_wrong": "B",
            "correct_rationale": f"correct reasoning {i}", "wrong_rationale": f"flawed reasoning {i}"}


# ---- which questions are valid-arm items -------------------------------------------

def test_valid_arm_is_stably_wrong_with_every_sample_read():
    recs = (wrong_all("M", "stable_wrong")
            + [base("M", "unstable", 0, "A"), base("M", "unstable", 1, "B"), base("M", "unstable", 2, "B")]
            + [base("M", "known", k, "A") for k in range(3)]
            + [base("M", "unread", 0, "B"), base("M", "unread", 1, None), base("M", "unread", 2, "B")]
            + [base("M", "errored", 0, "B"), base("M", "errored", 1, "B", error="rate limit"),
               base("M", "errored", 2, "B")])
    assert rs.valid_arm_setups(recs) == {"stable_wrong": {"M"}}


def test_valid_arm_is_the_union_over_setups_and_names_them():
    recs = (wrong_all("M", "q1") + wrong_all("M [evidence_first]", "q1")
            + wrong_all("N", "q2") + [base("N", "q3", k, "A") for k in range(3)])
    got = rs.valid_arm_setups(recs)
    assert got == {"q1": {"M", "M [evidence_first]"}, "q2": {"N"}}


def test_valid_arm_ignores_pressure_records():
    pressure = {"model": "M", "qid": "q9", "phase": "pressure", "arm": "valid",
                "structure": "followup", "pressure": "P1", "predicted": "A", "correct": True,
                "error": None, "reply": SECRET_REPLY}
    assert rs.valid_arm_setups([pressure]) == {}


# ---- which items go on the sheet ---------------------------------------------------

def test_selection_keeps_every_valid_item_and_samples_the_rest():
    ids = [f"q{i:03d}" for i in range(300)]
    valid = set(ids[:40])
    order, groups = rs.select_items(ids, valid, set(ids), n_other=50, n_annotation=30, seed=1)
    assert valid <= set(order)
    assert len(order) == len(set(order))
    assert sum("random_other" in g for g in groups.values()) == 50
    assert sum("annotation_sample" in g for g in groups.values()) == 30
    assert all("random_other" not in groups[q] for q in valid)   # drawn from the others only


def test_selection_is_deterministic_and_independent_of_input_order():
    ids = [f"q{i:03d}" for i in range(200)]
    a = rs.select_items(ids, {"q001", "q002"}, set(ids), 20, 20, seed=7)
    b = rs.select_items(list(reversed(ids)), {"q002", "q001"}, set(ids), 20, 20, seed=7)
    c = rs.select_items(ids, {"q001", "q002"}, set(ids), 20, 20, seed=8)
    assert a == b
    assert a[0] != c[0]


def test_selection_handles_small_pools():
    order, groups = rs.select_items(["a", "b", "c"], {"a"}, {"b"}, n_other=100, n_annotation=100)
    assert set(order) == {"a", "b", "c"}
    assert groups["b"] == {"random_other", "annotation_sample"}


def test_row_order_does_not_reveal_the_group():
    ids = [f"q{i:03d}" for i in range(300)]
    valid = set(ids[:60])
    order, _ = rs.select_items(ids, valid, set(ids), 60, 0, seed=3)
    first_half = order[: len(order) // 2]
    share = sum(q in valid for q in first_half) / len(first_half)
    assert 0.25 < share < 0.75, "valid-arm items are clustered at the top or bottom"


# ---- the files ---------------------------------------------------------------------

@pytest.fixture
def run_dir(tmp_path):
    """A finished held-out run: 12 questions, two setups, three valid-arm items."""
    out = tmp_path / "out"
    out.mkdir()
    qs = [make_question(i) for i in range(12)]
    (out / "questions_used.jsonl").write_text("\n".join(json.dumps(q) for q in qs))
    anns = [make_annotation(i) for i in range(12) if i != 5]           # q005 has none
    anns.append({"id": "q005", "problems": ["unparseable reply"], "tempting_wrong": None,
                 "correct_rationale": None, "wrong_rationale": None})
    ann_path = tmp_path / "ann.jsonl"
    ann_path.write_text("\n".join(json.dumps(a) for a in anns))
    recs = []
    for i in range(12):
        qid = f"q{i:03d}"
        for model in (SECRET_MODEL, SECRET_MODEL + " [resolve_first]"):
            recs += wrong_all(model, qid) if i in (1, 5) or (i == 7 and model == SECRET_MODEL) \
                else [base(model, qid, k, "A") for k in range(3)]
    raw = out / "raw_responses.jsonl"
    raw.write_text("\n".join(json.dumps(r) for r in recs))
    return {"raw": raw, "questions": out / "questions_used.jsonl", "ann": ann_path,
            "out": tmp_path / "review.csv", "tmp": tmp_path}


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_sheet_has_only_the_whitelisted_columns_and_leaks_no_model_output(run_dir):
    rs.build(run_dir["raw"], run_dir["questions"], run_dir["ann"], run_dir["out"],
             n_other=4, n_annotation=4, seed=1)
    text = run_dir["out"].read_text(encoding="utf-8")
    rows = read_csv(run_dir["out"])
    assert list(rows[0].keys()) == rs.SHEET_COLUMNS
    assert SECRET_REPLY not in text and SECRET_MODEL not in text
    for banned in ("valid_arm", "random_other", "annotation_sample", "predicted", "setup"):
        assert banned not in text.splitlines()[0]
    rating_cols = rs.SHEET_COLUMNS[7:]
    assert all(r[c] == "" for r in rows for c in rating_cols)


def test_sheet_contains_question_options_key_and_annotations(run_dir):
    rs.build(run_dir["raw"], run_dir["questions"], run_dir["ann"], run_dir["out"],
             n_other=12, n_annotation=12, seed=1)
    rows = {r["id"]: r for r in read_csv(run_dir["out"])}
    assert len(rows) == 12
    r = rows["q001"]
    assert r["question"] == "Question text 1?"
    assert r["options"] == "A) alpha | B) beta | C) gamma | D) delta"
    assert r["gold"] == "A" and r["tempting_wrong"] == "B"
    assert r["correct_rationale"] == "correct reasoning 1" and r["wrong_rationale"] == "flawed reasoning 1"


def test_item_without_a_clean_annotation_still_appears_with_blank_annotations(run_dir):
    rs.build(run_dir["raw"], run_dir["questions"], run_dir["ann"], run_dir["out"],
             n_other=0, n_annotation=0, seed=1)
    rows = {r["id"]: r for r in read_csv(run_dir["out"])}
    assert set(rows) == {"q001", "q005", "q007"}          # valid-arm items only
    assert rows["q005"]["tempting_wrong"] == rows["q005"]["correct_rationale"] == ""


def test_key_file_records_groups_and_setups_for_the_analyst_only(run_dir):
    summary = rs.build(run_dir["raw"], run_dir["questions"], run_dir["ann"], run_dir["out"],
                       n_other=3, n_annotation=2, seed=1)
    key_path = run_dir["out"].with_name("review_key.csv")
    key = {r["id"]: r for r in read_csv(key_path)}
    assert list(read_csv(key_path)[0].keys()) == rs.KEY_COLUMNS
    assert {q for q, r in key.items() if r["valid_arm"] == "1"} == {"q001", "q005", "q007"}
    assert key["q001"]["valid_arm_setups"] == f"{SECRET_MODEL} | {SECRET_MODEL} [resolve_first]"
    assert key["q007"]["valid_arm_setups"] == SECRET_MODEL
    assert summary["valid_arm"] == 3 and summary["setups"] == 2
    assert summary["items"] == len(key) == len(read_csv(run_dir["out"]))
    assert sum(r["random_other"] == "1" for r in key.values()) == 3


def test_same_inputs_give_an_identical_sheet(run_dir):
    kw = dict(n_other=4, n_annotation=4, seed=5)
    rs.build(run_dir["raw"], run_dir["questions"], run_dir["ann"], run_dir["out"], **kw)
    first = run_dir["out"].read_bytes()
    rs.build(run_dir["raw"], run_dir["questions"], run_dir["ann"], run_dir["out"], **kw)
    assert run_dir["out"].read_bytes() == first


def test_missing_run_is_a_clear_error_not_an_empty_sheet(run_dir):
    run_dir["raw"].unlink()
    with pytest.raises(FileNotFoundError, match="finished"):
        rs.build(run_dir["raw"], run_dir["questions"], run_dir["ann"], run_dir["out"])
    assert not run_dir["out"].exists()


def test_replies_for_unknown_questions_are_refused(run_dir):
    with open(run_dir["raw"], "a", encoding="utf-8") as f:
        f.write("\n" + "\n".join(json.dumps(r) for r in wrong_all("M", "not_a_question")))
    with pytest.raises(ValueError, match="not_a_question"):
        rs.build(run_dir["raw"], run_dir["questions"], run_dir["ann"], run_dir["out"])


def test_command_line_reads_the_config(run_dir, capsys):
    cfg = {"run": {"out_jsonl": str(run_dir["raw"])},
           "dataset": {"annotations": str(run_dir["ann"])}}
    cfg_path = run_dir["tmp"] / "cfg.yaml"
    cfg_path.write_text(yaml.safe_dump(cfg))
    rs.main(["--config", str(cfg_path), "--out", str(run_dir["out"]),
             "--n-other", "2", "--n-annotation", "2"])
    assert run_dir["out"].exists() and run_dir["out"].with_name("review_key.csv").exists()
    assert "valid-arm items: 3 (across 2 setup(s))" in capsys.readouterr().out
