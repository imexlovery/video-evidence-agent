# Functional Specification

Normative terms `MUST`, `MUST NOT`, `SHOULD`, and `MAY` apply to the V1.2 runtime. Exact Pydantic
field spelling may be refined during the authorized implementation, but the semantic ownership and
validation rules in this document cannot change without Owner approval.

## FS-1 — Start and input validation

1. A V1.2 run MUST have a unique versioned run identity and its own Run Bundle.
2. It MUST consume one complete V1.1 Canonical Transcript plus its manifest and video metadata.
3. It MAY consume one already-supplied local Visual Asset Set.
4. It MUST snapshot inputs and the non-secret run configuration before the first model call.
5. It MUST reject a Canonical Transcript over 50,000 Unicode characters as `INPUT_TOO_LARGE`.
6. It MUST NOT truncate, chunk, summarize, partially map, or merge an oversized input.
7. It MUST validate Canonical Transcript structure and evidence-unit identity before model use.
8. It MUST treat transcript text as untrusted data, never as Harness or tool instructions.

## FS-2 — Single run-level model configuration

1. Every model-mediated capability MUST share one Provider, Model, and credential configuration for
   the run.
2. The reference model is `GLM-5.3-Flash` through the project-owned OpenAI-compatible adapter.
3. A role MAY vary only its Prompt, explicit input Artifact, output Schema, and necessary call
   parameters.
4. A stage MUST NOT bind directly to a provider SDK.
5. V1.2 MUST NOT implement role-specific model variables, routing, alternate-model fallback, or
   alternate-provider fallback.
6. Model request evidence MUST omit the credential value.

## FS-3 — Claim Graph

The Claim Graph is the only source-facing semantic abstraction introduced by V1.2. Each Claim MUST
contain exactly the following domain information:

| Field | Contract |
|---|---|
| `claim_id` | Stable, non-empty identity unique within the Claim Graph |
| `claim_text` | One atomic proposition; not a section title or bundle of unrelated assertions |
| `claim_kind` | `STATED` or `SYNTHESIS` |
| `evidence_unit_ids` | One or more valid Canonical Transcript unit IDs |

Time ranges, V1.1 source status, and `SourceRef` MUST be derived deterministically from the referenced
Canonical Transcript units. The Claim model MUST NOT contain confidence, importance, external
knowledge, or a general relationship taxonomy.

`STATED` means the proposition is directly expressed by the cited source units. `SYNTHESIS` means it
is a conservative conclusion supported collectively by all cited units. A `SYNTHESIS` MUST NOT
introduce a fact that requires knowledge outside the Canonical Transcript.

Deterministic Claim validation MUST verify:

- unique non-empty IDs;
- atomic non-empty text;
- allowed Claim kind;
- existing evidence-unit IDs from the same input snapshot;
- non-empty evidence for every Claim;
- no key Claim supported only by evidence whose V1.1 state is `UNRESOLVED`.

Semantic validation/review MUST assess source entailment, atomicity, material omissions, and whether
a `SYNTHESIS` stays inside the evidence. The Design Baseline requires the capability but does not
force it to be a permanently separate model call.

## FS-4 — Editorial Plan

The Editorial Plan is the authority for all substantive reader-facing meaning. It MUST encode:

- the fixed Editorial Objective version;
- Hero title and core overview as final reader-facing content;
- an ordered, content-adaptive set of chapters;
- each chapter's final heading and ordered Editorial Content Units;
- Sources and Limitations content required by the report;
- Claim references for every substantive Editorial Content Unit;
- comparison, process, sequence, or grouping relationships whenever that structure carries meaning.

Each Editorial Content Unit MUST be individually identifiable, contain final reader-facing semantic
content, and reference one or more Claims. The exact identifier allocation and retained-ID behavior
across Semantic Revision are implementation/calibration mechanics. They MUST still support the
provenance and Revision checks required by this specification.

The Editorial Plan MAY choose chapter count, chapter responsibility, depth, focus, and content
density according to the source. It MUST NOT select visual components. It MUST NOT require every
report to contain metrics, comparison, process, image, or takeaway content.

The stable Report Shell consists only of:

1. Hero and core overview;
2. ordered adaptive body;
3. Sources;
4. Limitations.

## FS-5 — Provenance

For every substantive reader-facing text unit, the following chain MUST resolve within one Run
Bundle:

