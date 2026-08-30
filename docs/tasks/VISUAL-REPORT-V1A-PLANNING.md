# Task: Video Visual Report V1-A Topic Mapper + Report Planner

## Task metadata

| Field | Value |
|---|---|
| Task ID | `VR-V1A-PLANNING-001` |
| Target grade | `G1 PROTOTYPE` |
| Requirements status | `READY_FOR_ENGINEERING_HANDOFF` |
| Task status | `READY_FOR_OWNER_V1A_REVIEW` |
| Implementation status | `S7_COMPLETE — PROVIDER_CONFIGURATION_BLOCKED` |
| Current authorization | Owner explicitly authorized continuation on 2026-08-30; implementation and the complete six-identity admission attempt are complete, with no fallback model used |
| Required stop | `READY_FOR_OWNER_V1A_REVIEW` |
| V1-B/V1-C | Prohibited |

## Entry conditions

All conditions are required before changing product code:

1. the Owner explicitly authorizes implementation of this exact task;
2. branch and baseline are rechecked against `visual-report` and
   `6576d1e8a0df3aa7288a6b9c84b6615114d9decc`, with unrelated work preserved;
3. the requirements readiness file still matches the canonical package;
4. the three source manifest/transcript pairs remain readable and unchanged;
5. any material Owner change is appended to decision evidence and the package
   is revalidated before implementation continues.

No current document, green validator result, or credential availability may
substitute for condition 1.

## Required read order

1. `AGENTS.md`
2. `docs/visual-report/V1A-STATUS.md`
3. `docs/requirements/visual-report-v1a/requirements-readiness.json`
4. `docs/requirements/visual-report-v1a/00-handoff.md`
5. `docs/requirements/visual-report-v1a/12-engineering-context.md`
6. `03-functional-spec.md`, `06-interfaces-integrations.md`,
   `07-agent-behavior.md`, `09-test-acceptance.md`, `10-delivery-plan.md`, and
   `11-decisions-risks.md` in the same package
7. This task

## Objective

Implement the smallest local foreground path that turns one existing complete
timestamped transcript into a canonical Topic Map, then a compiled current V0
Report Plan, and finally `report.html`, using exactly one Topic Mapper call and
one Report Planner call. Supply deterministic/fake/replay checks and one frozen
three-video Development measurement for Owner review.

## Hard boundary

- Topic Mapper optimizes coverage; Report Planner optimizes compression,
  narrative, and existing semantic block selection. Never merge them.
- Both calls receive the full authorized transcript. Planner also receives the
  canonical Topic Map.
- The selected model is explicit through `VISUAL_REPORT_MODEL`, must fit the
  fixed full-context envelope and JSON contract, uses temperature zero, has SDK
  retry disabled, has no fallback, and is snapshotted in each run.
- Models select existing segment/topic IDs only. Deterministic code binds every
  timestamp and `SourceRef`, creates canonical IDs, validates metrics/budgets,
  compiles, owns state, and invokes the current renderer.
- No semantic repair, third call, hidden retry, silent block removal, manual-plan
  substitution, chunking/truncation fallback, or successful partial report.
- Every attempt gets a new directory. Preserve failures and cancellations.
- Do not modify frozen P0-B inputs, results, evaluation/history, retrieval,
  answering, Evidence Gate, or conclusions.

## Delivery slices

| Slice | Scope | Required evidence |
|---|---|---|
| `S0 Contract lock` | Versioned schemas/prompts, synthetic transcript/review fixtures, fake provider seam | Examples validate; no provider call; protected-path review |
| `S1 Source/run spine` | Read-only manifest/segment validation, limits, unique run/state/error/event/call traces | Invalid/boundary/duplicate/cancel tests; `provider_calls/model_calls=0/0` before admission |
| `S2 Topic Mapper` | One full-context call, strict proposal, deterministic binder and segment accounting | Success plus missing/duplicate/unknown/non-contiguous/injection fixtures |
| `S3 Report Planner` | One full-context + Topic Map call, strict proposal, omission accounting, block/metric/budget gates, V0 compiler | Valid compile plus forbidden fields, refs, metrics, budgets, and topic-selection failures |
| `S4 End-to-end CLI` | Add explicit `build-from-transcript` path and existing renderer composition | Synthetic fake-adapter run reaches `RENDERED` with exactly `2/2`; replay is deterministic |
| `S5 Evaluation preparation` | Three versioned review cards, scorer/signature/aggregate contracts | Cards validate and freeze before real calls |
| `S6 Development measurement` | Predeclare and execute three videos × two repeats under one frozen revision | Six retained terminal runs, twelve planned call traces, rubrics, aggregate conclusion |
| `S7 Review handoff` | Targeted/full regression, diff/protected review, task/status/evidence update | Stop at `READY_FOR_OWNER_V1A_REVIEW`; no self-acceptance or next phase |

Follow the dependency order in `10-delivery-plan.md`. Do not introduce parallel
or multi-agent implementation merely to shorten the session.

