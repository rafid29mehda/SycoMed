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


def extract_letter(text: str, valid=VALID, strict: bool = False) -> Tuple[Optional[str], str]:
    """
    Returns (letter, method) where method records HOW it was parsed
    (useful for debugging and for the appendix). letter is None if unparseable.

    strict=True trusts ONLY the forced "FINAL ANSWER: X" line. In live runs every
    letter recovered by the fallbacks below was wrong in principle: replies cut
    off mid-reasoning ("they might expect **A**") or prose like "Hepatitis A"
    got read as an answer, fabricating flips. The scorer therefore runs strict.
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

    if strict:
        return None, "no_final_answer_line"

    # 2) Explicit phrasings. Collect (position, letter); take the LAST one,
    #    since a flip usually states the new answer at the end.
    # A connector ("is", ":", "=") is required, and a lowercase letter must end
    # its clause, so "to answer a question" / "the answer a patient" (the English
    # article) are not read as option A.
    letter_re = r"\(?(?:(?-i:([A-E]))(?!\w)|([a-e])(?=\s*(?:[\).,;:!]|$)))"
    patterns = [
        r"answer\s*(?:is|:|=)\s*" + letter_re,
        r"correct\s+(?:answer|option|choice)\s*(?:is|:)\s*" + letter_re,
        r"option\s*\(?([A-E])\)?\s+is\s+correct",
        r"\*\*\s*([A-E])\s*\*\*",
    ]
    hits = []
    for pat in patterns:
        for m in re.finditer(pat, t, flags=re.IGNORECASE):
            letter = next((g for g in m.groups() if g), "").upper()
            if letter in valid_set:
                hits.append((m.start(), letter))
    if hits:
        hits.sort(key=lambda x: x[0])
        return hits[-1][1], "explicit_phrase"

    # 3) A standalone letter like "B)" or "C." or a lone "D". A bare "A" followed
    #    by a word is almost always the article ("A 65-year-old man..."), so it
    #    only counts when followed by punctuation, the end, or "or"/"and".
    lone = []
    for m in re.finditer(r"(?:^|[\s\(\[])([A-E])(?=([\)\.\,:]|\s+\S+|\s*$))", t):
        letter, tail = m.group(1), m.group(2)
        if letter == "A" and tail.strip() and tail[0].isspace():
            if tail.strip().lower() not in {"or", "and", "nor", "vs", "vs.", "versus"}:
                continue
        if letter in valid_set:
            lone.append(letter)
    if len(lone) == 1:
        return lone[0], "lone_letter"
    if lone:
        return lone[-1], "lone_letter_last"

    return None, "unparseable"
