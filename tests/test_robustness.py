"""Offline tests for the hosted-API plumbing: retries, adapters, error
accounting in the runner/scorer, and confidence intervals.

Nothing here touches the network; HTTP is replaced with small fakes.
"""
import json

import pytest
import requests

from core.runner import run_model
from core.scorer import score, wilson_interval
from models import base
from models.openai_adapter import OpenAICompatAdapter


# ---------- fake HTTP plumbing ----------

class FakeResp:
    def __init__(self, status=200, body=None, headers=None, text=None):
        self.status_code = status
        self._body = body if body is not None else {}
        self.headers = headers or {}
        self.reason = "Fake"
        self.text = text if text is not None else json.dumps(self._body)

    def json(self):
        return self._body

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} Fake", response=self)


def _ok(content="FINAL ANSWER: B", finish="stop"):
    return FakeResp(200, {"choices": [{"message": {"content": content},
                                       "finish_reason": finish}]})


@pytest.fixture
def no_sleep(monkeypatch):
    waits = []
    monkeypatch.setattr(base.time, "sleep", lambda s: waits.append(s))
    return waits


# ---------- retry behaviour ----------

def test_retry_honours_retry_after_header(monkeypatch, no_sleep):
    seq = [FakeResp(429, headers={"Retry-After": "7"}), _ok()]
    monkeypatch.setattr(base.requests, "post", lambda *a, **k: seq.pop(0))
    resp = base.post_with_retries("http://x", json={})
    assert resp.status_code == 200
    assert no_sleep == [7.0]


def test_retry_parses_groq_style_reset_header(monkeypatch, no_sleep):
    seq = [FakeResp(429, headers={"x-ratelimit-reset-tokens": "1.5s"}), _ok()]
    monkeypatch.setattr(base.requests, "post", lambda *a, **k: seq.pop(0))
    base.post_with_retries("http://x", json={})
    assert no_sleep == [1.5]


def test_retry_gives_up_at_once_when_quota_reset_is_far_away(monkeypatch, no_sleep):
    # e.g. a daily quota that resets in an hour: waiting is pointless.
    resp = FakeResp(429, headers={"x-ratelimit-reset-requests": "1h20m38.4s"})
    monkeypatch.setattr(base.requests, "post", lambda *a, **k: resp)
    with pytest.raises(requests.HTTPError):
        base.post_with_retries("http://x", json={})
    assert no_sleep == []


def test_http_error_message_includes_response_body(monkeypatch, no_sleep):
    resp = FakeResp(400, text='{"error": {"message": "bad param foo"}}')
    monkeypatch.setattr(base.requests, "post", lambda *a, **k: resp)
    with pytest.raises(requests.HTTPError) as ei:
        base.post_with_retries("http://x", json={})
    assert "bad param foo" in str(ei.value)


# ---------- OpenAI-compatible adapter ----------

def _adapter(**kw):
    return OpenAICompatAdapter(base_url="http://x", api_key="k", name="m",
                               model_id="gpt-5-mini", **kw)


def test_adapter_switches_to_max_completion_tokens(monkeypatch, no_sleep):
    payloads = []

    def fake_post(url, headers=None, json=None, timeout=None, **_):
        payloads.append(dict(json))
        if "max_tokens" in json:
            return FakeResp(400, text="Unsupported parameter: 'max_tokens' is not "
                                      "supported with this model. Use "
                                      "'max_completion_tokens' instead.")
        return _ok()

    monkeypatch.setattr(base.requests, "post", fake_post)
    a = _adapter()
    assert a.ask([{"role": "user", "content": "hi"}]) == "FINAL ANSWER: B"
    assert "max_completion_tokens" in payloads[-1] and "max_tokens" not in payloads[-1]
    # The learned setting is remembered: the next call goes straight through.
    a.ask([{"role": "user", "content": "hi"}])
    assert len(payloads) == 3


def test_adapter_drops_unsupported_temperature(monkeypatch, no_sleep):
    payloads = []

    def fake_post(url, headers=None, json=None, timeout=None, **_):
        payloads.append(dict(json))
        if "temperature" in json:
            return FakeResp(400, text="Unsupported value: 'temperature' does not "
                                      "support 0 with this model.")
        return _ok()

    monkeypatch.setattr(base.requests, "post", fake_post)
    a = _adapter()
    a.ask([{"role": "user", "content": "hi"}])
    assert "temperature" not in payloads[-1]


def test_adapter_passes_extra_params(monkeypatch, no_sleep):
    seen = {}

    def fake_post(url, headers=None, json=None, timeout=None, **_):
        seen.update(json)
        return _ok()

    monkeypatch.setattr(base.requests, "post", fake_post)
    _adapter(extra_params={"reasoning_effort": "minimal"}).ask(
        [{"role": "user", "content": "hi"}])
    assert seen["reasoning_effort"] == "minimal"


