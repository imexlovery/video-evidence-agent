# User Scenarios

## Scenario 1 — Generate a complete text-only report

**Preconditions**

- A V1.1 Canonical Transcript and manifest are valid and contain no more than 50,000 Unicode
  characters.
- The single run-level Provider/Model/credential configuration is valid.
- No Visual Asset Set is supplied.

**Flow**

1. The Owner selects the V1.2 path through the local CLI or Web entry point.
2. The Harness snapshots input and configuration.
3. It creates and reviews the Claim Graph and Editorial Plan.
4. It creates a Presentation Plan that uses text-capable legal components.
5. The Renderer creates `report.html`.
6. The Observer captures the complete 1080px page and minimum geometry evidence.
7. Visual review finds no rule-defined material Defect.

**Outcome**

The run is `COMPLETE`. The report is fully useful without images, and its substantive content is
traceable through Editorial Content Units and Claims to Canonical Transcript units.

## Scenario 2 — Use supplied visual assets selectively

**Preconditions**

- Scenario 1 preconditions hold.
- The Owner supplies a valid local Visual Asset Set with stable asset identifiers and source
  context.

**Flow**

Presentation decides whether an image supports an existing Editorial Content Unit, where to bind
it, and its visual weight. It may omit an irrelevant or harmful image. It cannot infer new report
claims from an image or write new semantic captions unless that text already belongs to Editorial.

**Outcome**

The report may use zero, some, or all supplied assets. Missing or unused assets never make an
otherwise valid text report fail.

## Scenario 3 — Preserve source uncertainty

**Preconditions**

One or more Canonical Transcript units carry V1.1 uncertainty or `UNRESOLVED` source status.

**Flow**

- Nonessential uncertain information is omitted first.
- Essential information that remains safely summarizable uses conservative wording and, when
  needed, a short limitation.
- An `UNRESOLVED` unit cannot independently support a key reader-facing conclusion.

**Outcomes**

- If the core report remains reliable with a local omission, delivery may be `DEGRADED`.
- If the main conclusion cannot be supported reliably, the run is `FAILED`.
- No review or Revision edits the Canonical Transcript.

## Scenario 4 — Repair a presentation Defect

**Preconditions**

The first render is source-grounded and semantically valid, but Browser Observation reveals one or
more related presentation Defects, such as clipping, overflow, or unreadable density.

**Flow**

1. Visual review reports the Defect set, blocking status, affected Presentation references, and
   why the issue affects readability or legal delivery.
2. The Controller authorizes one Presentation Revision and immediately spends one budget unit.
3. The Reviser receives the current Editorial Plan, Presentation Plan, and related Defects and emits
   a full replacement Presentation Plan.
4. Deterministic validation rejects semantic additions and illegal presentation choices.
5. A valid replacement is rendered, observed, and visually reviewed again.

**Outcome**

No Editorial wording changes. The run ends according to the current Defects and remaining budget.

## Scenario 5 — Escalate a rendered problem to Semantic Revision

**Preconditions**

Visual review identifies a problem whose root cause is content length, content selection,
redundancy, or another Editorial issue that cannot be reasonably solved within Presentation
authority. At least one Revision unit and the single Semantic Revision allowance remain.

**Flow**

1. Visual review recommends the Semantic layer but cannot edit it.
2. The Controller authorizes one Semantic Revision and spends one budget unit.
3. The Reviser may modify existing Claim/Editorial content or add omitted content only with explicit
   Canonical Transcript evidence.
4. Semantic validation/review runs again.
5. The old Presentation Plan, render, Browser Observation, and visual review are invalidated.
6. All invalidated downstream Artifacts are regenerated and reviewed.

**Outcome**

There is no mixed Semantic/Presentation Revision and no shortcut reuse of stale downstream output.

## Scenario 6 — Exhaust the Revision Budget

**Preconditions**

Two Revisions have been authorized, or one Semantic Revision has used the semantic allowance.

**Flow and outcome**

- If all hard gates pass and no material rule-defined Defect remains, the run is `COMPLETE`.
- If a valid, source-grounded, readable report remains with only a known non-blocking source
  omission or presentation Defect, the run is `DEGRADED`.
- If any blocking Defect remains, the run is `FAILED`.
- Purely aesthetic suggestions never consume budget and never block `COMPLETE`.

## Scenario 7 — Model response is invalid

**Preconditions**

A model call returns a complete response that fails JSON, Schema, grounding, or authority checks.

**Flow and outcome**

The response is retained as the model result and is not hiddenly resampled. If it was an initial
mandatory Artifact, the run is `FAILED`. If it was an authorized Reviser call, its budget unit stays
spent; the Controller uses only remaining budget and the current blocking status to continue or
terminate.

## Scenario 8 — Provider fails before a complete response

**Preconditions**

A transport failure, timeout, 429, or 5xx prevents receipt of a complete model response.

**Flow**

If the run-wide model retry has not been used, the same logical call may run once more with identical
input and configuration. No other failure kind permits that retry, and no later call receives a
second retry. The initial attempt and retry evidence are both retained.

**Outcome**

Success continues the fixed workflow. A second technical failure leaves a mandatory Artifact
unavailable, so the run is `FAILED`. There is no alternate model or provider fallback.

## Scenario 9 — Browser Observation is unavailable

**Preconditions**

The report renders, but the required desktop screenshot or minimum DOM observation cannot be
completed.

**Flow and outcome**

The technical operation receives only the finite identical retry allowed by its deterministic
integration policy. If mandatory observation remains unavailable, the run is `FAILED`; an
unobserved report cannot be labeled `COMPLETE` or `DEGRADED`.

## Scenario 10 — Reject an oversized transcript

**Preconditions**

The Canonical Transcript contains more than 50,000 Unicode characters.

**Outcome**

The Harness returns `FAILED` with `INPUT_TOO_LARGE` before any model call. It does not truncate,
chunk, select a prefix, or create a partial Claim Graph.

## Scenario 11 — Compare repeated runs honestly

**Calibration phase**

Historical samples may be run repeatedly to calibrate the Presentation Vocabulary, safety
ceilings, and call topology. Their output cannot become formal acceptance evidence.

**Formal phase**

After the Owner freezes the Final Spec, samples excluded from calibration are run under legacy
V1.0, V1.2 with Revision disabled, and full V1.2. Every condition is repeated; all results remain in
the denominator; no best result is selected; no selective rerun occurs; and Prompts or parameters
do not change during the evaluation.

## Scenario 12 — Inspect and reproduce a run

The Owner can inspect the input snapshot, each generated Artifact, deterministic validations,
model-call metadata without credentials, Browser Observation, Defects, Revision consumption, and
terminal reason. A saved valid Presentation Plan can be re-rendered and re-observed without a model
call. Replaying deterministic stages does not claim that a fresh model run would produce identical
prose.
