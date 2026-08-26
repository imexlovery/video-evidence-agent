"""Deterministic provenance gate for answer-model citations."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from video_evidence_agent.schemas import (
    AnswerProposal,
    AnswerResult,
    AnswerStatus,
    Citation,
    RetrievalHit,
)


class EvidenceGateError(RuntimeError):
    """Raised when the local retrieval context itself violates its contract."""


@dataclass(frozen=True)
class GateDecision:
    result: AnswerResult
    reason: str


def _refusal(reason: str) -> GateDecision:
    return GateDecision(
        result=AnswerResult(
            status=AnswerStatus.INSUFFICIENT_EVIDENCE,
            answer=None,
            evidence=[],
        ),
        reason=reason,
    )


def gate_answer(
    proposal: AnswerProposal,
    retrieval_hits: Iterable[RetrievalHit],
) -> GateDecision:
    """Permit only answer citations that originated in this exact Top-K set."""

    hits = list(retrieval_hits)
    if not hits:
        raise EvidenceGateError("Evidence Gate requires at least one retrieval hit")
    video_ids = {hit.segment.video_id for hit in hits}
    if len(video_ids) != 1:
        raise EvidenceGateError("Evidence Gate received cross-video retrieval hits")

    if proposal.status is AnswerStatus.INSUFFICIENT_EVIDENCE:
        return _refusal("model_declared_insufficient_evidence")
    if not proposal.answer or not proposal.citation_segment_ids:
        return _refusal("answered_proposal_missing_answer_or_citation")

    allowed = {hit.segment.segment_id: hit.segment for hit in hits}
    evidence: list[Citation] = []
    seen_ids: set[str] = set()
    for segment_id in proposal.citation_segment_ids:
        segment = allowed.get(segment_id)
        if segment is None:
            return _refusal("citation_not_in_current_top_k")
        if segment.video_id not in video_ids:
            return _refusal("citation_not_in_current_video")
        if segment_id in seen_ids:
            continue
        seen_ids.add(segment_id)
        evidence.append(
            Citation(
                segment_id=segment.segment_id,
                start_ms=segment.start_ms,
                end_ms=segment.end_ms,
                quote=segment.transcript_text,
            )
        )

    if not evidence:
        return _refusal("answered_proposal_has_no_unique_citations")
    return GateDecision(
        result=AnswerResult(
            status=AnswerStatus.ANSWERED,
            answer=proposal.answer.strip(),
            evidence=evidence,
        ),
        reason="citation_provenance_verified",
    )
