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
"""

from __future__ import annotations
from typing import List, Dict

from models.base import ModelAdapter, post_with_retries


class OllamaAdapter(ModelAdapter):
    def __init__(self, host: str = "http://localhost:11434", timeout: int = 300, **kwargs):
        super().__init__(**kwargs)
        self.host = host.rstrip("/")
        self.timeout = timeout

    def ask(self, messages: List[Dict[str, str]]) -> str:
        url = f"{self.host}/api/chat"
        payload = {
            "model": self.model_id,
            "messages": messages,
            "stream": False,                 # get the whole reply at once
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
        }
        resp = post_with_retries(url, json=payload, timeout=self.timeout)
        data = resp.json()
        # Ollama returns {"message": {"role": "assistant", "content": "..."}}
        return data.get("message", {}).get("content", "") or ""
