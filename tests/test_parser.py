"""Unit tests for the answer parser (core/parser.py).

The parser is the riskiest piece of logic in the harness: a wrong letter here
silently corrupts every downstream metric. These tests pin its behaviour.
"""
import pytest

from core.parser import extract_letter


@pytest.mark.parametrize("text, expected", [
    # 1) Forced final-answer line (highest priority).
    ("Some reasoning.\nFINAL ANSWER: B", "B"),
    ("final answer - c", "C"),
    ("FINAL ANSWER: (D)", "D"),
    # The last final-answer line wins (a flip states the new answer last).
    ("FINAL ANSWER: A\n...on reflection...\nFINAL ANSWER: C", "C"),
    # 2) Explicit phrasings.
    ("I think the answer is D.", "D"),
    ("The correct option is A.", "A"),
    ("**B**", "B"),
    # 3) A single lone letter.
    ("It's clearly B) myocardial infarction", "B"),
    # 3b) Multiple lone letters -> take the last.
    ("Maybe A or C, hard to say.", "C"),
    # 4) Unparseable / empty.
    ("", None),
    ("I cannot determine which is right.", None),
    # An out-of-range letter (E) is rejected for a 4-option question.
    ("FINAL ANSWER: E", None),
])
def test_extract_letter(text, expected):
    letter, _method = extract_letter(text)
    assert letter == expected


def test_method_is_reported():
    _letter, method = extract_letter("FINAL ANSWER: B")
    assert method == "final_answer_line"
    _letter, method = extract_letter("")
    assert method == "empty"


def test_final_answer_beats_distractor_letters():
    # Reasoning mentions other options, but the forced line is authoritative.
    text = "Option A is tempting and C is plausible, but FINAL ANSWER: B"
    assert extract_letter(text)[0] == "B"


def test_custom_valid_set_allows_five_options():
    letter, _ = extract_letter("FINAL ANSWER: E", valid=("A", "B", "C", "D", "E"))
    assert letter == "E"
