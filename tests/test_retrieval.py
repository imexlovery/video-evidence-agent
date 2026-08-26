import pytest

from video_evidence_agent.retrieval import (
    RetrievalError,
    r2_query_views,
    retrieve,
    retrieve_transcript_r2,
)
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


def test_r2_query_views_normalize_text_and_add_only_generic_aliases() -> None:
    views = r2_query_views("核心创作优势：ＦＦＭＰＥＧ 的使用成本？")

    assert views["base"] == "核心创作优势ffmpeg的使用成本"
    assert "好处优点" in views["aliases"]
    assert views["focus"]


def test_r2_retrieval_keeps_top_k_full_source_segments() -> None:
    target = _segment(0, "视频生成的好处是内容自由度非常高，可以组合天马行空的概念。")
    distractor = _segment(1, "这是一个普通的系统说明，没有创作内容。")
    filler = [_segment(index, f"这是第 {index} 个与问题无关的普通说明。") for index in range(2, 8)]

    hits = retrieve_transcript_r2(
        "视频生成与摄影、图形渲染相比时的核心创作优势是什么？",
        [target, distractor, *filler],
    )

    assert len(hits) == 5
    assert hits[0].segment.segment_id == target.segment_id
    assert all(hit.segment in [target, distractor, *filler] for hit in hits)
    assert [hit.rank for hit in hits] == [1, 2, 3, 4, 5]


def test_r2_multi_clause_query_keeps_distinct_evidence_candidates() -> None:
    simulation = _segment(0, "仿真训练需要高保真图像渲染和高速科学计算，并可能使用 GPU 并行资源。")
    real_robot = _segment(1, "真机训练要处理端云通信、权重同步和资源协调，也需要人在环。")
    unrelated = _segment(2, "这是与训练资源无关的普通说明。")

    hits = retrieve_transcript_r2(
        "仿真训练和真机训练分别有哪些资源、通信或人工参与约束？",
        [simulation, real_robot, unrelated],
    )

    assert {hit.segment.segment_id for hit in hits[:2]} == {
        simulation.segment_id,
        real_robot.segment_id,
    }


def test_r2_retrieval_rejects_blank_query() -> None:
    with pytest.raises(RetrievalError, match="question must not be blank"):
        retrieve_transcript_r2("  ", [_segment(0, "有效的测试文本")])
