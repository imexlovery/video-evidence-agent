import json
from pathlib import Path

import pytest

from video_evidence_agent.visual_report.models import (
    AssetManifest,
    ReportPlan,
)
from video_evidence_agent.visual_report.renderer import (
    RenderError,
    load_plan,
    render_report,
    resolve_assets,
)


def _source_ref() -> dict[str, object]:
    return {
        "segment_id": "demo-video-seg-000",
        "start_ms": 0,
        "end_ms": 500,
    }


def _block(block_id: str, block_type: str, **fields: object) -> dict[str, object]:
    return {
        "block_id": block_id,
        "type": block_type,
        "source_refs": [_source_ref()],
        **fields,
    }


def _plan() -> dict[str, object]:
    return {
        "schema_version": "visual-report.v0-prototype",
        "report_id": "demo-report",
        "video": {
            "video_id": "demo-video",
            "title": "测试技术视频",
            "duration_ms": 1000,
            "source_url": "https://example.test/video",
            "attribution": "本地测试来源。",
        },
        "hero": {
            "eyebrow": "VIDEO VISUAL REPORT",
            "title": "一个可追溯的测试报告",
            "tldr": "把结构化内容渲染成可读的离线页面。",
        },
        "sections": [
            {
                "section_id": "one",
                "kicker": "01 / START",
                "title": "第一段",
                "timestamp_ms": 0,
                "blocks": [
                    _block(
                        "insight",
                        "insight_card",
                        headline="安全文本",
                        body="<script>alert('x')</script> & quotes",
                    ),
                    _block(
                        "bullets",
                        "bullet_group",
                        headline="并列事实",
                        items=["事实一", "事实二"],
                    ),
                    _block(
                        "metrics",
                        "metric_row",
                        headline="两个数值",
                        items=[
                            {"value": "2", "label": "项目", "context": "测试"},
                            {"value": "1", "label": "页面"},
                        ],
                    ),
                    _block(
                        "comparison",
                        "comparison_card",
                        headline="左右对照",
                        left={"label": "LEFT", "items": ["起点"]},
                        right={"label": "RIGHT", "items": ["变化"]},
                    ),
                    _block(
                        "process",
                        "process_flow",
                        headline="三步流程",
                        steps=[
                            {"title": "一", "body": "先看来源"},
                            {"title": "二", "body": "再做结构"},
                            {"title": "三", "body": "最后渲染"},
                        ],
                    ),
                    _block(
                        "image-a",
                        "image_caption",
                        headline="第一张证据帧",
                        body="说明文字",
                        asset_id="frame-a",
                    ),
                    _block(
                        "takeaway",
                        "takeaway_box",
                        headline="带走三点",
                        takeaways=["一点", "两点"],
                    ),
                ],
            },
            {
                "section_id": "two",
                "kicker": "02 / MIDDLE",
                "title": "第二段",
                "timestamp_ms": 300,
                "blocks": [
                    _block(
                        "image-b",
                        "image_caption",
                        headline="第二张证据帧",
                        asset_id="frame-b",
                    )
                ],
            },
            {
                "section_id": "three",
                "kicker": "03 / END",
                "title": "第三段",
                "timestamp_ms": 600,
                "blocks": [
                    _block(
                        "closing",
                        "insight_card",
                        headline="结尾",
                        body="一个结论。",
                    )
                ],
            },
        ],
    }


def _assets() -> dict[str, object]:
    return {
        "schema_version": "visual-report-assets.v0-prototype",
        "assets": [
            {
                "asset_id": "frame-a",
                "type": "keyframe",
                "timestamp_ms": 100,
                "path": "assets/frame-a.jpg",
                "alt": "第一张测试帧",
                "caption": "第一张测试帧说明。",
            },
            {
                "asset_id": "frame-b",
                "type": "keyframe",
                "timestamp_ms": 700,
                "path": "assets/frame-b.jpg",
                "alt": "第二张测试帧",
                "caption": "第二张测试帧说明。",
            },
        ],
    }


def _write_fixture(tmp_path: Path) -> tuple[Path, Path, Path]:
    artifact_dir = tmp_path / "artifact"
    assets_dir = artifact_dir / "assets"
    assets_dir.mkdir(parents=True)
    (assets_dir / "frame-a.jpg").write_bytes(b"fake-jpeg-a")
    (assets_dir / "frame-b.jpg").write_bytes(b"fake-jpeg-b")
    plan_path = artifact_dir / "report-plan.json"
    assets_path = artifact_dir / "assets.json"
    output_path = artifact_dir / "report.html"
    plan_path.write_text(json.dumps(_plan(), ensure_ascii=False), encoding="utf-8")
    assets_path.write_text(json.dumps(_assets(), ensure_ascii=False), encoding="utf-8")
    return plan_path, assets_path, output_path


