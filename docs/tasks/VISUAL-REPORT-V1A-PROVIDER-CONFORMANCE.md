# Video Visual Report V1-A — Canonical Contract Restoration and Provider Conformance Goal

## Task identity

| Field | Value |
|---|---|
| Task ID | `VR-V1A-PROVIDER-CONFORMANCE-004` |
| Task status | `READY_FOR_OWNER_V1A_REVIEW — V1A_PROVIDER_CONFORMANCE_NO_GO` |
| Product stage | `V1-A — Automated Content Planning Prototype` |
| Grade | `G1 PROTOTYPE` |
| Execution mode | One continuous Goal; no routine Owner checkpoint |
| Frozen code/evidence baseline | `4ba28bf1b3288a6fb77bcc27378a45a69cd2b895` on branch `visual-report` |
| Historical terminal | `READY_FOR_OWNER_V1A_REVIEW — GOAL_RECOVERY_EXHAUSTED` |
| Maximum strategy candidates | `2` materially distinct provider/model/API strategies |
| Maximum new transcript-bearing calls | `24` provider calls and `24` model calls |
| Successful stop | `READY_FOR_OWNER_V1A_REVIEW — PENDING_OWNER_REVIEW` |
| Bounded conformance stop | `READY_FOR_OWNER_V1A_REVIEW — V1A_PROVIDER_CONFORMANCE_NO_GO` |
| Other honest stops | `READY_FOR_OWNER_V1A_REVIEW — FORMAL_MEASUREMENT_FAILED`, `READY_FOR_OWNER_V1A_REVIEW — EXTERNAL_BLOCKED`, or `READY_FOR_OWNER_V1A_REVIEW — CONTRACT_CHANGE_REQUIRED` |

## Owner authorization and interpretation

The Owner authorized this task after reviewing the exhausted recovery result.
The requested outcome is one continuous Goal that:

1. preserves the failed experiments and corrects their documentation;
2. restores the canonical V1-A Topic Mapper, Report Planner, and anti-template
   contracts;
3. evaluates at most two genuinely schema-constrained provider/model/API
   strategies without per-video tuning or prompt micro-version loops;
4. immediately runs one fresh three-video × two-repeat formal Development
   measurement if either strategy passes its complete three-video canary set;
5. otherwise records an explicit provider-conformance no-go; and
6. automatically handles ordinary in-scope engineering work without asking the
   Owner to republish intermediate task cards.

The Owner also stated that the proposed Goal wording was a draft and delegated
its refinement. This card narrows “strategy”, freezes both experiments before
the first transcript call, distinguishes provider conformance from product
quality, and prevents another sequential prompt-overfit loop.

## Goal

Starting from the frozen failed-experiment commit, produce one honest answer to
this question:

> Can an explicitly configured, natively schema-constrained provider/model/API
> strategy execute the canonical two-call V1-A contract across all three fixed
> videos without per-video repair, fixed-template drift, retry, or fallback?

If yes, use the first passing strategy unchanged for one new six-run formal
Development measurement and assemble the Owner review package. If no eligible
strategy passes, stop with preserved evidence and a provider-conformance no-go.
This task does not self-accept V1-A and does not enter V1-B/V1-C.

## Evidence labels

- The 22 prior candidate manifests, 20 failed canary runs, and `36/36` calls are
  `FAILED_EXPERIMENT` evidence. They are not a provider benchmark and must not
  be promoted as the V1-A prompt contract.
- A three-video strategy canary is `PROVIDER_CONFORMANCE_CANARY`. It is not part
  of the formal denominator and is not product-quality acceptance.
- A new six-run result is `DEVELOPMENT_MEASUREMENT`. It is not Freeze, Locked
  Eval, release, production evidence, or Owner acceptance.
- `V1A_PROVIDER_CONFORMANCE_NO_GO` means the two-strategy experiment could not
  satisfy the current provider-output boundary. It is not evidence that the
  two-stage V1-A architecture or product hypothesis is invalid.

## Source-of-truth order

1. The Owner messages authorizing this Goal and permitting the draft to be
   refined (`DEC-VR1A-053/054`)
