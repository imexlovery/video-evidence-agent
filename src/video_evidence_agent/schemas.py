"""Stable P0-A data contracts."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class AnswerStatus(StrEnum):
    ANSWERED = "ANSWERED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class AsrSegment(BaseModel):
    """An untouched ASR segment normalized only into millisecond boundaries."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    ordinal: int = Field(ge=0)
    start_ms: int = Field(ge=0)
    end_ms: int = Field(ge=1)
    text: str

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("ASR segment text must not be blank")
        return value

    @model_validator(mode="after")
    def end_must_follow_start(self) -> "AsrSegment":
        if self.end_ms <= self.start_ms:
            raise ValueError("ASR segment end_ms must be greater than start_ms")
        return self


class VideoSegment(BaseModel):
    """The P0-A retrieval unit. Time boundaries always remain attached."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    video_id: str = Field(min_length=1)
    segment_id: str = Field(min_length=1)
    ordinal: int = Field(ge=0)
    start_ms: int = Field(ge=0)
    end_ms: int = Field(ge=1)
    transcript_text: str
    source_asr_ordinals: tuple[int, ...] = ()
    source_transcript_unit_ids: tuple[str, ...] = ()

    @field_validator("transcript_text")
    @classmethod
    def transcript_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("VideoSegment transcript_text must not be blank")
        return value

    @model_validator(mode="after")
    def validate_boundaries(self) -> "VideoSegment":
        if self.end_ms <= self.start_ms:
            raise ValueError("VideoSegment end_ms must be greater than start_ms")
        if not self.source_asr_ordinals and not self.source_transcript_unit_ids:
            raise ValueError(
                "VideoSegment must retain source ASR or transcript-unit provenance"
            )
        return self


class RetrievalHit(BaseModel):
    """One raw, ranked TF-IDF retrieval result."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    rank: int = Field(ge=1)
    score: float
    segment: VideoSegment


class Citation(BaseModel):
    """A programmatic copy of an allowed source segment."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    segment_id: str
    start_ms: int = Field(ge=0)
    end_ms: int = Field(ge=1)
    quote: str

    @model_validator(mode="after")
    def validate_boundaries(self) -> "Citation":
        if self.end_ms <= self.start_ms:
            raise ValueError("Citation end_ms must be greater than start_ms")
        return self


class AnswerProposal(BaseModel):
    """The only shape accepted from a real answer model."""

    model_config = ConfigDict(extra="forbid")

    status: AnswerStatus
    answer: str | None = None
    citation_segment_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_status_shape(self) -> "AnswerProposal":
        if self.status is AnswerStatus.ANSWERED:
            if not self.answer or not self.answer.strip():
                raise ValueError("ANSWERED proposals need a non-empty answer")
            if not self.citation_segment_ids:
                raise ValueError("ANSWERED proposals need at least one citation")
        return self


class AnswerResult(BaseModel):
    """The externally visible P0-A answer/refusal contract."""

    model_config = ConfigDict(extra="forbid")

    status: AnswerStatus
    answer: str | None
    evidence: list[Citation]

    @model_validator(mode="after")
    def validate_status_shape(self) -> "AnswerResult":
        if self.status is AnswerStatus.ANSWERED:
            if not self.answer or not self.answer.strip() or not self.evidence:
                raise ValueError("ANSWERED results need an answer and evidence")
        elif self.answer is not None or self.evidence:
            raise ValueError("INSUFFICIENT_EVIDENCE results must be empty")
        return self


class QuestionSpec(BaseModel):
    """A frozen human-authored P0-A smoke question."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    question_id: str = Field(min_length=1)
    question: str = Field(min_length=1)
    should_answer: bool
    expected_interval: tuple[int, int] | None = None

    @model_validator(mode="after")
    def validate_interval(self) -> "QuestionSpec":
        if self.expected_interval is not None:
            start_ms, end_ms = self.expected_interval
            if start_ms < 0 or end_ms <= start_ms:
                raise ValueError("expected_interval must be a non-empty non-negative range")
        return self
