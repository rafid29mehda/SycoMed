"""
core/stats.py
-------------
Small, dependency-free statistics used by the scorer and the report.

  wilson_interval   95% interval for one proportion (fine for tiny n)
  newcombe_diff     95% interval for p1 - p2 of two independent proportions
  mcnemar_exact     exact two-sided p-value for paired binary outcomes
  holm              Holm step-down adjustment for several p-values
  paired_counts     discordant-pair counts for two {question: outcome} dicts
"""

from __future__ import annotations
import math
from typing import Dict, List, Tuple


def wilson_interval(k: int, n: int, z: float = 1.96) -> Tuple[float, float]:
    """95% Wilson score interval for a proportion k/n."""
    if n == 0:
        return 0.0, 0.0
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def newcombe_diff(k1: int, n1: int, k2: int, n2: int, z: float = 1.96) -> Tuple[float, float]:
    """Newcombe hybrid-score interval for p1 - p2 (independent samples).

    Returns (0, 0) if either sample is empty: no data, no interval.
    """
    if n1 == 0 or n2 == 0:
        return 0.0, 0.0
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson_interval(k1, n1, z)
    l2, u2 = wilson_interval(k2, n2, z)
    d = p1 - p2
    lo = d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return max(-1.0, lo), min(1.0, hi)


def mcnemar_exact(only_a: int, only_b: int) -> float:
    """Exact two-sided McNemar p-value from the two discordant counts."""
    n = only_a + only_b
    if n == 0:
        return 1.0
    k = min(only_a, only_b)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def holm(pvals: List[float]) -> List[float]:
    """Holm-adjusted p-values, returned in the input order."""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    adjusted = [0.0] * m
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * pvals[i])
        adjusted[i] = min(1.0, running)
    return adjusted


def paired_counts(a: Dict[str, bool], b: Dict[str, bool]) -> Tuple[int, int, int]:
    """(n_pairs, only_a, only_b) over questions present in both dicts."""
    common = set(a) & set(b)
    only_a = sum(1 for q in common if a[q] and not b[q])
    only_b = sum(1 for q in common if b[q] and not a[q])
    return len(common), only_a, only_b
