from video_evidence_agent.schemas import AsrSegment
from video_evidence_agent.segments import build_video_segments, validate_video_segments


def _asr(ordinal: int, start_ms: int, end_ms: int, text: str) -> AsrSegment:
    return AsrSegment(
        ordinal=ordinal,
        start_ms=start_ms,
        end_ms=end_ms,
        text=text,
    )


def test_segments_keep_real_boundaries_and_stable_ids() -> None:
    asr_segments = [
        _asr(0, 0, 20_000, "第一段中文内容"),
        _asr(1, 20_000, 45_000, "第二段中文内容"),
        _asr(2, 45_000, 70_000, "第三段中文内容"),
    ]

    first = build_video_segments("smoke-001", asr_segments)
    second = build_video_segments("smoke-001", asr_segments)

    assert [segment.segment_id for segment in first] == [
        "smoke-001-seg-000",
        "smoke-001-seg-001",
    ]
    assert [(segment.start_ms, segment.end_ms) for segment in first] == [
        (0, 45_000),
        (45_000, 70_000),
    ]
    assert first[0].source_asr_ordinals == (0, 1)
    assert first == second
    validate_video_segments(first)


def test_single_long_asr_segment_keeps_its_real_range() -> None:
    segments = build_video_segments(
        "smoke-001",
        [_asr(0, 5_000, 80_000, "一个超过最大长度的原始识别片段")],
    )

    assert len(segments) == 1
    assert (segments[0].start_ms, segments[0].end_ms) == (5_000, 80_000)
