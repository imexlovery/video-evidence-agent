"""Freeze, run, grade, and report the P0-B transcript-retrieval evaluation.

The formal P0-B chain is deliberately one file-backed method:

    local media -> FFmpeg/MLX Whisper -> VideoSegment -> character TF-IDF
    -> DeepSeek text answerer -> deterministic evidence gate -> Gold grader

The answerer receives only one question and that question's current Top-5
segments. Gold is loaded only by the grading and human-review path.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any

from video_evidence_agent.answering import (
    AnsweringConfigurationError,
    AnsweringProviderError,
    request_answer_traced,
)
from video_evidence_agent.audio import probe_media_duration_ms
from video_evidence_agent.evidence import gate_answer
from video_evidence_agent.p0b_schemas import (
    CorpusRecord,
    EvaluationMethod,
    P0BGoldRecord,
    P0BQuestion,
    QuestionType,
    load_jsonl,
    validate_gold_segments,
    validate_p0b_dataset,
)
from video_evidence_agent.retrieval import RetrievalError, retrieve
from video_evidence_agent.schemas import AnswerStatus, RetrievalHit, VideoSegment
from video_evidence_agent.segments import validate_video_segments


class P0BEvaluationError(RuntimeError):
    """Raised when a P0-B artifact or run would violate the locked contract."""


METHOD = EvaluationMethod.TRANSCRIPT_RETRIEVAL.value
EXPECTED_SEGMENT_COUNT = 127


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(f"{path.name}.partial")
    temporary_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(path)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise P0BEvaluationError(f"required P0-B JSON artifact does not exist: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise P0BEvaluationError(f"invalid JSON artifact: {path}") from exc
    if not isinstance(payload, dict):
        raise P0BEvaluationError(f"P0-B artifact must contain an object: {path}")
    return payload


def _relative(path: Path, project_root: Path) -> str:
    try:
        return path.resolve().relative_to(project_root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def _load_segments(path: Path, video_id: str) -> list[VideoSegment]:
    if not path.is_file():
        raise P0BEvaluationError(f"P0-B segments artifact does not exist: {path}")
    segments: list[VideoSegment] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            segment = VideoSegment.model_validate_json(line)
        except ValueError as exc:
            raise P0BEvaluationError(f"invalid VideoSegment at {path}:{line_number}") from exc
        if segment.video_id != video_id:
            raise P0BEvaluationError(f"segment video_id mismatch at {path}:{line_number}")
        segments.append(segment)
    try:
        validate_video_segments(segments)
    except RuntimeError as exc:
        raise P0BEvaluationError(f"invalid P0-B segment invariants: {path}") from exc
    return segments


def _source_files(project_root: Path) -> dict[str, str]:
    excluded_parts = {".git", ".venv", ".pytest_cache", ".ruff_cache", "artifacts"}
    files: dict[str, str] = {}
    for path in sorted(project_root.rglob("*.py")):
        if any(part in excluded_parts or part == "__pycache__" for part in path.parts):
            continue
        files[_relative(path, project_root)] = _sha256(path)
    for relative_path in ("pyproject.toml", "uv.lock"):
        path = project_root / relative_path
        if path.is_file():
            files[relative_path] = _sha256(path)
    return files


def _git_commit(project_root: Path) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    )
    commit = result.stdout.strip()
    return commit or None


def _configured_bool(*names: str) -> bool:
    return any(os.getenv(name, "").strip() for name in names)


def _answer_model_snapshot() -> dict[str, Any]:
    timeout_text = os.getenv("VIDEO_EVIDENCE_TIMEOUT_SECONDS", "120").strip()
    try:
        timeout_seconds = float(timeout_text)
    except ValueError as exc:
        raise P0BEvaluationError("VIDEO_EVIDENCE_TIMEOUT_SECONDS must be numeric") from exc
    if timeout_seconds <= 0:
        raise P0BEvaluationError("VIDEO_EVIDENCE_TIMEOUT_SECONDS must be positive")
    return {
        "provider": os.getenv("OPENAI_BASE_URL", "openai-compatible").strip()
        or "openai-compatible",
        "model": os.getenv("VIDEO_EVIDENCE_MODEL", "").strip() or None,
        "credential_present": _configured_bool("OPENAI_API_KEY"),
        "temperature": 0,
        "timeout_seconds": timeout_seconds,
        "response_schema": "AnswerProposal: status, answer, citation_segment_ids",
    }


def _expected_p0a_hashes(project_root: Path) -> dict[str, dict[str, str | bool | None]]:
    expected = {
        "reports/p0a-smoke-report.md": (
            "a57a15207c95f1c8217590a270cc30ce811001810f3fa6e25923953aed64ea9a"
        ),
        "artifacts/chinese-lips-mini-val-kj-001/smoke-run.json": (
            "55563f08c99a709347e0715917e66028767f79b0066265ab5d5c866fbe11cf74"
        ),
        "artifacts/chinese-lips-mini-val-kj-001/human-review.json": (
            "04d817974af0b73aeb39ce650ee980fe0ef6c904226c30ae147cc8dd20e23ed4"
        ),
        "pyproject.toml": "1b667d5de7cbc36a8c8cba0c8610c2d5acb0f36be98a7b248040b6fe4f6b6b7a",
        "uv.lock": "d62819c00268e64ff00d958b2cc5ebff587ed1f576c0e67e219999edb52d4851",
    }
    return {
        relative_path: {
            "expected_sha256": expected_hash,
            "actual_sha256": _sha256(project_root / relative_path)
            if (project_root / relative_path).is_file()
            else None,
            "verified": (project_root / relative_path).is_file()
            and _sha256(project_root / relative_path) == expected_hash,
        }
        for relative_path, expected_hash in expected.items()
    }


def _manifest_path(project_root: Path) -> Path:
    return project_root / "eval" / "p0b" / "eval-manifest.json"


def _resolve_media(media_root: Path, local_path_alias: str) -> Path:
    alias = Path(local_path_alias).expanduser()
    if alias.is_absolute():
        return alias
    if ".." in alias.parts:
        raise P0BEvaluationError("local_path_alias must not escape the media root")
    return media_root / alias


def _validate_media_record(record: CorpusRecord, media_root: Path) -> dict[str, Any]:
    media_path = _resolve_media(media_root, record.local_path_alias)
    if not media_path.is_file():
        raise P0BEvaluationError(f"corpus media does not exist: {media_path}")
    actual_hash = _sha256(media_path)
    if actual_hash != record.media_sha256:
        raise P0BEvaluationError(f"media hash mismatch for {record.video_id}")
    actual_duration_ms = probe_media_duration_ms(media_path)
    if actual_duration_ms != record.duration_ms:
        raise P0BEvaluationError(f"media duration mismatch for {record.video_id}")
    return {
        "video_id": record.video_id,
        "path": media_path.name,
        "sha256": actual_hash,
        "duration_ms": actual_duration_ms,
        "size_bytes": media_path.stat().st_size,
    }


def _ingest_for_video(
    *,
    project_root: Path,
    corpus_record: CorpusRecord,
) -> list[VideoSegment]:
    artifact_root = project_root / corpus_record.ingest_artifact_relpath
    manifest = _read_json(artifact_root / "manifest.json")
    if manifest.get("pipeline_status") != "SUCCEEDED":
        raise P0BEvaluationError(f"ingest is not successful for {corpus_record.video_id}")
    source = manifest.get("source")
    if not isinstance(source, dict) or source.get("sha256") != corpus_record.media_sha256:
        raise P0BEvaluationError(f"ingest source hash mismatch for {corpus_record.video_id}")
    if int(source.get("duration_ms", 0)) != corpus_record.duration_ms:
        raise P0BEvaluationError(f"ingest duration mismatch for {corpus_record.video_id}")
    return _load_segments(artifact_root / "segments.jsonl", corpus_record.video_id)


def _ingest_snapshot(
    *,
    project_root: Path,
    record: CorpusRecord,
    segments: list[VideoSegment],
) -> dict[str, Any]:
    artifact_root = project_root / record.ingest_artifact_relpath
    manifest_path = artifact_root / "manifest.json"
    segments_path = artifact_root / "segments.jsonl"
    manifest = _read_json(manifest_path)
    return {
        "video_id": record.video_id,
        "artifact_relpath": record.ingest_artifact_relpath,
        "manifest_sha256": _sha256(manifest_path),
        "segments_sha256": _sha256(segments_path),
        "segment_count": len(segments),
        "asr_model": manifest.get("asr", {}).get("model"),
    }


def _validate_formal_artifacts(
    *,
    project_root: Path,
    corpus: list[CorpusRecord],
    questions: list[P0BQuestion],
    gold: list[P0BGoldRecord],
    eval_revision: str,
    media_root: Path | None,
) -> tuple[dict[str, list[VideoSegment]], list[dict[str, Any]], list[dict[str, Any]]]:
    validate_p0b_dataset(corpus, questions, gold, eval_revision=eval_revision)
    media_snapshots: list[dict[str, Any]] = []
    if media_root is not None:
        for record in corpus:
            media_snapshots.append(_validate_media_record(record, media_root))

    segments_by_video: dict[str, list[VideoSegment]] = {}
    ingest_snapshots: list[dict[str, Any]] = []
    for record in corpus:
        segments = _ingest_for_video(project_root=project_root, corpus_record=record)
        segments_by_video[record.video_id] = segments
        ingest_snapshots.append(
            _ingest_snapshot(project_root=project_root, record=record, segments=segments)
        )
    total_segments = sum(len(segments) for segments in segments_by_video.values())
    if total_segments != EXPECTED_SEGMENT_COUNT:
        raise P0BEvaluationError(
            f"P0-B requires {EXPECTED_SEGMENT_COUNT} ingested VideoSegments, got {total_segments}"
        )
    validate_gold_segments(
        gold,
        segments_by_video,
        {record.video_id: record for record in corpus},
    )
    return segments_by_video, media_snapshots, ingest_snapshots


def freeze_p0b(
    *,
    project_root: Path,
    eval_revision: str,
    corpus_path: Path,
    questions_path: Path,
    gold_path: Path,
    answer_prompt_path: Path,
    media_root: Path | None = None,
) -> dict[str, Any]:
    """Create the immutable P0-B manifest before the single formal run."""

    manifest_path = _manifest_path(project_root)
    if manifest_path.exists():
        raise P0BEvaluationError(
            f"P0-B manifest already exists and is immutable: {manifest_path}; create a new revision"
        )
    corpus = load_jsonl(corpus_path, CorpusRecord)
    questions = load_jsonl(questions_path, P0BQuestion)
    gold = load_jsonl(gold_path, P0BGoldRecord)
    if not answer_prompt_path.is_file():
        raise P0BEvaluationError(f"P0-B answer prompt file does not exist: {answer_prompt_path}")
    media_root = media_root or project_root / "eval" / "p0b" / "media"
    _, media_snapshots, ingest_snapshots = _validate_formal_artifacts(
        project_root=project_root,
        corpus=corpus,
        questions=questions,
        gold=gold,
        eval_revision=eval_revision,
        media_root=media_root,
    )
    p0a_hashes = _expected_p0a_hashes(project_root)
    if not all(bool(item["verified"]) for item in p0a_hashes.values()):
        raise P0BEvaluationError("P0-A anchor hashes do not match; refuse to start P0-B")
    answer_model = _answer_model_snapshot()
    if not answer_model["credential_present"] or not answer_model["model"]:
        raise P0BEvaluationError(
            "DeepSeek text configuration is incomplete; OPENAI_API_KEY and "
            "VIDEO_EVIDENCE_MODEL are required"
        )
    manifest = {
        "schema_version": 1,
        "eval_revision": eval_revision,
        "evaluation_method": METHOD,
        "status": "FROZEN",
        "locked_at": _utc_now(),
        "locked_by": "local-owner",
        "chain": {
            "media": "local-only input; no upload",
            "audio": "local FFmpeg",
            "asr": "local mlx-whisper Chinese transcription",
            "segments": "timestamped VideoSegment",
            "retrieval": "character 2-4 gram TF-IDF Top-5",
            "answering": "DeepSeek text model receives question plus current Top-5 only",
            "grading": "deterministic checks plus owner semantic review against Gold",
        },
        "corpus": {
            "path": _relative(corpus_path, project_root),
            "sha256": _sha256(corpus_path),
            "video_count": len(corpus),
            "videos": [record.model_dump(mode="json") for record in corpus],
        },
        "questions": {
            "path": _relative(questions_path, project_root),
            "sha256": _sha256(questions_path),
            "count": len(questions),
        },
        "gold": {
            "path": _relative(gold_path, project_root),
            "sha256": _sha256(gold_path),
            "count": len(gold),
        },
        "prompt": {
            "path": _relative(answer_prompt_path, project_root),
            "sha256": _sha256(answer_prompt_path),
        },
        "answer_model": answer_model,
        "media_snapshots": media_snapshots,
        "ingest_snapshots": ingest_snapshots,
        "p0a_anchors": p0a_hashes,
        "source_revision": {
            "git_commit": _git_commit(project_root),
            "files": _source_files(project_root),
        },
        "runtime": {"python": os.sys.version, "platform": os.uname().machine},
    }
    _write_json(manifest_path, manifest)
    return manifest


def _manifest_corpus(manifest: dict[str, Any]) -> list[CorpusRecord]:
    raw_videos = manifest.get("corpus", {}).get("videos")
    if not isinstance(raw_videos, list):
        raise P0BEvaluationError("frozen manifest has no corpus video records")
    try:
        return [CorpusRecord.model_validate(item) for item in raw_videos]
    except ValueError as exc:
        raise P0BEvaluationError("frozen manifest corpus records are invalid") from exc


def verify_frozen_manifest(
    project_root: Path,
    manifest: dict[str, Any],
    *,
    media_root: Path | None = None,
) -> None:
    """Fail closed if frozen inputs, media, ingest, or source files changed."""

    if manifest.get("evaluation_method") != METHOD:
        raise P0BEvaluationError("frozen manifest does not use TRANSCRIPT_RETRIEVAL")
    expected_paths = [
        (manifest["corpus"]["path"], manifest["corpus"]["sha256"]),
        (manifest["questions"]["path"], manifest["questions"]["sha256"]),
        (manifest["gold"]["path"], manifest["gold"]["sha256"]),
        (manifest["prompt"]["path"], manifest["prompt"]["sha256"]),
    ]
    for relative_path, expected_hash in expected_paths:
        path = project_root / relative_path
        if not path.is_file() or _sha256(path) != expected_hash:
            raise P0BEvaluationError(f"frozen P0-B input changed: {relative_path}")
    for relative_path, expected_hash in manifest["source_revision"]["files"].items():
        path = project_root / relative_path
        if not path.is_file() or _sha256(path) != expected_hash:
            raise P0BEvaluationError(f"frozen P0-B source changed: {relative_path}")

    corpus = _manifest_corpus(manifest)
    media_root = media_root or project_root / "eval" / "p0b" / "media"
    for record in corpus:
        _validate_media_record(record, media_root)
        artifact_root = project_root / record.ingest_artifact_relpath
        snapshot = next(
            (
                item
                for item in manifest.get("ingest_snapshots", [])
                if item.get("video_id") == record.video_id
            ),
            None,
        )
        if not isinstance(snapshot, dict):
            raise P0BEvaluationError(f"frozen manifest has no ingest snapshot: {record.video_id}")
        for filename, key in (
            ("manifest.json", "manifest_sha256"),
            ("segments.jsonl", "segments_sha256"),
        ):
            path = artifact_root / filename
            if not path.is_file() or _sha256(path) != snapshot.get(key):
                raise P0BEvaluationError(f"frozen ingest artifact changed: {path}")


def _retrieval_payload(
    *,
    eval_revision: str,
    question: P0BQuestion,
    hits: list[RetrievalHit],
    elapsed_ms: int,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "eval_revision": eval_revision,
        "evaluation_method": METHOD,
        "video_id": question.video_id,
        "question_id": question.question_id,
        "question": question.question,
        "top_k_requested": 5,
        "retrieval_latency_ms": elapsed_ms,
        "hits": [hit.model_dump(mode="json") for hit in hits],
    }


def _safe_failure_message(exc: Exception) -> str:
    message = str(exc)
    for name in ("OPENAI_API_KEY",):
        secret = os.getenv(name, "").strip()
        if secret:
            message = message.replace(secret, "[REDACTED]")
    return message


def _failure_type(exc: Exception) -> str:
    cause = exc.__cause__
    if isinstance(exc, TimeoutError) or isinstance(cause, TimeoutError):
        return "timeout"
    if isinstance(exc, (AnsweringConfigurationError, AnsweringProviderError)):
        return "provider"
    if isinstance(exc, RetrievalError):
        return "retrieval"
    if isinstance(exc, P0BEvaluationError):
        return "ingest"
    return type(exc).__name__.lower()


def _write_failure(
    path: Path,
    *,
    eval_revision: str,
    question: P0BQuestion,
    exc: Exception,
    stage: str,
) -> None:
    payload: dict[str, Any] = {
        "schema_version": 1,
        "eval_revision": eval_revision,
        "evaluation_method": METHOD,
        "video_id": question.video_id,
        "question_id": question.question_id,
        "question": question.question,
        "call_status": "FAILED",
        "answer_status": None,
        "answer": None,
        "evidence": [],
        "failure_stage": stage,
        "failure_type": _failure_type(exc),
        "failure_class": type(exc).__name__,
        "failure_cause_class": type(exc.__cause__).__name__ if exc.__cause__ else None,
        "failure_message": _safe_failure_message(exc),
        "latency_ms": 0,
        "retrieval_latency_ms": None,
        "usage": {},
        "schema_valid": False,
    }
    _write_json(path, payload)


def _run_transcript_question(
    *,
    artifact_root: Path,
    eval_revision: str,
    question: P0BQuestion,
    segments: list[VideoSegment],
    answer_prompt: str,
) -> None:
    result_dir = artifact_root / "transcript-retrieval" / question.question_id
    result_path = result_dir / "result.json"
    try:
        retrieval_started_at = perf_counter()
        hits = retrieve(question.question, segments, top_k=5)
        retrieval_elapsed_ms = round((perf_counter() - retrieval_started_at) * 1000)
        # This write is intentionally before the only answer-model call.
        _write_json(
            result_dir / "retrieval.json",
            _retrieval_payload(
                eval_revision=eval_revision,
                question=question,
                hits=hits,
                elapsed_ms=retrieval_elapsed_ms,
            ),
        )
        trace = request_answer_traced(
            question.question,
            hits,
            system_instruction=answer_prompt,
        )
        raw_response_path: str | None = None
        if trace.raw_response is not None:
            _write_json(result_dir / "raw-response.json", trace.raw_response)
            raw_response_path = "raw-response.json"
        decision = gate_answer(trace.proposal, hits)
        _write_json(
            result_path,
            {
                "schema_version": 1,
                "eval_revision": eval_revision,
                "evaluation_method": METHOD,
                "video_id": question.video_id,
                "question_id": question.question_id,
                "question": question.question,
                "call_status": "SUCCEEDED",
                "answer_status": decision.result.status,
                "answer": decision.result.answer,
                "evidence": [
                    item.model_dump(mode="json") for item in decision.result.evidence
                ],
                "gate_reason": decision.reason,
                "schema_valid": trace.schema_valid,
                "schema_failure": not trace.schema_valid,
                "provider": trace.provider,
                "model": trace.model,
                "latency_ms": trace.latency_ms,
                "retrieval_latency_ms": retrieval_elapsed_ms,
                "usage": trace.usage,
                "raw_response_path": raw_response_path,
            },
        )
    except Exception as exc:
        stage = "retrieval" if isinstance(exc, RetrievalError) else "answering"
        _write_failure(
            result_path,
            eval_revision=eval_revision,
            question=question,
            exc=exc,
            stage=stage,
        )


def run_p0b_transcript_retrieval(
    *,
    project_root: Path,
    manifest: dict[str, Any],
    media_root: Path | None = None,
) -> dict[str, Any]:
    """Run exactly one text answer attempt per frozen question."""

    verify_frozen_manifest(project_root, manifest, media_root=media_root)
    eval_revision = str(manifest["eval_revision"])
    artifact_root = project_root / "artifacts" / "p0b" / eval_revision
    if artifact_root.exists() and any(artifact_root.iterdir()):
        raise P0BEvaluationError(f"P0-B run already exists and is immutable: {artifact_root}")
    corpus = load_jsonl(project_root / manifest["corpus"]["path"], CorpusRecord)
    questions = load_jsonl(project_root / manifest["questions"]["path"], P0BQuestion)
    validate_p0b_dataset(corpus, questions, eval_revision=eval_revision)
    answer_prompt = (project_root / manifest["prompt"]["path"]).read_text(encoding="utf-8")
    questions_by_video: dict[str, list[P0BQuestion]] = defaultdict(list)
    for question in questions:
        questions_by_video[question.video_id].append(question)

    started_at = _utc_now()
    for record in corpus:
        video_questions = questions_by_video[record.video_id]
        try:
            segments = _ingest_for_video(project_root=project_root, corpus_record=record)
        except Exception as exc:
            for question in video_questions:
                _write_failure(
                    artifact_root / "transcript-retrieval" / question.question_id / "result.json",
                    eval_revision=eval_revision,
                    question=question,
                    exc=exc,
                    stage="ingest",
                )
            continue
        for question in video_questions:
            _run_transcript_question(
                artifact_root=artifact_root,
                eval_revision=eval_revision,
                question=question,
                segments=segments,
                answer_prompt=answer_prompt,
            )

    result_manifest = {
        "schema_version": 1,
        "eval_revision": eval_revision,
        "evaluation_method": METHOD,
        "status": "RESULTS_RECORDED",
        "started_at": started_at,
        "completed_at": _utc_now(),
        "eval_manifest_sha256": _sha256(_manifest_path(project_root)),
        "question_count": len(questions),
        "result_count": len(questions),
        "expected_result_count": len(questions),
        "answer_model": manifest.get("answer_model", {}),
        "mock_used": False,
        "video_upload": False,
    }
    _write_json(artifact_root / "run-manifest.json", result_manifest)
    return result_manifest


def _load_result(path: Path) -> dict[str, Any]:
    return _read_json(path)


def _load_retrieval_hits(path: Path) -> list[RetrievalHit]:
    payload = _read_json(path)
    if payload.get("evaluation_method") != METHOD:
        raise P0BEvaluationError(f"retrieval artifact method mismatch: {path}")
    raw_hits = payload.get("hits")
    if not isinstance(raw_hits, list):
        raise P0BEvaluationError(f"retrieval artifact has no hits: {path}")
    try:
        hits = [RetrievalHit.model_validate(item) for item in raw_hits]
    except ValueError as exc:
        raise P0BEvaluationError(f"invalid retrieval artifact: {path}") from exc
    return sorted(hits, key=lambda hit: hit.rank)


def _interval_coverage(candidate: tuple[int, int], gold: tuple[int, int]) -> float:
    start_ms = max(candidate[0], gold[0])
    end_ms = min(candidate[1], gold[1])
    overlap = max(0, end_ms - start_ms)
    return overlap / (gold[1] - gold[0])


def _unit_hit(candidate: tuple[int, int], unit: Any) -> bool:
    return _interval_coverage(candidate, (unit.start_ms, unit.end_ms)) >= 0.5


def _retrieval_metrics(hits: list[RetrievalHit], gold: P0BGoldRecord) -> dict[str, Any]:
    answerable_units = gold.gold_evidence_units
    if not answerable_units:
        return {
            "question_hit_at_1": None,
            "question_hit_at_5": None,
            "evidence_unit_recall_at_5": None,
            "all_evidence_at_5": None,
            "mrr": None,
            "hit_units_at_5": 0,
            "unit_count": 0,
        }
    top_hits = hits[:5]
    hit_units_at_5 = sum(
        any(_unit_hit((hit.segment.start_ms, hit.segment.end_ms), unit) for hit in top_hits)
        for unit in answerable_units
    )
    hit_at_1 = (
        any(
            _unit_hit((hits[0].segment.start_ms, hits[0].segment.end_ms), unit)
            for unit in answerable_units
        )
        if hits
        else False
    )
    first_hit_rank = next(
        (
            hit.rank
            for hit in top_hits
            if any(
                _unit_hit((hit.segment.start_ms, hit.segment.end_ms), unit)
                for unit in answerable_units
            )
        ),
        None,
    )
    return {
        "question_hit_at_1": hit_at_1,
        "question_hit_at_5": hit_units_at_5 > 0,
        "evidence_unit_recall_at_5": hit_units_at_5 / len(answerable_units),
        "all_evidence_at_5": hit_units_at_5 == len(answerable_units),
        "mrr": 1 / first_hit_rank if first_hit_rank is not None else 0,
        "hit_units_at_5": hit_units_at_5,
        "unit_count": len(answerable_units),
    }


def _result_intervals(result: dict[str, Any]) -> list[tuple[int, int]]:
    intervals: list[tuple[int, int]] = []
    for item in result.get("evidence", []):
        if not isinstance(item, dict):
            continue
        try:
            start_ms = int(item["start_ms"])
            end_ms = int(item["end_ms"])
        except (KeyError, TypeError, ValueError):
            continue
        if end_ms > start_ms >= 0:
            intervals.append((start_ms, end_ms))
    return intervals


def _citation_provenance(result: dict[str, Any], hits: list[RetrievalHit]) -> bool:
    if result.get("evaluation_method") != METHOD or result.get("call_status") != "SUCCEEDED":
        return False
    if result.get("answer_status") == AnswerStatus.INSUFFICIENT_EVIDENCE:
        return not result.get("evidence")
    if result.get("answer_status") != AnswerStatus.ANSWERED:
        return False
    allowed = {hit.segment.segment_id: hit.segment for hit in hits}
    evidence = result.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        return False
    for citation in evidence:
        if not isinstance(citation, dict):
            return False
        segment = allowed.get(citation.get("segment_id"))
        if segment is None:
            return False
        if citation.get("quote") != segment.transcript_text:
            return False
        if citation.get("start_ms") != segment.start_ms:
            return False
        if citation.get("end_ms") != segment.end_ms:
            return False
    return result.get("gate_reason") == "citation_provenance_verified"


def _human_metrics(review_row: dict[str, Any] | None, answer_point_count: int) -> dict[str, Any]:
    if review_row is None:
        return {
            "answer_point_recall": None,
            "fully_correct_answer": None,
            "fully_supported_answer": None,
            "semantic_support": None,
        }
    coverage = review_row.get("answer_point_coverage")
    if isinstance(coverage, list) and answer_point_count:
        covered = sum(item is True for item in coverage[:answer_point_count])
        answer_point_recall = covered / answer_point_count
    else:
        answer_point_recall = None
    return {
        "answer_point_recall": answer_point_recall,
        "fully_correct_answer": review_row.get("fully_correct"),
        "fully_supported_answer": review_row.get("fully_supported"),
        "semantic_support": review_row.get("semantic_support"),
    }


def _grade_one(
    *,
    evaluation_method: EvaluationMethod,
    question: P0BQuestion,
    gold: P0BGoldRecord,
    result: dict[str, Any],
    retrieval_hits: list[RetrievalHit],
    review_row: dict[str, Any] | None,
) -> dict[str, Any]:
    if evaluation_method is not EvaluationMethod.TRANSCRIPT_RETRIEVAL:
        raise P0BEvaluationError(f"unsupported P0-B evaluation method: {evaluation_method}")
    retrieval = _retrieval_metrics(retrieval_hits, gold)
    intervals = _result_intervals(result)
    temporal_hit = (
        any(
            any(_unit_hit(interval, unit) for unit in gold.gold_evidence_units)
            for interval in intervals
        )
        if gold.should_answer
        else None
    )
    answer_status = result.get("answer_status")
    schema_failure = result.get("call_status") != "SUCCEEDED" or bool(
        result.get("schema_failure", False)
    )
    human = _human_metrics(review_row, len(gold.answer_points))
    expected_status = (
        AnswerStatus.ANSWERED if question.should_answer else AnswerStatus.INSUFFICIENT_EVIDENCE
    )
    return {
        "evaluation_method": evaluation_method.value,
        "video_id": question.video_id,
        "question_id": question.question_id,
        "question_type": question.question_type.value,
        "should_answer": question.should_answer,
        "call_status": result.get("call_status"),
        "answer_status": answer_status,
        "answer_status_accuracy": answer_status == expected_status,
        "failure_type": result.get("failure_type"),
        "retrieval": retrieval,
        "citation_provenance_verified": _citation_provenance(result, retrieval_hits),
        "citation_temporal_hit": temporal_hit,
        "correct_refusal": (
            not question.should_answer and answer_status == AnswerStatus.INSUFFICIENT_EVIDENCE
        ),
        "false_refusal": (
            question.should_answer and answer_status == AnswerStatus.INSUFFICIENT_EVIDENCE
        ),
        "schema_failure": schema_failure,
        "answer_point_recall": human["answer_point_recall"],
        "fully_correct_answer": human["fully_correct_answer"],
        "fully_supported_answer": human["fully_supported_answer"],
        "semantic_support": human["semantic_support"],
        "latency_ms": result.get("latency_ms"),
        "retrieval_latency_ms": result.get("retrieval_latency_ms"),
        "usage": result.get("usage", {}),
        "notes": result.get("failure_message"),
    }


def _count(rows: list[dict[str, Any]], key: str, *, expected: bool | None = True) -> dict[str, int]:
    eligible = [row for row in rows if expected is None or row["should_answer"] is expected]
    numerator = sum(row.get(key) is True for row in eligible)
    return {"numerator": numerator, "denominator": len(eligible)}


def _token_usage(rows: list[dict[str, Any]]) -> dict[str, Any]:
    totals: dict[str, int] = {}
    rows_with_usage = 0
    for row in rows:
        usage = row.get("usage")
        if not isinstance(usage, dict) or not usage:
            continue
        numeric = {key: value for key, value in usage.items() if isinstance(value, (int, float))}
        if not numeric:
            continue
        rows_with_usage += 1
        for key, value in numeric.items():
            totals[key] = totals.get(key, 0) + int(value)
    return {
        "available": bool(totals),
        "rows_with_usage": rows_with_usage,
        "totals": totals,
    }


def _aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    answerable = [row for row in rows if row["should_answer"]]
    ranked_answerable = [
        row for row in answerable if row["retrieval"]["question_hit_at_1"] is not None
    ]
    multi_ranked = [
        row
        for row in rows
        if row["question_type"] == QuestionType.MULTI_EVIDENCE.value
        and row["retrieval"]["all_evidence_at_5"] is not None
    ]
    recall_values = [
        float(row["retrieval"]["evidence_unit_recall_at_5"]) for row in ranked_answerable
    ]
    mrr_values = [float(row["retrieval"]["mrr"]) for row in ranked_answerable]
    answered_rows = [
        row
        for row in rows
        if row["call_status"] == "SUCCEEDED" and row["answer_status"] == AnswerStatus.ANSWERED
    ]
    answer_point_values = [
        float(row["answer_point_recall"])
        for row in rows
        if row["answer_point_recall"] is not None
    ]
    return {
        "question_count": len(rows),
        "answerable_count": len(answerable),
        "question_hit_at_1": {
            "numerator": sum(
                row["retrieval"]["question_hit_at_1"] is True for row in ranked_answerable
            ),
            "denominator": len(ranked_answerable),
        },
        "question_hit_at_5": {
            "numerator": sum(
                row["retrieval"]["question_hit_at_5"] is True for row in ranked_answerable
            ),
            "denominator": len(ranked_answerable),
        },
        "all_evidence_at_5": {
            "numerator": sum(row["retrieval"]["all_evidence_at_5"] is True for row in multi_ranked),
            "denominator": len(multi_ranked),
        },
        "evidence_unit_recall_at_5": {
            "mean": sum(recall_values) / len(recall_values) if recall_values else None
        },
        "mrr": {"mean": sum(mrr_values) / len(mrr_values) if mrr_values else None},
        "answer_status_accuracy": _count(rows, "answer_status_accuracy", expected=None),
        "correct_refusal": _count(rows, "correct_refusal", expected=False),
        "false_refusal": _count(rows, "false_refusal", expected=True),
        "citation_temporal_hit": _count(rows, "citation_temporal_hit", expected=True),
        "citation_provenance_invalid": {
            "numerator": sum(
                row["answer_status"] == AnswerStatus.ANSWERED
                and row["call_status"] == "SUCCEEDED"
                and not row["citation_provenance_verified"]
                for row in rows
            ),
            "denominator": len(answered_rows),
        },
        "schema_compliance": {
            "numerator": sum(not row["schema_failure"] for row in rows),
            "denominator": len(rows),
        },
        "schema_failure": {
            "numerator": sum(row["schema_failure"] for row in rows),
            "denominator": len(rows),
        },
        "answer_point_recall": {
            "mean": sum(answer_point_values) / len(answer_point_values)
            if answer_point_values
            else None
        },
        "fully_correct_answer": _count(rows, "fully_correct_answer", expected=True),
        "fully_supported_answer": _count(rows, "fully_supported_answer", expected=True),
        "semantic_support": _count(rows, "semantic_support", expected=True),
        "latency_ms": {
            "mean": sum(float(row["latency_ms"] or 0) for row in rows) / len(rows) if rows else None
        },
        "retrieval_latency_ms": {
            "mean": (
                sum(float(row["retrieval_latency_ms"] or 0) for row in rows) / len(rows)
                if rows
                else None
            )
        },
        "token_usage": _token_usage(rows),
    }


def _review_payload(
    *,
    question: P0BQuestion,
    gold: P0BGoldRecord,
    result: dict[str, Any],
) -> dict[str, Any]:
    return {
        "evaluation_method": METHOD,
        "video_id": question.video_id,
        "question_id": question.question_id,
        "question_type": question.question_type.value,
        "question": question.question,
        "should_answer": question.should_answer,
        "model_result": {
            "call_status": result.get("call_status"),
            "answer_status": result.get("answer_status"),
            "answer": result.get("answer"),
            "evidence": result.get("evidence", []),
            "failure_type": result.get("failure_type"),
            "failure_message": result.get("failure_message"),
        },
        "gold_reference": {
            "answer_points": gold.answer_points,
            "gold_evidence_units": [
                unit.model_dump(mode="json") for unit in gold.gold_evidence_units
            ],
            "unanswerable_rationale": gold.unanswerable_rationale,
        },
        "review": {
            "answer_point_coverage": None,
            "fully_correct": None,
            "fully_supported": None,
            "semantic_support": None,
            "notes": None,
        },
    }


def _write_human_review_materials(
    *,
    artifact_root: Path,
    questions: list[P0BQuestion],
    gold_by_id: dict[str, P0BGoldRecord],
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for question in questions:
        result_path = artifact_root / "transcript-retrieval" / question.question_id / "result.json"
        rows.append(
            _review_payload(
                question=question,
                gold=gold_by_id[question.question_id],
                result=_load_result(result_path),
            )
        )
    review = {
        "schema_version": 1,
        "status": "PENDING_OWNER_SEMANTIC_REVIEW",
        "reviewer": None,
        "reviewed_at": None,
        "instructions": (
            "Only the owner may fill review fields; deterministic provenance is not "
            "semantic support."
        ),
        "rows": rows,
    }
    _write_json(artifact_root / "human-review.json", review)
    jsonl_path = artifact_root / "human-review.jsonl"
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = jsonl_path.with_name(f"{jsonl_path.name}.partial")
    with temporary_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    temporary_path.replace(jsonl_path)
    return review


def _review_rows_by_question(review: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw_rows = review.get("rows")
    if not isinstance(raw_rows, list):
        return {}
    return {
        str(row["question_id"]): row.get("review", {})
        for row in raw_rows
        if isinstance(row, dict) and row.get("question_id") and isinstance(row.get("review"), dict)
    }


def grade_p0b(*, project_root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Auto-grade the one-method run and preserve the owner review boundary."""

    verify_frozen_manifest(project_root, manifest)
    eval_revision = str(manifest["eval_revision"])
    corpus = load_jsonl(project_root / manifest["corpus"]["path"], CorpusRecord)
    questions = load_jsonl(project_root / manifest["questions"]["path"], P0BQuestion)
    gold = load_jsonl(project_root / manifest["gold"]["path"], P0BGoldRecord)
    validate_p0b_dataset(corpus, questions, gold, eval_revision=eval_revision)
    corpus_by_video = {record.video_id: record for record in corpus}
    segments_by_video: dict[str, list[VideoSegment]] = {}
    for record in corpus:
        segments_by_video[record.video_id] = _ingest_for_video(
            project_root=project_root,
            corpus_record=record,
        )
    validate_gold_segments(gold, segments_by_video, corpus_by_video)

    artifact_root = project_root / "artifacts" / "p0b" / eval_revision
    run_manifest = _read_json(artifact_root / "run-manifest.json")
    if run_manifest.get("evaluation_method") != METHOD:
        raise P0BEvaluationError("run manifest method mismatch")
    review_path = artifact_root / "human-review.json"
    if review_path.is_file():
        human_review = _read_json(review_path)
    else:
        human_review = _write_human_review_materials(
            artifact_root=artifact_root,
            questions=questions,
            gold_by_id={item.question_id: item for item in gold},
        )
    review_by_question = _review_rows_by_question(human_review)
    gold_by_id = {answer_key.question_id: answer_key for answer_key in gold}
    rows: list[dict[str, Any]] = []
    for question in questions:
        result_path = artifact_root / "transcript-retrieval" / question.question_id / "result.json"
        result = _load_result(result_path)
        retrieval_path = (
            artifact_root
            / "transcript-retrieval"
            / question.question_id
            / "retrieval.json"
        )
        retrieval_hits = _load_retrieval_hits(retrieval_path) if retrieval_path.is_file() else []
        rows.append(
            _grade_one(
                evaluation_method=EvaluationMethod.TRANSCRIPT_RETRIEVAL,
                question=question,
                gold=gold_by_id[question.question_id],
                result=result,
                retrieval_hits=retrieval_hits,
                review_row=review_by_question.get(question.question_id),
            )
        )
    overall = _aggregate(rows)
    by_video = {
        video_id: _aggregate([row for row in rows if row["video_id"] == video_id])
        for video_id in corpus_by_video
    }
    by_question_type = {
        question_type.value: _aggregate(
            [row for row in rows if row["question_type"] == question_type.value]
        )
        for question_type in QuestionType
    }
    completed_calls = all(row["call_status"] == "SUCCEEDED" for row in rows)
    human_complete = human_review.get("status") == "COMPLETED"
    threshold_checks = {
        "question_hit_at_1_at_least_6_of_9": overall["question_hit_at_1"]["numerator"] >= 6,
        "question_hit_at_5_at_least_8_of_9": overall["question_hit_at_5"]["numerator"] >= 8,
        "multi_all_evidence_at_5_at_least_2_of_3": overall["all_evidence_at_5"]["numerator"] >= 2,
        "fully_supported_answer_at_least_7_of_9": (
            overall["fully_supported_answer"]["numerator"] >= 7
        ),
        "correct_refusal_at_least_2_of_3": overall["correct_refusal"]["numerator"] >= 2,
        "invalid_citation_provenance_is_zero": (
            overall["citation_provenance_invalid"]["numerator"] == 0
        ),
    }
    if not completed_calls:
        recommendation = "P0B_BLOCKED_EXECUTION_FAILURE"
        evaluation_status = "BLOCKED_EXECUTION_FAILURE"
    elif not human_complete:
        recommendation = "PENDING_OWNER_SEMANTIC_REVIEW"
        evaluation_status = "AUTO_SCORED_PENDING_OWNER_REVIEW"
    elif all(threshold_checks.values()):
        recommendation = "READY_FOR_OWNER_P0B_DECISION"
        evaluation_status = "OWNER_REVIEW_COMPLETE"
    else:
        recommendation = "P0B_RETRIEVAL_THRESHOLDS_NOT_MET"
        evaluation_status = "OWNER_REVIEW_COMPLETE"
    metrics = {
        "schema_version": 1,
        "eval_revision": eval_revision,
        "evaluation_method": METHOD,
        "generated_at": _utc_now(),
        "evaluation_status": evaluation_status,
        "human_review_status": human_review.get("status"),
        "result_count": len(rows),
        "expected_result_count": len(questions),
        "method": {
            "overall": overall,
            "by_video": by_video,
            "by_question_type": by_question_type,
        },
        "threshold_checks": threshold_checks,
        "recommendation": recommendation,
        "rows": rows,
    }
    _write_json(artifact_root / "metrics.json", metrics)
    return metrics


