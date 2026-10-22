"""
core/meta.py
------------
Provenance for a run, and call-count estimates before spending money.

  collect_meta(cfg, adapters, questions)  -> dict written to run_meta.json
  estimate_calls(cfg, n_questions)        -> upper bound on API calls

Nothing secret is recorded: API keys live in the environment and the config
only names the variable.
"""

from __future__ import annotations
import hashlib
import platform
import subprocess
import sys
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path
from typing import Dict, List

from prompts import pressures

_PACKAGES = ("requests", "pandas", "pyyaml", "datasets", "matplotlib")


def _git(*args) -> str:
    try:
        root = Path(__file__).resolve().parents[1]
        out = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=10)
        return out.stdout.strip() if out.returncode == 0 else ""
    except Exception:
        return ""


def _version(pkg: str) -> str:
    try:
        return metadata.version(pkg)
    except Exception:
        return ""


def collect_meta(cfg: Dict, adapters: List, questions: List[Dict]) -> Dict:
    """What a reader needs to reproduce or audit this run."""
    qids = "\n".join(str(q.get("id", "")) for q in questions)
    ann = cfg.get("dataset", {}).get("annotations")
    ann_hash = ""
    if ann:
        ann_path = Path(ann) if Path(ann).is_absolute() else Path(__file__).resolve().parents[1] / ann
        if ann_path.exists():
            ann_hash = hashlib.sha256(ann_path.read_bytes()).hexdigest()
    return {
        "started_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": {p: _version(p) for p in _PACKAGES},
        "git": {"commit": _git("rev-parse", "HEAD"),
                "dirty": bool(_git("status", "--porcelain"))},
        "dataset": {**{k: v for k, v in cfg.get("dataset", {}).items()},
                    "n_questions": len(questions),
                    "question_ids_sha256": hashlib.sha256(qids.encode()).hexdigest(),
                    **({"annotations_sha256": ann_hash} if ann_hash else {})},
        "config": cfg,
        "models": [{"name": getattr(a, "name", ""), "model_id": getattr(a, "model_id", ""),
                    # the model string the API says actually answered
                    "resolved_model_ids": sorted(getattr(a, "seen_models", set()))}
                   for a in adapters],
    }


def estimate_calls(cfg: Dict, n_questions: int) -> Dict:
    """Upper bound on API calls per question / model / run for this config."""
    run = cfg.get("run", {})
    structures = run.get("structures", ["followup"])
    samples = run.get("baseline_samples", 1)
    per_q = samples
    for structure in structures:
        usable = [p for p in cfg["pressures"] if pressures.n_variants(p, structure) > 0]
        per_q += len(usable) * (2 if structure == "prefilled" else 1)
    per_model = per_q * n_questions
    return {"per_question": per_q, "per_model": per_model,
            "models": len(cfg["models"]), "total": per_model * len(cfg["models"])}


def merge_meta(old: Dict, new: Dict) -> Dict:
    """Combine the metadata of a resumed run with the run it continues.

    Keeps the original start time and appends the resume time; model ids
    resolved by the API are unioned (a resume that makes no calls must not
    erase what the first run recorded).
    """
    merged = {**new, "started_utc": old.get("started_utc", new["started_utc"]),
              "resumed_utc": list(old.get("resumed_utc", [])) + [new["started_utc"]]}
    seen = {m["name"]: set(m.get("resolved_model_ids", [])) for m in old.get("models", [])}
    models = []
    for m in new.get("models", []):
        ids = sorted(seen.get(m["name"], set()) | set(m.get("resolved_model_ids", [])))
        models.append({**m, "resolved_model_ids": ids})
    merged["models"] = models
    return merged