2. `docs/requirements/visual-report-v1a/requirements-readiness.json`
3. `docs/requirements/visual-report-v1a/00-handoff.md`
4. Canonical contracts in `03-functional-spec.md`,
   `06-interfaces-integrations.md`, `07-agent-behavior.md`, and
   `09-test-acceptance.md`
5. `docs/requirements/visual-report-v1a/11-decisions-risks.md` and
   `12-engineering-context.md`
6. This task card
7. Historical task cards and immutable run/evaluation evidence

If current product code conflicts with the canonical requirements, the
requirements win. Preserve the conflicting code as Git history and correct it
in the working tree; do not reinterpret the requirement to match the failed
experiment.

## Historical preservation contract

Before editing product code, verify and then preserve:

- Git baseline `4ba28bf1b3288a6fb77bcc27378a45a69cd2b895`;
- historical formal revisions `vr1a-dev-896243b5ddf9`,
  `vr1a-dev-cecd6a62e6b2`, and `vr1a-dev-10f4334c8026`;
- all 22 `canary-candidate-*.json` manifests and all 20 admitted failed run
  directories from `VR-V1A-GOAL-RECOVERY-003`;
- every historical aggregate, report, review card, and pending rubric;
- frozen P0-B inputs/evaluation/history, source manifests/transcripts, V0
  renderer contracts, and canonical V0 visual artifacts; and
- any uncommitted documentation changes supplied with this task.

Never amend the baseline commit, reuse a historical run ID, overwrite an
aggregate, delete a failure, or move a failed attempt out of its denominator.

## G0 — Fact and baseline admission

1. Read `AGENTS.md`, `docs/visual-report/V1A-STATUS.md`, the readiness report,
   V1-A handoff/engineering context, canonical `03/06/07/09/10/11`, this card,
   and the historical recovery card.
2. Confirm branch, HEAD, worktree state, configured non-secret capability
   fields, and the historical artifact inventory. Never print or copy `.env`,
   credentials, transcript bodies, or raw restricted response content into
   chat/log commentary.
3. Confirm the historical documentation correction: the final p16 Planner
   object had both six source IDs in one block and only two sections.
4. Record a new append-only task evidence entry. Existing history remains
   immutable.

## G1 — Restore the canonical V1-A content contract

The current baseline is intentionally classified `FAILED_EXPERIMENT /
DO_NOT_PROMOTE`. Restore the following behavior before any new provider call.

### Topic Mapper

- Preserve the canonical strict proposal schema: `4–12` chronological,
  content-derived top-level topics and `0–5` content-derived subtopics.
- Every input segment enters exactly one primary topic or one explicit valid
  exclusion; substantive content cannot be excluded to hit a topic quota.
- Remove the exact-four-topic instruction, empty-subtopic requirement,
  exact-four example synthesis, and equivalent payload/test assumptions.
- Keep full-transcript context, existing-ID-only output, conservative grounding,
  and deterministic ID/time/coverage binding.

### Report Planner

- Preserve the canonical budget: `3–5` sections, `2–4` blocks per section,
  `8–14` blocks total, exactly one final `takeaway_box`, and the existing
  2,600-character visible-content ceiling.
- Select section/topic grouping and block types from source affordances. Do not
  force exact section/block counts, section distribution, topic assignment,
  block sequence, one-video content, or a fixed omission pattern.
- Restore all six permitted non-image block types and their canonical gates.
- Keep explicit selected/omitted topic accounting, 1–4 real refs per block,
  deterministic compilation, empty assets, and the current V0 renderer.

### Executable anti-overfit tests

Add or update provider-free tests that fail when prompt text, payloads, examples,
or helper code contain any operative requirement equivalent to:

- exactly four topics or always-empty subtopics;
- exactly three sections or exactly eight blocks;
- fixed `[2,3,3]` section distribution;
- fixed `topic-001`/`topic-002`/`topic-003`/`topic-004` section assignment;
- a fixed block-type sequence or disabled valid block types; or
- fixture/video-specific semantic content used to steer output.

Examples may demonstrate schema shape, but must not prescribe one report
signature. The existing canonical min/max schemas and deterministic binders
remain authoritative; do not weaken them to make a provider pass.

