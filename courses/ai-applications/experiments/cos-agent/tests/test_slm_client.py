"""Wire compatibility and failure handling without a model server."""

import asyncio
import json
from pathlib import Path

import httpx
import pytest
from pydantic import ValidationError

from beauty_agent.guardrail import HardSafetyGuardrail
from beauty_agent.slm import OpenAICompatSLMClient, build_messages
from beauty_agent.v3_contracts import SLMRequest


def _generate(handler, request=None, base_url="http://model.test"):
    client = OpenAICompatSLMClient(
        base_url, "test-model", api_key="mock-key", transport=httpx.MockTransport(handler),
    )
    return asyncio.run(client.generate(request or SLMRequest(mode="solution")))


def _completion(content):
    return httpx.Response(200, json={"choices": [{"message": {"content": content}}]})


def test_wire_payload_and_citations_are_ordered_and_unique():
    def handler(req):
        assert req.method == "POST"
        assert req.url == "http://model.test/v1/chat/completions"
        assert req.headers["Authorization"] == "Bearer mock-key"
        assert req.extensions["timeout"]["read"] == 15.0
        payload = json.loads(req.content)
        assert payload == {"model": "test-model", "messages": build_messages(request), "stream": False}
        return _completion("확인된 범위에서 설명해요. [ref:two] [ref:one] [ref:two]")

    request = SLMRequest(mode="solution", allowed_evidence_refs=["ref:one", "ref:two"])
    result = _generate(handler, request, base_url="http://model.test/v1/")
    assert result.provider == "openai_compat"
    assert result.cited_evidence_refs == ["ref:two", "ref:one"]
    assert not result.fallback_used


def test_prompt_matches_stage1_training_messages():
    path = Path(__file__).resolve().parents[1] / "data/qlora/v2/qlora_solution_hold_v2.jsonl"
    with path.open(encoding="utf-8") as stream:
        rows = [json.loads(next(stream)) for _ in range(2)]
        rows.append(next(row for line in stream if (row := json.loads(line))["mode"] == "hold"))

    for row in rows:
        system, user, _ = row["messages"]
        request = SLMRequest.model_validate_json(user["content"])
        messages = build_messages(request)
        assert messages[0] == system
        assert messages[1]["role"] == "user"
        actual = json.loads(messages[1]["content"])
        assert actual == json.loads(user["content"])
        assert "kb_judgments" not in actual
        if request.mode == "hold":
            assert actual["rag_chunks"] == []


def test_question_and_non_solution_rag_are_rejected():
    with pytest.raises(ValidationError):
        SLMRequest(mode="question")
    with pytest.raises(ValueError, match="require solution"):
        build_messages(SLMRequest(mode="hold").model_copy(update={"rag_chunks": [object()]}))
    assert json.loads(build_messages(SLMRequest(mode="nlu"))[1]["content"])["mode"] == "nlu"


@pytest.mark.parametrize(
    ("status", "body", "reason"),
    [
        (500, b"mock-key and server trace", "http_error"),
        (400, b"mock-key and server trace", "http_error"),
        (200, b"not json", "invalid_response"),
        (200, b'{"choices": []}', "invalid_response"),
        (200, b'{"choices":[{"message":{"content":{}}}]}', "invalid_response"),
        (200, b'{"choices":[{"message":{"content":" "}}]}', "empty_content"),
    ],
)
def test_http_error_and_invalid_payload_fallback(status, body, reason):
    result = _generate(lambda _: httpx.Response(status, content=body))
    assert result.provider == "rule_baseline_fallback"
    assert result.fallback_used and result.fallback_reason == reason
    assert "mock-key" not in result.content
    assert result.cited_evidence_refs == []


@pytest.mark.parametrize(("error", "reason"), [(httpx.ReadTimeout, "timeout"), (httpx.ConnectError, "network_error")])
def test_transport_error_uses_safe_hold_fallback(error, reason):
    def handler(req):
        raise error("mock-key URL details", request=req)

    result = _generate(handler, SLMRequest(mode="hold"))
    assert result.mode == "hold"
    assert result.fallback_used and result.fallback_reason == reason
    assert not result.cited_evidence_refs
    assert "보류" in result.content
    assert "mock-key" not in result.model_dump_json()


def test_total_deadline_cancels_slow_transport():
    cancelled = False

    async def handler(_):
        nonlocal cancelled
        try:
            await asyncio.sleep(10)
        finally:
            cancelled = True

    result = _generate(handler, SLMRequest(mode="solution", timeout_seconds=0.025))
    assert cancelled
    assert result.fallback_used and result.fallback_reason == "timeout"


def test_stream_without_content_length_stops_as_soon_as_limit_is_exceeded():
    class OversizeStream(httpx.AsyncByteStream):
        def __init__(self):
            self.closed = False

        async def __aiter__(self):
            yield b"x" * 32768
            yield b"x" * 32769
            pytest.fail("transport consumed another chunk after crossing 64 KiB")

        async def aclose(self):
            self.closed = True

    stream = OversizeStream()
    result = _generate(lambda _: httpx.Response(200, stream=stream))
    assert result.fallback_used and result.fallback_reason == "response_too_large"
    assert stream.closed


def test_per_request_byte_limit_is_honored_even_with_cached_transport_body():
    result = _generate(lambda _: _completion("조금 긴 응답"), SLMRequest(mode="solution", max_response_bytes=24))
    assert result.fallback_used and result.fallback_reason == "response_too_large"


def test_guardrail_can_validate_a_model_candidate_and_report_flags():
    request = SLMRequest(mode="solution")
    candidate = _generate(lambda _: _completion("예시 응답 [kb:B-C01]"), request)
    assert candidate.provider == "openai_compat"
    checked = HardSafetyGuardrail().validate(request, candidate)
    assert "kb_citation" in checked.flags
    assert checked.safe_response.fallback_reason == "guardrail_blocked"
    assert checked.safe_response.cited_evidence_refs == []
