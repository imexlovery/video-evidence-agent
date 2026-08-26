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

## P0-B locked Retrieval Eval

P0-B is a separate G1 offline evaluation of one formal method,
`TRANSCRIPT_RETRIEVAL`: three natural Chinese technical videos are processed by
local FFmpeg and Chinese MLX Whisper ASR, yielding 127 timestamped
`VideoSegment` objects; character 2–4 gram TF-IDF retrieves Top-5 evidence, and
DeepSeek answers from the question plus that Top-5 only. It is not an Agent
implementation and does not include Dense/Hybrid retrieval, OCR, VLM
enrichment, or a Web service.

The implementation is file-backed and fail-closed:

- `p0b-ingest` reuses the P0-A FFmpeg/Chinese ASR/VideoSegment pipeline for each
  corpus video;
- `p0b-freeze` records media, questions, Gold, the answer prompt, dependency and source
  hashes in an immutable, revision-specific manifest;
- `p0b-run` persists the current question's Top-5 before its single DeepSeek
  text call and writes one `TRANSCRIPT_RETRIEVAL` result or explicit failure
  artifact for every question; it never uploads video;
- `p0b-report` computes temporal retrieval/provenance metrics and keeps semantic
  answer review separate in the revision's artifact root.

The frozen `p0b-r1` run is closed after owner review and owner-authorized
per-question semantic labeling. Its final recommendation is
`P0B_RETRIEVAL_THRESHOLDS_NOT_MET`, so it is not labeled `PASSED`.

The formal inputs are already owner-confirmed in `eval/p0b/`: three videos,
twelve questions, twelve Gold rows, and the real 127-segment ingest artifacts.
`p0b-freeze` validates their hashes, durations, segment IDs, and P0-A anchor
hashes before creating the manifest. The answer call uses the project-root
`.env` values `OPENAI_API_KEY`, `OPENAI_BASE_URL`, and
`VIDEO_EVIDENCE_MODEL`; no separate video-provider configuration exists and
there is no Mock answer path.

The historical `p0b-r1` evaluation remains frozen at
`eval/p0b/eval-manifest.json` with results under `artifacts/p0b/p0b-r1/`; its
retrieval thresholds were not met and it is not labeled `PASSED`. The active
follow-up is the narrow `p0b-r2` revision: it keeps the same three videos,
127 segments, 12 questions, and Gold, and only adds deterministic lexical
query-view/score aggregation, an evidence-insufficiency prompt, and revision
isolation. It does not use Gemini, upload video, or add Dense/Hybrid/Reranker,
VLM, Agent, or service components. Its planned manifest and results are
`eval/p0b/revisions/p0b-r2/eval-manifest.json` and
`artifacts/p0b/p0b-r2/`. The r2 manifest is frozen and its one authorized 12-call
run has been recorded. All 12 provider attempts ended in `APIConnectionError`,
so the final report is `P0B_BLOCKED_EXECUTION_FAILURE`; the revision was not
retried or labeled `PASSED`.
