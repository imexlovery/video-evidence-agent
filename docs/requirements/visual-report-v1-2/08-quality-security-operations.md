# Quality, Security, Reliability, and Local Operations

## Quality model

V1.2 quality has four independent dimensions:

1. **Source credibility** — every substantive unit is grounded and uncertainty is honest.
2. **Editorial usefulness** — an unseen reader can understand conclusions, reasoning, evidence, and
   limitations.
3. **Presentation readability** — the 1080px desktop report is coherent, legible, and free of
   rule-defined material visual Defects.
4. **Run stability** — hard failures, unacceptable worst cases, and cross-run variance are bounded
   without best-of-N selection.

Visual attractiveness is evaluated by the Owner during calibration/formal review, but taste alone
cannot activate the runtime Revision loop.

## Hard delivery gates

Every `COMPLETE` or `DEGRADED` run MUST pass all of these gates:

| Gate | Deterministic or reviewed evidence |
|---|---|
| valid complete input | V1.1 schema/manifest validation and character count |
| legal Claim Graph | schema, evidence closure, allowed kinds, derived source metadata |
| legal Editorial Plan | fixed Objective, Report Shell, Claim provenance, no unsupported semantics |
| completed Semantic review | review record bound to current semantic snapshot |
| legal Presentation Plan | vocabulary/ceiling/asset/content-coverage validation |
| deterministic render | canonical HTML and render version/summary |
| real desktop observation | full 1080px screenshot plus minimum DOM evidence |
| completed visual review | review record bound to current render/Observation |
| bounded control | retry and Revision invariants; no stale downstream Artifact |
| safe delivery | escaped content, valid local assets, no blocking Defect |

`DEGRADED` relaxes none of these gates. It only permits a known non-blocking omission or
presentation Defect.

## Defect rules

The implementation MUST maintain a small, testable rule set rather than an open aesthetic
taxonomy. Initial rules need only cover observable conditions required by the baseline:

- unsupported or untraceable reader-facing content;
- Presentation-owned semantic content or relationship;
- missing mandatory Report Shell content;
- missing/invalid asset reference;
- horizontal overflow at the canonical viewport;
- clipping or inaccessible content;
- unreadable density under the active deterministic ceiling;
- missing screenshot/geometry evidence;
- stale downstream Artifact after Revision;
- source attribution or required limitation not legally delivered.

Calibration may sharpen measurable boundaries and remove rules without demonstrated value. Adding
a broad style-lint taxonomy is outside this baseline.

## Security boundaries

### Credentials

- API keys stay in environment configuration.
- Keys MUST NOT appear in Prompts, request snapshots, Run Bundles, HTML, screenshots, logs, errors,
  or Web payloads.
- The run records only Provider/model labels and credential presence.
- No credential fallback or embedded development key is allowed.

### Untrusted content and prompt injection

- Transcript text, subtitles, OCR, asset metadata, and previous report text are untrusted data.
- System instructions explicitly delimit them as content and deny tool/workflow authority.
- The model has no tools or browser control, reducing the effect of embedded instructions.
- The Renderer escapes all reader content and never inserts model-authored executable HTML/CSS.
- Asset paths are resolved and validated within authorized local inputs; no remote fetch occurs.

### Filesystem

- Each run writes only to its explicit unique Run Bundle.
- Atomic writes are used for canonical Artifacts when consistent with existing primitives.
- Historical V0/V1-A evidence and other run directories are read-only to the V1.2 Controller.
- V1.2 performs no automatic deletion, publication, upload, or external file mutation.

### Browser

- The Observer opens only generated local report content.
- It exposes no navigation/click/DOM mutation to the model.
- External source links in the report are not followed during observation.

## Privacy and content rights

The local G2 product may send Canonical Transcript text, supplied images, and report screenshots to
the configured model Provider. The user-facing product must disclose this before external-provider
use. The Owner chooses the Provider and inputs and remains responsible for having permission to
process them.

V1.2 adds no rights taxonomy, policy engine, user-consent store, or hosted data-processing path.
Public release, redistribution, and comprehensive privacy/copyright policy belong to the later
productization phase.

## Reliability policy

### Model calls

- Eligible technical failures: transport error, timeout, 429, 5xx before a complete response.
- Maximum: one shared identical model retry for the entire run; after use, later calls cannot retry.
- Complete response: never retried because parsing or validation fails.
- No alternate model/provider or hidden resampling.

### Deterministic processes

Renderer and Observer may each receive one identical operation retry for a transient process-level
failure. A retry does not use stale output and does not change inputs. Continued failure ends the
run as `FAILED`.

### Revisions

- Maximum two authorized Reviser calls in total.
- Maximum one Semantic Reviser call.
- Budget is consumed at authorization.
- Every replacement is revalidated; every affected downstream Artifact is regenerated.

## Load, latency, and cost boundary

V1.2 is a single-owner local controlled pilot. It makes no RPS, concurrent-user, uptime, p95/p99,
or completion-time service promise. Existing single-process/FIFO Web behavior is sufficient.

Work per run is bounded by:

- one complete transcript of at most 50,000 Unicode characters;
- one optional supplied asset set under implementation-defined local file limits;
- fixed required capability sequence;
- at most two Revisions;
- at most one shared eligible identical model retry in the run;
- no discovery, external RAG, long-context chunk fan-out, or best-of-N generation.

The Run Bundle SHOULD record provider usage and elapsed time when available so calibration can
measure cost. Cost cannot justify bypassing source, observation, or hard-validation gates.

## Observability

Every run records enough evidence to reconstruct:

- input/configuration identity;
- capability order and Artifact versions;
- model Provider/model/Prompt/Schema versions;
- response completion, parsing, validation, and eligible retry;
- Revision authorization, layer, Defect set, and budget remaining;
- render and Observer runtime versions;
- hard-gate results;
- terminal outcome and reason.

No centralized telemetry, analytics, tracing service, or remote log sink is required. Local Run
Bundles are the audit surface.

## Failure and degraded operation

The system never serves a stale or invalid report as a successful result. It fails closed when a
mandatory Artifact, Renderer, Observer, or blocking-quality gate is unavailable. `DEGRADED` is
allowed only when the report is otherwise valid and the remaining issue is explicitly non-blocking.

Partial Artifacts and failed responses remain inspectable in the Run Bundle. Re-running after a
terminal result creates a new run identity; it does not overwrite or relabel the prior outcome.

## Local operating model

The named Owner is the pilot operator and support owner. Operation consists of:

- configure the external Provider locally;
- start the existing CLI or loopback Web surface;
- inspect terminal outcome and Run Bundle;
- manually restart with a new run identity when desired;
- retain/archive/delete local files through normal filesystem control.

There is no deployment environment, on-call rotation, automated incident workflow, SLA, customer
support, entitlement, billing, or commercial offboarding in V1.2. A move to ongoing external use
requires a new productization design rather than inheriting the G2 assumptions.

## Shutdown and recovery

The Owner may stop the local process. An interrupted run cannot be promoted to a successful terminal
report based on partial files. Retained snapshots support diagnosis and deterministic replay, but
V1.2 does not require durable checkpoint/resume; recovery is a new run identity. The existing source
and prior Run Bundle remain unchanged.
