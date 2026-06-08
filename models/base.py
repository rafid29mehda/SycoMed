"""
models/base.py
--------------
Defines the common interface every model adapter must implement, plus a
factory that builds the right adapter from a config dict.

The whole point of SycoMed being "model-agnostic" lives here: every model,
whether it runs locally via Ollama or behind an API, is hidden behind the
same tiny method:

    adapter.ask(messages) -> str

`messages` is a list of chat turns in the OpenAI format:
    [{"role": "system", "content": "..."},
     {"role": "user", "content": "..."},
     {"role": "assistant", "content": "..."},
     {"role": "user", "content": "..."}]

To add a brand-new provider later, you only write one new adapter class and
register it in `get_adapter`. Nothing else in the codebase changes.
"""

from __future__ import annotations
import os
import time
from abc import ABC, abstractmethod
from typing import List, Dict

import requests

# HTTP status codes that are worth retrying (rate limits + transient 5xx).
RETRYABLE_STATUS = {429, 500, 502, 503, 504}


def post_with_retries(url, *, headers=None, json=None, timeout=120,
                      max_retries: int = 3, backoff: float = 2.0):
    """POST a JSON request with simple exponential backoff.

    Retries on connection errors, timeouts, and transient HTTP responses
    (429 / 5xx). Non-transient errors (e.g. 400, 401, 404) are raised at once.
    If every attempt fails the last error is raised, so the run loop in
    core/runner.py can log it and move on rather than crashing the whole run.
    """
    last_err = None
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, headers=headers, json=json, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout) as e:
            last_err = e
        else:
            if resp.status_code not in RETRYABLE_STATUS:
                resp.raise_for_status()  # raises on non-retryable 4xx, else returns
                return resp
            last_err = requests.HTTPError(f"{resp.status_code} {resp.reason}", response=resp)
        if attempt < max_retries - 1:
            time.sleep(backoff ** attempt)
    raise last_err


class ModelAdapter(ABC):
    """Common interface for all models."""

    def __init__(self, name: str, model_id: str, temperature: float = 0.0,
                 max_tokens: int = 512, **kwargs):
        self.name = name          # human-friendly label used in the scorecard
        self.model_id = model_id  # the provider's model string
        self.temperature = temperature
        self.max_tokens = max_tokens

    @abstractmethod
    def ask(self, messages: List[Dict[str, str]]) -> str:
        """Send a chat conversation and return the model's text reply."""
        raise NotImplementedError


def get_adapter(cfg: Dict) -> ModelAdapter:
    """
    Build an adapter from a config entry like:
        {provider: ollama,       name: "Llama 3.1 8B", model_id: "llama3.1:8b"}
        {provider: openai_compat, name: "Gemini Flash", model_id: "gemini-2.0-flash",
         base_url: "https://generativelanguage.googleapis.com/v1beta/openai/",
         api_key_env: "GEMINI_API_KEY"}
    """
    # Imported here (not at top) to avoid circular imports.
    from models.ollama_adapter import OllamaAdapter
    from models.openai_adapter import OpenAICompatAdapter

    provider = cfg.get("provider")
    common = dict(
        name=cfg["name"],
        model_id=cfg["model_id"],
        temperature=cfg.get("temperature", 0.0),
        max_tokens=cfg.get("max_tokens", 512),
    )

    if provider == "ollama":
        return OllamaAdapter(host=cfg.get("host", "http://localhost:11434"), **common)

    if provider == "openai_compat":
        api_key_env = cfg.get("api_key_env", "OPENAI_API_KEY")
        api_key = os.environ.get(api_key_env, "")
        return OpenAICompatAdapter(
            base_url=cfg["base_url"],
            api_key=api_key,
            **common,
        )

    raise ValueError(f"Unknown provider: {provider!r}. Use 'ollama' or 'openai_compat'.")