### Provider-free admission

Before strategy selection, pass targeted tests, full pytest, Ruff,
`git diff --check`, protected-path review, saved-response replay, and the V0
renderer regression. Ordinary code/test/serialization defects found here are
fixed automatically inside the Goal and revalidated without an Owner
checkpoint.

## G2 — Define and freeze at most two eligible strategies

### What counts as a strategy

A strategy is one immutable tuple:

```text
provider identity
+ exact model identity/version
+ exact API surface/endpoint family
+ native schema-constrained response mechanism
+ submitted structural schema hashes
+ Mapper and Planner prompt-bundle hashes
+ temperature/reasoning/token/timeout settings
+ SDK/package and adapter code snapshot
```

Changing any tuple field creates a different strategy. Changing prompt wording,
examples, token limits, schema projection, or reasoning settings after a canary
begins is not a retry of the same strategy and is prohibited by this task.

### Native schema-constrained eligibility

An eligible strategy must use a provider-documented mechanism that constrains
generation to a submitted JSON Schema or an equivalent provider-native typed
schema at the API decoding boundary for the exact selected model/API. The
submitted schema must preserve required fields, JSON types, enums/
discriminators, `additionalProperties=false`, and supported list bounds. ID
membership, chronology, grounding, cross-field budgets, and source entailment
remain deterministic application checks.

These do **not** qualify by themselves:

- `response_format={"type":"json_object"}`;
- “return JSON” instructions, examples, Markdown stripping, or parser repair;
- post-generation Pydantic validation without provider-side constrained output;
- tools/function calls that would change the current no-tools product contract;
- SDK retries, alternate-model fallback, semantic repair, or a third call.

Provider compatibility must be supported by current official documentation or
an official capability/metadata response for the exact model/API. Capability
preflight must not send a real transcript or perform an uncounted generation.

### Strategy registry and freeze

Before the first transcript-bearing call:

1. resolve Strategy A and the optional Strategy B;
2. record for each candidate its official capability evidence, exact tuple,
   eligibility result, and non-secret configuration readiness;
3. freeze all shared product code, canonical schemas/compiler, both strategy
   adapters, and both prompt bundles;
4. predeclare three unique canary IDs per eligible strategy in one versioned
   manifest; and
5. record the maximum call ledger before execution.

Both prompt bundles must implement the same canonical semantics. Any
provider-specific wording may only express transport requirements, must be
predeclared before Strategy A runs, and cannot incorporate observations from
Strategy A. Two prompt variants on the same provider/model/API mechanism do not
count as two strategies.

If only one eligible strategy is available, run it. A missing credential,
billing/quota/access, external-network permission, or provider-specific source
authorization for the only remaining strategy is `EXTERNAL_BLOCKED`, not a
conformance result. A documented capability mismatch is a strategy
`CAPABILITY_NO_GO` and consumes no transcript call.

## G3 — Strategy A cross-video canary

Execute the predeclared Kling, RLinf, and Wu Yi canary runs exactly once each,
in that order, even if an earlier run fails. This corrects the previous
Kling-only recovery bias. For every run:

- use the same frozen Strategy A tuple and full authorized transcript;
- allow at most one Mapper call and, only if it validates, one Planner call;
- set SDK retry to zero and prohibit third calls, repair, truncation, chunking,
  manual plans, or provider/model fallback; and
- retain the complete run and accurate provider/model-call count.

Strategy A passes only if all three runs:

- reach `RENDERED` on the first Mapper and Planner responses;
- report exactly `2/2` provider/model calls;
- pass strict proposal, binder, compiler, source-ref, empty-assets, and renderer
  gates; and
- do not all share one normalized section/block structure signature.

The canary is an execution/conformance gate. Do not fill human quality scores or
claim formal product quality from it.

If Strategy A passes, do not execute Strategy B. Continue immediately to G5.
If it fails, preserve all three runs and continue to the already-frozen Strategy
B when one is eligible.

## G4 — Strategy B cross-video canary, only if needed