def _count_text(value: dict[str, int]) -> str:
    if value["denominator"] == 0:
        return "N/A"
    return f"{value['numerator']}/{value['denominator']}"


def _mean_text(value: dict[str, Any]) -> str:
    mean = value.get("mean")
    return "N/A" if mean is None else str(round(float(mean), 4))


def render_p0b_report(*, metrics: dict[str, Any], report_path: Path) -> None:
    """Render one-method metrics without turning machine checks into semantics."""

    method = metrics["method"]
    overall = method["overall"]
    rows = metrics.get("rows", [])
    lines = [
        "# P0-B Transcript Retrieval Evaluation Report",
        "",
        f"- eval_revision: `{metrics['eval_revision']}`",
        f"- evaluation_method: `{metrics['evaluation_method']}`",
        f"- evaluation_status: `{metrics['evaluation_status']}`",
        f"- human_review_status: `{metrics.get('human_review_status')}`",
        f"- recommendation: `{metrics['recommendation']}`",
        "",
        "## Scope and evidence boundary",
        "",
        (
            "The formal chain is three local Chinese technical videos, local FFmpeg and "
            "MLX Whisper Chinese ASR, 127 timestamped VideoSegments, character 2–4 gram "
            "TF-IDF Top-5, and one DeepSeek text answer call per question. No video is "
            "uploaded to an answer provider."
        ),
        (
            "The answer model receives only the question and its current Top-5 segments. "
            "Gold, full transcripts, and answer points are excluded from that call."
        ),
        (
            "Retrieval, deterministic citation provenance, timestamp overlap, schema "
            "compliance, model status, and owner semantic review are reported separately."
        ),
        "",
        "## Overall metrics",
        "",
        (
            "| method | results | QuestionHit@1 | QuestionHit@5 | Gold evidence-unit "
            "recall@5 | AllEvidence@5 (multi) | MRR | answer/refusal accuracy | "
            "correct refusal | provenance invalid | schema failures | mean latency ms |"
        ),
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        "| "
        + " | ".join(
            [
                metrics["evaluation_method"],
                str(overall["question_count"]),
                _count_text(overall["question_hit_at_1"]),
                _count_text(overall["question_hit_at_5"]),
                _mean_text(overall["evidence_unit_recall_at_5"]),
                _count_text(overall["all_evidence_at_5"]),
                _mean_text(overall["mrr"]),
                _count_text(overall["answer_status_accuracy"]),
                _count_text(overall["correct_refusal"]),
                _count_text(overall["citation_provenance_invalid"]),
                _count_text(overall["schema_failure"]),
                _mean_text(overall["latency_ms"]),
            ]
        )
        + " |",
        "",
        "Token usage (provider-reported, if available): "
        + json.dumps(overall["token_usage"], ensure_ascii=False),
        "",
        "## Deterministic checks",
        "",
        "| check | result |",
        "| --- | --- |",
    ]
    for name, value in metrics["threshold_checks"].items():
        lines.append(f"| {name} | {'PASS' if value else 'FAIL'} |")
    lines.extend(
        [
            "",
            "Additional deterministic metrics: "
            f"temporal citation hit `{_count_text(overall['citation_temporal_hit'])}`, "
            f"schema compliance `{_count_text(overall['schema_compliance'])}`, "
            f"mean retrieval latency `{_mean_text(overall['retrieval_latency_ms'])} ms`. ",
            "",
            "## Per-video and question-type slices",
            "",
            "| slice | QuestionHit@5 | AllEvidence@5 | answer/refusal accuracy | "
            "correct refusal | fully supported (owner) | schema failures |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for slice_name, aggregate in method["by_video"].items():
        lines.append(
            f"| video `{slice_name}` | {_count_text(aggregate['question_hit_at_5'])} | "
            f"{_count_text(aggregate['all_evidence_at_5'])} | "
            f"{_count_text(aggregate['answer_status_accuracy'])} | "
            f"{_count_text(aggregate['correct_refusal'])} | "
            f"{_count_text(aggregate['fully_supported_answer'])} | "
            f"{_count_text(aggregate['schema_failure'])} |"
        )
    for slice_name, aggregate in method["by_question_type"].items():
        lines.append(
            f"| type `{slice_name}` | {_count_text(aggregate['question_hit_at_5'])} | "
            f"{_count_text(aggregate['all_evidence_at_5'])} | "
            f"{_count_text(aggregate['answer_status_accuracy'])} | "
            f"{_count_text(aggregate['correct_refusal'])} | "
            f"{_count_text(aggregate['fully_supported_answer'])} | "
            f"{_count_text(aggregate['schema_failure'])} |"
        )
    lines.extend(
        [
            "",
            "## Per-question audit trail",
            "",
            "| video | question | type | call | answer status | answer/refusal | hit@1 | "
            "hit@5 | temporal citation | provenance | schema | owner review | failure |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        retrieval = row["retrieval"]
        owner_review = row["fully_supported_answer"]
        lines.append(
            f"| {row['video_id']} | {row['question_id']} | {row['question_type']} | "
            f"{row['call_status']} | {row['answer_status']} | {row['answer_status_accuracy']} | "
            f"{retrieval['question_hit_at_1']} | {retrieval['question_hit_at_5']} | "
            f"{row['citation_temporal_hit']} | {row['citation_provenance_verified']} | "
            f"{not row['schema_failure']} | {owner_review} | {row.get('failure_type') or ''} |"
        )
    lines.extend(
        [
            "",
            "## Human review boundary",
            "",
            (
                "`human-review.json` and `human-review.jsonl` contain one row per question "
                "with the model answer, program-restored evidence, Gold answer points, "
                "and Gold evidence units. The owner must fill `review` fields."
            ),
            (
                "`citation_provenance_verified` only means that the cited ID, quote, and "
                "timestamps came from this question's Top-5. It is not semantic correctness "
                "or evidence support."
            ),
            "",
            "## Decision boundary",
            "",
            f"Current recommendation: `{metrics['recommendation']}`.",
            "P0-B is not declared PASSED before owner semantic review. No Dense, Hybrid, "
            "Reranker, OCR, VLM, Agent, Web/API, database, or P1 work is authorized by "
            "this report.",
            "",
        ]
    )
    _write_json(report_path.with_suffix(".json"), metrics)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = report_path.with_name(f"{report_path.name}.partial")
    temporary_path.write_text("\n".join(lines), encoding="utf-8")
    temporary_path.replace(report_path)
