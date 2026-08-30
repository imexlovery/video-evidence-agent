# Video Visual Report V1-A — Delivery Plan

## Documentation-only notice

This file defines the bounded work for a later implementation session. The
current requirements phase does not execute any slice, modify product code or
dependencies, call a model, create runtime evidence, or advance into V1-B/C.

## Current-grade delivery boundary

V1-A is `G1 PROTOTYPE`. The later implementation may add one local foreground
path from an existing transcript to Topic Map, Report Plan, empty asset
manifest, and rendered HTML. It may exercise the three authorized transcripts
through one explicitly configured OpenAI-compatible text model only after the
requirements package passes its independent readiness check and the Owner
separately authorizes implementation.

The delivery is complete only when the bounded implementation, deterministic
checks, three product reports, desktop/mobile evidence, and Owner review package exist. It is
not production release, V1-A acceptance, V1-B authorization, or permission to
publish restricted fixtures.

## Deferred-by-grade promotion path

| Capability | Current boundary/workaround | Risk | Owner | Upgrade trigger | Promotion implementation/test/sign-off |
|---|---|---|---|---|---|
| MP4 and ASR input | Read existing `VideoSegment` JSONL | Pipeline is not end to end | Owner | V1-A content planning accepted | Separate V1-C design; one local MP4 reproduces the transcript contract; Owner sign-off |
| Automatic keyframes/assets | Emit no `image_caption`; use empty asset manifest | V1-A reports contain no newly selected images | Owner | Content plans are useful without visual-selection confound | Separate V1-B design and measured candidate-selection acceptance |
| OCR/frame VLM | Transcript only | Important unspoken visual facts may be absent | Owner | Repeated, source-cited transcript gap across fixtures | Smallest targeted visual-understanding experiment; Owner sign-off |
| Service, database, queue, accounts | One synchronous local run | No concurrency, tenancy, background recovery, or service reliability | Owner | Named pilot users and workload require G2 | New G2 requirements, access/recovery/support tests, explicit promotion |
| Public publishing | Local non-public research artifacts | Current fixture rights do not permit redistribution | Owner | Separately licensed source and publication decision | Rights review plus new acceptance package |

## Implementation principles

- Preserve the V0 renderer and frozen P0-B artifacts; add the smallest
  project-owned planning path around their public contracts.
- Keep Topic Mapper and Report Planner separate: one base model call each,
  sequentially, with the full transcript in both contexts; allow at most one
  identical technical retry across a run.
- Treat model output as an untrusted proposal. Pydantic validation, source
  binding, IDs, timestamps, budgets, compilation, state, and rendering remain
  deterministic.
- Fail visibly. Do not rewrite, merge, split, truncate, or synthesize semantic
  content; do not retry semantic failures, fall back to another model, or
  substitute a manual plan. The one eligible API/JSON retry is explicit and
  attempt-recorded.
- Give every run a new directory and retain successes, failures, and
  cancellations in the declared evidence denominator.
- Freeze prompts, semantic contracts, provider/model, compiler, sources, review
  cards, and product-review code before the three product runs.

## Dependency and critical path

```text
Readiness + Owner implementation authorization
  -> S0 contracts and synthetic fixtures
  -> S1 deterministic source/run spine
  -> S2 Topic Mapper proposal + binder
  -> S3 Report Planner proposal + compiler
  -> S4 end-to-end CLI + existing renderer
  -> S5 review cards, viewport capture and product-review harness
  -> S6 frozen three-video product build with bounded technical retry
  -> S7 content/visual evidence and status handoff for Owner review
```

The path is deliberately sequential because S3 consumes the canonical S2
artifact, S4 composes S1–S3, and the product set must not begin before
S0–S5 are frozen. There is no justified parallel implementation stream in this
small prototype.

## Historical post-measurement Goal recovery delivery

S0–S7 produced a working provider-free implementation but the first configured
provider measurement failed before Planner. The Owner therefore authorized
`VR-V1A-GOAL-RECOVERY-003` as one continuous delivery unit:

```text
preserve v3 failure evidence
  -> diagnose the real provider output contract
  -> smallest prompt/transport/observability repair
  -> provider-free regression
  -> one fresh canary per fixed video
  -> freeze six new formal identities
  -> execute and evaluate the complete revision once
  -> if an in-scope execution defect remains, preserve it and repeat with a new revision
  -> full regression and Owner-review handoff
```

