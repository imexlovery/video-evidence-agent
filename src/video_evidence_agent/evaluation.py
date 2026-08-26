"""Local ASR evaluation against restricted Chinese-LiPS ground truth."""

from __future__ import annotations

import json
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from opencc import OpenCC

from video_evidence_agent.schemas import AsrSegment


class EvaluationError(RuntimeError):
    """Raised when evaluation inputs violate the frozen P0-A contract."""


SIMPLIFIER = OpenCC("t2s")


@dataclass(frozen=True)
class GroundTruthClip:
    clip_id: str
    ordinal: int
    start_ms: int
    end_ms: int
    text: str


def normalize_cer_text(text: str, *, simplify: bool = True) -> str:
    """Apply the frozen Chinese CER normalization."""

    normalized = unicodedata.normalize("NFKC", text).casefold()
    if simplify:
        normalized = SIMPLIFIER.convert(normalized)
    return "".join(
        character
        for character in normalized
        if unicodedata.category(character)[0] in {"L", "N"}
    )


def levenshtein_distance(reference: str, hypothesis: str) -> int:
    """Return character edit distance with memory linear in the shorter input."""

    if len(reference) < len(hypothesis):
        reference, hypothesis = hypothesis, reference
    previous = list(range(len(hypothesis) + 1))
    for reference_index, reference_character in enumerate(reference, start=1):
        current = [reference_index]
        for hypothesis_index, hypothesis_character in enumerate(hypothesis, start=1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[hypothesis_index] + 1,
                    previous[hypothesis_index - 1]
                    + (reference_character != hypothesis_character),
                )
            )
        previous = current
    return previous[-1]


def _metric(
    reference_text: str,
    hypothesis_text: str,
    *,
    simplify: bool = True,
) -> dict[str, int | float]:
    reference = normalize_cer_text(reference_text, simplify=simplify)
    hypothesis = normalize_cer_text(hypothesis_text, simplify=simplify)
    if not reference:
        raise EvaluationError("normalized CER reference must not be empty")
    distance = levenshtein_distance(reference, hypothesis)
    return {
        "edit_distance": distance,
        "reference_characters": len(reference),
        "hypothesis_characters": len(hypothesis),
        "cer": distance / len(reference),
    }


def load_ground_truth(path: Path) -> list[GroundTruthClip]:
    if not path.is_file():
        raise EvaluationError(f"ground-truth artifact does not exist: {path}")
    clips: list[GroundTruthClip] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
            clip = GroundTruthClip(
                clip_id=str(row["clip_id"]),
                ordinal=int(row["ordinal"]),
                start_ms=int(row["start_ms"]),
                end_ms=int(row["end_ms"]),
                text=str(row["gt_text"]),
            )
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise EvaluationError(f"invalid ground truth at {path}:{line_number}") from exc
        if clip.ordinal != len(clips):
            raise EvaluationError("ground-truth ordinals must be contiguous from zero")
        if clip.end_ms <= clip.start_ms or (clips and clip.start_ms != clips[-1].end_ms):
            raise EvaluationError("ground-truth intervals must be positive and contiguous")
        if not clip.clip_id or not clip.text.strip():
            raise EvaluationError("ground-truth clip ID and text must not be blank")
        clips.append(clip)
    if not clips:
        raise EvaluationError("ground-truth artifact is empty")
    return clips


def load_asr_segments(path: Path) -> list[AsrSegment]:
    if not path.is_file():
        raise EvaluationError(f"ASR artifact does not exist: {path}")
    try:
        payload: Any = json.loads(path.read_text(encoding="utf-8"))
        raw_segments = payload["segments"]
        segments = [AsrSegment.model_validate(row) for row in raw_segments]
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise EvaluationError(f"ASR artifact is invalid: {path}") from exc
    if not segments:
        raise EvaluationError("ASR artifact has no normalized segments")
    if [segment.ordinal for segment in segments] != sorted(
        segment.ordinal for segment in segments
    ):
        raise EvaluationError("ASR segments must be ordered by ordinal")
    return segments


def _assign_segments(
    clips: list[GroundTruthClip],
    segments: list[AsrSegment],
) -> tuple[dict[int, list[AsrSegment]], list[int]]:
    assigned = {clip.ordinal: [] for clip in clips}
    unassigned: list[int] = []
    for segment in segments:
        overlaps = [
            (
                max(
                    0,
                    min(segment.end_ms, clip.end_ms)
                    - max(segment.start_ms, clip.start_ms),
                ),
                clip.ordinal,
            )
            for clip in clips
        ]
        overlap_ms, clip_ordinal = max(overlaps, key=lambda item: (item[0], -item[1]))
        if overlap_ms == 0:
            unassigned.append(segment.ordinal)
            continue
        assigned[clip_ordinal].append(segment)
    return assigned, unassigned


def evaluate_asr(
    clips: list[GroundTruthClip],
    segments: list[AsrSegment],
) -> dict[str, object]:
    """Calculate aggregate and per-clip CER without copying restricted text to output."""

    assigned, unassigned = _assign_segments(clips, segments)
    per_clip: list[dict[str, object]] = []
    for clip in clips:
        clip_segments = assigned[clip.ordinal]
        hypothesis = "".join(segment.text for segment in clip_segments)
        metric = _metric(clip.text, hypothesis)
        script_sensitive_metric = _metric(clip.text, hypothesis, simplify=False)
        per_clip.append(
            {
                "clip_id": clip.clip_id,
                "ordinal": clip.ordinal,
                "start_ms": clip.start_ms,
                "end_ms": clip.end_ms,
                "assigned_asr_ordinals": [segment.ordinal for segment in clip_segments],
                **metric,
                "script_sensitive_cer": script_sensitive_metric["cer"],
            }
        )

    reference_text = "".join(clip.text for clip in clips)
    hypothesis_text = "".join(segment.text for segment in segments)
    return {
        "schema_version": 1,
        "metric": "character_error_rate",
        "normalization": (
            "Unicode NFKC; casefold; OpenCC t2s; retain Unicode letters and numbers only"
        ),
        "assignment": "each ASR segment assigned once to the clip with greatest time overlap",
        "overall": _metric(reference_text, hypothesis_text),
        "script_sensitive_overall": _metric(
            reference_text,
            hypothesis_text,
            simplify=False,
        ),
        "clip_count": len(clips),
        "asr_segment_count": len(segments),
        "unassigned_asr_ordinals": unassigned,
        "clips": per_clip,
    }
