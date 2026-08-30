"""Frozen V1-A measurement manifests and deterministic evaluation artifacts.

The evaluator deliberately keeps semantic quality judgement human-owned.  It
calculates source/accounting/render invariants, writes one rubric template per
declared run, and reports pending human fields instead of inventing scores.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urlsplit

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from .planning import (
    CALL_SCHEMA_VERSION,
    COMPILER_VERSION,
    MAPPER_PROMPT_VERSION,
    MAPPER_SYSTEM_INSTRUCTION,
    PLAN_PROPOSAL_SCHEMA_VERSION,
    PLANNER_PROMPT_VERSION,
    PLANNER_SYSTEM_INSTRUCTION,
    REVIEW_CARD_SCHEMA_VERSION,
    TOPIC_MAP_SCHEMA_VERSION,
    TOPIC_PROPOSAL_SCHEMA_VERSION,
    PlanningError,
    ReviewCard,
    TopicMap,
    stable_json,
)
from .planning_runtime import SourceSnapshot, load_source

MEASUREMENT_SCHEMA_VERSION = "visual-report-measurement-freeze.v1a-prototype"
EVALUATION_SCHEMA_VERSION = "visual-report-evaluation.v1a-prototype"
RUN_EVALUATION_SCHEMA_VERSION = "visual-report-run-evaluation.v1a-prototype"
RUBRIC_SCHEMA_VERSION = "visual-report-human-rubric.v1a-prototype"
EVALUATOR_VERSION = "visual-report-v1a-evaluator.v1"

FIXED_SOURCES: tuple[tuple[str, str, str], ...] = (
    (
        "p0b-kling-2024",
        "artifacts/p0b-ingest/p0b-kling-2024/manifest.json",
        "artifacts/p0b-ingest/p0b-kling-2024/segments.jsonl",
    ),
    (
        "p0b-rlinf-2026",
        "artifacts/p0b-ingest/p0b-rlinf-2026/manifest.json",
        "artifacts/p0b-ingest/p0b-rlinf-2026/segments.jsonl",
    ),
    (
        "p0b-wuyi-goals",
        "artifacts/p0b-ingest/p0b-wuyi-goals/manifest.json",
        "artifacts/p0b-ingest/p0b-wuyi-goals/segments.jsonl",
    ),
)

QUALITY_THRESHOLDS: dict[str, object] = {
    "must_cover_recall_min": 0.90,
    "major_unsupported_claims_max": 0,
    "source_ref_validity": 1.0,
    "first_pass_success_runs": 6,
    "human_average_min": 4.0,
    "human_repeat_min": 3,
    "repeat_category_delta_max": 1,
    "anti_template_all_identical": False,
}


class EvaluationError(PlanningError):
    """A stable evaluator/freeze failure."""


class StrictEvaluationModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class RunDeclaration(StrictEvaluationModel):
    run_id: str = Field(min_length=1, max_length=80)
    video_id: str = Field(min_length=1, max_length=100)
    repeat: Literal[1, 2]
    planned_provider_calls: Literal[2] = 2
    planned_model_calls: Literal[2] = 2


class MeasurementFreeze(StrictEvaluationModel):
    schema_version: Literal[MEASUREMENT_SCHEMA_VERSION]
    revision_id: str = Field(min_length=1, max_length=80)
    status: Literal["FROZEN", "FROZEN_PROVIDER_BLOCKED"]
    frozen_at: str = Field(min_length=1)
    repository_root: str = Field(min_length=1)
    artifact_root: str = Field(min_length=1)
    sources: tuple[dict[str, object], ...] = Field(min_length=3, max_length=3)
    provider: dict[str, object]
    prompts: dict[str, object]
    schemas: dict[str, object]
    review_cards: tuple[dict[str, object], ...] = Field(min_length=3, max_length=3)
    evaluator: dict[str, object]
    thresholds: dict[str, object]
    runs: tuple[RunDeclaration, ...] = Field(min_length=6, max_length=6)

    @model_validator(mode="after")
    def validate_denominator(self) -> "MeasurementFreeze":
        ids = [run.run_id for run in self.runs]
        if len(ids) != len(set(ids)):
            raise ValueError("measurement run IDs must be unique")
        pairs = {(run.video_id, run.repeat) for run in self.runs}
        expected = {(video_id, repeat) for video_id, _, _ in FIXED_SOURCES for repeat in (1, 2)}
        if pairs != expected:
            raise ValueError("measurement must declare exactly two repeats for each fixed video")
        if len(self.review_cards) != 3:
            raise ValueError("measurement must freeze three review cards")
        return self


class HumanScores(StrictEvaluationModel):
    coverage: int | None = Field(default=None, ge=1, le=5)
    grounding: int | None = Field(default=None, ge=1, le=5)
    prioritization: int | None = Field(default=None, ge=1, le=5)
    narrative: int | None = Field(default=None, ge=1, le=5)
    block_appropriateness: int | None = Field(default=None, ge=1, le=5)
    redundancy: int | None = Field(default=None, ge=1, le=5)

    @property
    def complete(self) -> bool:
        return all(
            value is not None
            for value in (
                self.coverage,
                self.grounding,
                self.prioritization,
                self.narrative,
                self.block_appropriateness,
                self.redundancy,
            )
        )


class HumanRubric(StrictEvaluationModel):
    schema_version: Literal[RUBRIC_SCHEMA_VERSION]
    revision_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    video_id: str = Field(min_length=1)
    reviewer: str = Field(min_length=1)
    status: Literal["PENDING_OWNER_REVIEW", "SCORED"]
    scores: HumanScores
    major_unsupported_claims: tuple[str, ...] = ()
    source_notes: tuple[str, ...] = ()

    @model_validator(mode="after")
    def validate_status(self) -> "HumanRubric":
        if self.status == "SCORED" and not self.scores.complete:
            raise ValueError("SCORED rubric requires all six category scores")
        return self


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _read_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise EvaluationError("EVALUATION_INPUT_NOT_FOUND", f"file not found: {path}") from exc
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvaluationError("EVALUATION_INPUT_ERROR", f"cannot read JSON: {path}") from exc


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    try:
        rows = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    except (FileNotFoundError, OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvaluationError("EVALUATION_INPUT_ERROR", f"cannot read JSONL: {path}") from exc
    if not all(isinstance(row, dict) for row in rows):
        raise EvaluationError("EVALUATION_INPUT_ERROR", f"JSONL rows must be objects: {path}")
    return rows  # type: ignore[return-value]


def _write_new_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    except FileExistsError as exc:
        raise EvaluationError("EVALUATION_OUTPUT_EXISTS", f"output already exists: {path}") from exc
    except OSError as exc:
        raise EvaluationError("EVALUATION_OUTPUT_ERROR", f"cannot write output: {path}") from exc


def _sanitized_provider_label(base_url: str) -> str:
    if not base_url:
        return "openai"
    parsed = urlsplit(base_url)
    if parsed.scheme and parsed.hostname:
        port = f":{parsed.port}" if parsed.port else ""
        return f"{parsed.scheme}://{parsed.hostname}{port}"
    return "openai-compatible-custom-endpoint"


def environment_snapshot(repository_root: Path) -> dict[str, object]:
    """Return only non-secret provider admission facts."""
    load_dotenv(repository_root / ".env", override=False)
    api_key_present = bool(os.getenv("OPENAI_API_KEY", "").strip())
    model = os.getenv("VISUAL_REPORT_MODEL", "").strip()
    base_url = os.getenv("OPENAI_BASE_URL", "").strip()
    timeout_raw = os.getenv("VISUAL_REPORT_TIMEOUT_SECONDS", "120").strip()
    try:
        timeout_seconds = float(timeout_raw)
    except ValueError:
        timeout_seconds = None
    blockers: list[str] = []
    if not api_key_present:
        blockers.append("OPENAI_API_KEY is not present")
    if not model:
        blockers.append("VISUAL_REPORT_MODEL is not configured")
    if timeout_seconds is None:
        blockers.append("VISUAL_REPORT_TIMEOUT_SECONDS is not numeric")
    elif timeout_seconds <= 0:
        blockers.append("VISUAL_REPORT_TIMEOUT_SECONDS must be positive")
    try:
        sdk_version = importlib.metadata.version("openai")
    except importlib.metadata.PackageNotFoundError:
        sdk_version = "unavailable"
    return {
        "admission": "READY" if not blockers else "BLOCKED_CONFIGURATION",
        "blockers": blockers,
        "provider": _sanitized_provider_label(base_url),
        "model": model or "unavailable",
        "credential_present": api_key_present,
        "timeout_seconds": timeout_seconds if timeout_seconds is not None else "invalid",
        "response_mode": "json_object",
        "temperature": 0,
        "sdk_max_retries": 0,
        "sdk_version": sdk_version,
    }


def _card_paths(card_root: Path) -> dict[str, Path]:
    return {
        video_id: card_root / f"{video_id}.v1.json" for video_id, _, _ in FIXED_SOURCES
    }


def _card_payload(path: Path) -> ReviewCard:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise EvaluationError("REVIEW_CARD_SCHEMA_ERROR", f"card must be an object: {path}")
    try:
        return ReviewCard.model_validate(payload)
    except ValidationError as exc:
        raise EvaluationError("REVIEW_CARD_SCHEMA_ERROR", str(exc)) from exc


def validate_review_card(card: ReviewCard, source: SourceSnapshot) -> None:
    if card.video_id != source.video_id:
        raise EvaluationError("REVIEW_CARD_SOURCE_MISMATCH", "review card video_id differs")
    valid_ids = {segment.segment_id for segment in source.segments}
    for concept in (*card.must_cover, *card.optional, *card.known_asr_traps):
        if set(concept.source_segment_ids) - valid_ids:
            raise EvaluationError(
                "REVIEW_CARD_SOURCE_MISMATCH",
                f"review card references unknown segment for {concept.label}",
            )
    for claim in card.prohibited_overclaims:
        if set(claim.source_segment_ids) - valid_ids:
            raise EvaluationError(
                "REVIEW_CARD_SOURCE_MISMATCH",
                f"review card overclaim references unknown segment for {claim.claim}",
            )


def _stable_revision_payload(
    *,
    repository_root: Path,
    artifact_root: Path,
    sources: list[dict[str, object]],
    provider: dict[str, object],
    cards: list[dict[str, object]],
    evaluator_sha256: str,
    runs: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "schema_version": MEASUREMENT_SCHEMA_VERSION,
        "repository_root": str(repository_root.resolve()),
        "artifact_root": str(artifact_root.resolve()),
        "sources": sources,
        "provider": provider,
        "prompts": {
            "mapper_version": MAPPER_PROMPT_VERSION,
            "mapper_sha256": _sha256_bytes(MAPPER_SYSTEM_INSTRUCTION.encode("utf-8")),
            "planner_version": PLANNER_PROMPT_VERSION,
            "planner_sha256": _sha256_bytes(PLANNER_SYSTEM_INSTRUCTION.encode("utf-8")),
        },
        "schemas": {
            "topic_proposal": TOPIC_PROPOSAL_SCHEMA_VERSION,
            "topic_map": TOPIC_MAP_SCHEMA_VERSION,
            "plan_proposal": PLAN_PROPOSAL_SCHEMA_VERSION,
            "call": CALL_SCHEMA_VERSION,
            "compiler": COMPILER_VERSION,
        },
        "review_cards": cards,
        "evaluator": {
            "version": EVALUATOR_VERSION,
            "module": str(Path(__file__).resolve()),
            "sha256": evaluator_sha256,
        },
        "thresholds": QUALITY_THRESHOLDS,
        "runs": runs,
    }


def freeze_measurement(
    *,
    repository_root: Path,
    artifact_root: Path,
    card_root: Path,
    output_path: Path,
) -> MeasurementFreeze:
    """Validate and write one immutable six-run measurement declaration."""
    repository_root = repository_root.resolve()
    artifact_root = artifact_root.resolve()
    card_root = card_root.resolve()
    source_rows: list[dict[str, object]] = []
    for video_id, manifest_rel, segments_rel in FIXED_SOURCES:
        manifest_path = repository_root / manifest_rel
        segments_path = repository_root / segments_rel
        source = load_source(manifest_path, segments_path)
        if source.video_id != video_id:
            raise EvaluationError(
                "SOURCE_SNAPSHOT_MISMATCH", f"unexpected source video_id: {video_id}"
            )
        source_rows.append(
            {
                "video_id": video_id,
                "manifest_path": str(manifest_path),
                "segments_path": str(segments_path),
                "manifest_sha256": source.manifest_sha256,
                "segments_sha256": source.segments_sha256,
                "segment_count": len(source.segments),
                "duration_ms": source.duration_ms,
            }
        )

    cards: list[dict[str, object]] = []
    for video_id, _, _ in FIXED_SOURCES:
        path = _card_paths(card_root)[video_id]
        card = _card_payload(path)
        source_row = next(row for row in source_rows if row["video_id"] == video_id)
        source = load_source(
            Path(str(source_row["manifest_path"])), Path(str(source_row["segments_path"]))
        )
        validate_review_card(card, source)
        cards.append(
            {
                "video_id": video_id,
                "path": str(path),
                "sha256": _sha256_file(path),
                "schema_version": REVIEW_CARD_SCHEMA_VERSION,
            }
        )

    provider = environment_snapshot(repository_root)
    evaluator_sha256 = _sha256_file(Path(__file__).resolve())
    seed_payload = _stable_revision_payload(
        repository_root=repository_root,
        artifact_root=artifact_root,
        sources=source_rows,
        provider=provider,
        cards=cards,
        evaluator_sha256=evaluator_sha256,
        runs=[],
    )
    revision_seed = _sha256_bytes(stable_json(seed_payload).encode("utf-8"))[:10]
    runs = [
        {
            "run_id": f"{video_id}-v1a-{revision_seed}-r{repeat}",
            "video_id": video_id,
            "repeat": repeat,
            "planned_provider_calls": 2,
            "planned_model_calls": 2,
        }
        for video_id, _, _ in FIXED_SOURCES
        for repeat in (1, 2)
    ]
    stable_payload = _stable_revision_payload(
        repository_root=repository_root,
        artifact_root=artifact_root,
        sources=source_rows,
        provider=provider,
        cards=cards,
        evaluator_sha256=evaluator_sha256,
        runs=runs,
    )
    revision_id = f"vr1a-dev-{_sha256_bytes(stable_json(stable_payload).encode('utf-8'))[:12]}"
    payload = {
        **stable_payload,
        "revision_id": revision_id,
        "status": "FROZEN" if provider["admission"] == "READY" else "FROZEN_PROVIDER_BLOCKED",
        "frozen_at": _now(),
    }
    _write_new_json(output_path, payload)
    try:
        return MeasurementFreeze.model_validate(payload)
    except ValidationError as exc:
        raise EvaluationError("MEASUREMENT_SCHEMA_ERROR", str(exc)) from exc


def load_measurement(path: Path) -> MeasurementFreeze:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise EvaluationError("MEASUREMENT_SCHEMA_ERROR", "measurement manifest must be an object")
    try:
        return MeasurementFreeze.model_validate(payload)
    except ValidationError as exc:
        raise EvaluationError("MEASUREMENT_SCHEMA_ERROR", str(exc)) from exc


def _segment_map(source: SourceSnapshot) -> dict[str, Any]:
    return {segment.segment_id: segment for segment in source.segments}


def _valid_source_ref(ref: object, segments: dict[str, Any]) -> bool:
    segment_id = getattr(ref, "segment_id", None)
    segment = segments.get(segment_id)
    return bool(
        segment is not None
        and getattr(ref, "start_ms", None) == segment.start_ms
        and getattr(ref, "end_ms", None) == segment.end_ms
    )


def _read_run_json(run_dir: Path) -> dict[str, object] | None:
    path = run_dir / "run.json"
    if not path.is_file():
        return None
    payload = _read_json(path)
    return payload if isinstance(payload, dict) else None


def _structure_signature(plan: Any) -> str:
    shape = {
        "sections": [
            {
                "block_count": len(section.blocks),
                "types": [block.type for block in section.blocks],
            }
            for section in plan.sections
        ]
    }
    return _sha256_bytes(stable_json(shape).encode("utf-8"))[:16]


def _card_recall(card: ReviewCard, source_ids: set[str]) -> dict[str, object]:
    items: list[dict[str, object]] = []
    for concept in card.must_cover:
        expected = set(concept.source_segment_ids)
        retained = expected & source_ids
        items.append(
            {
                "label": concept.label,
                "expected_source_count": len(expected),
                "retained_source_count": len(retained),
                "retained": bool(retained),
                "source_reference_recall": len(retained) / len(expected),
            }
        )
    retained_count = sum(bool(item["retained"]) for item in items)
    return {
        "concept_count": len(items),
        "retained_concept_count": retained_count,
        "concept_recall_proxy": retained_count / len(items) if items else 0.0,
        "items": items,
    }


def _rubric_template(declaration: RunDeclaration, revision_id: str) -> HumanRubric:
    return HumanRubric(
        schema_version=RUBRIC_SCHEMA_VERSION,
        revision_id=revision_id,
        run_id=declaration.run_id,
        video_id=declaration.video_id,
        reviewer="owner-or-designated-human",
        status="PENDING_OWNER_REVIEW",
        scores=HumanScores(),
        major_unsupported_claims=(),
        source_notes=(),
    )


def _load_or_create_rubric(
    declaration: RunDeclaration, revision_id: str, rubric_path: Path
) -> HumanRubric:
    if rubric_path.exists():
        payload = _read_json(rubric_path)
        try:
            rubric = HumanRubric.model_validate(payload)
        except ValidationError as exc:
            raise EvaluationError("RUBRIC_SCHEMA_ERROR", str(exc)) from exc
        if rubric.revision_id != revision_id or rubric.run_id != declaration.run_id:
            raise EvaluationError("RUBRIC_REVISION_MISMATCH", f"stale rubric: {rubric_path}")
        return rubric
    rubric = _rubric_template(declaration, revision_id)
    _write_new_json(rubric_path, rubric.model_dump(mode="json"))
    return rubric


def _score_run(
    declaration: RunDeclaration,
    freeze: MeasurementFreeze,
    source: SourceSnapshot,
    card: ReviewCard,
    run_dir: Path,
    rubric_path: Path,
) -> dict[str, object]:
    row: dict[str, object] = {
        "run_id": declaration.run_id,
        "video_id": declaration.video_id,
        "repeat": declaration.repeat,
        "run_dir": str(run_dir),
        "state": "MISSING",
        "provider_calls": 0,
        "model_calls": 0,
        "deterministic": {
            "execution_valid": False,
            "revision_snapshot_match": False,
            "first_pass_schema_compile_render": False,
            "segment_accounting_valid": False,
            "topic_map_source_refs_valid": False,
            "report_source_refs_valid": False,
            "assets_empty": False,
            "must_cover_reference_recall": None,
            "structure_signature": None,
            "errors": ["run.json is missing"],
        },
        "human_rubric_path": str(rubric_path),
    }
    run_payload = _read_run_json(run_dir)
    if run_payload is None:
        rubric = _load_or_create_rubric(declaration, freeze.revision_id, rubric_path)
        row["human_rubric"] = rubric.model_dump(mode="json")
        return row
    row["state"] = run_payload.get("state", "UNKNOWN")
    row["provider_calls"] = run_payload.get("provider_calls", 0)
    row["model_calls"] = run_payload.get("model_calls", 0)
    row["usage"] = run_payload.get("usage", {})
    row["latency_ms_total"] = run_payload.get("latency_ms_total", 0)
    row["cost"] = run_payload.get("cost", "unavailable")
    errors: list[str] = []
    deterministic = row["deterministic"]
    assert isinstance(deterministic, dict)

    source_snapshot = run_payload.get("source")
    source_row = next(
        (item for item in freeze.sources if item.get("video_id") == declaration.video_id),
        {},
    )
    config_snapshot = run_payload.get("config")
    expected_config = freeze.provider
    snapshot_match = (
        run_payload.get("run_id") == declaration.run_id
        and isinstance(source_snapshot, dict)
        and source_snapshot.get("video_id") == source_row.get("video_id")
        and source_snapshot.get("manifest_sha256") == source_row.get("manifest_sha256")
        and source_snapshot.get("segments_sha256") == source_row.get("segments_sha256")
        and isinstance(config_snapshot, dict)
        and all(config_snapshot.get(key) == expected_config.get(key) for key in (
            "provider",
            "model",
            "timeout_seconds",
            "credential_present",
            "response_mode",
            "temperature",
            "sdk_max_retries",
            "sdk_version",
        ))
    )
    deterministic["revision_snapshot_match"] = snapshot_match
    if not snapshot_match:
        errors.append("run source/config snapshot does not match frozen measurement")

    calls_path = run_dir / "model-calls.jsonl"
    calls = _read_jsonl(calls_path) if calls_path.is_file() else []
    call_valid = (
        len(calls) == 2
        and [call.get("stage") for call in calls] == ["topic_mapper", "report_planner"]
        and all(
            call.get("schema_version") == CALL_SCHEMA_VERSION
            and call.get("schema_valid") is True
            and call.get("error_category") is None
            for call in calls
        )
    )
    deterministic["first_pass_schema_compile_render"] = bool(
        run_payload.get("state") == "RENDERED"
        and run_payload.get("provider_calls") == 2
        and run_payload.get("model_calls") == 2
        and call_valid
        and (run_dir / "report.html").is_file()
        and snapshot_match
    )
    if not call_valid:
        errors.append("model call trace is not two successful first-pass calls")

    segments = _segment_map(source)
    topic_map: TopicMap | None = None
    topic_path = run_dir / "topic-map.json"
    if topic_path.is_file():
        try:
            topic_map = TopicMap.model_validate(_read_json(topic_path))
        except ValidationError as exc:
            errors.append(f"topic map schema error: {exc.errors()[0].get('msg', 'invalid')}")
    if topic_map is not None:
        map_refs = [ref for topic in topic_map.topics for ref in topic.source_refs]
        map_refs.extend(exclusion.source_ref for exclusion in topic_map.exclusions)
        map_valid = all(_valid_source_ref(ref, segments) for ref in map_refs)
        assigned = [ref.segment_id for ref in map_refs]
        accounting = (
            topic_map.video_id == source.video_id
            and topic_map.coverage.input_segment_count == len(source.segments)
            and topic_map.coverage.mapped_count + topic_map.coverage.excluded_count
            == len(source.segments)
            and len(assigned) == len(set(assigned)) == len(source.segments)
        )
        deterministic["topic_map_source_refs_valid"] = map_valid
        deterministic["segment_accounting_valid"] = accounting
        deterministic["must_cover_reference_recall"] = _card_recall(card, set(assigned))
        if not map_valid:
            errors.append("topic map contains invalid source refs")
        if not accounting:
            errors.append("topic map segment accounting is invalid")
    else:
        errors.append("topic map artifact is missing or invalid")

    plan_path = run_dir / "report-plan.json"
    assets_path = run_dir / "assets.json"
    plan: Any | None = None
    if plan_path.is_file() and topic_map is not None:
        try:
            from .models import AssetManifest, ReportPlan

            plan = ReportPlan.model_validate(_read_json(plan_path))
            assets = AssetManifest.model_validate(_read_json(assets_path))
            deterministic["assets_empty"] = len(assets.assets) == 0
        except (ValidationError, EvaluationError) as exc:
            errors.append(f"report artifact schema error: {exc}")
    else:
        errors.append("report plan or topic map artifact is missing")
    if plan is not None:
        report_refs = [
            ref
            for section in plan.sections
            for block in section.blocks
            for ref in block.source_refs
        ]
        refs_valid = all(_valid_source_ref(ref, segments) for ref in report_refs)
        deterministic["report_source_refs_valid"] = refs_valid
        deterministic["structure_signature"] = _structure_signature(plan)
        if not refs_valid:
            errors.append("report plan contains invalid source refs")
        if not bool(deterministic["assets_empty"]):
            errors.append("assets manifest is not empty")
    deterministic["errors"] = errors
    deterministic["execution_valid"] = bool(
        deterministic["first_pass_schema_compile_render"]
        and deterministic["segment_accounting_valid"]
        and deterministic["topic_map_source_refs_valid"]
        and deterministic["report_source_refs_valid"]
        and deterministic["assets_empty"]
    )
    rubric = _load_or_create_rubric(declaration, freeze.revision_id, rubric_path)
    row["human_rubric"] = rubric.model_dump(mode="json")
    return row


def _human_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    categories = (
        "coverage",
        "grounding",
        "prioritization",
        "narrative",
        "block_appropriateness",
        "redundancy",
    )
    by_video: dict[str, dict[str, object]] = {}
    pending = False
    for video_id in sorted({str(row["video_id"]) for row in rows}):
        video_rows = [row for row in rows if row["video_id"] == video_id]
        category_summary: dict[str, object] = {}
        for category in categories:
            values = [
                row.get("human_rubric", {}).get("scores", {}).get(category)
                for row in video_rows
                if isinstance(row.get("human_rubric"), dict)
            ]
            values = [value for value in values if isinstance(value, int)]
            category_summary[category] = {
                "scores": values,
                "average": sum(values) / len(values) if values else None,
                "min": min(values) if values else None,
            }
            if len(values) < 2:
                pending = True
        by_video[video_id] = category_summary
    return {"status": "PENDING_OWNER_REVIEW" if pending else "SCORED", "by_video": by_video}


def evaluate_measurement(
    *, measurement_path: Path, output_root: Path
) -> dict[str, object]:
    """Evaluate all six declared identities without rescore or repair."""
    freeze = load_measurement(measurement_path)
    repository_root = Path(freeze.repository_root)
    artifact_root = Path(freeze.artifact_root)
    source_by_video: dict[str, SourceSnapshot] = {}
    card_by_video: dict[str, ReviewCard] = {}
    for source_row in freeze.sources:
        source = load_source(
            Path(str(source_row["manifest_path"])), Path(str(source_row["segments_path"]))
        )
        if (
            source.manifest_sha256 != source_row.get("manifest_sha256")
            or source.segments_sha256 != source_row.get("segments_sha256")
            or len(source.segments) != source_row.get("segment_count")
            or source.duration_ms != source_row.get("duration_ms")
        ):
            raise EvaluationError(
                "MEASUREMENT_STALE", f"source snapshot changed: {source.video_id}"
            )
        source_by_video[source.video_id] = source
    evaluator_row = freeze.evaluator
    evaluator_path = Path(str(evaluator_row.get("module", "")))
    if not evaluator_path.is_file() or _sha256_file(evaluator_path) != evaluator_row.get("sha256"):
        raise EvaluationError("MEASUREMENT_STALE", "evaluator source changed after freeze")
    for card_row in freeze.review_cards:
        card = _card_payload(Path(str(card_row["path"])))
        source = source_by_video.get(card.video_id)
        if source is None:
            raise EvaluationError(
                "REVIEW_CARD_SOURCE_MISMATCH", f"unknown card video: {card.video_id}"
            )
        validate_review_card(card, source)
        if _sha256_file(Path(str(card_row["path"]))) != card_row["sha256"]:
            raise EvaluationError("MEASUREMENT_STALE", f"review card changed: {card.video_id}")
        card_by_video[card.video_id] = card

    revision_root = output_root.resolve() / freeze.revision_id
    try:
        revision_root.mkdir(parents=True, exist_ok=False)
    except FileExistsError as exc:
        raise EvaluationError(
            "EVALUATION_OUTPUT_EXISTS", f"evaluation already exists: {revision_root}"
        ) from exc
    run_rows: list[dict[str, object]] = []
    for declaration in freeze.runs:
        source = source_by_video[declaration.video_id]
        card = card_by_video[declaration.video_id]
        rubric_path = revision_root / "rubrics" / f"{declaration.run_id}.json"
        run_rows.append(
            _score_run(
                declaration,
                freeze,
                source,
                card,
                artifact_root / declaration.run_id,
                rubric_path,
            )
        )
    for row in run_rows:
        _write_new_json(revision_root / "runs" / f"{row['run_id']}.json", row)

    successful = [row for row in run_rows if row["deterministic"]["execution_valid"]]
    calls = sum(int(row.get("provider_calls", 0)) for row in run_rows)
    model_calls = sum(int(row.get("model_calls", 0)) for row in run_rows)
    latency = sum(int(row.get("latency_ms_total", 0)) for row in run_rows)
    usage: Counter[str] = Counter()
    for row in run_rows:
        candidate = row.get("usage", {})
        if isinstance(candidate, dict):
            for key, value in candidate.items():
                if isinstance(value, int):
                    usage[key] += value
    signatures = {
        str(row["run_id"]): row["deterministic"]["structure_signature"]
        for row in run_rows
        if row["deterministic"]["structure_signature"] is not None
    }
    by_video: dict[str, dict[str, object]] = {}
    for video_id in source_by_video:
        video_rows = [row for row in run_rows if row["video_id"] == video_id]
        by_video[video_id] = {
            "run_ids": [row["run_id"] for row in video_rows],
            "execution_valid_count": sum(
                bool(row["deterministic"]["execution_valid"]) for row in video_rows
            ),
            "first_pass_success_count": sum(
                bool(row["deterministic"]["first_pass_schema_compile_render"])
                for row in video_rows
            ),
            "structure_signatures": [
                row["deterministic"]["structure_signature"] for row in video_rows
            ],
        }
    human = _human_summary(run_rows)
    provider = freeze.provider
    measurement_valid = bool(
        provider.get("admission") == "READY"
        and len(run_rows) == 6
        and len(successful) == 6
        and calls == 12
        and model_calls == 12
    )
    if provider.get("admission") != "READY":
        conclusion = "BLOCKED_PROVIDER_CONFIGURATION"
    elif not measurement_valid:
        conclusion = "MEASUREMENT_EXECUTION_FAILED"
    elif human["status"] != "SCORED":
        conclusion = "PENDING_OWNER_REVIEW"
    else:
        conclusion = "QUALITY_REVIEW_RECORDED_OWNER_DECISION_REQUIRED"
    aggregate = {
        "schema_version": EVALUATION_SCHEMA_VERSION,
        "evaluator_version": EVALUATOR_VERSION,
        "revision_id": freeze.revision_id,
        "measurement_valid": measurement_valid,
        "quality_status": human["status"],
        "conclusion": conclusion,
        "denominator": {
            "declared_runs": len(freeze.runs),
            "declared_provider_calls": sum(run.planned_provider_calls for run in freeze.runs),
            "declared_model_calls": sum(run.planned_model_calls for run in freeze.runs),
            "observed_provider_calls": calls,
            "observed_model_calls": model_calls,
        },
        "provider": provider,
        "usage": dict(usage),
        "latency_ms_total": latency,
        "cost": "unavailable",
        "thresholds": freeze.thresholds,
        "runs": run_rows,
        "by_video": by_video,
        "structure_signatures": signatures,
        "all_successful_signatures_identical": (
            len(set(signatures.values())) == 1 if signatures else None
        ),
        "human_rubric": human,
        "owner_action": (
            "Review each retained run and complete the six human rubric files; "
            "do not treat this artifact as OWNER_ACCEPTED."
        ),
        "generated_at": _now(),
        "source_revision": str(measurement_path.resolve()),
        "repository_root": str(repository_root.resolve()),
    }
    _write_new_json(revision_root / "aggregate.json", aggregate)
    return aggregate


__all__ = [
    "EVALUATOR_VERSION",
    "EVALUATION_SCHEMA_VERSION",
    "FIXED_SOURCES",
    "HumanRubric",
    "MeasurementFreeze",
    "evaluate_measurement",
    "environment_snapshot",
    "freeze_measurement",
    "load_measurement",
    "validate_review_card",
]