The implementation agent continues through ordinary schema, prompt-contract,
provider-mode, reasoning/token configuration, test, CLI, compiler, trace, and
evaluator defects without another Owner checkpoint. It must stop for missing or
invalid credentials, billing/quota/access, source/security authorization,
unavailable compatible provider capability, a scope/threshold change, or the
bounded recovery ceiling. Detailed limits and exact terminal states live in
the task card and `09-test-acceptance.md`.

That delivery unit is complete at `GOAL_RECOVERY_EXHAUSTED`; its 36-call
authority is closed. Its sequential prompt candidates are retained as failed
experiment evidence and are not a template for further delivery.

## Completed canonical provider-conformance delivery

The completed implementation session ran as one continuous Goal under
`VR-V1A-PROVIDER-CONFORMANCE-004`:

```text
verify frozen commit and historical preservation
  -> restore canonical variable Topic Mapper and Planner contracts
  -> add anti-overfit provider-free tests
  -> pass targeted/full/Ruff/replay/V0/protected gates
  -> capability-qualify and pre-freeze at most two native-schema strategies
  -> execute Strategy A across all three videos exactly once
  -> if A passes 3/3, skip B; otherwise execute frozen Strategy B across all three
  -> if neither passes, provider-conformance no-go
  -> if one passes, freeze one fresh 3-video x 2-repeat formal revision
  -> execute all six once, evaluator once, full regression and documentation closeout
  -> stop for Owner review
```

The shared canonical code, both provider adapters, both strategy prompt bundles,
and all canary identities freeze before Strategy A's first transcript call.
Ordinary engineering errors are automatically repaired during the preceding
provider-free admission. After freeze, failures consume the strategy and cannot
start a prompt micro-version. This front-loads repair while keeping the
provider comparison causal and bounded.

The call ceiling is 24 new transcript-bearing calls: at most 12 across two
three-video canary sets and 12 in the single formal measurement after the first
pass. All three canaries in an admitted set run even if the first fails; this
prevents another Kling-only search loop. Formal runs likewise all remain in the
declared denominator. Credentials/billing/quota/access/network/source authority
and product-contract changes are the only Owner/external hard stops.

The task closed at `V1A_PROVIDER_CONFORMANCE_NO_GO`: both DeepSeek Responses
strategies completed their three-video sets, all six canaries failed, `8/8`
calls were retained, and no formal measurement was created. Its authority is
exhausted and must not be reused.

## Cancelled minimal strict-boundary isolation delivery

`VR-V1A-BOUNDARY-ISOLATION-005` was a documentation-only proposal. The Owner
declined the official OpenAI credential/provider path before authorization, so
the task is retained as `NEVER_EXECUTED` evidence and the four-call flow below
must not run.

```text
preserve e72503f and all historical evidence
  -> build and validate one strict provider-schema projection without changing canonical models
  -> pass provider-free request/equivalence/replay/regression gates
  -> freeze one direct strict provider/model/API tuple and four call identities
  -> synthetic Mapper call
  -> independent synthetic Planner call
  -> if both pass, one full RLinf Mapper call
  -> if mapping passes, one full RLinf Planner call and render
  -> classify the first failing boundary and stop for Owner review
```

The maximum is four generation requests. Calls 1–2 use the existing synthetic
fixture and isolate stage schemas independently. Calls 3–4 are the only possible
real-transcript calls and use only RLinf. No three-video canary, repeat, formal
measurement, evaluator, rubric, or Route B/C implementation occurs. Ordinary
engineering defects would have been repaired before Call 1; no Call 1 occurred.

## Current semantic-v2 product-prototype delivery

`VR-V1A-CONTRACT-SIMPLIFICATION-006` is the Owner-confirmed product contract.
Its future implementation runs as one continuous Goal:

```text
preserve e72503f and every historical/cancelled artifact
  -> add versioned semantic-v2 raw/canonical contracts and governance ledger
  -> implement/test Topic Resolver and non-semantic deterministic compiler
  -> prove no rewrite/merge/split/synthesis and the one-retry policy with fakes
  -> use existing DeepSeek Chat Completions JSON-object boundary only
  -> pass provider-free v2 replay, V0, full, Ruff and protected/history gates
  -> freeze one prompt/contract/compiler/provider tuple and three identities
  -> execute Kling/RLinf/Wu Yi product runs once each
  -> allow at most one identical recorded technical retry per run
  -> render each successful report and capture desktop/mobile screenshots
  -> create three content/visual rubrics and cross-video product comparison
  -> full regression and documentation closeout
  -> stop for Owner review
```

