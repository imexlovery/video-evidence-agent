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

from .models import AssetManifest, ReportPlan
from .planning import (
    CALL_SCHEMA_VERSION,
    COMPILER_VERSION,
    MAPPER_PROMPT_VERSION,
    MAPPER_SYSTEM_INSTRUCTION,
    MAX_OUTPUT_TOKENS,
    PLAN_PROPOSAL_SCHEMA_VERSION,
    PLANNER_PROMPT_VERSION,
    PLANNER_SYSTEM_INSTRUCTION,
    REVIEW_CARD_SCHEMA_VERSION,
    SEMANTIC_V2_CALL_SCHEMA_VERSION,
    SEMANTIC_V2_COMPILER_VERSION,
    SEMANTIC_V2_MAPPER_PROMPT_VERSION,
    SEMANTIC_V2_MAPPER_SYSTEM_INSTRUCTION,
    SEMANTIC_V2_NORMALIZATION_SCHEMA_VERSION,
    SEMANTIC_V2_PLAN_PROPOSAL_SCHEMA_VERSION,
    SEMANTIC_V2_PLANNER_PROMPT_VERSION,
    SEMANTIC_V2_PLANNER_SYSTEM_INSTRUCTION,
    SEMANTIC_V2_TOPIC_MAP_SCHEMA_VERSION,
    SEMANTIC_V2_TOPIC_PROPOSAL_SCHEMA_VERSION,
    THINKING_MODE,
    TOPIC_MAP_SCHEMA_VERSION,
    TOPIC_PROPOSAL_SCHEMA_VERSION,
    PlanningError,
    ReportPlanProposal,
    ReviewCard,
    SemanticV2ReportPlanProposal,
    SemanticV2TopicMap,
    SemanticV2TopicMapProposal,
    TopicMap,
    TopicMapProposal,
    stable_json,
)
from .planning_runtime import (
    API_SURFACE,
    REASONING_EFFORT,
    RESPONSE_MODE,
    SCHEMA_MECHANISM,
    SEMANTIC_V2_API_SURFACE,
    SEMANTIC_V2_RESPONSE_MODE,
    SEMANTIC_V2_SCHEMA_MECHANISM,
    SourceSnapshot,
    load_source,
)

MEASUREMENT_SCHEMA_VERSION = "visual-report-measurement-freeze.v1a-prototype"
EVALUATION_SCHEMA_VERSION = "visual-report-evaluation.v1a-prototype"
RUN_EVALUATION_SCHEMA_VERSION = "visual-report-run-evaluation.v1a-prototype"
RUBRIC_SCHEMA_VERSION = "visual-report-human-rubric.v1a-prototype"
EVALUATOR_VERSION = "visual-report-v1a-evaluator.v1"
PROVIDER_CONFORMANCE_SCHEMA_VERSION = "visual-report-provider-conformance.v1a"
PROVIDER_CONFORMANCE_RESULT_SCHEMA_VERSION = "visual-report-provider-conformance-result.v1a"
PROVIDER_CONFORMANCE_ADAPTER_ID = "openai.responses.text.json_schema.v1a"
SEMANTIC_V2_PRODUCT_MANIFEST_SCHEMA_VERSION = (
    "visual-report-semantic-v2-product-manifest.v1a"
)
SEMANTIC_V2_PRODUCT_EVALUATION_SCHEMA_VERSION = (
    "visual-report-semantic-v2-product-evaluation.v1a"
)
SEMANTIC_V2_PRODUCT_RUBRIC_SCHEMA_VERSION = "visual-report-semantic-v2-product-rubric.v1a"
SEMANTIC_V2_PRODUCT_PACKAGE_SCHEMA_VERSION = "visual-report-semantic-v2-review-package.v1a"
SEMANTIC_V2_PRODUCT_EVALUATOR_VERSION = "visual-report-semantic-v2-product-evaluator.v1"
DEEPSEEK_RESPONSES_DOC = "https://api-docs.deepseek.com/api/create-response/"
DEEPSEEK_MODELS_DOC = (
    "https://api-docs.deepseek.com/quick_start/pricing/?article_id=article_1779470751466_8"
)
SUPPORTED_DEEPSEEK_MODELS: tuple[str, ...] = (
    "deepseek-v4-flash-vision-exp",
    "deepseek-v4-flash",
)

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


class ProductRunDeclaration(StrictEvaluationModel):
    run_id: str = Field(min_length=1, max_length=80)
    video_id: str = Field(min_length=1, max_length=100)
    planned_provider_calls: Literal[2] = 2
    maximum_provider_calls: Literal[3] = 3


class SemanticV2ProductFreeze(StrictEvaluationModel):
    schema_version: Literal[SEMANTIC_V2_PRODUCT_MANIFEST_SCHEMA_VERSION]
    revision_id: str = Field(min_length=1, max_length=100)
    status: Literal["FROZEN", "FROZEN_PROVIDER_BLOCKED"]
    frozen_at: str = Field(min_length=1)
    repository_root: str = Field(min_length=1)
    source_root: str = Field(min_length=1)
    artifact_root: str = Field(min_length=1)
    sources: tuple[dict[str, object], ...] = Field(min_length=3, max_length=3)
    provider: dict[str, object]
    contract: dict[str, object]
    prompts: dict[str, object]
    schemas: dict[str, object]
    review_cards: tuple[dict[str, object], ...] = Field(min_length=3, max_length=3)
    evaluator: dict[str, object]
    runtime: dict[str, object]
    limits: dict[str, object]
    runs: tuple[ProductRunDeclaration, ...] = Field(min_length=3, max_length=3)
    derived_from_manifest: str | None = None
    derived_at: str | None = None
    derivation_reason: str | None = None

    @model_validator(mode="after")
    def validate_product_set(self) -> "SemanticV2ProductFreeze":
        expected = {video_id for video_id, _, _ in FIXED_SOURCES}
        actual = {run.video_id for run in self.runs}
        if actual != expected:
            raise ValueError("semantic-v2 product freeze must contain the three fixed videos")
        ids = [run.run_id for run in self.runs]
        if len(ids) != len(set(ids)):
            raise ValueError("semantic-v2 product run IDs must be unique")
        if len(self.review_cards) != 3:
            raise ValueError("semantic-v2 product freeze must contain three review cards")
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
        "api_surface": API_SURFACE,
        "response_mode": RESPONSE_MODE,
        "schema_mechanism": SCHEMA_MECHANISM,
        "temperature": 0,
        "thinking_mode": THINKING_MODE,
        "reasoning_effort": REASONING_EFFORT,
        "output_token_limit": MAX_OUTPUT_TOKENS,
        "sdk_max_retries": 0,
        "sdk_version": sdk_version,
    }


def _card_paths(card_root: Path) -> dict[str, Path]:
    return {video_id: card_root / f"{video_id}.v1.json" for video_id, _, _ in FIXED_SOURCES}


def _card_payload(path: Path) -> ReviewCard:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise EvaluationError("REVIEW_CARD_SCHEMA_ERROR", f"card must be an object: {path}")
    try:
        return ReviewCard.model_validate(payload)
    except ValidationError as exc:
        raise EvaluationError("REVIEW_CARD_SCHEMA_ERROR", str(exc)) from exc


