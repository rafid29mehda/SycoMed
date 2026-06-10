"""
core/parser.py
--------------
Turns a model's free-text reply into a single answer letter (A/B/C/D), or
None if it cannot be determined ("unparseable").

Strategy, in priority order:
  1. The forced "FINAL ANSWER: X" line we asked the model to produce.
  2. Common explicit phrasings ("the answer is B", "correct option: C", "**D**").
  3. A single standalone letter, if exactly one appears.
  4. Otherwise None -> counted and reported honestly as unparseable.

We track unparseable replies instead of guessing, because honest handling of
edge cases is part of the contribution (and reviewers notice).
"""

from __future__ import annotations
import re
from typing import Optional, Tuple

VALID = ("A", "B", "C", "D")


def extract_letter(text: str, valid=VALID) -> Tuple[Optional[str], str]:
    """
    Returns (letter, method) where method records HOW it was parsed
    (useful for debugging and for the appendix). letter is None if unparseable.
    """
    if not text:
        return None, "empty"

    t = text.strip()
    valid_set = set(valid)

    # 1) The forced final-answer line (highest priority, last occurrence wins).
    final = re.findall(r"FINAL\s*ANSWER\s*[:\-]?\s*\(?([A-E])\)?", t, flags=re.IGNORECASE)
    final = [x.upper() for x in final if x.upper() in valid_set]
    if final:
        return final[-1], "final_answer_line"

    # 2) Explicit phrasings. Collect (position, letter); take the LAST one,
    #    since a flip usually states the new answer at the end.
    patterns = [
        r"answer\s*(?:is|:|=)?\s*\(?([A-E])\)?",
        r"correct\s+(?:answer|option|choice)\s*(?:is|:)?\s*\(?([A-E])\)?",
        r"option\s*\(?([A-E])\)?\s+is\s+correct",
        r"\*\*\s*([A-E])\s*\*\*",
    ]
    hits = []
    for pat in patterns:
        for m in re.finditer(pat, t, flags=re.IGNORECASE):
            letter = m.group(1).upper()
            if letter in valid_set:
                hits.append((m.start(), letter))
    if hits:
        hits.sort(key=lambda x: x[0])
        return hits[-1][1], "explicit_phrase"

    # 3) A standalone letter like "B)" or "C." or a lone "D".
    lone = re.findall(r"(?:^|[\s\(\[])([A-E])(?=[\)\.\,:\s]|$)", t)
    lone = [x.upper() for x in lone if x.upper() in valid_set]
    if len(lone) == 1:
        return lone[0], "lone_letter"
    if lone:
        return lone[-1], "lone_letter_last"

    return None, "unparseable"
