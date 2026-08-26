"""Frozen data contracts and validators for the P0-B retrieval evaluation."""

from __future__ import annotations

import json
from collections.abc import Iterable
from enum import StrEnum
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from video_evidence_agent.schemas import VideoSegment


class P0BValidationError(ValueError):
    """Raised when a P0-B input would make the locked evaluation ambiguous."""


class QuestionType(StrEnum):
    SINGLE_LEXICAL = "SINGLE_LEXICAL"
    SINGLE_PARAPHRASE = "SINGLE_PARAPHRASE"
    MULTI_EVIDENCE = "MULTI_EVIDENCE"
    UNANSWERABLE = "UNANSWERABLE"


class EvaluationMethod(StrEnum):
    """The one formally evaluated P0-B method."""

    TRANSCRIPT_RETRIEVAL = "TRANSCRIPT_RETRIEVAL"


class P0BQuestion(BaseModel):
    """The only question fields passed to the answer method."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    question_id: str = Field(min_length=1)
    video_id: str = Field(min_length=1)
    question_type: QuestionType
    question: str = Field(min_length=1)
    should_answer: bool

    @field_validator("question", "question_id", "video_id")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("P0-B identifiers and questions must not be blank")
        return value.strip()

    @model_validator(mode="after")
    def question_type_matches_answerability(self) -> "P0BQuestion":
        if self.question_type is QuestionType.UNANSWERABLE and self.should_answer:
            raise ValueError("UNANSWERABLE questions must set should_answer=false")
        if self.question_type is not QuestionType.UNANSWERABLE and not self.should_answer:
            raise ValueError("answerable question types must set should_answer=true")
        return self


class GoldEvidenceUnit(BaseModel):
    """A human-labelled semantic interval and its accepted retrieval units."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    unit_id: str = Field(min_length=1)
    start_ms: int = Field(ge=0)
    end_ms: int = Field(ge=1)
    gold_segment_ids: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_interval_and_ids(self) -> "GoldEvidenceUnit":
        if self.end_ms <= self.start_ms:
            raise ValueError("Gold evidence intervals must be positive")
        if len(set(self.gold_segment_ids)) != len(self.gold_segment_ids):
            raise ValueError("Gold segment IDs must be unique within one evidence unit")
        if any(not segment_id.strip() for segment_id in self.gold_segment_ids):
            raise ValueError("Gold segment IDs must not be blank")
        return self


class P0BGoldRecord(BaseModel):
    """Human-only answer key. This file must never be passed to the answer method."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    eval_revision: str = Field(min_length=1)
    question_id: str = Field(min_length=1)
    video_id: str = Field(min_length=1)
    question_type: QuestionType
    question: str = Field(min_length=1)
    should_answer: bool
    gold_evidence_units: list[GoldEvidenceUnit] = Field(default_factory=list)
    answer_points: list[str] = Field(default_factory=list)
    unanswerable_rationale: str | None = None
    annotator_status: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_answer_key_shape(self) -> "P0BGoldRecord":
        if self.question_type is QuestionType.UNANSWERABLE:
            if self.should_answer:
                raise ValueError("UNANSWERABLE gold must set should_answer=false")
            if self.gold_evidence_units or self.answer_points:
                raise ValueError("UNANSWERABLE gold cannot contain evidence or answer points")
            if not self.unanswerable_rationale or not self.unanswerable_rationale.strip():
                raise ValueError("UNANSWERABLE gold needs a review rationale")
        else:
            if not self.should_answer:
                raise ValueError("answerable gold must set should_answer=true")
            if not self.gold_evidence_units:
                raise ValueError("answerable gold needs at least one evidence unit")
            if not self.answer_points or any(not point.strip() for point in self.answer_points):
                raise ValueError("answerable gold needs non-empty answer points")
            if self.unanswerable_rationale is not None:
                raise ValueError("answerable gold cannot contain an unanswerable rationale")
        return self


class CorpusRecord(BaseModel):
    """Versioned metadata for one natural continuous Chinese technical video."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    video_id: str = Field(min_length=1)
    source_url: str = Field(min_length=1)
    use_basis: str = Field(min_length=1)
    license: str = Field(min_length=1)
    attribution: str = Field(min_length=1)
    local_path_alias: str = Field(min_length=1)
    media_sha256: str = Field(min_length=64, max_length=64)
    duration_ms: int = Field(ge=1)
    language: str = Field(min_length=1)
    content_type: str = Field(min_length=1)
    sensitivity: str = Field(min_length=1)
    ingest_artifact_relpath: str = Field(min_length=1)

    @field_validator("media_sha256")
    @classmethod
    def validate_sha256(cls, value: str) -> str:
        normalized = value.lower()
        if len(normalized) != 64 or any(
            character not in "0123456789abcdef" for character in normalized
        ):
            raise ValueError("media_sha256 must be a 64-character hexadecimal SHA-256")
        return normalized

    @model_validator(mode="after")
    def validate_language_and_metadata(self) -> "CorpusRecord":
        if self.language.lower() not in {"zh", "zh-cn", "中文", "chinese"}:
            raise ValueError("P0-B corpus records must identify Chinese primary speech")
        for field_name in (
            "source_url",
            "use_basis",
            "license",
            "attribution",
            "local_path_alias",
            "ingest_artifact_relpath",
        ):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must not be blank")
        return self


