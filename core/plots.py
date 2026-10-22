"""
core/plots.py
-------------
Figures from a scorecard.csv (columns written by core/scorer.py).

    python core/plots.py [scorecard.csv] [out_dir]

Produces (follow-up structure by default, the primary design):
    capitulation_vs_update.png   one panel per model: how often it adopts a WRONG
                                 claim (blue) vs a CORRECT claim (orange), by pressure
    discrimination.png           J = update - capitulation per model and pressure,
                                 with 95% intervals; 0 = ignores whether the user is right

Colours are slots 1-2 of the validated reference palette (see the dataviz skill);
the pair passes the lightness, chroma, CVD and contrast checks on the light surface.
The legend carries identity, so colour is never the only cue.
"""

from __future__ import annotations
import math
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # no display needed; just save files
import matplotlib.pyplot as plt

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e4e3df"
CAP, UPD = "#2a78d6", "#eb6834"          # categorical slots 1 and 2


def _style(ax):
    ax.set_facecolor(SURFACE)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=INK_2, labelsize=8)


def _err(df, col, lo, hi):
    """Asymmetric error bars (clipped at zero width) from interval columns."""
    return [(df[col] - df[lo]).clip(lower=0).fillna(0), (df[hi] - df[col]).clip(lower=0).fillna(0)]


def make_plots(csv_path: Path, out_dir: Path, structure: str = "followup"):
    df = pd.read_csv(csv_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    df = df[(df["structure"] == structure) & (df["pressure"] != "P0")]
    if df.empty:
        print(f"No {structure!r} rows to plot.")
        return
    models = list(dict.fromkeys(df["model"]))
    pressures = sorted(df["pressure"].unique())

    # ---- 1. capitulation vs update, one panel per model ----
    cols = min(3, len(models))
    rows = math.ceil(len(models) / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(4.2 * cols, 3.0 * rows + 0.6),
                             sharey=True, squeeze=False, facecolor=SURFACE)
    width = 0.38
    for ax, model in zip(axes.flat, models):
        sub = df[df["model"] == model].set_index("pressure").reindex(pressures).reset_index()
        x = range(len(pressures))
        ax.bar([i - width / 2 - 0.01 for i in x], sub["capitulation"].fillna(0), width,
               color=CAP, label="adopts a wrong claim (capitulation)",
               yerr=_err(sub, "capitulation", "cap_ci_low", "cap_ci_high"),
               error_kw={"ecolor": INK_2, "lw": 0.8, "capsize": 2})
        ax.bar([i + width / 2 + 0.01 for i in x], sub["update_rate"].fillna(0), width,
               color=UPD, label="adopts a correct claim (update)",
               yerr=_err(sub, "update_rate", "upd_ci_low", "upd_ci_high"),
               error_kw={"ecolor": INK_2, "lw": 0.8, "capsize": 2})
        ax.set_xticks(list(x))
        ax.set_xticklabels(pressures)
        ax.set_ylim(0, 1.05)
        ax.set_title(model, fontsize=9, color=INK, loc="left")
        ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
        _style(ax)
    for ax in list(axes.flat)[len(models):]:
        ax.axis("off")
    handles, labels = axes.flat[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False, fontsize=9,
               labelcolor=INK_2)
    fig.suptitle("Does the model follow the claim, or the truth?", fontsize=11, color=INK, x=0.01,
                 ha="left")
    fig.tight_layout(rect=(0, 0.06, 1, 0.95))
    fig.savefig(out_dir / "capitulation_vs_update.png", dpi=160, facecolor=SURFACE)
    plt.close(fig)

    # ---- 2. discrimination, dot + interval per model, one panel per pressure ----
    fig, axes = plt.subplots(1, len(pressures), figsize=(2.6 * len(pressures) + 2.2, 0.55 * len(models) + 1.6),
                             sharey=True, squeeze=False, facecolor=SURFACE)
    for ax, p in zip(axes.flat, pressures):
        sub = df[df["pressure"] == p].set_index("model").reindex(models).reset_index()
        y = list(range(len(models)))
        ax.axvline(0, color=INK_2, lw=0.9)
        ax.errorbar(sub["discrimination"], y,
                    xerr=_err(sub, "discrimination", "disc_ci_low", "disc_ci_high"),
                    fmt="o", color=CAP, ecolor=CAP, elinewidth=1.6, capsize=0, markersize=6,
                    markeredgecolor=SURFACE, markeredgewidth=1.2)
        ax.set_yticks(y)
        ax.set_yticklabels(models, fontsize=8, color=INK)
        ax.invert_yaxis()
        ax.set_xlim(-0.2, 1.0)
        ax.set_title(p, fontsize=9, color=INK, loc="left")
        ax.grid(axis="x", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.set_facecolor(SURFACE)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(GRID)
        ax.tick_params(colors=INK_2, labelsize=8, length=0)
    fig.supxlabel("J = update − capitulation   (0 = ignores whether the user is right; 1 = follows the truth)",
                  fontsize=8.5, color=INK_2)
    fig.tight_layout()
    fig.savefig(out_dir / "discrimination.png", dpi=160, facecolor=SURFACE)
    plt.close(fig)
    print(f"Saved plots to {out_dir}")


if __name__ == "__main__":
    import sys
    root = Path(__file__).resolve().parents[1]
    csv = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "outputs" / "scorecard.csv"
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else csv.parent / "plots"
    make_plots(csv, out)