Every complete run keeps one accepted Mapper and one accepted Planner
proposal; an eligible technical anomaly may add the single recorded wire
attempt allowed for that run. The Topic Mapper proposes approximate
spans/representative evidence rather than exact segment
partition; the Planner proposes flat semantic content units rather than final
typed union blocks. Deterministic code owns identity/ref binding, compatible
type mapping and V0 validation, with every change recorded, but cannot rewrite,
merge, split, truncate, or synthesize semantic content.

Provider-free work uses `0/0` calls. The three runs use six base calls and at
most three technical retries, for a nine-call ceiling. A retry uses the
identical current-stage request and never reacts to valid semantic output.
First-attempt schema/JSON success remains diagnostic; three report contents and
their 1080 px/approximately 390 px visual results drive Owner review. No
per-video tuning, prompt micro-version, second model/provider, six-run formal,
official OpenAI, GLM/Qwen, or semantic fabrication is allowed.

## Historical v1 vertical slices

| Slice | User value | Scope | Dependencies | Verification | Definition of done |
|---|---|---|---|---|---|
| `S0 — Contract lock` | Makes later behavior explainable before provider use | Add V1-A implementation task/status, schema models, prompt constants, synthetic transcript/review fixtures, and fake adapter seam | Requirements readiness; Owner implementation authorization | Schema examples load; protected-path diff review; fake call count starts at zero | All contracts in `03`, `06`, `07`, and `09` have executable fixtures; no provider call |
| `S1 — Source and run spine` | Creates auditable, non-overwriting executions | Load manifest/segments read-only; enforce limits; create unique run; state/error/event/call trace writer | S0 | Valid/boundary/invalid source tests; duplicate run rejection; cancellation/failure persistence | Invalid input proves `provider_calls/model_calls=0/0`; `run.json` is canonical |
| `S2 — Topic Mapper` | Exposes what the full video contains and any exclusions | Full-context builder, exactly one Mapper call, strict proposal schema, binder, coverage accounting | S1 | Fake success; missing/duplicate/unknown/non-contiguous ID cases; prompt-injection transcript fixture | Canonical Topic Map binds every segment once or fails; no report/block choices |
| `S3 — Report Planner` | Converts coverage into an editorial report candidate | Full transcript + canonical map context, exactly one Planner call, strict proposal schema, topic omission accounting, source/metric/budget gates, V0 compiler | S2 | Block affordance, unknown refs, metric, budgets, topic selection, forbidden image/layout fields | Valid proposal compiles deterministically to current V0 plan plus empty asset manifest |
| `S4 — End-to-end local report` | Lets the Owner build one report from an existing transcript | Add `build-from-transcript` command and compose S1–S3 with existing renderer | S3 | Fake-adapter integration; replay; real V0 render regression; error exit/status matrix | Synthetic input reaches `RENDERED` with exactly two calls; failures produce no successful HTML claim |
| `S5 — Evaluation preparation` | Makes qualitative acceptance repeatable | Three versioned review cards, scoring schema, structure signature, aggregate/evidence command | S4 | Card source-ID validation; scorer fixture; stale-revision detection | All three cards are frozen and Owner-reviewable before real calls |
| `S6 — Development measurement` | Tests usefulness and stability across different videos | Declare six immutable run IDs; execute two repeats per fixed video using one frozen revision; score every attempt | S5; credentials; configured model; Owner-approved checkpoint | Six run manifests, twelve planned call traces, deterministic results, human rubrics, aggregate conclusion | All declared attempts remain in denominator; no prompt/model/compiler change within revision |
| `S7 — Review handoff` | Gives the Owner a truthful accept/reject package | Run targeted/full regression and diff checks; update V1-A task/status/evidence; summarize misses without retuning | S6 | Commands in `09`; protected artifact check; evidence inventory | Stop at `READY_FOR_OWNER_V1A_REVIEW`; no V1-B/C work or self-acceptance |

## Parallel work

No multi-agent or concurrent delivery is planned. One implementer owns the
bounded sequence and may batch independent read-only reviews, but must not run
the three product identities concurrently if doing so obscures call counts,
logs, or local artifact ownership.

## Shared contracts, module owners, and review boundaries

