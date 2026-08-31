# Task: Video Visual Report V1-A Provider Development Measurement

## Task metadata

| Field | Value |
|---|---|
| Task ID | `VR-V1A-MEASUREMENT-002` |
| Target grade | `G1 PROTOTYPE` |
| Requirements status | `READY_FOR_ENGINEERING_HANDOFF` |
| Task status | `READY_FOR_OWNER_V1A_REVIEW — MEASUREMENT_EXECUTION_FAILED` |
| Code baseline | `f8cb402d37bc05a30c7a912ed044548a71c128c7` (`feat(visual-report): implement V1-A planning prototype`) |
| Expected pre-task Owner work | Uncommitted `.env.example` update that names the intended V1-A model; preserve it |
| Documentation handoff changes | This task card plus V1-A status, append-only decision evidence, coverage, and regenerated readiness; preserve them |
| Previous failed evidence | Revision `vr1a-dev-cecd6a62e6b2`; six immutable `FAILED/CONFIGURATION_ERROR` runs with `0/0` calls |
| Current measurement evidence | Revision `vr1a-dev-10f4334c8026`; six immutable failed runs retained; evaluator conclusion `MEASUREMENT_EXECUTION_FAILED` |
| Required stop | `READY_FOR_OWNER_V1A_REVIEW` with an honest execution conclusion |
| V1-B/V1-C | Prohibited |

## Owner authorization

On 2026-08-30 the Owner stated:

> 已经提交git，然后进行了env.example的更新，暂未提交，就在此版本基础上进行下一步测试，依旧按文档驱动的方式，给出下一步任务卡，我去新session施工

Together with the earlier authorization to send all three complete transcripts
to the configured OpenAI-compatible provider, this authorizes one new complete
V1-A Development measurement under this task. It does not authorize prompt,
schema, compiler, evaluator, review-card, renderer, dependency, or product-code
changes, and it does not authorize V1-B/V1-C.

## Required read order

1. `AGENTS.md`
2. `docs/visual-report/V1A-STATUS.md`
3. `docs/requirements/visual-report-v1a/requirements-readiness.json`
4. `docs/requirements/visual-report-v1a/00-handoff.md`
5. `docs/requirements/visual-report-v1a/12-engineering-context.md`
6. `03-functional-spec.md`, `06-interfaces-integrations.md`,
   `07-agent-behavior.md`, `09-test-acceptance.md`, `10-delivery-plan.md`, and
   `11-decisions-risks.md` in the same requirements package
7. `docs/tasks/VISUAL-REPORT-V1A-PLANNING.md`
8. This task card

## Objective

Using the committed V1-A implementation and one explicit compatible model,
freeze and execute a fresh three-video × two-repeat Development measurement,
then generate the deterministic evaluation package for Owner review.

The task tests the already-built Topic Mapper + Report Planner path. It does
not improve or tune that path. A failed run is measurement evidence, not
permission to repair, retry, change the model, or replace the run.

## Critical configuration distinction

`.env.example` is documentation and is not runtime configuration. The current
code loads process environment variables and the repository-local untracked
`.env` file. Before freezing a revision, the runtime must expose:

- `OPENAI_API_KEY` — presence only may be checked or logged;
- `OPENAI_BASE_URL` — normalized provider label only;
- `VISUAL_REPORT_MODEL=deepseek-v4-flash-vision-exp` unless the Owner changes
  the model before freeze;
- `VISUAL_REPORT_TIMEOUT_SECONDS=120` unless the Owner changes it before
  freeze.

Never print, read back, copy into a task artifact, or commit the credential.
Do not source `.env` into shell output. The implementation's
`environment_snapshot()` is the safe preflight authority.

## Hard boundary

- Keep Topic Mapper and Report Planner as two sequential independent calls.
- Both calls receive the complete authorized transcript; Planner also receives
  the canonical Topic Map.
