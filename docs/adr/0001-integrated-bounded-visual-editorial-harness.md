---
status: accepted
date: 2026-09-04
---

# Use an integrated bounded Visual Editorial Harness

V1.2 is one G2 local Visual Editorial Agent/Harness rather than separate Semantic and Renderer
products or an unconstrained coding agent. It uses one fixed Design System with a controlled
Presentation Vocabulary, keeps the Renderer deterministic, makes Browser/DOM Screenshot
Observation part of the runtime loop, and routes observed Defects to at most two Revision attempts per
run; no more than one may be a Semantic Revision, while both may be Presentation Revisions. This trades
free-form generation and unlimited refinement for traceable variation, real rendered feedback, and
a finite COMPLETE, DEGRADED, or FAILED outcome.

## Consequences

- Models may select legal presentation choices but may not emit HTML, CSS, colors, or coordinates.
- One model is invoked through fixed Harness stages and explicit Artifact Snapshots, not a free
  ReAct, browser, or tool loop. Stage roles are not required to become permanent components or
  first-class product states.
- V1.2 is a single-model architecture. Claim, Editorial, Semantic Critic/Reviser, Presentation,
  and Visual Critic/Reviser roles share one run-level Provider/model/credential configuration and
  differ only through Prompt, input Artifact, output Schema, and necessary call parameters. The
  reference model is `GLM-5.3-Flash`; V1.2 has no role-level model variables, routing, or fallback.
  A project-owned ModelClient/Provider Adapter keeps stages independent from a concrete SDK.
  Role-level overrides may be added later only when evaluation demonstrates a real need.
- The V1.2 Harness remains project-owned Python/Pydantic rather than adopting a general Agent
  framework. Typed Artifact-to-Stage boundaries preserve a future migration path if real workflow
  complexity later warrants one; frameworkless is not a permanent product principle.
- V1.2 is a parallel versioned execution path for its schemas, Harness, Run Bundle, and run
  identities. It shares the Canonical Transcript, ingest, Web/CLI infrastructure, and reusable
  renderer/design primitives with the existing product; it neither rewrites historical contracts
  nor automatically falls back to the legacy path. Default-path promotion requires same-source
  comparison, repeated-run evaluation, and separate Owner acceptance.
- A Critic reports typed Defects; it does not rewrite the whole report.
- V1.2 freezes review capabilities, not a permanent one-call-per-role topology. Semantic output
  must receive explicit semantic validation/review; Presentation must be rendered and observed;
  rendered output must receive visual review; and every Revision must revalidate affected results.
  Whether Critic and Reviser are separate model calls is reserved for calibration and ablation.
- Browser Observation comes from a narrow deterministic sensor; the model neither navigates freely
  nor mutates the DOM. Owner acceptance remains a separate product gate.
- Defect severity has only blocking and non-blocking forms. A Defect must be tied to a rule and
  affect credibility, readability, or legal delivery; aesthetic opportunities neither trigger a
  Revision nor prevent `COMPLETE`.
- The Claim Graph contains only atomic source-backed Claims and evidence links: stable `claim_id`,
  `claim_text`, `STATED` or `SYNTHESIS`, and Canonical Transcript evidence-unit IDs. Time, source
  status, and `SourceRef` are derived deterministically; confidence, importance, relationship
  taxonomy, and external knowledge are absent.
- Semantic ownership is one-way: Claim Graph to Editorial Plan to Presentation Plan. Editorial is
  authoritative for final reader-facing wording, order, comparison, process, sequence, and grouping.
  Presentation may only choose legal visual expression and supplied-asset treatment; it cannot add
  semantic copy, conclusions, or relationships. The Renderer may generate deterministic,
  non-semantic UI chrome such as numbering and labels.
- V1.2 defines no named Presentation Profile. Repeated presentation strategies may become profiles
  only after evaluation demonstrates stable value.
