from video_evidence_agent.retrieval import retrieve
from video_evidence_agent.schemas import VideoSegment


def _segment(ordinal: int, text: str) -> VideoSegment:
    return VideoSegment(
        video_id="smoke-001",
        segment_id=f"smoke-001-seg-{ordinal:03d}",
        ordinal=ordinal,
        start_ms=ordinal * 45_000,
        end_ms=(ordinal + 1) * 45_000,
        transcript_text=text,
        source_asr_ordinals=(ordinal,),
    )


def test_character_tfidf_returns_ranked_full_segments() -> None:
    audio_segment = _segment(0, "使用 FFmpeg 将视频音频转换为单声道十六千赫兹 WAV 文件。")
    review_segment = _segment(1, "模型上线前需要进行离线评测和人工审查。")

    hits = retrieve("怎样将视频音频转换为单声道文件？", [audio_segment, review_segment])

    assert hits[0].segment.segment_id == audio_segment.segment_id
    assert hits[0].segment.start_ms == 0
    assert hits[0].score >= hits[1].score
    assert [hit.rank for hit in hits] == [1, 2]
