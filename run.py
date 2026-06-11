"""
run.py -- the single command that runs everything.

Usage:
    python run.py                  # uses config.yaml
    python run.py --config my.yaml

What it does:
    1. Reads config.yaml.
    2. Loads + samples the questions.
    3. For each model, runs the baseline + pressure loop (core/runner.py).
    4. Scores all results into outputs/scorecard.csv (core/scorer.py).
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

import yaml

# Make sure the project root is importable when run as `python run.py`.
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from data.load_medqa import load_questions, save_jsonl
from models.base import get_adapter
from core.runner import run_model
from core.scorer import score


def main():
    ap = argparse.ArgumentParser(description="SycoMed: medical LLM sycophancy harness")
    ap.add_argument("--config", default="config.yaml")
    args = ap.parse_args()

    cfg = yaml.safe_load(open(ROOT / args.config, encoding="utf-8"))

    # Load environment variables from .env if python-dotenv is installed.
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
    except Exception:
        pass

    d = cfg["dataset"]
    questions = load_questions(
        source=d["source"], n=d.get("n", 200),
        seed=d.get("seed", 42), jsonl_path=d.get("jsonl_path", ""),
    )
    print(f"Loaded {len(questions)} questions (source={d['source']}, seed={d.get('seed')}).")

    # Save the exact sample used, so a run can be reproduced or inspected later.
    save_jsonl(questions, ROOT / "outputs" / "questions_used.jsonl")

    run_cfg = cfg["run"]
    out_jsonl = ROOT / run_cfg["out_jsonl"]
    out_csv = ROOT / run_cfg["out_csv"]
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)

    if run_cfg.get("fresh", True) and out_jsonl.exists():
        out_jsonl.unlink()

    pressure_ids = cfg["pressures"]
    sleep = run_cfg.get("sleep", 0.0)

    for m_cfg in cfg["models"]:
        print(f"\n>>> Running model: {m_cfg['name']} ({m_cfg['provider']})")
        try:
            adapter = get_adapter(m_cfg)
        except Exception as e:
            print(f"    Could not build adapter: {e}")
            continue
        run_model(adapter, questions, pressure_ids, out_jsonl, sleep=sleep)

    print("\nScoring...")
    score(out_jsonl, out_csv)
    print(f"\nDone. Scorecard -> {out_csv}")
    print(f"Raw responses    -> {out_jsonl}")


if __name__ == "__main__":
    main()