Run Strategy B under the identical three-video/one-attempt protocol. Strategy B
must differ materially in provider/model/API schema-constrained capability, not
in video-specific prompt content. Do not tune it from Strategy A output.

If Strategy B passes, continue immediately to G5. If Strategy A and Strategy B
both fail capability admission or their complete three-video canaries, run no
formal measurement and stop at:

`READY_FOR_OWNER_V1A_REVIEW — V1A_PROVIDER_CONFORMANCE_NO_GO`

The no-go package must state each strategy tuple, capability evidence, all six
predeclared canary identities or capability-no-go reason, actual calls, failure
categories, and why no formal denominator was created.

## Freeze boundary after the first transcript call

The automatic-repair authority ends at the experiment freeze:

- before the first transcript call, ordinary in-scope engineering defects are
  fixed and revalidated automatically;
- after a strategy's first transcript call, its prompt, schema, adapter,
  model/API settings, compiler, and three-run canary set are immutable;
- a canary-discovered defect is retained as that strategy's result, not repaired
  and rerun under a micro-version; and
- only the already-predeclared materially distinct next strategy may execute.

This boundary is deliberate. It satisfies the Owner's request for automatic
engineering work while preventing another 20-run prompt-tuning loop.

## G5 — One fresh formal Development measurement

After the first 3/3 passing strategy, freeze one wholly new formal revision. Do
not reuse any historical or canary run identity. Before execution:

1. snapshot the winning strategy tuple, code, prompts, schemas, compiler,
   sources, review cards, evaluator, and exact run manifest;
2. predeclare two unique runs for each of the three fixed videos; and
3. prove the six-run manifest is complete and excluded from all earlier
   denominators.

Execute all six runs exactly once, even if one fails. Do not tune, repair,
retry, switch strategy, replace an identity, or create a second formal revision
inside this Goal. Then run the evaluator exactly once against all six declared
runs and create/retain six Owner rubrics with status `PENDING_OWNER_REVIEW`.
Never invent human scores or monetary cost.

Run full pytest, Ruff, `git diff --check`, protected-path/history checks, replay,
V0 renderer regression, and document/artifact inventory. Update this card,
`docs/visual-report/V1A-STATUS.md`, and the aggregate conclusion in the same
session.

Terminal mapping:

- All six runs are `RENDERED`, observed calls are `12/12`, evaluator
  `measurement_valid=true`, and six reports/rubrics exist:
  `READY_FOR_OWNER_V1A_REVIEW — PENDING_OWNER_REVIEW`.
- Any formal run fails/cancels, call accounting differs, aggregate is invalid,
  or required evidence is absent:
  `READY_FOR_OWNER_V1A_REVIEW — FORMAL_MEASUREMENT_FAILED`.

Human rubric thresholds in `09-test-acceptance.md` remain Owner-owned. Even a
fully rendered, measurement-valid revision is not `OWNER_ACCEPTED` until the
Owner reviews and records that decision.

## G2–G4 — Frozen native strategies and complete canary result

The pre-call freeze is recorded in
`eval/visual-report-v1a/provider-conformance-manifest.json` at revision
`vr1a-provider-0335b314c0a1`. It contains exactly two eligible strategies,
both using DeepSeek Responses `text.format.json_schema`, the same canonical
Mapper/Planner prompt bundle and submitted schema hashes, adapter hash,
temperature `0`, reasoning effort `none`, output limit `8192`, timeout `120`,
SDK retry `0`, and six unique canary identities. Strategy A is
`deepseek-v4-flash-vision-exp`; Strategy B is `deepseek-v4-flash`. Official
capability evidence is retained in the manifest for the Responses API and
model/API availability.

Strategy A executed once for all three fixed videos and retained `5/5` calls:

| Run | State | Calls | Failure category and observed boundary |
|---|---|---:|---|
| `p0b-kling-2024-v1a-candidate-a-canary` | `FAILED` | `2/2` | `MODEL_OUTPUT_PARSE_ERROR` at Planner; no render |
| `p0b-rlinf-2026-v1a-candidate-a-canary` | `FAILED` | `1/1` | `TOPIC_MAP_SCHEMA_ERROR`; 13 topics exceeded the 12-topic bound |
| `p0b-wuyi-goals-v1a-candidate-a-canary` | `FAILED` | `2/2` | `PLAN_PROPOSAL_SCHEMA_ERROR`; source list and section/block bounds failed |