- V1.2 may place and weight supplied local visual assets but does not discover, extract, search for,
  or generate them; an empty asset set must preserve the full report workflow.
- The fixed-width 1080px desktop Canonical Report is the only V1.2 visual quality surface. Mobile
  remains best-effort and the Web Shell is only an execution and report-opening surface.
- V1.2 uses one versioned fixed Editorial Objective and exposes no Editorial Brief, audience,
  depth, content, or style customization input.
- Source uncertainty reuses V1.1 status: nonessential uncertainty is omitted, essential content is
  qualified when safe, and an unsupported core conclusion fails. Semantic repair never changes the
  Canonical Transcript.
- V1.2 processes one complete Canonical Transcript up to the existing 50,000 Unicode-character
  envelope. Oversize input fails before model use; there is no truncation, chunking, or Claim merge.
- Reports share a small Report Shell while the Editorial body is content-adaptive. No report is
  required to fill fixed component quotas or include every component family.
- The legacy `ReportPlan` and its seven Typed Blocks are not V1.2 compatibility contracts. Their
  implementations may be reused as Presentation Vocabulary candidates, while Presentation owns a
  new controlled plan and Editorial never selects visual block types. Arbitrary HTML/CSS,
  coordinates, and a general page DSL remain prohibited.
- The configured multimodal model may read supplied visual assets and rendered report screenshots.
  Provider disclosure belongs to the product boundary; V1.2 adds no asset-rights subsystem or
  local/external processing fork.
- The specification does not require a standalone revision-accounting domain object.
- Visual Critic cannot edit semantics, but it may recommend the defect layer. When Presentation
  cannot resolve an Editorial root cause, the Controller may spend the remaining budget on the one
  allowed Semantic Revision, invalidating and rebuilding downstream Presentation, render, and
  observation artifacts.
- One Revision may address a related set of Defects in only one layer. V1.2 defines no Patch DSL:
  the relevant Reviser regenerates a valid typed artifact. Presentation replacement is constrained
  by schema and hard validation. Semantic replacement may modify existing Claim or Editorial content
  and add omitted content only with explicit Canonical Transcript evidence. A successful Semantic
  Revision invalidates and regenerates Presentation, render, observation, and visual-review output.
  Stable-ID retention and authorized-scope diff mechanics are calibration decisions, not a complex
  Design Baseline subsystem. Limited identical retries for technical failures are separate from the
  Revision Budget.
- At most one shared run-level identical model retry is allowed, and only when no complete response
  was obtained because of a transient transport, timeout, 429, or 5xx failure. Any complete response
  is the model result even when later validation rejects it; it is never hiddenly resampled.
  Controller authorization consumes one Revision unit before a Reviser call, including when its
  result is invalid or exceeds authority. V1.2 deliberately defines no finer retry/revision failure
  taxonomy.
- Multi-style templates and arbitrary per-run style generation remain outside V1.2.
- Before the V1.2 specification is frozen, an architecture-ablation pass removes mechanisms that
  do not directly serve report quality, source trust, or the finite self-repair loop.
- The current documentation is the V1.2 Design Baseline, not the Final V1.2 Spec. A separately
  authorized minimal vertical implementation calibrates the Presentation Vocabulary, safety
  ceilings, and other evidence-reserved parameters. Architecture ablation follows calibration;
  only then may the Owner freeze the Final V1.2 Spec. Calibration cannot reopen fixed semantic,
  authority, Renderer/Observer, or bounded-revision boundaries.
- Historical samples are calibration inputs only. Formal comparison after Final V1.2 Spec freeze
  uses samples excluded from tuning, compares legacy V1.0, V1.2 without Revision, and full V1.2,
  repeats every condition, retains every result in the denominator, and evaluates hard failures,
  worst cases, unacceptable-run rate, cross-run variance, and human quality. Calibration evidence
  determines the locked sample and repeat counts rather than hard-coding an unevidenced 27-run set.
