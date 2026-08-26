# P0-B R1 evidence ledger

- Evidence status: `FROZEN / OWNER_REVIEWED / CLOSED_WITH_RETRIEVAL_THRESHOLDS_NOT_MET`.
- Evaluation method: `TRANSCRIPT_RETRIEVAL`.
- Date: 2026-08-26.
- Scope: local media → FFmpeg → Chinese `mlx-whisper` → `VideoSegment` → character
  2–4 gram TF-IDF Top-5 → DeepSeek text answer → local evidence gate → Gold.
- The answer workflow never uploads video. DeepSeek receives only the current
  question and its current Top-5 segments.

## Existing real ingest evidence

The command below completed against the three local media files. Metal access was
unavailable inside the sandbox, so the same local command was run outside the
sandbox after approval. It did not contact an answer provider.

```text
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run video-evidence p0b-ingest --project-root . --corpus eval/p0b/corpus.jsonl --media-root eval/p0b/media --preview-seconds 300 --target-segment-ms 45000 --max-segment-ms 60000
```

| video_id | SHA-256 prefix | duration_ms | ASR model | VideoSegments | pipeline status |
| --- | --- | ---: | --- | ---: | --- |
| `p0b-kling-2024` | `e539a0b0e85e` | 2022421 | `mlx-community/whisper-small-mlx` | 43 | `SUCCEEDED` |
| `p0b-rlinf-2026` | `f0d0dc489a1d` | 2093120 | `mlx-community/whisper-small-mlx` | 46 | `SUCCEEDED` |
| `p0b-wuyi-goals` | `04b383544d96` | 1763207 | `mlx-community/whisper-small-mlx` | 38 | `SUCCEEDED` |

The ingest artifacts contain 127 non-empty, timestamped `VideoSegment` objects.
The current freeze command rechecks each source hash and duration, each ingest
manifest/segment hash, the 127-segment total, and every Gold segment/time
mapping before it writes `eval/p0b/eval-manifest.json`.

## Owner-confirmed formal inputs

The owner confirmed the local source-use basis, all 12 question/Gold semantics and
time intervals, and the Kling online-version answer correction (`720P / 5 秒`) in
the task conversation on 2026-08-26. The active files are:

- `eval/p0b/corpus.jsonl`: 3 videos, hashes, durations, and ingest paths;
- `eval/p0b/questions.jsonl`: 12 questions, 4 per video;
- `eval/p0b/gold.jsonl`: 12 Gold rows with unchanged answer points, refusal
  rationales, intervals, and segment IDs.

The `.draft.jsonl` files remain historical construction inputs and are not used
by freeze, run, grading, or the answer prompt.

## Freeze and run boundary

The `eval/p0b/eval-manifest.json` was created only after the migrated code and
all pre-freeze checks passed. After `p0b-r1` is frozen, corpus/questions/Gold, the
DeepSeek answer prompt, source hashes, ingest snapshots, and media hashes are
immutable. The run creates exactly one result slot per question under
`artifacts/p0b/p0b-r1/transcript-retrieval/` and preserves provider, timeout,
schema, retrieval, and ingest failures without retrying or overwriting them.

Automatic grading reports retrieval, status, provenance, temporal overlap,
schema, latency, and provider-reported token usage. The owner reviewed the
generated per-question materials and then explicitly delegated the final
`fully_correct`, `fully_supported`, `semantic_support`, and answer-point coverage
judgments to Codex under the frozen rubric. This ledger does not treat those
human semantic labels as deterministic provenance checks.

## Frozen run and automatic score — 2026-08-26

`eval/p0b/eval-manifest.json` now records `p0b-r1` as `FROZEN`, with the corpus,
questions, Gold, prompt, source files, ingest snapshots, and media hashes. The
run created 12/12 `TRANSCRIPT_RETRIEVAL` result slots and 12/12 retrieval files;
all 12 DeepSeek calls completed successfully, with no video upload.

Automatic results:

| metric | result |
| --- | ---: |
| QuestionHit@1 | 2/9 |
| QuestionHit@5 | 7/9 |
| Gold evidence-unit recall@5 | 0.648148 |
| AllEvidence@5 | 1/3 |
| MRR | 0.435185 |
| answer/refusal status accuracy | 10/12 |
| correct refusal | 2/3 |
| invalid citation provenance | 0/9 |
| schema failures | 0/12 |
| mean answer latency | 3645.08 ms |
| token usage | 21,332 total tokens reported |

The per-question semantic package is at
`artifacts/p0b/p0b-r1/human-review.json` and `.jsonl`. The owner attestation
records that all 12 rows were reviewed across Answer, Evidence, Quote, and
Points. The owner then explicitly authorized Codex to judge and record the
per-row booleans. All 12 review rows now contain labels and concise failure notes
where needed; no raw answer, retrieval artifact, Gold row, or frozen input was
changed.

Semantic adjudication results:

| metric | result |
| --- | ---: |
| answer-point coverage mean | 0.685185 |
| fully correct, answerable questions | 5/9 |
| fully supported, answerable questions | 5/9 |
| semantic support, answerable questions | 8/9 |
| correct refusal | 2/3 |

The evaluation remains closed with recommendation
`P0B_RETRIEVAL_THRESHOLDS_NOT_MET`: QuestionHit@1, QuestionHit@5,
AllEvidence@5, and fully-supported-answer did not meet the frozen thresholds.
No later stage is started and P0-B is not labeled `PASSED`.

## P0-B R2 construction status — 2026-08-26

The owner subsequently authorized implementation of the document-published
`P0-B-R2` task. The r1 evaluation remains the immutable historical baseline;
its manifest, inputs, results, raw responses, human-review labels, report, and
failure conclusion were not rewritten. The recoverable source baseline is Git
commit `982f5ea5d8036a65ce9779ec1d24a5d1f495511d`, with protected artifact hashes
recorded in `docs/tasks/p0b-r2/r1-baseline.json`.

The r2 implementation is deliberately limited to the existing
`TRANSCRIPT_RETRIEVAL` method. It adds a transparent deterministic query-view
and score-aggregation profile over character 2–4 gram TF-IDF, keeps the output
as the original timestamped Top-5 `VideoSegment` objects, adds an r2 refusal
prompt, and isolates the r2 manifest/artifact paths. It does not change media,
ASR, segment boundaries, questions, Gold, or the DeepSeek context boundary, and
does not add Dense, Hybrid, Reranker, Embedding, VLM, Agent, or service code.

Development-only regression checks on the fixed corpus/retrieval artifacts
showed `QuestionHit@1 = 6/9`, `QuestionHit@5 = 9/9`, `AllEvidence@5 = 2/3`, and
`MRR = 0.805556` for the candidate lexical profile. These are not the formal r2
result: they were run before freeze and before any new answer-model calls, and
must not be presented as a P0-B pass.

The current stage is `IMPLEMENTATION_IN_PROGRESS / PREFREEZE`. Offline tests and
static checks have passed so far (`28 passed`; Ruff clean; `git diff --check`
clean). The r2 manifest has not yet been frozen and no new DeepSeek calls have
been made. After freeze, a separate explicit owner authorization is still
required for the one-call-per-question 12-question formal run.