Strategy B then executed once for all three fixed videos and retained `3/3`
calls:

| Run | State | Calls | Failure category and observed boundary |
|---|---|---:|---|
| `p0b-kling-2024-v1a-candidate-b-canary` | `FAILED` | `1/1` | `SEGMENT_ACCOUNTING_ERROR`; a segment was assigned more than once |
| `p0b-rlinf-2026-v1a-candidate-b-canary` | `FAILED` | `1/1` | `TOPIC_MAP_SCHEMA_ERROR`; 13 topics exceeded the 12-topic bound |
| `p0b-wuyi-goals-v1a-candidate-b-canary` | `FAILED` | `1/1` | `TOPIC_MAP_SCHEMA_ERROR`; 13 topics exceeded the 12-topic bound |

The append-only final result is
`eval/visual-report-v1a/provider-conformance-result.json`, with
`terminal_status=NO_GO`, `conclusion=V1A_PROVIDER_CONFORMANCE_NO_GO`,
`observed_provider_calls/model_calls=8/8`, and no selected strategy. The
intermediate A result remains at
`eval/visual-report-v1a/provider-conformance-result-a.json`; it is not a
formal measurement. Every run trace confirms the native Responses/schema
mechanism and SDK retry `0`; all raw responses and failed run directories are
retained locally without semantic repair or rerun.

No formal six-run Development measurement, evaluator aggregate, report, or
human rubric was created because neither complete three-video canary passed.
The exact terminal is:

`READY_FOR_OWNER_V1A_REVIEW — V1A_PROVIDER_CONFORMANCE_NO_GO`

## New-call budget

| Path | Maximum canary calls | Maximum formal calls | Maximum total |
|---|---:|---:|---:|
| Strategy A passes | `6` | `12` | `18` |
| Strategy A fails, Strategy B passes | `12` | `12` | `24` |
| Both strategies fail | `12` | `0` | `12` |

The table is a ceiling, not a target. A Mapper failure consumes one actual call
and skips Planner. Capability/metadata inspection consumes no model-generation
call. Every actual provider and model call is recorded; hidden or SDK-level
retry is prohibited.

## Allowed change envelope

The Goal may make the smallest changes needed to:

- V1-A planning/provider/runtime/evaluator code under
  `src/video_evidence_agent/visual_report/`;
- `tests/test_visual_report_planning.py` or a narrowly justified adjacent V1-A
  test file;
- V1-A non-secret configuration examples, versioned strategy/canary/formal
  manifests, review artifacts, tasks, status, and requirements evidence; and
- `pyproject.toml`/`uv.lock` only when official schema-constrained API support
  demonstrably requires an SDK change that the installed version cannot
  express. Use the existing uv workflow and add no framework.

Transport observability from the failed experiment may remain only when it is
secret-safe and compatible with the restored canonical contract.

## Prohibited changes

- weakening canonical proposal/binder/compiler/source/budget contracts;
- exact-count or fixed-signature prompts, per-video branches, fixture-specific
  semantic hints, or prompt learning from canary/formal results;
- same-strategy rerun, prompt micro-version, hidden retry, provider fallback
  inside a run, third model call, semantic repair, field coercion, block
  deletion, manual plan substitution, transcript truncation/chunking, or
  selective denominator replacement;
- changing historical manifests/runs/aggregates/rubrics or frozen P0-B/V0
  evidence;
- MP4/ASR, image/keyframe work, OCR/VLM, Agent/LangGraph/RAG, database, queue,
  service/API/UI, deployment, publishing, V1-B, or V1-C; and
- committing, pushing, opening a PR, deploying, or recording `OWNER_ACCEPTED`
  unless separately and explicitly requested.

## Hard stops requiring Owner/external action

Stop without an intermediate checkpoint only when continuing requires:

- a missing/invalid credential, billing/quota/account access, external network
  permission, or provider outage that prevents the remaining eligible strategy;
