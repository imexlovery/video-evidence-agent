"""Minimal real-model interface for evidence-constrained P0-A answers."""

from __future__ import annotations

import json
import os
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from video_evidence_agent.schemas import AnswerProposal, AnswerStatus, RetrievalHit

# Load only the project-local, gitignored file. Existing process environment
# values win, so CI and explicit shell exports remain authoritative.
load_dotenv(Path(__file__).resolve().parents[2] / ".env", override=False)


class AnsweringConfigurationError(RuntimeError):
    """Raised when no real answer-model credential/configuration is present."""


class AnsweringProviderError(RuntimeError):
    """Raised when the configured real provider cannot return an answer."""


@dataclass(frozen=True)
class AnswerTrace:
    """P0-B observability around one transcript-retrieval answer call."""

    proposal: AnswerProposal
    provider: str
    model: str
    latency_ms: int
    usage: dict[str, Any]
    raw_response: dict[str, Any] | str | None
    schema_valid: bool


SYSTEM_INSTRUCTION = """
You answer questions about one Chinese technical video.
Use only the supplied Top-K transcript segments as evidence. Do not use outside
knowledge or infer facts that are not supported by those segments. If the
evidence is insufficient, return the refusal shape. Return one JSON object with
exactly these keys: status, answer, citation_segment_ids.

For a supported answer, status must be ANSWERED, answer must be concise Chinese,
and citation_segment_ids must contain one or more IDs from the supplied segments.
For an unsupported answer, return:
{"status":"INSUFFICIENT_EVIDENCE","answer":null,"citation_segment_ids":[]}
""".strip()


def _configured_client() -> tuple[OpenAI, str]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("VIDEO_EVIDENCE_MODEL", "").strip()
    if not api_key:
        raise AnsweringConfigurationError("OPENAI_API_KEY is required; no mock fallback exists")
    if not model:
        raise AnsweringConfigurationError(
            "VIDEO_EVIDENCE_MODEL is required; no implicit provider model is selected"
        )

    base_url = os.getenv("OPENAI_BASE_URL", "").strip()
    options: dict[str, Any] = {"api_key": api_key}
    if base_url:
        options["base_url"] = base_url
    timeout_seconds = float(os.getenv("VIDEO_EVIDENCE_TIMEOUT_SECONDS", "120"))
    if timeout_seconds <= 0:
        raise AnsweringConfigurationError("VIDEO_EVIDENCE_TIMEOUT_SECONDS must be positive")
    options["timeout"] = timeout_seconds
    return OpenAI(**options), model


def _context(question: str, hits: list[RetrievalHit]) -> str:
    payload = {
        "question": question,
        "top_k_segments": [
            {
                "segment_id": hit.segment.segment_id,
                "start_ms": hit.segment.start_ms,
                "end_ms": hit.segment.end_ms,
                "transcript_text": hit.segment.transcript_text,
            }
            for hit in hits
        ],
    }
    return json.dumps(payload, ensure_ascii=False)


def _invalid_model_output() -> AnswerProposal:
    return AnswerProposal(
        status=AnswerStatus.INSUFFICIENT_EVIDENCE,
        answer=None,
        citation_segment_ids=[],
    )


def _jsonable_response(response: Any) -> dict[str, Any] | str:
    """Serialize provider output without emitting request credentials."""

    try:
        model_dump = response.model_dump(mode="json")
    except (AttributeError, TypeError, ValueError):
        try:
            model_dump = json.loads(response.model_dump_json())
        except (AttributeError, TypeError, ValueError, json.JSONDecodeError):
            return type(response).__name__
    return model_dump if isinstance(model_dump, dict) else str(model_dump)


def _usage_payload(response: Any) -> dict[str, Any]:
    usage = getattr(response, "usage", None)
    if usage is None:
        return {}
    try:
        payload = usage.model_dump(mode="json")
    except (AttributeError, TypeError, ValueError):
        payload = {}
    return payload if isinstance(payload, dict) else {}


def request_answer_traced(
    question: str,
    retrieval_hits: Iterable[RetrievalHit],
    *,
    system_instruction: str | None = None,
) -> AnswerTrace:
    """Call a configured real provider and retain one immutable call trace."""

    hits = list(retrieval_hits)
    if not question.strip():
        raise AnsweringProviderError("question must not be blank")
    if not hits:
        raise AnsweringProviderError("answering requires at least one retrieval hit")

    client, model = _configured_client()
    started_at = perf_counter()
    instruction = SYSTEM_INSTRUCTION
    if system_instruction and system_instruction.strip():
        instruction = (
            f"{SYSTEM_INSTRUCTION}\n\nFrozen P0-B instruction:\n{system_instruction.strip()}"
        )
    try:
        response = client.chat.completions.create(
            model=model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": _context(question, hits)},
            ],
        )
    except Exception as exc:
        raise AnsweringProviderError(f"real answer provider failed: {type(exc).__name__}") from exc

    latency_ms = round((perf_counter() - started_at) * 1000)
    raw_response = _jsonable_response(response)
    usage = _usage_payload(response)
    if not response.choices or response.choices[0].message.content is None:
        return AnswerTrace(
            proposal=_invalid_model_output(),
            provider=os.getenv("OPENAI_BASE_URL", "openai-compatible") or "openai-compatible",
            model=model,
            latency_ms=latency_ms,
            usage=usage,
            raw_response=raw_response,
            schema_valid=False,
        )
    try:
        payload = json.loads(response.choices[0].message.content)
        proposal = AnswerProposal.model_validate(payload)
    except (json.JSONDecodeError, ValueError, TypeError):
        return AnswerTrace(
            proposal=_invalid_model_output(),
            provider=os.getenv("OPENAI_BASE_URL", "openai-compatible") or "openai-compatible",
            model=model,
            latency_ms=latency_ms,
            usage=usage,
            raw_response=raw_response,
            schema_valid=False,
        )
    return AnswerTrace(
        proposal=proposal,
        provider=os.getenv("OPENAI_BASE_URL", "openai-compatible") or "openai-compatible",
        model=model,
        latency_ms=latency_ms,
        usage=usage,
        raw_response=raw_response,
        schema_valid=True,
    )


def request_answer(question: str, retrieval_hits: Iterable[RetrievalHit]) -> AnswerProposal:
    """Compatibility wrapper for P0-A callers."""

    return request_answer_traced(question, retrieval_hits).proposal
