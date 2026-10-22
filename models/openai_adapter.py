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

Newer "reasoning" models (e.g. OpenAI's GPT-5 family) differ from the classic
chat API: they take `max_completion_tokens` instead of `max_tokens`, and some
reject `temperature: 0`. Rather than hard-coding model names, the adapter reads
the API's 400 response, adjusts the request once, and remembers the fix.
Provider-specific knobs (e.g. `reasoning_effort`) go in `extra_params` in
config.yaml and are merged into the request body.

Reasoning models also spend `max_tokens` on hidden thinking. If that leaves no
visible text the adapter raises, so the run records an error instead of scoring
an empty reply as a wrong answer. Raise `max_tokens` for those models.
"""

from __future__ import annotations
from typing import List, Dict, Optional

import requests

from models.base import ModelAdapter, post_with_retries


class OpenAICompatAdapter(ModelAdapter):
    def __init__(self, base_url: str, api_key: str, timeout: int = 120,
                 extra_params: Optional[Dict] = None, **kwargs):
        super().__init__(**kwargs)
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.extra_params = dict(extra_params or {})
        # Learned from the API's own error messages (see _adapt_to_error).
        self._token_param = "max_tokens"
        self._send_temperature = True
        self.seen_models = set()      # model ids the API reports it served

    def _payload(self, messages) -> Dict:
        payload = {"model": self.model_id, "messages": messages,
                   self._token_param: self.max_tokens}
        if self._send_temperature:
            payload["temperature"] = self.temperature
        payload.update(self.extra_params)
        return payload

    def _adapt_to_error(self, err: requests.HTTPError) -> bool:
        """Adjust request settings after a 400; True if the caller should retry.

        Idempotent on purpose: with parallel workers several calls fail with the
        same 400 before any of them has adapted, and the late ones must retry
        with the already-corrected settings instead of giving up.
        """
        resp = getattr(err, "response", None)
        if resp is None or resp.status_code != 400:
            return False
        text = f"{err} {getattr(resp, 'text', '')}".lower()
        if "max_completion_tokens" in text and "max_tokens" in text:
            self._token_param = "max_completion_tokens"
            return True
        if "temperature" in text and "temperature" not in self.extra_params:
            self._send_temperature = False
            return True
        return False

    def ask(self, messages: List[Dict[str, str]]) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        for _ in range(4):  # fix the token param, then the temperature (+1 for races)
            try:
                resp = post_with_retries(url, headers=headers,
                                         json=self._payload(messages),
                                         timeout=self.timeout)
                break
            except requests.HTTPError as e:
                if not self._adapt_to_error(e):
                    raise
        else:
            raise RuntimeError("could not find request parameters this model accepts")

        # Standard shape: {"choices": [{"message": {"content": "..."}}]}
        body = resp.json()
        if body.get("model"):
            self.seen_models.add(body["model"])
        choice = body["choices"][0]
        text = choice["message"].get("content") or ""
        if not text.strip() and choice.get("finish_reason") == "length":
            raise RuntimeError(
                "empty reply: the token budget ran out before any visible text "
                "(reasoning model?). Raise max_tokens for this model.")
        return text