- Use exactly the one frozen model, temperature `0`, JSON-object response mode,
  SDK retry `0`, and no alternate provider/model fallback.
- No third model call, hidden retry, semantic repair, manual-plan substitution,
  truncation/chunking fallback, block deletion, selective rerun, or in-revision
  configuration change.
- All six declared identities remain in the denominator, including failures
  and cancellations.
- Preserve revision `vr1a-dev-cecd6a62e6b2`, its six failed run directories,
  its evaluator output, and all earlier measurement manifests unchanged.
- Do not modify product code, prompts, schemas, compiler, evaluator, review
  cards, dependencies, V0 artifacts, P0-B evidence, or source transcripts.
- Do not commit, push, create a PR, publish, deploy, or enter V1-B/V1-C unless
  the Owner separately asks.

## Entry conditions

All conditions must pass before the new freeze:

1. Branch is `visual-report` and `HEAD` is
   `f8cb402d37bc05a30c7a912ed044548a71c128c7`.
2. The uncommitted `.env.example` Owner change is present and preserved. Any
   other pre-existing work is identified and left untouched.
3. The three source manifest/segment pairs and three versioned review cards are
   readable and unchanged.
4. Targeted tests, full tests, Ruff, and `git diff --check` pass before any
   external call.
5. A safe environment snapshot reports `admission=READY`, an empty blocker
   list, the exact intended model, credential presence `true`, timeout `120`,
   temperature `0`, and SDK retries `0`.
6. `eval/visual-report-v1a/measurement-manifest-v3.json` does not exist.

Safe preflight command:

```bash
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run python -c \
  'import json; from pathlib import Path; from video_evidence_agent.visual_report.evaluation import environment_snapshot; print(json.dumps(environment_snapshot(Path.cwd()), ensure_ascii=False, indent=2))'
```

This command may expose model name and normalized provider label, but never a
credential value. If admission is not `READY`, stop without a model call and
record the blocker in this card and `V1A-STATUS.md`.

## Execution slices

### M0 — Baseline and provider-free gate

Run:

```bash
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run ruff check .
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q tests/test_visual_report_planning.py
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q
git diff --check
```

Also inspect `git status --short --branch` and protected-path diffs. M0 must
make `provider_calls/model_calls=0/0`.

### M1 — Freeze one new complete revision

Only after the safe preflight reports `READY`, run:

```bash
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run python -m video_evidence_agent.visual_report freeze-measurement \
  --repository-root . \
  --artifact-root artifacts/visual-report/v1a \
  --card-root eval/visual-report-v1a/review-cards \
  --output eval/visual-report-v1a/measurement-manifest-v3.json
```

Before any pipeline run, inspect the new manifest and require:

- `status=FROZEN` and `provider.admission=READY`;
- no provider blocker;
- exact intended provider/model/timeout/temperature/retry snapshot;
- the same three source hashes and review-card hashes as the validated inputs;
- six unique new run IDs, two per video, none equal to or colliding with an
  existing run directory;
- twelve planned provider/model calls.

If the freeze is provider-blocked, stale, or inconsistent, retain the manifest
and stop. Do not overwrite it or create another revision inside this task.

### M2 — Execute all six declared runs

Read the six IDs from `measurement-manifest-v3.json`. Execute six explicit
foreground commands, mapping each declared ID to its declared video:

```bash
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run python -m video_evidence_agent.visual_report build-from-transcript \
  --manifest artifacts/p0b-ingest/<video-id>/manifest.json \
  --segments artifacts/p0b-ingest/<video-id>/segments.jsonl \
  --run-id <declared-run-id> \
  --output-root artifacts/visual-report/v1a
```

Run each declared identity once. After every command, inspect only non-secret
run metadata: terminal state, error category, admitted/provider/model call
counts, model snapshot, usage when available, and artifact paths. Do not print
transcript bodies or credentials.

