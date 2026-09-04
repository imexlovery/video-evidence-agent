# Visual Report V1.2 Design Baseline — Engineering Handoff

Document state: `DESIGN_BASELINE`  
Target implementation grade: `G2 CONTROLLED_PILOT`  
Implementation authority: `NOT_AUTHORIZED_BY_THIS_PACKAGE`  
Final specification state: `NOT_YET_OWNER_FROZEN`

## Owner boundary

The Owner accepted commit `2bce883` as the V1.1 product baseline and ended V1.1. The repository
then advanced through documentation commit `2eae354`; V1.2 design work began from that later
documentation HEAD without changing the accepted V1.1 product baseline. V1.2 requirements and
technical design are authorized. Product code, dependency changes, model runs, browser runs,
calibration, formal evaluation, default-path promotion, and deployment each require later authority.

This package is the V1.2 Design Baseline. It fixes product boundaries, semantic ownership, source
trust, bounded revision, Renderer/Observer authority, and terminal outcomes. It is not the Final
V1.2 Spec. The Final Spec may be frozen only by the Owner after a separately authorized minimal
vertical implementation, real-run calibration, and Architecture Ablation.

## Build target

Build one local Visual Editorial Agent/Harness that converts a complete V1.1 Canonical Transcript
into a source-grounded, visually reviewed, fixed-width desktop HTML report. The Harness is a fixed,
typed workflow rather than a free coding-agent loop:

`Canonical Transcript → Claim Graph → Editorial Plan → Presentation Plan → Render → Observe → Review`

The Controller may perform at most two defect-routed Revisions. At most one may be Semantic; both
may be Presentation. The run always stops with `COMPLETE`, `DEGRADED`, or `FAILED`.

## Primary outcome

The fixed Editorial Objective is:

> 让未观看原视频的读者能够独立理解视频的主要结论、论证脉络、关键依据和重要限制。

The product is intended for one named local Owner under close manual oversight. It drafts an
inspectable report; it does not publish, send, or mutate an external system.

## Non-negotiable contracts

1. The full Canonical Transcript is the only factual authority. V1.2 introduces no external
   knowledge and never edits, guesses, or corrects that transcript.
2. The accepted input is at most 50,000 Unicode characters. Oversize input fails as
   `INPUT_TOO_LARGE`; there is no truncation, hidden chunking, partial Claim Graph, or cross-chunk
   merge.
3. Semantic ownership is one-way: Claim Graph → Editorial Plan → Presentation Plan.
4. Every substantive reader-facing unit traces to a Claim and then to Canonical Transcript units.
5. Editorial owns all final reader-facing wording and semantic relationships. Presentation cannot
   create copy, conclusions, comparisons, process, sequence, or grouping meaning.
6. One Design System and a controlled Presentation Vocabulary permit meaningful layout choices
   without model-authored HTML, CSS, colors, coordinates, or a general page DSL.
7. Renderer output is deterministic for the same valid inputs. Renderer-generated numbering and
   labels are non-semantic UI chrome.
8. Browser Observation is mandatory runtime evidence for the 1080px desktop report. The Observer
   is a narrow deterministic sensor; the model cannot navigate freely or mutate the DOM.
9. Revision regenerates a typed Artifact. There is no Patch DSL and no unbounded refinement loop.
10. Any successful Semantic Revision invalidates and regenerates Presentation, Render, Browser
    Observation, and visual review.
11. Aesthetic opportunity alone is not a Defect. Defects are rule-defined, blocking or
    non-blocking problems affecting credibility, readability, or legal delivery.
12. V1.2 is a versioned path with no automatic fallback to legacy V1.0. Historical V0/V1-A
    contracts and evidence remain untouched.

## Required inputs

- one valid V1.1 Canonical Transcript and its manifest/provenance;
- existing video metadata required by the report shell;
- one run-level Provider, Model, and credential configuration;
- an optional already-supplied local Visual Asset Set.

