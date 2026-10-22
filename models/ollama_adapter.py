"""
models/ollama_adapter.py
------------------------
Talks to a LOCAL model served by Ollama (https://ollama.com).

Ollama runs a small web server on your Mac at http://localhost:11434.
We POST the conversation to /api/chat and read back the reply. This is
completely free and runs on your M3's GPU automatically.

Before using this, make sure:
    1. Ollama is installed and running.
    2. You have pulled the model, e.g.:  ollama pull llama3.1:8b

Context window (num_ctx):
    Llama 3.2's Ollama tag advertises 131,072 tokens. If we omit num_ctx,
    Ollama reserves a KV cache for that full window — about 15 GB for a 3B
    model — which thrashes an 18 GB Mac before the first answer. SycoMed
    prompts are a medical MCQ plus a short replayed chat, nowhere near 128k.
    We therefore send num_ctx sized to *this* conversation (prompt + max_tokens).
    That is an engine setting, not a change to questions, pressures, or metrics.
    Set num_ctx in config.yaml only if you need to force a specific window.
"""

from __future__ import annotations
from typing import List, Dict, Optional

from models.base import ModelAdapter, post_with_retries


def estimate_tokens(text: str) -> int:
    """Upper-bound token count for English medical text (~3 chars/token)."""
    if not text:
        return 0
    return max(1, (len(text) + 2) // 3)


def needed_ctx(messages: List[Dict[str, str]], max_tokens: int) -> int:
    """Smallest Ollama num_ctx that still fits this request, rounded up to 256."""
    prompt = sum(estimate_tokens(m.get("content") or "") for m in messages)
    raw = prompt + int(max_tokens) + 64
    return max(512, ((raw + 255) // 256) * 256)


class OllamaAdapter(ModelAdapter):
    def __init__(self, host: str = "http://localhost:11434", timeout: int = 300,
                 num_ctx: Optional[int] = None, **kwargs):
        super().__init__(**kwargs)
        self.host = host.rstrip("/")
        self.timeout = timeout
        self.num_ctx = num_ctx

    def ask(self, messages: List[Dict[str, str]]) -> str:
        url = f"{self.host}/api/chat"
        ctx = self.num_ctx if self.num_ctx else needed_ctx(messages, self.max_tokens)
        payload = {
            "model": self.model_id,
            "messages": messages,
            "stream": False,                 # get the whole reply at once
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
                "num_ctx": ctx,
            },
        }
        resp = post_with_retries(url, json=payload, timeout=self.timeout)
        data = resp.json()
        # Ollama returns {"message": {"role": "assistant", "content": "..."}}
        return data.get("message", {}).get("content", "") or ""
