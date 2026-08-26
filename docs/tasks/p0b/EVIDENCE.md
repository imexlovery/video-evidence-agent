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

The current stage is `CLOSED / BLOCKED_EXECUTION_FAILURE`. Offline tests and
static checks passed (`28 passed`; Ruff clean; `git diff --check` clean), and the
formal input validation passed for 3 videos, 12 questions, 12 Gold rows, 127
segments, all Gold mappings, and all media hashes/durations. The r2 manifest is
at `eval/p0b/revisions/p0b-r2/eval-manifest.json`; it pins source commit
`3e280afc5d11a7976575ca0c8c660d6c79d70aaa` and artifact root
`artifacts/p0b/p0b-r2/`. The owner subsequently authorized the one-call-per-question
12-question formal run; its failures are recorded below.

## P0-B R2 formal run and closeout — 2026-08-26

The owner then explicitly authorized the 12 new DeepSeek text calls. The locked
run executed once against the frozen manifest. All 12 question-specific
`retrieval.json` files were persisted before their answer attempt, and all 12
formal result slots were created. Every answer attempt failed with
`provider / APIConnectionError`; no raw provider response or token usage was
available. The failure artifacts retain the failure class without exposing a
credential, and no question was retried or overwritten.

The retrieval-only automatic audit of the persisted Top-5 files was:

| metric | r2 result |
| --- | ---: |
| QuestionHit@1 | 6/9 |
| QuestionHit@5 | 9/9 |
| Gold evidence-unit recall@5 | 0.962963 |
| AllEvidence@5 | 2/3 |
| MRR | 0.805556 |

Answer/refusal accuracy, schema compliance, citation temporal/provenance
validity, latency, token usage, and semantic support were not evaluable because
no model call succeeded. The automatically generated report is
`reports/p0b-r2-retrieval-eval.md` with its JSON companion; it records
`BLOCKED_EXECUTION_FAILURE`. The generated
`artifacts/p0b/p0b-r2/human-review.json` and `.jsonl` contain all 12 rows with
semantic review fields left null. There is no answer content for meaningful
owner semantic adjudication, so this revision is closed blocked and is not
`P0B_R2_PASSED`.

## DeepSeek connection diagnosis — 2026-08-26

The r2 provider failure was diagnosed after closeout without rerunning any
formal question. In the sandbox, a no-auth request to the configured endpoint
failed with `PermissionError: [Errno 1] Operation not permitted`, which the
OpenAI-compatible client surfaced during the formal run as
`APIConnectionError`. The project `.env` itself has a configured endpoint,
model, and credential.

In a network-enabled execution context, the same endpoint returned the expected
HTTP 401 for a no-auth request, and one authenticated non-answer
`models.list()` request using the project `.env` succeeded and returned three
models. This confirms the root cause was the sandbox network restriction, not
an invalid DeepSeek endpoint or credential. The operational fix is to run any
future formal revision from a network-enabled environment. The frozen r2
manifest and its 12 failed result slots remain immutable; r2 is not rerun.

## P0-B R3 takeover and offline verification — 2026-08-26

Status: `IN_PROGRESS / P0B-R3-02_WAITING_OWNER_AUTHORIZATION`.

The execution-only R3 task was read and accepted as the active follow-up. The
closed R2 state remains `P0B_BLOCKED_EXECUTION_FAILURE`; no R2 result, report,
metric, review, prompt, input, or failure slot was rewritten. The R2 protection
snapshot is `docs/tasks/p0b-r3/r2-baseline.json` and records hashes for the R2
manifest, run manifest, metrics, human-review artifacts, report files, and all
24 question-specific retrieval/result artifacts.

Offline verification completed before any provider call:

- `UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q` —
  exit 0, `28 passed`;
- `UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run ruff check .` —
  exit 0, all checks passed;
- `git diff --check` — exit 0;
- the protected R2 source commit to current HEAD diff for `src`, `tests`,
  `pyproject.toml`, and `uv.lock` is empty;
- corpus, questions, Gold, and decision ledger JSONL validation — exit 0;
- R2 frozen-manifest input/source/media/ingest pins, P0-A anchors, all three
  media hashes/durations, all 127 non-empty timestamped segments, and every
  Gold segment/time mapping — verified by the existing read-only validation
  path;
- fixed population is 3 videos, 12 questions, 12 Gold rows, and 127 segments;
- R3 manifest, artifact root, and report paths were absent at takeover and
  remain uncreated; `docs/tasks/p0b-r3/` now contains only the allowed R2
  protection baseline;
- external calls: `0` (P0-A preflight `0`, formal R3 calls `0`), video upload:
  `false`, mock result: `false`.

The working-tree `.DS_Store` files, the pre-existing modified decision ledger,
the issued R3 task document, and the two draft JSONL files were recorded. The
existing decision-ledger lines were preserved; only the allowed append-only R3
evidence line was added. The next action is the owner authorization checkpoint for
`最多 1 次 P0-A 预检 + 12 次正式调用`; until that explicit authorization,
no provider command may run.

## P0-B R3 preflight and freeze — 2026-08-26

