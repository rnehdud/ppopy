"""Bounded async client for the OpenAI-compatible chat completions endpoint."""

from __future__ import annotations

import asyncio
import json
import math
import zlib

import httpx
from pydantic import ValidationError

from beauty_agent.v3_contracts import SLMRequest, SLMResponse

from ._citations import extract_citations
from .prompt_builder import build_messages
from .rule_fallback import RuleBaselineFallback

class _ResponseFailure(Exception):
    """An internal error carrying a fixed, safe fallback code."""


_COMPRESSION_WINDOWS = {"gzip": zlib.MAX_WBITS + 16, "deflate": zlib.MAX_WBITS}


async def _read_body(response: httpx.Response, limit: int) -> bytearray:
    encoding = response.headers.get("content-encoding", "identity").strip().lower()
    if encoding != "identity" and encoding not in _COMPRESSION_WINDOWS:
        raise _ResponseFailure("invalid_response")
    if encoding == "identity":
        length = response.headers.get("content-length", "").strip().lstrip("0")
        limit_text = str(limit)
        if length.isascii() and length.isdecimal() and (len(length), length) > (len(limit_text), limit_text):
            raise _ResponseFailure("response_too_large")

    # Preloaded transport responses already hold decoded content. For network
    # streams, cap each decompression call before it can inflate a whole chunk.
    body = bytearray()
    if encoding == "identity" or response.is_stream_consumed:
        async for chunk in response.aiter_bytes():
            if len(body) + len(chunk) > limit:
                raise _ResponseFailure("response_too_large")
            body.extend(chunk)
        return body

    window = _COMPRESSION_WINDOWS[encoding]
    decoder = zlib.decompressobj(window)
    try:
        async for chunk in response.aiter_raw():
            while chunk:
                if decoder.eof:
                    if encoding != "gzip":
                        raise _ResponseFailure("invalid_response")
                    decoder = zlib.decompressobj(window)
                remaining = limit - len(body)
                decoded = decoder.decompress(chunk, remaining + 1)
                if len(decoded) > remaining:
                    raise _ResponseFailure("response_too_large")
                body.extend(decoded)
                chunk = decoder.unused_data
    except zlib.error:
        raise _ResponseFailure("invalid_response") from None
    if not decoder.eof:
        raise _ResponseFailure("invalid_response")
    return body


class OpenAICompatSLMClient:
    """Generate a candidate for the Control Plane to validate before returning."""

    def __init__(
        self,
        base_url: str,
        model: str,
        *,
        api_key: str | None = None,
        temperature: float = 0.0,
        max_tokens: int | None = 1024,
        adapter_revision: str | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
        fallback: RuleBaselineFallback | None = None,
    ) -> None:
        if not math.isfinite(temperature) or not 0.0 <= temperature <= 2.0:
            raise ValueError("temperature must be between 0 and 2")
        if max_tokens is not None and max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        base_url = base_url.rstrip("/")
        api_root = base_url if base_url.endswith("/v1") else f"{base_url}/v1"
        self._endpoint = f"{api_root}/chat/completions"
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._adapter_revision = adapter_revision
        self._headers = {"Accept-Encoding": "gzip, deflate"}
        if api_key:
            self._headers["Authorization"] = f"Bearer {api_key}"
        self._transport = transport
        self._fallback = fallback if fallback is not None else RuleBaselineFallback()

    async def generate(self, request: SLMRequest) -> SLMResponse:
        messages = build_messages(request)
        try:
            content = await asyncio.wait_for(self._read_completion(request, messages), request.timeout_seconds)
            return SLMResponse(
                mode=request.mode,
                content=content,
                cited_evidence_refs=extract_citations(content),
                model=self._model,
                adapter_revision=self._adapter_revision,
            )
        except (asyncio.TimeoutError, httpx.TimeoutException):
            return self._fallback.build(request, reason="timeout")
        except httpx.HTTPStatusError:
            return self._fallback.build(request, reason="http_error")
        except (httpx.RequestError, httpx.InvalidURL):
            return self._fallback.build(request, reason="network_error")
        except _ResponseFailure as error:
            return self._fallback.build(request, reason=str(error))
        except ValidationError:
            return self._fallback.build(request, reason="invalid_response")

    async def _read_completion(self, request: SLMRequest, messages: list[dict[str, str]]) -> str:
        payload = {
            "model": self._model,
            "messages": messages,
            "stream": False,
            "temperature": self._temperature,
        }
        if self._max_tokens is not None:
            payload["max_tokens"] = self._max_tokens
        async with httpx.AsyncClient(transport=self._transport, timeout=request.timeout_seconds) as client:
            async with client.stream("POST", self._endpoint, headers=self._headers, json=payload) as response:
                response.raise_for_status()
                body = await _read_body(response, request.max_response_bytes)

        try:
            content = json.loads(body)["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError, TypeError, RecursionError):
            raise _ResponseFailure("invalid_response") from None
        if not isinstance(content, str):
            raise _ResponseFailure("invalid_response")
        if not content.strip():
            raise _ResponseFailure("empty_content")
        return content
