# Visual Report V1 — Roadmap

Updated: 2026-09-04

The roadmap preserves separately testable quality layers, but V1.2 now designs
their Agent coordination and shared contracts end to end. Internal construction
slices are sequencing boundaries, not separate architecture designs.

## V1.0 — Runnable Alpha baseline

Status: `IMPLEMENTED / QUALITY_NOT_ACCEPTED`

V1.0 is the current local MP4 and Bilibili URL product path. It includes ASR,
45–60 second `VideoSegment` projection, semantic-v2 planning, the deterministic
renderer, loopback Web use, and the single-process FIFO queue.

The historical implementation name `V1-A` remains in schemas, commands, task
IDs, tests, paths, and retained evidence. No compatibility rename is planned.

## V1.1 — Transcript Foundation

Status: `V1.1_FROZEN`

Objective: build one general, traceable transcript layer from ASR, text subtitle
tracks, and burned-in subtitle OCR, then project it back into the current V1.0
`VideoSegment` contract.

Key boundaries:

- reliable explicit-ROI subtitle OCR first;
- Auto ROI best-effort only;
- sparse sampling, visual-change filtering, perceptual deduplication, and
  temporal subtitle merging;
- high-confidence, local, source-backed fusion only;
- ambiguous or sentence-level conflict keeps provisional ASR and is marked
  `UNRESOLVED`;
- original ASR/OCR/subtitle content is never overwritten;
- current semantic-v2 prompts/planning and renderer remain unchanged;
- no VLM, keyframes, full-scene OCR, RAG, Agent, database, multi-tenancy, or
  deployment.

Execution card:
[`docs/tasks/VISUAL-REPORT-V1-1-TRANSCRIPT-FOUNDATION.md`](../tasks/VISUAL-REPORT-V1-1-TRANSCRIPT-FOUNDATION.md).

The Owner authorized the continuous construction Goal on 2026-09-01. A/B/C were
implemented and locally validated. Their completion did not automatically
promote the project to V1.2.

The full-video coverage correction completed local OCR and Fusion for one
1,566,677 ms real video at `coverage_ratio=1.0`. The regenerated Canonical
Transcript then passed through fresh, non-replay Fused and ASR-only semantic-v2
calls plus the deterministic renderer. Both reached `RENDERED`, returning V1.1
to Owner Review without implying acceptance or promotion to V1.2.

That content review found a remaining general Fusion gap: reliable repeated OCR
was still discarded by strict single-span handling or attached to the wrong
neighboring ASR Unit. V1.1 is therefore back in `CHANGES_REQUESTED`. Its final
bounded repair is limited to frame-candidate consensus, ±1 neighboring Unit
matching, conservative 1–8 character replace-only Fusion, and one complete
fresh-video rerun. Passing that repair makes V1.1 eligible for Owner freeze
review; it does not authorize V1.2.

That bounded repair is now the completed `V1.1 Fusion` construction baseline.
The next task must build directly on that existing commit/worktree and must not
reimplement or loosen Fusion. Owner review chose not to freeze V1.1 yet because
upstream ASR and OCR errors remain visible. One last bounded model refresh was
construction-ready: Large V3 Turbo ASR plus PP-OCRv6 Small detection and
recognition, followed by a complete fresh-video ASR-only/Fused comparison.
Fresh Semantic-v2 uses the already configured Zhipu GLM endpoint and
`glm-5.3-flash`; it does not return to the historical DeepSeek provider.
Limited or mixed quality gain is a valid measured result and ends the task
rather than triggering another transcript subsystem redesign.

Model-refresh execution card:
[`docs/tasks/VISUAL-REPORT-V1-1-MODEL-UPGRADE.md`](../tasks/VISUAL-REPORT-V1-1-MODEL-UPGRADE.md).

The authorized model-refresh execution completed. The final Small/Large
fresh run reached full-video OCR coverage and generated new ASR-only/Fused
Semantic-v2 reports with the unchanged Zhipu GLM path. The measured result is
mixed: selected Large V3 Turbo ASR terms improve, while unchanged Fusion
accepts fewer OCR replacements than Task 013. That construction run stopped at
`READY_FOR_OWNER_V1.1_MODEL_REVIEW`.

On 2026-09-04, the Owner accepted HEAD `2bce883` as the V1.1 baseline and ended
V1.1. The mixed source-model outcome and residual recognition errors remain
documented limitations rather than triggers for more V1.1 tuning. This decision
freezes the V1.1 input contract and separately authorizes V1.2 requirements and
technical design; it does not authorize V1.2 product implementation.

## V1.2 — Visual Editorial Agent / Harness

