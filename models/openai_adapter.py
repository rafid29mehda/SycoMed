"""
models/openai_adapter.py
------------------------
Talks to any service that speaks the OpenAI /chat/completions format.

One adapter, many providers -- you just change `base_url` and the API-key
environment variable in config.yaml:

  OpenAI   base_url: https://api.openai.com/v1
  Gemini   base_url: https://generativelanguage.googleapis.com/v1beta/openai/
  Groq     base_url: https://api.groq.com/openai/v1
  OpenRouter base_url: https://openrouter.ai/api/v1
  Together base_url: https://api.together.xyz/v1

The API key is read from an environment variable (set in your .env file),
never hard-coded. See .env.example.
"""

from __future__ import annotations
from typing import List, Dict

from models.base import ModelAdapter, post_with_retries


class OpenAICompatAdapter(ModelAdapter):
    def __init__(self, base_url: str, api_key: str, timeout: int = 120, **kwargs):
        super().__init__(**kwargs)
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def ask(self, messages: List[Dict[str, str]]) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model_id,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        resp = post_with_retries(url, headers=headers, json=payload, timeout=self.timeout)
        data = resp.json()
        # Standard shape: {"choices": [{"message": {"content": "..."}}]}
        return data["choices"][0]["message"]["content"] or ""