A run failure stays in the denominator. Do not reuse its ID or modify frozen
configuration. Continue the remaining declared identities unless the Owner
interrupts, a credential/security exposure is suspected, or continuing would
violate the frozen contract. Record any deliberate stop as cancellation or
incomplete measurement evidence.

### M3 — Deterministic evaluation

After every declared identity has a retained terminal directory, run exactly
once:

```bash
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run python -m video_evidence_agent.visual_report evaluate \
  --measurement-manifest eval/visual-report-v1a/measurement-manifest-v3.json \
  --output-root artifacts/visual-report/v1a/evaluation
```

Do not delete an evaluation directory to rerun the evaluator. Preserve its
aggregate, six deterministic run rows, and six generated human-rubric files.

### M4 — Review handoff and regression

- Re-run the M0 checks after measurement.
- Verify that every successful run contains canonical Topic Map, proposal,
  current V0 plan, empty assets manifest, `report.html`, call trace, events,
  and terminal `run.json`.
- Verify reports remain local/offline and no restricted media was uploaded or
  published.
- Update this task's execution evidence and `docs/visual-report/V1A-STATUS.md`
  in the same session.
- Present all six report and rubric paths to the Owner. Do not fill human
  scores or claim content-quality acceptance on the Owner's behalf.

## Measurement acceptance

### Execution-valid outcome

The new aggregate must show:

- `measurement_valid=true`;
- six declared and six execution-valid runs;
- observed `provider_calls/model_calls=12/12`;
- 6/6 first-response schema/compile/render success;
- 100% valid source refs and segment accounting;
- six retained `RENDERED` runs;
- `conclusion=PENDING_OWNER_REVIEW` until human rubrics are completed.

This outcome advances only to `READY_FOR_OWNER_V1A_REVIEW`; it is not
`OWNER_ACCEPTED`.

### Honest failed outcome

Any configuration, provider, schema, grounding, compile, render, stale-snapshot,
or denominator failure must remain visible. The aggregate may conclude
`BLOCKED_PROVIDER_CONFIGURATION` or `MEASUREMENT_EXECUTION_FAILED`. Record the
exact observed state and stop at Owner review. Do not tune or repair within this
measurement task.

### Later Owner quality gate

The Owner separately reviews the six reports against the frozen rubrics:

- must-cover recall ≥90% per run with no complete must-cover miss;
- zero major unsupported claim or metric;
- 100% valid block source references;
- prioritization, narrative, and block appropriateness average ≥4/5 per video,
  with neither repeat below 3;
- per-video rubric-category delta ≤1;
- the three videos do not all share one normalized structure signature.

Human scoring and Owner acceptance are not part of this execution task's
automatic completion claim.

## Required execution evidence

Record this section from the completed session; do not infer success from the
freeze or from provider admission alone:

