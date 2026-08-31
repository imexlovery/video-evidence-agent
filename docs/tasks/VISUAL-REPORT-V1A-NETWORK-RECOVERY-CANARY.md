# VR-V1A-NETWORK-RECOVERY-CANARY-009

## Task control

| Field | Value |
|---|---|
| Grade | `G1 PROTOTYPE` |
| Task status | `READY_FOR_OWNER_V1A_REVIEW — NETWORK_RECOVERY_CANARY_PASSED` |
| Task kind | Independent network-recovery diagnostic; `diagnostic_only=true` |
| Repository | `/Users/tristana/Develop/video-evidence-agent` |
| Branch | `visual-report` |
| Design authority | `DEC-VR1A-061/062/065/066/067/068` plus the existing V1-A contracts |
| Frozen read-only baseline | Task 008 revision `vr1a-semantic-v2-29d077aa0bdc` |
| Diagnostic video | `p0b-kling-2024` only |
| Diagnostic run ID | `p0b-kling-2024-semantic-v2-network-recovery-canary-009` |
| Expected calls | `2` provider/model calls for a successful Mapper + Planner path |
| Absolute call ceiling | `3` provider/model calls for this task |
| Current-session execution | `COMPLETED`; one Kling canary; provider/model calls `2/2`; no retry |
| Owner-only boundary | No Task 008 mutation, selective continuation, product acceptance, RLinf/Wu Yi run, Web smoke, evaluator, rubric, commit, push, PR, deploy, V1-B, or V1-C |

## Purpose and classification

Task 009 answers one narrow diagnostic question: whether the existing frozen
DeepSeek semantic-v2 pipeline can complete a single Kling canary when the
provider domain is excluded from the proxy for this one `uv` child process.
It does not measure product quality or prove that the V1-A route is stable.

This task is independent of the exhausted Task 008 product set. It is not a
selective rerun of Task 008's Kling identity, does not replace its two retained
`APIConnectionError` attempts, and cannot add RLinf or Wu Yi after the Task 008
external stop. A successful canary only authorizes a separately designed and
explicitly authorized new complete three-video revision; it never authorizes
continuing the two videos that Task 008 did not start.

## Task 008 preservation contract

The following evidence is immutable input to this diagnostic and must remain
unchanged:

| Evidence | Path or identity | Required fact |
|---|---|---|
| Frozen revision | `eval/visual-report-v1a/semantic-v2-adaptive-budget-web-closure-008-manifest.json` | `revision_id=vr1a-semantic-v2-29d077aa0bdc`; manifest SHA-256 `13e7784d161f101c1e75bbdd104db722d61a72beff56ef65caf45d35431e81b3` |
| Task 008 Kling run | `artifacts/visual-report/v1a/p0b-kling-2024-semantic-v2-e3d720ac27/` | `FAILED`, `PROVIDER_ERROR`, two identical `APIConnectionError` attempts, `provider_calls/model_calls=2/2` |
| Task 008 aggregate | `artifacts/visual-report/v1a/evaluation-008/vr1a-semantic-v2-29d077aa0bdc/aggregate.json` | `technical_status=FAILED`, `stop_state=PROTOTYPE_EXECUTION_INCONCLUSIVE`, observed calls `2/2` |
| Task 008 product manifest | Same frozen manifest | RLinf and Wu Yi were not started after the Kling external stop; product set remains `2/9` and Goal usage `2/12` |
| Working tree | Current checkout | All uncommitted Task 008 source, tests, documents, and manifest are Owner work and must be preserved |

No Task 008 file, run directory, aggregate, manifest, revision, or failure
identity may be edited, overwritten, relabeled, deleted, backfilled, or used as
the new run directory.

## Frozen diagnostic inputs and output

### Input contract `IN-VR1A-NETWORK-CANARY/009-v1`

The next execution session must freeze the following before the first provider
request:

- the new diagnostic run ID shown in Task control;
- the existing Kling manifest and `segments.jsonl` from the Task 008 source
  snapshot;
- the Task 008 revision, prompt versions, raw/canonical semantic-v2 schemas,
  normalizer/compiler, evaluator version, and current V0 renderer contract;
