from __future__ import annotations

import json
import threading
import time
from pathlib import Path
from types import SimpleNamespace
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from video_evidence_agent.schemas import VideoSegment
from video_evidence_agent.visual_report.planning import (
    SEMANTIC_V2_PLAN_PROPOSAL_SCHEMA_VERSION,
    SEMANTIC_V2_TOPIC_PROPOSAL_SCHEMA_VERSION,
    FakeSemanticV2PlanningProvider,
)
from video_evidence_agent.visual_report.url_ingest import (
    BilibiliSource,
    DownloadResult,
    IngestResult,
    UrlIngestError,
    clean_bilibili_url,
    download_bilibili_video,
    ingest_downloaded_video,
    validate_bilibili_url,
)
from video_evidence_agent.visual_report.web import UrlIngestWebApp, create_web_server


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


def _synthetic_source(download: DownloadResult, run_dir: Path) -> IngestResult:
    video_id = download.source.video_id
    artifact_root = run_dir / "ingest" / video_id
    artifact_root.mkdir(parents=True)
    segments = [
        VideoSegment(
            video_id=video_id,
            segment_id=f"{video_id}-seg-{index:03d}",
            ordinal=index,
            start_ms=index * 1000,
            end_ms=(index + 1) * 1000,
            transcript_text=f"第{index + 1}段说明视频中的一个具体步骤。",
            source_asr_ordinals=(index,),
        )
        for index in range(6)
    ]
    (artifact_root / "segments.jsonl").write_text(
        "".join(
            json.dumps(item.model_dump(mode="json"), ensure_ascii=False) + "\n"
            for item in segments
        ),
        encoding="utf-8",
    )
    (artifact_root / "manifest.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "pipeline_status": "SUCCEEDED",
                "video_id": video_id,
                "source": {
                    "path": str(download.media_path),
                    "origin_url": download.source.canonical_url,
                    "attribution": download.attribution,
                    "duration_ms": 6000,
                },
                "segmenting": {"segment_count": len(segments)},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return IngestResult(
        video_id=video_id,
        artifact_root=artifact_root,
        manifest_path=artifact_root / "manifest.json",
        segments_path=artifact_root / "segments.jsonl",
        command=("video-evidence", "ingest"),
    )


def _proposals(source: BilibiliSource) -> tuple[dict[str, object], dict[str, object]]:
    ids = [f"{source.video_id}-seg-{index:03d}" for index in range(6)]
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
    plan = {
        "schema_version": SEMANTIC_V2_PLAN_PROPOSAL_SCHEMA_VERSION,
        "hero": {"title": "可追溯执行", "tldr": "保留来源和重点。", "source_segment_ids": [ids[0]]},
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
    return topic_map, plan


@pytest.mark.parametrize(
    ("submitted_url", "expected_url"),
    (
        (
            "https://www.bilibili.com/video/BV1HM4m1U7bM/?spm_id_from=xxx&vd_source=xxx&p=3",
            "https://www.bilibili.com/video/BV1HM4m1U7bM/?p=3",
        ),
        (
            "https://bilibili.com/video/BV1HM4m1U7bM/?spm_id_from=xxx&vd_source=xxx",
            "https://www.bilibili.com/video/BV1HM4m1U7bM/",
        ),
    ),
)
def test_bilibili_url_cleaning_keeps_only_bvid_and_numeric_page(
    submitted_url: str, expected_url: str
) -> None:
    assert clean_bilibili_url(submitted_url) == expected_url
    source = validate_bilibili_url(submitted_url)
    assert source.bvid == "BV1HM4m1U7bM"
    assert source.submitted_url == submitted_url
    assert source.canonical_url == expected_url
    assert source.video_id == "bilibili-BV1HM4m1U7bM"
    for value in (
        "http://www.bilibili.com/video/BV1HM4m1U7bM",
        "https://example.com/video/BV1HM4m1U7bM",
        "https://www.bilibili.com/video/BV1HM4m1U7bM/extra",
        "https://www.bilibili.com/video/BV1HM4m1U7bM/?p=3#page",
        "https://www.bilibili.com/",
    ):
        with pytest.raises(UrlIngestError) as error:
            validate_bilibili_url(value)
        assert error.value.category == "URL_INVALID"


def test_download_adapter_uses_frozen_argv_and_verifies_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = validate_bilibili_url(
        "https://www.bilibili.com/video/BV1HM4m1U7bM/?spm_id_from=xxx&vd_source=xxx&p=3"
    )
    observed: dict[str, object] = {}

    def runner(command: list[str], **kwargs: object) -> SimpleNamespace:
        observed["command"] = command
        observed["kwargs"] = kwargs
        download_dir = Path(command[command.index("-P") + 1])
        download_dir.mkdir(parents=True, exist_ok=True)
        media_path = download_dir / "source.mp4"
        media_path.write_bytes(b"media")
        (download_dir / "source.info.json").write_text(
            json.dumps({"title": "测试视频", "uploader": "测试作者"}), encoding="utf-8"
        )
        return SimpleNamespace(returncode=0, stdout=str(media_path) + "\n")

    monkeypatch.setattr(
        "video_evidence_agent.visual_report.url_ingest.shutil.which",
        lambda name: "/opt/homebrew/bin/yt-dlp" if name == "yt-dlp" else None,
    )
    result = download_bilibili_video(source, tmp_path, runner=runner)
    assert result.media_path == (tmp_path / "download" / "source.mp4").resolve()
    assert result.title == "测试视频"
    assert result.uploader == "测试作者"
    assert observed["command"] == [
        "/opt/homebrew/bin/yt-dlp",
        "--ignore-config",
        "--no-playlist",
        "-P",
        str((tmp_path / "download").resolve()),
        "-o",
        "source.%(ext)s",
        "-S",
        "res:1080,vcodec:h264,acodec:aac",
        "--merge-output-format",
        "mp4",
        "--write-info-json",
        "--print",
        "after_move:filepath",
        source.canonical_url,
    ]
    assert observed["kwargs"] == {
        "capture_output": True,
        "text": True,
        "check": False,
        "shell": False,
    }


def test_existing_ingest_boundary_uses_command_and_requires_success(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = validate_bilibili_url("https://www.bilibili.com/video/BV1HM4m1U7bM")
    download_dir = tmp_path / "download"
    download_dir.mkdir()
    media_path = download_dir / "source.mp4"
    media_path.write_bytes(b"media")
    info_path = download_dir / "source.info.json"
    info_path.write_text("{}", encoding="utf-8")
    download = DownloadResult(
        source=source,
        media_path=media_path,
        info_path=info_path,
        title="测试视频",
        uploader="测试作者",
        attribution="Bilibili；测试作者；《测试视频》；" + source.canonical_url,
        command=("yt-dlp",),
    )
    observed: dict[str, object] = {}

    def runner(command: list[str], **kwargs: object) -> SimpleNamespace:
        observed["command"] = command
        observed["kwargs"] = kwargs
        _synthetic_source(download, tmp_path)
        return SimpleNamespace(returncode=0, stdout="ingested\n")

    monkeypatch.setattr(
        "video_evidence_agent.visual_report.url_ingest.shutil.which",
        lambda name: "/venv/bin/video-evidence" if name == "video-evidence" else None,
    )
    result = ingest_downloaded_video(download, tmp_path, runner=runner)
    assert result.video_id == source.video_id
    assert result.manifest_path.is_file()
    command = observed["command"]
    assert isinstance(command, list)
    assert command[:2] == ["/venv/bin/video-evidence", "ingest"]
    assert "--no-playlist" not in command
    assert observed["kwargs"] == {
        "capture_output": True,
        "text": True,
        "check": False,
        "shell": False,
    }


def test_url_web_composes_one_run_and_serves_canonical_report(tmp_path: Path) -> None:
    submitted_url = (
        "https://www.bilibili.com/video/BV1HM4m1U7bM/"
        "?spm_id_from=xxx&vd_source=xxx&p=3"
    )
    source = validate_bilibili_url(submitted_url)
    topic_map, report_plan = _proposals(source)
    provider = FakeSemanticV2PlanningProvider([topic_map, report_plan])
    started = threading.Event()
    release = threading.Event()

    def downloader(current_source: BilibiliSource, run_dir: Path) -> DownloadResult:
        started.set()
        release.wait(timeout=5)
        download_dir = run_dir / "download"
        download_dir.mkdir(parents=True)
        media_path = download_dir / "source.mp4"
        media_path.write_bytes(b"media")
        info_path = download_dir / "source.info.json"
        info_path.write_text(
            json.dumps({"title": "测试视频", "uploader": "测试作者"}), encoding="utf-8"
        )
        return DownloadResult(
            source=current_source,
            media_path=media_path,
            info_path=info_path,
            title="测试视频",
            uploader="测试作者",
            attribution="Bilibili；测试作者；《测试视频》；" + current_source.canonical_url,
            command=("yt-dlp",),
        )

    def ingestor(download: DownloadResult, run_dir: Path) -> IngestResult:
        return _synthetic_source(download, run_dir)

    app = UrlIngestWebApp(
        artifact_root=tmp_path / "runs",
        provider_factory=lambda: provider,
        downloader=downloader,
        ingestor=ingestor,
    )
    server = create_web_server(app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        status, page, _ = _request(base_url, "/visual-report/")
        assert status == 200
        assert isinstance(page, bytes)
        assert 'name="url"' in page.decode("utf-8")
        assert "OPENAI_API_KEY" not in page.decode("utf-8")

        status, invalid, _ = _request(
            base_url,
            "/api/visual-report/runs",
            method="POST",
            payload={
                "url": "https://example.com/video/BV1HM4m1U7bM",
                "client_request_id": "bad-001",
            },
        )
        assert status == 400
        assert invalid == {"error_category": "URL_INVALID"}
        assert provider.provider_calls == 0

        request_payload = {
            "url": submitted_url,
            "client_request_id": "url-web-001",
        }
        status, first, _ = _request(
            base_url, "/api/visual-report/runs", method="POST", payload=request_payload
        )
        assert status == 202
        assert isinstance(first, dict)
        run_id = str(first["run_id"])
        assert started.wait(timeout=5)
        status, downloading, _ = _request(base_url, f"/api/visual-report/runs/{run_id}")
        assert status == 200
        assert isinstance(downloading, dict)
        assert downloading["state"] == "CREATED"
        assert downloading["stage"] == "DOWNLOADING"

        release.set()
        rendered = _wait_for_state(base_url, run_id, "RENDERED")
        assert rendered["stage"] == "RENDERED"
        assert rendered["report_url"] == f"/visual-report/runs/{run_id}/report"
        assert provider.provider_calls == 2

        status, duplicate, _ = _request(
            base_url, "/api/visual-report/runs", method="POST", payload=request_payload
        )
        assert status == 200
        assert isinstance(duplicate, dict)
        assert duplicate["duplicate"] is True
        assert duplicate["run_id"] == run_id

        status, report, headers = _request(base_url, str(rendered["report_url"]))
        assert status == 200
        assert headers["Content-Type"].startswith("text/html")
        assert isinstance(report, bytes)
        assert b"report.html" not in report
        run_payload = json.loads((tmp_path / "runs" / run_id / "run.json").read_text())
        assert run_payload["url_ingest"]["status"] == "RENDERED"
        assert (tmp_path / "runs" / run_id / "download" / "source.mp4").is_file()
        assert (tmp_path / "runs" / run_id / "ingest" / source.video_id / "manifest.json").is_file()
    finally:
        release.set()
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_url_web_queues_second_run_and_starts_it_automatically(tmp_path: Path) -> None:
    first_started = threading.Event()
    release_first = threading.Event()
    download_order: list[str] = []

    def downloader(source: BilibiliSource, run_dir: Path) -> DownloadResult:
        download_order.append(source.bvid)
        if len(download_order) == 1:
            first_started.set()
            release_first.wait(timeout=5)
        download_dir = run_dir / "download"
        download_dir.mkdir(parents=True)
        media_path = download_dir / "source.mp4"
        media_path.write_bytes(b"media")
        info_path = download_dir / "source.info.json"
        info_path.write_text(
            json.dumps({"title": source.bvid, "uploader": "测试作者"}), encoding="utf-8"
        )
        return DownloadResult(
            source=source,
            media_path=media_path,
            info_path=info_path,
            title=source.bvid,
            uploader="测试作者",
            attribution=f"Bilibili；测试作者；《{source.bvid}》；{source.canonical_url}",
            command=("yt-dlp",),
        )

    def run_builder(**kwargs: object) -> None:
        recorder = kwargs["recorder"]
        for state in ("MAPPING", "TOPIC_MAPPED", "PLANNING", "PLAN_VALIDATED"):
            recorder.transition(state)
        (recorder.run_dir / "report.html").write_text("<h1>report</h1>", encoding="utf-8")
        recorder.transition("RENDERED")

    app = UrlIngestWebApp(
        artifact_root=tmp_path / "runs",
        downloader=downloader,
        ingestor=_synthetic_source,
        run_builder=run_builder,
    )
    server = create_web_server(app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        first_status, first, _ = _request(
            base_url,
            "/api/visual-report/runs",
            method="POST",
            payload={
                "url": "https://www.bilibili.com/video/BV1HM4m1U7bM",
                "client_request_id": "queue-001",
            },
        )
        assert first_status == 202
        assert isinstance(first, dict)
        first_run_id = str(first["run_id"])
        assert first_started.wait(timeout=5)

        second_status, second, _ = _request(
            base_url,
            "/api/visual-report/runs",
            method="POST",
            payload={
                "url": "https://www.bilibili.com/video/BV1RxWnzbE7g",
                "client_request_id": "queue-002",
            },
        )
        assert second_status == 202
        assert isinstance(second, dict)
        second_run_id = str(second["run_id"])
        assert second["state"] == "CREATED"
        assert second["stage"] == "QUEUED"
        assert second["queue_position"] == 1
        assert second["active_run_id"] == first_run_id
        assert download_order == ["BV1HM4m1U7bM"]
        assert (tmp_path / "runs" / second_run_id / "run.json").is_file()

        page_status, page, _ = _request(base_url, "/visual-report/")
        assert page_status == 200
        assert isinstance(page, bytes)
        assert "等待处理" in page.decode("utf-8")
        assert "完成后会自动开始" in page.decode("utf-8")

        release_first.set()
        _wait_for_state(base_url, first_run_id, "RENDERED")
        second_rendered = _wait_for_state(base_url, second_run_id, "RENDERED")
        assert second_rendered["stage"] == "RENDERED"
        assert second_rendered["queue_position"] == 0
        assert download_order == ["BV1HM4m1U7bM", "BV1RxWnzbE7g"]
        assert (tmp_path / "runs" / first_run_id / "report.html").is_file()
        assert (tmp_path / "runs" / second_run_id / "report.html").is_file()
    finally:
        release_first.set()
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_url_web_download_failure_is_safe_and_retained(tmp_path: Path) -> None:
    def downloader(source: BilibiliSource, run_dir: Path) -> DownloadResult:
        raise UrlIngestError("DOWNLOAD_ERROR", "external-debug-secret")

    app = UrlIngestWebApp(artifact_root=tmp_path / "runs", downloader=downloader)
    server = create_web_server(app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        status, first, _ = _request(
            base_url,
            "/api/visual-report/runs",
            method="POST",
            payload={
                "url": "https://www.bilibili.com/video/BV1HM4m1U7bM",
                "client_request_id": "url-failure-001",
            },
        )
        assert status == 202
        assert isinstance(first, dict)
        failed = _wait_for_state(base_url, str(first["run_id"]), "FAILED")
        assert failed["error_category"] == "DOWNLOAD_ERROR"
        assert failed["report_url"] is None
        run_path = tmp_path / "runs" / str(first["run_id"]) / "run.json"
        run_payload = json.loads(run_path.read_text())
        run_text = json.dumps(run_payload)
        assert "external-debug-secret" not in run_text
        assert "OPENAI_API_KEY" not in run_text
        assert run_payload["error"] == {
            "category": "DOWNLOAD_ERROR",
            "message": "url ingest failed",
        }
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
