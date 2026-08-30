from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from video_evidence_agent.schemas import VideoSegment
from video_evidence_agent.visual_report.planning import (
    SEMANTIC_V2_PLAN_PROPOSAL_SCHEMA_VERSION,
    SEMANTIC_V2_TOPIC_PROPOSAL_SCHEMA_VERSION,
    FakeSemanticV2PlanningProvider,
    PlanningError,
    normalize_semantic_v2_topic_proposal,
)
from video_evidence_agent.visual_report.planning_runtime import (
    OpenAISemanticV2PlanningProvider,
    PlanningConfig,
    ProviderCallError,
    build_from_transcript_v2,
    replay_semantic_v2_proposals,
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
        model="deepseek-chat",
        timeout_seconds=10,
        credential_present=True,
        response_mode="json_object",
        api_surface="chat_completions",
        schema_mechanism="chat.completions.response_format.json_object",
    )
    provider = OpenAISemanticV2PlanningProvider(client, config)  # type: ignore[arg-type]
    result = provider.complete("topic_mapper", "system", {"transcript_segments": ["full"]})
    assert result.raw_text == '{"ok":true}'
    assert captured["temperature"] == 0
    assert captured["response_format"] == {"type": "json_object"}
    messages = captured["messages"]
    assert isinstance(messages, list)
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert "full" in messages[1]["content"]