- the exact Task 008 provider tuple: DeepSeek
  `deepseek-v4-flash-vision-exp`, Chat Completions JSON object, Thinking enabled,
  `reasoning_effort=high`, `max_tokens=32768`, temperature `0`, SDK retry `0`,
  and the existing per-run technical retry rule;
- the process-only transport overrides `NO_PROXY=api.deepseek.com` and
  `no_proxy=api.deepseek.com`.

The manifest, transcript, request body, model, API surface, prompt, schema,
normalizer, compiler, budgets, source, and renderer must be byte-for-byte the
same frozen product inputs wherever the existing run contract records them.
The two proxy variables are diagnostic transport metadata only; they must not
change the request body or product revision.

### Output contract `OUT-VR1A-NETWORK-CANARY/009-v1`

The canary must create one new run directory under
`artifacts/visual-report/v1a/` and retain the existing run artifacts required
by the V1-A contract. Its diagnostic manifest or run evidence must explicitly
contain:

```json
{
  "task_id": "VR-V1A-NETWORK-RECOVERY-CANARY-009",
  "diagnostic_only": true,
  "base_revision_id": "vr1a-semantic-v2-29d077aa0bdc",
  "video_id": "p0b-kling-2024",
  "run_id": "p0b-kling-2024-semantic-v2-network-recovery-canary-009",
  "network_overrides": {
    "NO_PROXY": "api.deepseek.com",
    "no_proxy": "api.deepseek.com"
  },
  "product_set_membership": "excluded",
  "task008_replacement": false
}
```

The run must retain `run.json`, `events.jsonl`, `model-calls.jsonl`, raw and
canonical stage artifacts when available, the empty asset manifest and
`report.html` only on a successful render. The diagnostic-only marker must be
visible in the run/task evidence without changing Task 008's manifest or
aggregate. No product aggregate, formal measurement denominator, evaluator
result, or Owner rubric is created for Task 009.

## Network and configuration boundary

Use the existing configured environment for the frozen provider and model.
Only the following two variables may be added, inline, to the single `uv`
child process:

```bash
NO_PROXY=api.deepseek.com \
no_proxy=api.deepseek.com \
uv run python -m video_evidence_agent.visual_report build-from-transcript \
  --manifest artifacts/p0b-ingest/p0b-kling-2024/manifest.json \
  --segments artifacts/p0b-ingest/p0b-kling-2024/segments.jsonl \
  --run-id p0b-kling-2024-semantic-v2-network-recovery-canary-009 \
  --output-root artifacts/visual-report/v1a
```

The command must not modify a global proxy setting, shell profile, `.env`,
provider configuration, model selection, API surface, Thinking setting,
reasoning effort, output limit, prompt, schema, normalizer, compiler, budget,
source, or renderer. Existing `OPENAI_API_KEY`, `OPENAI_BASE_URL`,
`VISUAL_REPORT_MODEL`, and timeout configuration remain provisioned outside the
inline override; their values must never be printed. The next session must
verify that the requested run ID is unused before creating it and must stop if
an existing directory is found.

## Pipeline and retry protocol

Run exactly one complete single-video pipeline when the run is admitted:

```text
Topic Mapper → Report Planner → deterministic Compiler → existing V0 Renderer
```

- A normal successful run is expected to use one Mapper call and one Planner
  call: `provider_calls/model_calls=2/2`.
- The existing run-level technical retry policy remains unchanged. Only a
  qualifying connection/timeout/HTTP `429`/provider `5xx`, empty content,
  provider-declared incomplete output, or malformed non-decodable JSON may use
  one identical retry at the current stage.
- If the retry is used, both attempts must be retained and the Task 009 total
  must remain at or below `3` provider/model calls.
- Valid JSON with weak semantics, invalid grounding, unsupported metrics,
  insufficient content, V0 incompatibility, or a hard budget failure is not
  retryable.
- No call may be added for an evaluator, human rubric, Web smoke, RLinf, Wu Yi,
  prompt correction, semantic repair, fallback provider/model, or a third
  semantic stage.

## Deterministic and product boundaries

