from __future__ import annotations

import json
import math
from pathlib import Path
from types import SimpleNamespace

import pytest

from video_evidence_agent.schemas import VideoSegment
from video_evidence_agent.visual_report.planning import (
    SEMANTIC_V2_COMPILER_VERSION,
    SEMANTIC_V2_HARD_MAX_COMPILED_BLOCKS,
    SEMANTIC_V2_HARD_MAX_VISIBLE_CHARACTERS,
    SEMANTIC_V2_MAX_OUTPUT_TOKENS,
    SEMANTIC_V2_MODEL,
    SEMANTIC_V2_PLAN_PROPOSAL_SCHEMA_VERSION,
    SEMANTIC_V2_PLANNER_SYSTEM_INSTRUCTION,
    SEMANTIC_V2_REASONING_EFFORT,
    SEMANTIC_V2_THINKING_MODE,
    SEMANTIC_V2_TOPIC_PROPOSAL_SCHEMA_VERSION,
    FakeSemanticV2PlanningProvider,
    PlanningError,
    ProviderResult,
    build_semantic_v2_planning_budget,
    normalize_semantic_v2_topic_proposal,
    resolve_semantic_v2_topic_map,
    semantic_v2_budget_diagnostics,
    semantic_v2_planner_payload,
)
from video_evidence_agent.visual_report.planning_runtime import (
    SEMANTIC_V2_RESPONSE_MODE,
    SEMANTIC_V2_SCHEMA_MECHANISM,
    OpenAISemanticV2PlanningProvider,
    PlanningConfig,
    ProviderCallError,
    _semantic_v2_request_sha256,
    build_from_transcript_v2,
    load_source,
    replay_semantic_v2_proposals,
    semantic_v2_chat_completion_request,
)

FIXTURE_ROOT = Path("tests/fixtures/visual-report-v1a")


