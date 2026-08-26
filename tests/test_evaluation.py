import pytest

from video_evidence_agent.evaluation import (
    GroundTruthClip,
    evaluate_asr,
    levenshtein_distance,
    normalize_cer_text,
)
from video_evidence_agent.schemas import AsrSegment


def test_cer_normalization_and_distance() -> None:
    assert normalize_cer_text(" ＡＢＣ，你 好！123 ") == "abc你好123"
    assert normalize_cer_text("網絡與資訊") == "网络与资讯"
    assert levenshtein_distance("你好世界", "你号世界") == 1


def test_evaluation_assigns_boundary_segment_once() -> None:
    clips = [
        GroundTruthClip("clip-1", 0, 0, 1000, "你好"),
        GroundTruthClip("clip-2", 1, 1000, 2000, "世界"),
    ]
    segments = [
        AsrSegment(ordinal=0, start_ms=0, end_ms=800, text="你好"),
        AsrSegment(ordinal=1, start_ms=800, end_ms=1800, text="世界"),
    ]

    result = evaluate_asr(clips, segments)

    assert result["overall"]["cer"] == pytest.approx(0.0)
    assert result["clips"][0]["assigned_asr_ordinals"] == [0]
    assert result["clips"][1]["assigned_asr_ordinals"] == [1]
    assert result["unassigned_asr_ordinals"] == []