The owner authorization for the approved question/Top-K transcript payload was
recorded before the call. Exactly one disposable P0-A preflight was executed
against `https://api.deepseek.com` with `deepseek-v4-flash`; it exited 0,
returned a parsed `AnswerProposal` with `ANSWERED`, and passed the existing
Evidence Gate with `citation_provenance_verified`. The preflight evidence is
`docs/tasks/p0b-r3/preflight.json`; it records the five segment IDs, model,
status, the observed 2,375ms end-to-end interval, unavailable provider-only
latency, unavailable usage, and no error. It is not part of the P0-B score.

After that success, `p0b-r3` was frozen at
`eval/p0b/revisions/p0b-r3/eval-manifest.json`; its SHA-256 is
`45000b84fc5c0902993d5e7d81ed16e912e34b87a8c750b0018357375e535e1a`.
The manifest revalidated the fixed inputs, media, ingest artifacts, Gold
mappings, P0-A anchors, and source pins. Formal calls completed before the
next step: `0`; remaining formal budget: `12`. The next command is the single
`p0b-run`; no other preflight or formal call is permitted.

## P0-B R3 formal run and automatic grading — 2026-08-26

The single authorized `p0b-run` executed once against the frozen R3 manifest.
All 12 question-specific retrieval artifacts were persisted before answering;
all 12 formal result slots completed successfully and were schema-compliant.
There were no retries, overwrites, Mock results, video uploads, or provider
failures. The formal run evidence is `docs/tasks/p0b-r3/run.json`; the raw
retrieval/result artifacts remain under `artifacts/p0b/p0b-r3/`.

Automatic grading is recorded in `docs/tasks/p0b-r3/grade.json` and
`artifacts/p0b/p0b-r3/metrics.json`:

| metric | R3 result | frozen threshold/status |
| --- | ---: | --- |
| QuestionHit@1 | 6/9 | meets >= 6/9 |
| QuestionHit@5 | 9/9 | meets >= 8/9 |
| Gold evidence-unit recall@5 | 0.962963 mean | diagnostic |
| Multi AllEvidence@5 | 2/3 | meets >= 2/3 |
| MRR | 0.805556 mean | diagnostic |
| answer/refusal status accuracy | 11/12 | diagnostic |
| correct refusal | 2/3 | meets >= 2/3 |
| invalid citation provenance | 0/10 | meets 0 |
| schema failures | 0/12 | diagnostic |
| mean answer latency | 4799.58 ms | diagnostic |
| reported token usage | 23,858 total | cost not computed |

The current status is `AUTO_SCORED_PENDING_OWNER_REVIEW`. Fully-supported
answer, fully-correct answer, semantic support, and answer-point coverage are
not yet scored: `artifacts/p0b/p0b-r3/human-review.json` and `.jsonl` contain
all 12 rows, the complete current model answer/evidence/quote material, and
the unchanged Gold reference material, with owner review fields still null.
The R3 report has not been generated, no P0-B pass is claimed, and P1 has not
started. The next and final in-scope checkpoint is owner semantic review.

## P0-B R3 owner-authorized semantic review and final report — 2026-08-26

After the owner inspected the presented per-question R3 material, the owner
explicitly authorized Codex to fill the frozen-rubric semantic labels and
complete the remaining R3 report work. The authorization is recorded as
`DEC-P0B-033`; it does not itself select a final P0-B decision or authorize P1.

All 12 rows in `artifacts/p0b/p0b-r3/human-review.json` and `.jsonl` now contain
review labels. The nine answerable rows have answer-point coverage mean `1.0`,
fully-correct answer `9/9`, fully-supported answer `9/9`, and semantic support
`9/9`. Two of the three unanswerable rows correctly emitted
`INSUFFICIENT_EVIDENCE`. `p0b-r1-kling-u` instead answered that the parameter
count was not disclosed; its statement is citation-supported, but the frozen
contract required an explicit refusal, so its `fully_correct` and
`fully_supported` labels are false.

The required report command exited 0 and generated
`reports/p0b-r3-retrieval-eval.md` plus its JSON companion. All six frozen Gate
checks pass:

| Gate | R3 result | threshold |
| --- | ---: | ---: |
| QuestionHit@1 | 6/9 | >= 6/9 |
| QuestionHit@5 | 9/9 | >= 8/9 |
| Multi AllEvidence@5 | 2/3 | >= 2/3 |
| FullySupportedAnswer | 9/9 | >= 7/9 |
| CorrectRefusal | 2/3 | >= 2/3 |
| Invalid citation provenance | 0/10 | 0 |

The final R3 recommendation is `READY_FOR_OWNER_P0B_DECISION`, not an automatic
P0-B pass. The owner must still explicitly choose `P0B_PASSED_OWNER_ACCEPTED`,
`P0B_THRESHOLDS_NOT_MET`, or `P0B_BLOCKED`. No P1 work has started or been
authorized.

## P0-B R3 owner decision and closeout — 2026-08-26

The owner explicitly selected `P0B_PASSED_OWNER_ACCEPTED` after reviewing the
complete R3 report and semantic-review evidence. This decision is recorded as
`DEC-P0B-037`. The R3 closeout status is now
`P0B_PASSED_OWNER_ACCEPTED`; the scoped P0-B evaluation is accepted, while P1
remains unstarted and unauthorized.

The report and closeout evidence preserve the six passed Gate counts, the
12-call execution boundary, the known Kling refusal-contract failure, the
fixed-regression-set limitations, and the distinction between P0-B acceptance
and any future P1 authorization.
