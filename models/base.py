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
import re
import time
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

import requests

# HTTP status codes that are worth retrying (rate limits + transient 5xx).
RETRYABLE_STATUS = {429, 500, 502, 503, 504}

# If a server asks us to wait longer than this, the quota is effectively
# exhausted (e.g. a daily limit); fail fast instead of hanging the run.
MAX_WAIT_SECONDS = 120.0

_DURATION_PART = re.compile(r"(\d+(?:\.\d+)?)(ms|h|m|s)")
_UNIT_SECONDS = {"ms": 0.001, "s": 1.0, "m": 60.0, "h": 3600.0}


def parse_duration(value: str) -> Optional[float]:
    """Parse '7', '1.5s', '577ms' or '1h20m38.4s' into seconds (None if unparseable)."""
    value = (value or "").strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        pass
    parts = _DURATION_PART.findall(value)
    if not parts or "".join(n + u for n, u in parts) != value:
        return None
    return sum(float(n) * _UNIT_SECONDS[u] for n, u in parts)


def _server_wait(resp) -> Optional[float]:
    """How long the server says to wait before retrying, if it says."""
    headers = {k.lower(): v for k, v in (resp.headers or {}).items()}
    waits = []
    if "retry-after" in headers:
        waits.append(parse_duration(headers["retry-after"]))
    else:
        # Groq-style: the quota that is exhausted is the one that resets last.
        for key in ("x-ratelimit-reset-requests", "x-ratelimit-reset-tokens"):
            if key in headers:
                waits.append(parse_duration(headers[key]))
    waits = [w for w in waits if w is not None]
    return max(waits) if waits else None


def _http_error(resp) -> requests.HTTPError:
    """An HTTPError whose message carries the API's own explanation."""
    body = (getattr(resp, "text", "") or "").strip().replace("\n", " ")
    msg = f"{resp.status_code} {getattr(resp, 'reason', '')}".strip()
    if body:
        msg += f": {body[:300]}"
    return requests.HTTPError(msg, response=resp)


def post_with_retries(url, *, headers=None, json=None, timeout=120,
                      max_retries: int = 6, backoff: float = 2.0):
    """POST a JSON request, retrying transient failures.

    Retries on connection errors, timeouts, and transient HTTP responses
    (429 / 5xx). When the server sends Retry-After (or Groq-style rate-limit
    reset headers) we wait that long; otherwise we back off exponentially. If the
    server asks for more than MAX_WAIT_SECONDS we give up at once. Non-transient
    errors (400, 401, 404, ...) are raised immediately, with the response body
    in the message. If every attempt fails the last error is raised, so the run
    loop in core/runner.py can log it and move on instead of crashing the run.
    """
    last_err = None
    for attempt in range(max_retries):
        wait = backoff ** attempt
        try:
            resp = requests.post(url, headers=headers, json=json, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout) as e:
            last_err = e
        else:
            if resp.status_code not in RETRYABLE_STATUS:
                if resp.status_code >= 400:
                    raise _http_error(resp)
                return resp
            last_err = _http_error(resp)
            server = _server_wait(resp)
            if server is not None:
                if server > MAX_WAIT_SECONDS:
                    raise last_err
                wait = server
        if attempt < max_retries - 1:
            time.sleep(wait)
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
        return OllamaAdapter(
            host=cfg.get("host", "http://localhost:11434"),
            num_ctx=cfg.get("num_ctx"),
            **common,
        )

    if provider == "openai_compat":
        api_key_env = cfg.get("api_key_env", "OPENAI_API_KEY")
        api_key = os.environ.get(api_key_env, "")
        return OpenAICompatAdapter(
            base_url=cfg["base_url"],
            api_key=api_key,
            extra_params=cfg.get("extra_params"),
            **common,
        )

    raise ValueError(f"Unknown provider: {provider!r}. Use 'ollama' or 'openai_compat'.")
