"""The V1-A foreground source, provider, run, and artifact boundary."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import re
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any, Callable, Mapping
from urllib.parse import urlsplit

from dotenv import load_dotenv
from openai import APITimeoutError, OpenAI
from pydantic import ValidationError

from video_evidence_agent.schemas import VideoSegment
from video_evidence_agent.segments import SegmentBuildError, validate_video_segments

from .planning import (
    CALL_SCHEMA_VERSION,
    COMPILER_VERSION,
    MAPPER_PROMPT_VERSION,
    MAPPER_SYSTEM_INSTRUCTION,
    MAX_OUTPUT_TOKENS,
    PLAN_PROPOSAL_SCHEMA_VERSION,
    PLANNER_PROMPT_VERSION,
    PLANNER_SYSTEM_INSTRUCTION,
    SEMANTIC_V2_CALL_SCHEMA_VERSION,
    SEMANTIC_V2_COMPILER_VERSION,
    SEMANTIC_V2_MAPPER_PROMPT_VERSION,
    SEMANTIC_V2_MAPPER_SYSTEM_INSTRUCTION,
    SEMANTIC_V2_MAX_OUTPUT_TOKENS,
    SEMANTIC_V2_MODEL,
    SEMANTIC_V2_NORMALIZATION_SCHEMA_VERSION,
    SEMANTIC_V2_PLAN_PROPOSAL_SCHEMA_VERSION,
    SEMANTIC_V2_PLANNER_PROMPT_VERSION,
    SEMANTIC_V2_PLANNER_SYSTEM_INSTRUCTION,
    SEMANTIC_V2_REASONING_EFFORT,
    SEMANTIC_V2_THINKING_MODE,
    SEMANTIC_V2_TOPIC_MAP_SCHEMA_VERSION,
    SEMANTIC_V2_TOPIC_PROPOSAL_SCHEMA_VERSION,
    THINKING_MODE,
    TOPIC_MAP_SCHEMA_VERSION,
    TOPIC_PROPOSAL_SCHEMA_VERSION,
    PlanningError,
    ReportPlanProposal,
    SemanticV2TopicMap,
    TopicMap,
    TopicMapProposal,
    bind_topic_map,
    compile_report_plan,
    compile_semantic_v2_report_plan,
    mapper_payload,
    normalize_semantic_v2_plan_proposal,
    normalize_semantic_v2_topic_proposal,
    planner_payload,
    resolve_semantic_v2_topic_map,
    semantic_v2_mapper_payload,
    semantic_v2_planner_payload,
    stable_json,
    validate_transcript_envelope,
)
from .renderer import RenderError, render_report

RUN_SCHEMA_VERSION = "visual-report-planning-run.v1a-prototype"
EVENT_SCHEMA_VERSION = "visual-report-planning-event.v1a-prototype"
SEMANTIC_V2_RUN_SCHEMA_VERSION = "visual-report-planning-run.v1a-semantic-v2"
SEMANTIC_V2_EVENT_SCHEMA_VERSION = "visual-report-planning-event.v1a-semantic-v2"
API_SURFACE = "responses"
RESPONSE_MODE = "json_schema"
SCHEMA_MECHANISM = "responses.text.format.json_schema"
SEMANTIC_V2_API_SURFACE = "chat_completions"
SEMANTIC_V2_RESPONSE_MODE = "json_object"
SEMANTIC_V2_SCHEMA_MECHANISM = "chat.completions.response_format.json_object"
SEMANTIC_V2_PROVIDER_ENDPOINT = "https://api.deepseek.com"
REASONING_EFFORT = "none"
TEMPERATURE = 0


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _atomic_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_path = Path(handle.name)
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
    except OSError as exc:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
        raise PlanningError("OUTPUT_IO_ERROR", f"cannot write {path}") from exc


def _append_jsonl(path: Path, payload: object) -> None:
    try:
        with path.open("a", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, separators=(",", ":"))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
    except OSError as exc:
        raise PlanningError("OUTPUT_IO_ERROR", f"cannot append {path}") from exc


@dataclass(frozen=True)
class SourceSnapshot:
    manifest_path: Path
    segments_path: Path
    manifest_sha256: str
    segments_sha256: str
    video_id: str
    title: str
    duration_ms: int
    source_url: str
    attribution: str
    segments: tuple[VideoSegment, ...]

    @property
    def video_payload(self) -> dict[str, object]:
        return {
            "video_id": self.video_id,
            "title": self.title,
            "duration_ms": self.duration_ms,
            "language": "zh",
        }


def _title_from_attribution(attribution: str, video_id: str) -> str:
    match = re.search(r"《([^》]+)》", attribution)
    return match.group(1).strip() if match else video_id


def load_source(manifest_path: Path, segments_path: Path) -> SourceSnapshot:
    try:
        manifest_bytes = manifest_path.read_bytes()
        segments_bytes = segments_path.read_bytes()
    except FileNotFoundError as exc:
        raise PlanningError("SOURCE_NOT_FOUND", "manifest or segments file not found") from exc
    except OSError as exc:
        raise PlanningError("SOURCE_NOT_FOUND", "manifest or segments file cannot be read") from exc
    try:
        manifest = json.loads(manifest_bytes.decode("utf-8"))
        rows = [
            json.loads(line) for line in segments_bytes.decode("utf-8").splitlines() if line.strip()
        ]
        segments = [VideoSegment.model_validate(row) for row in rows]
        validate_video_segments(segments)
    except (UnicodeDecodeError, json.JSONDecodeError, ValidationError, SegmentBuildError) as exc:
        raise PlanningError("TRANSCRIPT_SCHEMA_ERROR", str(exc)) from exc
    if not isinstance(manifest, dict):
        raise PlanningError("MANIFEST_MISMATCH", "manifest must be an object")
    source = manifest.get("source")
    segmenting = manifest.get("segmenting")
    if not isinstance(source, dict) or not isinstance(segmenting, dict):
        raise PlanningError("MANIFEST_MISMATCH", "manifest source/segmenting is missing")
    video_id = manifest.get("video_id")
    duration_ms = source.get("duration_ms")
    if not isinstance(video_id, str) or not video_id or not segments:
        raise PlanningError("MANIFEST_MISMATCH", "manifest video_id or transcript is missing")
    if video_id != segments[0].video_id:
        raise PlanningError("MANIFEST_MISMATCH", "manifest and transcript video_id differ")
    if not isinstance(duration_ms, int) or duration_ms <= 0:
        raise PlanningError("MANIFEST_MISMATCH", "manifest duration_ms is invalid")
    if segmenting.get("segment_count") != len(segments):
        raise PlanningError("MANIFEST_MISMATCH", "manifest segment_count differs")
    if any(segment.end_ms > duration_ms for segment in segments):
        raise PlanningError("MANIFEST_MISMATCH", "transcript exceeds manifest duration")
    source_url = source.get("origin_url")
    attribution = source.get("attribution")
    if not isinstance(source_url, str) or not source_url.strip():
        raise PlanningError("MANIFEST_MISMATCH", "manifest origin_url is missing")
    if not isinstance(attribution, str) or not attribution.strip():
        raise PlanningError("MANIFEST_MISMATCH", "manifest attribution is missing")
    validate_transcript_envelope(segments)
    return SourceSnapshot(
        manifest_path=manifest_path.resolve(),
        segments_path=segments_path.resolve(),
        manifest_sha256=_sha256_bytes(manifest_bytes),
        segments_sha256=_sha256_bytes(segments_bytes),
        video_id=video_id,
        title=_title_from_attribution(attribution, video_id),
        duration_ms=duration_ms,
        source_url=source_url,
        attribution=attribution,
        segments=tuple(segments),
    )


@dataclass(frozen=True)
class PlanningConfig:
    provider_label: str
    model: str
    timeout_seconds: float
    credential_present: bool
    response_mode: str = RESPONSE_MODE
    temperature: int = TEMPERATURE
    temperature_stability_evidence: str = "not_applicable"
    thinking_mode: str = THINKING_MODE
    output_token_limit: int = MAX_OUTPUT_TOKENS
    sdk_max_retries: int = 0
    sdk_version: str = "unknown"
    api_surface: str = API_SURFACE
    schema_mechanism: str = SCHEMA_MECHANISM
    reasoning_effort: str = REASONING_EFFORT
    strategy_id: str | None = None
    strategy_manifest_sha256: str | None = None
    model_version: str | None = None
    mapper_prompt_version: str = MAPPER_PROMPT_VERSION
    planner_prompt_version: str = PLANNER_PROMPT_VERSION
    topic_proposal_schema: str = TOPIC_PROPOSAL_SCHEMA_VERSION
    topic_map_schema: str = TOPIC_MAP_SCHEMA_VERSION
    plan_proposal_schema: str = PLAN_PROPOSAL_SCHEMA_VERSION
    compiler_version: str = COMPILER_VERSION

    def public_snapshot(self) -> dict[str, object]:
        return {
            "provider": self.provider_label,
            "model": self.model,
            "timeout_seconds": self.timeout_seconds,
            "credential_present": self.credential_present,
            "response_mode": self.response_mode,
            "api_surface": self.api_surface,
            "schema_mechanism": self.schema_mechanism,
            "temperature": self.temperature,
            "temperature_stability_evidence": self.temperature_stability_evidence,
            "thinking_mode": self.thinking_mode,
            "reasoning_effort": self.reasoning_effort,
            "output_token_limit": self.output_token_limit,
            "sdk_max_retries": self.sdk_max_retries,
            "sdk_version": self.sdk_version,
            "strategy_id": self.strategy_id,
            "strategy_manifest_sha256": self.strategy_manifest_sha256,
            "model_version": self.model_version,
            "mapper_prompt_version": self.mapper_prompt_version,
            "planner_prompt_version": self.planner_prompt_version,
            "topic_proposal_schema": self.topic_proposal_schema,
            "topic_map_schema": self.topic_map_schema,
            "plan_proposal_schema": self.plan_proposal_schema,
            "compiler_version": self.compiler_version,
        }


def _provider_label(base_url: str) -> str:
    if not base_url:
        return "openai"
    parsed = urlsplit(base_url)
    if parsed.scheme and parsed.hostname:
        port = f":{parsed.port}" if parsed.port else ""
        return f"{parsed.scheme}://{parsed.hostname}{port}"
    return "openai-compatible-custom-endpoint"


class ProviderCallError(RuntimeError):
    def __init__(
        self,
        category: str,
        message: str,
        latency_ms: int,
        *,
        usage: dict[str, Any] | None = None,
        finish_reason: str | None = None,
        content_present: bool = False,
        content_bytes: int = 0,
        content_sha256: str | None = None,
        retryable: bool = False,
    ) -> None:
        self.category = category
        self.latency_ms = latency_ms
        self.usage = usage or {}
        self.finish_reason = finish_reason
        self.content_present = content_present
        self.content_bytes = content_bytes
        self.content_sha256 = content_sha256
        self.retryable = retryable
        super().__init__(message)


@dataclass(frozen=True)
class ProviderResult:
    raw_text: str
    usage: dict[str, Any]
    latency_ms: int
    finish_reason: str | None = None
    content_present: bool = True
    content_bytes: int = 0
    content_sha256: str | None = None


class OpenAIPlanningProvider:
    def __init__(self, client: OpenAI, config: PlanningConfig) -> None:
        self.client = client
        self.config = config

    @classmethod
    def from_environment(
        cls, strategy: Mapping[str, object] | None = None
    ) -> "OpenAIPlanningProvider":
        if strategy is None:
            raise PlanningError(
                "CONFIGURATION_ERROR",
                "a frozen provider conformance strategy is required for real runs",
            )
        load_dotenv(Path(__file__).resolve().parents[3] / ".env", override=False)
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        base_url = os.getenv("OPENAI_BASE_URL", "").strip()
        try:
            timeout_seconds = float(os.getenv("VISUAL_REPORT_TIMEOUT_SECONDS", "120"))
        except ValueError as exc:
            raise PlanningError(
                "CONFIGURATION_ERROR", "VISUAL_REPORT_TIMEOUT_SECONDS must be numeric"
            ) from exc
        if not api_key:
            raise PlanningError("CONFIGURATION_ERROR", "OPENAI_API_KEY is required")
        if timeout_seconds <= 0:
            raise PlanningError(
                "CONFIGURATION_ERROR", "VISUAL_REPORT_TIMEOUT_SECONDS must be positive"
            )
        strategy_id = strategy.get("strategy_id")
        strategy_config = strategy.get("config")
        if not isinstance(strategy_id, str) or not strategy_id:
            raise PlanningError("CONFIGURATION_ERROR", "strategy_id is missing")
        if strategy.get("eligibility") != "ELIGIBLE" or not isinstance(strategy_config, dict):
            raise PlanningError("CONFIGURATION_ERROR", "provider strategy is not eligible")
        expected = {
            "provider": strategy_config.get("provider"),
            "timeout_seconds": strategy_config.get("timeout_seconds"),
            "api_surface": strategy_config.get("api_surface"),
            "response_mode": strategy_config.get("response_mode"),
            "schema_mechanism": strategy_config.get("schema_mechanism"),
            "temperature": strategy_config.get("temperature"),
            "thinking_mode": strategy_config.get("thinking_mode"),
            "reasoning_effort": strategy_config.get("reasoning_effort"),
            "output_token_limit": strategy_config.get("output_token_limit"),
            "sdk_max_retries": strategy_config.get("sdk_max_retries"),
        }
        if expected["provider"] != _provider_label(base_url):
            raise PlanningError(
                "CONFIGURATION_ERROR", "provider endpoint differs from frozen strategy"
            )
        if expected["timeout_seconds"] != timeout_seconds:
            raise PlanningError("CONFIGURATION_ERROR", "timeout differs from frozen strategy")
        if expected["api_surface"] != API_SURFACE:
            raise PlanningError("CONFIGURATION_ERROR", "strategy must use Responses API")
        if expected["response_mode"] != RESPONSE_MODE:
            raise PlanningError("CONFIGURATION_ERROR", "strategy must use native JSON Schema")
        if expected["schema_mechanism"] != SCHEMA_MECHANISM:
            raise PlanningError("CONFIGURATION_ERROR", "strategy schema mechanism is not supported")
        if (
            expected["temperature"] != TEMPERATURE
            or expected["reasoning_effort"] != REASONING_EFFORT
        ):
            raise PlanningError("CONFIGURATION_ERROR", "strategy sampling controls differ")
        if expected["thinking_mode"] != THINKING_MODE:
            raise PlanningError("CONFIGURATION_ERROR", "strategy thinking mode differs")
        if expected["output_token_limit"] != MAX_OUTPUT_TOKENS:
            raise PlanningError("CONFIGURATION_ERROR", "strategy output limit differs")
        if expected["sdk_max_retries"] != 0:
            raise PlanningError("CONFIGURATION_ERROR", "strategy SDK retries must be zero")
        model = strategy.get("model")
        if not isinstance(model, str) or not model:
            raise PlanningError("CONFIGURATION_ERROR", "strategy model is missing")
        options: dict[str, Any] = {
            "api_key": api_key,
            "timeout": timeout_seconds,
            "max_retries": 0,
        }
        if base_url:
            options["base_url"] = base_url
        config = PlanningConfig(
            provider_label=_provider_label(base_url),
            model=model,
            timeout_seconds=timeout_seconds,
            credential_present=True,
            response_mode=RESPONSE_MODE,
            api_surface=API_SURFACE,
            schema_mechanism=SCHEMA_MECHANISM,
            reasoning_effort=REASONING_EFFORT,
            strategy_id=strategy_id,
            strategy_manifest_sha256=(
                str(strategy["strategy_manifest_sha256"])
                if strategy.get("strategy_manifest_sha256")
                else None
            ),
            model_version=(
                str(strategy["model_version"]) if strategy.get("model_version") else None
            ),
            sdk_version=importlib.metadata.version("openai"),
        )
        expected_sdk_version = strategy_config.get("sdk_version")
        if expected_sdk_version != config.sdk_version:
            raise PlanningError(
                "CONFIGURATION_ERROR", "OpenAI SDK version differs from frozen strategy"
            )
        return cls(OpenAI(**options), config)

    @staticmethod
    def _schema_name(stage: str) -> str:
        names = {
            "topic_mapper": "v1a_topic_map_proposal",
            "report_planner": "v1a_report_plan_proposal",
        }
        try:
            return names[stage]
        except KeyError as exc:
            raise ProviderCallError("CONFIGURATION_ERROR", "unknown planning stage", 0) from exc

    @staticmethod
    def _usage(response: object) -> dict[str, Any]:
        usage = getattr(response, "usage", None)
        if usage is None:
            return {}
        try:
            candidate = usage.model_dump(mode="json")
            if isinstance(candidate, dict):
                return candidate
        except (AttributeError, TypeError, ValueError):
            pass
        return {}

    @staticmethod
    def _finish_reason(response: object) -> str | None:
        incomplete = getattr(response, "incomplete_details", None)
        reason = getattr(incomplete, "reason", None)
        if isinstance(reason, str) and reason:
            return reason
        status = getattr(response, "status", None)
        return status if isinstance(status, str) and status != "completed" else None

    @staticmethod
    def _output_text(response: object) -> str | None:
        direct = getattr(response, "output_text", None)
        if isinstance(direct, str) and direct:
            return direct
        output = getattr(response, "output", None)
        if not isinstance(output, list):
            return None
        chunks: list[str] = []
        for item in output:
            content = getattr(item, "content", None)
            if not isinstance(content, list):
                continue
            for part in content:
                text = getattr(part, "text", None)
                if isinstance(text, str):
                    chunks.append(text)
        joined = "".join(chunks)
        return joined or None

    def complete(
        self, stage: str, system_instruction: str, payload: dict[str, object]
    ) -> ProviderResult:
        started = perf_counter()
        output_contract = payload.get("output_contract")
        schema = output_contract.get("json_schema") if isinstance(output_contract, dict) else None
        if not isinstance(schema, dict):
            raise ProviderCallError("CONFIGURATION_ERROR", "native response schema is missing", 0)
        try:
            response = self.client.responses.create(
                model=self.config.model,
                temperature=TEMPERATURE,
                max_output_tokens=self.config.output_token_limit,
                reasoning={"effort": self.config.reasoning_effort},
                instructions=system_instruction,
                input=stable_json(payload),
                text={
                    "format": {
                        "type": RESPONSE_MODE,
                        "name": self._schema_name(stage),
                        "schema": schema,
                    }
                },
            )
        except (TimeoutError, APITimeoutError) as exc:
            latency_ms = round((perf_counter() - started) * 1000)
            raise ProviderCallError(
                "PROVIDER_TIMEOUT", "provider request timed out", latency_ms
            ) from exc
        except Exception as exc:
            latency_ms = round((perf_counter() - started) * 1000)
            raise ProviderCallError(
                "PROVIDER_ERROR", f"provider request failed: {type(exc).__name__}", latency_ms
            ) from exc
        latency_ms = round((perf_counter() - started) * 1000)
        usage = self._usage(response)
        finish_reason = self._finish_reason(response)
        content = self._output_text(response)
        content_present = isinstance(content, str) and bool(content)
        content_bytes = len(content.encode("utf-8")) if isinstance(content, str) else 0
        content_sha256 = (
            _sha256_bytes(content.encode("utf-8")) if isinstance(content, str) else None
        )
        if not content_present:
            raise ProviderCallError(
                "PROVIDER_ERROR",
                "provider returned no message content",
                latency_ms,
                usage=usage,
                finish_reason=finish_reason,
                content_present=False,
                content_bytes=content_bytes,
                content_sha256=content_sha256,
            )
        return ProviderResult(
            raw_text=content,
            usage=usage,
            latency_ms=latency_ms,
            finish_reason=finish_reason,
            content_present=content_present,
            content_bytes=content_bytes,
            content_sha256=content_sha256,
        )


def semantic_v2_chat_completion_request(
    stage: str,
    system_instruction: str,
    payload: dict[str, object],
    config: PlanningConfig,
) -> dict[str, object]:
    """Build the exact non-secret Chat Completions request for semantic v2."""
    return {
        "model": config.model,
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": stable_json(payload)},
        ],
        "temperature": config.temperature,
        "max_tokens": config.output_token_limit,
        "response_format": {"type": config.response_mode},
        "reasoning_effort": config.reasoning_effort,
        "extra_body": {"thinking": {"type": config.thinking_mode}},
    }


def _validate_semantic_v2_request_config(config: PlanningConfig) -> None:
    expected = {
        "provider_label": SEMANTIC_V2_PROVIDER_ENDPOINT,
        "model": SEMANTIC_V2_MODEL,
        "response_mode": SEMANTIC_V2_RESPONSE_MODE,
        "api_surface": SEMANTIC_V2_API_SURFACE,
        "schema_mechanism": SEMANTIC_V2_SCHEMA_MECHANISM,
        "temperature": TEMPERATURE,
        "temperature_stability_evidence": "excluded_in_thinking_mode",
        "thinking_mode": SEMANTIC_V2_THINKING_MODE,
        "reasoning_effort": SEMANTIC_V2_REASONING_EFFORT,
        "output_token_limit": SEMANTIC_V2_MAX_OUTPUT_TOKENS,
        "sdk_max_retries": 0,
    }
    for field_name, expected_value in expected.items():
        if getattr(config, field_name) != expected_value:
            raise ProviderCallError(
                "CONFIGURATION_ERROR",
                f"semantic-v2 request config differs from frozen value: {field_name}",
                0,
            )


class OpenAISemanticV2PlanningProvider:
    """The current DeepSeek-compatible Chat Completions provider seam."""

    def __init__(self, client: OpenAI, config: PlanningConfig) -> None:
        self.client = client
        self.config = config

    @classmethod
    def from_environment(cls) -> "OpenAISemanticV2PlanningProvider":
        load_dotenv(Path(__file__).resolve().parents[3] / ".env", override=False)
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        base_url = os.getenv("OPENAI_BASE_URL", "").strip()
        model = os.getenv("VISUAL_REPORT_MODEL", "").strip()
        if not api_key:
            raise PlanningError("CONFIGURATION_ERROR", "OPENAI_API_KEY is required")
        if base_url.rstrip("/") != SEMANTIC_V2_PROVIDER_ENDPOINT:
            raise PlanningError(
                "CONFIGURATION_ERROR",
                "OPENAI_BASE_URL must be https://api.deepseek.com for semantic-v2",
            )
        if not model:
            raise PlanningError("CONFIGURATION_ERROR", "VISUAL_REPORT_MODEL is required")
        if model != SEMANTIC_V2_MODEL:
            raise PlanningError(
                "CONFIGURATION_ERROR",
                f"VISUAL_REPORT_MODEL must be {SEMANTIC_V2_MODEL} for semantic-v2",
            )
        try:
            timeout_seconds = float(os.getenv("VISUAL_REPORT_TIMEOUT_SECONDS", "120"))
        except ValueError as exc:
            raise PlanningError(
                "CONFIGURATION_ERROR", "VISUAL_REPORT_TIMEOUT_SECONDS must be numeric"
            ) from exc
        if timeout_seconds <= 0:
            raise PlanningError(
                "CONFIGURATION_ERROR", "VISUAL_REPORT_TIMEOUT_SECONDS must be positive"
            )
        options: dict[str, Any] = {
            "api_key": api_key,
            "timeout": timeout_seconds,
            "max_retries": 0,
        }
        if base_url:
            options["base_url"] = base_url
        config = PlanningConfig(
            provider_label=_provider_label(base_url),
            model=model,
            timeout_seconds=timeout_seconds,
            credential_present=True,
            response_mode=SEMANTIC_V2_RESPONSE_MODE,
            api_surface=SEMANTIC_V2_API_SURFACE,
            schema_mechanism=SEMANTIC_V2_SCHEMA_MECHANISM,
            temperature_stability_evidence="excluded_in_thinking_mode",
            thinking_mode=SEMANTIC_V2_THINKING_MODE,
            output_token_limit=SEMANTIC_V2_MAX_OUTPUT_TOKENS,
            reasoning_effort=SEMANTIC_V2_REASONING_EFFORT,
            mapper_prompt_version=SEMANTIC_V2_MAPPER_PROMPT_VERSION,
            planner_prompt_version=SEMANTIC_V2_PLANNER_PROMPT_VERSION,
            topic_proposal_schema=SEMANTIC_V2_TOPIC_PROPOSAL_SCHEMA_VERSION,
            topic_map_schema=SEMANTIC_V2_TOPIC_MAP_SCHEMA_VERSION,
            plan_proposal_schema=SEMANTIC_V2_PLAN_PROPOSAL_SCHEMA_VERSION,
            compiler_version=SEMANTIC_V2_COMPILER_VERSION,
            sdk_version=importlib.metadata.version("openai"),
        )
        return cls(OpenAI(**options), config)

    @staticmethod
    def _usage(response: object) -> dict[str, Any]:
        usage = getattr(response, "usage", None)
        if usage is None:
            return {}
        try:
            candidate = usage.model_dump(mode="json")
            if isinstance(candidate, dict):
                return candidate
        except (AttributeError, TypeError, ValueError):
            pass
        if isinstance(usage, dict):
            return dict(usage)
        return {}

    @staticmethod
    def _status_code(error: BaseException) -> int | None:
        value = getattr(error, "status_code", None)
        if isinstance(value, int):
            return value
        response = getattr(error, "response", None)
        value = getattr(response, "status_code", None)
        return value if isinstance(value, int) else None

    @classmethod
    def _retryable_transport_error(cls, error: BaseException) -> bool:
        name = type(error).__name__.lower()
        status_code = cls._status_code(error)
        return (
            isinstance(error, (TimeoutError, APITimeoutError))
            or "connection" in name
            or "timeout" in name
            or "rate" in name
            or status_code == 429
            or (status_code is not None and status_code >= 500)
        )

    def complete(
        self, stage: str, system_instruction: str, payload: dict[str, object]
    ) -> ProviderResult:
        if stage not in {"topic_mapper", "report_planner"}:
            raise ProviderCallError("CONFIGURATION_ERROR", "unknown planning stage", 0)
        _validate_semantic_v2_request_config(self.config)
        request = semantic_v2_chat_completion_request(
            stage, system_instruction, payload, self.config
        )
        started = perf_counter()
        try:
            response = self.client.chat.completions.create(**request)
        except Exception as exc:
            latency_ms = round((perf_counter() - started) * 1000)
            category = (
                "PROVIDER_TIMEOUT"
                if isinstance(exc, (TimeoutError, APITimeoutError))
                else "PROVIDER_ERROR"
            )
            raise ProviderCallError(
                category,
                f"provider request failed: {type(exc).__name__}",
                latency_ms,
                retryable=self._retryable_transport_error(exc),
            ) from exc
        latency_ms = round((perf_counter() - started) * 1000)
        usage = self._usage(response)
        choices = getattr(response, "choices", None)
        choice = choices[0] if isinstance(choices, list) and choices else None
        message = getattr(choice, "message", None)
        content = getattr(message, "content", None)
        finish_reason = getattr(choice, "finish_reason", None)
        if not isinstance(content, str):
            content = None
        content_bytes = len(content.encode("utf-8")) if content is not None else 0
        content_sha256 = _sha256_bytes(content.encode("utf-8")) if content is not None else None
        if not content:
            raise ProviderCallError(
                "PROVIDER_ERROR",
                "provider returned no message content",
                latency_ms,
                usage=usage,
                finish_reason=finish_reason if isinstance(finish_reason, str) else None,
                content_present=False,
                content_bytes=content_bytes,
                content_sha256=content_sha256,
                retryable=True,
            )
        return ProviderResult(
            raw_text=content,
            usage=usage,
            latency_ms=latency_ms,
            finish_reason=finish_reason if isinstance(finish_reason, str) else None,
            content_present=True,
            content_bytes=content_bytes,
            content_sha256=content_sha256,
        )


class RunRecorder:
    def __init__(
        self,
        run_id: str,
        run_dir: Path,
        *,
        schema_version: str = RUN_SCHEMA_VERSION,
        event_schema_version: str = EVENT_SCHEMA_VERSION,
        call_schema_version: str = CALL_SCHEMA_VERSION,
    ) -> None:
        self.run_id = run_id
        self.run_dir = run_dir
        self.run_path = run_dir / "run.json"
        self.events_path = run_dir / "events.jsonl"
        self.calls_path = run_dir / "model-calls.jsonl"
        self.event_schema_version = event_schema_version
        self.call_schema_version = call_schema_version
        self.payload: dict[str, Any] = {
            "schema_version": schema_version,
            "run_id": run_id,
            "state": "CREATED",
            "created_at": _now(),
            "updated_at": _now(),
            "provider_calls": 0,
            "model_calls": 0,
            "latency_ms_total": 0,
            "latency_ms": [],
            "usage": {},
            "cost": "unavailable",
            "artifacts": {},
            "error": None,
        }
        _atomic_json(self.run_path, self.payload)
        self.event("CREATED")

    @classmethod
    def create(
        cls,
        output_root: Path,
        run_id: str,
        *,
        schema_version: str = RUN_SCHEMA_VERSION,
        event_schema_version: str = EVENT_SCHEMA_VERSION,
        call_schema_version: str = CALL_SCHEMA_VERSION,
    ) -> "RunRecorder":
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}", run_id):
            raise PlanningError("CONFIGURATION_ERROR", "run_id must be a safe 1-80 character slug")
        run_dir = output_root.resolve() / run_id
        try:
            run_dir.mkdir(parents=True, exist_ok=False)
        except FileExistsError as exc:
            raise PlanningError(
                "OUTPUT_IO_ERROR", f"run directory already exists: {run_id}"
            ) from exc
        except OSError as exc:
            raise PlanningError("OUTPUT_IO_ERROR", "cannot create run directory") from exc
        return cls(
            run_id,
            run_dir,
            schema_version=schema_version,
            event_schema_version=event_schema_version,
            call_schema_version=call_schema_version,
        )

    def save(self) -> None:
        self.payload["updated_at"] = _now()
        _atomic_json(self.run_path, self.payload)

    def event(self, state: str, **detail: object) -> None:
        _append_jsonl(
            self.events_path,
            {
                "schema_version": self.event_schema_version,
                "at": _now(),
                "state": state,
                **detail,
            },
        )

    def transition(self, state: str) -> None:
        if self.payload["state"] in {"FAILED", "CANCELLED", "RENDERED"}:
            raise PlanningError("OUTPUT_IO_ERROR", "terminal run state cannot advance")
        allowed: dict[str, set[str]] = {
            "CREATED": {"MAPPING"},
            "MAPPING": {"TOPIC_MAPPED"},
            "TOPIC_MAPPED": {"PLANNING"},
            "PLANNING": {"PLAN_VALIDATED"},
            "PLAN_VALIDATED": {"RENDERED"},
        }
        current = str(self.payload["state"])
        if state not in allowed.get(current, set()):
            raise PlanningError(
                "OUTPUT_IO_ERROR", f"invalid state transition: {current} -> {state}"
            )
        self.payload["state"] = state
        self.save()
        self.event(state)

    def configure(self, config: PlanningConfig, source: SourceSnapshot) -> None:
        self.payload["config"] = config.public_snapshot()
        self.payload["strategy_id"] = config.strategy_id
        self.payload["strategy_manifest_sha256"] = config.strategy_manifest_sha256
        self.payload["source"] = {
            "video_id": source.video_id,
            "manifest_path": str(source.manifest_path),
            "segments_path": str(source.segments_path),
            "manifest_sha256": source.manifest_sha256,
            "segments_sha256": source.segments_sha256,
            "segment_count": len(source.segments),
        }
        mapper_prompt_version = getattr(config, "mapper_prompt_version", MAPPER_PROMPT_VERSION)
        planner_prompt_version = getattr(config, "planner_prompt_version", PLANNER_PROMPT_VERSION)
        mapper_instruction = (
            SEMANTIC_V2_MAPPER_SYSTEM_INSTRUCTION
            if mapper_prompt_version == SEMANTIC_V2_MAPPER_PROMPT_VERSION
            else MAPPER_SYSTEM_INSTRUCTION
        )
        planner_instruction = (
            SEMANTIC_V2_PLANNER_SYSTEM_INSTRUCTION
            if planner_prompt_version == SEMANTIC_V2_PLANNER_PROMPT_VERSION
            else PLANNER_SYSTEM_INSTRUCTION
        )
        self.payload["prompt_sha256"] = {
            mapper_prompt_version: _sha256_bytes(mapper_instruction.encode("utf-8")),
            planner_prompt_version: _sha256_bytes(planner_instruction.encode("utf-8")),
        }
        self.save()

    def admit_call(self) -> None:
        self.payload["provider_calls"] += 1
        self.payload["model_calls"] += 1
        self.save()

    def record_call(
        self,
        *,
        stage: str,
        prompt_version: str,
        config: PlanningConfig,
        latency_ms: int,
        usage: dict[str, Any],
        schema_valid: bool,
        error_category: str | None = None,
        finish_reason: str | None = None,
        content_present: bool = False,
        content_bytes: int = 0,
        content_sha256: str | None = None,
        schema_name: str | None = None,
        schema_sha256: str | None = None,
        attempt: int | None = None,
        request_sha256: str | None = None,
        retry_of_attempt: int | None = None,
        retry_eligible: bool | None = None,
        retry_used: bool | None = None,
    ) -> None:
        call_payload: dict[str, object] = {
            "schema_version": self.call_schema_version,
                "at": _now(),
                "stage": stage,
                "provider": config.provider_label,
                "model": config.model,
                "prompt_version": prompt_version,
                "temperature": config.temperature,
                "timeout_seconds": config.timeout_seconds,
                "response_mode": config.response_mode,
                "api_surface": config.api_surface,
                "schema_mechanism": config.schema_mechanism,
                "sdk_max_retries": config.sdk_max_retries,
                "sdk_version": config.sdk_version,
                "thinking_mode": config.thinking_mode,
                "reasoning_effort": config.reasoning_effort,
                "output_token_limit": config.output_token_limit,
                "temperature_stability_evidence": getattr(
                    config, "temperature_stability_evidence", "not_applicable"
                ),
                "strategy_id": config.strategy_id,
                "strategy_manifest_sha256": config.strategy_manifest_sha256,
                "model_version": config.model_version,
                "schema_name": schema_name,
                "schema_sha256": schema_sha256,
                "latency_ms": latency_ms,
                "usage": usage,
                "schema_valid": schema_valid,
                "error_category": error_category,
                "finish_reason": finish_reason,
                "content_present": content_present,
                "content_bytes": content_bytes,
                "content_sha256": content_sha256,
        }
        if attempt is not None:
            call_payload["attempt"] = attempt
        if request_sha256 is not None:
            call_payload["request_sha256"] = request_sha256
        if retry_of_attempt is not None:
            call_payload["retry_of_attempt"] = retry_of_attempt
        if retry_eligible is not None:
            call_payload["retry_eligible"] = retry_eligible
        if retry_used is not None:
            call_payload["retry_used"] = retry_used
        _append_jsonl(self.calls_path, call_payload)
        aggregate = self.payload.setdefault("usage", {})
        for key, value in usage.items():
            if isinstance(value, int):
                aggregate[key] = int(aggregate.get(key, 0)) + value
        self.payload["latency_ms_total"] += latency_ms
        self.payload["latency_ms"].append({"stage": stage, "value": latency_ms})
        self.save()

    def artifact(self, name: str, path: Path) -> None:
        self.payload["artifacts"][name] = {"path": path.name, "sha256": _sha256_file(path)}
        self.save()

    def fail(self, error: PlanningError, state: str = "FAILED") -> None:
        if self.payload["state"] in {"FAILED", "CANCELLED", "RENDERED"}:
            return
        self.payload["state"] = state
        self.payload["error"] = {"category": error.category, "message": error.message}
        self.save()
        self.event(state, error_category=error.category)


@dataclass(frozen=True)
class PlanningRunSummary:
    run_id: str
    run_dir: Path
    state: str
    provider_calls: int
    model_calls: int
    section_count: int
    block_count: int
    report_path: Path


def _parse_response(raw_text: str, stage: str) -> dict[str, object]:
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise PlanningError("MODEL_OUTPUT_PARSE_ERROR", f"{stage} response is not JSON") from exc
    if not isinstance(payload, dict):
        raise PlanningError("MODEL_OUTPUT_PARSE_ERROR", f"{stage} response must be an object")
    return payload


def _write_raw(path: Path, raw_text: str) -> None:
    try:
        payload: object = json.loads(raw_text)
    except json.JSONDecodeError:
        payload = {"raw_text": raw_text}
    _atomic_json(path, payload)


def _call_stage(
    recorder: RunRecorder,
    provider: Any,
    *,
    stage: str,
    prompt_version: str,
    instruction: str,
    payload: dict[str, object],
    raw_path: Path,
    schema_error_category: str,
    validator: Callable[[dict[str, object]], Any],
) -> Any:
    output_contract = payload.get("output_contract")
    schema = output_contract.get("json_schema") if isinstance(output_contract, dict) else None
    schema_name = {
        "topic_mapper": "v1a_topic_map_proposal",
        "report_planner": "v1a_report_plan_proposal",
    }.get(stage)
    schema_sha256 = (
        _sha256_bytes(stable_json(schema).encode("utf-8")) if isinstance(schema, dict) else None
    )
    recorder.admit_call()
    try:
        result = provider.complete(stage, instruction, payload)
    except KeyboardInterrupt:
        recorder.record_call(
            stage=stage,
            prompt_version=prompt_version,
            config=provider.config,
            latency_ms=0,
            usage={},
            schema_valid=False,
            error_category="CANCELLED",
            schema_name=schema_name,
            schema_sha256=schema_sha256,
        )
        raise
    except ProviderCallError as exc:
        recorder.record_call(
            stage=stage,
            prompt_version=prompt_version,
            config=provider.config,
            latency_ms=exc.latency_ms,
            usage=exc.usage,
            schema_valid=False,
            error_category=exc.category,
            finish_reason=exc.finish_reason,
            content_present=exc.content_present,
            content_bytes=exc.content_bytes,
            content_sha256=exc.content_sha256,
            schema_name=schema_name,
            schema_sha256=schema_sha256,
        )
        raise PlanningError(exc.category, str(exc)) from exc
    except Exception as exc:
        recorder.record_call(
            stage=stage,
            prompt_version=prompt_version,
            config=provider.config,
            latency_ms=0,
            usage={},
            schema_valid=False,
            error_category="PROVIDER_ERROR",
            schema_name=schema_name,
            schema_sha256=schema_sha256,
        )
        raise PlanningError(
            "PROVIDER_ERROR", f"provider request failed: {type(exc).__name__}"
        ) from exc
    _write_raw(raw_path, result.raw_text)
    try:
        parsed = _parse_response(result.raw_text, stage)
    except PlanningError as exc:
        recorder.record_call(
            stage=stage,
            prompt_version=prompt_version,
            config=provider.config,
            latency_ms=result.latency_ms,
            usage=result.usage,
            schema_valid=False,
            error_category=exc.category,
            finish_reason=result.finish_reason,
            content_present=result.content_present,
            content_bytes=result.content_bytes,
            content_sha256=result.content_sha256,
            schema_name=schema_name,
            schema_sha256=schema_sha256,
        )
        recorder.artifact(raw_path.stem, raw_path)
        raise
    try:
        validated = validator(parsed)
    except ValidationError as exc:
        recorder.record_call(
            stage=stage,
            prompt_version=prompt_version,
            config=provider.config,
            latency_ms=result.latency_ms,
            usage=result.usage,
            schema_valid=False,
            error_category=schema_error_category,
            finish_reason=result.finish_reason,
            content_present=result.content_present,
            content_bytes=result.content_bytes,
            content_sha256=result.content_sha256,
            schema_name=schema_name,
            schema_sha256=schema_sha256,
        )
        recorder.artifact(raw_path.stem, raw_path)
        raise PlanningError(schema_error_category, str(exc)) from exc
    recorder.record_call(
        stage=stage,
        prompt_version=prompt_version,
        config=provider.config,
        latency_ms=result.latency_ms,
        usage=result.usage,
        schema_valid=True,
        finish_reason=result.finish_reason,
        content_present=result.content_present,
        content_bytes=result.content_bytes,
        content_sha256=result.content_sha256,
        schema_name=schema_name,
        schema_sha256=schema_sha256,
    )
    recorder.artifact(raw_path.stem, raw_path)
    return validated


def build_from_transcript(
    *,
    manifest_path: Path,
    segments_path: Path,
    run_id: str,
    output_root: Path,
    provider: Any | None = None,
    strategy: Mapping[str, object] | None = None,
) -> PlanningRunSummary:
    recorder = RunRecorder.create(output_root, run_id)
    try:
        active_provider = provider or OpenAIPlanningProvider.from_environment(strategy)
        source = load_source(manifest_path, segments_path)
        recorder.configure(active_provider.config, source)
        segments = list(source.segments)

        recorder.transition("MAPPING")
        topic_proposal = _call_stage(
            recorder,
            active_provider,
            stage="topic_mapper",
            prompt_version=MAPPER_PROMPT_VERSION,
            instruction=MAPPER_SYSTEM_INSTRUCTION,
            payload=mapper_payload(source.video_payload, segments),
            raw_path=recorder.run_dir / "topic-map.raw.json",
            schema_error_category="TOPIC_MAP_SCHEMA_ERROR",
            validator=TopicMapProposal.model_validate,
        )
        topic_map = bind_topic_map(topic_proposal, segments)
        topic_path = recorder.run_dir / "topic-map.json"
        _atomic_json(topic_path, topic_map.model_dump(mode="json"))
        recorder.artifact("topic_map", topic_path)
        recorder.transition("TOPIC_MAPPED")

        recorder.transition("PLANNING")
        plan_proposal = _call_stage(
            recorder,
            active_provider,
            stage="report_planner",
            prompt_version=PLANNER_PROMPT_VERSION,
            instruction=PLANNER_SYSTEM_INSTRUCTION,
            payload=planner_payload(source.video_payload, segments, topic_map),
            raw_path=recorder.run_dir / "report-plan.raw.json",
            schema_error_category="PLAN_PROPOSAL_SCHEMA_ERROR",
            validator=ReportPlanProposal.model_validate,
        )
        plan, assets = compile_report_plan(
            plan_proposal,
            topic_map,
            segments,
            title=source.title,
            source_url=source.source_url,
            attribution=source.attribution,
            duration_ms=source.duration_ms,
        )
        plan_path = recorder.run_dir / "report-plan.json"
        assets_path = recorder.run_dir / "assets.json"
        _atomic_json(plan_path, plan.model_dump(mode="json"))
        _atomic_json(assets_path, assets.model_dump(mode="json"))
        recorder.artifact("report_plan", plan_path)
        recorder.artifact("assets", assets_path)
        validation_path = recorder.run_dir / "validation.json"
        _atomic_json(
            validation_path,
            {
                "topic_count": len(topic_map.topics),
                "mapped_count": topic_map.coverage.mapped_count,
                "excluded_count": topic_map.coverage.excluded_count,
                "section_count": len(plan.sections),
                "block_count": sum(len(section.blocks) for section in plan.sections),
                "source_ref_count": sum(
                    len(block.source_refs) for section in plan.sections for block in section.blocks
                ),
                "asset_count": 0,
            },
        )
        recorder.artifact("validation", validation_path)
        recorder.transition("PLAN_VALIDATED")

        report_path = recorder.run_dir / "report.html"
        try:
            render_summary = render_report(plan_path, assets_path, report_path)
        except RenderError as exc:
            raise PlanningError("RENDER_ERROR", str(exc)) from exc
        recorder.artifact("report_html", report_path)
        if recorder.payload["provider_calls"] != 2 or recorder.payload["model_calls"] != 2:
            raise PlanningError("PROVIDER_ERROR", "successful run must contain exactly two calls")
        recorder.transition("RENDERED")
        return PlanningRunSummary(
            run_id=run_id,
            run_dir=recorder.run_dir,
            state="RENDERED",
            provider_calls=2,
            model_calls=2,
            section_count=render_summary.section_count,
            block_count=render_summary.block_count,
            report_path=report_path,
        )
    except KeyboardInterrupt as exc:
        error = PlanningError("CANCELLED", "run cancelled by operator")
        recorder.fail(error, state="CANCELLED")
        raise error from exc
    except PlanningError as exc:
        recorder.fail(exc)
        raise
    except OSError as exc:
        error = PlanningError("OUTPUT_IO_ERROR", type(exc).__name__)
        recorder.fail(error)
        raise error from exc


def _semantic_v2_request_sha256(
    stage: str,
    instruction: str,
    payload: dict[str, object],
    config: Any,
) -> str:
    if isinstance(config, PlanningConfig):
        request = semantic_v2_chat_completion_request(stage, instruction, payload, config)
    else:
        request = {
            "model": getattr(config, "model", None),
            "messages": [
                {"role": "system", "content": instruction},
                {"role": "user", "content": stable_json(payload)},
            ],
            "temperature": getattr(config, "temperature", TEMPERATURE),
            "max_tokens": getattr(config, "output_token_limit", MAX_OUTPUT_TOKENS),
            "response_format": {
                "type": getattr(config, "response_mode", SEMANTIC_V2_RESPONSE_MODE)
            },
            "reasoning_effort": getattr(config, "reasoning_effort", None),
            "extra_body": {
                "thinking": {"type": getattr(config, "thinking_mode", None)}
            },
        }
    return _sha256_bytes(
        stable_json({"stage": stage, "request": request}).encode("utf-8")
    )


def _semantic_v2_call_stage(
    recorder: RunRecorder,
    provider: Any,
    *,
    stage: str,
    prompt_version: str,
    instruction: str,
    payload: dict[str, object],
    raw_path: Path,
    normalizer: Callable[[Mapping[str, object]], Any],
    retry_state: dict[str, bool],
) -> tuple[Any, list[dict[str, object]]]:
    """Run one semantic stage with one shared, identical technical retry."""
    request_sha256 = _semantic_v2_request_sha256(
        stage, instruction, payload, provider.config
    )
    output_contract = payload.get("output_contract")
    schema = output_contract.get("json_schema") if isinstance(output_contract, dict) else None
    schema_sha256 = (
        _sha256_bytes(stable_json(schema).encode("utf-8")) if isinstance(schema, dict) else None
    )
    schema_name = f"semantic_v2_{stage}"
    for attempt in (1, 2):
        if attempt == 2 and retry_state.get("used") is not True:
            raise PlanningError("PROVIDER_ERROR", "semantic-v2 retry state is inconsistent")
        recorder.admit_call()
        retry_of_attempt = attempt - 1 if attempt > 1 else None
        try:
            result = provider.complete(stage, instruction, payload)
        except KeyboardInterrupt:
            recorder.record_call(
                stage=stage,
                prompt_version=prompt_version,
                config=provider.config,
                latency_ms=0,
                usage={},
                schema_valid=False,
                error_category="CANCELLED",
                schema_name=schema_name,
                schema_sha256=schema_sha256,
                attempt=attempt,
                request_sha256=request_sha256,
                retry_of_attempt=retry_of_attempt,
                retry_eligible=False,
                retry_used=retry_state.get("used", False),
            )
            raise
        except ProviderCallError as exc:
            eligible = bool(exc.retryable)
            recorder.record_call(
                stage=stage,
                prompt_version=prompt_version,
                config=provider.config,
                latency_ms=exc.latency_ms,
                usage=exc.usage,
                schema_valid=False,
                error_category=exc.category,
                finish_reason=exc.finish_reason,
                content_present=exc.content_present,
                content_bytes=exc.content_bytes,
                content_sha256=exc.content_sha256,
                schema_name=schema_name,
                schema_sha256=schema_sha256,
                attempt=attempt,
                request_sha256=request_sha256,
                retry_of_attempt=retry_of_attempt,
                retry_eligible=eligible,
                retry_used=retry_state.get("used", False),
            )
            if eligible and not retry_state.get("used", False):
                retry_state["used"] = True
                recorder.event(
                    "TECHNICAL_RETRY_ADMITTED",
                    stage=stage,
                    retry_of_attempt=attempt,
                    request_sha256=request_sha256,
                    reason=exc.category,
                )
                continue
            raise PlanningError(exc.category, str(exc)) from exc
        except Exception as exc:
            recorder.record_call(
                stage=stage,
                prompt_version=prompt_version,
                config=provider.config,
                latency_ms=0,
                usage={},
                schema_valid=False,
                error_category="PROVIDER_ERROR",
                schema_name=schema_name,
                schema_sha256=schema_sha256,
                attempt=attempt,
                request_sha256=request_sha256,
                retry_of_attempt=retry_of_attempt,
                retry_eligible=False,
                retry_used=retry_state.get("used", False),
            )
            raise PlanningError(
                "PROVIDER_ERROR", f"provider request failed: {type(exc).__name__}"
            ) from exc

        attempt_path = raw_path.parent / f"{raw_path.name}.attempt-{attempt:02d}.json"
        _write_raw(attempt_path, result.raw_text)
        recorder.artifact(f"{raw_path.stem}_attempt_{attempt:02d}", attempt_path)
        if result.finish_reason not in {None, "stop", "completed"}:
            error = PlanningError(
                "MODEL_OUTPUT_INCOMPLETE",
                f"{stage} response finished with {result.finish_reason}",
            )
            recorder.record_call(
                stage=stage,
                prompt_version=prompt_version,
                config=provider.config,
                latency_ms=result.latency_ms,
                usage=result.usage,
                schema_valid=False,
                error_category=error.category,
                finish_reason=result.finish_reason,
                content_present=result.content_present,
                content_bytes=result.content_bytes,
                content_sha256=result.content_sha256,
                schema_name=schema_name,
                schema_sha256=schema_sha256,
                attempt=attempt,
                request_sha256=request_sha256,
                retry_of_attempt=retry_of_attempt,
                retry_eligible=True,
                retry_used=retry_state.get("used", False),
            )
            if not retry_state.get("used", False):
                retry_state["used"] = True
                recorder.event(
                    "TECHNICAL_RETRY_ADMITTED",
                    stage=stage,
                    retry_of_attempt=attempt,
                    request_sha256=request_sha256,
                    reason=error.category,
                )
                continue
            raise error
        try:
            parsed = _parse_response(result.raw_text, stage)
        except PlanningError as error:
            recorder.record_call(
                stage=stage,
                prompt_version=prompt_version,
                config=provider.config,
                latency_ms=result.latency_ms,
                usage=result.usage,
                schema_valid=False,
                error_category=error.category,
                finish_reason=result.finish_reason,
                content_present=result.content_present,
                content_bytes=result.content_bytes,
                content_sha256=result.content_sha256,
                schema_name=schema_name,
                schema_sha256=schema_sha256,
                attempt=attempt,
                request_sha256=request_sha256,
                retry_of_attempt=retry_of_attempt,
                retry_eligible=True,
                retry_used=retry_state.get("used", False),
            )
            if not retry_state.get("used", False):
                retry_state["used"] = True
                recorder.event(
                    "TECHNICAL_RETRY_ADMITTED",
                    stage=stage,
                    retry_of_attempt=attempt,
                    request_sha256=request_sha256,
                    reason=error.category,
                )
                continue
            raise
        try:
            normalized = normalizer(parsed)
        except PlanningError as error:
            recorder.record_call(
                stage=stage,
                prompt_version=prompt_version,
                config=provider.config,
                latency_ms=result.latency_ms,
                usage=result.usage,
                schema_valid=False,
                error_category=error.category,
                finish_reason=result.finish_reason,
                content_present=result.content_present,
                content_bytes=result.content_bytes,
                content_sha256=result.content_sha256,
                schema_name=schema_name,
                schema_sha256=schema_sha256,
                attempt=attempt,
                request_sha256=request_sha256,
                retry_of_attempt=retry_of_attempt,
                retry_eligible=False,
                retry_used=retry_state.get("used", False),
            )
            raise
        recorder.record_call(
            stage=stage,
            prompt_version=prompt_version,
            config=provider.config,
            latency_ms=result.latency_ms,
            usage=result.usage,
            schema_valid=True,
            finish_reason=result.finish_reason,
            content_present=result.content_present,
            content_bytes=result.content_bytes,
            content_sha256=result.content_sha256,
            schema_name=schema_name,
            schema_sha256=schema_sha256,
            attempt=attempt,
            request_sha256=request_sha256,
            retry_of_attempt=retry_of_attempt,
            retry_eligible=False,
            retry_used=retry_state.get("used", False),
        )
        _write_raw(raw_path, result.raw_text)
        recorder.artifact(raw_path.stem, raw_path)
        return normalized.proposal, list(normalized.events)
    raise PlanningError("PROVIDER_ERROR", "semantic-v2 call loop exhausted")


def _semantic_v2_events_payload(
    stage: str, events: list[dict[str, object]]
) -> dict[str, object]:
    return {
        "schema_version": SEMANTIC_V2_NORMALIZATION_SCHEMA_VERSION,
        "compiler_version": SEMANTIC_V2_COMPILER_VERSION,
        "stage": stage,
        "events": events,
        "event_count": len(events),
    }


def build_from_transcript_v2(
    *,
    manifest_path: Path,
    segments_path: Path,
    run_id: str,
    output_root: Path,
    provider: Any | None = None,
    recorder: RunRecorder | None = None,
) -> PlanningRunSummary:
    """Build one current semantic-v2 product prototype report."""
    if recorder is None:
        recorder = RunRecorder.create(
            output_root,
            run_id,
            schema_version=SEMANTIC_V2_RUN_SCHEMA_VERSION,
            event_schema_version=SEMANTIC_V2_EVENT_SCHEMA_VERSION,
            call_schema_version=SEMANTIC_V2_CALL_SCHEMA_VERSION,
        )
    retry_state = {"used": False}
    try:
        active_provider = provider or OpenAISemanticV2PlanningProvider.from_environment()
        source = load_source(manifest_path, segments_path)
        recorder.configure(active_provider.config, source)
        recorder.payload["pipeline"] = "semantic-v2-product-prototype"
        recorder.payload["base_model_call_budget"] = 2
        recorder.payload["maximum_model_call_budget"] = 3
        recorder.payload["semantic_stages"] = ["topic_mapper", "report_planner"]
        recorder.payload["technical_retry_policy"] = {
            "max_retries_per_run": 1,
            "identical_request": True,
            "sdk_max_retries": 0,
        }
        recorder.save()
        segments = list(source.segments)

        recorder.transition("MAPPING")
        topic_payload = semantic_v2_mapper_payload(source.video_payload, segments)
        topic_proposal, topic_events = _semantic_v2_call_stage(
            recorder,
            active_provider,
            stage="topic_mapper",
            prompt_version=SEMANTIC_V2_MAPPER_PROMPT_VERSION,
            instruction=SEMANTIC_V2_MAPPER_SYSTEM_INSTRUCTION,
            payload=topic_payload,
            raw_path=recorder.run_dir / "topic-map.raw.json",
            normalizer=normalize_semantic_v2_topic_proposal,
            retry_state=retry_state,
        )
        topic_map, topic_events = resolve_semantic_v2_topic_map(
            topic_proposal, segments, events=topic_events
        )
        topic_path = recorder.run_dir / "topic-map.json"
        _atomic_json(topic_path, topic_map.model_dump(mode="json"))
        recorder.artifact("topic_map", topic_path)
        topic_normalization_path = recorder.run_dir / "topic-normalization.json"
        _atomic_json(
            topic_normalization_path,
            _semantic_v2_events_payload("topic_mapper", topic_events),
        )
        recorder.artifact("topic_normalization", topic_normalization_path)
        recorder.transition("TOPIC_MAPPED")

        recorder.transition("PLANNING")
        plan_payload = semantic_v2_planner_payload(source.video_payload, segments, topic_map)
        plan_proposal, plan_events = _semantic_v2_call_stage(
            recorder,
            active_provider,
            stage="report_planner",
            prompt_version=SEMANTIC_V2_PLANNER_PROMPT_VERSION,
            instruction=SEMANTIC_V2_PLANNER_SYSTEM_INSTRUCTION,
            payload=plan_payload,
            raw_path=recorder.run_dir / "report-plan.raw.json",
            normalizer=normalize_semantic_v2_plan_proposal,
            retry_state=retry_state,
        )
        plan, assets, ledger = compile_semantic_v2_report_plan(
            plan_proposal,
            topic_map,
            segments,
            title=source.title,
            source_url=source.source_url,
            attribution=source.attribution,
            duration_ms=source.duration_ms,
            normalization_events=plan_events,
        )
        planner_normalization_path = recorder.run_dir / "planner-normalization.json"
        _atomic_json(
            planner_normalization_path,
            _semantic_v2_events_payload("report_planner", plan_events),
        )
        recorder.artifact("planner_normalization", planner_normalization_path)
        plan_path = recorder.run_dir / "report-plan.json"
        assets_path = recorder.run_dir / "assets.json"
        normalization_path = recorder.run_dir / "normalization.json"
        _atomic_json(plan_path, plan.model_dump(mode="json"))
        _atomic_json(assets_path, assets.model_dump(mode="json"))
        _atomic_json(normalization_path, ledger.model_dump(mode="json"))
        recorder.artifact("report_plan", plan_path)
        recorder.artifact("assets", assets_path)
        recorder.artifact("normalization", normalization_path)
        validation_path = recorder.run_dir / "validation.json"
        _atomic_json(
            validation_path,
            {
                "pipeline": "semantic-v2-product-prototype",
                "video_id": topic_map.video_id,
                "topic_count": len(topic_map.topics),
                "span_covered_count": topic_map.coverage.span_covered_count,
                "representative_covered_count": topic_map.coverage.representative_covered_count,
                "uncovered_segment_ids": list(topic_map.coverage.uncovered_segment_ids),
                "overlap_segment_ids": list(topic_map.coverage.overlap_segment_ids),
                "section_count": len(plan.sections),
                "block_count": sum(len(section.blocks) for section in plan.sections),
                "source_ref_count": sum(
                    len(block.source_refs) for section in plan.sections for block in section.blocks
                ),
                "hero_source_segment_ids": list(plan_proposal.hero.source_segment_ids),
                "asset_count": len(assets.assets),
                "normalization_summary": ledger.summary,
            },
        )
        recorder.artifact("validation", validation_path)
        recorder.transition("PLAN_VALIDATED")

        report_path = recorder.run_dir / "report.html"
        try:
            render_summary = render_report(plan_path, assets_path, report_path)
        except RenderError as exc:
            raise PlanningError("RENDER_ERROR", str(exc)) from exc
        recorder.artifact("report_html", report_path)
        provider_calls = int(recorder.payload["provider_calls"])
        if provider_calls not in {2, 3} or provider_calls > 3:
            raise PlanningError(
                "PROVIDER_ERROR", "successful semantic-v2 run must contain two or three calls"
            )
        recorder.payload["retry_used"] = retry_state["used"]
        recorder.save()
        recorder.transition("RENDERED")
        return PlanningRunSummary(
            run_id=run_id,
            run_dir=recorder.run_dir,
            state="RENDERED",
            provider_calls=provider_calls,
            model_calls=int(recorder.payload["model_calls"]),
            section_count=render_summary.section_count,
            block_count=render_summary.block_count,
            report_path=report_path,
        )
    except KeyboardInterrupt as exc:
        error = PlanningError("CANCELLED", "run cancelled by operator")
        recorder.fail(error, state="CANCELLED")
        raise error from exc
    except PlanningError as exc:
        recorder.payload["retry_used"] = retry_state["used"]
        recorder.save()
        recorder.fail(exc)
        raise
    except OSError as exc:
        error = PlanningError("OUTPUT_IO_ERROR", type(exc).__name__)
        recorder.fail(error)
        raise error from exc


@dataclass(frozen=True)
class ReplaySummary:
    provider_calls: int
    model_calls: int
    topic_map: TopicMap
    report_plan_sha256: str
    report_html_sha256: str


def replay_proposals(
    *,
    manifest_path: Path,
    segments_path: Path,
    topic_proposal_payload: dict[str, object],
    plan_proposal_payload: dict[str, object],
    output_dir: Path,
) -> ReplaySummary:
    source = load_source(manifest_path, segments_path)
    segments = list(source.segments)
    try:
        topic_proposal = TopicMapProposal.model_validate(topic_proposal_payload)
    except ValidationError as exc:
        raise PlanningError("TOPIC_MAP_SCHEMA_ERROR", str(exc)) from exc
    topic_map = bind_topic_map(topic_proposal, segments)
    try:
        plan_proposal = ReportPlanProposal.model_validate(plan_proposal_payload)
    except ValidationError as exc:
        raise PlanningError("PLAN_PROPOSAL_SCHEMA_ERROR", str(exc)) from exc
    plan, assets = compile_report_plan(
        plan_proposal,
        topic_map,
        segments,
        title=source.title,
        source_url=source.source_url,
        attribution=source.attribution,
        duration_ms=source.duration_ms,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    plan_path = output_dir / "report-plan.json"
    assets_path = output_dir / "assets.json"
    report_path = output_dir / "report.html"
    _atomic_json(plan_path, plan.model_dump(mode="json"))
    _atomic_json(assets_path, assets.model_dump(mode="json"))
    render_report(plan_path, assets_path, report_path)
    return ReplaySummary(
        provider_calls=0,
        model_calls=0,
        topic_map=topic_map,
        report_plan_sha256=_sha256_file(plan_path),
        report_html_sha256=_sha256_file(report_path),
    )


@dataclass(frozen=True)
class SemanticV2ReplaySummary:
    provider_calls: int
    model_calls: int
    topic_map: SemanticV2TopicMap
    report_plan_sha256: str
    report_html_sha256: str
    normalization_sha256: str


def replay_semantic_v2_proposals(
    *,
    manifest_path: Path,
    segments_path: Path,
    topic_proposal_payload: dict[str, object],
    plan_proposal_payload: dict[str, object],
    output_dir: Path,
) -> SemanticV2ReplaySummary:
    """Replay accepted v2 proposal JSON locally with zero provider calls."""
    source = load_source(manifest_path, segments_path)
    segments = list(source.segments)
    topic_result = normalize_semantic_v2_topic_proposal(topic_proposal_payload)
    topic_events = list(topic_result.events)
    topic_map, topic_events = resolve_semantic_v2_topic_map(
        topic_result.proposal, segments, events=topic_events
    )
    plan_result = normalize_semantic_v2_plan_proposal(plan_proposal_payload)
    plan_events = list(plan_result.events)
    plan, assets, ledger = compile_semantic_v2_report_plan(
        plan_result.proposal,
        topic_map,
        segments,
        title=source.title,
        source_url=source.source_url,
        attribution=source.attribution,
        duration_ms=source.duration_ms,
        normalization_events=plan_events,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    plan_path = output_dir / "report-plan.json"
    assets_path = output_dir / "assets.json"
    topic_path = output_dir / "topic-map.json"
    normalization_path = output_dir / "normalization.json"
    report_path = output_dir / "report.html"
    _atomic_json(topic_path, topic_map.model_dump(mode="json"))
    _atomic_json(plan_path, plan.model_dump(mode="json"))
    _atomic_json(assets_path, assets.model_dump(mode="json"))
    _atomic_json(normalization_path, ledger.model_dump(mode="json"))
    render_report(plan_path, assets_path, report_path)
    return SemanticV2ReplaySummary(
        provider_calls=0,
        model_calls=0,
        topic_map=topic_map,
        report_plan_sha256=_sha256_file(plan_path),
        report_html_sha256=_sha256_file(report_path),
        normalization_sha256=_sha256_file(normalization_path),
    )
