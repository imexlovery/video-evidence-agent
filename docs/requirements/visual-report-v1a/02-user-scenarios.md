# Video Visual Report V1-A — User Scenarios

## Actors

- **Owner/learner:** consumes the reports, owns current product-prototype
  acceptance, and retains authority over historical measurement conclusions.
- **Implementer/operator:** invokes the local command, inspects artifacts, and
  may repair ordinary code defects inside the Goal; prompt/model/semantic
  changes require a separately authorized complete product revision.
- **Configured provider:** returns shallow semantic Topic Map and Report Plan
  proposals; it has no tool, file, renderer, or publication authority.

Scenarios `SCN-VR1A-001` through `006` below describe the implemented and
measured historical v1 contract. The current Owner-confirmed semantic-v2
product prototype is described in `SCN-VR1A-009` through `013`.

## `SCN-VR1A-001` — Successful transcript-to-report run

| Field | Contract |
|---|---|
| Trigger | Implementer explicitly runs V1-A for one authorized transcript |
| Preconditions | Manifest/segments exist and validate; explicit provider model and credential are configured; output run ID is unused |
| Producer/input | Frozen ingest manifest and ordered `VideoSegment` JSONL |
| Source flow | Validate source → assemble full transcript context → Topic Mapper proposal → deterministic accounting/binding → Report Planner proposal → deterministic grounding/budget/compiler gates |
| Output/side effect | Local Topic Map, Report Plan, empty assets manifest, `report.html`, run/call traces |
| Consumer | Owner reviews the generated structure/content; implementation/eval code reads structured artifacts |
| Success evidence | Exit 0, exactly two admitted calls, all validators pass, current renderer succeeds, artifacts name prompt/model/source versions |
| Retention/deletion | Run directory remains until Owner deletes it; source artifacts stay read-only |

## `SCN-VR1A-002` — Topic Mapper makes coverage explicit

The Mapper receives every ordered transcript segment. It emits 4–12 ordered
topics plus explicit exclusions. Deterministic validation requires each segment
to appear exactly once as a primary topic member or exclusion. Repeated themes
later in the video become a new ordered topic instance rather than a
non-contiguous hidden merge. The Mapper cannot choose report blocks or omit a
segment without naming a bounded reason.

## `SCN-VR1A-003` — Planner compresses rather than repeats

The Planner receives both the canonical Topic Map and the full transcript. It
chooses 3–5 report sections, marks every mapped topic included or intentionally
omitted, and emits 8–14 text blocks. It may reorganize topics into a clearer
narrative, but every block must cite one to four source segment IDs from that
section's selected topics. Deterministic code, not the model, generates IDs,
timestamps, kickers, metadata, and renderer fields.

## `SCN-VR1A-004` — Invalid model output fails without repair

If either model response is malformed, references an unknown segment/topic,
leaves a source segment unaccounted, emits an unsupported metric/layout field,
or violates a budget, the run becomes `FAILED`. Raw response and failure
category remain in its run directory. There is no semantic patch, block
substitution, silent truncation, third call, or automatic rerun. A deliberate
retry uses a new run ID and preserves the failure.

For current semantic-v2, a soft adaptive-budget or density miss is not a budget
violation. Only the current hard limits or an unchanged lower-level V0/field/
grounding rule causes this failure behavior.

## `SCN-VR1A-005` — Provider unavailable or timed out

The current call fails with `PROVIDER_ERROR` or `PROVIDER_TIMEOUT`. The system
does not fall back to another model, cached answer, one-call prompt, or manual
plan. No successful `report.html` is claimed. The operator may fix configuration
or retry explicitly with a new run identity.

## `SCN-VR1A-006` — Three-video Development measurement

1. Human review cards are authored from the three fixed transcripts before the
   final measured prompt version is run. They name must-cover topics, known ASR
   traps, prohibited overclaims, and source segments.
2. One prompt/model/config revision is frozen for the measurement.
3. Kling, RLinf, and Wu Yi each run twice, producing six independent run
   directories and twelve planned model calls.
