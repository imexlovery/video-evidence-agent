"""Local character n-gram TF-IDF retrieval for one video's VideoSegments.

``retrieve`` is the original P0-A path and remains intentionally unchanged.
P0-B R2 uses :func:`retrieve_transcript_r2`, a still-lexical TF-IDF profile
that builds a few deterministic query views before blending their scores. It
does not add a second model, a semantic index, or a post-retrieval reranker.
"""

from __future__ import annotations

import unicodedata
from collections.abc import Iterable
from typing import Final

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from video_evidence_agent.schemas import RetrievalHit, VideoSegment


class RetrievalError(RuntimeError):
    """Raised when a P0-A retrieval request is invalid."""


R2_RETRIEVAL_PROFILE: Final[str] = "char_tfidf_2_4_query_views_v1"
R2_QUERY_VIEW_WEIGHTS: Final[dict[str, float]] = {
    "base": 0.10,
    "focus": 0.36,
    "aliases": 0.54,
}

# These are generic Chinese question-surface forms, not question IDs or Gold
# labels. The aliases are deliberately small and transparent so a frozen
# manifest can identify the exact retrieval profile used by an evaluation.
_R2_QUERY_ALIASES: Final[tuple[tuple[str, str], ...]] = (
    ("资源、通信或人工参与问题", "资源 通信 同步 人在环"),
    ("降低视频处理成本", "效率 压缩 成本"),
    ("核心创作优势", "好处 优点"),
    ("创作优势", "好处 优点"),
    ("使用上手成本", "使用成本 上手门槛"),
    ("首次发布", "第一版发布 首次发布"),
    ("首发日期", "第一版发布 日期 时间"),
    ("发布的日期", "发布 日期 时间"),
    ("数据处理", "数据处理 数据平台 标签"),
    ("系统约束", "资源 通信 同步 约束"),
    ("真机训练", "真机 真实环境"),
    ("仿真和真机", "仿真 真机"),
    ("模型设计", "模型 设计 结构"),
    ("行为偏离意图", "行为 偏离"),
    ("训练目标", "训练目标 奖励函数"),
    ("真实目标", "真实目标 价值"),
    ("对齐问题", "对齐问题 价值对齐"),
    ("人工参与", "人在环"),
    ("仿真训练", "仿真"),
    ("通信", "通信 通讯"),
    ("处理成本", "效率 压缩 成本"),
    ("泛化能力", "泛化性"),
    ("泛化", "泛化性"),
    ("奖励", "奖励 分数 加分"),
    ("主要改善", "提升 改善"),
    ("哪两类", "哪两种 两个"),
    ("精确累计下载量", "确切 数字 数量 下载量"),
    ("年度研究经费", "年度 经费 费用 资金"),
    ("确切参数量", "确切 参数量 规模"),
    ("视频分辨率", "分辨率"),
    ("单次时长", "时长 长度"),
    ("内容自由度", "自由度 想象力"),
)

_R2_QUERY_STOP_PHRASES: Final[tuple[str, ...]] = (
    "技术方案中",
    "开放版本",
    "学会回答",
    "演讲者",
    "演讲中",
    "请概括",
    "当前",
    "线上",
    "视频",
    "单次",
    "分别",
    "多少",
    "相比",
    "相较",
    "只用",
    "认为",
    "主要",
    "哪些",
    "哪一类",
    "哪两类",
    "概括",
    "问题",
    "为何",
    "为什么",
    "为让",
    "设置",
    "示例",
    "系统",
    "模型",
    "做法",
    "提到",
    "是什么",
    "是否",
    "演讲",
    "说",
    "的",
    "和",
    "与",
    "把",
    "中",
    "时",
)


def _r2_normalize(text: str) -> str:
    """Normalize harmless text variants while retaining Chinese/Latin content."""

    normalized = unicodedata.normalize("NFKC", text).casefold()
    return "".join(
        character
        for character in normalized
        if not character.isspace() and not unicodedata.category(character).startswith("P")
    )


def _r2_core_question(normalized_question: str) -> str:
    core = normalized_question
    for phrase in _R2_QUERY_STOP_PHRASES:
        core = core.replace(_r2_normalize(phrase), "")
    return core


