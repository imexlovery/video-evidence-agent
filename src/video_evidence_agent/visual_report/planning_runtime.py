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
from typing import Any, Callable
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
    PLAN_PROPOSAL_SCHEMA_VERSION,
    PLANNER_PROMPT_VERSION,
    PLANNER_SYSTEM_INSTRUCTION,
    TOPIC_MAP_SCHEMA_VERSION,
    TOPIC_PROPOSAL_SCHEMA_VERSION,
    PlanningError,
    ReportPlanProposal,
    TopicMap,
    TopicMapProposal,
    bind_topic_map,
    compile_report_plan,
    mapper_payload,
    planner_payload,
    stable_json,
    validate_transcript_envelope,
)
from .renderer import RenderError, render_report

RUN_SCHEMA_VERSION = "visual-report-planning-run.v1a-prototype"
EVENT_SCHEMA_VERSION = "visual-report-planning-event.v1a-prototype"
RESPONSE_MODE = "json_object"
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
            json.loads(line)
            for line in segments_bytes.decode("utf-8").splitlines()
            if line.strip()
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
    sdk_max_retries: int = 0
    sdk_version: str = "unknown"

    def public_snapshot(self) -> dict[str, object]:
        return {
            "provider": self.provider_label,
            "model": self.model,
            "timeout_seconds": self.timeout_seconds,
            "credential_present": self.credential_present,
            "response_mode": self.response_mode,
            "temperature": self.temperature,
            "sdk_max_retries": self.sdk_max_retries,
            "sdk_version": self.sdk_version,
            "mapper_prompt_version": MAPPER_PROMPT_VERSION,
            "planner_prompt_version": PLANNER_PROMPT_VERSION,
            "topic_proposal_schema": TOPIC_PROPOSAL_SCHEMA_VERSION,
            "topic_map_schema": TOPIC_MAP_SCHEMA_VERSION,
            "plan_proposal_schema": PLAN_PROPOSAL_SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
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
    def __init__(self, category: str, message: str, latency_ms: int) -> None:
        self.category = category
        self.latency_ms = latency_ms
        super().__init__(message)


@dataclass(frozen=True)
class ProviderResult:
    raw_text: str
    usage: dict[str, Any]
    latency_ms: int


class OpenAIPlanningProvider:
    def __init__(self, client: OpenAI, config: PlanningConfig) -> None:
        self.client = client
        self.config = config

    @classmethod
    def from_environment(cls) -> "OpenAIPlanningProvider":
        load_dotenv(Path(__file__).resolve().parents[3] / ".env", override=False)
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        model = os.getenv("VISUAL_REPORT_MODEL", "").strip()
        base_url = os.getenv("OPENAI_BASE_URL", "").strip()
        try:
            timeout_seconds = float(os.getenv("VISUAL_REPORT_TIMEOUT_SECONDS", "120"))
        except ValueError as exc:
            raise PlanningError(
                "CONFIGURATION_ERROR", "VISUAL_REPORT_TIMEOUT_SECONDS must be numeric"
            ) from exc
        if not api_key:
            raise PlanningError("CONFIGURATION_ERROR", "OPENAI_API_KEY is required")
        if not model:
            raise PlanningError("CONFIGURATION_ERROR", "VISUAL_REPORT_MODEL is required")
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
            sdk_version=importlib.metadata.version("openai"),
        )
        return cls(OpenAI(**options), config)

    def complete(
        self, stage: str, system_instruction: str, payload: dict[str, object]
    ) -> ProviderResult:
        del stage
        started = perf_counter()
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                temperature=TEMPERATURE,
                response_format={"type": RESPONSE_MODE},
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": stable_json(payload)},
                ],
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
        if not response.choices or response.choices[0].message.content is None:
            raise ProviderCallError(
                "PROVIDER_ERROR", "provider returned no message content", latency_ms
            )
        usage: dict[str, Any] = {}
        if response.usage is not None:
            try:
                candidate = response.usage.model_dump(mode="json")
                if isinstance(candidate, dict):
                    usage = candidate
            except (AttributeError, TypeError, ValueError):
                pass
        return ProviderResult(
            raw_text=response.choices[0].message.content,
            usage=usage,
            latency_ms=latency_ms,
        )


class RunRecorder:
    def __init__(self, run_id: str, run_dir: Path) -> None:
        self.run_id = run_id
        self.run_dir = run_dir
        self.run_path = run_dir / "run.json"
        self.events_path = run_dir / "events.jsonl"
        self.calls_path = run_dir / "model-calls.jsonl"
        self.payload: dict[str, Any] = {
            "schema_version": RUN_SCHEMA_VERSION,
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
    def create(cls, output_root: Path, run_id: str) -> "RunRecorder":
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
        return cls(run_id, run_dir)

    def save(self) -> None:
        self.payload["updated_at"] = _now()
        _atomic_json(self.run_path, self.payload)

    def event(self, state: str, **detail: object) -> None:
        _append_jsonl(
            self.events_path,
            {"schema_version": EVENT_SCHEMA_VERSION, "at": _now(), "state": state, **detail},
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
        self.payload["source"] = {
            "video_id": source.video_id,
            "manifest_path": str(source.manifest_path),
            "segments_path": str(source.segments_path),
            "manifest_sha256": source.manifest_sha256,
            "segments_sha256": source.segments_sha256,
            "segment_count": len(source.segments),
        }
        self.payload["prompt_sha256"] = {
            MAPPER_PROMPT_VERSION: _sha256_bytes(MAPPER_SYSTEM_INSTRUCTION.encode("utf-8")),
            PLANNER_PROMPT_VERSION: _sha256_bytes(PLANNER_SYSTEM_INSTRUCTION.encode("utf-8")),
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
    ) -> None:
        _append_jsonl(
            self.calls_path,
            {
                "schema_version": CALL_SCHEMA_VERSION,
                "at": _now(),
                "stage": stage,
                "provider": config.provider_label,
                "model": config.model,
                "prompt_version": prompt_version,
                "temperature": config.temperature,
                "timeout_seconds": config.timeout_seconds,
                "response_mode": config.response_mode,
                "sdk_max_retries": config.sdk_max_retries,
                "sdk_version": config.sdk_version,
                "latency_ms": latency_ms,
                "usage": usage,
                "schema_valid": schema_valid,
                "error_category": error_category,
            },
        )
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
        )
        raise
    except ProviderCallError as exc:
        recorder.record_call(
            stage=stage,
            prompt_version=prompt_version,
            config=provider.config,
            latency_ms=exc.latency_ms,
            usage={},
            schema_valid=False,
            error_category=exc.category,
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
) -> PlanningRunSummary:
    recorder = RunRecorder.create(output_root, run_id)
    try:
        active_provider = provider or OpenAIPlanningProvider.from_environment()
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