ModelT = TypeVar("ModelT", bound=BaseModel)


def load_jsonl(path: Path, model_type: type[ModelT]) -> list[ModelT]:
    """Load one strict Pydantic object per non-empty JSONL line."""

    if not path.is_file():
        raise P0BValidationError(f"JSONL artifact does not exist: {path}")
    rows: list[ModelT] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(model_type.model_validate(json.loads(line)))
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            raise P0BValidationError(
                f"invalid {model_type.__name__} at {path}:{line_number}"
            ) from exc
    if not rows:
        raise P0BValidationError(f"JSONL artifact is empty: {path}")
    return rows


def write_jsonl(path: Path, rows: Iterable[BaseModel]) -> None:
    """Atomically write versioned JSONL without changing the input objects."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(f"{path.name}.partial")
    with temporary_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row.model_dump(mode="json"), ensure_ascii=False))
            handle.write("\n")
    temporary_path.replace(path)


def validate_p0b_dataset(
    corpus: list[CorpusRecord],
    questions: list[P0BQuestion],
    gold: list[P0BGoldRecord] | None = None,
    *,
    eval_revision: str | None = None,
) -> None:
    """Enforce the locked 3-video/12-question population and optional Gold match."""

    if len(corpus) != 3:
        raise P0BValidationError(f"P0-B requires exactly 3 corpus videos, got {len(corpus)}")
    corpus_ids = [record.video_id for record in corpus]
    if len(set(corpus_ids)) != len(corpus_ids):
        raise P0BValidationError("corpus video_id values must be unique")
    if len(questions) != 12:
        raise P0BValidationError(f"P0-B requires exactly 12 questions, got {len(questions)}")
    question_ids = [question.question_id for question in questions]
    if len(set(question_ids)) != len(question_ids):
        raise P0BValidationError("question_id values must be unique")
    counts = {question_type: 0 for question_type in QuestionType}
    per_video: dict[str, list[P0BQuestion]] = {video_id: [] for video_id in corpus_ids}
    for question in questions:
        if question.video_id not in per_video:
            raise P0BValidationError(f"question references unknown video: {question.video_id}")
        counts[question.question_type] += 1
        per_video[question.video_id].append(question)
    expected_counts = {
        QuestionType.SINGLE_LEXICAL: 3,
        QuestionType.SINGLE_PARAPHRASE: 3,
        QuestionType.MULTI_EVIDENCE: 3,
        QuestionType.UNANSWERABLE: 3,
    }
    if counts != expected_counts:
        raise P0BValidationError(
            f"question type distribution is {counts}, expected {expected_counts}"
        )
    if any(len(video_questions) != 4 for video_questions in per_video.values()):
        raise P0BValidationError("each P0-B video must have exactly four questions")

    if gold is None:
        return
    if len(gold) != len(questions):
        raise P0BValidationError("Gold must contain exactly one row per P0-B question")
    questions_by_id = {question.question_id: question for question in questions}
    gold_ids: set[str] = set()
    for answer_key in gold:
        if answer_key.question_id in gold_ids:
            raise P0BValidationError(f"duplicate Gold question_id: {answer_key.question_id}")
        gold_ids.add(answer_key.question_id)
        question = questions_by_id.get(answer_key.question_id)
        if question is None:
            raise P0BValidationError(f"Gold references unknown question: {answer_key.question_id}")
        if answer_key.video_id != question.video_id or answer_key.question != question.question:
            raise P0BValidationError(f"Gold does not match frozen question: {question.question_id}")
        if answer_key.question_type is not question.question_type:
            raise P0BValidationError(f"Gold type does not match question: {question.question_id}")
        if answer_key.should_answer != question.should_answer:
            raise P0BValidationError(
                f"Gold answerability does not match question: {question.question_id}"
            )
        if eval_revision is not None and answer_key.eval_revision != eval_revision:
            raise P0BValidationError(f"Gold revision mismatch: {question.question_id}")
    if gold_ids != set(questions_by_id):
        raise P0BValidationError("Gold question IDs do not exactly match frozen questions")


def validate_gold_segments(
    gold: Iterable[P0BGoldRecord],
    segments_by_video: dict[str, list[VideoSegment]],
    corpus_by_video: dict[str, CorpusRecord],
) -> None:
    """Check Gold segment IDs and intervals against the frozen ingest artifacts."""

    for answer_key in gold:
        if answer_key.video_id not in segments_by_video:
            raise P0BValidationError(f"missing ingest artifacts for {answer_key.video_id}")
        segments = segments_by_video[answer_key.video_id]
        segment_by_id = {segment.segment_id: segment for segment in segments}
        duration_ms = corpus_by_video[answer_key.video_id].duration_ms
        for unit in answer_key.gold_evidence_units:
            if unit.end_ms > duration_ms:
                raise P0BValidationError(
                    f"Gold interval exceeds video duration: {answer_key.question_id}"
                )
            for segment_id in unit.gold_segment_ids:
                segment = segment_by_id.get(segment_id)
                if segment is None:
                    raise P0BValidationError(f"Gold references unknown segment: {segment_id}")
                if segment.video_id != answer_key.video_id:
                    raise P0BValidationError(f"Gold segment crosses videos: {segment_id}")
