# Task: Video Visual Report V1-A Goal Recovery and Development Measurement

## Task metadata

| Field | Value |
|---|---|
| Task ID | `VR-V1A-GOAL-RECOVERY-003` |
| Grade | `G1 PROTOTYPE` |
| Mode | One continuous Goal session |
| Task status | `READY_FOR_OWNER_V1A_REVIEW — GOAL_RECOVERY_EXHAUSTED` |
| Repository | `/Users/tristana/Develop/video-evidence-agent` |
| Branch | `visual-report` |
| Code baseline | `f8cb402d37bc05a30c7a912ed044548a71c128c7` plus all current uncommitted Owner work |
| Historical failed revision | `vr1a-dev-10f4334c8026` — immutable |
| Previous conclusion | `READY_FOR_OWNER_V1A_REVIEW — MEASUREMENT_EXECUTION_FAILED` |
| Required successful stop | `READY_FOR_OWNER_V1A_REVIEW — PENDING_OWNER_REVIEW` |
| Bounded unsuccessful stops | `READY_FOR_OWNER_V1A_REVIEW — GOAL_RECOVERY_EXHAUSTED` or `READY_FOR_OWNER_V1A_REVIEW — EXTERNAL_BLOCKED` |

## Owner authorization

On 2026-08-30 the Owner asked to stop splitting V1-A into many manually
published construction sessions and instead run the already-approved V1-A
design through one Goal session. That session is authorized to diagnose,
repair, test, call the configured provider, run fresh canaries and complete
Development measurements, evaluate the results, and update the task/status
evidence without pausing for ordinary in-scope engineering failures.

This is a new authorization after `VR-V1A-MEASUREMENT-002`. It does not rewrite,
retry, rescore, or relabel `vr1a-dev-10f4334c8026` or any of its six failed run
directories.

## Goal

Starting from the current working tree, make the smallest evidence-backed V1-A
repair that lets the configured OpenAI-compatible provider produce first-pass
strict Topic Mapper and Report Planner outputs, then complete one valid frozen
three-video × two-repeat Development measurement and hand the real reports and
pending human rubrics to the Owner.

The implementation agent must create one active Goal for this objective and
continue across automatic Goal turns until it reaches one of the three terminal
states in this task. Do not set a token budget unless the Owner adds one.

Routine failures are work to diagnose and repair, not reasons to ask the Owner
to publish another task. The hard stops in this card are the only exceptions.

## Required read order

Read before changing code or admitting a provider call:

1. `AGENTS.md`
2. `docs/visual-report/V1A-STATUS.md`
3. `docs/requirements/visual-report-v1a/requirements-readiness.json`
4. `docs/requirements/visual-report-v1a/00-handoff.md`
5. `docs/requirements/visual-report-v1a/12-engineering-context.md`
6. `docs/requirements/visual-report-v1a/03-functional-spec.md`
7. `docs/requirements/visual-report-v1a/06-interfaces-integrations.md`
8. `docs/requirements/visual-report-v1a/07-agent-behavior.md`
9. `docs/requirements/visual-report-v1a/09-test-acceptance.md`
10. `docs/requirements/visual-report-v1a/10-delivery-plan.md`
11. `docs/requirements/visual-report-v1a/11-decisions-risks.md`
12. `docs/tasks/VISUAL-REPORT-V1A-PLANNING.md`
13. `docs/tasks/VISUAL-REPORT-V1A-MEASUREMENT.md`
14. this task card

Then inspect the current implementation, the frozen v3 measurement manifest,
the six `run.json` files, their raw Mapper responses and call traces, and the
v3 aggregate. Treat raw transcripts, responses, local credentials, and local
artifacts as non-public data even though transcript provider processing is
authorized.

## Current diagnosis to verify, not blindly assume

The last measurement established a provider-output-contract failure, not a
V1-A quality result:

- one run ended in `PROVIDER_ERROR` before a valid Mapper proposal;
- five runs returned JSON that failed the strict Topic Map schema;
- no run reached Planner, compiler, or renderer;
- observed `provider_calls/model_calls=6/6`, not the planned `12/12`;
- the evaluator correctly returned `measurement_valid=false` and
  `MEASUREMENT_EXECUTION_FAILED`;
- provider-free tests passed because their fake responses were already valid,
  so they did not prove that the real prompt transports the exact schema;