def _segments() -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in (FIXTURE_ROOT / "segments.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _v2_proposals() -> tuple[dict[str, object], dict[str, object]]:
    segments = _segments()
    ids = [str(item["segment_id"]) for item in segments]
    topic_map = {
        "schema_version": SEMANTIC_V2_TOPIC_PROPOSAL_SCHEMA_VERSION,
        "topics": [
            {
                "title": "背景",
                "summary": "说明问题背景和限制。",
                "importance": "primary",
                "start_segment_id": ids[0],
                "end_segment_id": ids[1],
                "representative_segment_ids": [ids[0]],
            },
            {
                "title": "方案比较",
                "summary": "比较离线与在线方案。",
                "importance": "primary",
                "start_segment_id": ids[2],
                "end_segment_id": ids[3],
                "representative_segment_ids": [ids[2]],
            },
            {
                "title": "执行步骤",
                "summary": "给出准备、执行、复盘步骤。",
                "importance": "primary",
                "start_segment_id": ids[4],
                "end_segment_id": ids[5],
                "representative_segment_ids": [ids[4]],
            },
        ],
    }
    report_plan = {
        "schema_version": SEMANTIC_V2_PLAN_PROPOSAL_SCHEMA_VERSION,
        "hero": {
            "title": "可追溯执行",
            "tldr": "报告保留重点、来源和显式省略。",
            "source_segment_ids": [ids[6]],
        },
        "sections": [
            {
                "title": "背景与限制",
                "topic_ids": ["topic-001"],
                "content_units": [
                    {
                        "suggested_block_type": "insight_card",
                        "headline": "先明确问题",
                        "body": "第一部分解释问题背景，主要限制需要被明确记录。",
                        "topic_ids": ["topic-001"],
                        "source_segment_ids": [ids[0], ids[1]],
                    }
                ],
            },
            {
                "title": "方案选择",
                "topic_ids": ["topic-002"],
                "content_units": [
                    {
                        "suggested_block_type": "comparison_card",
                        "headline": "离线与在线",
                        "left_label": "离线方案",
                        "left_items": ["离线方案"],
                        "right_label": "在线方案",
                        "right_items": ["在线方案能够持续接收新的反馈。"],
                        "topic_ids": ["topic-002"],
                        "source_segment_ids": [ids[2], ids[3]],
                    }
                ],
            },
            {
                "title": "执行与复盘",
                "topic_ids": ["topic-003"],
                "content_units": [
                    {
                        "suggested_block_type": "process_flow",
                        "headline": "保留执行链路",
                        "items": ["准备", "执行", "复盘"],
                        "topic_ids": ["topic-003"],
                        "source_segment_ids": [ids[4], ids[5]],
                    }
                ],
            },
        ],
    }
    return topic_map, report_plan


def test_semantic_v2_normalizer_and_resolver_keep_semantics_and_diagnostics() -> None:
    topic_map, _ = _v2_proposals()
    topic_map["metadata"] = {"layout": "forbidden"}
    topic_map["topics"][0]["title"] = " 背景 "
    topic_map["topics"][0]["representative_segment_ids"] = [
        topic_map["topics"][0]["representative_segment_ids"][0],
        topic_map["topics"][0]["representative_segment_ids"][0],
        "unknown-segment",
    ]
    result = normalize_semantic_v2_topic_proposal(topic_map)
    assert result.proposal.topics[0].title == "背景"
    assert "metadata" not in result.proposal.model_dump()
    rule_ids = {str(event["rule_id"]) for event in result.events}
    assert {"DISCARD_UNKNOWN_FIELD", "TRIM_WHITESPACE", "DEDUPLICATE_SOURCE_ID"} <= rule_ids

    segments = [VideoSegment.model_validate(item) for item in _segments()]
    from video_evidence_agent.visual_report.planning import resolve_semantic_v2_topic_map

    canonical, events = resolve_semantic_v2_topic_map(result.proposal, segments)
    assert [topic.topic_id for topic in canonical.topics] == [
        "topic-001",
        "topic-002",
        "topic-003",
    ]
    assert canonical.coverage.uncovered_segment_ids == (
        "synthetic-v1a-seg-006",
        "synthetic-v1a-seg-007",
    )
    assert canonical.topics[0].summary == "说明问题背景和限制。"
    assert any(event["rule_id"] == "RECORD_TOPIC_COVERAGE_DIAGNOSTICS" for event in events)


@pytest.mark.parametrize(
    ("duration_ms", "primary_topic_count", "expected"),
    [
        (0, 0, 6),
        (60_000, 1, 6),
        (600_000, 0, 6),
        (600_001, 0, 7),
        (1_000_000, 0, 10),
        (1, 13, 24),
        (60_000_000, 0, 24),
    ],
)
def test_semantic_v2_adaptive_budget_formula_and_clamps(
    duration_ms: int, primary_topic_count: int, expected: int
) -> None:
    budget = build_semantic_v2_planning_budget(
        duration_ms=duration_ms, primary_topic_count=primary_topic_count
    )
    assert budget.recommended_block_budget == expected
    assert budget.recommendations_are_soft is True
    assert budget.hard_limits == {
        "compiled_blocks": SEMANTIC_V2_HARD_MAX_COMPILED_BLOCKS,
        "visible_authored_characters": SEMANTIC_V2_HARD_MAX_VISIBLE_CHARACTERS,
    }


def test_semantic_v2_budget_payload_and_diagnostics_are_deterministic() -> None:
    topic_payload, _ = _v2_proposals()
    segments = [VideoSegment.model_validate(item) for item in _segments()]
    from video_evidence_agent.visual_report.planning import resolve_semantic_v2_topic_map

    topic_result = normalize_semantic_v2_topic_proposal(topic_payload)
    topic_map, _ = resolve_semantic_v2_topic_map(topic_result.proposal, segments)
    budget = build_semantic_v2_planning_budget(
        duration_ms=8_000,
        primary_topic_count=3,
    )
    payload = semantic_v2_planner_payload(
        {"video_id": "synthetic-v1a", "title": "合成样例", "duration_ms": 8_000},
        segments,
        topic_map,
        planning_budget=budget,
    )
    assert payload["planning_budget"] == budget.model_dump(mode="json")
    assert "block 数量是软范围提示" in SEMANTIC_V2_PLANNER_SYSTEM_INSTRUCTION
    assert "不要为了命中推荐值而填充" in SEMANTIC_V2_PLANNER_SYSTEM_INSTRUCTION
    assert "重复、截断、改写、合并或拆分" in SEMANTIC_V2_PLANNER_SYSTEM_INSTRUCTION

    undershoot = semantic_v2_budget_diagnostics(
        budget,
        actual_compiled_block_count=5,
        actual_visible_authored_characters=899,
    )
    assert undershoot["block_budget_status"] == "BUDGET_UNDERSHOOT"
    assert undershoot["visible_density_status"] == "DENSITY_UNDERSHOOT"
    assert undershoot["hard_failure"] is False

    overshoot = semantic_v2_budget_diagnostics(
        budget,
        actual_compiled_block_count=7,
        actual_visible_authored_characters=1_821,
    )
    assert overshoot["block_budget_status"] == "BUDGET_OVERSHOOT"
    assert overshoot["visible_density_status"] == "DENSITY_OVERSHOOT"
    assert overshoot["hard_failure"] is False

    exact_boundary = semantic_v2_budget_diagnostics(
        budget,
        actual_compiled_block_count=SEMANTIC_V2_HARD_MAX_COMPILED_BLOCKS,
        actual_visible_authored_characters=SEMANTIC_V2_HARD_MAX_VISIBLE_CHARACTERS,
        compiler_version=SEMANTIC_V2_COMPILER_VERSION,
    )
    assert exact_boundary["hard_checks"]["compiled_blocks"]["passed"] is True
    assert exact_boundary["hard_checks"]["visible_authored_characters"]["passed"] is True
    assert exact_boundary["hard_failure"] is False

    above_boundary = semantic_v2_budget_diagnostics(
        budget,
        actual_compiled_block_count=SEMANTIC_V2_HARD_MAX_COMPILED_BLOCKS + 1,
        actual_visible_authored_characters=SEMANTIC_V2_HARD_MAX_VISIBLE_CHARACTERS + 1,
    )
    assert above_boundary["hard_failure"] is True
    assert above_boundary["hard_checks"]["compiled_blocks"]["passed"] is False
    assert above_boundary["hard_checks"]["visible_authored_characters"]["passed"] is False


def test_semantic_v2_budget_derives_current_retained_recommendations() -> None:
    retained_inputs = [
        ("p0b-kling-2024", "p0b-kling-2024-semantic-v2-98d9af23a9"),
        ("p0b-rlinf-2026", "p0b-rlinf-2026-semantic-v2-98d9af23a9"),
        ("p0b-wuyi-goals", "p0b-wuyi-goals-semantic-v2-98d9af23a9"),
    ]
    recommendations: list[int] = []
    for video_id, run_id in retained_inputs:
        source = load_source(
            Path(f"artifacts/p0b-ingest/{video_id}/manifest.json"),
            Path(f"artifacts/p0b-ingest/{video_id}/segments.jsonl"),
        )
        topic_payload = json.loads(
            (
                Path("artifacts/visual-report/v1a")
                / run_id
                / "topic-map.raw.json"
            ).read_text(encoding="utf-8")
        )
        topic_result = normalize_semantic_v2_topic_proposal(topic_payload)
        topic_map, _ = resolve_semantic_v2_topic_map(topic_result.proposal, source.segments)
        primary_topic_count = sum(
            topic.importance == "primary" for topic in topic_map.topics
        )
        budget = build_semantic_v2_planning_budget(
            duration_ms=source.duration_ms,
            primary_topic_count=primary_topic_count,
        )
        derived = min(
            24,
            max(
                6,
                math.ceil(
                    max(source.duration_ms / 60_000 * 0.6, primary_topic_count * 2, 6)
                ),
            ),
        )
        assert budget.recommended_block_budget == derived
        recommendations.append(derived)
    assert recommendations == [21, 21, 18]


def test_semantic_v2_run_compiles_without_semantic_rewrite(tmp_path: Path) -> None:
    topic_map, report_plan = _v2_proposals()
    provider = FakeSemanticV2PlanningProvider([topic_map, report_plan])
    summary = build_from_transcript_v2(
        manifest_path=FIXTURE_ROOT / "manifest.json",
        segments_path=FIXTURE_ROOT / "segments.jsonl",
        run_id="semantic-v2-success",
        output_root=tmp_path,
        provider=provider,
    )
    assert summary.state == "RENDERED"
    assert summary.provider_calls == summary.model_calls == 2
    plan = json.loads((summary.run_dir / "report-plan.json").read_text(encoding="utf-8"))
    assert plan["sections"][0]["blocks"][0]["body"] == (
        "第一部分解释问题背景，主要限制需要被明确记录。"
    )
    ledger = json.loads((summary.run_dir / "normalization.json").read_text(encoding="utf-8"))
    assert ledger["summary"]["semantic_rewrite_count"] == 0
    assert ledger["summary"]["semantic_merge_count"] == 0
    assert ledger["summary"]["semantic_split_count"] == 0
    assert ledger["summary"]["semantic_synthesis_count"] == 0
    assert json.loads((summary.run_dir / "assets.json").read_text(encoding="utf-8"))["assets"] == []
    planning_budget = json.loads(
        (summary.run_dir / "planning-budget.json").read_text(encoding="utf-8")
    )
    assert planning_budget["recommended_block_budget"] == 6
    assert planning_budget["formula_version"] == planning_budget["schema_version"]
    budget_diagnostics = json.loads(
        (summary.run_dir / "budget-diagnostics.json").read_text(encoding="utf-8")
    )
    assert budget_diagnostics["actual_compiled_block_count"] == 3
    assert budget_diagnostics["hard_failure"] is False
    planner_request = json.loads(
        (summary.run_dir / "planner-request.json").read_text(encoding="utf-8")
    )
    assert planner_request["planning_budget"] == {
        key: value for key, value in planning_budget.items() if key != "formula_version"
    }
    assert planner_request["frozen_before_call"] is True
    run_payload = json.loads((summary.run_dir / "run.json").read_text(encoding="utf-8"))
    assert run_payload["planning_budget"] == planner_request["planning_budget"]
    assert run_payload["request_snapshots"]["report_planner"] == planner_request
    assert run_payload["config"] == provider.config.public_snapshot()
    assert run_payload["config"]["model"] == "fake-semantic-v2-model"
    assert run_payload["config"]["thinking_mode"] == SEMANTIC_V2_THINKING_MODE
    assert run_payload["config"]["reasoning_effort"] == SEMANTIC_V2_REASONING_EFFORT
    assert run_payload["config"]["output_token_limit"] == SEMANTIC_V2_MAX_OUTPUT_TOKENS
    assert run_payload["config"]["temperature_stability_evidence"] == (
        "excluded_in_thinking_mode"
    )


def test_semantic_v2_allows_one_shared_identical_technical_retry(tmp_path: Path) -> None:
    topic_map, report_plan = _v2_proposals()

    class RetryOnce(FakeSemanticV2PlanningProvider):
        def __init__(self) -> None:
            super().__init__([topic_map, report_plan])
            self.attempts = 0

        def complete(self, stage: str, system_instruction: str, payload: dict[str, object]):
            self.attempts += 1
            if self.attempts == 1:
                raise ProviderCallError(
                    "PROVIDER_ERROR", "temporary connection", 1, retryable=True
                )
            return super().complete(stage, system_instruction, payload)

    provider = RetryOnce()
    summary = build_from_transcript_v2(
        manifest_path=FIXTURE_ROOT / "manifest.json",
        segments_path=FIXTURE_ROOT / "segments.jsonl",
        run_id="semantic-v2-retry",
        output_root=tmp_path,
        provider=provider,
    )
    assert summary.provider_calls == summary.model_calls == 3
    run_payload = json.loads((summary.run_dir / "run.json").read_text(encoding="utf-8"))
    assert run_payload["retry_used"] is True
    calls = [
        json.loads(line)
        for line in (summary.run_dir / "model-calls.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert len(calls) == 3
    assert calls[0]["request_sha256"] == calls[1]["request_sha256"]
    assert calls[0]["retry_eligible"] is True
    assert calls[1]["retry_of_attempt"] == 1
    assert calls[1]["retry_used"] is True


def test_semantic_v2_schema_failure_is_not_retried(tmp_path: Path) -> None:
    provider = FakeSemanticV2PlanningProvider(
        [{"schema_version": SEMANTIC_V2_TOPIC_PROPOSAL_SCHEMA_VERSION, "topics": []}]
    )
    with pytest.raises(PlanningError, match="TOPIC_MAP_SCHEMA_ERROR"):
        build_from_transcript_v2(
            manifest_path=FIXTURE_ROOT / "manifest.json",
            segments_path=FIXTURE_ROOT / "segments.jsonl",
            run_id="semantic-v2-schema-failure",
            output_root=tmp_path,
            provider=provider,
        )
    run_dir = tmp_path / "semantic-v2-schema-failure"
    calls = [json.loads(line) for line in (run_dir / "model-calls.jsonl").read_text().splitlines()]
    assert len(calls) == 1
    assert calls[0]["retry_eligible"] is False
    assert json.loads((run_dir / "run.json").read_text())["provider_calls"] == 1


def test_semantic_v2_replay_is_zero_provider_calls_and_deterministic(tmp_path: Path) -> None:
    topic_map, report_plan = _v2_proposals()
    provider = FakeSemanticV2PlanningProvider([topic_map, report_plan])
    first = build_from_transcript_v2(
        manifest_path=FIXTURE_ROOT / "manifest.json",
        segments_path=FIXTURE_ROOT / "segments.jsonl",
        run_id="semantic-v2-replay-source",
        output_root=tmp_path,
        provider=provider,
    )
    replay = replay_semantic_v2_proposals(
        manifest_path=FIXTURE_ROOT / "manifest.json",
        segments_path=FIXTURE_ROOT / "segments.jsonl",
        topic_proposal_payload=json.loads(
            (first.run_dir / "topic-map.raw.json").read_text(encoding="utf-8")
        ),
        plan_proposal_payload=json.loads(
            (first.run_dir / "report-plan.raw.json").read_text(encoding="utf-8")
        ),
        output_dir=tmp_path / "replay",
    )
    assert replay.provider_calls == replay.model_calls == 0
    assert replay.report_plan_sha256 == __import__("hashlib").sha256(
        (first.run_dir / "report-plan.json").read_bytes()
    ).hexdigest()
    assert replay.topic_map.model_dump(mode="json") == json.loads(
        (first.run_dir / "topic-map.json").read_text(encoding="utf-8")
    )
    for artifact_name in (
        "planning-budget.json",
        "planner-request.json",
        "budget-diagnostics.json",
        "report.html",
    ):
        assert (tmp_path / "replay" / artifact_name).is_file()
    replay_request = json.loads(
        (tmp_path / "replay" / "planner-request.json").read_text(encoding="utf-8")
    )
    assert replay_request["provider_calls"] == replay_request["model_calls"] == 0


def test_semantic_v2_provider_uses_chat_json_object_request() -> None:
    captured: dict[str, object] = {}

    class Completions:
        def create(self, **kwargs: object):
            captured.update(kwargs)
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        finish_reason="stop",
                        message=SimpleNamespace(content='{"ok":true}'),
                    )
                ],
                usage=None,
            )

    client = SimpleNamespace(chat=SimpleNamespace(completions=Completions()))
    config = PlanningConfig(
        provider_label="https://api.deepseek.com",
        model=SEMANTIC_V2_MODEL,
        timeout_seconds=10,
        credential_present=True,
        response_mode=SEMANTIC_V2_RESPONSE_MODE,
        temperature_stability_evidence="excluded_in_thinking_mode",
        thinking_mode=SEMANTIC_V2_THINKING_MODE,
        output_token_limit=SEMANTIC_V2_MAX_OUTPUT_TOKENS,
        reasoning_effort=SEMANTIC_V2_REASONING_EFFORT,
        api_surface="chat_completions",
        schema_mechanism=SEMANTIC_V2_SCHEMA_MECHANISM,
    )
    provider = OpenAISemanticV2PlanningProvider(client, config)  # type: ignore[arg-type]
    result = provider.complete("topic_mapper", "system", {"transcript_segments": ["full"]})
    assert result.raw_text == '{"ok":true}'
    assert captured["temperature"] == 0
    assert captured["max_tokens"] == SEMANTIC_V2_MAX_OUTPUT_TOKENS
    assert captured["response_format"] == {"type": SEMANTIC_V2_RESPONSE_MODE}
    assert captured["reasoning_effort"] == SEMANTIC_V2_REASONING_EFFORT
    assert captured["extra_body"] == {"thinking": {"type": SEMANTIC_V2_THINKING_MODE}}
    messages = captured["messages"]
    assert isinstance(messages, list)
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert "full" in messages[1]["content"]