| Evidence | Result |
|---|---|
| Baseline branch/HEAD/worktree | `PASS` — branch `visual-report` at `f8cb402d37bc05a30c7a912ed044548a71c128c7`; the pre-existing `.env.example` and documentation handoff modifications were preserved; no product/protected-path diff was introduced. |
| Pre-call targeted/full tests and Ruff | `PASS — provider-free` — Ruff passed; the normal-environment pytest invocations exposed one stale environment-sensitive assertion (`14 passed, 1 failed` targeted; `52 passed, 1 failed` full) because the test expected the old blocked configuration; rerunning only the tests with `VISUAL_REPORT_MODEL=` passed (`15 passed`, `53 passed`); `git diff --check` passed; no test path made a provider/model call. |
| Safe provider admission snapshot | `PASS` — `admission=READY`, blockers `[]`, provider label `https://api.deepseek.com`, model `deepseek-v4-flash-vision-exp`, `credential_present=true`, timeout `120`, response mode `json_object`, temperature `0`, SDK retries `0`, SDK `3.3.1`; no credential value was displayed. |
| New manifest path/revision/run IDs | `PASS` — `eval/visual-report-v1a/measurement-manifest-v3.json`, revision `vr1a-dev-10f4334c8026`, status `FROZEN`; six new non-colliding IDs: `p0b-kling-2024-v1a-cdfab9d75b-r1/r2`, `p0b-rlinf-2026-v1a-cdfab9d75b-r1/r2`, and `p0b-wuyi-goals-v1a-cdfab9d75b-r1/r2`; 12 planned provider/model calls. |
| Six terminal run states | `6/6 retained FAILED` — Kling r1 `PROVIDER_ERROR`; Kling r2, RLinf r1/r2, and Wu Yi r1/r2 `TOPIC_MAP_SCHEMA_ERROR`; no cancellation; no run ID was reused. |
| Observed provider/model calls | `6/6` — one Mapper call per declared run and zero Planner calls; declared denominator remains `12/12`; SDK retry snapshot remained `0`; no fallback, repair, or third call occurred. |
| Aggregate path and conclusion | `PASS — evaluator executed once` — `artifacts/visual-report/v1a/evaluation/vr1a-dev-10f4334c8026/aggregate.json`; `measurement_valid=false`, `conclusion=MEASUREMENT_EXECUTION_FAILED`; denominator `6` declared runs, `12` planned provider/model calls, `6/6` observed provider/model calls; six deterministic rows and six pending human-rubric files retained. |
| Post-run regression/diff/protected paths | `PASS` — post-run Ruff, provider-free targeted tests (`15 passed`), provider-free full tests (`53 passed`), and `git diff --check` passed; no diff under `src`, dependencies, `eval/p0b`, `artifacts/p0b-ingest`, or V0 artifacts; all six new run directories retain terminal metadata/events/call traces, and none has a success `report.html`. |
| Owner report/rubric handoff | No report exists because all six runs failed before rendering; six human rubric files are retained under `artifacts/visual-report/v1a/evaluation/vr1a-dev-10f4334c8026/rubrics/` and remain `PENDING_OWNER_REVIEW`; no human score or quality acceptance was filled. |

### Owner handoff inventory

Report paths: none — all six declared runs stopped before `RENDERED` and no
`report.html` was generated.

Rubric paths:

- `artifacts/visual-report/v1a/evaluation/vr1a-dev-10f4334c8026/rubrics/p0b-kling-2024-v1a-cdfab9d75b-r1.json`
- `artifacts/visual-report/v1a/evaluation/vr1a-dev-10f4334c8026/rubrics/p0b-kling-2024-v1a-cdfab9d75b-r2.json`
- `artifacts/visual-report/v1a/evaluation/vr1a-dev-10f4334c8026/rubrics/p0b-rlinf-2026-v1a-cdfab9d75b-r1.json`
- `artifacts/visual-report/v1a/evaluation/vr1a-dev-10f4334c8026/rubrics/p0b-rlinf-2026-v1a-cdfab9d75b-r2.json`
- `artifacts/visual-report/v1a/evaluation/vr1a-dev-10f4334c8026/rubrics/p0b-wuyi-goals-v1a-cdfab9d75b-r1.json`
- `artifacts/visual-report/v1a/evaluation/vr1a-dev-10f4334c8026/rubrics/p0b-wuyi-goals-v1a-cdfab9d75b-r2.json`

## Completion and stop rule

Complete this task only after all six declared identities and the one immutable
evaluation output are retained, or after an honest blocker is recorded. Stop at
`READY_FOR_OWNER_V1A_REVIEW` with one of these exact qualifiers:

- `PENDING_OWNER_REVIEW`;
- `PROVIDER_CONFIGURATION_BLOCKED`;
- `MEASUREMENT_EXECUTION_FAILED`;
- `MEASUREMENT_CANCELLED`.

Only the Owner may record V1-A acceptance, authorize a repair/new full
revision, or begin V1-B/V1-C.