- the current prompt names a schema version but does not transport the actual
  field contract or a valid output example;
- the current request uses JSON-object mode without an explicit output-token
  cap or recorded reasoning/thinking control.

Inspect the five raw invalid responses structurally. At minimum, preserve
regression coverage for the observed wrong shapes: integer segment ordinals,
`segment_ids` instead of `source_segment_ids`, topics represented as strings,
`description` replacing required summaries/refs, and missing
`schema_version`. Do not copy transcript content into tests when a synthetic
fixture proves the same contract.

## Non-negotiable V1-A runtime invariants

These remain unchanged throughout every candidate and formal revision:

- Topic Mapper and Report Planner are two sequential independent model calls.
- Both receive the complete authorized transcript; Planner also receives the
  bound canonical Topic Map.
- One successful pipeline run has exactly `2/2` admitted provider/model calls.
- Models emit semantic content and existing `segment_id` values only.
- Deterministic code owns canonical topic/block IDs, timestamps, `SourceRef`,
  budgets, validation, compilation, run state, and renderer invocation.
- The strict proposal schemas remain fail-closed. Do not weaken them merely to
  accept the five observed provider guesses.
- No semantic repair, field renaming/coercion, invalid-block deletion, manual
  plan substitution, third model call, SDK retry, alternate provider/model
  fallback, hidden truncation, or chunking is allowed inside a pipeline run.
- Mapper failure prevents Planner; Planner/compile failure prevents a rendered
  success claim.
- V1-A compiles the current V0 `ReportPlan`, emits an empty current
  `assets.json`, and reuses the existing deterministic renderer.
- Every diagnostic, canary, and measured run uses a unique directory and is
  retained in its original terminal state.
- A prompt, schema, model, response mode, source, compiler, evaluator, or
  policy change creates a new candidate/measurement revision. Never mutate a
  frozen revision.

Automatic Goal recovery is an engineering loop *between* new immutable run
identities and revisions. It is not an in-run retry or an LLM repair loop.

## Authorized change envelope

Make only changes demonstrated necessary by the observed failure, normally in:

- `src/video_evidence_agent/visual_report/planning.py`
- `src/video_evidence_agent/visual_report/planning_runtime.py`
- `src/video_evidence_agent/visual_report/evaluation.py` only for a reproduced
  evaluator/evidence defect
- `src/video_evidence_agent/visual_report/__main__.py` only for a reproduced
  CLI/config surface defect
- `tests/test_visual_report_planning.py` and its existing synthetic fixtures
- `.env.example` for non-secret, operator-facing V1-A settings only
- fresh versioned manifests/review/evaluation artifacts under
  `eval/visual-report-v1a/` and ignored `artifacts/visual-report/v1a/`
- this task, the V1-A status page, and V1-A requirement/evidence documents

Use the existing OpenAI SDK and Pydantic stack. Dependency changes are allowed
only if a reproduced provider capability gap cannot be solved through the
installed SDK's supported API; document the evidence before `uv add` and keep
the change minimal. Never edit or print `.env`, secret values, or authorization
headers.

Do not modify frozen P0-B evidence, source transcripts/manifests, the answering
path, V0 report content/assets/screenshots, deployment/infrastructure, or any
V1-B/V1-C capability. A V0 renderer/model change requires a reproduced V1-A
compatibility defect that cannot be fixed in the V1-A adapter and must be
called out explicitly in the handoff.

## Required repair properties

The exact transport is implementation-delegated inside the approved
OpenAI-compatible boundary, but the repaired contract must provide all of the
following:

1. The runtime Mapper and Planner requests transport the exact required output
   field contract, using provider-enforced JSON Schema when the selected model
   truly supports it, or otherwise an explicit schema plus compact valid JSON
   example in JSON-object mode. Merely naming the schema version is insufficient.
2. Both prompts explicitly require all mandatory fields and exact existing
   `segment_id` strings. Provider output still passes through the same strict
   Pydantic validation and deterministic binder/compiler.
3. The request sets and snapshots an explicit output-token limit with enough
   headroom for the declared Mapper/Planner budgets.
4. Reasoning/thinking mode is explicitly controlled and recorded. If the
   provider ignores temperature in thinking mode, disable thinking for this
   schema task or select another compatible model within `DEC-VR1A-048`; do not
   claim temperature-zero determinism when the provider does not supply it.
