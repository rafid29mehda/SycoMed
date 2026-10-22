"""
run.py -- the single command that runs everything.

Usage:
    python run.py                  # uses config.yaml
    python run.py --config my.yaml

What it does:
    1. Reads config.yaml.
    2. Loads + samples the questions.
    3. For each model, runs the baseline + pressure loop (core/runner.py).
    4. Scores all results into outputs/scorecard.csv (core/scorer.py) and writes
       the paired-test report next to it (core/report.py, docs/PROTOCOL.md).
"""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

import yaml

# Make sure the project root is importable when run as `python run.py`.
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from data.load_medqa import load_questions, save_jsonl
from data.annotate import attach_annotations
from models.base import get_adapter
from core.runner import run_model
from core.scorer import score, load_records
from core.report import build_report
from core.meta import collect_meta, estimate_calls, merge_meta


def main():
    ap = argparse.ArgumentParser(description="SycoMed: medical LLM sycophancy harness")
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--dry-run", action="store_true",
                    help="load the questions, print how many API calls this config "
                         "would make (upper bound), and stop")
    ap.add_argument("--resume", action="store_true",
                    help="keep finished, error-free questions already in the output "
                         "file and only run the rest (use after a quota/abort)")
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
        skip=d.get("skip", 0),
    )
    print(f"Loaded {len(questions)} questions (source={d['source']}, seed={d.get('seed')}).")
    if d.get("annotations"):
        n_ann = attach_annotations(questions, ROOT / d["annotations"])
        print(f"Attached {n_ann}/{len(questions)} annotations (tempting wrong option + rationales); "
              "P6 runs only on annotated questions.")

    run_cfg = cfg["run"]

    if args.dry_run:
        est = estimate_calls(cfg, len(questions))
        print(f"\nDry run: {len(questions)} questions x {est['models']} model setup(s)")
        print(f"  up to {est['per_question']} calls per question, "
              f"{est['per_model']} per model, {est['total']} in total")
        print("  (an upper bound: baselines that are unstable or unreadable get no challenges)")
        return

    out_jsonl = ROOT / run_cfg["out_jsonl"]
    out_csv = ROOT / run_cfg["out_csv"]
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)

    # Save the exact sample used (next to the other outputs of this run), so a
    # run can be reproduced or inspected later.
    save_jsonl(questions, out_jsonl.parent / "questions_used.jsonl")

    resume = args.resume or run_cfg.get("resume", False)
    if run_cfg.get("fresh", True) and not resume and out_jsonl.exists():
        out_jsonl.unlink()

    pressure_ids = cfg["pressures"]
    sleep = run_cfg.get("sleep", 0.0)
    structures = run_cfg.get("structures", ["followup"])

    adapters = []
    for m_cfg in cfg["models"]:
        print(f"\n>>> Running model: {m_cfg['name']} ({m_cfg['provider']})")
        try:
            adapter = get_adapter(m_cfg)
        except Exception as e:
            print(f"    Could not build adapter: {e}")
            continue
        adapters.append(adapter)
        run_model(adapter, questions, pressure_ids, out_jsonl, sleep=sleep,
                  strict_parse=run_cfg.get("strict_parse", True),
                  structures=structures,
                  workers=m_cfg.get("workers", run_cfg.get("workers", 1)),
                  system_variant=m_cfg.get("system_variant", "default"),
                  baseline_samples=run_cfg.get("baseline_samples", 3),
                  resume=resume)

    # Provenance: what exactly produced these numbers (no secrets are recorded).
    meta = collect_meta(cfg, adapters, questions)
    meta_path = out_jsonl.parent / "run_meta.json"
    if resume and meta_path.exists():
        meta = merge_meta(json.loads(meta_path.read_text(encoding="utf-8")), meta)
    meta_path.write_text(
        json.dumps(meta, indent=2, default=str), encoding="utf-8")

    print("\nScoring...")
    score(out_jsonl, out_csv)
    out_md = out_csv.with_name("report.md")
    out_md.write_text(build_report(load_records(out_jsonl)), encoding="utf-8")
    try:
        from core.plots import make_plots
        make_plots(out_csv, out_csv.parent / "plots")
    except Exception as e:  # a plotting problem must never lose a finished run
        print(f"(plots skipped: {e})")
    print(f"\nDone. Scorecard -> {out_csv}")
    print(f"Report           -> {out_md}")
    print(f"Raw responses    -> {out_jsonl}")


if __name__ == "__main__":
    main()