Status: `DESIGN_BASELINE_COMPLETE / IMPLEMENTATION_NOT_AUTHORIZED`

The V1.2 Design Baseline defines one source-grounded, end-to-end Harness that transforms the
frozen V1.1 Canonical Transcript into a visually reviewed report while keeping
each quality layer independently observable. The shared workflow comprises:

1. Canonical Transcript to Claim Graph;
2. Claim Graph to Editorial Plan;
3. explicit semantic validation/review and optional bounded Semantic Revision;
4. Editorial Plan to Presentation Plan;
5. deterministic rendering;
6. runtime Browser/DOM Screenshot Observation;
7. typed presentation Defect detection and optional Presentation Revision; and
8. final validation plus complete run-artifact retention.

The run has one defect-routed Revision Budget of at most two revision attempts.
No more than one may be a Semantic Revision; both may instead be
Presentation Revisions. Budget exhaustion must terminate as `COMPLETE`,
`DEGRADED`, or `FAILED`, never as an open-ended optimization loop.

Terminal outcomes use only a blocking/non-blocking distinction, not a severity
taxonomy. `COMPLETE` requires every mandatory stage, including the full 1080px
Browser Observation, plus all source-grounding, Schema, authority, Renderer,
and DOM hard gates; no rule-defined material Defect may remain. `DEGRADED`
requires a valid, source-grounded, readable Candidate Report and passing hard
gates, but permits a known non-blocking source omission or Presentation Defect
to remain after the Revision Budget ends. `FAILED` covers an input such as
`INPUT_TOO_LARGE`, inability to produce a valid grounded report, mandatory
Renderer or Browser Observer failure after technical retry, or any unresolved
blocking Defect. Pure aesthetic opportunity is not a Defect and neither
triggers Revision nor prevents `COMPLETE`.

The first design keeps these mechanisms deliberately small. Each Claim contains
only a stable ID, one atomic `STATED` or source-supported `SYNTHESIS` statement,
and Canonical Transcript evidence-unit IDs; time, source status, and `SourceRef`
are derived deterministically. It is not a general relationship taxonomy and
may not introduce external knowledge. Semantic ownership is one-way from Claim
Graph to Editorial Plan to Presentation Plan. Editorial owns final wording,
chapter order, and semantic comparison, process, sequence, and grouping.
Presentation owns only legal visual expression and cannot add semantic copy,
conclusions, or relationships. Every substantive rendered unit traces through
an Editorial Content Unit and Claim to Canonical Transcript units. The
specification requires only the bounded counters needed by the Controller, not
a standalone revision-accounting object.

The Harness invokes one model through fixed stages and explicit Artifact
Snapshots rather than a free ReAct/browser/tool loop. Claim Builder, Critic,
and Reviser are execution roles, not mandatory long-lived components or
first-class product states; the pre-freeze ablation may merge or remove roles
whose measured contribution does not justify a separate call.

The Design Baseline freezes capabilities rather than an immutable model-call
topology. Semantic output must receive explicit semantic validation/review;
Presentation must be rendered and observed; the real rendered result must
receive visual review; and every Revision must revalidate the affected result.
The Controller owns bounded revision and termination. Whether Semantic Critic
is a separate call, or Critic and Reviser are split calls, is resolved only by
minimal-vertical-loop calibration and Architecture Ablation. Revision review
is mandatory, but need not be implemented as a standalone Critic call.

V1.2 is a single-model architecture. Claim construction, Editorial planning,
Semantic Critic/Reviser, Presentation planning, and Visual Critic/Reviser all
use one run-level Provider, model, and credential configuration. The current
reference model is `GLM-5.3-Flash`. Roles differ only through Prompt, input
Artifact, output Schema, and necessary call parameters. V1.2 defines no
`semantic_model`, `presentation_model`, or `visual_model` configuration, model
routing, or fallback. A unified ModelClient/Provider Adapter prevents stages
from binding directly to a provider SDK. A role-level override is a future
capability that requires evaluation evidence of a material role-specific need.

The V1.2 implementation base remains a project-owned Python/Pydantic Harness.
It does not introduce LangGraph, Hypha, MCP workflow, or a general multi-Agent
runtime. Every stage keeps a typed Artifact-to-Stage-to-Artifact boundary so
later evidence can justify migration without changing the product model;
frameworkless is not a permanent product principle.

V1.2 uses a parallel versioned path for its schemas, Harness/orchestrator, Run
Bundle, and run identity. It continues to share the Canonical Transcript,
ingest, Web/CLI infrastructure, and reusable renderer/design primitives instead
of cloning the whole product. It does not mutate historical V0/V1-A contracts
or frozen evidence, and neither V1.2 nor the legacy path automatically falls
back to the other. Switching the default path remains a separate Owner decision
after same-source comparison and repeated-run evaluation.

