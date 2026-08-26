# Video Evidence Agent

P0-A is a G1 feasibility smoke test, not a production Agent or a Web service.
It verifies one narrow path: a real Chinese MP4 is converted to audio, transcribed
with timestamps, grouped into VideoSegments, retrieved with local character
n-gram TF-IDF, and answered only with citations from the retrieved segments.

## Deliberately excluded

Agent planning, tool calling, OCR, VLM, vector databases, hybrid retrieval,
FastAPI, UI, workers, and multi-video evaluation are outside P0-A.

## Prerequisites

- Apple Silicon Mac
- Python 3.12 managed by uv
- FFmpeg and FFprobe on PATH
- A local, legally obtained Chinese technical MP4
- A real OpenAI-compatible Chat Completions credential for evidence-constrained
  answering. The program never falls back to a mock answerer.

Copy `.env.example` to `.env` and fill `OPENAI_API_KEY` outside version control.
The CLI automatically loads this project-local, gitignored file; explicit
process environment variables take precedence. You do not need to re-enter the
key for every command or terminal. The current template targets DeepSeek's
OpenAI-compatible endpoint with `deepseek-v4-flash`.

## Reproduce P0-A

    uv sync --locked
    source .venv/bin/activate
    video-evidence ingest /absolute/path/to/video.mp4 --video-id smoke-001 \
      --source-url "https://source.example/video" \
      --source-license "license name" \
      --source-attribution "creator / required attribution"
    video-evidence smoke smoke-001 --questions eval/p0a/questions.jsonl
    video-evidence review smoke-001 --questions eval/p0a/questions.jsonl

The current R1 sample uses an accepted, non-commercial Chinese-LiPS subset.
Keep all dataset metadata, transcripts, media, questions, and derived artifacts
under the ignored `artifacts/` directory. With the pinned validation metadata
already present, the bounded preparation and evaluation path is:

    uv run video-evidence prepare-chinese-lips-mini \
      --metadata artifacts/chinese-lips-mini-val-kj-001/source/meta_valid.csv \
      --revision db96948538811029011eee44602438a26710ecd9 \
      --speaker 127_21_M_KJ
    uv run video-evidence ingest \
      artifacts/chinese-lips-mini-val-kj-001/composite.mp4 \
      --video-id chinese-lips-mini-val-kj-001 \
      --preview-seconds 60 \
      --asr-model mlx-community/whisper-small-mlx
    uv run video-evidence evaluate-asr \
      --video-id chinese-lips-mini-val-kj-001
    uv run video-evidence smoke chinese-lips-mini-val-kj-001 \
      --questions artifacts/chinese-lips-mini-val-kj-001/questions.jsonl
    uv run video-evidence review chinese-lips-mini-val-kj-001 \
      --questions artifacts/chinese-lips-mini-val-kj-001/questions.jsonl

Preparation inspects the remote ZIP directory and fails before payload reads if
the selected compressed entries exceed 64 MiB. `--reuse-extracted` is only for
rebuilding a provenance-matched local extraction without another network read.

The same artifacts can be queried again without re-transcribing:

    uv run video-evidence ask smoke-001 --question "问题文本" --top-k 5

The review command creates a DRAFT report from the real artifacts. It records
programmatic citation provenance but intentionally leaves ASR accuracy and
semantic evidence support for a human reviewer.

Artifacts are intentionally ignored by Git. A valid P0-A acceptance requires
the real MP4, real ASR output, persisted Top-K results, a real model call,
human review of ASR/retrieval/citation support, and the completed smoke report.
Automated tests alone are not acceptance evidence.

The ingest manifest records the source URL, license, attribution, local-use
note, input hash and duration. Do not invent these fields: use the source
publisher's actual attribution and license information.