## Fixed source population

| Video ID | Segment count | Duration |
|---|---:|---:|
| `p0b-kling-2024` | 43 | 2,022,421 ms |
| `p0b-rlinf-2026` | 46 | 2,093,120 ms |
| `p0b-wuyi-goals` | 38 | 1,763,207 ms |

Matching source paths are
`artifacts/p0b-ingest/<video-id>/{manifest.json,segments.jsonl}`. They are
read-only, authorized for the two external text calls, and remain local/non-
public research sources. V1-A never sends media.

## Owner-confirmed measurement acceptance

The declared measurement revision contains six pipeline identities and twelve
planned model calls. All attempts remain in the denominator.

| Metric | Pass threshold |
|---|---|
| Mapper segment accounting | 100% mapped or explicit exclusion |
| Must-cover recall | ≥90% per run and no must-cover item completely absent |
| Major unsupported claim/metric | 0 |
| Block source refs | 100% valid |
| First-response schema/compile/render | 6/6 without repair |
| Prioritization/narrative/block appropriateness | ≥4/5 average per video; neither repeat below 3 |
| Repeat stability | Per-video rubric-category delta ≤1; both repeats pass |
| Anti-template | The three normalized structures are not all identical and semantic affordances fit the source |

Any prompt, model, provider policy, source snapshot, schema, compiler, review
card, or evaluator change creates a new full measurement revision. Never replace
or selectively rerun a historical failure.

## Required later verification

```bash
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run ruff check .
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q tests/test_visual_report_planning.py
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q
git diff --check
```

Also run the implemented provider-free replay/failure commands, the six explicit
real Development runs, and the V1-A evaluation command defined within the
approved CLI/artifact contracts. Credential diagnostics may report presence
only; never read or print secret values.

## Current execution evidence

| Item | State |
|---|---|
| Product source changes | `S1–S7 — source/run spine, mapper/planner/compiler, CLI, evaluator; no V0/P0-B changes` |
| Dependency changes | `0 — existing dependency set retained` |
| Provider/model calls | `0/0 — no external provider or model call; all checks use local fake/replay` |
| Code tests | `PASS — targeted Ruff; 15/15 planning/runtime/evaluator tests` |
| Six-run Development measurement | `COMPLETED_ATTEMPT — six frozen identities retained as FAILED/CONFIGURATION_ERROR, each 0/0; twelve external calls were not admitted` |
| V1-A quality conclusion | `BLOCKED_PROVIDER_CONFIGURATION — measurement_valid=false; human rubric remains pending` |

S0–S7 evidence on 2026-08-30:

- `UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run ruff check src/video_evidence_agent/visual_report/planning.py tests/test_visual_report_planning.py` → pass;
- `UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q tests/test_visual_report_planning.py` → `15 passed`;
- `freeze-measurement` produced current revision `vr1a-dev-cecd6a62e6b2` in `eval/visual-report-v1a/measurement-manifest-v2.json`, validating all three fixed source snapshots and review cards and predeclaring six run IDs / twelve planned calls;
- the six declared IDs in `artifacts/visual-report/v1a/` each ended `FAILED` with `CONFIGURATION_ERROR: VISUAL_REPORT_MODEL is required`; every `run.json` records `provider_calls/model_calls=0/0`, and no fallback model was attempted;
- `evaluate --measurement-manifest eval/visual-report-v1a/measurement-manifest-v2.json` produced `artifacts/visual-report/v1a/evaluation/vr1a-dev-cecd6a62e6b2/aggregate.json` with six deterministic rows, six pending human-rubric files, `measurement_valid=false`, and `conclusion=BLOCKED_PROVIDER_CONFIGURATION`;
- existing V0 renderer regression command completed with a `4 sections, 13 blocks` HTML output in a non-repository temporary path;
- full `UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run ruff check .` → pass; full `uv run pytest -q` → `53 passed`; targeted planning tests → `15 passed`;
- `git diff --check` → pass;
- protected P0-B source/eval/answering/retrieval paths → no task diff;
- `measurement-manifest.json` is retained as the earlier evaluator revision; the `-v2` manifest is current after the evaluator stale-snapshot guard was frozen. No historical artifact was overwritten.

## Explicit non-goals

MP4/ASR, keyframes/assets, `image_caption`, OCR/VLM, Agent/LangGraph/tools,
RAG/vector storage, database/cache/queue, service/API/UI, accounts, URL input,
multi-video synthesis, multiple templates, free layout, publishing, deployment,
fine-tuning, prompt self-improvement, V1-B, and V1-C.

## Completion and stop rule

Automated and Development evidence may advance this task only to
`READY_FOR_OWNER_V1A_REVIEW`. The Owner alone records V1-A acceptance or
authorizes another phase. A failed threshold produces an honest failed/review
state with all evidence retained; it never triggers hidden repair or automatic
V1-B/C work.