def test_schema_accepts_all_seven_closed_block_types() -> None:
    plan = ReportPlan.model_validate(_plan())
    block_types = {block.type for block in plan.sections[0].blocks}

    assert block_types == {
        "insight_card",
        "bullet_group",
        "metric_row",
        "comparison_card",
        "process_flow",
        "image_caption",
        "takeaway_box",
    }


def test_real_components_render_and_escape_authored_text(tmp_path: Path) -> None:
    plan_path, assets_path, output_path = _write_fixture(tmp_path)

    summary = render_report(plan_path, assets_path, output_path)
    rendered = output_path.read_text(encoding="utf-8")

    assert summary.section_count == 3
    assert summary.block_count == 9
    assert summary.used_asset_count == 2
    assert 'data-block-type="process_flow"' in rendered
    assert 'data-block-type="takeaway_box"' in rendered
    assert "&lt;script&gt;alert(&#x27;x&#x27;)&lt;/script&gt;" in rendered
    assert "<script>alert" not in rendered
    assert 'src="https://' not in rendered
    assert 'href="https://' not in rendered
    assert "data-source-refs=" in rendered
    assert "00:00" in rendered


def test_repeat_render_is_deterministic(tmp_path: Path) -> None:
    plan_path, assets_path, output_path = _write_fixture(tmp_path)

    render_report(plan_path, assets_path, output_path)
    first = output_path.read_text(encoding="utf-8")
    render_report(plan_path, assets_path, output_path)

    assert output_path.read_text(encoding="utf-8") == first


def test_invalid_plan_fails_without_replacing_prior_output(tmp_path: Path) -> None:
    plan_path, assets_path, output_path = _write_fixture(tmp_path)
    render_report(plan_path, assets_path, output_path)
    prior = output_path.read_text(encoding="utf-8")

    plan_path.write_text("{\"schema_version\": \"visual-report.v0-prototype\"}", encoding="utf-8")
    with pytest.raises(RenderError, match="PLAN_SCHEMA_ERROR"):
        render_report(plan_path, assets_path, output_path)

    assert output_path.read_text(encoding="utf-8") == prior


def test_unknown_block_and_extra_layout_fields_fail_closed(tmp_path: Path) -> None:
    plan_path, assets_path, _ = _write_fixture(tmp_path)
    payload = _plan()
    sections = payload["sections"]
    assert isinstance(sections, list)
    first_section = sections[0]
    assert isinstance(first_section, dict)
    first_block = first_section["blocks"][0]
    assert isinstance(first_block, dict)
    first_block["type"] = "freeform"
    first_block["layout"] = {"columns": 4}
    plan_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(RenderError, match="PLAN_SCHEMA_ERROR"):
        load_plan(plan_path)


@pytest.mark.parametrize(
    "unsafe_path",
    ["../outside.jpg", "/tmp/frame.jpg", "https://x.test/a.jpg", "javascript:bad"],
)
def test_unsafe_asset_paths_fail_closed(tmp_path: Path, unsafe_path: str) -> None:
    manifest_path = tmp_path / "assets.json"
    manifest = AssetManifest.model_validate(
        {
            "schema_version": "visual-report-assets.v0-prototype",
            "assets": [
                {
                    "asset_id": "frame-a",
                    "type": "keyframe",
                    "timestamp_ms": 0,
                    "path": unsafe_path,
                    "alt": "帧",
                    "caption": "说明",
                }
            ],
        }
    )

    with pytest.raises(RenderError, match="UNSAFE_ASSET_PATH"):
        resolve_assets(manifest_path, manifest, 1000)


def test_missing_asset_reference_is_a_visible_failure(tmp_path: Path) -> None:
    plan_path, assets_path, output_path = _write_fixture(tmp_path)
    payload = _plan()
    first_image = payload["sections"][0]["blocks"][5]
    first_image["asset_id"] = "not-present"
    plan_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(RenderError, match="UNKNOWN_ASSET_REFERENCE"):
        render_report(plan_path, assets_path, output_path)