V1.2 may consume an optional supplied local Visual Asset Set. Presentation may
choose whether to use an asset, where to bind it, and its visual weight, but
V1.2 does not discover, extract, search for, or generate images. The text-only
path remains complete. Browser Observation is produced by a narrow
deterministic local-page sensor; the model cannot freely navigate or mutate the
DOM. Required viewport gates follow the product surfaces explicitly committed
by the final V1.2 specification.

V1.2 formally supports only the fixed-width 1080px desktop Canonical Report as
a visual quality surface. Mobile remains best-effort and does not participate
in `COMPLETE`; the Web Shell remains only the run, status, and report-opening
surface. Runtime generation uses one versioned fixed Editorial Objective: a
reader who did not watch the video should independently understand its main
conclusions, reasoning, key support, and important limitations. V1.2 has no
Editorial Brief or audience, depth, content, or style customization input.

Source uncertainty consumes the existing V1.1 resolution and flags without a
new confidence or uncertainty system. Nonessential uncertainty is omitted;
essential content may be stated cautiously when safe; one unresolved source
cannot independently support a key reader-facing conclusion. A report whose
core conclusion cannot be supported fails, and no Semantic Revision may change or
guess the Canonical Transcript.

V1.2 processes one complete Canonical Transcript within the existing 50,000
Unicode-character semantic envelope. Oversize input fails as `INPUT_TOO_LARGE`
before a model call. The Harness does not truncate, hide chunking, generate
partial Claim Graphs, or merge chunks.

Every report retains a small stable Report Shell: Hero and core overview, an
ordered body, and Sources and Limitations. The Editorial body is otherwise
content-adaptive: Editorial chooses chapter count, responsibilities, depth, and
density; Presentation chooses legal components. There are no fixed component
quotas or mandatory metric, comparison, process, or takeaway blocks. Only
small deterministic safety ceilings remain, with exact values frozen during
implementation evaluation and ablation rather than derived through a complex
dynamic-budget algorithm.

The legacy `ReportPlan` and its seven Typed Block types are not compatibility
contracts for V1.2. Existing component implementations may be selected as
candidate Presentation Vocabulary primitives, but V1.2 may merge, remove, or
add components as needed. Editorial does not choose visual block types;
Presentation independently selects a controlled expression for unchanged
Editorial content. Arbitrary HTML/CSS, coordinates, and a general page DSL
remain prohibited. The final Vocabulary and its small safety ceilings are
resolved through implementation evaluation and the pre-freeze ablation.

The configured multimodal model may read supplied Visual Assets and Renderer
screenshots as ordinary model inputs. V1.2 adds no rights taxonomy, asset
permission subsystem, or special local/external decision path. When an external
Provider is configured, the product boundary must disclose that text, images,
and report screenshots may be sent to it. Hosted publication and public URL
ingest boundaries remain separate V1.3 productization decisions.

V1.2 defines no named Presentation Profile. Presentation selects components,
density, hierarchy, emphasis, image weight, and spatial grouping directly from
the controlled vocabulary. Only repeated, valuable strategies demonstrated by
later evaluation may become profiles.

Visual Critic may report that a presentation symptom has an Editorial root
cause, but it cannot edit Editorial artifacts. Presentation repair remains the
default. If that layer cannot reasonably fix content length, selection, or
redundancy, the Controller may spend the remaining budget on the one permitted
Semantic Revision. A successful Semantic Revision invalidates the old Presentation
Plan and requires fresh Presentation, render, and observation artifacts. The
global two-Revision ceiling prevents an open cross-layer loop.

One Revision may address multiple related Defects, but only within one layer.
V1.2 does not define a Patch DSL or operation taxonomy. A Presentation Reviser
reads the current Editorial Plan, Presentation Plan, and Defect set, then emits
a replacement Presentation Plan that must pass schema and hard-constraint
validation before fresh rendering and observation. A Semantic Revision may
modify existing Claim or Editorial content and add omitted content only with
explicit Canonical Transcript evidence. Once accepted, it invalidates and
regenerates Presentation, render, observation, and visual-review output. Stable
ID allocation and retention and the exact authorized-scope diff mechanism are
left to minimal implementation and calibration, without a complex semantic
diff or invalidation framework in the Design Baseline. Each Semantic or
Presentation Revision consumes one budget unit regardless of Defect count;
Semantic and Presentation changes cannot be mixed. Finite identical retry for
technical failure is separate from the Revision Budget.

