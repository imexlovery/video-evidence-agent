"""Minimal real-model interface for evidence-constrained P0-A answers."""

from __future__ import annotations

import json
import os
from collections.abc import Iterable
from pathlib import Path
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


def request_answer(question: str, retrieval_hits: Iterable[RetrievalHit]) -> AnswerProposal:
    """Call a configured real provider, never a local or mock answer fallback."""

    hits = list(retrieval_hits)
    if not question.strip():
        raise AnsweringProviderError("question must not be blank")
    if not hits:
        raise AnsweringProviderError("answering requires at least one retrieval hit")

    client, model = _configured_client()
    try:
        response = client.chat.completions.create(
            model=model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": _context(question, hits)},
            ],
        )
    except Exception as exc:
        raise AnsweringProviderError(f"real answer provider failed: {type(exc).__name__}") from exc

    if not response.choices or response.choices[0].message.content is None:
        return _invalid_model_output()
    try:
        payload = json.loads(response.choices[0].message.content)
        return AnswerProposal.model_validate(payload)
    except (json.JSONDecodeError, ValueError, TypeError):
        return _invalid_model_output()