The reference model is `GLM-5.3-Flash`. Every model-mediated role uses the same run configuration.
Role behavior differs through Prompt, input Artifact, output Schema, and necessary call parameters.

## Required retained outputs

- immutable input and configuration snapshot;
- Claim Graph and semantic-review evidence;
- Editorial Plan;
- Presentation Plan;
- deterministic validation evidence;
- rendered `report.html`;
- 1080px screenshot and minimum DOM/geometry observation;
- visual-review Defects and Revision evidence, when present;
- terminal run record and Candidate Report path.

The canonical provenance chain is:

`reader-facing content → Editorial Content Unit → Claim → Canonical Transcript Unit`

## Integration posture

V1.2 adds versioned schemas, Harness/Controller logic, Run Bundles, and run identities. It reuses the
V1.1 Canonical Transcript, current MP4/Bilibili ingest, local Web/CLI foundations, unified
OpenAI-compatible configuration, and renderer/design primitives that remain useful. The legacy
`ReportPlan` and seven Typed Blocks are implementation candidates, not compatibility contracts.

Use project-owned Python 3.12 and Pydantic with the repository's `uv` workflow. Do not introduce
LangGraph, Hypha, MCP workflow orchestration, a general multi-agent runtime, a database, accounts,
multi-tenancy, hosting, or deployment for V1.2. Maintain typed Artifact → Stage → Artifact seams so
a later framework migration remains possible if demonstrated complexity warrants it.

## Calibration-owned parameters

The following are intentionally resolved by real-run calibration without reopening the contracts
above:

- the smallest useful Presentation Vocabulary;
- deterministic report-length, component-count, and density ceilings;
- whether semantic review needs an independent model call;
- whether Critic and Reviser calls remain separate;
- minimum Observer field detail beyond screenshot, geometry, overflow, and clipping;
- stable-ID allocation/retention and the simplest sufficient Semantic Revision scope check;
- locked evaluation sample count and repeat count.

These are bounded implementation choices, not missing product decisions. Architecture Ablation
must remove any such mechanism that does not directly improve report quality, source trust, or the
finite self-repair loop.

## Construction and gate order

1. A new Owner goal authorizes only the minimal vertical implementation.
2. Historical samples calibrate evidence-owned parameters and compare candidate call topologies.
3. Architecture Ablation removes unsupported machinery.
4. The Owner reviews and freezes the Final V1.2 Spec.
5. Untuned locked samples compare legacy V1.0, V1.2 without Revision, and full V1.2 with repeated
   runs and every result in the denominator.
6. The Owner separately accepts or rejects V1.2 and separately decides whether it becomes default.

Green tests, a generated readiness report, or successful calibration do not cross an Owner gate.

## Package map

- `01-product-requirements.md`: user, outcome, scope, and success contract.
- `02-user-scenarios.md`: end-to-end and failure scenarios.
- `03-functional-spec.md`: normative behavior and Artifact contracts.
- `04-system-design.md`: components, data flow, state, and invalidation.
- `05-data-memory.md`: sources, Run Bundle, provenance, retention, and replay.
- `06-interfaces-integrations.md`: CLI/Web, model, renderer, and observer boundaries.
- `07-agent-behavior.md`: authority, grounding, review, and finite repair.
- `08-quality-security-operations.md`: hard gates, safety, reliability, and local operation.
- `09-test-acceptance.md`: tests, calibration, formal evaluation, and Owner gates.
- `10-delivery-plan.md`: authorized construction sequence.
- `11-decisions-risks.md`: decision summary, risks, and ablation register.
- `12-engineering-context.md`: current repository evidence and implementation seams.
- `decision-evidence.jsonl`: append-only Owner decision evidence.
- `coverage.json`: decision coverage of discovery areas and critical gates.
- `requirements-readiness.json`: validator-generated package assessment; it is not Owner approval.