def test_semantic_v2_request_shape_and_hash_are_stable() -> None:
    config = PlanningConfig(
        provider_label="https://api.deepseek.com",
        model=SEMANTIC_V2_MODEL,
        timeout_seconds=10,
        credential_present=True,
        response_mode=SEMANTIC_V2_RESPONSE_MODE,
        temperature_stability_evidence="excluded_in_thinking_mode",
        thinking_mode=SEMANTIC_V2_THINKING_MODE,
        output_token_limit=SEMANTIC_V2_MAX_OUTPUT_TOKENS,
        reasoning_effort=SEMANTIC_V2_REASONING_EFFORT,
        api_surface="chat_completions",
        schema_mechanism=SEMANTIC_V2_SCHEMA_MECHANISM,
    )
    payload = {"transcript_segments": ["full"], "output_contract": {"json_schema": {}}}
    request = semantic_v2_chat_completion_request("topic_mapper", "system", payload, config)
    assert request == {
        "model": SEMANTIC_V2_MODEL,
        "messages": [
            {"role": "system", "content": "system"},
            {
                "role": "user",
                "content": (
                    '{"output_contract":{"json_schema":{}},'
                    '"transcript_segments":["full"]}'
                ),
            },
        ],
        "temperature": 0,
        "max_tokens": SEMANTIC_V2_MAX_OUTPUT_TOKENS,
        "response_format": {"type": SEMANTIC_V2_RESPONSE_MODE},
        "reasoning_effort": SEMANTIC_V2_REASONING_EFFORT,
        "extra_body": {"thinking": {"type": SEMANTIC_V2_THINKING_MODE}},
    }
    first = _semantic_v2_request_sha256("topic_mapper", "system", payload, config)
    second = _semantic_v2_request_sha256("topic_mapper", "system", payload, config)
    changed = _semantic_v2_request_sha256(
        "report_planner", "system", payload, config
    )
    assert first == second
    assert first != changed


