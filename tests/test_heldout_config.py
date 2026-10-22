"""Guards for the locked held-out configuration (docs/PROTOCOL.md, Amendment 1)."""

from pathlib import Path

import pytest
import yaml

from prompts import pressures

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def cfg():
    return yaml.safe_load(open(ROOT / "configs" / "heldout.yaml", encoding="utf-8"))


def test_heldout_questions_are_disjoint_from_pilots_and_dev(cfg):
    # Studies 1-3 used the first 600 shuffled questions (the dev set is the first 100).
    assert cfg["dataset"]["source"] == "medqa"
    assert cfg["dataset"]["seed"] == 42
    assert cfg["dataset"]["skip"] >= 600


def test_heldout_replies_can_never_be_deleted_by_a_rerun(cfg):
    assert cfg["run"]["fresh"] is False
    assert cfg["run"]["resume"] is True


def test_heldout_uses_the_protocol_design(cfg):
    assert cfg["run"]["baseline_samples"] == 3
    assert cfg["run"]["strict_parse"] is True
    assert set(cfg["run"]["structures"]) == {"followup", "preemptive", "prefilled"}
    assert cfg["pressures"] == ["P0", "P1", "P2", "P3", "P5", "P6"]
    for p in cfg["pressures"]:
        assert any(pressures.n_variants(p, s) > 0 for s in cfg["run"]["structures"])
    assert cfg["dataset"]["annotations"] == "data/annotations/heldout.jsonl"
    assert cfg["annotate"]["model_id"]


def test_every_mitigation_has_a_default_sibling_for_the_paired_comparison(cfg):
    names = {m["name"]: m for m in cfg["models"]}
    assert len(names) == len(cfg["models"]), "duplicate model names"
    for name, m in names.items():
        variant = m.get("system_variant", "default")
        if variant == "default":
            assert "[" not in name
            continue
        assert name.endswith(f"[{variant}]")
        base = name[: name.rindex(" [")]
        assert base in names and names[base].get("system_variant", "default") == "default"
        assert names[base]["model_id"] == m["model_id"]
    variants = {m.get("system_variant", "default") for m in cfg["models"]}
    assert variants == {"default", "evidence_first", "resolve_first"}