5. Non-secret response diagnostics record response mode, exact model,
   reasoning setting, output-token limit, finish reason, content-present flag,
   content byte count/hash, latency, usage, and stable error category. Raw
   responses remain in the unique local run directory; requests/transcripts
   and credentials are not copied into status logs.
6. Tests cover the five observed wrong shapes, valid Mapper and Planner
   response transport, truncation/no-content/provider-error behavior, exact
   call counts, and replay. A test must prove the runtime prompt/request exposes
   the current schema rather than only feeding a pre-valid fake response.

Before selecting or changing a real model/response mode, verify the current
capability against the provider's official documentation or a non-transcript
capability preflight. Freeze and record the exact result; do not silently fall
back during a run.

## One-session execution protocol

### G0 — Preserve and classify the baseline

- Record `git status --short`, current HEAD, changed/untracked paths, configured
  variable presence as booleans, and the v3 failure inventory.
- Preserve the Owner's uncommitted `.env.example` and all current documentation,
  manifests, failed runs, aggregates, and rubrics.
- Confirm no product source changed after the committed V1-A baseline before
  applying this task's repair. If it did, classify and preserve it rather than
  overwriting it.
- Write a concise root-cause note in this task's evidence section before code
  changes. Separate provider transport, output-contract, validator, evaluator,
  and semantic-quality findings.

### G1 — Repair the real output contract provider-free

- Implement the smallest repair satisfying “Required repair properties.”
- Add synthetic regression cases for every observed invalid response shape.
- Run targeted Ruff and the V1-A planning tests until green.
- Run a fake end-to-end build/replay and prove successful `2/2` call accounting
  plus deterministic compiler/render output; provider-free replay remains
  `0/0`.
- Do not admit a real provider call while any targeted check fails.

### G2 — Three-video canary gate

- Create a fresh candidate revision and three new canary run IDs, one for each
  fixed video. Canary identities are diagnostic evidence, never members of a
  later six-run denominator.
- Execute each canary once, sequentially. Stop the current canary set on its
  first failure; do not retry its run ID.
- All three must reach `RENDERED`, each with a first-pass valid Mapper and
  Planner response and exactly `2/2` calls, before a formal revision can freeze.
- Inspect the generated Topic Map, plan, empty assets, HTML, run state, raw
  response, and non-secret call trace for contract completeness. Do not assign
  human quality scores at this gate.

If a canary fails, retain it, diagnose the failure, return to G1 automatically,
and create a new candidate revision and new canary IDs after the repair. Never
turn a canary failure into a retry of the same identity.

### G3 — Freeze and execute a fresh formal measurement

- Only after G2 passes, freeze prompts, exact provider/model/API mode,
  reasoning setting, token limit, schemas, compiler, evaluator, source hashes,
  review cards, and code revision into a new manifest. Do not overwrite v2/v3
  manifests or their evaluation directories.
- Predeclare six new run IDs: two repeats for each fixed video. Canary IDs are
  excluded from this denominator.
- Execute all six exactly once even if an earlier formal run fails. No tuning or
  repair occurs inside that frozen six-run revision.
- Run the evaluator exactly once after all six reach terminal state. Retain all
  failures/cancellations in the denominator and keep `cost=unavailable` unless
  an authoritative versioned price source exists.
- Never fill human rubric scores, fabricate reports, or record Owner acceptance.

### G4 — Automatic cross-revision recovery

If the formal aggregate is invalid because of an in-scope implementation,
prompt-contract, response-mode, reasoning-control, token-budget, transport
observability, compiler, CLI, or evaluator defect:

1. freeze the entire failed revision, aggregate, raw outputs, and rubric files;
2. write a specific evidence-backed diagnosis;
3. repair only the demonstrated defect;
4. rerun G1 provider-free gates;
5. run G2 with new canary IDs;
6. freeze and run G3 with a wholly new six-run revision.

Do this without asking the Owner to publish another session. A transient
provider error inside a formal revision remains a failed measured run; it is
never retried or removed. A later complete revision is allowed only through
this explicit recovery loop.

If the measurement is execution-valid but misses semantic/human quality
thresholds, stop for Owner review. Do not auto-tune prompts against the six
reports, because that would turn the fixed Development population into an
optimization set.

