"""Local character n-gram TF-IDF retrieval for one video's VideoSegments."""

from __future__ import annotations

from collections.abc import Iterable

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from video_evidence_agent.schemas import RetrievalHit, VideoSegment


class RetrievalError(RuntimeError):
    """Raised when a P0-A retrieval request is invalid."""


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
