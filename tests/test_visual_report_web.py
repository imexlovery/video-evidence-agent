from __future__ import annotations

import json
import threading
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from video_evidence_agent.visual_report.planning import (
    SEMANTIC_V2_PLAN_PROPOSAL_SCHEMA_VERSION,
    SEMANTIC_V2_TOPIC_PROPOSAL_SCHEMA_VERSION,
    FakeSemanticV2PlanningProvider,
)
from video_evidence_agent.visual_report.planning_runtime import load_source
from video_evidence_agent.visual_report.web import (
    ALLOWED_VIDEO_IDS,
    VisualReportWebApp,
    create_web_server,
)

SOURCE_ROOT = Path("/Users/tristana/Develop/video-evidence-agent")


def _source_paths(video_id: str) -> tuple[Path, Path]:
    base = SOURCE_ROOT / "artifacts" / "p0b-ingest" / video_id
    return base / "manifest.json", base / "segments.jsonl"


def _proposals(video_id: str) -> tuple[dict[str, object], dict[str, object]]:
    manifest_path, segments_path = _source_paths(video_id)
    source = load_source(manifest_path, segments_path)
    ids = [segment.segment_id for segment in source.segments]
    topic_map = {
        "schema_version": SEMANTIC_V2_TOPIC_PROPOSAL_SCHEMA_VERSION,
        "topics": [
            {
                "title": "背景",
                "summary": "说明背景和约束。",
                "importance": "primary",
                "start_segment_id": ids[0],
                "end_segment_id": ids[1],
                "representative_segment_ids": [ids[0]],
            },
            {
                "title": "方案",
                "summary": "说明方案选择。",
                "importance": "primary",
                "start_segment_id": ids[2],
                "end_segment_id": ids[3],
                "representative_segment_ids": [ids[2]],
            },
            {
                "title": "执行",
                "summary": "说明执行步骤。",
                "importance": "primary",
                "start_segment_id": ids[4],
                "end_segment_id": ids[5],
                "representative_segment_ids": [ids[4]],
            },
        ],
    }
    report_plan = {
        "schema_version": SEMANTIC_V2_PLAN_PROPOSAL_SCHEMA_VERSION,
        "hero": {"title": "可追溯执行", "tldr": "保留来源和重点。", "source_segment_ids": [ids[6]]},
        "sections": [
            {
                "title": "背景",
                "topic_ids": ["topic-001"],
                "content_units": [
                    {
                        "suggested_block_type": "insight_card",
                        "headline": "明确背景",
                        "body": "这部分记录背景和约束。",
                        "topic_ids": ["topic-001"],
                        "source_segment_ids": [ids[0], ids[1]],
                    }
                ],
            },
            {
                "title": "方案",
                "topic_ids": ["topic-002"],
                "content_units": [
                    {
                        "suggested_block_type": "insight_card",
                        "headline": "选择方案",
                        "body": "这部分记录方案选择。",
                        "topic_ids": ["topic-002"],
                        "source_segment_ids": [ids[2], ids[3]],
                    }
                ],
            },
            {
                "title": "执行",
                "topic_ids": ["topic-003"],
                "content_units": [
                    {
                        "suggested_block_type": "takeaway_box",
                        "headline": "执行步骤",
                        "items": ["准备", "执行", "复盘"],
                        "topic_ids": ["topic-003"],
                        "source_segment_ids": [ids[4], ids[5]],
                    }
                ],
            },
        ],
    }
    return topic_map, report_plan


def _request(
    base_url: str, path: str, *, method: str = "GET", payload: object | None = None
) -> tuple[int, dict[str, object] | bytes, dict[str, str]]:
    body = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = Request(base_url + path, data=body, headers=headers, method=method)
    try:
        with urlopen(request, timeout=5) as response:
            content = response.read()
            status = response.status
            response_headers = {key: value for key, value in response.headers.items()}
    except HTTPError as exc:
        content = exc.read()
        status = exc.code
        response_headers = {key: value for key, value in exc.headers.items()}
    if response_headers.get("Content-Type", "").startswith("application/json"):
        return status, json.loads(content.decode("utf-8")), response_headers
    return status, content, response_headers