4. Every failure remains in the denominator; no selective rerun replaces it.
5. Deterministic metrics and blinded-as-practical human rubric scores are
   aggregated per video and overall.
6. Results are labeled `Development measurement`; the Owner accepts, rejects,
   or requests a new prompt revision. No V1-B/C follows automatically.

## Alternate, partial, and recovery behavior

| ID | Situation | Required result | Recovery |
|---|---|---|---|
| `FAIL-VR1A-001` | Manifest/JSONL missing or invalid | Fail before any model call | Correct input; new run ID |
| `FAIL-VR1A-002` | Transcript exceeds configured context envelope | `INPUT_TOO_LARGE`; do not truncate invisibly | Select an authorized bounded fixture or separately redesign chunking |
| `FAIL-VR1A-003` | Mapper output invalid | Preserve raw response; zero Planner calls | New explicit run after correction |
| `FAIL-VR1A-004` | Planner output invalid | Preserve valid Topic Map and raw Planner response; no report success | New explicit run |
| `FAIL-VR1A-005` | Renderer fails on compiled plan | `RENDER_ERROR`; prior other runs unaffected | Fix implementation; rerun as new identity |
| `FAIL-VR1A-006` | Ctrl-C | Mark current run `CANCELLED` when manifest can be updated; never success | New explicit run |
| `FAIL-VR1A-007` | Model returns useful but incomplete content | Failure, not successful partial report | Prompt/schema correction and new run |
| `FAIL-VR1A-008` | Review finds major overclaim | Measurement fails; artifact retained | New prompt/model revision across the full measurement set |

## Duplicate, ordering, cancellation, and late-result rules

- A run ID may be created once. Existing run directories are never reused.
- Transcript ordinals must be consecutive, IDs unique, and timestamps ordered.
- Provider calls are sequential: Planner cannot start until the bound Topic Map
  passes.
- No successful partial output exists. Earlier stage artifacts are diagnostic.
- The foreground process owns cancellation; there is no worker or callback that
  can later advance a cancelled run.

## Lifecycle

- **Onboarding/configuration:** read the V1-A package; configure the explicit
  provider/model through named environment variables; never inspect secret
  values in logs.
- **Normal use:** one command, one transcript, one run directory.
- **Administration/support:** not applicable — one local Owner and no service.
- **Change/release:** prompt/schema/model changes create a new version and make
  earlier product or measurement conclusions non-current, while retaining
  their evidence; another product set requires Owner authority.
- **Offboarding/deletion:** Owner may delete V1-A run directories; frozen source
  transcripts and historical design/evidence remain protected.

## Misuse and abuse scenarios

- Transcript text that looks like instructions remains JSON data and cannot
  override system instructions.
- A model attempt to emit layout, remote assets, HTML, or unknown IDs is rejected.
- Credentials never enter prompts, artifacts, or error messages.
- The restricted source videos, frames, and rendered reports are not published
  merely because transcript processing was authorized.

## Current semantic-v2 product scenarios

### `SCN-VR1A-009` — Mapper proposes a global semantic map

The Mapper emits content-derived topics with approximate start/end IDs and
representative existing segment IDs. A deterministic Topic Resolver removes
unknown/duplicate IDs, expands valid inclusive spans, assigns canonical IDs
and timestamps, and exposes overlap/uncovered diagnostics. Exact partition and
explicit exclusions are no longer provider-facing success conditions. No
usable grounded topic still fails before Planner.

### `SCN-VR1A-010` — Planner proposes semantic content units

The Planner receives the complete transcript plus resolved Topic Map and emits
Hero content, semantic sections, flat content units, advisory block types, and
existing source IDs. Deterministic code chooses compatible current V0 block
types, binds refs, computes topic omissions, enforces budgets, and renders only
when at least three grounded usable units remain across 3–5 nonempty sections.

### `SCN-VR1A-011` — Normalization is visible and non-semantic

