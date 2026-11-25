"""Bounded async client for the OpenAI-compatible chat completions endpoint."""

from __future__ import annotations

import asyncio
import json

import httpx
from pydantic import ValidationError

from beauty_agent.v3_contracts import SLMRequest, SLMResponse

from ._citations import extract_citations
from .prompt_builder import build_messages
from .rule_fallback import RuleBaselineFallback

class _ResponseFailure(Exception):
    """An internal error carrying a fixed, safe fallback code."""


class OpenAICompatSLMClient:
    """Generate a candidate for the Control Plane to validate before returning."""

    def __init__(
        self,
        base_url: str,
        model: str,
        *,
        api_key: str | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
        fallback: RuleBaselineFallback | None = None,
    ) -> None:
        base_url = base_url.rstrip("/")
        api_root = base_url if base_url.endswith("/v1") else f"{base_url}/v1"
        self._endpoint = f"{api_root}/chat/completions"
        self._model = model
        self._headers = {"Accept-Encoding": "identity"}
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
        payload = {"model": self._model, "messages": messages, "stream": False}
        body = bytearray()
        async with httpx.AsyncClient(transport=self._transport, timeout=request.timeout_seconds) as client:
            async with client.stream("POST", self._endpoint, headers=self._headers, json=payload) as response:
                response.raise_for_status()
                length = response.headers.get("content-length", "").strip().lstrip("0")
                limit = str(request.max_response_bytes)
                if length.isascii() and length.isdecimal() and (len(length), length) > (len(limit), limit):
                    raise _ResponseFailure("response_too_large")
                if response.headers.get("content-encoding", "identity").lower() != "identity":
                    raise _ResponseFailure("invalid_response")

                async for chunk in response.aiter_bytes():
                    if len(body) + len(chunk) > request.max_response_bytes:
                        raise _ResponseFailure("response_too_large")
                    body.extend(chunk)

        try:
            content = json.loads(body)["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError, TypeError, RecursionError):
            raise _ResponseFailure("invalid_response") from None
        if not isinstance(content, str):
            raise _ResponseFailure("invalid_response")
        if not content.strip():
            raise _ResponseFailure("empty_content")
        return content