| Contract | Canonical owner | V1-A permission | Review boundary |
|---|---|---|---|
| `VideoSegment` and ingest manifest | Existing P0-B source/ingest modules | Read serialized artifacts only | Any schema/source mutation is out of scope |
| Topic/plan proposal contracts | New V1-A planning module | Create and version | Shallow allowlisted semantic-v2 parse; unknown fields are logged/discarded; model never becomes authority; historical strict schemas remain unchanged |
| Canonical Topic Map | New deterministic binder | Create | Every retained source ID/time binds exactly; uncovered/overlap diagnostics replace an exact partition requirement |
| Current `ReportPlan` and `AssetManifest` | Existing V0 visual-report module | Consume unchanged; fix only a demonstrated regression with Owner-visible evidence | Renderer contract regression blocks delivery |
| Run state and evidence | New local recorder/evaluator | Create append-oriented artifacts | Files do not advance state by their mere presence |
| P0-B evaluation/history | Frozen existing evaluation package | No changes | Any diff blocks delivery |

## Schema, API, and data migration order

There is no database, API, migration, or backfill. Add provisional V1-A schemas
before orchestration; add compiler adapters after those schemas; add the CLI
only after the composed path is tested. Existing V0 schema versions remain
unchanged. Any future V1-A schema change creates a new explicit version and a
new complete product revision rather than rewriting historical artifacts.

## Environments, fixtures, and test data

- Python `>=3.12,<3.13`, project-local uv environment, current lock file.
- Unit and integration tests use a local fake provider and synthetic Chinese
  segments. Saved replay responses make no provider/model call.
- The current product prototype uses only `p0b-kling-2024`,
  `p0b-rlinf-2026`, and `p0b-wuyi-goals` with matching manifests.
- Real transcripts may be sent to the current configured provider by Owner
  authorization; media files are never sent by V1-A.
- Review cards are created and frozen before the product runs. The V0 RLinf plan may
  inform reviewer calibration but is not machine-consumed Gold.

## Rollout, feature flags, compatibility, and rollback

There is no deployment or feature flag. V1-A is reached through a new explicit
local subcommand; existing `video-evidence` commands and the V0 `render` command
remain compatible. Rollback means reverting the V1-A source/test/docs change in
version control and leaving already-created run evidence untouched or moving it
out of the active artifact root under Owner control. Never rewrite frozen P0-B
or historical V1-A measurement evidence.

## Operational readiness

For G1, operation is limited to one foreground run owned by the local operator.
Required evidence is explicit configuration failure, bounded provider timeout,
one explicit identical technical retry with no hidden/semantic retry or
fallback, terminal run state, non-secret logs, preserved partial diagnostics,
and deterministic replay. There is no uptime, paging,
backup, disaster-recovery, or on-call commitment.

## Commercial go-live and customer lifecycle

Not applicable. V1-A has no customers, tenant identity, entitlement, usage
billing, support desk, incident SLA, offboarding workflow, or public release.
Promotion requires a separately designed G2 boundary; passing G1 cannot create
commercial commitments implicitly.

## Release definition of done

- Every `REQ-VR1A-*` requirement maps to at least one executable or human-owned
  acceptance item.
- Source, schema, failure, adversarial, replay, integration, renderer-regression,
  and protected-diff checks pass.
- Three predeclared product-run identities and every attempt/terminal state are
  retained; total provider calls do not exceed nine.
- Three canonical reports, six viewport screenshots, content/visual rubrics,
  and cross-video comparison exist, or the exact technical/contract stop is
  recorded; valid but unusable semantic output is separately labeled
  content-insufficient, without an automatic product-route No-Go claim.
- The Owner-approved thresholds are evaluated as product evidence; misses are
  reported, not semantically repaired or selectively regenerated.
- Provider/model/config/prompt/source/compiler/review-card versions, call count,
  usage, latency, and cost availability are reported honestly.
- Status stops for Owner review. V1-A acceptance and V1-B/C remain Owner-only
  decisions.

## Explicitly excluded future work

MP4/ASR orchestration, keyframe extraction or selection, `image_caption`, OCR,
VLM, RAG, Agent, LangGraph, tool loops, multi-agent runtime, database, cache,
queue, API, UI, URL input, multi-video synthesis, multiple templates, free
layout, publishing, deployment, prompt self-optimization, fine-tuning, and any
V1-B/V1-C implementation.
