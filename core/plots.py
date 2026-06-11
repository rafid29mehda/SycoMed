"""
core/plots.py
-------------
Makes simple summary figures from outputs/scorecard.csv.

Run after a full run:
    python core/plots.py

Produces:
    outputs/plots/flip_rate_by_model.png   (flip rate under the authority cue P2)
    outputs/plots/pressure_profile.png      (flip rate across pressures, per model)
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # no display needed; just save files
import matplotlib.pyplot as plt


def make_plots(csv_path: Path, out_dir: Path, headline_pressure: str = "P2"):
    df = pd.read_csv(csv_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) Bar chart: flip rate per model under the headline pressure.
    sub = df[df["pressure"] == headline_pressure].sort_values("flip_rate")
    if not sub.empty:
        plt.figure(figsize=(7, 4))
        plt.barh(sub["model"], sub["flip_rate"])
        plt.xlabel(f"Flip rate under {headline_pressure} (authority cue)")
        plt.title("Sycophancy: fraction of correct answers reversed")
        plt.tight_layout()
        plt.savefig(out_dir / "flip_rate_by_model.png", dpi=150)
        plt.close()

    # 2) Line/grouped chart: flip rate across pressures, per model.
    pivot = df.pivot(index="pressure", columns="model", values="flip_rate")
    if not pivot.empty:
        plt.figure(figsize=(7, 4))
        for col in pivot.columns:
            plt.plot(pivot.index, pivot[col], marker="o", label=col)
        plt.ylabel("Flip rate")
        plt.xlabel("Pressure type")
        plt.title("Pressure-sensitivity profile")
        plt.legend(fontsize=8)
        plt.tight_layout()
        plt.savefig(out_dir / "pressure_profile.png", dpi=150)
        plt.close()

    print(f"Saved plots to {out_dir}")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    make_plots(root / "outputs" / "scorecard.csv", root / "outputs" / "plots")