The model responsibilities and deterministic ownership remain exactly those of
the frozen semantic-v2 revision. Models select semantic content and existing
source IDs only. Deterministic code owns canonical IDs, timestamps, source
refs, adaptive budget, typed-block compatibility, validation, state, evidence,
and rendering. The normalizer/compiler may not rewrite, shorten, expand,
delete for budget, merge, split, fabricate, or synthesize semantic content.

`diagnostic_only=true` means:

- the canary is excluded from the Task 008 product set and every V1-A product
  or formal-measurement denominator;
- a passing `RENDERED` state is transport/runtime evidence only, not product
  quality, stability, acceptance, or release evidence;
- a failure does not alter the Task 008 conclusion or authorize a rerun of its
  remaining videos; and
- the run stops immediately after its success or classified failure.

## Stop rules and terminal matrix

No evaluator, human rubric, Web server/smoke, RLinf/Wu Yi run, prompt tuning,
compiler/provider/model change, micro-version, commit, push, PR, deployment,
V1-B, or V1-C may follow the canary. Use exactly one terminal classification:

| Observed boundary | Required terminal |
|---|---|
| Mapper and Planner complete; compiler and existing V0 renderer produce the diagnostic report | `READY_FOR_OWNER_V1A_REVIEW — NETWORK_RECOVERY_CANARY_PASSED` |
| The configured endpoint remains unreachable after the allowed identical technical retry, with configuration otherwise valid | `READY_FOR_OWNER_V1A_REVIEW — NETWORK_RECOVERY_EXTERNAL_BLOCKED` |
| Credential, balance, permission, or configured model access is unavailable | `READY_FOR_OWNER_V1A_REVIEW — NETWORK_RECOVERY_CONFIGURATION_BLOCKED` |
| An API/JSON technical failure remains after one eligible identical retry and cannot be classified as endpoint reachability or configuration | `READY_FOR_OWNER_V1A_REVIEW — NETWORK_RECOVERY_RUNTIME_INCONCLUSIVE` |
| Network succeeds, but valid semantic output cannot compile or render without prohibited semantic repair | `READY_FOR_OWNER_V1A_REVIEW — NETWORK_RECOVERY_CONTENT_INSUFFICIENT` |
| Continuing would require changing prompt, compiler, provider, model, budget, source, renderer, or another product contract | `READY_FOR_OWNER_V1A_REVIEW — NETWORK_RECOVERY_CONTRACT_CHANGE_REQUIRED` |

The terminal, run state, attempt count, and evidence paths must be appended to
this task and `docs/visual-report/V1A-STATUS.md` after the separate execution
session. No terminal is recorded during the current requirements session.

## Acceptance matrix for the next execution session

| ID | Evidence | Pass condition |
|---|---|---|
| `NRC-001` | Branch/worktree and Task 008 inventory | `visual-report` is current; all Task 008 source, tests, docs, manifest, run, aggregate, and failure attempts remain unchanged |
| `NRC-002` | Diagnostic manifest/run metadata | New run ID is unique; `diagnostic_only=true`; Task 008 revision is referenced read-only; product-set membership is excluded |
| `NRC-003` | Process environment inspection | Only inline `NO_PROXY`/`no_proxy` additions are present; global proxy, shell profile, and `.env` are unchanged |
| `NRC-004` | Request/config snapshot comparison | Provider, model, API, Thinking, reasoning, tokens, prompts, schemas, normalizer, compiler, budgets, sources, and renderer match Task 008; only transport override differs |
| `NRC-005` | Complete canary trace | Topic Mapper → Report Planner → Compiler → V0 Renderer executes once; normal success is `2/2`; no more than `3` calls total |
| `NRC-006` | Retry ledger | Any retry is eligible, identical, synchronous, and retained; semantic output never triggers retry |
| `NRC-007` | Isolation audit | Task 008 aggregate/manifest/run and unstarted RLinf/Wu Yi/Web identities are untouched; no product denominator or evaluator is created |
| `NRC-008` | Terminal evidence | Exactly one terminal from the matrix is recorded with stable category, stage, calls, and artifact paths; execution stops immediately |
| `NRC-009` | Post-task scope review | No prompt tuning, product-code/dependency/infrastructure change, commit, push, PR, deployment, V1-B, or V1-C occurred |