@pytest.fixture
def web_server(tmp_path: Path):
    topic_map, report_plan = _proposals("p0b-kling-2024")
    provider = FakeSemanticV2PlanningProvider([topic_map, report_plan])
    app = VisualReportWebApp(
        source_root=SOURCE_ROOT,
        artifact_root=tmp_path / "runs",
        provider_factory=lambda: provider,
    )
    server = create_web_server(app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    yield app, provider, base_url
    server.shutdown()
    server.server_close()
    thread.join(timeout=5)


def _wait_for_state(base_url: str, run_id: str, state: str) -> dict[str, object]:
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        status, payload, _ = _request(base_url, f"/api/visual-report/runs/{run_id}")
        assert status == 200
        assert isinstance(payload, dict)
        if payload["state"] == state:
            return payload
        time.sleep(0.01)
    raise AssertionError(f"run did not reach {state}")


def test_web_sources_and_page_are_allowlisted_and_provider_free(web_server) -> None:
    _, provider, base_url = web_server
    status, sources, _ = _request(base_url, "/api/visual-report/sources")
    assert status == 200
    assert isinstance(sources, dict)
    assert [row["video_id"] for row in sources["sources"]] == list(ALLOWED_VIDEO_IDS)
    assert all(
        set(row) == {"video_id", "title", "duration_ms", "segment_count"}
        for row in sources["sources"]
    )

    status, page, headers = _request(base_url, "/visual-report/")
    assert status == 200
    assert headers["Content-Type"].startswith("text/html")
    assert isinstance(page, bytes)
    page_text = page.decode("utf-8")
    assert "OPENAI_API_KEY" not in page_text
    assert "/api/visual-report/sources" in page_text
    assert provider.provider_calls == 0


def test_web_run_replay_reuses_run_and_serves_canonical_report(web_server) -> None:
    _, provider, base_url = web_server
    request_payload = {
        "video_id": "p0b-kling-2024",
        "client_request_id": "browser-replay-001",
    }
    status, first, _ = _request(
        base_url, "/api/visual-report/runs", method="POST", payload=request_payload
    )
    assert status == 202
    assert isinstance(first, dict)
    run_id = str(first["run_id"])
    assert first["report_url"] is None
    rendered = _wait_for_state(base_url, run_id, "RENDERED")
    assert rendered["report_url"] == f"/visual-report/runs/{run_id}/report"
    assert provider.provider_calls == 2

    status, duplicate, _ = _request(
        base_url, "/api/visual-report/runs", method="POST", payload=request_payload
    )
    assert status == 200
    assert isinstance(duplicate, dict)
    assert duplicate["duplicate"] is True
    assert duplicate["run_id"] == run_id
    assert provider.provider_calls == 2

    status, report, headers = _request(base_url, str(rendered["report_url"]))
    assert status == 200
    assert headers["Content-Type"].startswith("text/html")
    assert isinstance(report, bytes)
    assert b"report.html" not in report


def test_web_active_run_rejects_other_request_without_provider_call(tmp_path: Path) -> None:
    topic_map, report_plan = _proposals("p0b-kling-2024")
    started = threading.Event()
    release = threading.Event()

    class BlockingProvider(FakeSemanticV2PlanningProvider):
        def complete(self, stage: str, system_instruction: str, payload: dict[str, object]):
            result = super().complete(stage, system_instruction, payload)
            started.set()
            release.wait(timeout=5)
            return result

    provider = BlockingProvider([topic_map, report_plan])
    app = VisualReportWebApp(
        source_root=SOURCE_ROOT,
        artifact_root=tmp_path / "runs",
        provider_factory=lambda: provider,
    )
    server = create_web_server(app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        status, first, _ = _request(
            base_url,
            "/api/visual-report/runs",
            method="POST",
            payload={"video_id": "p0b-kling-2024", "client_request_id": "active-001"},
        )
        assert status == 202
        assert isinstance(first, dict)
        assert started.wait(timeout=5)
        status, rejected, _ = _request(
            base_url,
            "/api/visual-report/runs",
            method="POST",
            payload={"video_id": "p0b-rlinf-2026", "client_request_id": "active-002"},
        )
        assert status == 409
        assert rejected == {"error_category": "RUN_ACTIVE"}
        assert provider.provider_calls == 1
        release.set()
        _wait_for_state(base_url, str(first["run_id"]), "RENDERED")
    finally:
        release.set()
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_web_invalid_video_and_traversal_never_start_provider(tmp_path: Path) -> None:
    calls = 0

    def factory() -> object:
        nonlocal calls
        calls += 1
        return FakeSemanticV2PlanningProvider([])

    app = VisualReportWebApp(
        source_root=SOURCE_ROOT,
        artifact_root=tmp_path / "runs",
        provider_factory=factory,
    )
    server = create_web_server(app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        status, payload, _ = _request(
            base_url,
            "/api/visual-report/runs",
            method="POST",
            payload={"video_id": "../secret", "client_request_id": "bad-video"},
        )
        assert status == 400
        assert payload == {"error_category": "VIDEO_NOT_ALLOWLISTED"}
        status, payload, _ = _request(base_url, "/api/visual-report/runs/%2e%2e%2fsecret")
        assert status == 404
        assert payload == {"error_category": "RUN_NOT_FOUND"}
        assert calls == 0
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_web_failure_has_safe_status_and_no_report_url(tmp_path: Path) -> None:
    provider = FakeSemanticV2PlanningProvider(["not-json", "not-json"])
    app = VisualReportWebApp(
        source_root=SOURCE_ROOT,
        artifact_root=tmp_path / "runs",
        provider_factory=lambda: provider,
    )
    server = create_web_server(app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        status, first, _ = _request(
            base_url,
            "/api/visual-report/runs",
            method="POST",
            payload={"video_id": "p0b-kling-2024", "client_request_id": "failure-001"},
        )
        assert status == 202
        assert isinstance(first, dict)
        failed = _wait_for_state(base_url, str(first["run_id"]), "FAILED")
        assert failed["error_category"] == "MODEL_OUTPUT_PARSE_ERROR"
        assert failed["report_url"] is None
        status, payload, _ = _request(
            base_url, f"/visual-report/runs/{first['run_id']}/report"
        )
        assert status == 409
        assert payload == {"error_category": "REPORT_NOT_READY"}
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
