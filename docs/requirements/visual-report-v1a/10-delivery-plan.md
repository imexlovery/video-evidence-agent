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
checks, six-run Development measurement, and Owner review package exist. It is
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
- Keep Topic Mapper and Report Planner separate: one admitted model call each,
  sequentially, with the full transcript in both contexts.
- Treat model output as an untrusted proposal. Pydantic validation, source
  binding, IDs, timestamps, budgets, compilation, state, and rendering remain
  deterministic.
- Fail visibly. Do not semantically repair, retry, fall back to another model,
  delete an invalid block, or substitute a manual plan inside a run.
- Give every run a new directory and retain successes, failures, and
  cancellations in the declared evidence denominator.
- Freeze prompts, schemas, provider/model, compiler, sources, review cards, and
  evaluation code before the six measured runs.

## Dependency and critical path

```text
Readiness + Owner implementation authorization
  -> S0 contracts and synthetic fixtures
  -> S1 deterministic source/run spine
  -> S2 Topic Mapper proposal + binder
  -> S3 Report Planner proposal + compiler
  -> S4 end-to-end CLI + existing renderer
  -> S5 evaluation cards and harness
  -> S6 frozen 3-video x 2-repeat Development measurement
  -> S7 evidence/status handoff for Owner review
```

The path is deliberately sequential because S3 consumes the canonical S2
artifact, S4 composes S1–S3, and the measured denominator must not begin before
S0–S5 are frozen. There is no justified parallel implementation stream in this
small prototype.

## Vertical slices

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
the six measurement identities concurrently if doing so obscures call counts,
logs, or local artifact ownership.

## Shared contracts, module owners, and review boundaries

| Contract | Canonical owner | V1-A permission | Review boundary |
|---|---|---|---|
| `VideoSegment` and ingest manifest | Existing P0-B source/ingest modules | Read serialized artifacts only | Any schema/source mutation is out of scope |
| Topic/plan proposal contracts | New V1-A planning module | Create and version | Strict `extra="forbid"`; model never becomes authority |
| Canonical Topic Map | New deterministic binder | Create | Exact source-ID/time accounting required |
| Current `ReportPlan` and `AssetManifest` | Existing V0 visual-report module | Consume unchanged; fix only a demonstrated regression with Owner-visible evidence | Renderer contract regression blocks delivery |
| Run state and evidence | New local recorder/evaluator | Create append-oriented artifacts | Files do not advance state by their mere presence |
| P0-B evaluation/history | Frozen existing evaluation package | No changes | Any diff blocks delivery |

## Schema, API, and data migration order

There is no database, API, migration, or backfill. Add provisional V1-A schemas
before orchestration; add compiler adapters after those schemas; add the CLI
only after the composed path is tested. Existing V0 schema versions remain
unchanged. Any future V1-A schema change creates a new explicit version and a
new measurement revision rather than rewriting historical artifacts.

## Environments, fixtures, and test data

- Python `>=3.12,<3.13`, project-local uv environment, current lock file.
- Unit and integration tests use a local fake provider and synthetic Chinese
  segments. Saved replay responses make no provider/model call.
- Real Development measurement uses only `p0b-kling-2024`,
  `p0b-rlinf-2026`, and `p0b-wuyi-goals` with matching manifests.
- Real transcripts may be sent to the current configured provider by Owner
  authorization; media files are never sent by V1-A.
- Review cards are created and frozen before measurement. The V0 RLinf plan may
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
no automatic retry/fallback, terminal run state, non-secret logs, preserved
partial diagnostics, and deterministic replay. There is no uptime, paging,
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
- Six predeclared run identities and all their terminal states are retained.
- The Owner-approved thresholds are evaluated exactly as written; misses are
  reported, not repaired or selectively rerun inside the measurement revision.
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