### G5 — Regression and handoff

After the latest formal evaluator result:

- run targeted tests, full pytest, Ruff, `git diff --check`, protected-path
  review, and the existing V0 renderer regression;
- verify all earlier failed revisions and run directories still exist and have
  unchanged terminal identities;
- update this task's evidence section and `docs/visual-report/V1A-STATUS.md` in
  the same session;
- list changed source/test/docs paths, all new candidate/formal revisions,
  call counts, failure categories, aggregate path, reports, and pending rubrics;
- stop at the exact terminal state. Do not commit, push, open a PR, deploy,
  publish, start V1-B/V1-C, or record `OWNER_ACCEPTED` unless the Owner adds a
  separate explicit instruction.

## Autonomous decision policy

Do not pause for routine choices that can be resolved from repository evidence,
provider official capability documentation, tests, or the fixed V1-A contract.
In particular, continue automatically through prompt/schema transport fixes,
provider-supported response API selection, reasoning/token configuration,
targeted test repair, fresh canaries, fresh revision manifests, evaluator
repair, and regression failures within the authorized paths.

Prefer the smallest sufficient change. Do not use automatic recovery as a
reason to refactor unrelated code, add compatibility layers, introduce an
Agent/framework/service, or harden beyond the observed defect.

## Recovery and provider-call budget

- At most two new formal six-run measurement revisions may be attempted by this
  task.
- Canary attempts stop on first failure and use fresh identities. Combined
  canary and formal execution may admit at most 36 new provider/model calls.
- Each pipeline identity still admits at most two calls, one Mapper and one
  Planner; SDK retry remains zero.
- Provider-free diagnosis, tests, replay, and deterministic evaluation do not
  consume this external-call budget.
- Stop early as soon as one formal revision is execution-valid; do not spend the
  remaining budget on optional tuning or extra measurements.

The budget is a safety ceiling, not a target and not permission to make repeated
unchanged attempts. Every later candidate must be justified by a recorded
diagnosis and a material repair/configuration revision.

## Hard stops

Stop at `READY_FOR_OWNER_V1A_REVIEW — EXTERNAL_BLOCKED` without inventing a
workaround when any of these applies:

- credentials are absent/invalid, billing/quota/access is denied, or the Owner
  must change an external account or secret;
- the approved endpoint has no compatible model/response mode within the fixed
  full-context, two-call, strict-schema boundary;
- continuing would expose credentials, publish restricted artifacts, or require
  new privacy/source authorization;
- the fix requires changing frozen P0-B/source data, adding MP4/ASR, images,
  OCR/VLM, RAG, Agent/LangGraph, database/service/deployment, V1-B, or V1-C;
- a required decision would alter the Owner-confirmed quality thresholds,
  denominator, product behavior, or phase authority.

Stop at `READY_FOR_OWNER_V1A_REVIEW — GOAL_RECOVERY_EXHAUSTED` when the two
formal-attempt or 36-call ceiling is reached without an execution-valid formal
revision. Preserve and summarize all evidence; do not request a third attempt
inside the same Goal.

## Acceptance and terminal states

### `READY_FOR_OWNER_V1A_REVIEW — PENDING_OWNER_REVIEW`

Use only when the latest formal aggregate has:

- `measurement_valid=true`;
- six declared runs, all six `RENDERED`;
- observed `provider_calls/model_calls=12/12`;
- first-pass strict Mapper schema, Planner schema, compile, empty-assets render,
  and source-ref validation for `6/6` runs;
- six real report paths and six pending Owner rubric files;
- deterministic acceptance checks evaluated exactly as specified;
- no human scores or `OWNER_ACCEPTED` claim.

The Owner then reviews report quality and fills/approves the rubrics. A valid
measurement can still fail human quality thresholds; that is an honest Owner
review result, not permission to tune or continue into V1-B/C.

### `READY_FOR_OWNER_V1A_REVIEW — GOAL_RECOVERY_EXHAUSTED`

Use when the bounded autonomous recovery budget ends without a valid formal
measurement. Report every revision and failure; do not hide a failed candidate
or reuse a favorable subset.

### `READY_FOR_OWNER_V1A_REVIEW — EXTERNAL_BLOCKED`

Use for a hard stop requiring Owner authority or external-state change. Show
the exact non-secret blocker and the smallest action the Owner must take.