def test_adapter_flags_reply_cut_off_before_any_text(monkeypatch, no_sleep):
    # A reasoning model that spends its whole budget thinking returns "".
    monkeypatch.setattr(base.requests, "post",
                        lambda *a, **k: _ok(content="", finish="length"))
    with pytest.raises(RuntimeError, match="max_tokens"):
        _adapter().ask([{"role": "user", "content": "hi"}])


# ---------- errors must not be scored as wrong answers ----------

Q = {"id": "q1", "question": "Q?", "answer_letter": "B",
     "options": {"A": "a", "B": "b", "C": "c", "D": "d"}}


class FlakyAdapter:
    name = "Flaky"

    def __init__(self, fail_on=()):
        self.calls = 0
        self.fail_on = set(fail_on)

    def ask(self, messages):
        self.calls += 1
        if self.calls in self.fail_on:
            raise requests.HTTPError("429 Too Many Requests")
        return "FINAL ANSWER: B"


def _score(tmp_path, adapter, questions, pressures=("P1",)):
    jsonl, csv = tmp_path / "raw.jsonl", tmp_path / "s.csv"
    run_model(adapter, questions, list(pressures), jsonl)
    return score(jsonl, csv)


def test_failed_baseline_is_not_counted_as_a_wrong_answer(tmp_path):
    qs = [dict(Q, id="q1"), dict(Q, id="q2")]
    df = _score(tmp_path, FlakyAdapter(fail_on={1}), qs)
    row = df.iloc[0]
    assert row["baseline_errors"] == 1
    assert row["baseline_n"] == 1          # only the call that really answered
    assert row["baseline_acc"] == 1.0


def test_failed_pressure_call_is_excluded_from_flip_denominator(tmp_path):
    # call 1 = baseline, call 2 = pressure P1 (fails)
    df = _score(tmp_path, FlakyAdapter(fail_on={2}), [Q])
    row = df.iloc[0]
    assert row["pressure_errors"] == 1
    assert row["tested_n"] == 0


def test_runner_aborts_a_model_after_many_consecutive_errors(tmp_path):
    adapter = FlakyAdapter(fail_on=range(1, 1000))
    qs = [dict(Q, id=f"q{i}") for i in range(50)]
    run_model(adapter, qs, ["P1"], tmp_path / "raw.jsonl", max_consecutive_errors=5)
    assert adapter.calls == 5


# ---------- confidence intervals ----------

def test_wilson_interval_known_values():
    lo, hi = wilson_interval(0, 10)
    assert lo == 0.0 and hi == pytest.approx(0.2775, abs=1e-3)
    lo, hi = wilson_interval(5, 10)
    assert (lo, hi) == pytest.approx((0.2366, 0.7634), abs=1e-3)
    assert wilson_interval(0, 0) == (0.0, 0.0)


def test_adapter_adaptation_is_idempotent_for_concurrent_workers(monkeypatch, no_sleep):
    # Eight workers all see the same 400 before any of them has adapted. The
    # first one flips the setting; the other seven must still retry, not give up.
    a = _adapter()
    err = requests.HTTPError("400", response=FakeResp(
        400, text="Unsupported parameter: 'max_tokens'. Use 'max_completion_tokens' instead."))
    assert a._adapt_to_error(err) is True
    assert a._token_param == "max_completion_tokens"
    assert a._adapt_to_error(err) is True          # a late arrival: retry, do not raise
    terr = requests.HTTPError("400", response=FakeResp(
        400, text="Unsupported value: 'temperature' does not support 0 with this model."))
    assert a._adapt_to_error(terr) is True and a._send_temperature is False
    assert a._adapt_to_error(terr) is True
    other = requests.HTTPError("400", response=FakeResp(400, text="messages: invalid"))
    assert a._adapt_to_error(other) is False


def test_parallel_adaptation_end_to_end(monkeypatch, no_sleep):
    from concurrent.futures import ThreadPoolExecutor

    def fake_post(url, headers=None, json=None, timeout=None, **_):
        if "max_tokens" in json:
            return FakeResp(400, text="Unsupported parameter: 'max_tokens'. "
                                      "Use 'max_completion_tokens' instead.")
        if "temperature" in json:
            return FakeResp(400, text="Unsupported value: 'temperature' does not support 0.")
        return _ok()

    monkeypatch.setattr(base.requests, "post", fake_post)
    a = _adapter()
    with ThreadPoolExecutor(max_workers=8) as pool:
        replies = list(pool.map(lambda _: a.ask([{"role": "user", "content": "hi"}]), range(40)))
    assert replies == ["FINAL ANSWER: B"] * 40
