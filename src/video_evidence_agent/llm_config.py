"""Environment names shared by the OpenAI-compatible LLM clients."""

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_BASE_URL_ENV = "OPENAI_BASE_URL"

# The current answer and semantic-v2 paths intentionally use one model setting.
OPENAI_MODEL_ENV = "VIDEO_EVIDENCE_MODEL"


def normalize_openai_base_url(value: str) -> str:
    """Accept either an SDK base URL or its Chat Completions endpoint."""
    normalized = value.strip().rstrip("/")
    suffix = "/chat/completions"
    return normalized[: -len(suffix)] if normalized.endswith(suffix) else normalized