## Required verification commands

```bash
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run ruff check .
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q tests/test_visual_report_planning.py
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q
git diff --check
```

Also run the existing documented V0 renderer regression, the task-selected
three-video canary commands, six explicit `build-from-transcript` commands per
formal revision, and the existing V1-A evaluator command. Record exact commands
and outcomes in this card; do not place secret values or transcript bodies in
the evidence.

## Execution evidence

### 2026-08-30 — G0 baseline and root-cause classification

- Goal: `01a05229-fefa-7250-b60b-e2c22e2581b1`, active; repository HEAD is
  `f8cb402d37bc05a30c7a912ed044548a71c128c7` on `visual-report`.
- The pre-existing `.env.example`, V1-A requirement/status changes, untracked
  recovery/measurement task cards, and `measurement-manifest-v3.json` remain
  untouched. No product, dependency, P0-B, source-transcript, or V0 artifact
  path had a pre-recovery diff. The local `.env` exists, but process-level
  credential/model variables were absent until the runtime's safe dotenv
  loader; no secret value was read into evidence.
- Historical evidence is retained: v2 revision
  `vr1a-dev-cecd6a62e6b2`, v3 revision `vr1a-dev-10f4334c8026`, all twelve
  historical run directories, both historical evaluation aggregates, and all
  pending rubric files remain present.
- Provider transport finding: v3 run
  `p0b-kling-2024-v1a-cdfab9d75b-r1` ended with one admitted Mapper call and
  `PROVIDER_ERROR` caused by `APIConnectionError`. This is a failed run, not a
  retry target or a V1-A quality result.
- Mapper output-contract finding: the other five v3 runs each admitted one
  Mapper call and returned parseable JSON rejected by the unchanged strict
  schema. Observed wrong shapes were: missing `schema_version`; topic objects
  using integer ordinal `segment_ids`; `topics` represented as strings; and
  topic objects using `description` without `summary` or
  `source_segment_ids`. No Planner call, compiler result, renderer result, or
  semantic-quality score exists for v3.
- Validator finding: `TopicMapProposal` fail-closed behavior is correct and
  remains unchanged; no field coercion, aliasing, semantic repair, or schema
  weakening is authorized.
- Evaluator finding: v3 aggregate is correct with
  `measurement_valid=false`, `conclusion=MEASUREMENT_EXECUTION_FAILED`,
  declared calls `12/12`, observed calls `6/6`, six deterministic rows, and six
  pending rubrics. No evaluator defect is indicated by the retained evidence.
- Repair target: the current Mapper/Planner requests only name the schema
  version, use JSON-object mode without an explicit output-token limit or
  reasoning/thinking control, and traces omit response finish/content
  diagnostics. The smallest authorized repair is to transport exact mandatory
  fields plus valid compact examples, set and snapshot explicit token/reasoning
  controls, and record non-secret response diagnostics while preserving the
  strict validator and two-call runtime boundary.
- Provider capability gate: the current official DeepSeek Chat Completions,
  JSON Output, Thinking Mode, and model documentation confirms
  `deepseek-v4-flash-vision-exp` supports Chat Completions, `json_object`,
  `max_tokens`, and an explicit `thinking.type=disabled` control. The candidate
  therefore keeps the existing explicit model/JSON-object route and will freeze
  `thinking_mode=disabled`, temperature `0`, and `output_token_limit=8192`; no
  alternate model or response mode is introduced.

Fill this section append-only during the Goal session. Do not pre-mark future
work as passed.

| Evidence | Result |
|---|---|
| Goal ID/status | `PENDING` |
| Baseline HEAD and preserved worktree | `PENDING` |
| v3 failure/root-cause classification | `PENDING` |
| Changed source/test/config/docs paths | `PENDING` |
| Provider-free targeted gate | `PENDING` |
| Canary revisions, IDs, calls, terminal states | `PENDING` |
| Formal revisions and manifests | `PENDING` |
| Formal run inventory and `provider_calls/model_calls` | `PENDING` |
| Evaluator aggregate and `measurement_valid` | `PENDING` |
| Report and pending-rubric inventory | `PENDING` |
| Full regression/Ruff/diff/V0 renderer | `PENDING` |
| Protected and historical evidence preservation | `PENDING` |
| Final exact terminal state | `PENDING` |