- new source/privacy/egress authority beyond the three authorized transcripts
  and selected strategy boundary;
- changing the canonical V1-A product contract, quality thresholds, two-call
  topology, fixed population, or no-retry rule; or
- any excluded V1-B/V1-C, infrastructure, publication, or production work.

Use `READY_FOR_OWNER_V1A_REVIEW — EXTERNAL_BLOCKED` for the first two classes and
`READY_FOR_OWNER_V1A_REVIEW — CONTRACT_CHANGE_REQUIRED` for the latter two.
Do not convert an external block into provider-conformance evidence.

## Required evidence ledger

Fill this table with exact evidence during the Goal. Do not pre-mark it passed.

| Evidence | Result |
|---|---|
| Baseline commit/worktree and historical preservation | `PASS` — frozen HEAD, Owner documentation, P0-B/V0 paths, historical manifests, and prior run identities were preserved |
| Canonical prompt/payload drift removed | `PASS` — content-driven ranges, optional subtopics, all six block types, and no fixed assignment/sequence remain operative |
| Anti-overfit/static contract tests | `PASS` — provider-free assertions reject fixed-count/topic-assignment/sequence payload drift and preserve shape-only examples |
| Provider-free targeted/full/Ruff/replay/V0 gates | `PASS` — targeted visual-report tests `41 passed`, full suite `69 passed`, Ruff clean, replay `0/0`, V0 renderer regression exit `0`, diff/protected-path checks clean |
| Strategy A exact tuple/capability evidence/frozen hashes | `PASS` — frozen manifest records DeepSeek Responses/json_schema, model/version, adapter, canonical prompt/schema hashes, zero retry, temperature 0, reasoning none, timeout 120, and SDK 3.3.1 |
| Strategy B exact tuple/capability evidence/frozen hashes or reason unused | `PASS` — frozen manifest records the independent `deepseek-v4-flash` native strategy with the same predeclared canonical bundle and distinct model identity |
| Canary manifest, six possible identities, run states, signatures, and calls | `PASS` — all 6 predeclared identities executed once; all 6 `FAILED`, 0 rendered; result records `8/8` provider/model calls and no signatures |
| Winning strategy or two-strategy no-go | `PASS` — `V1A_PROVIDER_CONFORMANCE_NO_GO`; neither strategy reached 3/3 render with non-identical signatures |
| Fresh formal revision/manifest and six-run inventory, when gated | `NOT_CREATED` — correct because no strategy passed the complete canary gate |
| Evaluator aggregate, reports, and pending rubrics, when gated | `NOT_CREATED` — correct because no formal denominator was authorized |
| Full regression/diff/protected/history checks | `PASS` — post-run full tests `69 passed`, Ruff clean, replay `0/0`, V0 renderer exit `0`, `git diff --check`, protected paths, and historical identities clean |
| Final exact terminal state | `PASS` — `READY_FOR_OWNER_V1A_REVIEW — V1A_PROVIDER_CONFORMANCE_NO_GO` |

### 2026-08-30 — G0 baseline admission and root-cause classification

- Goal `01a05229-fefa-7250-b60b-e2c22e2581b1` remains active. The checkout is
  on branch `visual-report` at the frozen HEAD
  `4ba28bf1b3288a6fb77bcc27378a45a69cd2b895`.
- The only pre-existing worktree changes are the Owner's V1-A requirements,
  readiness/decision evidence, status, historical recovery card, and the new
  provider-conformance card. No product source, dependency, P0-B source/eval,
  transcript, or V0 artifact path has a diff; the untracked provider-
  conformance card is preserved.
- Historical inventory is intact: `measurement-manifest.json`, `-v1`, `-v2`,
  and `-v3`; the three historical formal revisions; 22
  `canary-candidate-*.json` manifests; 20 admitted canary directories; and
  the existing evaluation directories, aggregates, reports, and pending
  rubrics. The active historical v3 manifest still declares six runs and the
  old `12/12` planned-call denominator.
