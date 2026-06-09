"""
data/load_medqa.py
------------------
Loads questions and normalizes them to ONE standard shape the rest of the code
expects:

    {
      "id": "q123",
      "question": "....",
      "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
      "answer_letter": "B"
    }

Three sources, tried in order of what you ask for:
  - "medqa"  : downloads MedQA (USMLE, 4 options) from Hugging Face.
  - "jsonl"  : reads a local .jsonl you provide (already normalized).
  - "sample" : a tiny built-in set so the pipeline runs out-of-the-box.

A fixed random seed makes the sample reproducible.
"""

from __future__ import annotations
import json
import random
from pathlib import Path
from typing import List, Dict

LETTERS = ["A", "B", "C", "D"]

# A tiny built-in set so you can dry-run before downloading anything.
SAMPLE = [
    {
        "id": "s1",
        "question": "A 65-year-old man has sudden crushing chest pain radiating to "
                    "the left arm, sweating, and nausea. Most likely diagnosis?",
        "options": {"A": "Heartburn", "B": "Myocardial infarction",
                    "C": "Muscle strain", "D": "Panic attack"},
        "answer_letter": "B",
    },
    {
        "id": "s2",
        "question": "Which vitamin deficiency causes scurvy?",
        "options": {"A": "Vitamin A", "B": "Vitamin B12",
                    "C": "Vitamin C", "D": "Vitamin D"},
        "answer_letter": "C",
    },
    {
        "id": "s3",
        "question": "First-line treatment for anaphylaxis is?",
        "options": {"A": "Oral antihistamine", "B": "Intramuscular epinephrine",
                    "C": "Inhaled steroid", "D": "Intravenous fluids only"},
        "answer_letter": "B",
    },
    {
        "id": "s4",
        "question": "The most common cause of community-acquired pneumonia is?",
        "options": {"A": "Streptococcus pneumoniae", "B": "Mycobacterium tuberculosis",
                    "C": "Candida albicans", "D": "Influenza virus"},
        "answer_letter": "A",
    },
    {
        "id": "s5",
        "question": "Which organ produces insulin?",
        "options": {"A": "Liver", "B": "Pancreas", "C": "Kidney", "D": "Spleen"},
        "answer_letter": "B",
    },
]


def _normalize_hf_row(row: Dict, idx: int) -> Dict:
    """
    Normalize a Hugging Face MedQA row. Schemas vary across mirrors, so we
    handle the common ones. Returns None if it cannot be normalized.
    """
    q_text = row.get("question") or row.get("Question")
    options = None
    answer_letter = None

    # Common layout: options is a dict {"A": "...", ...}; answer_idx is "A".
    if isinstance(row.get("options"), dict):
        options = {k.upper(): v for k, v in row["options"].items() if k.upper() in LETTERS}
        ans = row.get("answer_idx") or row.get("answer_key")
        if isinstance(ans, str) and ans.upper() in LETTERS:
            answer_letter = ans.upper()

    # Layout: options is a list; answer is the full answer text.
    if options is None and isinstance(row.get("options"), list):
        opts = row["options"][:4]
        options = {LETTERS[i]: opts[i] for i in range(len(opts))}
        ans_text = row.get("answer")
        if ans_text is not None:
            for k, v in options.items():
                if str(v).strip() == str(ans_text).strip():
                    answer_letter = k
                    break

    if not q_text or not options or answer_letter is None:
        return None
    if not all(l in options for l in LETTERS):
        return None

    return {
        "id": str(row.get("id", f"hf{idx}")),
        "question": q_text,
        "options": options,
        "answer_letter": answer_letter,
    }


def load_questions(source: str = "sample", n: int = 200, seed: int = 42,
                   jsonl_path: str = "") -> List[Dict]:
    rng = random.Random(seed)

    if source == "sample":
        items = list(SAMPLE)

    elif source == "jsonl":
        items = []
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    items.append(json.loads(line))

    elif source == "medqa":
        from datasets import load_dataset  # imported lazily
        # Primary mirror; change in config if needed.
        ds = load_dataset("GBaker/MedQA-USMLE-4-options", split="test")
        items = []
        for idx, row in enumerate(ds):
            norm = _normalize_hf_row(row, idx)
            if norm is not None:
                items.append(norm)
    else:
        raise ValueError(f"Unknown source: {source!r}")

    rng.shuffle(items)
    if n and n < len(items):
        items = items[:n]
    return items


def save_jsonl(items: List[Dict], path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    # Quick manual test: prints how many questions loaded.
    qs = load_questions("sample")
    print(f"Loaded {len(qs)} sample questions.")
    print(json.dumps(qs[0], indent=2))