def _r2_aliases(normalized_question: str) -> str:
    aliases: list[str] = []
    matched_sources: list[str] = []
    for source, target in _R2_QUERY_ALIASES:
        normalized_source = _r2_normalize(source)
        if normalized_source in normalized_question and not any(
            normalized_source in matched_source for matched_source in matched_sources
        ):
            aliases.append(_r2_normalize(target))
            matched_sources.append(normalized_source)
    return "".join(aliases)


def r2_query_views(question: str) -> dict[str, str]:
    """Return the transparent deterministic query views used by the R2 profile."""

    if not question.strip():
        raise RetrievalError("question must not be blank")
    normalized = _r2_normalize(question)
    aliases = _r2_aliases(normalized)
    core = _r2_core_question(normalized)
    return {
        "base": normalized,
        "focus": core + aliases,
        "aliases": aliases or normalized,
    }


def retrieve_transcript_r2(
    question: str,
    segments: Iterable[VideoSegment],
    *,
    top_k: int = 5,
) -> list[RetrievalHit]:
    """Retrieve full source segments with the frozen P0-B R2 TF-IDF profile.

    The profile fits one character 2–4 gram TF-IDF index over the current
    video's normalized segments. Three deterministic views of the same
    question are scored against that index and blended at fixed weights. The
    returned objects are the original timestamped ``VideoSegment`` instances;
    no derived text unit is exposed to the answerer.
    """

    if not question.strip():
        raise RetrievalError("question must not be blank")
    if top_k <= 0:
        raise RetrievalError("top_k must be positive")

    materialized = list(segments)
    if not materialized:
        raise RetrievalError("cannot retrieve from an empty VideoSegment set")

    views = r2_query_views(question)
    vectorizer = TfidfVectorizer(
        analyzer="char",
        ngram_range=(2, 4),
        sublinear_tf=True,
    )
    try:
        document_matrix = vectorizer.fit_transform(
            [_r2_normalize(segment.transcript_text) for segment in materialized]
        )
        query_matrix = vectorizer.transform(
            [views["base"], views["focus"], views["aliases"]]
        )
    except ValueError as exc:
        raise RetrievalError("unable to construct a character n-gram index") from exc

    similarities = cosine_similarity(query_matrix, document_matrix)
    scores = (
        R2_QUERY_VIEW_WEIGHTS["base"] * similarities[0]
        + R2_QUERY_VIEW_WEIGHTS["focus"] * similarities[1]
        + R2_QUERY_VIEW_WEIGHTS["aliases"] * similarities[2]
    )
    ordered_indexes = sorted(
        range(len(materialized)),
        key=lambda index: (-float(scores[index]), materialized[index].ordinal),
    )
    limit = min(top_k, len(materialized))
    return [
        RetrievalHit(rank=rank, score=float(scores[index]), segment=materialized[index])
        for rank, index in enumerate(ordered_indexes[:limit], start=1)
    ]


def retrieve(
    question: str,
    segments: Iterable[VideoSegment],
    *,
    top_k: int = 5,
) -> list[RetrievalHit]:
    """Return raw ranked scores with full timestamped VideoSegments."""

    if not question.strip():
        raise RetrievalError("question must not be blank")
    if top_k <= 0:
        raise RetrievalError("top_k must be positive")

    materialized = list(segments)
    if not materialized:
        raise RetrievalError("cannot retrieve from an empty VideoSegment set")

    vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 4))
    try:
        document_matrix = vectorizer.fit_transform(
            [segment.transcript_text for segment in materialized]
        )
        query_vector = vectorizer.transform([question])
    except ValueError as exc:
        raise RetrievalError("unable to construct a character n-gram index") from exc

    scores = cosine_similarity(query_vector, document_matrix).ravel()
    ordered_indexes = sorted(
        range(len(materialized)),
        key=lambda index: (-float(scores[index]), materialized[index].ordinal),
    )
    limit = min(top_k, len(materialized))
    return [
        RetrievalHit(rank=rank, score=float(scores[index]), segment=materialized[index])
        for rank, index in enumerate(ordered_indexes[:limit], start=1)
    ]