### 2026-08-30 — G1/G2 recovery stop at external boundary

- The repair stayed within the authorized envelope. `planning.py` now
  transports the exact Mapper/Planner field contracts and compact valid
  examples; the installed OpenAI SDK request now records and sends
  `json_object`, temperature `0`, `max_tokens=8192`, and
  `thinking.type=disabled`; response traces include non-secret finish/content
  diagnostics. Strict Pydantic validation, deterministic binding/compiler,
  the two-call boundary, and no-retry behavior remain unchanged.
- Provider-free verification passed before the first canary: targeted planning
  tests `24 passed`, full pytest `62 passed`, full Ruff `All checks passed!`,
  `git diff --check`, protected-path review (`19` changed/untracked paths),
  and the offline V0 renderer regression (`4 sections, 13 blocks, 4 used
  assets`) rendered to a fresh `/private/tmp` output without touching the
  canonical V0 artifact.
- Fresh candidate `vr1a-canary-251171cb760b` was recorded in
  `eval/visual-report-v1a/canary-candidate-vr1a-canary-251171cb760b.json`.
  Its Kling canary
  `p0b-kling-2024-v1a-251171cb760b-canary` was executed once and retained as
  `FAILED`, with `provider_calls/model_calls=1/1` and
  `PROVIDER_ERROR`/`APIConnectionError` before Mapper content; no retry or
  other canary in that set was admitted.
- Transport diagnosis: the sandboxed path first attempted the configured
  local proxy at `127.0.0.1:7897` and failed to connect; an explicit no-proxy
  check then failed DNS resolution for `api.deepseek.com`. A new candidate
  `vr1a-canary-73b6a5104201` was recorded with fresh canary identities, but
  the required external-network execution was rejected by the security
  boundary because it would send restricted transcript-derived payloads to
  `https://api.deepseek.com`. Its run IDs were therefore not admitted.
- No new formal measurement revision was frozen; no formal six-run
  denominator, evaluator aggregate, or Owner rubric set was created by this
  recovery attempt. Historical revisions `vr1a-dev-cecd6a62e6b2` and
  `vr1a-dev-10f4334c8026`, all prior runs/aggregates/rubrics, the current
  uncommitted Owner work, and frozen P0-B/source/V0 paths remain preserved.
- Exact terminal state: `READY_FOR_OWNER_V1A_REVIEW — EXTERNAL_BLOCKED`.
  Continuing requires explicit approval for the restricted full-transcript
  egress to the configured DeepSeek endpoint and an execution environment
  with external network access. No `OWNER_ACCEPTED` state or V1-B/V1-C work
  was recorded.

### 2026-08-30 — G1/G2/G5 final bounded recovery stop

- The Owner subsequently gave explicit ordinary-message authorization for the
  complete authorized transcript-derived payload to be sent to
  `https://api.deepseek.com` for the V1-A canary and formal measurement. The
  approved external execution path was used only for retained canary
  identities; no credential value or transcript body was copied into this
  evidence.
- The implementation repair remains within the V1-A envelope. `planning.py`
  transports the strict Mapper/Planner contracts, valid examples, dynamic
  section source allowlists, exact planning budgets, single-line JSON
  serialization checks, `json_object`, temperature `0`, `max_tokens=8192`,
  `thinking.type=disabled`, and non-secret response diagnostics. The strict
  Pydantic schemas, deterministic binder/compiler, two independent calls, and
  SDK retry `0` remain unchanged. Changed implementation/test paths are
  `src/video_evidence_agent/visual_report/planning.py`,
  `src/video_evidence_agent/visual_report/planning_runtime.py`,
  `src/video_evidence_agent/visual_report/evaluation.py`, and
  `tests/test_visual_report_planning.py`; existing Owner requirement/status
  changes and the recovery/measurement task evidence files remain preserved.
- Provider-free validation after the final p16 repair passed: targeted
  planning tests `28 passed`, full pytest `66 passed`, full Ruff `All checks
  passed!`, and `git diff --check` passed. The existing V0 renderer regression
  passed with `4 sections, 13 blocks, 4 used assets` to a fresh temporary
  output. The protected-path check passed for `39` changed/untracked paths:
  no P0-B/source-transcript/manifest/V0 renderer or canonical V0 artifact path
  was changed.