@pytest.mark.parametrize("raw_response", ["not-json", "{"])
def test_semantic_v2_malformed_outputs_retain_one_identical_retry(
    tmp_path: Path, raw_response: str
) -> None:
    provider = FakeSemanticV2PlanningProvider([raw_response, raw_response])
    with pytest.raises(PlanningError, match="MODEL_OUTPUT_PARSE_ERROR"):
        build_from_transcript_v2(
            manifest_path=FIXTURE_ROOT / "manifest.json",
            segments_path=FIXTURE_ROOT / "segments.jsonl",
            run_id="semantic-v2-malformed-output",
            output_root=tmp_path,
            provider=provider,
        )
    run_dir = tmp_path / "semantic-v2-malformed-output"
    calls = [
        json.loads(line)
        for line in (run_dir / "model-calls.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert len(calls) == 2
    assert calls[0]["retry_eligible"] is True
    assert calls[1]["retry_eligible"] is True
    assert calls[0]["request_sha256"] == calls[1]["request_sha256"]
    assert calls[1]["retry_of_attempt"] == 1
    assert json.loads((run_dir / "run.json").read_text(encoding="utf-8"))["provider_calls"] == 2


def test_semantic_v2_incomplete_output_is_retained_with_one_retry(tmp_path: Path) -> None:
    topic_map, _ = _v2_proposals()

    class IncompleteProvider(FakeSemanticV2PlanningProvider):
        def __init__(self) -> None:
            super().__init__([topic_map, topic_map])

        def complete(self, stage: str, system_instruction: str, payload: dict[str, object]):
            result = super().complete(stage, system_instruction, payload)
            return ProviderResult(
                raw_text=result.raw_text,
                usage=result.usage,
                latency_ms=result.latency_ms,
                finish_reason="length",
                content_present=result.content_present,
                content_bytes=result.content_bytes,
                content_sha256=result.content_sha256,
            )

    provider = IncompleteProvider()
    with pytest.raises(PlanningError, match="MODEL_OUTPUT_INCOMPLETE"):
        build_from_transcript_v2(
            manifest_path=FIXTURE_ROOT / "manifest.json",
            segments_path=FIXTURE_ROOT / "segments.jsonl",
            run_id="semantic-v2-incomplete-output",
            output_root=tmp_path,
            provider=provider,
        )
    run_dir = tmp_path / "semantic-v2-incomplete-output"
    calls = [
        json.loads(line)
        for line in (run_dir / "model-calls.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert len(calls) == 2
    assert all(call["error_category"] == "MODEL_OUTPUT_INCOMPLETE" for call in calls)
    assert calls[0]["request_sha256"] == calls[1]["request_sha256"]