Known syntactic, reference, and structural mismatches may be governed without
another semantic stage. Every ordered raw-to-final event is retained in
`normalization.json`. A rule may trim whitespace, deduplicate IDs, bind refs,
map complete supplied shapes to compatible V0 blocks, or omit a whole unusable
unit. It may not rewrite, merge, split, shorten, expand, or synthesize semantic
content.

### `SCN-VR1A-012` — Three-video product prototype

One frozen DeepSeek Chat Completions JSON-object tuple runs Kling, RLinf, and
Wu Yi once each. Each successful run renders canonical HTML, then receives one
1080 px desktop and one approximately 390 px mobile browser review. The Owner
judges content, grounding, editorial usefulness, cross-video fit, and visual
usability; no six-run formal measurement follows automatically.

### `SCN-VR1A-013` — One technical retry does not decide product viability

If a run encounters an eligible API/JSON technical anomaly, its current stage
may retry exactly once with identical input/configuration. Both attempts and
the trigger are retained. Valid but weak semantic content is never retried.
Retry exhaustion yields `PROTOTYPE_EXECUTION_INCONCLUSIVE`, not a Visual Report
product-route No-Go. A successful retry remains fully eligible for content and
visual review.

### `SCN-VR1A-014` — Adaptive budget scales without becoming a template

After Topic Resolver, deterministic code uses source duration and canonical
primary-topic count to recommend report capacity. Planner may deviate when the
source calls for less or more grounded explanation. The compiler records an
undershoot/overshoot and density status but does not delete, rewrite, merge,
split, pad, or retry content to hit the recommendation. More than 32 compiled
blocks or 8,000 visible authored characters fails visibly.

### `SCN-VR1A-015` — Text gate opens the existing local Web loop

The Owner first sees three replay-validated, newly frozen reports. Only when all
three new product identities reach `RENDERED` may the existing loopback Web MVP
start. The Owner selects an allowlisted source, starts one unique run, watches
the canonical `run.json` state, and opens its report. A duplicate submit cannot
start a second paid call, credentials stay server-only, and no hosted/public
surface or V1-B/C capability appears.

### `SCN-VR1A-016` — Independent network-recovery diagnostic canary

After Task 008 stops at its external block, the operator starts a separate
Task 009 Goal with a new Kling run ID. The operator preserves the Task 008
revision, manifest, failed run, aggregate, and unstarted identities, and adds
only `NO_PROXY=api.deepseek.com` and `no_proxy=api.deepseek.com` to that one
`uv` child process. The same Topic Mapper → Report Planner → Compiler → V0
Renderer path runs once. A successful render is marked `diagnostic_only=true`
and excluded from every product or formal-measurement denominator. The run
stops immediately after success or one classified failure; it never proceeds
to RLinf, Wu Yi, Web, evaluator, rubric, tuning, or a new product revision.

| Boundary | User-visible result |
|---|---|
| Full canary renders | `READY_FOR_OWNER_V1A_REVIEW — NETWORK_RECOVERY_CANARY_PASSED` |
| Endpoint remains unreachable after the eligible retry | `READY_FOR_OWNER_V1A_REVIEW — NETWORK_RECOVERY_EXTERNAL_BLOCKED` |
| Credential, balance, permission, or model access is unavailable | `READY_FOR_OWNER_V1A_REVIEW — NETWORK_RECOVERY_CONFIGURATION_BLOCKED` |
| API/JSON technical failure remains after one eligible identical retry | `READY_FOR_OWNER_V1A_REVIEW — NETWORK_RECOVERY_RUNTIME_INCONCLUSIVE` |
| Network works but valid content cannot compile/render | `READY_FOR_OWNER_V1A_REVIEW — NETWORK_RECOVERY_CONTENT_INSUFFICIENT` |
| Further progress requires a contract/provider/model/compiler change | `READY_FOR_OWNER_V1A_REVIEW — NETWORK_RECOVERY_CONTRACT_CHANGE_REQUIRED` |