- All canary candidate manifests are retained under
  `eval/visual-report-v1a/canary-candidate-*.json`. There are `22` candidate
  revisions: `20` admitted Kling canary run directories and `2` metadata-only
  candidates whose identities were never admitted. The admitted run inventory
  is `20/20 FAILED`, `36/36` provider/model calls, and no canary reached
  `RENDERED`; because each candidate set stopped on its first Kling failure,
  no RLinf or Wu Yi canary identity was admitted. Grouped failure evidence is:
  `PROVIDER_ERROR` `vr1a-canary-251171cb760b` (`1/1`),
  `TOPIC_MAP_SCHEMA_ERROR` `vr1a-canary-73b6a5104201` and
  `vr1a-canary-1a6dc2fafbb8` (`1/1` each),
  `SEGMENT_ACCOUNTING_ERROR` `vr1a-canary-d61de0d61859` (`1/1`),
  `PLAN_PROPOSAL_SCHEMA_ERROR` revisions
  `vr1a-canary-f546c3c31ccf`, `vr1a-canary-13535d6767d4`,
  `vr1a-canary-6118248a90dd`, `vr1a-canary-7da6666f2155`,
  `vr1a-canary-7670dc10af8f`, `vr1a-canary-1b423dace1b0`,
  `vr1a-canary-4d7581860c8b`, `vr1a-canary-5da9bfd5d191`, and
  `vr1a-canary-bf6742e01263` (`2/2` each),
  `TOPIC_SELECTION_ERROR` revisions `vr1a-canary-7d254cf7c5b4`,
  `vr1a-canary-987726641865`, `vr1a-canary-c2956d54be70`,
  `vr1a-canary-077b9e0a4277`, `vr1a-canary-a0906d45dafb`, and
  `vr1a-canary-e9f21b0fd703` (`2/2` each), and
  `MODEL_OUTPUT_PARSE_ERROR` `vr1a-canary-c0a39e4f8c05` (`2/2`). The
  metadata-only revisions `vr1a-canary-734ea5f6c0ac` and
  `vr1a-canary-1187f095b1fa` remain preserved and admitted no calls.
- The final canary failure was p16 Kling
  `p0b-kling-2024-v1a-bf6742e01263-canary`, retained as `FAILED` with
  `provider_calls/model_calls=2/2` and `PLAN_PROPOSAL_SCHEMA_ERROR` because
  one insight block returned six source IDs against the strict four-ID bound.
  This reached the combined recovery ceiling of `36/36`; no retry, third
  call, semantic repair, or alternate candidate execution was admitted after
  it.
- No new formal recovery revision was frozen or executed: the three-video
  canary gate did not pass and the external-call ceiling was exhausted. The
  historical manifests `measurement-manifest-v1.json` →
  `vr1a-dev-896243b5ddf9`, `measurement-manifest-v2.json` →
  `vr1a-dev-cecd6a62e6b2`, and `measurement-manifest-v3.json` →
  `vr1a-dev-10f4334c8026` remain present with six declared identities each;
  all historical run/evaluation identities, aggregates, and six pending
  rubrics per revision passed preservation checks. The v3 evaluator was
  invoked in an isolated temporary output and correctly returned
  `MEASUREMENT_STALE` because the current source snapshot differs from its
  frozen revision; no historical aggregate was overwritten. No new report or
  rubric exists for this exhausted recovery attempt.
- Final offline preservation result: `PROTECTED_PATH_CHECK=PASS`,
  `CANARY_PRESERVATION=PASS`, historical identity preservation `PASS`, and
  `FORMAL_RECOVERY_MANIFESTS=0`. No commit, push, PR, deployment, publication,
  `OWNER_ACCEPTED`, V1-B, or V1-C action was taken.
- Exact terminal state: `READY_FOR_OWNER_V1A_REVIEW — GOAL_RECOVERY_EXHAUSTED`.
  The bounded autonomous recovery budget ended without an execution-valid
  formal measurement; the Owner review boundary remains active and no
  acceptance is implied.

## Completion rule

The Goal is complete only after G5 and exactly one terminal state above is
recorded in both this task and `docs/visual-report/V1A-STATUS.md`. A commentary
update, passing targeted test, successful canary, or one rendered report is not
completion. If the Goal system continues the task across turns, resume from the
durable task/status/artifact evidence instead of restarting or asking the Owner
to republish the same scope.
