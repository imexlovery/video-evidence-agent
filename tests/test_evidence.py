from video_evidence_agent.evidence import gate_answer
from video_evidence_agent.schemas import AnswerProposal, AnswerStatus, RetrievalHit, VideoSegment


def _hit() -> RetrievalHit:
    segment = VideoSegment(
        video_id="smoke-001",
        segment_id="smoke-001-seg-000",
        ordinal=0,
        start_ms=12_000,
        end_ms=42_000,
        transcript_text="讲者说明应先完成离线评测，再决定是否上线。",
        source_asr_ordinals=(3, 4),
    )
    return RetrievalHit(rank=1, score=0.9, segment=segment)


def test_gate_refills_quote_from_retrieved_source() -> None:
    hit = _hit()
    proposal = AnswerProposal(
        status=AnswerStatus.ANSWERED,
        answer="讲者建议先完成离线评测。",
        citation_segment_ids=[hit.segment.segment_id],
    )

    decision = gate_answer(proposal, [hit])

    assert decision.result.status is AnswerStatus.ANSWERED
    assert decision.result.evidence[0].quote == hit.segment.transcript_text
    assert decision.result.evidence[0].start_ms == 12_000


def test_gate_rejects_citation_outside_current_top_k() -> None:
    proposal = AnswerProposal(
        status=AnswerStatus.ANSWERED,
        answer="这个答案不应通过。",
        citation_segment_ids=["other-video-seg-000"],
    )

    decision = gate_answer(proposal, [_hit()])

    assert decision.result.status is AnswerStatus.INSUFFICIENT_EVIDENCE
    assert decision.result.answer is None
    assert decision.result.evidence == []


def test_gate_rejects_answer_with_no_citations() -> None:
    malformed = AnswerProposal.model_construct(
        status=AnswerStatus.ANSWERED,
        answer="没有证据的答案。",
        citation_segment_ids=[],
    )

    decision = gate_answer(malformed, [_hit()])

    assert decision.result.status is AnswerStatus.INSUFFICIENT_EVIDENCE
