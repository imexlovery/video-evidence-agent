# Delivery Plan

## Current delivery

This package completes requirements and technical design only. It changes no product code,
dependency, runtime configuration, prompt used by the product, model output, browser output,
evaluation result, default path, or deployment state.

The V1.2 Design Baseline is one end-to-end architecture. Semantic, Presentation, Renderer, Browser
Observation, and bounded repair are internal construction slices, not separate roadmap versions or
independent product designs.

## Required future authorization

Before construction, the Owner must issue a new goal that names:

- the V1.2 Design Baseline package and repository revision to build from;
- whether the goal permits product/dependency changes;
- whether it permits external Provider calls and real browser calibration runs;
- the samples authorized for calibration;
- the stop state and whether a commit is requested.

No documentation validator result supplies those permissions.

## Minimal vertical implementation

When authorized, implement the smallest complete vertical loop through these continuous internal
slices. Do not create Owner approval gates between slices unless the future goal explicitly does so.

### Slice A — Versioned Artifact spine and Controller

Deliver:

- isolated V1.2 package/module boundary;
- input/config snapshot and unique Run Bundle;
- minimum Claim Graph, Editorial Plan, Presentation Plan, Observation, Defect, and run-record
  Pydantic contracts;
- Controller capability order, terminal classifier, retry rule, and Revision counters;
- deterministic reference/provenance validators;
- fake-model contract tests.

Stop and repair ordinary failures inside the authorized goal. Do not generalize into a workflow
framework, Patch DSL, event system, or database.

### Slice B — Semantic capability

Deliver:

- source-bounded Claim construction;
- Editorial planning against the fixed Objective;
- explicit Semantic validation/review;
- uncertainty and omission behavior;
- one authorized Semantic Revision path;
- provenance from Editorial Content Units to Canonical Transcript units.

The initial call topology is the simplest implementation that preserves Artifact snapshots. It is a
calibration candidate, not a permanent architecture claim.

### Slice C — Presentation, Render, and Observe

Deliver:

- the smallest useful controlled Presentation Vocabulary;
- Presentation planning with zero semantic write authority;
- one deterministic Design System/Renderer path;
- text-only completion and optional supplied-asset binding;
- actual 1080px full-page screenshot and minimum DOM geometry/overflow/clipping sensor;
- visual review, Presentation Revision, and allowed Semantic escalation;
- fresh validation/render/observation after every Revision;
- local CLI/Web selection/status/open integration.

Reuse legacy renderer/design primitives only where they naturally implement the new contract. Do not
retain old `ReportPlan` or seven-block constraints for compatibility.

### Slice D — Integrated validation

Deliver:

- all unit, integration, security, and failure-path tests in `09-test-acceptance.md`;
- an end-to-end fake-model run with a real local render and Observer;
- affected legacy test coverage proving path isolation;
- clean-start instructions and evidence;
- a concise implementation report listing actual files, commands, and known limitations.

If real Provider/browser runs were not explicitly authorized, stop here without performing them.

## Calibration campaign

Under explicit real-run authority:

1. Declare historical calibration samples and one immutable calibration revision.
2. Run the complete vertical loop and retain every result.
3. Measure hard failures, unacceptable outcomes, quality variance, Revision behavior, latency, and
   cost.
4. Adjust only calibration-owned parameters with a new version identity.
5. Compare combined/separate semantic review and Critic/Reviser calls.
6. Converge the Presentation Vocabulary, ceilings, Observer detail, and semantic scope guard.
7. Do not use any locked formal-evaluation sample.

Calibration is allowed to simplify mechanisms and tune reserved parameters. It cannot relax source
trust, one-way semantic ownership, the deterministic Renderer/Observer boundary, retry semantics,
Revision ceilings, or terminal meaning.

## Architecture Ablation

After calibration, remove or combine every mechanism whose direct value is not demonstrated. At
minimum, challenge:

- independent Semantic Critic call;
- separate Critic and Reviser calls;
- each Presentation component and configuration dimension;
- each Observer field beyond the minimum sensor;
- each safety-ceiling rule;
- any stable-ID/diff machinery beyond the minimum needed for provenance and bounded authority;
- any compatibility or abstraction layer added during construction.

Record retained and removed mechanisms with same-source evidence. Update the complete requirement
package to the calibrated contract without reopening Owner-confirmed core boundaries.

## Final Spec and formal evaluation

The Owner freezes the Final V1.2 Spec only after reviewing calibration and ablation evidence. That
freeze sets the Prompt/Schema/Design System/Renderer/Observer versions, quality rubric,
unacceptable-run definition, locked sample count, repeat count, and formal thresholds.

Formal evaluation then compares legacy V1.0, V1.2 without Revision, and full V1.2 on untuned locked
samples. All results stay in the denominator. No configuration change or selective rerun is allowed.

## Default-path promotion and rollback

Even if V1.2 is accepted, it remains a parallel path until the Owner separately promotes it. The
promotion plan must preserve an explicit legacy selection during the initial switch window and
record the promoted V1.2 contract/version. Rollback changes the selected default; it does not mutate
or relabel existing V1.2 Run Bundles.

## Deferred productization

V1.3 may evaluate optional free-text Editorial Instruction, named Presentation Profiles supported by
evaluation, mobile commitments, hosted/public service boundaries, accounts/tenancy, broader privacy
and rights policy, and public Bilibili ingest behavior. None should be scaffolded in V1.2 without a
new requirements decision.

## Completion evidence by stage

| Stage | Evidence | Authority to advance |
|---|---|---|
| Design Baseline | this package plus generated validator report | Owner authorizes construction |
| minimal vertical implementation | tests, fake E2E, implementation report | explicit calibration authority |
| calibration | all runs, measurements, parameter revisions | proceed to ablation inside authorized goal |
| Architecture Ablation | retain/remove ledger and updated package | Owner freezes Final Spec |
| formal evaluation | locked full denominator and human review | Owner accepts/rejects product |
| default switch | accepted evaluation plus rollback plan | Owner promotes default |

At every row, technical success is evidence for the named decision, not implicit authorization.