- The safe environment snapshot reports `admission=READY`, provider label
  `https://api.deepseek.com`, model `deepseek-v4-flash-vision-exp`,
  `credential_present=true`, timeout `120`, temperature `0`,
  `response_mode=json_object`, `thinking_mode=disabled`, output limit `8192`,
  SDK retry `0`, and SDK `3.3.1`. No credential value was read into evidence.
- The v3 run inventory remains one `PROVIDER_ERROR` Mapper admission and five
  `TOPIC_MAP_SCHEMA_ERROR` Mapper admissions, each `1/1`, with no Planner call
  or rendered report. Structural summaries of the five retained Mapper
  responses show missing `schema_version`, integer/renamed segment fields,
  string topics, and `description` without the required summary/source IDs.
- The final p16 Kling run
  `p0b-kling-2024-v1a-bf6742e01263-canary` remains `FAILED` at `2/2`. Its
  retained `run.json` records two strict Planner validation errors: one block
  had six source IDs against the four-ID bound and the proposal's `sections`
  validation produced `too_short`. The raw artifact currently has three
  top-level section entries with block counts `[2, 3, 3]`; this does not alter
  the recorded strict-validation failure or permit any historical rewrite.
- Root cause is separated: transport/provider failures are not V1-A quality
  evidence; the strict validator and deterministic compiler are not weakened;
  the frozen implementation's operative prompt/payload behavior is the
  noncanonical drift (exact four topics, empty subtopics, exact 3/8 structure,
  fixed topic assignment/sequence, and disabled valid block types); and the
  active adapter is JSON-object-only rather than native schema-constrained.
- G0 is complete without a transcript-bearing call. The next gate is to remove
  the canonical drift, add executable anti-overfit checks, and prove the
  provider-free/native-schema strategy admission surface before freezing any
  canary identity.

| G0 evidence | Result |
|---|---|
| Baseline commit/worktree and historical preservation | `PASS` — frozen HEAD/branch match; Owner documentation work and all historical identities/artifacts preserved |
| Configured non-secret capability fields | `PASS` — safe snapshot is `READY`; old response mode is recorded as non-qualifying for this Goal |
| Historical v3 failure inventory | `PASS` — `1` provider failure, `5` Mapper schema failures, `6/6` observed calls, no Planner/render |
| Historical p16 documentation/structure check | `PASS` — retained strict error includes six source IDs and `sections too_short`; raw artifact is retained unchanged |
| Transcript-bearing calls in G0 | `0` |

### 2026-08-30 — G1 canonical restoration and provider-free admission

- The operative Topic Mapper contract now uses content-derived `4–12` topics,
  content-derived `0–5` subtopics, full transcript coverage, and optional
  subtopics; its shape example uses placeholders and does not synthesize a
  four-topic answer.
- The operative Report Planner contract now uses the canonical `3–5`, `2–4`,
  and `8–14` ranges, all six non-image block types, source affordances, and
  selected/omitted topic accounting. Fixed `[2,3,3]` distribution, topic
  assignment, block sequence, and fixture-steering fields are absent.
- Provider-free tests explicitly reject the prior fixed structure and verify
  the native Responses request shape. No semantic schema, binder, compiler,
  empty-assets, or renderer gate was weakened.
- Provider-free admission passed: targeted visual-report tests `41 passed`,
  full suite `69 passed`, Ruff clean, `git diff --check` clean, saved-response
  replay recorded `provider_calls/model_calls=0/0`, V0 renderer regression
  rendered the unchanged V0 input into `/private/tmp`, and protected
  P0-B/historical/V0 paths had no diff.
- No transcript-bearing provider/model call has occurred. The next gate is one
  append-only conformance manifest containing both native strategy tuples,
  official capability evidence, schemas/prompts/adapter hashes, and all
  eligible canary IDs before any real transcript egress.

## Completion rule

This Goal is complete only when exactly one terminal state defined above is
recorded in this card and `docs/visual-report/V1A-STATUS.md`, with all admitted
calls and immutable identities accounted for. Passing local tests, one provider
response, one rendered report, or a 3/3 canary is not by itself completion.
Resume from durable evidence across automatic Goal turns; do not ask the Owner
to restate the same task or create another task card for ordinary engineering
errors.