## Current documentation-session boundary

This requirements/documentation session creates no diagnostic manifest, run
directory, runtime artifact, model request, evaluator output, or human rubric.
It only publishes this task, appends the two Owner evidence records, updates
the canonical requirements/status links, and regenerates the independent
requirements-readiness artifact. Current-session `model_calls=0` is a required
reported fact.

## Next construction-session Goal prompt

Copy the following into a separate execution session only after the Owner starts
Task 009:

```text
Goal: Execute VR-V1A-NETWORK-RECOVERY-CANARY-009 as one bounded diagnostic-only
network recovery canary.

Repository: /Users/tristana/Develop/video-evidence-agent
Branch: visual-report

Preserve all existing uncommitted Task 008 Owner work. Do not reset, overwrite,
reinitialize, or selectively rerun Task 008. Treat the frozen revision
vr1a-semantic-v2-29d077aa0bdc, its manifest, Kling run
p0b-kling-2024-semantic-v2-e3d720ac27, aggregate, and all historical evidence as
read-only. Task 008 ended at READY_FOR_OWNER_V1A_REVIEW — EXTERNAL_BLOCKED after
two retained identical APIConnectionError attempts, 2/2; RLinf, Wu Yi, and Web
smoke were not started.

Before any provider request, verify the new run ID is unused and freeze
diagnostic_only=true for:
p0b-kling-2024-semantic-v2-network-recovery-canary-009.
Use only the existing Kling manifest and segments with the exact Task 008
provider/model/API/Thinking/reasoning/max_tokens/prompt/schema/normalizer/
compiler/budget/source/renderer tuple. The only process-level network override
is:

NO_PROXY=api.deepseek.com \
no_proxy=api.deepseek.com \
uv run ...

Do not modify the global proxy, shell profile, .env, dependencies, product
code, runtime contract, or infrastructure. Do not print secrets. Run one
complete pipeline only: Topic Mapper → Report Planner → Compiler → V0 Renderer.
Expect 2 provider/model calls on success. Apply the existing identical technical
retry rule only for an eligible API/JSON technical anomaly, retain both
attempts, and never exceed 3 total calls. Do not retry semantic output.

Stop immediately after success or failure. Do not run RLinf, Wu Yi, Web smoke,
evaluator, rubric, prompt tuning, contract repair, micro-version, commit, push,
PR, deploy, V1-B, or V1-C. Do not add this canary to Task 008 or any product or
formal-measurement denominator. Append the run/task evidence and V1A status with
exactly one terminal:

READY_FOR_OWNER_V1A_REVIEW — NETWORK_RECOVERY_CANARY_PASSED
READY_FOR_OWNER_V1A_REVIEW — NETWORK_RECOVERY_EXTERNAL_BLOCKED
READY_FOR_OWNER_V1A_REVIEW — NETWORK_RECOVERY_CONFIGURATION_BLOCKED
READY_FOR_OWNER_V1A_REVIEW — NETWORK_RECOVERY_RUNTIME_INCONCLUSIVE
READY_FOR_OWNER_V1A_REVIEW — NETWORK_RECOVERY_CONTENT_INSUFFICIENT
READY_FOR_OWNER_V1A_REVIEW — NETWORK_RECOVERY_CONTRACT_CHANGE_REQUIRED

Return the exact terminal, run ID, provider/model call totals, preserved
Task 008 evidence paths, new diagnostic artifact paths, and whether any product
code/dependency/runtime/infrastructure change occurred.
```

## Execution evidence — 2026-08-31

The canary run ID was verified unused immediately before execution. The first
shell attempt stopped in `uv` cache initialization before the pipeline started,
created no run directory, and made no provider/model call. One controlled
execution of the same semantic-v2 entry point then ran with only the requested
process-scoped `NO_PROXY=api.deepseek.com` and `no_proxy=api.deepseek.com`
overrides.

The single executed pipeline completed in order:

```text
Topic Mapper → Report Planner → deterministic Compiler → V0 Renderer
```

Observed result:

- run state: `RENDERED`;
- exact terminal: `READY_FOR_OWNER_V1A_REVIEW — NETWORK_RECOVERY_CANARY_PASSED`;
- provider/model calls: `2/2` (`topic_mapper=1`, `report_planner=1`);
- technical retry: not used; both attempts had `finish_reason=stop` and valid
  semantic-v2 JSON;
- output: 5 sections, 14 compiled blocks, empty asset manifest and canonical
  `report.html`;
- adaptive diagnostics: recommendation `21` blocks, actual `14`, visible
  authored characters `1,055`; both are soft undershoots and hard limits passed;
- normalization ledger: 3 recorded non-semantic events, 1 whole unusable unit
  omission, and zero semantic rewrite/merge/split/synthesis events.

The run and diagnostic manifest explicitly record `diagnostic_only=true`, base
revision `vr1a-semantic-v2-29d077aa0bdc`, both process override labels,
`product_set_membership=excluded`, and `task008_replacement=false`.

New diagnostic evidence:

- `artifacts/visual-report/v1a/p0b-kling-2024-semantic-v2-network-recovery-canary-009/diagnostic-manifest.json`
- `artifacts/visual-report/v1a/p0b-kling-2024-semantic-v2-network-recovery-canary-009/run.json`
- `artifacts/visual-report/v1a/p0b-kling-2024-semantic-v2-network-recovery-canary-009/events.jsonl`
- `artifacts/visual-report/v1a/p0b-kling-2024-semantic-v2-network-recovery-canary-009/model-calls.jsonl`
- `artifacts/visual-report/v1a/p0b-kling-2024-semantic-v2-network-recovery-canary-009/topic-map.json`
- `artifacts/visual-report/v1a/p0b-kling-2024-semantic-v2-network-recovery-canary-009/topic-map.raw.json`
- `artifacts/visual-report/v1a/p0b-kling-2024-semantic-v2-network-recovery-canary-009/topic-normalization.json`
- `artifacts/visual-report/v1a/p0b-kling-2024-semantic-v2-network-recovery-canary-009/planning-budget.json`
- `artifacts/visual-report/v1a/p0b-kling-2024-semantic-v2-network-recovery-canary-009/planner-request.json`
- `artifacts/visual-report/v1a/p0b-kling-2024-semantic-v2-network-recovery-canary-009/report-plan.raw.json`
- `artifacts/visual-report/v1a/p0b-kling-2024-semantic-v2-network-recovery-canary-009/report-plan.json`
- `artifacts/visual-report/v1a/p0b-kling-2024-semantic-v2-network-recovery-canary-009/planner-normalization.json`
- `artifacts/visual-report/v1a/p0b-kling-2024-semantic-v2-network-recovery-canary-009/normalization.json`
- `artifacts/visual-report/v1a/p0b-kling-2024-semantic-v2-network-recovery-canary-009/budget-diagnostics.json`
- `artifacts/visual-report/v1a/p0b-kling-2024-semantic-v2-network-recovery-canary-009/validation.json`
- `artifacts/visual-report/v1a/p0b-kling-2024-semantic-v2-network-recovery-canary-009/assets.json`
- `artifacts/visual-report/v1a/p0b-kling-2024-semantic-v2-network-recovery-canary-009/report.html`

Preserved Task 008 evidence remains read-only and unchanged:

- `eval/visual-report-v1a/semantic-v2-adaptive-budget-web-closure-008-manifest.json`
- `artifacts/visual-report/v1a/p0b-kling-2024-semantic-v2-e3d720ac27/`
- `artifacts/visual-report/v1a/evaluation-008/vr1a-semantic-v2-29d077aa0bdc/aggregate.json`

The frozen Task 008 manifest, Kling `run.json`, events, model-call ledger, and
aggregate retained their pre-run SHA-256 values. No RLinf, Wu Yi, Web smoke,
evaluator, rubric, new product/formal denominator, prompt tuning, contract
repair, commit, push, PR, deployment, V1-B, or V1-C action followed the
canary. No product-code, dependency, runtime, or infrastructure file changed;
only this task/status evidence and the new diagnostic run artifacts were added
or updated.
