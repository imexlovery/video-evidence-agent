"""Build stable, timestamp-faithful VideoSegments from ASR segments."""

from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any

from video_evidence_agent.schemas import AsrSegment, VideoSegment


class SegmentBuildError(RuntimeError):
    """Raised when ASR boundaries cannot form valid P0-A retrieval units."""


FINAL_SEGMENT_END_TOLERANCE_MS = 1_000


def _validate_asr_order(segments: list[AsrSegment]) -> None:
    previous_end_ms: int | None = None
    for segment in segments:
        if previous_end_ms is not None and segment.start_ms < previous_end_ms:
            raise SegmentBuildError("ASR segments overlap and cannot be merged safely")
        previous_end_ms = segment.end_ms


def _normalise_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def validate_video_segments(segments: Iterable[VideoSegment]) -> None:
    """Enforce P0-A temporal, ordinal, and provenance invariants."""

    materialized = list(segments)
    if not materialized:
        raise SegmentBuildError("at least one VideoSegment is required")

    video_id = materialized[0].video_id
    previous_end_ms: int | None = None
    seen_ids: set[str] = set()
    for expected_ordinal, segment in enumerate(materialized):
        if segment.video_id != video_id:
            raise SegmentBuildError("all VideoSegments must belong to one video")
        if segment.ordinal != expected_ordinal:
            raise SegmentBuildError("VideoSegment ordinals must be consecutive from zero")
        if segment.segment_id in seen_ids:
            raise SegmentBuildError("VideoSegment IDs must be unique")
        if previous_end_ms is not None and segment.start_ms < previous_end_ms:
            raise SegmentBuildError("VideoSegments must not overlap")
        if not segment.transcript_text.strip():
            raise SegmentBuildError("VideoSegments must have transcript text")
        seen_ids.add(segment.segment_id)
        previous_end_ms = segment.end_ms


def build_video_segments(
    video_id: str,
    asr_segments: Iterable[AsrSegment],
    *,
    target_duration_ms: int = 45_000,
    max_duration_ms: int = 60_000,
    duration_ms: int | None = None,
) -> list[VideoSegment]:
    """Merge ASR boundaries, correcting only a bounded final tail overrun."""

    if not video_id.strip():
        raise SegmentBuildError("video_id must not be blank")
    if target_duration_ms <= 0 or max_duration_ms <= 0:
        raise SegmentBuildError("segment durations must be positive")
    if target_duration_ms > max_duration_ms:
        raise SegmentBuildError("target duration cannot exceed maximum duration")
    if duration_ms is not None and duration_ms <= 0:
        raise SegmentBuildError("source duration must be positive")

    ordered = sorted(asr_segments, key=lambda item: (item.start_ms, item.end_ms, item.ordinal))
    if not ordered:
        raise SegmentBuildError("ASR returned no segments to merge")
    _validate_asr_order(ordered)

    groups: list[list[AsrSegment]] = []
    current: list[AsrSegment] = []
    for candidate in ordered:
        if current:
            current_duration_ms = current[-1].end_ms - current[0].start_ms
            candidate_duration_ms = candidate.end_ms - current[0].start_ms
            should_split = (
                current_duration_ms >= target_duration_ms
                or candidate_duration_ms > max_duration_ms
            )
            if should_split:
                groups.append(current)
                current = []
        current.append(candidate)
    if current:
        groups.append(current)

    output: list[VideoSegment] = []
    for ordinal, group in enumerate(groups):
        start = group[0]
        end = group[-1]
        end_ms = end.end_ms
        if (
            ordinal == len(groups) - 1
            and duration_ms is not None
            and end_ms > duration_ms
            and end_ms - duration_ms <= FINAL_SEGMENT_END_TOLERANCE_MS
            and start.start_ms < duration_ms
        ):
            end_ms = duration_ms
        transcript_text = _normalise_whitespace(" ".join(item.text for item in group))
        output.append(
            VideoSegment(
                video_id=video_id,
                segment_id=f"{video_id}-seg-{ordinal:03d}",
                ordinal=ordinal,
                start_ms=start.start_ms,
                end_ms=end_ms,
                transcript_text=transcript_text,
                source_asr_ordinals=tuple(item.ordinal for item in group),
            )
        )

    validate_video_segments(output)
    return output


def build_video_segments_from_transcript(
    video_id: str,
    transcript_units: Iterable[Any],
    *,
    target_duration_ms: int = 45_000,
    max_duration_ms: int = 60_000,
    duration_ms: int | None = None,
) -> list[VideoSegment]:
    """Batch canonical units while retaining both unit and ASR provenance."""

    if not video_id.strip():
        raise SegmentBuildError("video_id must not be blank")
    if target_duration_ms <= 0 or max_duration_ms <= 0:
        raise SegmentBuildError("segment durations must be positive")
    if target_duration_ms > max_duration_ms:
        raise SegmentBuildError("target duration cannot exceed maximum duration")
    if duration_ms is not None and duration_ms <= 0:
        raise SegmentBuildError("source duration must be positive")

    ordered = sorted(
        transcript_units,
        key=lambda item: (item.start_ms, item.end_ms, item.unit_id),
    )
    if not ordered:
        raise SegmentBuildError("canonical transcript returned no units")
    previous_end_ms: int | None = None
    for unit in ordered:
        if unit.end_ms <= unit.start_ms:
            raise SegmentBuildError("canonical transcript unit has invalid boundaries")
        if previous_end_ms is not None and unit.start_ms < previous_end_ms:
            raise SegmentBuildError("canonical transcript units overlap")
        previous_end_ms = unit.end_ms

    groups: list[list[Any]] = []
    current: list[Any] = []
    for candidate in ordered:
        if current:
            current_duration_ms = current[-1].end_ms - current[0].start_ms
            candidate_duration_ms = candidate.end_ms - current[0].start_ms
            if current_duration_ms >= target_duration_ms or candidate_duration_ms > max_duration_ms:
                groups.append(current)
                current = []
        current.append(candidate)
    if current:
        groups.append(current)

    output: list[VideoSegment] = []
    for ordinal, group in enumerate(groups):
        start_ms = group[0].start_ms
        end_ms = group[-1].end_ms
        if (
            ordinal == len(groups) - 1
            and duration_ms is not None
            and end_ms > duration_ms
            and end_ms - duration_ms <= FINAL_SEGMENT_END_TOLERANCE_MS
            and start_ms < duration_ms
        ):
            end_ms = duration_ms
        asr_ordinals: list[int] = []
        for unit in group:
            provenance = getattr(unit, "provenance", {})
            values = provenance.get("asr_ordinals", []) if isinstance(provenance, dict) else []
            if isinstance(values, int):
                values = [values]
            if isinstance(values, (list, tuple)):
                for value in values:
                    if isinstance(value, int) and value not in asr_ordinals:
                        asr_ordinals.append(value)
        output.append(
            VideoSegment(
                video_id=video_id,
                segment_id=f"{video_id}-seg-{ordinal:03d}",
                ordinal=ordinal,
                start_ms=start_ms,
                end_ms=end_ms,
                transcript_text=_normalise_whitespace(
                    " ".join(str(unit.canonical_text) for unit in group)
                ),
                source_asr_ordinals=tuple(asr_ordinals),
                source_transcript_unit_ids=tuple(unit.unit_id for unit in group),
            )
        )

    validate_video_segments(output)
    return output