`rendered content → Editorial Content Unit → Claim → Canonical Transcript Unit`

Deterministic provenance validation MUST fail a Plan that has a missing reference, a cross-run
reference, an empty Claim binding, or reader-facing semantic text not owned by Editorial.

Renderer/Design System MAY generate non-semantic UI chrome, including ordinal numbering, source
labels, time labels, and step labels. Such chrome MUST be deterministic and MUST NOT assert new facts.

## FS-6 — Source uncertainty

V1.2 MUST reuse V1.1 source states rather than create a confidence score or uncertainty taxonomy.

- Uncertain nonessential information SHOULD be omitted.
- Critical information MAY be conservatively summarized only when the cited evidence safely
  supports that wording; a short uncertainty notice MUST be included when needed.
- `UNRESOLVED` evidence MUST NOT independently support a key conclusion.
- If source uncertainty prevents a reliable core report, the run MUST be `FAILED`.
- A credible report with a local non-blocking omission MAY be `DEGRADED`.
- No Semantic Revision may edit or reinterpret the Canonical Transcript as corrected source text.

## FS-7 — Presentation Plan

The Presentation Plan MUST reference one exact Editorial Plan snapshot and decide only how its
existing content is shown. It MUST contain sufficient typed information for:

- Report Shell placement and ordered content placement;
- legal component selection from the controlled Presentation Vocabulary;
- visual hierarchy, density, emphasis, and spatial grouping;
- optional supplied-asset binding and image weight;
- deterministic rendering and post-render element tracing.

It MUST NOT contain fields that introduce new reader-facing semantic copy, conclusions, or
relationships. It MUST NOT change Editorial wording, omit an Editorial Content Unit designated for
delivery, or invent image-derived claims. Reader-visible captions and meaning-bearing alt text MUST
be owned by Editorial. Only non-semantic asset labels may be derived deterministically from
validated asset metadata.

The model MUST NOT emit HTML, CSS, colors, coordinates, SVG paths, arbitrary grids, or a general
page DSL. V1.2 has one Design System and no named Presentation Profiles. The Presentation
Vocabulary and deterministic safety ceilings are calibration-owned Final Spec parameters.

## FS-8 — Visual assets

The Visual Asset Set is optional. Each supplied asset MUST have a stable asset ID, readable local
path, declared media type, source context, and available semantic description or Editorial binding.
The implementation MUST validate file existence and supported format before planning.

V1.2 MAY select, place, and weight supplied assets. It MUST NOT discover assets, extract frames,
search a video with a VLM, perform full-video visual understanding, call image search, or generate
images. An empty asset set MUST leave the full report path operational.

## FS-9 — Deterministic validation and rendering

Before rendering, deterministic code MUST validate:

- Artifact schema and version;
- ownership boundaries and provenance closure;
- all referenced Claim, content, and asset identities;
- controlled vocabulary membership;
- safety ceilings active for the implementation revision;
- Report Shell completeness;
- absence of model-authored executable page content.

The Renderer MUST produce the same HTML bytes for the same validated Artifact snapshots, renderer
version, and local assets. It MUST escape reader content and resolve only validated local assets. It
MUST NOT make editorial or presentation choices.

`report.html` is the Canonical Report. It uses the fixed-width 1080px desktop design surface and
natural document height. Mobile output MAY remain usable but is not a V1.2 completion gate.

## FS-10 — Browser Observation

Every deliverable run MUST load the actual `report.html` in the configured local browser runtime at
the 1080px desktop viewport. The narrow deterministic Browser Observer MUST capture at least:

- one full-page rendered screenshot;
- viewport and page dimensions;
- basic geometry for traceable report sections/components;
- horizontal and vertical overflow signals;
- clipping signals for observed elements;
- observation success/failure and runtime version metadata.

The Observer MUST NOT browse external pages, follow links, mutate the DOM, repair the report, or
make subjective judgments. The Visual review capability consumes its evidence. A missing mandatory
desktop observation makes delivery `FAILED` after the allowed technical retry is exhausted.

## FS-11 — Defects and visual review

A Defect MUST identify:

- the violated rule;
- `BLOCKING` or `NON_BLOCKING`;
- the affected semantic or presentation references;
- observed evidence;
- the recommended defect layer: Semantic or Presentation.

A Defect exists only when the problem affects source credibility, readability, or legal delivery.
Pure aesthetic opportunity is not a Defect, consumes no Revision Budget, and cannot prevent
`COMPLETE`.

