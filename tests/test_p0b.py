import pytest

from video_evidence_agent.p0b_eval import _grade_one, _retrieval_metrics
from video_evidence_agent.p0b_schemas import (
    CorpusRecord,
    EvaluationMethod,
    GoldEvidenceUnit,
    P0BGoldRecord,
    P0BQuestion,
    P0BValidationError,
    QuestionType,
    validate_p0b_dataset,
)
from video_evidence_agent.schemas import AnswerStatus, RetrievalHit, VideoSegment


def _corpus() -> list[CorpusRecord]:
    return [
        CorpusRecord(
            video_id=f"p0b-v0{index}",
            source_url=f"https://example.test/p0b-v0{index}",
            use_basis="公开技术视频，本地非商业离线评估",
            license="CC BY 4.0",
            attribution="Example publisher",
            local_path_alias=f"p0b-v0{index}.mp4",
            media_sha256="a" * 64,
            duration_ms=60_000,
            language="zh",
            content_type="developer_talk",
            sensitivity="public",
            ingest_artifact_relpath=f"artifacts/p0b/p0b-r1/videos/p0b-v0{index}",
        )
        for index in range(1, 4)
    ]


def _questions() -> list[P0BQuestion]:
    question_types = [
        QuestionType.SINGLE_LEXICAL,
        QuestionType.SINGLE_PARAPHRASE,
        QuestionType.MULTI_EVIDENCE,
        QuestionType.UNANSWERABLE,
    ]
    return [
        P0BQuestion(
            question_id=f"p0b-v0{video_index}-q{question_index}",
            video_id=f"p0b-v0{video_index}",
            question_type=question_type,
            question=f"第 {video_index} 个视频的第 {question_index} 个问题？",
            should_answer=question_type is not QuestionType.UNANSWERABLE,
        )
        for video_index in range(1, 4)
        for question_index, question_type in enumerate(question_types, start=1)
    ]


def _gold(question: P0BQuestion) -> P0BGoldRecord:
    if question.question_type is QuestionType.UNANSWERABLE:
        return P0BGoldRecord(
            eval_revision="p0b-r1",
            question_id=question.question_id,
            video_id=question.video_id,
            question_type=question.question_type,
            question=question.question,
            should_answer=False,
            unanswerable_rationale="完整 transcript 和原视频复核均没有该事实。",
            annotator_status="USER_CONFIRMED",
        )
    return P0BGoldRecord(
        eval_revision="p0b-r1",
        question_id=question.question_id,
        video_id=question.video_id,
        question_type=question.question_type,
        question=question.question,
        should_answer=True,
        gold_evidence_units=[
            GoldEvidenceUnit(
                unit_id="e01",
                start_ms=100,
                end_ms=200,
                gold_segment_ids=[f"{question.video_id}-seg-000"],
            )
        ],
        answer_points=["一个必须覆盖的语义要点"],
        annotator_status="USER_CONFIRMED",
    )


def _segment(segment_id: str, start_ms: int, end_ms: int) -> VideoSegment:
    return VideoSegment(
        video_id="p0b-v01",
        segment_id=segment_id,
        ordinal=int(segment_id.rsplit("-", 1)[-1]),
        start_ms=start_ms,
        end_ms=end_ms,
        transcript_text="测试证据文本",
        source_asr_ordinals=(0,),
    )


def test_p0b_dataset_freezes_three_videos_and_four_question_types() -> None:
    questions = _questions()
    gold = [_gold(question) for question in questions]

    validate_p0b_dataset(_corpus(), questions, gold, eval_revision="p0b-r1")

    with pytest.raises(P0BValidationError, match="exactly 12"):
        validate_p0b_dataset(_corpus(), questions[:-1], eval_revision="p0b-r1")


def test_retrieval_grader_treats_half_overlap_as_hit_but_boundary_touch_as_miss() -> None:
    question = _questions()[0]
    gold = _gold(question)
    hits = [
        RetrievalHit(rank=1, score=0.9, segment=_segment("p0b-v01-seg-000", 0, 149)),
        RetrievalHit(rank=2, score=0.8, segment=_segment("p0b-v01-seg-001", 50, 150)),
    ]

    metrics = _retrieval_metrics(hits, gold)

    assert metrics["question_hit_at_1"] is False
    assert metrics["question_hit_at_5"] is True
    assert metrics["all_evidence_at_5"] is True
    assert metrics["mrr"] == pytest.approx(0.5)


def test_transcript_retrieval_grade_separates_provenance_from_human_support() -> None:
    question = _questions()[0]
    gold = _gold(question)
    segment = _segment("p0b-v01-seg-000", 0, 300)
    result = {
        "evaluation_method": EvaluationMethod.TRANSCRIPT_RETRIEVAL.value,
        "call_status": "SUCCEEDED",
        "answer_status": AnswerStatus.ANSWERED,
        "answer": "答案",
        "evidence": [
            {
                "segment_id": segment.segment_id,
                "start_ms": segment.start_ms,
                "end_ms": segment.end_ms,
                "quote": segment.transcript_text,
            }
        ],
        "gate_reason": "citation_provenance_verified",
    }
    row = _grade_one(
        evaluation_method=EvaluationMethod.TRANSCRIPT_RETRIEVAL,
        question=question,
        gold=gold,
        result=result,
        retrieval_hits=[RetrievalHit(rank=1, score=1.0, segment=segment)],
        review_row=None,
    )

    assert row["evaluation_method"] == "TRANSCRIPT_RETRIEVAL"
    assert row["answer_status_accuracy"] is True
    assert row["citation_provenance_verified"] is True
    assert row["citation_temporal_hit"] is True
    assert row["fully_supported_answer"] is None


def test_unanswerable_retrieval_metrics_are_not_counted_as_ranked_hits() -> None:
    question = _questions()[3]
    gold = _gold(question)

    metrics = _retrieval_metrics([], gold)

    assert metrics["question_hit_at_1"] is None
    assert metrics["question_hit_at_5"] is None
    assert metrics["mrr"] is None
