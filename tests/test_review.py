import argparse
import json
from pathlib import Path

from video_evidence_agent import cli


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def test_review_draft_keeps_semantic_support_for_a_human(tmp_path: Path) -> None:
    artifacts = tmp_path / "artifacts"
    artifact_root = artifacts / "smoke-001"
    _write_json(
        artifact_root / "manifest.json",
        {
            "pipeline_status": "SUCCEEDED",
            "video_id": "smoke-001",
            "source": {
                "origin_url": "https://example.test/video",
                "license": "CC BY-SA 4.0",
                "attribution": "Example speaker",
                "use_note": "local smoke",
                "sha256": "abc",
                "duration_ms": 90_000,
            },
            "audio": {
                "channels": 1,
                "sample_rate_hz": 16_000,
                "duration_ms": 90_000,
            },
            "asr": {
                "engine": "mlx-whisper",
                "model": "test-model",
                "language": "zh",
            },
            "segmenting": {
                "target_duration_ms": 45_000,
                "max_duration_ms": 60_000,
                "segment_count": 2,
            },
            "phase_elapsed_ms": {"asr_full": 123},
        },
    )
    _write_json(
        artifact_root / "asr.json",
        {
            "dropped_empty_raw_segment_ordinals": [],
            "dropped_non_positive_raw_segment_ordinals": [],
            "dropped_unrepresentable_raw_segment_ordinals": [],
            "segments": [
                {"start_ms": 0, "end_ms": 20_000, "text": "开始的识别文本"},
                {"start_ms": 35_000, "end_ms": 55_000, "text": "中段的识别文本"},
                {"start_ms": 70_000, "end_ms": 90_000, "text": "结尾的识别文本"},
            ]
        },
    )
    _write_json(
        artifact_root / "retrieval" / "q-1.json",
        {
            "hits": [
                {
                    "score": 0.9,
                    "segment": {
                        "segment_id": "smoke-001-seg-000",
                        "start_ms": 0,
                        "end_ms": 45_000,
                    },
                }
            ]
        },
    )
    _write_json(
        artifact_root / "answers" / "q-1.json",
        {
            "status": "ANSWERED",
            "answer": "测试答案",
            "evidence": [
                {
                    "segment_id": "smoke-001-seg-000",
                    "start_ms": 0,
                    "end_ms": 45_000,
                    "quote": "开始的识别文本",
                }
            ],
        },
    )
    _write_json(
        artifact_root / "answers" / "q-1.gate.json",
        {"gate_reason": "citation_provenance_verified"},
    )

    questions = tmp_path / "questions.jsonl"
    questions.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "question_id": "q-1",
                        "question": "第一个问题",
                        "should_answer": True,
                        "expected_interval": [0, 45_000],
                    },
                    ensure_ascii=False,
                ),
                json.dumps(
                    {
                        "question_id": "q-2",
                        "question": "第二个问题",
                        "should_answer": True,
                        "expected_interval": [45_000, 90_000],
                    },
                    ensure_ascii=False,
                ),
                json.dumps(
                    {
                        "question_id": "q-3",
                        "question": "不可回答的问题",
                        "should_answer": False,
                        "expected_interval": None,
                    },
                    ensure_ascii=False,
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    report_path = tmp_path / "p0a-smoke-report.md"

    result = cli._review(
        argparse.Namespace(
            video_id="smoke-001",
            artifacts_dir=artifacts,
            questions=questions,
            report=report_path,
        )
    )

    report = report_path.read_text(encoding="utf-8")
    assert result == 0
    assert "PENDING_HUMAN_REVIEW" in report
    assert "citation_provenance_verified" in report
    assert "第一个问题" in report