Visual review MUST inspect the real screenshot and Browser Observation. It has no Semantic write
authority and cannot directly edit any Artifact.

## FS-12 — Revision control

The Controller owns one run-wide Revision Budget:

- maximum authorized Revisions: 2;
- maximum Semantic Revisions: 1;
- maximum Presentation Revisions: 2;
- one Revision may address a related Defect set in one layer;
- Semantic and Presentation changes cannot be mixed in one Revision.

A Revision unit is consumed when the Controller authorizes the Reviser call, before its result is
known. An invalid, ungrounded, or authority-violating Reviser result still consumes that unit.

### Presentation Revision

The Reviser receives the current Editorial Plan, current Presentation Plan, and related
Presentation Defects. It emits a complete replacement Presentation Plan. A valid replacement MUST
be rendered, observed, and visually reviewed again.

### Semantic Revision

The Reviser may modify existing Claims or Editorial Content and may add omitted content. Every new
Claim or content unit MUST bind explicit supporting Canonical Transcript evidence. The replacement
MUST pass Semantic schema, grounding, provenance, and authority validation/review.

A successful Semantic Revision invalidates the old Presentation Plan, render, Browser Observation,
and visual review. All MUST be regenerated. The implementation MUST use the smallest sufficient
scope guard, but the Design Baseline forbids a complex Patch language, semantic diff framework, or
invalidation framework.

### Visual-to-Semantic escalation

Presentation Revision is the default response to a visual Defect. Visual review MAY recommend
Semantic escalation only when content length, selection, redundancy, or another Editorial root cause
cannot be reasonably solved within Presentation authority. The Controller alone authorizes it and
only when budget and the one-Semantic limit permit.

## FS-13 — Technical retry

At most one run-wide identical model retry is allowed. It may be spent on a logical model call only
when no complete response was received because of transport failure, timeout, 429, or 5xx. The
retry MUST use the same input, Prompt, Schema, model, provider, and relevant parameters. Once used,
no later model call may retry.

Once a complete model response exists, it is the result even if JSON, Schema, grounding, provenance,
or authority validation fails. V1.2 MUST NOT perform hidden resampling. Technical retry is not a
Revision and does not restore a spent Revision unit.

Deterministic Renderer/Observer process failures MAY receive one identical operation retry. They
MUST NOT trigger model fallback or silent use of stale output.

## FS-14 — Terminal outcomes

Only these report-generation terminal outcomes are legal:

### `COMPLETE`

- all mandatory capabilities ran successfully;
- source, schema, provenance, authority, Renderer, and DOM hard gates pass;
- the full 1080px Browser Observation exists;
- no unresolved material rule-defined Defect remains.

### `DEGRADED`

- a valid, source-grounded, readable Candidate Report exists;
- all hard gates pass;
- a known non-blocking local source omission or presentation Defect remains after bounded repair.

### `FAILED`

At least one of the following is true:

- input is oversized or structurally invalid;
- an initial mandatory Artifact cannot become valid;
- no valid grounded report exists;
- mandatory Renderer or Observer work remains unavailable after technical retry;
- a blocking Defect remains when no legal Revision can resolve it.

`DEGRADED` MUST NOT be used to bypass a hard gate. Run status is not Owner acceptance.

## FS-15 — Capability sequence without fixed call topology

The Harness MUST execute these capability boundaries in order:

1. input/configuration snapshot and validation;
2. Claim Graph and Editorial production;
3. explicit Semantic validation/review;
4. Presentation planning and deterministic validation;
5. deterministic Render and Browser Observation;
6. visual review;
7. defect-routed bounded Revision and revalidation, when authorized;
8. terminal classification and Run Bundle closure.

The implementation MAY combine or separate model calls inside those boundaries during calibration.
It MUST NOT let the model add stages, select arbitrary tools, browse freely, or decide to continue
without Controller authorization.

## FS-16 — Minimum failure reasons

Failure reasons are diagnostics, not a new state taxonomy. The implementation MUST distinguish at
least: invalid input, `INPUT_TOO_LARGE`, missing model configuration, model technical exhaustion,
invalid Semantic Artifact, invalid Presentation Artifact, render failure, observation failure, and
unresolved blocking Defect. Raw secrets and full provider payloads containing credentials MUST NOT
appear in user-visible errors.