Technical retry follows one minimal rule. When no complete model response is
obtained because of a transient transport failure, timeout, 429, or 5xx, the
run may spend its one shared model retry on the same logical call. Once a
complete response exists, it is the model result regardless of whether JSON, Schema,
grounding, authority, or other validation later accepts it; there is no hidden
resampling. Controller authorization of a Reviser immediately consumes one
Revision unit, including when the response is invalid or exceeds its authority.
If an initial mandatory Artifact cannot become valid, the run is `FAILED`.
After Revision failure, the Controller uses only the existing blocking Defect
and remaining budget to continue or terminate. The Design Baseline introduces
no finer retry/revision failure state machine.

The common state model, Artifact contracts, Defect routing, Revision authority,
budgets, failure behavior, evidence lineage, and stop conditions are now defined
before implementation. Continuous internal construction slices are:

- **A — Typed spine and editorial intelligence:** versioned Run Bundle,
  Controller, Claim Graph, Editorial Plan, grounding, explicit Semantic review,
  and bounded Semantic Revision;
- **B — Presentation intelligence:** Presentation Plan, one fixed Design System,
  a controlled Presentation Vocabulary, and the deterministic Renderer contract;
- **C — Closed-loop quality:** runtime Browser/DOM Screenshot Observation,
  presentation Defect detection, global issue routing, bounded revision,
  comparison evaluation, and run freezing.

These slices share one design and one Controller. They may be implemented and
evaluated incrementally, but must not introduce throwaway cross-version
contracts. V1.2 should compare semantic behavior against the V1.1 transcript
rather than compensate for ASR mistakes inside prompts.

Before the V1.2 specification is frozen, one architecture-ablation review must
remove any mechanism that does not directly support report quality, source
trust, or the finite self-repair loop.

The complete Design Baseline is
[`docs/requirements/visual-report-v1-2/`](../requirements/visual-report-v1-2/00-handoff.md).
Its validator-generated `requirements-readiness.json` reports 100% decision
coverage with no blocker or error. This is documentation completeness for a
future engineering authorization, not implementation authority, Final Spec
freeze, or product acceptance.

The current documentation deliverable is the V1.2 Design Baseline, not the
Final V1.2 Spec. It fixes product boundaries, Artifact ownership, source trust,
bounded Revision, Renderer/Observer authority, and core terminal semantics.
After separate implementation authorization, one minimal vertical loop may be
built and run to calibrate the Presentation Vocabulary, safety ceilings, and
other parameters explicitly reserved for runtime evidence. Calibration is
followed by the unified Architecture Ablation, after which only the Owner may
freeze the Final V1.2 Spec. Calibration may converge evidence-reserved
parameters or remove low-value mechanisms; it may not reopen any confirmed
semantic or authority boundary.

Historical report samples belong only to the implementation Calibration Set.
After Final V1.2 Spec freeze, formal evaluation uses samples that did not
participate in tuning and compares legacy V1.0, V1.2 with Revision disabled,
and full V1.2. Every condition runs repeatedly; every result stays in the
denominator; and no Prompt or parameter changes during the formal evaluation.
Evaluation covers hard failures, worst-case quality, unacceptable-run rate,
cross-run variance, and human quality judgment. The locked sample count and
repeat count are frozen after calibration from observed per-run cost, variance,
and human-review burden rather than precommitting the Design Baseline to a
three-by-three-by-three matrix.

The current authority permits documentation and read-only inspection only. No
prompt, Topic Mapper, Report Planner, Agent runtime, Renderer, browser tool,
dependency, model call, or generated runtime artifact may be changed or
executed under this design authorization.

## V1.3 — Post-Harness evolution

Status: `DEFERRED / SCOPE_TO_BE_DECIDED_AFTER_V1.2`

V1.3 is intentionally not preassigned to a renderer-only redesign because
Presentation, Renderer, Browser Observation, and visual repair now belong to
the integrated V1.2 Harness. Evidence from V1.2 will determine whether V1.3
should focus on multi-style templates, Skill/plugin packaging, broader content
domains, an optional free-text Editorial Instruction, evidence-derived
Presentation Profiles, quality hardening, or another explicitly approved
direction.

## Promotion order

```text
V1.0 runnable baseline
  → V1.1 frozen transcript foundation
  → V1.2 integrated Visual Editorial Agent / Harness
  → V1.3 evidence-selected post-Harness evolution
  → later deployment/multi-user work only when product quality warrants it
```

There is no date or automatic promotion. Requirements/design authority,
implementation authority, validation, Owner acceptance, deployment, and
publication remain separate decisions.