def _fixed_source_rows(repository_root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for video_id, manifest_rel, segments_rel in FIXED_SOURCES:
        manifest_path = repository_root / manifest_rel
        segments_path = repository_root / segments_rel
        source = load_source(manifest_path, segments_path)
        if source.video_id != video_id:
            raise EvaluationError(
                "SOURCE_SNAPSHOT_MISMATCH", f"unexpected source video_id: {video_id}"
            )
        rows.append(
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
    return rows


def _review_card_rows(
    card_root: Path, source_rows: list[dict[str, object]]
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    card_paths = _card_paths(card_root)
    for video_id, _, _ in FIXED_SOURCES:
        path = card_paths[video_id]
        card = _card_payload(path)
        source_row = next(row for row in source_rows if row["video_id"] == video_id)
        source = load_source(
            Path(str(source_row["manifest_path"])), Path(str(source_row["segments_path"]))
        )
        validate_review_card(card, source)
        rows.append(
            {
                "video_id": video_id,
                "path": str(path),
                "sha256": _sha256_file(path),
                "schema_version": REVIEW_CARD_SCHEMA_VERSION,
            }
        )
    return rows


def _schema_fingerprint(
    name: str, schema_version: str, schema: dict[str, object]
) -> dict[str, object]:
    return {
        "name": name,
        "schema_version": schema_version,
        "sha256": _sha256_bytes(stable_json(schema).encode("utf-8")),
    }


def _provider_contract_snapshot() -> dict[str, object]:
    return {
        "prompts": {
            "mapper": {
                "version": MAPPER_PROMPT_VERSION,
                "sha256": _sha256_bytes(MAPPER_SYSTEM_INSTRUCTION.encode("utf-8")),
            },
            "planner": {
                "version": PLANNER_PROMPT_VERSION,
                "sha256": _sha256_bytes(PLANNER_SYSTEM_INSTRUCTION.encode("utf-8")),
            },
        },
        "schemas": {
            "topic_mapper": _schema_fingerprint(
                "v1a_topic_map_proposal",
                TOPIC_PROPOSAL_SCHEMA_VERSION,
                TopicMapProposal.model_json_schema(),
            ),
            "report_planner": _schema_fingerprint(
                "v1a_report_plan_proposal",
                PLAN_PROPOSAL_SCHEMA_VERSION,
                ReportPlanProposal.model_json_schema(),
            ),
        },
        "compiler_version": COMPILER_VERSION,
        "call_schema_version": CALL_SCHEMA_VERSION,
        "adapter_id": PROVIDER_CONFORMANCE_ADAPTER_ID,
    }


def _provider_adapter_snapshot() -> dict[str, object]:
    path = Path(__file__).with_name("planning_runtime.py").resolve()
    return {
        "adapter_id": PROVIDER_CONFORMANCE_ADAPTER_ID,
        "module": str(path),
        "sha256": _sha256_file(path),
        "api_surface": API_SURFACE,
        "schema_mechanism": SCHEMA_MECHANISM,
    }


def _canary_declarations(model_suffix: str) -> list[dict[str, object]]:
    return [
        {
            "run_id": f"{video_id}-v1a-{model_suffix}-canary",
            "video_id": video_id,
            "planned_provider_calls": 2,
            "planned_model_calls": 2,
        }
        for video_id, _, _ in FIXED_SOURCES
    ]


def _validate_provider_conformance_manifest(payload: object) -> dict[str, object]:
    if not isinstance(payload, dict):
        raise EvaluationError(
            "PROVIDER_CONFORMANCE_SCHEMA_ERROR", "conformance manifest must be an object"
        )
    if payload.get("schema_version") != PROVIDER_CONFORMANCE_SCHEMA_VERSION:
        raise EvaluationError(
            "PROVIDER_CONFORMANCE_SCHEMA_ERROR", "unsupported conformance manifest version"
        )
    if payload.get("status") not in {"FROZEN", "EXTERNAL_BLOCKED"}:
        raise EvaluationError("PROVIDER_CONFORMANCE_SCHEMA_ERROR", "invalid conformance status")
    strategies = payload.get("strategies")
    if not isinstance(strategies, list) or not 1 <= len(strategies) <= 2:
        raise EvaluationError(
            "PROVIDER_CONFORMANCE_SCHEMA_ERROR", "one or two strategies must be frozen"
        )
    contract = _provider_contract_snapshot()
    adapter = _provider_adapter_snapshot()
    ids: set[str] = set()
    canary_ids: set[str] = set()
    for index, strategy in enumerate(strategies, start=1):
        if not isinstance(strategy, dict):
            raise EvaluationError("PROVIDER_CONFORMANCE_SCHEMA_ERROR", "strategy must be an object")
        strategy_id = strategy.get("strategy_id")
        if not isinstance(strategy_id, str) or not strategy_id or strategy_id in ids:
            raise EvaluationError(
                "PROVIDER_CONFORMANCE_SCHEMA_ERROR", "strategy IDs must be unique"
            )
        ids.add(strategy_id)
        if strategy.get("order") != index:
            raise EvaluationError("PROVIDER_CONFORMANCE_SCHEMA_ERROR", "strategy order is invalid")
        if strategy.get("api_surface") != API_SURFACE:
            raise EvaluationError(
                "PROVIDER_CONFORMANCE_SCHEMA_ERROR", "strategy is not Responses API"
            )
        if strategy.get("response_mode") != RESPONSE_MODE:
            raise EvaluationError(
                "PROVIDER_CONFORMANCE_SCHEMA_ERROR", "strategy is not native JSON Schema"
            )
        if strategy.get("schema_mechanism") != SCHEMA_MECHANISM:
            raise EvaluationError(
                "PROVIDER_CONFORMANCE_SCHEMA_ERROR", "strategy schema mechanism is invalid"
            )
        if strategy.get("adapter") != adapter:
            raise EvaluationError(
                "PROVIDER_CONFORMANCE_SCHEMA_ERROR", "adapter changed after freeze"
            )
        if strategy.get("contract") != contract:
            raise EvaluationError(
                "PROVIDER_CONFORMANCE_SCHEMA_ERROR", "prompt or schema contract changed"
            )
        config = strategy.get("config")
        if not isinstance(config, dict):
            raise EvaluationError("PROVIDER_CONFORMANCE_SCHEMA_ERROR", "strategy config is missing")
        for key, expected in {
            "api_surface": API_SURFACE,
            "response_mode": RESPONSE_MODE,
            "schema_mechanism": SCHEMA_MECHANISM,
            "temperature": 0,
            "thinking_mode": THINKING_MODE,
            "reasoning_effort": REASONING_EFFORT,
            "output_token_limit": MAX_OUTPUT_TOKENS,
            "sdk_max_retries": 0,
        }.items():
            if config.get(key) != expected:
                raise EvaluationError(
                    "PROVIDER_CONFORMANCE_SCHEMA_ERROR", f"invalid strategy config: {key}"
                )
        canary_runs = strategy.get("canary_runs")
        if not isinstance(canary_runs, list) or len(canary_runs) != 3:
            raise EvaluationError(
                "PROVIDER_CONFORMANCE_SCHEMA_ERROR", "each strategy needs three canary runs"
            )
        video_ids: set[str] = set()
        for declaration in canary_runs:
            if not isinstance(declaration, dict):
                raise EvaluationError(
                    "PROVIDER_CONFORMANCE_SCHEMA_ERROR", "canary declaration is invalid"
                )
            video_id = declaration.get("video_id")
            run_id = declaration.get("run_id")
            if video_id not in {item[0] for item in FIXED_SOURCES} or video_id in video_ids:
                raise EvaluationError(
                    "PROVIDER_CONFORMANCE_SCHEMA_ERROR", "canary videos must be unique"
                )
            if not isinstance(run_id, str) or run_id in canary_ids:
                raise EvaluationError(
                    "PROVIDER_CONFORMANCE_SCHEMA_ERROR", "canary run IDs must be unique"
                )
            if (
                declaration.get("planned_provider_calls") != 2
                or declaration.get("planned_model_calls") != 2
            ):
                raise EvaluationError(
                    "PROVIDER_CONFORMANCE_SCHEMA_ERROR", "canary call budget must be two"
                )
            video_ids.add(str(video_id))
            canary_ids.add(run_id)
    shared = payload.get("shared_contract")
    if shared != contract:
        raise EvaluationError(
            "PROVIDER_CONFORMANCE_SCHEMA_ERROR", "shared contract is not canonical"
        )
    return payload


def freeze_provider_conformance(
    *,
    repository_root: Path,
    artifact_root: Path,
    card_root: Path,
    output_path: Path,
) -> dict[str, object]:
    """Freeze all provider strategies and canary identities before transcript egress."""
    repository_root = repository_root.resolve()
    artifact_root = artifact_root.resolve()
    card_root = card_root.resolve()
    source_rows = _fixed_source_rows(repository_root)
    card_rows = _review_card_rows(card_root, source_rows)
    environment = environment_snapshot(repository_root)
    contract = _provider_contract_snapshot()
    adapter = _provider_adapter_snapshot()
    current_model = str(environment.get("model", ""))
    first_model = (
        current_model
        if current_model in SUPPORTED_DEEPSEEK_MODELS
        else SUPPORTED_DEEPSEEK_MODELS[0]
    )
    second_model = next(model for model in SUPPORTED_DEEPSEEK_MODELS if model != first_model)
    base_eligible = bool(
        environment.get("admission") == "READY"
        and environment.get("provider") == "https://api.deepseek.com"
        and environment.get("credential_present") is True
        and environment.get("timeout_seconds") == 120.0
        and environment.get("sdk_version") not in {None, "unavailable"}
    )
    endpoint = os.getenv("OPENAI_BASE_URL", "").strip() or "https://api.openai.com/v1"
    strategies: list[dict[str, object]] = []
    for order, model in enumerate((first_model, second_model), start=1):
        suffix = "a" if order == 1 else "b"
        strategy_id = f"{model}-responses-json-schema-{suffix}"
        eligible = base_eligible
        blockers = [] if eligible else list(environment.get("blockers", []))
        if environment.get("provider") != "https://api.deepseek.com":
            blockers.append("DeepSeek endpoint is not configured")
        if environment.get("timeout_seconds") != 120.0:
            blockers.append("timeout must be 120 seconds for this frozen strategy")
        strategies.append(
            {
                "strategy_id": strategy_id,
                "order": order,
                "provider": "DeepSeek",
                "provider_label": environment.get("provider"),
                "endpoint": endpoint,
                "model": model,
                "model_version": model,
                "api_surface": API_SURFACE,
                "response_mode": RESPONSE_MODE,
                "schema_mechanism": SCHEMA_MECHANISM,
                "adapter": adapter,
                "contract": contract,
                "config": {
                    "provider": environment.get("provider"),
                    "model": model,
                    "model_version": model,
                    "timeout_seconds": 120.0,
                    "credential_present": bool(environment.get("credential_present")),
                    "api_surface": API_SURFACE,
                    "response_mode": RESPONSE_MODE,
                    "schema_mechanism": SCHEMA_MECHANISM,
                    "temperature": 0,
                    "thinking_mode": THINKING_MODE,
                    "reasoning_effort": REASONING_EFFORT,
                    "output_token_limit": MAX_OUTPUT_TOKENS,
                    "sdk_max_retries": 0,
                    "sdk_version": environment.get("sdk_version"),
                },
                "prompt_bundle": contract["prompts"],
                "schemas": contract["schemas"],
                "capability_evidence": [
                    {
                        "source": "DeepSeek Responses API reference",
                        "url": DEEPSEEK_RESPONSES_DOC,
                        "claim": (
                            "Responses text.format supports provider-native json_schema "
                            "with name and schema."
                        ),
                    },
                    {
                        "source": "DeepSeek model and API availability",
                        "url": DEEPSEEK_MODELS_DOC,
                        "claim": (
                            f"{model} is a declared DeepSeek model available to the Responses API."
                        ),
                    },
                ],
                "eligibility": "ELIGIBLE" if eligible else "INELIGIBLE",
                "eligibility_blockers": blockers,
                "canary_runs": _canary_declarations(f"candidate-{suffix}"),
            }
        )
    stable_payload = {
        "schema_version": PROVIDER_CONFORMANCE_SCHEMA_VERSION,
        "repository_root": str(repository_root),
        "artifact_root": str(artifact_root),
        "sources": source_rows,
        "review_cards": card_rows,
        "environment": environment,
        "shared_contract": contract,
        "strategies": strategies,
        "call_ledger": {
            "max_new_transcript_bearing_provider_model_calls": 24,
            "canary_max_calls": 12,
            "formal_max_calls": 12,
            "per_run_max_calls": 2,
            "sdk_max_retries": 0,
            "comparison_stop": (
                "stop after first strategy with three rendered canaries and "
                "non-identical signatures"
            ),
        },
        "source_policy": (
            "full transcript for every mapper and planner call; no chunking or fallback"
        ),
    }
    revision_id = f"vr1a-provider-{_sha256_bytes(stable_json(stable_payload).encode('utf-8'))[:12]}"
    payload = {
        **stable_payload,
        "revision_id": revision_id,
        "status": "FROZEN" if base_eligible else "EXTERNAL_BLOCKED",
        "frozen_at": _now(),
    }
    _validate_provider_conformance_manifest(payload)
    _write_new_json(output_path, payload)
    return payload


def load_provider_conformance_manifest(path: Path) -> dict[str, object]:
    payload = _read_json(path)
    return _validate_provider_conformance_manifest(payload)


def load_provider_conformance_strategy(
    path: Path, strategy_id: str | None = None
) -> dict[str, object]:
    payload = load_provider_conformance_manifest(path)
    strategies = payload["strategies"]
    assert isinstance(strategies, list)
    eligible = [
        item
        for item in strategies
        if isinstance(item, dict) and item.get("eligibility") == "ELIGIBLE"
    ]
    if strategy_id is None:
        if len(eligible) != 1:
            raise EvaluationError(
                "PROVIDER_CONFORMANCE_SELECTION_ERROR",
                "strategy_id is required when more than one eligible strategy is frozen",
            )
        selected = eligible[0]
    else:
        selected = next(
            (
                item
                for item in strategies
                if isinstance(item, dict) and item.get("strategy_id") == strategy_id
            ),
            None,
        )
        if selected is None:
            raise EvaluationError("PROVIDER_CONFORMANCE_SELECTION_ERROR", "unknown strategy_id")
        if selected.get("eligibility") != "ELIGIBLE":
            raise EvaluationError(
                "PROVIDER_CONFORMANCE_SELECTION_ERROR", "selected strategy is ineligible"
            )
    result = dict(selected)
    result["strategy_manifest_sha256"] = _sha256_file(path.resolve())
    result["manifest_revision_id"] = payload.get("revision_id")
    return result


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
    strategy_manifest_path: Path | None = None,
    strategy_id: str | None = None,
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
    if strategy_manifest_path is not None:
        strategy = load_provider_conformance_strategy(strategy_manifest_path, strategy_id)
        strategy_config = strategy.get("config")
        if not isinstance(strategy_config, dict):
            raise EvaluationError("PROVIDER_CONFORMANCE_SCHEMA_ERROR", "strategy config is missing")
        provider = {
            **provider,
            **{
                key: strategy_config.get(key)
                for key in (
                    "provider",
                    "model",
                    "model_version",
                    "timeout_seconds",
                    "credential_present",
                    "api_surface",
                    "response_mode",
                    "schema_mechanism",
                    "temperature",
                    "thinking_mode",
                    "reasoning_effort",
                    "output_token_limit",
                    "sdk_max_retries",
                    "sdk_version",
                )
                if key in strategy_config
            },
            "strategy_id": strategy.get("strategy_id"),
            "strategy_manifest_sha256": strategy.get("strategy_manifest_sha256"),
            "strategy_manifest_path": str(strategy_manifest_path.resolve()),
            "strategy_revision_id": strategy.get("manifest_revision_id"),
        }
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
    collisions = [
        str(run["run_id"]) for run in runs if (artifact_root / str(run["run_id"])).exists()
    ]
    if collisions:
        raise EvaluationError(
            "EVALUATION_OUTPUT_EXISTS",
            f"measurement run directories already exist: {', '.join(collisions)}",
        )
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
        and all(
            config_snapshot.get(key) == expected_config.get(key)
            for key in (
                "provider",
                "model",
                "model_version",
                "timeout_seconds",
                "credential_present",
                "api_surface",
                "response_mode",
                "schema_mechanism",
                "temperature",
                "thinking_mode",
                "reasoning_effort",
                "output_token_limit",
                "sdk_max_retries",
                "sdk_version",
                "strategy_id",
                "strategy_manifest_sha256",
            )
        )
    )
    deterministic["revision_snapshot_match"] = snapshot_match
    if not snapshot_match:
        errors.append("run source/config snapshot does not match frozen measurement")

    calls_path = run_dir / "model-calls.jsonl"
    calls = _read_jsonl(calls_path) if calls_path.is_file() else []
    expected_call_config = freeze.provider
    call_valid = (
        len(calls) == 2
        and [call.get("stage") for call in calls] == ["topic_mapper", "report_planner"]
        and all(
            call.get("schema_version") == CALL_SCHEMA_VERSION
            and call.get("schema_valid") is True
            and call.get("error_category") is None
            and call.get("api_surface") == expected_call_config.get("api_surface")
            and call.get("response_mode") == expected_call_config.get("response_mode")
            and call.get("schema_mechanism") == expected_call_config.get("schema_mechanism")
            and call.get("reasoning_effort") == expected_call_config.get("reasoning_effort")
            and call.get("strategy_id") == expected_call_config.get("strategy_id")
            and call.get("strategy_manifest_sha256")
            == expected_call_config.get("strategy_manifest_sha256")
            and call.get("schema_name")
            == {
                "topic_mapper": "v1a_topic_map_proposal",
                "report_planner": "v1a_report_plan_proposal",
            }.get(str(call.get("stage")))
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


def evaluate_measurement(*, measurement_path: Path, output_root: Path) -> dict[str, object]:
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
                bool(row["deterministic"]["first_pass_schema_compile_render"]) for row in video_rows
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


def _conformance_run_outcome(
    declaration: dict[str, object], strategy: dict[str, object], artifact_root: Path
) -> dict[str, object]:
    run_id = str(declaration.get("run_id"))
    run_dir = artifact_root / run_id
    run_payload = _read_run_json(run_dir)
    calls_path = run_dir / "model-calls.jsonl"
    calls = _read_jsonl(calls_path) if calls_path.is_file() else []
    errors: list[str] = []
    signature: str | None = None
    state = "MISSING"
    observed_provider_calls = 0
    observed_model_calls = 0
    if run_payload is None:
        errors.append("run.json is missing")
    else:
        state = str(run_payload.get("state", "UNKNOWN"))
        observed_provider_calls = int(run_payload.get("provider_calls", 0))
        observed_model_calls = int(run_payload.get("model_calls", 0))
        config = run_payload.get("config")
        expected_config = strategy.get("config")
        if not isinstance(config, dict) or not isinstance(expected_config, dict):
            errors.append("strategy config snapshot is missing")
        else:
            for key in (
                "provider",
                "model",
                "model_version",
                "timeout_seconds",
                "credential_present",
                "api_surface",
                "response_mode",
                "schema_mechanism",
                "temperature",
                "thinking_mode",
                "reasoning_effort",
                "output_token_limit",
                "sdk_max_retries",
                "sdk_version",
            ):
                if config.get(key) != expected_config.get(key):
                    errors.append(f"config snapshot mismatch: {key}")
        if run_payload.get("strategy_id") != strategy.get("strategy_id"):
            errors.append("run strategy_id mismatch")
        expected_manifest_sha = strategy.get("strategy_manifest_sha256")
        if (
            expected_manifest_sha is not None
            and run_payload.get("strategy_manifest_sha256") != expected_manifest_sha
        ):
            errors.append("run strategy manifest hash mismatch")
    if len(calls) != 2:
        errors.append("model call trace is not exactly two calls")
    else:
        expected_model = strategy.get("model")
        expected_config = strategy.get("config")
        for index, (call, stage) in enumerate(zip(calls, ("topic_mapper", "report_planner"))):
            if call.get("stage") != stage:
                errors.append(f"call {index + 1} stage mismatch")
            if call.get("schema_valid") is not True or call.get("error_category") is not None:
                errors.append(f"call {index + 1} was not a successful first-pass call")
            if call.get("model") != expected_model:
                errors.append(f"call {index + 1} model mismatch")
            if isinstance(expected_config, dict):
                for key in ("api_surface", "response_mode", "schema_mechanism", "reasoning_effort"):
                    if call.get(key) != expected_config.get(key):
                        errors.append(f"call {index + 1} {key} mismatch")
    plan_path = run_dir / "report-plan.json"
    if plan_path.is_file():
        try:
            from .models import ReportPlan

            signature = _structure_signature(ReportPlan.model_validate(_read_json(plan_path)))
        except ValidationError:
            errors.append("report plan is invalid")
    else:
        errors.append("report plan is missing")
    success = (
        not errors
        and state == "RENDERED"
        and observed_provider_calls == 2
        and observed_model_calls == 2
        and (run_dir / "report.html").is_file()
        and signature is not None
    )
    return {
        "run_id": run_id,
        "video_id": declaration.get("video_id"),
        "state": state,
        "provider_calls": observed_provider_calls,
        "model_calls": observed_model_calls,
        "rendered": success,
        "structure_signature": signature,
        "errors": errors,
    }


def finalize_provider_conformance(
    *,
    manifest_path: Path,
    artifact_root: Path,
    output_path: Path,
) -> dict[str, object]:
    """Record canary outcomes without changing the frozen candidate manifest."""
    manifest = load_provider_conformance_manifest(manifest_path)
    strategies = manifest["strategies"]
    assert isinstance(strategies, list)
    strategy_rows: list[dict[str, object]] = []
    selected_strategy_id: str | None = None
    stop_reached = False
    total_calls = 0
    for strategy in strategies:
        assert isinstance(strategy, dict)
        if strategy.get("eligibility") != "ELIGIBLE":
            strategy_rows.append(
                {
                    "strategy_id": strategy.get("strategy_id"),
                    "eligibility": strategy.get("eligibility"),
                    "status": "INELIGIBLE",
                    "runs": [],
                    "observed_provider_calls": 0,
                    "observed_model_calls": 0,
                }
            )
            continue
        if stop_reached:
            strategy_rows.append(
                {
                    "strategy_id": strategy.get("strategy_id"),
                    "eligibility": "ELIGIBLE",
                    "status": "NOT_RUN_AFTER_COMPARISON_STOP",
                    "runs": [],
                    "observed_provider_calls": 0,
                    "observed_model_calls": 0,
                }
            )
            continue
        declarations = strategy.get("canary_runs")
        assert isinstance(declarations, list)
        strategy_for_run = dict(strategy)
        strategy_for_run["strategy_manifest_sha256"] = _sha256_file(manifest_path.resolve())
        outcomes = [
            _conformance_run_outcome(declaration, strategy_for_run, artifact_root)
            for declaration in declarations
            if isinstance(declaration, dict)
        ]
        calls = sum(int(outcome["provider_calls"]) for outcome in outcomes)
        model_calls = sum(int(outcome["model_calls"]) for outcome in outcomes)
        total_calls += calls
        rendered = [outcome for outcome in outcomes if outcome["rendered"] is True]
        signatures = [outcome["structure_signature"] for outcome in rendered]
        all_runs_terminal = len(outcomes) == 3 and all(
            outcome["state"] in {"RENDERED", "FAILED", "CANCELLED"} for outcome in outcomes
        )
        complete_pass = all_runs_terminal and len(rendered) == 3 and len(set(signatures)) > 1
        status = "PASS" if complete_pass else ("FAIL" if all_runs_terminal else "INCOMPLETE")
        row = {
            "strategy_id": strategy.get("strategy_id"),
            "eligibility": "ELIGIBLE",
            "status": status,
            "runs": outcomes,
            "observed_provider_calls": calls,
            "observed_model_calls": model_calls,
            "rendered_count": len(rendered),
            "unique_rendered_signatures": len(set(signatures)),
        }
        strategy_rows.append(row)
        if complete_pass:
            selected_strategy_id = str(strategy["strategy_id"])
            stop_reached = True
    eligible_rows = [row for row in strategy_rows if row.get("eligibility") == "ELIGIBLE"]
    all_complete = all(row.get("status") in {"PASS", "FAIL"} for row in eligible_rows)
    if selected_strategy_id is not None:
        terminal_status = "PASS"
        conclusion = "STOPPED_AFTER_FIRST_PASS"
    elif all_complete and eligible_rows:
        terminal_status = "NO_GO"
        conclusion = "V1A_PROVIDER_CONFORMANCE_NO_GO"
    elif not eligible_rows:
        terminal_status = "NO_GO"
        conclusion = "EXTERNAL_BLOCKED"
    else:
        terminal_status = "PENDING"
        conclusion = "AWAITING_REMAINING_ELIGIBLE_CANARIES"
    if total_calls > 24:
        raise EvaluationError(
            "PROVIDER_CONFORMANCE_CALL_LIMIT", "canary calls exceeded frozen limit"
        )
    result = {
        "schema_version": PROVIDER_CONFORMANCE_RESULT_SCHEMA_VERSION,
        "manifest_path": str(manifest_path.resolve()),
        "manifest_revision_id": manifest.get("revision_id"),
        "manifest_sha256": _sha256_file(manifest_path.resolve()),
        "artifact_root": str(artifact_root.resolve()),
        "terminal_status": terminal_status,
        "conclusion": conclusion,
        "selected_strategy_id": selected_strategy_id,
        "comparison_stop": stop_reached,
        "max_new_transcript_bearing_provider_model_calls": 24,
        "observed_provider_calls": total_calls,
        "observed_model_calls": total_calls,
        "strategies": strategy_rows,
        "generated_at": _now(),
    }
    _write_new_json(output_path, result)
    return result


def _semantic_v2_product_source_rows(source_root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for video_id, manifest_rel, segments_rel in FIXED_SOURCES:
        manifest_path = source_root / manifest_rel
        segments_path = source_root / segments_rel
        source = load_source(manifest_path, segments_path)
        if source.video_id != video_id:
            raise EvaluationError(
                "SOURCE_SNAPSHOT_MISMATCH", f"unexpected source video_id: {video_id}"
            )
        rows.append(
            {
                "video_id": video_id,
                "manifest_path": str(manifest_path.resolve()),
                "segments_path": str(segments_path.resolve()),
                "manifest_sha256": source.manifest_sha256,
                "segments_sha256": source.segments_sha256,
                "segment_count": len(source.segments),
                "duration_ms": source.duration_ms,
            }
        )
    return rows


def _semantic_v2_provider_snapshot(repository_root: Path) -> dict[str, object]:
    snapshot = environment_snapshot(repository_root)
    blockers = list(snapshot.get("blockers", []))
    provider = str(snapshot.get("provider", ""))
    model = str(snapshot.get("model", ""))
    if "deepseek" not in provider.lower() or not model.lower().startswith("deepseek"):
        blockers.append("current product prototype requires the configured DeepSeek endpoint/model")
    snapshot.update(
        {
            "provider_family": "DeepSeek",
            "api_surface": SEMANTIC_V2_API_SURFACE,
            "response_mode": SEMANTIC_V2_RESPONSE_MODE,
            "schema_mechanism": SEMANTIC_V2_SCHEMA_MECHANISM,
            "temperature": 0,
            "thinking_mode": THINKING_MODE,
            "reasoning_effort": "none",
            "output_token_limit": MAX_OUTPUT_TOKENS,
            "sdk_max_retries": 0,
            "technical_retry_max_per_run": 1,
            "blockers": blockers,
            "admission": "READY" if not blockers else "BLOCKED_CONFIGURATION",
        }
    )
    return snapshot


def _semantic_v2_contract_snapshot() -> dict[str, object]:
    return {
        "prompts": {
            "mapper": {
                "version": SEMANTIC_V2_MAPPER_PROMPT_VERSION,
                "sha256": _sha256_bytes(
                    SEMANTIC_V2_MAPPER_SYSTEM_INSTRUCTION.encode("utf-8")
                ),
            },
            "planner": {
                "version": SEMANTIC_V2_PLANNER_PROMPT_VERSION,
                "sha256": _sha256_bytes(
                    SEMANTIC_V2_PLANNER_SYSTEM_INSTRUCTION.encode("utf-8")
                ),
            },
        },
        "schemas": {
            "topic_proposal": _schema_fingerprint(
                "semantic_v2_topic_map_proposal",
                SEMANTIC_V2_TOPIC_PROPOSAL_SCHEMA_VERSION,
                SemanticV2TopicMapProposal.model_json_schema(),
            ),
            "topic_map": {
                "name": "semantic_v2_topic_map",
                "schema_version": SEMANTIC_V2_TOPIC_MAP_SCHEMA_VERSION,
            },
            "plan_proposal": _schema_fingerprint(
                "semantic_v2_report_plan_proposal",
                SEMANTIC_V2_PLAN_PROPOSAL_SCHEMA_VERSION,
                SemanticV2ReportPlanProposal.model_json_schema(),
            ),
            "normalization": {
                "name": "semantic_v2_normalization_ledger",
                "schema_version": SEMANTIC_V2_NORMALIZATION_SCHEMA_VERSION,
            },
            "call": SEMANTIC_V2_CALL_SCHEMA_VERSION,
            "compiler": SEMANTIC_V2_COMPILER_VERSION,
        },
        "pipeline": [
            "topic_mapper",
            "deterministic_topic_resolver",
            "report_planner",
            "deterministic_v0_compiler",
            "v0_renderer",
        ],
    }


def freeze_semantic_v2_product_prototype(
    *,
    repository_root: Path,
    artifact_root: Path,
    card_root: Path,
    output_path: Path,
    source_root: Path | None = None,
) -> SemanticV2ProductFreeze:
    """Freeze one current three-video semantic-v2 prototype set."""
    repository_root = repository_root.resolve()
    source_root = (source_root or repository_root).resolve()
    artifact_root = artifact_root.resolve()
    card_root = card_root.resolve()
    source_rows = _semantic_v2_product_source_rows(source_root)
    card_rows: list[dict[str, object]] = []
    card_paths = _card_paths(card_root)
    for video_id, _, _ in FIXED_SOURCES:
        path = card_paths[video_id]
        card = _card_payload(path)
        source_row = next(row for row in source_rows if row["video_id"] == video_id)
        source = load_source(
            Path(str(source_row["manifest_path"])), Path(str(source_row["segments_path"]))
        )
        validate_review_card(card, source)
        card_rows.append(
            {
                "video_id": video_id,
                "path": str(path.resolve()),
                "sha256": _sha256_file(path),
                "schema_version": REVIEW_CARD_SCHEMA_VERSION,
            }
        )
    provider = _semantic_v2_provider_snapshot(repository_root)
    contract = _semantic_v2_contract_snapshot()
    runtime_path = Path(__file__).with_name("planning_runtime.py").resolve()
    evaluator_path = Path(__file__).resolve()
    stable_payload = {
        "schema_version": SEMANTIC_V2_PRODUCT_MANIFEST_SCHEMA_VERSION,
        "repository_root": str(repository_root),
        "source_root": str(source_root),
        "artifact_root": str(artifact_root),
        "sources": source_rows,
        "provider": provider,
        "contract": contract,
        "review_cards": card_rows,
        "evaluator": {
            "version": SEMANTIC_V2_PRODUCT_EVALUATOR_VERSION,
            "module": str(evaluator_path),
            "sha256": _sha256_file(evaluator_path),
        },
        "runtime": {
            "module": str(runtime_path),
            "sha256": _sha256_file(runtime_path),
        },
        "limits": {
            "videos": 3,
            "base_provider_calls_per_run": 2,
            "maximum_provider_calls_per_run": 3,
            "maximum_total_provider_calls": 9,
            "technical_retry_max_per_run": 1,
            "formal_six_run_measurement": False,
        },
    }
    revision_seed = _sha256_bytes(stable_json(stable_payload).encode("utf-8"))[:10]
    runs = [
        {
            "run_id": f"{video_id}-semantic-v2-{revision_seed}",
            "video_id": video_id,
            "planned_provider_calls": 2,
            "maximum_provider_calls": 3,
        }
        for video_id, _, _ in FIXED_SOURCES
    ]
    collisions = [
        str(run["run_id"]) for run in runs if (artifact_root / str(run["run_id"])).exists()
    ]
    if collisions:
        raise EvaluationError(
            "EVALUATION_OUTPUT_EXISTS",
            f"semantic-v2 product run directories already exist: {', '.join(collisions)}",
        )
    revision_hash = _sha256_bytes(
        stable_json({**stable_payload, "runs": runs}).encode("utf-8")
    )[:12]
    payload = {
        **stable_payload,
        "revision_id": f"vr1a-semantic-v2-{revision_hash}",
        "status": "FROZEN" if provider["admission"] == "READY" else "FROZEN_PROVIDER_BLOCKED",
        "frozen_at": _now(),
        "prompts": contract["prompts"],
        "schemas": contract["schemas"],
        "runs": runs,
    }
    _write_new_json(output_path, payload)
    try:
        return SemanticV2ProductFreeze.model_validate(payload)
    except ValidationError as exc:
        raise EvaluationError("SEMANTIC_V2_MANIFEST_SCHEMA_ERROR", str(exc)) from exc


def load_semantic_v2_product_freeze(path: Path) -> SemanticV2ProductFreeze:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise EvaluationError(
            "SEMANTIC_V2_MANIFEST_SCHEMA_ERROR", "product manifest must be an object"
        )
    try:
        return SemanticV2ProductFreeze.model_validate(payload)
    except ValidationError as exc:
        raise EvaluationError("SEMANTIC_V2_MANIFEST_SCHEMA_ERROR", str(exc)) from exc


def derive_semantic_v2_product_review_manifest(
    *, source_manifest_path: Path, output_path: Path
) -> SemanticV2ProductFreeze:
    """Create an append-only review revision after a deterministic evaluator fix."""
    source_payload = _read_json(source_manifest_path)
    if not isinstance(source_payload, dict):
        raise EvaluationError(
            "SEMANTIC_V2_MANIFEST_SCHEMA_ERROR", "source manifest must be an object"
        )
    source_freeze = load_semantic_v2_product_freeze(source_manifest_path)
    evaluator_path = Path(__file__).resolve()
    payload = {
        **source_payload,
        "revision_id": f"{source_freeze.revision_id}-review",
        "derived_from_manifest": str(source_manifest_path.resolve()),
        "evaluator": {
            "version": SEMANTIC_V2_PRODUCT_EVALUATOR_VERSION,
            "module": str(evaluator_path),
            "sha256": _sha256_file(evaluator_path),
        },
        "derived_at": _now(),
        "derivation_reason": "deterministic evaluator accepts a recovered single technical retry",
    }
    # The review revision keeps the exact frozen sources, provider tuple, and
    # run identities; it authorizes no new provider call.
    _write_new_json(output_path, payload)
    try:
        return SemanticV2ProductFreeze.model_validate(payload)
    except ValidationError as exc:
        raise EvaluationError("SEMANTIC_V2_MANIFEST_SCHEMA_ERROR", str(exc)) from exc


def _semantic_v2_pending_rubric(
    *, revision_id: str, run_id: str, video_id: str, path: Path
) -> dict[str, object]:
    payload = {
        "schema_version": SEMANTIC_V2_PRODUCT_RUBRIC_SCHEMA_VERSION,
        "revision_id": revision_id,
        "run_id": run_id,
        "video_id": video_id,
        "reviewer": "owner-or-designated-human",
        "status": "PENDING_OWNER_REVIEW",
        "categories": {
            "content_coverage": None,
            "grounding": None,
            "cross_video_structure_fit": None,
            "desktop_visual_quality": None,
            "mobile_visual_quality": None,
        },
        "major_unsupported_claims": [],
        "source_notes": [],
    }
    _write_new_json(path, payload)
    return payload


def _semantic_v2_product_run_row(
    declaration: ProductRunDeclaration,
    freeze: SemanticV2ProductFreeze,
    source: SourceSnapshot,
    card: ReviewCard,
    run_dir: Path,
    rubric_path: Path,
) -> dict[str, object]:
    row: dict[str, object] = {
        "run_id": declaration.run_id,
        "video_id": declaration.video_id,
        "run_dir": str(run_dir),
        "state": "MISSING",
        "provider_calls": 0,
        "model_calls": 0,
        "technical_status": "FAILED",
        "content_review_status": "PENDING_OWNER_REVIEW",
        "visual_review_status": "PENDING_OWNER_REVIEW",
        "deterministic": {
            "execution_valid": False,
            "source_snapshot_match": False,
            "topic_map_valid": False,
            "report_plan_valid": False,
            "normalization_ledger_valid": False,
            "assets_empty": False,
            "report_present": False,
            "desktop_screenshot_present": False,
            "mobile_screenshot_present": False,
            "structure_signature": None,
            "must_cover_reference_recall": None,
            "errors": ["run.json is missing"],
        },
        "review_artifacts": {
            "run_json": str(run_dir / "run.json"),
            "topic_map": str(run_dir / "topic-map.json"),
            "report_plan": str(run_dir / "report-plan.json"),
            "normalization": str(run_dir / "normalization.json"),
            "report_html": str(run_dir / "report.html"),
            "desktop_screenshot": str(run_dir / "screenshots" / "desktop.png"),
            "mobile_screenshot": str(run_dir / "screenshots" / "mobile.png"),
            "rubric": str(rubric_path),
        },
    }
    run_payload = _read_run_json(run_dir)
    if run_payload is None:
        row["human_rubric"] = _semantic_v2_pending_rubric(
            revision_id=freeze.revision_id,
            run_id=declaration.run_id,
            video_id=declaration.video_id,
            path=rubric_path,
        )
        return row
    row["state"] = run_payload.get("state", "UNKNOWN")
    row["provider_calls"] = int(run_payload.get("provider_calls", 0))
    row["model_calls"] = int(run_payload.get("model_calls", 0))
    row["usage"] = run_payload.get("usage", {})
    row["latency_ms_total"] = run_payload.get("latency_ms_total", 0)
    row["cost"] = run_payload.get("cost", "unavailable")
    calls_path = run_dir / "model-calls.jsonl"
    calls = _read_jsonl(calls_path) if calls_path.is_file() else []
    errors: list[str] = []
    deterministic = row["deterministic"]
    assert isinstance(deterministic, dict)
    source_row = next(
        (item for item in freeze.sources if item.get("video_id") == declaration.video_id),
        {},
    )
    source_snapshot = run_payload.get("source")
    source_match = (
        isinstance(source_snapshot, dict)
        and source_snapshot.get("video_id") == source.video_id
        and source_snapshot.get("manifest_sha256") == source_row.get("manifest_sha256")
        and source_snapshot.get("segments_sha256") == source_row.get("segments_sha256")
        and source_snapshot.get("segment_count") == len(source.segments)
    )
    deterministic["source_snapshot_match"] = source_match
    if not source_match:
        errors.append("source snapshot differs from frozen product manifest")
    expected_config = freeze.provider
    config = run_payload.get("config")
    if not isinstance(config, dict):
        errors.append("run config snapshot is missing")
    else:
        for key in (
            "provider",
            "model",
            "timeout_seconds",
            "credential_present",
            "api_surface",
            "response_mode",
            "schema_mechanism",
            "temperature",
            "thinking_mode",
            "reasoning_effort",
            "output_token_limit",
            "sdk_max_retries",
        ):
            if expected_config.get(key) != config.get(key):
                errors.append(f"run config differs from frozen product contract: {key}")
    observed_calls = int(run_payload.get("provider_calls", 0))
    calls_valid = observed_calls in {2, 3} and observed_calls == len(calls)
    if not calls_valid:
        errors.append("provider call count is outside the two-base/three-maximum contract")
    call_stages = [str(call.get("stage")) for call in calls]
    valid_call_stages = {
        ("topic_mapper", "report_planner"),
        ("topic_mapper", "topic_mapper", "report_planner"),
        ("topic_mapper", "report_planner", "report_planner"),
    }
    if tuple(call_stages) not in valid_call_stages:
        errors.append("semantic stage order is not mapper then planner with at most one retry")
    call_errors = [str(call.get("error_category")) for call in calls if call.get("error_category")]
    row["technical_failures"] = call_errors
    recovered_retry = (
        len(calls) == 3
        and len(call_errors) == 1
        and calls[-1].get("error_category") is None
        and run_payload.get("retry_used") is True
        and (
            (
                calls[0].get("request_sha256") == calls[1].get("request_sha256")
                and calls[1].get("retry_of_attempt") == 1
            )
            or (
                calls[1].get("request_sha256") == calls[2].get("request_sha256")
                and calls[2].get("retry_of_attempt") == 1
            )
        )
    )
    if call_errors and not recovered_retry:
        errors.append("provider call error was not recovered within the single retry contract")

    segment_by_id = _segment_map(source)
    topic_map: SemanticV2TopicMap | None = None
    topic_path = run_dir / "topic-map.json"
    if topic_path.is_file():
        try:
            topic_map = SemanticV2TopicMap.model_validate(_read_json(topic_path))
        except ValidationError as exc:
            errors.append(
                "semantic-v2 Topic Map schema error: "
                f"{exc.errors()[0].get('msg', 'invalid')}"
            )
    if topic_map is not None:
        map_refs = [ref for topic in topic_map.topics for ref in topic.source_refs]
        map_refs.extend(
            ref for topic in topic_map.topics for ref in topic.representative_source_refs
        )
        map_valid = topic_map.video_id == source.video_id and all(
            _valid_source_ref(ref, segment_by_id) for ref in map_refs
        )
        deterministic["topic_map_valid"] = map_valid
        deterministic["must_cover_reference_recall"] = _card_recall(
            card, {ref.segment_id for ref in map_refs}
        )
        if not map_valid:
            errors.append("semantic-v2 Topic Map source refs are invalid")
    else:
        errors.append("semantic-v2 Topic Map artifact is missing or invalid")

    plan: ReportPlan | None = None
    plan_path = run_dir / "report-plan.json"
    assets_path = run_dir / "assets.json"
    if plan_path.is_file() and assets_path.is_file():
        try:
            plan = ReportPlan.model_validate(_read_json(plan_path))
            assets = AssetManifest.model_validate(_read_json(assets_path))
            deterministic["assets_empty"] = len(assets.assets) == 0
        except ValidationError as exc:
            errors.append(
                "V0 report artifact schema error: "
                f"{exc.errors()[0].get('msg', 'invalid')}"
            )
    else:
        errors.append("report plan or assets artifact is missing")
    if plan is not None:
        report_refs = [
            ref
            for section in plan.sections
            for block in section.blocks
            for ref in block.source_refs
        ]
        report_refs_valid = all(_valid_source_ref(ref, segment_by_id) for ref in report_refs)
        deterministic["report_plan_valid"] = report_refs_valid
        deterministic["structure_signature"] = _structure_signature(plan)
        if not report_refs_valid:
            errors.append("report plan source refs are invalid")
        if not deterministic["assets_empty"]:
            errors.append("assets manifest is not empty")
    normalization_path = run_dir / "normalization.json"
    if normalization_path.is_file():
        normalization = _read_json(normalization_path)
        deterministic["normalization_ledger_valid"] = isinstance(normalization, dict) and (
            normalization.get("schema_version") == SEMANTIC_V2_NORMALIZATION_SCHEMA_VERSION
            and isinstance(normalization.get("summary"), dict)
            and all(
                int(normalization["summary"].get(key, -1)) == 0
                for key in (
                    "semantic_rewrite_count",
                    "semantic_merge_count",
                    "semantic_split_count",
                    "semantic_synthesis_count",
                )
            )
        )
    if not deterministic["normalization_ledger_valid"]:
        errors.append("normalization ledger is missing, invalid, or records semantic repair")
    report_present = (run_dir / "report.html").is_file()
    desktop_present = (run_dir / "screenshots" / "desktop.png").is_file()
    mobile_present = (run_dir / "screenshots" / "mobile.png").is_file()
    deterministic["report_present"] = report_present
    deterministic["desktop_screenshot_present"] = desktop_present
    deterministic["mobile_screenshot_present"] = mobile_present
    if not report_present:
        errors.append("report.html is missing")
    deterministic["errors"] = errors
    deterministic["execution_valid"] = bool(
        run_payload.get("state") == "RENDERED"
        and calls_valid
        and source_match
        and deterministic["topic_map_valid"]
        and deterministic["report_plan_valid"]
        and deterministic["normalization_ledger_valid"]
        and deterministic["assets_empty"]
        and report_present
        and (not call_errors or recovered_retry)
        and not errors
    )
    row["technical_status"] = "PASS" if deterministic["execution_valid"] else "FAILED"
    row["content_review_status"] = (
        "PENDING_OWNER_REVIEW" if report_present else "NOT_AVAILABLE"
    )
    row["visual_review_status"] = (
        "PENDING_OWNER_REVIEW" if desktop_present and mobile_present else "NOT_AVAILABLE"
    )
    row["human_rubric"] = _semantic_v2_pending_rubric(
        revision_id=freeze.revision_id,
        run_id=declaration.run_id,
        video_id=declaration.video_id,
        path=rubric_path,
    )
    return row


def review_semantic_v2_product_prototype(
    *, manifest_path: Path, output_root: Path
) -> dict[str, object]:
    """Create the deterministic product review package and pending Owner gates."""
    freeze = load_semantic_v2_product_freeze(manifest_path)
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
                "SEMANTIC_V2_MANIFEST_STALE", f"source changed: {source.video_id}"
            )
        source_by_video[source.video_id] = source
    for card_row in freeze.review_cards:
        card_path = Path(str(card_row["path"]))
        card = _card_payload(card_path)
        source = source_by_video.get(card.video_id)
        if source is None:
            raise EvaluationError(
                "REVIEW_CARD_SOURCE_MISMATCH", f"unknown card video: {card.video_id}"
            )
        validate_review_card(card, source)
        if _sha256_file(card_path) != card_row.get("sha256"):
            raise EvaluationError(
                "SEMANTIC_V2_MANIFEST_STALE", f"review card changed: {card.video_id}"
            )
        card_by_video[card.video_id] = card
    runtime_row = freeze.runtime
    runtime_path = Path(str(runtime_row.get("module", "")))
    if not runtime_path.is_file() or _sha256_file(runtime_path) != runtime_row.get("sha256"):
        raise EvaluationError("SEMANTIC_V2_MANIFEST_STALE", "planning runtime changed after freeze")
    evaluator_row = freeze.evaluator
    evaluator_path = Path(str(evaluator_row.get("module", "")))
    if not evaluator_path.is_file() or _sha256_file(evaluator_path) != evaluator_row.get("sha256"):
        raise EvaluationError("SEMANTIC_V2_MANIFEST_STALE", "evaluator changed after freeze")

    revision_root = output_root.resolve() / freeze.revision_id
    try:
        revision_root.mkdir(parents=True, exist_ok=False)
    except FileExistsError as exc:
        raise EvaluationError(
            "EVALUATION_OUTPUT_EXISTS", f"product evaluation already exists: {revision_root}"
        ) from exc
    run_rows: list[dict[str, object]] = []
    artifact_root = Path(freeze.artifact_root)
    for declaration in freeze.runs:
        source = source_by_video[declaration.video_id]
        card = card_by_video[declaration.video_id]
        rubric_path = revision_root / "rubrics" / f"{declaration.run_id}.json"
        run_rows.append(
            _semantic_v2_product_run_row(
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

    structure_signatures = {
        str(row["run_id"]): row["deterministic"]["structure_signature"]
        for row in run_rows
        if isinstance(row.get("deterministic"), dict)
        and row["deterministic"].get("structure_signature") is not None
    }
    by_video = {
        video_id: {
            "run_id": next(row["run_id"] for row in run_rows if row["video_id"] == video_id),
            "technical_status": next(
                row["technical_status"] for row in run_rows if row["video_id"] == video_id
            ),
            "structure_signature": next(
                row["deterministic"]["structure_signature"]
                for row in run_rows
                if row["video_id"] == video_id
            ),
            "report_present": next(
                row["deterministic"]["report_present"]
                for row in run_rows
                if row["video_id"] == video_id
            ),
            "desktop_screenshot_present": next(
                row["deterministic"]["desktop_screenshot_present"]
                for row in run_rows
                if row["video_id"] == video_id
            ),
            "mobile_screenshot_present": next(
                row["deterministic"]["mobile_screenshot_present"]
                for row in run_rows
                if row["video_id"] == video_id
            ),
        }
        for video_id, _, _ in FIXED_SOURCES
    }
    all_execution_valid = all(
        bool(row["deterministic"]["execution_valid"]) for row in run_rows
    )
    all_screenshots = all(
        bool(row["deterministic"]["desktop_screenshot_present"])
        and bool(row["deterministic"]["mobile_screenshot_present"])
        for row in run_rows
    )
    observed_calls = sum(int(row.get("provider_calls", 0)) for row in run_rows)
    technical_status = "PASS" if all_execution_valid else "FAILED"
    if all_execution_valid and all_screenshots:
        stop_state = "READY_FOR_OWNER_V1A_REVIEW"
        conclusion = "PROTOTYPE_REPORTS_READY"
    elif all_execution_valid:
        stop_state = "PROTOTYPE_EXECUTION_INCONCLUSIVE"
        conclusion = "SCREENSHOT_EVIDENCE_PENDING"
    else:
        failed_rows = [
            row for row in run_rows if row["technical_status"] != "PASS"
        ]
        transport_failure_categories = {
            "PROVIDER_ERROR",
            "MODEL_OUTPUT_INCOMPLETE",
            "MODEL_OUTPUT_PARSE_ERROR",
        }
        has_transport_failure = any(
            category in transport_failure_categories
            for row in failed_rows
            for category in row.get("technical_failures", [])
        )
        if has_transport_failure:
            stop_state = "PROTOTYPE_EXECUTION_INCONCLUSIVE"
        elif any(
            "Topic Map" in error or "report plan" in error
            for row in failed_rows
            for error in row["deterministic"].get("errors", [])
        ):
            stop_state = "PROTOTYPE_CONTENT_INSUFFICIENT"
        else:
            stop_state = "PROTOTYPE_SET_INVALID"
        conclusion = "TECHNICAL_EXECUTION_FAILURE"
    cross_video = {
        "schema_version": "visual-report-semantic-v2-cross-video-comparison.v1a",
        "videos": by_video,
        "structure_signatures": structure_signatures,
        "all_structure_signatures_identical": (
            len(set(structure_signatures.values())) == 1 if structure_signatures else None
        ),
        "comparison_status": "PENDING_OWNER_REVIEW",
        "owner_questions": [
            "Do topic boundaries and summaries capture each product video's actual narrative?",
            "Does each report prioritize the right content for its video rather than "
            "a shared template?",
            "Are desktop and mobile layouts readable at the captured viewports?",
        ],
    }
    cross_video_path = revision_root / "cross-video-comparison.json"
    _write_new_json(cross_video_path, cross_video)
    aggregate = {
        "schema_version": SEMANTIC_V2_PRODUCT_EVALUATION_SCHEMA_VERSION,
        "evaluator_version": SEMANTIC_V2_PRODUCT_EVALUATOR_VERSION,
        "manifest_path": str(manifest_path.resolve()),
        "manifest_revision_id": freeze.revision_id,
        "technical_status": technical_status,
        "stop_state": stop_state,
        "conclusion": conclusion,
        "quality_status": "PENDING_OWNER_REVIEW",
        "denominator": {
            "declared_videos": 3,
            "declared_runs": 3,
            "base_provider_calls": 6,
            "maximum_provider_calls": 9,
            "observed_provider_calls": observed_calls,
            "observed_model_calls": sum(int(row.get("model_calls", 0)) for row in run_rows),
            "formal_six_run_measurement": False,
        },
        "provider": freeze.provider,
        "runs": run_rows,
        "by_video": by_video,
        "cross_video_comparison": str(cross_video_path),
        "technical_vs_content": {
            "technical_execution": technical_status,
            "content_quality": "PENDING_OWNER_REVIEW",
            "visual_quality": "PENDING_OWNER_REVIEW" if all_screenshots else "NOT_AVAILABLE",
        },
        "owner_action": (
            "Owner must review the retained Topic Maps, plans, reports, screenshots, "
            "and pending rubrics; "
            "this artifact is not Owner acceptance."
        ),
        "generated_at": _now(),
    }
    aggregate_path = revision_root / "aggregate.json"
    _write_new_json(aggregate_path, aggregate)
    package = {
        "schema_version": SEMANTIC_V2_PRODUCT_PACKAGE_SCHEMA_VERSION,
        "manifest_path": str(manifest_path.resolve()),
        "manifest_revision_id": freeze.revision_id,
        "status": stop_state,
        "conclusion": conclusion,
        "review_status": "PENDING_OWNER_REVIEW",
        "sources": list(freeze.sources),
        "review_cards": list(freeze.review_cards),
        "runs": [
            {
                "run_id": row["run_id"],
                "video_id": row["video_id"],
                "artifacts": row["review_artifacts"],
                "technical_status": row["technical_status"],
                "content_review_status": row["content_review_status"],
                "visual_review_status": row["visual_review_status"],
                "deterministic": row["deterministic"],
                "rubric": row["human_rubric"],
            }
            for row in run_rows
        ],
        "cross_video_comparison": str(cross_video_path),
        "aggregate": str(aggregate_path),
        "owner_gate": "READY_FOR_OWNER_V1A_REVIEW only; no acceptance recorded",
        "generated_at": _now(),
    }
    _write_new_json(revision_root / "review-package.json", package)
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
    "freeze_semantic_v2_product_prototype",
    "derive_semantic_v2_product_review_manifest",
    "load_semantic_v2_product_freeze",
    "load_measurement",
    "review_semantic_v2_product_prototype",
    "validate_review_card",
]
