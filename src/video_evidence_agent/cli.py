"""Command-line entry points for the bounded P0-A smoke path."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any

from video_evidence_agent.answering import request_answer
from video_evidence_agent.asr import transcribe_audio
from video_evidence_agent.audio import extract_audio, probe_media_duration_ms
from video_evidence_agent.chinese_lips import prepare_chinese_lips_mini
from video_evidence_agent.evaluation import evaluate_asr, load_asr_segments, load_ground_truth
from video_evidence_agent.evidence import GateDecision, gate_answer
from video_evidence_agent.p0b_eval import (
    _resolve_media,
    freeze_p0b,
    grade_p0b,
    render_p0b_report,
    run_p0b_transcript_retrieval,
)
from video_evidence_agent.p0b_schemas import (
    CorpusRecord,
    P0BQuestion,
    load_jsonl,
    validate_p0b_dataset,
)
from video_evidence_agent.retrieval import retrieve
from video_evidence_agent.schemas import QuestionSpec, RetrievalHit, VideoSegment
from video_evidence_agent.segments import validate_video_segments
from video_evidence_agent.transcript_foundation import (
    OcrError,
    TranscriptFoundationError,
    asr_events_from_payload,
    build_canonical_transcript,
    detect_auto_roi,
    discover_subtitle_source,
    extract_subtitle_ocr_events,
    frame_candidate_rows,
    load_event_jsonl,
    parse_roi,
    parse_subtitle_file,
    parse_subtitle_or_event_file,
    write_transcript_artifacts,
)


class CliError(RuntimeError):
    """Raised for invalid P0-A command-line inputs and artifact state."""


IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _elapsed_ms(started_at: float) -> int:
    return round((perf_counter() - started_at) * 1000)


def _validate_identifier(value: str, label: str) -> str:
    if not IDENTIFIER_PATTERN.fullmatch(value):
        raise CliError(f"{label} must use only letters, digits, dots, underscores, and hyphens")
    return value


def _artifact_root(artifacts_dir: Path, video_id: str) -> Path:
    return artifacts_dir / _validate_identifier(video_id, "video_id")


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(f"{path.name}.partial")
    temporary_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(path)


def _write_text(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(f"{path.name}.partial")
    temporary_path.write_text(contents, encoding="utf-8")
    temporary_path.replace(path)


def _write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(f"{path.name}.partial")
    with temporary_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, default=str))
            handle.write("\n")
    temporary_path.replace(path)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise CliError(f"required artifact does not exist: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CliError(f"artifact contains invalid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise CliError(f"artifact must contain a JSON object: {path}")
    return payload


def _read_segments(path: Path, video_id: str) -> list[VideoSegment]:
    if not path.is_file():
        raise CliError(f"segment artifact does not exist: {path}")
    segments: list[VideoSegment] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            segment = VideoSegment.model_validate_json(line)
        except ValueError as exc:
            raise CliError(f"invalid VideoSegment at {path}:{line_number}") from exc
        if segment.video_id != video_id:
            raise CliError("segment artifact video_id does not match requested video")
        segments.append(segment)
    try:
        validate_video_segments(segments)
    except RuntimeError as exc:
        raise CliError(f"segment artifact violates P0-A invariants: {exc}") from exc
    return segments


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _question_id(question: str, requested_id: str | None) -> str:
    if requested_id:
        return _validate_identifier(requested_id, "question_id")
    digest = hashlib.sha256(question.encode("utf-8")).hexdigest()[:12]
    return f"ad-hoc-{digest}"


def _optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    return value.strip() or None


def _source_provenance(args: argparse.Namespace) -> dict[str, str | None]:
    return {
        "origin_url": _optional_text(getattr(args, "source_url", None)),
        "license": _optional_text(getattr(args, "source_license", None)),
        "attribution": _optional_text(getattr(args, "source_attribution", None)),
        "use_note": _optional_text(getattr(args, "source_use_note", None))
        or "local P0-A smoke only; raw media is not committed",
    }


def _render_timestamp(milliseconds: int) -> str:
    total_seconds = milliseconds // 1000
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"


def _print_answer(result: GateDecision) -> None:
    payload = result.result
    print(f"status: {payload.status.value}")
    if payload.answer:
        print(f"answer: {payload.answer}")
    for citation in payload.evidence:
        print(
            "evidence: "
            f"{citation.segment_id} "
            f"{_render_timestamp(citation.start_ms)}–{_render_timestamp(citation.end_ms)}"
        )


def _prepare_chinese_lips(args: argparse.Namespace) -> int:
    video_id = _validate_identifier(args.video_id, "video_id")
    artifact_root = _artifact_root(args.artifacts_dir, video_id)
    manifest = prepare_chinese_lips_mini(
        metadata_path=args.metadata,
        artifact_root=artifact_root,
        repo_id=args.repo_id,
        revision=args.revision,
        archive_filename=args.archive,
        topic=args.topic,
        clip_count=args.clip_count,
        speaker=args.speaker,
        max_compressed_bytes=args.max_compressed_mib * 1024 * 1024,
        reuse_extracted=args.reuse_extracted,
    )
    dataset = manifest["dataset"]
    composite = manifest["composite"]
    if not isinstance(dataset, dict) or not isinstance(composite, dict):
        raise CliError("Chinese-LiPS preparation returned an invalid manifest")
    print(
        f"prepared {video_id}: {dataset['clip_count']} clips, "
        f"{composite['duration_ms']} ms composite, "
        f"{dataset['selected_compressed_bytes']} compressed source bytes"
    )
    return 0


def _evaluate_asr(args: argparse.Namespace) -> int:
    video_id = _validate_identifier(args.video_id, "video_id")
    artifact_root = _artifact_root(args.artifacts_dir, video_id)
    asr_path = artifact_root / "asr.json"
    ground_truth_path = artifact_root / "ground-truth.jsonl"
    result = evaluate_asr(
        load_ground_truth(ground_truth_path),
        load_asr_segments(asr_path),
    )
    result["video_id"] = video_id
    result["inputs"] = {
        "asr_path": asr_path.name,
        "asr_sha256": _sha256(asr_path),
        "ground_truth_path": ground_truth_path.name,
        "ground_truth_sha256": _sha256(ground_truth_path),
    }
    _write_json(artifact_root / "cer.json", result)
    overall = result["overall"]
    if not isinstance(overall, dict):
        raise CliError("ASR evaluation returned an invalid overall result")
    print(
        f"evaluated {video_id}: CER={float(overall['cer']):.4f}, "
        f"{overall['edit_distance']}/{overall['reference_characters']} edits"
    )
    return 0


def _transcript_ocr(args: argparse.Namespace) -> int:
    video_id = _validate_identifier(args.video_id, "video_id")
    video_path = Path(args.video_path).expanduser()
    if not video_path.is_file():
        raise CliError(f"video input does not exist: {video_path}")
    try:
        roi = parse_roi(args.roi)
        events = extract_subtitle_ocr_events(
            video_path,
            roi,
            sample_fps=args.sample_fps,
            start_ms=args.start_ms,
            end_ms=args.end_ms,
        )
    except OcrError as exc:
        raise CliError(str(exc)) from exc
    _write_jsonl(args.output, [event.model_dump(mode="json") for event in events])
    candidates_path = args.output.parent / "subtitle-ocr-frame-candidates.jsonl"
    _write_jsonl(candidates_path, frame_candidate_rows(events))
    print(
        f"OCR {video_id}: {len(events)} deduplicated subtitle events -> {args.output}; "
        f"{len(frame_candidate_rows(events))} frame candidates -> {candidates_path}"
    )
    return 0


def _manifest_video_details(manifest: dict[str, Any]) -> tuple[str, int]:
    video_id = manifest.get("video_id")
    source = manifest.get("source")
    duration_ms = source.get("duration_ms") if isinstance(source, dict) else None
    if not isinstance(video_id, str) or not video_id.strip():
        raise CliError("manifest video_id is missing")
    if not isinstance(duration_ms, int) or duration_ms <= 0:
        raise CliError("manifest source.duration_ms is invalid")
    return video_id, duration_ms


def _ocr_coverage_from_events(
    events: list[Any], *, video_duration_ms: int
) -> dict[str, Any]:
    """Project OCR run coverage into the manifest without inferring it from event times."""

    if not events:
        return {
            "coverage_status": "UNKNOWN",
            "processed_start_ms": None,
            "processed_end_ms": None,
            "video_duration_ms": video_duration_ms,
            "coverage_ratio": None,
        }
    provenance = events[0].provenance
    required = (
        "processed_start_ms",
        "processed_end_ms",
        "video_duration_ms",
        "coverage_ratio",
        "coverage_status",
    )
    if not all(key in provenance for key in required):
        return {
            "coverage_status": "UNKNOWN",
            "processed_start_ms": None,
            "processed_end_ms": None,
            "video_duration_ms": video_duration_ms,
            "coverage_ratio": None,
        }
    return {key: provenance[key] for key in required}


def _fuse_transcript(args: argparse.Namespace) -> int:
    input_manifest = _read_json(args.manifest)
    video_id, duration_ms = _manifest_video_details(input_manifest)
    asr_payload = _read_json(args.asr)
    try:
        asr_events = asr_events_from_payload(asr_payload, payload_path=args.asr)
        ocr_events = load_event_jsonl(args.ocr, expected_source="ocr") if args.ocr else []
        subtitle_events = (
            parse_subtitle_or_event_file(args.subtitle) if args.subtitle else []
        )
        ocr_coverage = (
            _ocr_coverage_from_events(ocr_events, video_duration_ms=duration_ms)
            if args.ocr
            else {}
        )
        source_status: dict[str, dict[str, Any]] = {
            "asr": {"status": "READY", "count": len(asr_events), "path": args.asr.name},
            "subtitle_track": {
                "status": "READY" if subtitle_events else "ABSENT",
                "count": len(subtitle_events),
                "path": args.subtitle.name if args.subtitle else None,
            },
            "ocr": {
                "status": "READY" if ocr_events else "OFF",
                "count": len(ocr_events),
                "path": args.ocr.name if args.ocr else None,
                **ocr_coverage,
            },
        }
        coverage_status = ocr_coverage.get("coverage_status")
        coverage_warnings = (
            [f"OCR_{coverage_status}_COVERAGE"]
            if coverage_status in {"PARTIAL", "UNKNOWN"}
            else []
        )
        build = build_canonical_transcript(
            video_id=video_id,
            duration_ms=duration_ms,
            asr_events=asr_events,
            subtitle_events=subtitle_events,
            ocr_events=ocr_events,
            transcript_mode=args.transcript_mode,
            source_status=source_status,
            warnings=coverage_warnings,
        )
    except TranscriptFoundationError as exc:
        raise CliError(str(exc)) from exc
    paths = write_transcript_artifacts(
        build,
        args.output_root,
        base_manifest=input_manifest,
        write_ocr_events=bool(args.ocr),
    )
    print(
        f"fused {video_id}: {len(build.canonical_units)} units, "
        f"{len(build.segments)} segments, status={build.manifest.status} -> "
        f"{paths['transcript_manifest']}"
    )
    return 0


def _ingest_transcript(
    args: argparse.Namespace,
    *,
    source_path: Path,
    artifact_root: Path,
    asr_path: Path,
    source_duration_ms: int,
    manifest: dict[str, Any],
) -> tuple[Any, dict[str, Path], dict[str, dict[str, Any]]]:
    transcript_mode = getattr(args, "transcript_mode", "asr-only")
    ocr_mode = getattr(args, "ocr_mode", "off")
    if transcript_mode not in {"asr-only", "fused"}:
        raise CliError("transcript_mode must be asr-only or fused")
    if ocr_mode not in {"off", "roi", "auto"}:
        raise CliError("ocr_mode must be off, roi, or auto")
    asr_payload = _read_json(asr_path)
    asr_events = asr_events_from_payload(asr_payload, payload_path=asr_path)
    warnings: list[str] = []
    source_status: dict[str, dict[str, Any]] = {
        "asr": {"status": "READY", "count": len(asr_events), "path": asr_path.name},
        "subtitle_track": {"status": "OFF", "count": 0, "path": None},
        "ocr": {"status": "OFF", "count": 0, "path": None},
    }
    subtitle_events: list[Any] = []
    if transcript_mode == "fused":
        explicit_subtitle = getattr(args, "subtitle_file", None)
        explicit_path = Path(explicit_subtitle).expanduser() if explicit_subtitle else None
        try:
            discovery = discover_subtitle_source(
                source_path,
                explicit_path=explicit_path,
                artifact_root=artifact_root,
            )
        except OSError:
            discovery = None
        if discovery is None:
            source_status["subtitle_track"] = {
                "status": "FAILED",
                "count": 0,
                "path": str(explicit_path) if explicit_path else None,
            }
            warnings.append("SUBTITLE_DISCOVERY_FAILED")
        elif discovery.status == "AVAILABLE" and discovery.path is not None:
            source_status["subtitle_track"] = {
                "status": "READY",
                "count": 0,
                "path": str(discovery.path),
                "format": discovery.format,
                "track_index": discovery.track_index,
                "language": discovery.language,
            }
            try:
                subtitle_events = parse_subtitle_file(discovery.path)
                source_status["subtitle_track"]["count"] = len(subtitle_events)
            except Exception:
                source_status["subtitle_track"]["status"] = "FAILED"
                warnings.append("SUBTITLE_PARSE_FAILED")
        else:
            source_status["subtitle_track"] = {
                "status": discovery.status,
                "count": 0,
                "path": None,
            }
            if discovery.warning and discovery.warning != "SUBTITLE_ABSENT":
                warnings.append(discovery.warning)
    if transcript_mode == "fused" and ocr_mode != "off":
        write_ocr_events = True
        if ocr_mode == "roi":
            try:
                requested_roi = parse_roi(getattr(args, "ocr_roi", None))
            except OcrError as exc:
                raise CliError(str(exc)) from exc
        else:
            requested_roi = None
        try:
            if ocr_mode == "roi":
                roi = requested_roi
            else:
                auto = detect_auto_roi(source_path, sample_fps=1.0)
                warnings.extend(auto.warnings)
                if auto.roi is None:
                    source_status["ocr"] = {"status": "UNSTABLE", "count": 0, "path": None}
                    roi = None
                else:
                    roi = auto.roi
            if roi is not None:
                ocr_events = extract_subtitle_ocr_events(
                    source_path,
                    roi,
                    sample_fps=2.0,
                    duration_ms=source_duration_ms,
                    roi_mode="explicit" if ocr_mode == "roi" else "auto",
                )
                source_status["ocr"] = {
                    "status": "READY" if ocr_events else "ABSENT",
                    "count": len(ocr_events),
                    "path": "subtitle-ocr-events.jsonl",
                    "roi": list(roi),
                    "coverage_status": "FULL",
                    "processed_start_ms": 0,
                    "processed_end_ms": source_duration_ms,
                    "video_duration_ms": source_duration_ms,
                    "coverage_ratio": 1.0,
                }
                if not ocr_events:
                    warnings.append("OCR_NO_EVENTS")
        except Exception:
            source_status["ocr"] = {
                "status": "FAILED",
                "count": 0,
                "path": "subtitle-ocr-events.jsonl",
            }
            warnings.append("OCR_FAILED")
            ocr_events = []
    else:
        write_ocr_events = False
        ocr_events = []

    build = build_canonical_transcript(
        video_id=manifest["video_id"],
        duration_ms=source_duration_ms,
        asr_events=asr_events,
        subtitle_events=subtitle_events,
        ocr_events=ocr_events,
        transcript_mode=transcript_mode,
        source_status=source_status,
        warnings=warnings,
        target_segment_ms=args.target_segment_ms,
        max_segment_ms=args.max_segment_ms,
    )
    manifest_for_transcript = dict(manifest)
    manifest_for_transcript["source"] = {
        **dict(manifest.get("source") or {}),
        "duration_ms": source_duration_ms,
    }
    manifest_for_transcript["segmenting"] = {
        "target_duration_ms": args.target_segment_ms,
        "max_duration_ms": args.max_segment_ms,
        "segment_count": len(build.segments),
        "path": "segments.jsonl",
    }
    paths = write_transcript_artifacts(
        build,
        artifact_root,
        base_manifest=manifest_for_transcript,
        write_ocr_events=write_ocr_events,
    )
    return build, paths, source_status


def _ingest(args: argparse.Namespace) -> int:
    video_id = _validate_identifier(args.video_id, "video_id")
    source_path = Path(args.video_path).expanduser()
    if not source_path.is_file():
        raise CliError(f"video input does not exist: {source_path}")
    if args.preview_seconds <= 0:
        raise CliError("preview_seconds must be positive")

    artifact_root = _artifact_root(args.artifacts_dir, video_id)
    audio_path = artifact_root / "audio.wav"
    preview_audio_path = artifact_root / "audio-preview.wav"
    preview_asr_path = artifact_root / "asr-preview.json"
    asr_path = artifact_root / "asr.json"
    segments_path = artifact_root / "segments.jsonl"
    manifest_path = artifact_root / "manifest.json"
    source_path = source_path.resolve()
    source_sha256 = _sha256(source_path)

    timing: dict[str, int] = {}
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "pipeline_status": "IN_PROGRESS",
        "started_at": _utc_now(),
        "video_id": video_id,
        "source": {
            "path": str(source_path),
            "sha256": source_sha256,
            **_source_provenance(args),
        },
    }
    _write_json(manifest_path, manifest)

    stage = "source_probe"
    try:
        phase_started_at = perf_counter()
        source_duration_ms = probe_media_duration_ms(source_path)
        timing["source_probe"] = _elapsed_ms(phase_started_at)

        stage = "audio_extraction"
        phase_started_at = perf_counter()
        audio_result = extract_audio(source_path, audio_path)
        timing["audio_extraction"] = _elapsed_ms(phase_started_at)

        stage = "asr_preview"
        preview_seconds = min(args.preview_seconds, max(1, audio_result.probe.duration_ms // 1000))
        phase_started_at = perf_counter()
        preview_audio_result = extract_audio(
            source_path,
            preview_audio_path,
            limit_seconds=preview_seconds,
        )
        preview_run = transcribe_audio(
            preview_audio_path,
            model=args.asr_model,
            language="zh",
        )
        timing["asr_preview"] = _elapsed_ms(phase_started_at)
        _write_json(
            preview_asr_path,
            {
                "schema_version": 1,
                "preview_seconds_requested": args.preview_seconds,
                "preview_seconds_actual": preview_seconds,
                "audio": {
                    "path": preview_audio_path.name,
                    "duration_ms": preview_audio_result.probe.duration_ms,
                },
                **preview_run.to_dict(),
            },
        )

        stage = "asr_full"
        phase_started_at = perf_counter()
        full_run = transcribe_audio(audio_path, model=args.asr_model, language="zh")
        timing["asr_full"] = _elapsed_ms(phase_started_at)
        _write_json(
            asr_path,
            {
                "schema_version": 1,
                **full_run.to_dict(),
            },
        )

        stage = "transcript_foundation"
        phase_started_at = perf_counter()
        transcript_build, transcript_paths, _ = _ingest_transcript(
            args,
            source_path=source_path,
            artifact_root=artifact_root,
            asr_path=asr_path,
            source_duration_ms=source_duration_ms,
            manifest=manifest,
        )
        segments = list(transcript_build.segments)
        timing["transcript_foundation"] = _elapsed_ms(phase_started_at)
    except (Exception, KeyboardInterrupt) as exc:
        manifest.update(
            {
                "pipeline_status": "FAILED",
                "completed_at": _utc_now(),
                "phase_elapsed_ms": timing,
                "failure": {
                    "stage": stage,
                    "error_type": type(exc).__name__,
                    "message": str(exc),
                },
            }
        )
        _write_json(manifest_path, manifest)
        raise

    manifest.update(
        {
            "pipeline_status": "SUCCEEDED",
            "completed_at": _utc_now(),
            "source": {
                "path": str(source_path),
                "sha256": source_sha256,
                "duration_ms": source_duration_ms,
                **_source_provenance(args),
            },
            "audio": {
                "path": audio_path.name,
                "command": list(audio_result.command),
                "channels": audio_result.probe.channels,
                "sample_rate_hz": audio_result.probe.sample_rate_hz,
                "duration_ms": audio_result.probe.duration_ms,
            },
            "asr": {
                "engine": full_run.engine,
                "model": full_run.model,
                "language": full_run.language,
                "preview_path": preview_asr_path.name,
                "full_path": asr_path.name,
            },
            "segmenting": {
                "target_duration_ms": args.target_segment_ms,
                "max_duration_ms": args.max_segment_ms,
                "segment_count": len(segments),
                "path": segments_path.name,
            },
            "transcript": transcript_build.manifest.model_copy(
                update={
                    "artifacts": {
                        key: path.name for key, path in transcript_paths.items()
                    }
                }
            ).model_dump(mode="json"),
            "phase_elapsed_ms": timing,
        }
    )
    _write_json(manifest_path, manifest)
    print(f"ingested {video_id}: {len(segments)} timestamped VideoSegments")
    return 0


def _persist_retrieval(
    artifact_root: Path,
    *,
    video_id: str,
    question_id: str,
    question: str,
    top_k: int,
    segments: list[VideoSegment],
) -> list[RetrievalHit]:
    hits = retrieve(question, segments, top_k=top_k)
    _write_json(
        artifact_root / "retrieval" / f"{question_id}.json",
        {
            "schema_version": 1,
            "generated_at": _utc_now(),
            "video_id": video_id,
            "question_id": question_id,
            "question": question,
            "top_k_requested": top_k,
            "hits": [hit.model_dump(mode="json") for hit in hits],
        },
    )
    return hits


def _ask_one(
    *,
    artifacts_dir: Path,
    video_id: str,
    question: str,
    question_id: str,
    top_k: int,
) -> GateDecision:
    artifact_root = _artifact_root(artifacts_dir, video_id)
    manifest = _read_json(artifact_root / "manifest.json")
    if manifest.get("pipeline_status") != "SUCCEEDED":
        raise CliError("manifest is not a successful P0-A ingest")
    segments = _read_segments(artifact_root / "segments.jsonl", video_id)
    hits = _persist_retrieval(
        artifact_root,
        video_id=video_id,
        question_id=question_id,
        question=question,
        top_k=top_k,
        segments=segments,
    )
    proposal = request_answer(question, hits)
    decision = gate_answer(proposal, hits)
    _write_json(
        artifact_root / "answers" / f"{question_id}.json",
        decision.result.model_dump(mode="json"),
    )
    _write_json(
        artifact_root / "answers" / f"{question_id}.gate.json",
        {
            "schema_version": 1,
            "generated_at": _utc_now(),
            "gate_reason": decision.reason,
            "model_proposal": proposal.model_dump(mode="json"),
        },
    )
    return decision


def _ask(args: argparse.Namespace) -> int:
    video_id = _validate_identifier(args.video_id, "video_id")
    question_id = _question_id(args.question, args.question_id)
    decision = _ask_one(
        artifacts_dir=args.artifacts_dir,
        video_id=video_id,
        question=args.question,
        question_id=question_id,
        top_k=args.top_k,
    )
    _print_answer(decision)
    return 0


def _load_questions(path: Path) -> list[QuestionSpec]:
    if not path.is_file():
        raise CliError(f"question set does not exist: {path}")
    questions: list[QuestionSpec] = []
    seen_ids: set[str] = set()
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            question = QuestionSpec.model_validate_json(line)
        except ValueError as exc:
            raise CliError(f"invalid question at {path}:{line_number}") from exc
        _validate_identifier(question.question_id, "question_id")
        if question.question_id in seen_ids:
            raise CliError(f"duplicate question_id in {path}: {question.question_id}")
        seen_ids.add(question.question_id)
        questions.append(question)
    if not 3 <= len(questions) <= 5:
        raise CliError("P0-A smoke set must contain 3 to 5 questions")
    if sum(question.should_answer for question in questions) < 2:
        raise CliError("P0-A smoke set needs at least two answerable questions")
    if all(question.should_answer for question in questions):
        raise CliError("P0-A smoke set needs at least one unanswerable question")
    return questions


def _smoke(args: argparse.Namespace) -> int:
    video_id = _validate_identifier(args.video_id, "video_id")
    questions = _load_questions(args.questions)
    artifact_root = _artifact_root(args.artifacts_dir, video_id)
    rows: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []

    for question in questions:
        try:
            decision = _ask_one(
                artifacts_dir=args.artifacts_dir,
                video_id=video_id,
                question=question.question,
                question_id=question.question_id,
                top_k=args.top_k,
            )
            _print_answer(decision)
            rows.append(
                {
                    "question_id": question.question_id,
                    "question": question.question,
                    "should_answer": question.should_answer,
                    "expected_interval": question.expected_interval,
                    "final_status": decision.result.status.value,
                    "citation_valid": decision.reason == "citation_provenance_verified",
                    "gate_reason": decision.reason,
                }
            )
        except Exception as exc:
            failures.append(
                {
                    "question_id": question.question_id,
                    "error_type": type(exc).__name__,
                    "message": str(exc),
                }
            )
    _write_json(
        artifact_root / "smoke-run.json",
        {
            "schema_version": 1,
            "generated_at": _utc_now(),
            "video_id": video_id,
            "question_count": len(questions),
            "status": "SUCCEEDED" if not failures else "FAILED",
            "results": rows,
            "failures": failures,
        },
    )
    if failures:
        print(f"smoke failed for {len(failures)} question(s); see smoke-run.json", file=sys.stderr)
        return 1
    return 0


def _markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def _asr_samples(asr_payload: dict[str, Any], duration_ms: int) -> list[dict[str, object]]:
    raw_segments = asr_payload.get("segments")
    if not isinstance(raw_segments, list) or not raw_segments:
        raise CliError("ASR artifact has no normalized segments for human review")

    segments = [item for item in raw_segments if isinstance(item, dict)]
    if not segments:
        raise CliError("ASR artifact has no valid normalized segment objects")

    def nearest(target_ms: int) -> dict[str, object]:
        def distance(segment: dict[str, object]) -> int:
            try:
                start_ms = int(segment["start_ms"])
                end_ms = int(segment["end_ms"])
            except (KeyError, TypeError, ValueError) as exc:
                raise CliError("ASR review segment has invalid boundaries") from exc
            return abs(((start_ms + end_ms) // 2) - target_ms)

        return min(segments, key=distance)

    return [nearest(0), nearest(duration_ms // 2), nearest(max(0, duration_ms - 1))]


def _r1_question_asr_samples(
    artifact_root: Path,
    asr_payload: dict[str, Any],
    questions: list[QuestionSpec],
) -> list[dict[str, object]] | None:
    """Use the three confirmed question clips as R1's short ASR review samples."""

    ground_truth_path = artifact_root / "ground-truth.jsonl"
    if not ground_truth_path.is_file():
        return None
    raw_segments = asr_payload.get("segments")
    if not isinstance(raw_segments, list) or not raw_segments:
        raise CliError("ASR artifact has no normalized segments for human review")
    asr_segments = [item for item in raw_segments if isinstance(item, dict)]
    if not asr_segments:
        raise CliError("ASR artifact has no valid normalized segments")

    ground_truth: list[dict[str, int]] = []
    for line_number, line in enumerate(
        ground_truth_path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
            ground_truth.append(
                {
                    "start_ms": int(row["start_ms"]),
                    "end_ms": int(row["end_ms"]),
                }
            )
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise CliError(f"invalid ground truth at {ground_truth_path}:{line_number}") from exc

    samples: list[dict[str, object]] = []
    for question in questions:
        if not question.should_answer or question.expected_interval is None:
            continue
        interval = question.expected_interval
        matching_clips = [
            clip for clip in ground_truth if (clip["start_ms"], clip["end_ms"]) == interval
        ]
        if len(matching_clips) != 1:
            raise CliError(f"question {question.question_id} does not map to one ground-truth clip")
        clip = matching_clips[0]
        overlapping = []
        for segment in asr_segments:
            try:
                start_ms = int(segment["start_ms"])
                end_ms = int(segment["end_ms"])
                text = str(segment["text"])
            except (KeyError, TypeError, ValueError) as exc:
                raise CliError("ASR review segment has invalid fields") from exc
            overlap_ms = max(0, min(end_ms, clip["end_ms"]) - max(start_ms, clip["start_ms"]))
            if overlap_ms > 0:
                overlapping.append((start_ms, end_ms, text))
        if not overlapping:
            raise CliError(f"question {question.question_id} has no overlapping ASR sample")
        samples.append(
            {
                "question_id": question.question_id,
                "start_ms": min(item[0] for item in overlapping),
                "end_ms": max(item[1] for item in overlapping),
                "text": " ".join(item[2] for item in overlapping),
            }
        )
    return samples if len(samples) >= 3 else None


def _human_review_confirmation(artifact_root: Path) -> tuple[set[str], str]:
    path = artifact_root / "human-review.json"
    if not path.is_file():
        return set(), "PENDING_HUMAN_REVIEW"
    payload = _read_json(path)
    raw_question_ids = payload.get("confirmed_question_ids", [])
    if not isinstance(raw_question_ids, list) or not all(
        isinstance(item, str) for item in raw_question_ids
    ):
        raise CliError("human-review artifact has invalid confirmed question IDs")
    answer_citation_review = payload.get("answer_citation_review", "PENDING_HUMAN_REVIEW")
    if answer_citation_review not in {"PENDING_HUMAN_REVIEW", "CONFIRMED"}:
        raise CliError("human-review artifact has invalid answer citation status")
    return set(raw_question_ids), answer_citation_review


def _retrieval_summary(path: Path) -> tuple[str, str]:
    if not path.is_file():
        return "NOT_RUN", "NOT_RUN"
    payload = _read_json(path)
    raw_hits = payload.get("hits")
    if not isinstance(raw_hits, list) or not raw_hits:
        return "NO_HITS", "NO_HITS"

    summaries: list[str] = []
    for raw_hit in raw_hits:
        if not isinstance(raw_hit, dict) or not isinstance(raw_hit.get("segment"), dict):
            continue
        segment = raw_hit["segment"]
        try:
            summary = (
                f"{segment['segment_id']} "
                f"{_render_timestamp(int(segment['start_ms']))}–"
                f"{_render_timestamp(int(segment['end_ms']))} "
                f"score={float(raw_hit['score']):.4f}"
            )
        except (KeyError, TypeError, ValueError):
            continue
        summaries.append(summary)
    if not summaries:
        return "INVALID_HITS", "INVALID_HITS"
    return summaries[0], "; ".join(summaries)


def _answer_summary(answer_path: Path, gate_path: Path) -> tuple[str, str, str]:
    if not answer_path.is_file():
        return "NOT_RUN", "NOT_RUN", "NOT_RUN"
    answer = _read_json(answer_path)
    status = _markdown_cell(answer.get("status", "INVALID"))
    gate_reason = "GATE_RECORD_MISSING"
    if gate_path.is_file():
        gate_reason = _markdown_cell(_read_json(gate_path).get("gate_reason", "INVALID"))
    citation_valid = "yes" if gate_reason == "citation_provenance_verified" else "no"
    return status, citation_valid, gate_reason


def _first_answered_trace(
    artifact_root: Path,
    questions: list[QuestionSpec],
) -> str:
    for question in questions:
        answer_path = artifact_root / "answers" / f"{question.question_id}.json"
        retrieval_path = artifact_root / "retrieval" / f"{question.question_id}.json"
        if not answer_path.is_file() or not retrieval_path.is_file():
            continue
        answer = _read_json(answer_path)
        if answer.get("status") != "ANSWERED":
            continue
        top_1, top_5 = _retrieval_summary(retrieval_path)
        evidence = answer.get("evidence")
        if not isinstance(evidence, list):
            evidence = []
        evidence_lines = [
            (
                f"- {item.get('segment_id')} "
                f"{_render_timestamp(int(item.get('start_ms', 0)))}–"
                f"{_render_timestamp(int(item.get('end_ms', 0)))}: "
                f"{_markdown_cell(item.get('quote', ''))}"
            )
            for item in evidence
            if isinstance(item, dict)
        ]
        return "\n".join(
            [
                f"问题：{question.question}",
                f"Top-1：{top_1}",
                f"Top-K：{top_5}",
                f"答案：{answer.get('answer')}",
                "程序回填的 evidence：",
                *evidence_lines,
            ]
        )
    return "没有可展示的 ANSWERED 真实案例；不得用 Mock 或手写案例替代。"


def _render_review_report(
    *,
    manifest: dict[str, Any],
    asr_payload: dict[str, Any],
    artifact_root: Path,
    questions: list[QuestionSpec],
) -> str:
    source = manifest.get("source")
    audio = manifest.get("audio")
    asr = manifest.get("asr")
    segmenting = manifest.get("segmenting")
    if not all(isinstance(item, dict) for item in [source, audio, asr, segmenting]):
        raise CliError("successful manifest lacks P0-A provenance fields")

    source_duration_ms = source.get("duration_ms")
    if not isinstance(source_duration_ms, int) or source_duration_ms <= 0:
        raise CliError("successful manifest has no valid source duration")
    r1_samples = _r1_question_asr_samples(artifact_root, asr_payload, questions)
    if r1_samples is None:
        samples = _asr_samples(asr_payload, source_duration_ms)
        sample_labels = ["开始", "中段", "结尾"]
    else:
        samples = r1_samples
        sample_labels = [f"问题 {sample['question_id']}" for sample in samples]
    confirmed_question_ids, answer_citation_review = _human_review_confirmation(artifact_root)
    finalized = answer_citation_review == "CONFIRMED" and all(
        question.question_id in confirmed_question_ids for question in questions
    )
    phase_elapsed = json.dumps(manifest.get("phase_elapsed_ms", {}), ensure_ascii=False)
    dropped_empty_raw_segments = asr_payload.get("dropped_empty_raw_segment_ordinals", [])
    if not isinstance(dropped_empty_raw_segments, list):
        raise CliError("ASR artifact has invalid empty-segment provenance")
    dropped_non_positive_raw_segments = asr_payload.get(
        "dropped_non_positive_raw_segment_ordinals",
        [],
    )
    if not isinstance(dropped_non_positive_raw_segments, list):
        raise CliError("ASR artifact has invalid non-positive-segment provenance")
    dropped_unrepresentable_raw_segments = asr_payload.get(
        "dropped_unrepresentable_raw_segment_ordinals",
        [],
    )
    if not isinstance(dropped_unrepresentable_raw_segments, list):
        raise CliError("ASR artifact has invalid unrepresentable-segment provenance")

    rows: list[str] = []
    for question in questions:
        top_1, top_5 = _retrieval_summary(
            artifact_root / "retrieval" / f"{question.question_id}.json"
        )
        final_status, citation_valid, gate_reason = _answer_summary(
            artifact_root / "answers" / f"{question.question_id}.json",
            artifact_root / "answers" / f"{question.question_id}.gate.json",
        )
        expected_interval = (
            "N/A"
            if question.expected_interval is None
            else f"{_render_timestamp(question.expected_interval[0])}–"
            f"{_render_timestamp(question.expected_interval[1])}"
        )
        rows.append(
            "| "
            + " | ".join(
                [
                    _markdown_cell(question.question_id),
                    _markdown_cell(question.question),
                    str(question.should_answer).lower(),
                    expected_interval,
                    _markdown_cell(top_1),
                    _markdown_cell(top_5),
                    _markdown_cell(final_status),
                    citation_valid,
                    (
                        "CONFIRMED"
                        if answer_citation_review == "CONFIRMED"
                        and question.question_id in confirmed_question_ids
                        else "PENDING_HUMAN_REVIEW"
                    ),
                    _markdown_cell(gate_reason),
                ]
            )
            + " |"
        )

    sample_rows: list[str] = []
    for label, segment in zip(sample_labels, samples, strict=True):
        try:
            range_text = (
                f"{_render_timestamp(int(segment['start_ms']))}–"
                f"{_render_timestamp(int(segment['end_ms']))}"
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise CliError("ASR review segment has invalid boundaries") from exc
        sample_review = (
            "USER_CONFIRMED" if segment.get("question_id") in confirmed_question_ids else "PENDING"
        )
        sample_rows.append(
            f"| {label} | {range_text} | {_markdown_cell(segment.get('text', ''))} | "
            f"{sample_review} |"
        )

    trace = _first_answered_trace(artifact_root, questions)
    document_status = (
        "- 文档状态：FINAL — 用户已确认 ASR 短片、问题、答案与 citation 语义支持。"
        if finalized
        else "- 文档状态：DRAFT — 需要人工复核后才能作为验收证据。"
    )
    conclusion = (
        [
            "- P0-A 验收决定：PASSED — Gate A-G 已完成，按范围停止。",
            "- 已知失败与 transcript-only 边界：已记录；原始 ASR 保留繁体，"
            "CER 同时保存繁转简与字形敏感指标；未使用 OCR/VLM。",
            "- P0-B 建议：STOP — 等待用户另行授权，不自动进入下一阶段。",
            "",
            "用户已完成 owner acceptance；本报告是 P0-A 最终证据。",
        ]
        if finalized
        else [
            "- P0-A 验收决定：PENDING_HUMAN_REVIEW",
            "- 已知失败与 transcript-only 边界：PENDING_HUMAN_REVIEW",
            "- P0-B 建议：PENDING_HUMAN_REVIEW",
            "",
            "不得在人工复核未完成、真实模型未调用或问题集不是人类基于原视频编写时，将本报告标记为通过。",
        ]
    )
    review_note = (
        "human_supported 已由用户核对并确认；citation_valid 记录程序化来源校验。"
        if finalized
        else "human_supported 必须由人工核对 citation 是否真正支持答案；"
        "citation_valid 只表示程序验证了引用来源。"
    )
    asr_review_note = (
        "R1 的三个问题短片与答案 citation 语义均已由用户确认；不要修改 ASR 原文。"
        if finalized
        else "R1 的三个问题短片已由用户确认；答案 citation 仍需单独核对是否真正支持答案。"
        "不要修改 ASR 原文。"
    )
    return "\n".join(
        [
            "# P0-A Smoke Report",
            "",
            document_status,
            f"- video_id：{manifest.get('video_id')}",
            f"- 生成时间：{_utc_now()}",
            "",
            "## 视频与运行配置",
            "",
            f"- 来源：{source.get('origin_url') or '未记录'}",
            f"- 授权：{source.get('license') or '未记录'}",
            f"- 署名：{source.get('attribution') or '未记录'}",
            f"- 本地使用说明：{source.get('use_note') or '未记录'}",
            f"- 输入 SHA-256：{source.get('sha256')}",
            f"- 视频时长：{_render_timestamp(source_duration_ms)}",
            f"- 音频：{audio.get('channels')} channel, {audio.get('sample_rate_hz')} Hz, "
            f"{_render_timestamp(int(audio.get('duration_ms', 0)))}",
            f"- ASR：{asr.get('engine')} / {asr.get('model')} / {asr.get('language')}",
            f"- 不参与检索的原始空文本 ASR segments：{dropped_empty_raw_segments}",
            f"- 不参与检索的原始零/负时长 ASR segments：{dropped_non_positive_raw_segments}",
            f"- 不参与检索的原始亚毫秒 ASR segments：{dropped_unrepresentable_raw_segments}",
            f"- 切分：目标 {segmenting.get('target_duration_ms')} ms，"
            f"最大 {segmenting.get('max_duration_ms')} ms，"
            f"{segmenting.get('segment_count')} 个 VideoSegments",
            f"- 阶段耗时（ms）：{phase_elapsed}",
            "",
            "## ASR 人工抽查",
            "",
            "| 位置 | 时间段 | ASR 原文 | 人工结论 |",
            "| --- | --- | --- | --- |",
            *sample_rows,
            "",
            asr_review_note,
            "",
            "## 逐题 Smoke 结果",
            "",
            "| question_id | question | should_answer | expected_interval | top_1 | top_5 | "
            "final_status | citation_valid | human_supported | notes |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            *rows,
            "",
            review_note,
            "",
            "## 一个完整真实案例",
            "",
            trace,
            "",
            "## 结论与下一步",
            "",
            *conclusion,
            "",
        ]
    )


def _review(args: argparse.Namespace) -> int:
    video_id = _validate_identifier(args.video_id, "video_id")
    artifact_root = _artifact_root(args.artifacts_dir, video_id)
    manifest = _read_json(artifact_root / "manifest.json")
    if manifest.get("pipeline_status") != "SUCCEEDED":
        raise CliError("cannot build a review report from a non-successful ingest")
    questions = _load_questions(args.questions)
    asr_payload = _read_json(artifact_root / "asr.json")
    report = _render_review_report(
        manifest=manifest,
        asr_payload=asr_payload,
        artifact_root=artifact_root,
        questions=questions,
    )
    _write_text(args.report, report)
    print(f"wrote P0-A review report: {args.report}")
    return 0


def _p0b_project_root(args: argparse.Namespace) -> Path:
    return Path(args.project_root).expanduser().resolve()


def _p0b_freeze(args: argparse.Namespace) -> int:
    project_root = _p0b_project_root(args)
    manifest = freeze_p0b(
        project_root=project_root,
        eval_revision=args.eval_revision,
        corpus_path=(project_root / args.corpus).resolve(),
        questions_path=(project_root / args.questions).resolve(),
        gold_path=(project_root / args.gold).resolve(),
        answer_prompt_path=(project_root / args.answer_prompt).resolve(),
        media_root=(project_root / args.media_root).resolve(),
        manifest_path=(project_root / args.manifest_out).resolve()
        if args.manifest_out
        else None,
        gold_revision=args.gold_revision,
    )
    print(
        f"froze {manifest['eval_revision']}: {manifest['corpus']['video_count']} videos, "
        f"{manifest['questions']['count']} questions"
    )
    return 0


def _p0b_ingest(args: argparse.Namespace) -> int:
    project_root = _p0b_project_root(args)
    corpus_path = (project_root / args.corpus).resolve()
    corpus = load_jsonl(corpus_path, CorpusRecord)
    questions_path = (project_root / args.questions).resolve() if args.questions else None
    questions = load_jsonl(questions_path, P0BQuestion) if questions_path else []
    if questions:
        validate_p0b_dataset(corpus, questions)
    for record in corpus:
        video_path = _resolve_media(
            (project_root / args.media_root).resolve(), record.local_path_alias
        )
        artifact_relpath = Path(record.ingest_artifact_relpath)
        ingest_args = argparse.Namespace(
            video_id=record.video_id,
            video_path=str(video_path),
            artifacts_dir=project_root / artifact_relpath.parent,
            preview_seconds=args.preview_seconds,
            asr_model=args.asr_model,
            target_segment_ms=args.target_segment_ms,
            max_segment_ms=args.max_segment_ms,
            source_url=record.source_url,
            source_license=record.license,
            source_attribution=record.attribution,
            source_use_note=record.use_basis,
        )
        _ingest(ingest_args)
    print(f"ingested {len(corpus)} P0-B videos")
    return 0


def _p0b_run(args: argparse.Namespace) -> int:
    project_root = _p0b_project_root(args)
    manifest = _read_json((project_root / args.manifest).resolve())
    result = run_p0b_transcript_retrieval(
        project_root=project_root,
        manifest=manifest,
        media_root=(project_root / args.media_root).resolve(),
    )
    print(
        f"recorded P0-B {result['evaluation_method']}: {result['result_count']} result slots; "
        "inspect artifacts/p0b before grading"
    )
    return 0


def _p0b_grade(args: argparse.Namespace) -> int:
    project_root = _p0b_project_root(args)
    manifest = _read_json((project_root / args.manifest).resolve())
    metrics = grade_p0b(project_root=project_root, manifest=manifest)
    print(
        f"graded {metrics['result_count']} P0-B results: "
        f"status={metrics['evaluation_status']} recommendation={metrics['recommendation']}"
    )
    return 0


def _p0b_report(args: argparse.Namespace) -> int:
    project_root = _p0b_project_root(args)
    manifest = _read_json((project_root / args.manifest).resolve())
    metrics = grade_p0b(project_root=project_root, manifest=manifest)
    report_path = (project_root / args.report).resolve()
    render_p0b_report(metrics=metrics, report_path=report_path)
    print(f"wrote P0-B report: {report_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="video-evidence",
        description="P0-A Chinese video transcript evidence smoke test",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser(
        "prepare-chinese-lips-mini",
        help="range-read and compose the bounded Chinese-LiPS validation slice",
    )
    prepare.add_argument("--metadata", type=Path, required=True)
    prepare.add_argument(
        "--video-id",
        default="chinese-lips-mini-val-kj-001",
    )
    prepare.add_argument("--artifacts-dir", type=Path, default=Path("artifacts"))
    prepare.add_argument("--repo-id", default="BAAI/Chinese-LiPS")
    prepare.add_argument("--revision", required=True)
    prepare.add_argument("--archive", default="processed_val.zip")
    prepare.add_argument("--topic", default="KJ")
    prepare.add_argument("--speaker")
    prepare.add_argument("--clip-count", type=int, default=30)
    prepare.add_argument("--max-compressed-mib", type=int, default=64)
    prepare.add_argument(
        "--reuse-extracted",
        action="store_true",
        help="rebuild from a provenance-matched existing extraction without network access",
    )
    prepare.set_defaults(handler=_prepare_chinese_lips)

    evaluate = subparsers.add_parser(
        "evaluate-asr",
        help="compute aggregate and per-clip CER against local restricted ground truth",
    )
    evaluate.add_argument("--video-id", required=True)
    evaluate.add_argument("--artifacts-dir", type=Path, default=Path("artifacts"))
    evaluate.set_defaults(handler=_evaluate_asr)

    transcript_ocr = subparsers.add_parser(
        "transcript-ocr",
        help="extract deduplicated burned-in subtitle OCR events from one local video",
    )
    transcript_ocr.add_argument("video_path")
    transcript_ocr.add_argument("--video-id", required=True)
    transcript_ocr.add_argument("--roi", required=True, help="normalized x1,y1,x2,y2")
    transcript_ocr.add_argument("--sample-fps", type=float, default=2.0)
    transcript_ocr.add_argument("--start-ms", type=int, default=0)
    transcript_ocr.add_argument("--end-ms", type=int)
    transcript_ocr.add_argument("--output", type=Path, required=True)
    transcript_ocr.set_defaults(handler=_transcript_ocr)

    fuse = subparsers.add_parser(
        "fuse-transcript",
        help="align ASR, subtitle-track, and OCR events into the canonical transcript",
    )
    fuse.add_argument("--manifest", type=Path, required=True)
    fuse.add_argument("--asr", type=Path, required=True)
    fuse.add_argument("--ocr", type=Path)
    fuse.add_argument("--subtitle", type=Path)
    fuse.add_argument("--output-root", type=Path, required=True)
    fuse.add_argument(
        "--transcript-mode", choices=("asr-only", "fused"), default="fused"
    )
    fuse.set_defaults(handler=_fuse_transcript)

    ingest = subparsers.add_parser("ingest", help="extract, transcribe, and segment one MP4")
    ingest.add_argument("video_path")
    ingest.add_argument("--video-id", required=True)
    ingest.add_argument("--artifacts-dir", type=Path, default=Path("artifacts"))
    ingest.add_argument(
        "--asr-model",
        default=os.getenv("VIDEO_EVIDENCE_ASR_MODEL", "mlx-community/whisper-large-v3-turbo"),
        help="MLX Whisper model ID or local model path",
    )
    ingest.add_argument("--preview-seconds", type=int, default=300)
    ingest.add_argument("--target-segment-ms", type=int, default=45_000)
    ingest.add_argument("--max-segment-ms", type=int, default=60_000)
    ingest.add_argument(
        "--transcript-mode", choices=("asr-only", "fused"), default="fused"
    )
    ingest.add_argument("--ocr-mode", choices=("off", "roi", "auto"), default="off")
    ingest.add_argument("--ocr-roi", help="normalized x1,y1,x2,y2 for explicit ROI OCR")
    ingest.add_argument("--subtitle-file", type=Path)
    ingest.add_argument("--source-url")
    ingest.add_argument("--source-license")
    ingest.add_argument("--source-attribution")
    ingest.add_argument(
        "--source-use-note",
        default="local P0-A smoke only; raw media is not committed",
    )
    ingest.set_defaults(handler=_ingest)

    ask = subparsers.add_parser("ask", help="retrieve then answer one question using a real model")
    ask.add_argument("video_id")
    ask.add_argument("--question", required=True)
    ask.add_argument("--question-id")
    ask.add_argument("--top-k", type=int, default=5)
    ask.add_argument("--artifacts-dir", type=Path, default=Path("artifacts"))
    ask.set_defaults(handler=_ask)

    smoke = subparsers.add_parser("smoke", help="run the frozen 3-5 question smoke set")
    smoke.add_argument("video_id")
    smoke.add_argument("--questions", type=Path, required=True)
    smoke.add_argument("--top-k", type=int, default=5)
    smoke.add_argument("--artifacts-dir", type=Path, default=Path("artifacts"))
    smoke.set_defaults(handler=_smoke)

    review = subparsers.add_parser(
        "review",
        help="generate a human-review draft from real P0-A artifacts",
    )
    review.add_argument("video_id")
    review.add_argument("--questions", type=Path, required=True)
    review.add_argument("--artifacts-dir", type=Path, default=Path("artifacts"))
    review.add_argument("--report", type=Path, default=Path("reports/p0a-smoke-report.md"))
    review.set_defaults(handler=_review)

    p0b_freeze = subparsers.add_parser(
        "p0b-freeze",
        help="freeze the P0-B corpus, questions, Gold, prompts, and source hashes",
    )
    p0b_freeze.add_argument("--project-root", type=Path, default=Path("."))
    p0b_freeze.add_argument("--eval-revision", default="p0b-r1")
    p0b_freeze.add_argument("--corpus", type=Path, default=Path("eval/p0b/corpus.jsonl"))
    p0b_freeze.add_argument("--questions", type=Path, default=Path("eval/p0b/questions.jsonl"))
    p0b_freeze.add_argument("--gold", type=Path, default=Path("eval/p0b/gold.jsonl"))
    p0b_freeze.add_argument(
        "--manifest-out",
        type=Path,
        help="write a new revision-specific manifest without touching the default r1 manifest",
    )
    p0b_freeze.add_argument(
        "--gold-revision",
        help="revision of a deliberately reused Gold file, for example p0b-r1",
    )
    p0b_freeze.add_argument(
        "--answer-prompt", type=Path, default=Path("eval/p0b/prompts/transcript-retrieval-v1.md")
    )
    p0b_freeze.add_argument("--media-root", type=Path, default=Path("eval/p0b/media"))
    p0b_freeze.set_defaults(handler=_p0b_freeze)

    p0b_ingest = subparsers.add_parser(
        "p0b-ingest",
        help="run the existing FFmpeg/Chinese ASR ingest for every frozen corpus video",
    )
    p0b_ingest.add_argument("--project-root", type=Path, default=Path("."))
    p0b_ingest.add_argument("--corpus", type=Path, default=Path("eval/p0b/corpus.jsonl"))
    p0b_ingest.add_argument("--questions", type=Path)
    p0b_ingest.add_argument("--media-root", type=Path, default=Path("eval/p0b/media"))
    p0b_ingest.add_argument("--asr-model", default=os.getenv("VIDEO_EVIDENCE_ASR_MODEL", ""))
    p0b_ingest.add_argument("--preview-seconds", type=int, default=300)
    p0b_ingest.add_argument("--target-segment-ms", type=int, default=45_000)
    p0b_ingest.add_argument("--max-segment-ms", type=int, default=60_000)
    p0b_ingest.set_defaults(handler=_p0b_ingest)

    p0b_run = subparsers.add_parser(
        "p0b-run",
        help="run one locked TRANSCRIPT_RETRIEVAL result per frozen question",
    )
    p0b_run.add_argument("--project-root", type=Path, default=Path("."))
    p0b_run.add_argument("--manifest", type=Path, default=Path("eval/p0b/eval-manifest.json"))
    p0b_run.add_argument("--media-root", type=Path, default=Path("eval/p0b/media"))
    p0b_run.set_defaults(handler=_p0b_run)

    p0b_grade = subparsers.add_parser(
        "p0b-grade",
        help="grade preserved P0-B results after the locked run",
    )
    p0b_grade.add_argument("--project-root", type=Path, default=Path("."))
    p0b_grade.add_argument("--manifest", type=Path, default=Path("eval/p0b/eval-manifest.json"))
    p0b_grade.set_defaults(handler=_p0b_grade)

    p0b_report = subparsers.add_parser(
        "p0b-report",
        help="grade and render the P0-B report without changing result artifacts",
    )
    p0b_report.add_argument("--project-root", type=Path, default=Path("."))
    p0b_report.add_argument("--manifest", type=Path, default=Path("eval/p0b/eval-manifest.json"))
    p0b_report.add_argument("--report", type=Path, default=Path("reports/p0b-retrieval-eval.md"))
    p0b_report.set_defaults(handler=_p0b_report)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.handler(args)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
