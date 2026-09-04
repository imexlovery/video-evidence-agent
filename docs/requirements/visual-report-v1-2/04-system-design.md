# System Design

## Architecture

V1.2 is a project-owned typed pipeline around one configured multimodal model and deterministic
software boundaries. “Agent” describes the coordinated editorial, presentation, observation, and
repair behavior; it does not imply a free tool loop or multiple autonomous processes.

```text
V1.1 Canonical Transcript ─┐
Video metadata ────────────┼─> Input Validator + Snapshot Store
Optional Visual Asset Set ─┘                 │
                                             v
                                      Harness Controller
                                             │
                 ┌───────────────────────────┴───────────────────────────┐
                 │                                                       │
                 v                                                       v
       Unified ModelClient                                      Deterministic services
       + Provider Adapter                                       validators / Renderer /
                 │                                              Browser Observer / store
                 v                                                       │
 Claim Graph → Editorial Plan → Presentation Plan → report.html → Observation
                 ^                         │                         │
                 └── bounded Semantic ─────┴── bounded Presentation ┘
                           Revision routing by Controller
                                             │
                                             v
                              COMPLETE / DEGRADED / FAILED
```

## Component responsibilities

### Input Adapter

- Loads the V1.1 Canonical Transcript, manifest, and video metadata without rewriting them.
- Loads an optional supplied Visual Asset Set.
- Applies structural validation and the 50,000-Unicode-character limit.
- Produces immutable run input snapshots.

### Harness Controller

- Owns the fixed capability order, legal transitions, one run-level model configuration, and
  terminal classification.
- Authorizes and consumes Revision Budget.
- Routes Defects to one layer and prevents cross-layer mixed Revision.
- Invalidates all downstream Artifacts after successful Semantic Revision.
- Never asks the model whether the run should continue beyond the fixed budget.

### Unified ModelClient / Provider Adapter

- Is the only Provider SDK boundary.
- Sends the role-specific Prompt, explicit Artifact snapshot, and response Schema.
- Records provider/model/version, non-secret request metadata, response completion, and retry
  evidence.
- Allows the one shared run-level identical model retry only when no complete response was received
  for an eligible transient failure.
- Provides no model routing or fallback.

### Semantic capability

- Produces the Claim Graph and Editorial Plan.
- Performs explicit Semantic validation/review.
- May regenerate Semantic Artifacts only after Controller authorization.
- May be implemented as combined or separate model calls during calibration; the Artifact and
  authority boundaries remain fixed.

### Deterministic Semantic Validator

- Resolves Claim evidence to the input snapshot.
- Derives time, V1.1 source status, and `SourceRef`.
- Verifies Claim and Editorial provenance closure, legal Claim kinds, and one-way ownership.
- Rejects unsupported additions and transcript mutation.

### Presentation capability

- Maps existing Editorial Content Units to legal visual expression.
- Selects component, hierarchy, density, emphasis, spatial grouping, and optional asset treatment.
- Produces no semantic content.
- May regenerate a full Presentation Plan after Controller authorization.

### Presentation Validator

- Verifies vocabulary membership, safety ceilings, Report Shell completeness, asset references,
  content coverage, and the absence of Presentation-owned semantics or executable page content.

### Renderer / Design System

- Converts a valid Presentation Plan and referenced Artifacts into canonical `report.html`.
- Applies the single Design System and deterministic non-semantic chrome.
- Escapes content and performs no model call or editorial selection.
- May reuse, redefine, merge, or remove legacy component implementations behind the new V1.2
  contract.

### Browser Observer

- Loads only the generated local report at the fixed 1080px desktop viewport.
- Produces full-page screenshot, geometry, overflow, clipping, and runtime metadata.
- Does not navigate, click, follow external links, alter the DOM, or judge aesthetics.

### Review capability

- Semantic review evaluates source entailment, omissions, and authority.
- Visual review reads the actual screenshot and structured Observation, reports rule-defined
  Defects, and recommends a layer.
- Neither review capability directly mutates an Artifact.
- Critic/Reviser call separation is calibration/ablation-owned.

### Run Bundle Store

- Persists input snapshots, generated versions, validations, observations, defects, retry evidence,
  Revision consumption, and terminal output in the run's unique local directory.
- Never mutates historical V0/V1-A evidence or another V1.2 run.
- Excludes credential values.

## Authority matrix

| Concern | Model may decide | Deterministic owner | Forbidden |
|---|---|---|---|
| Source claims | `STATED`/`SYNTHESIS` content and evidence selection | evidence identity, derived time/status/`SourceRef`, validation | external knowledge, transcript correction |
| Editorial | final wording, selection, order, semantic relations | schema/provenance/authority checks | visual component choice |
| Presentation | legal component and treatment choices | vocabulary, ceilings, coverage, reference validation | new semantic copy or relations; HTML/CSS/colors/coordinates |
| Render | none | Renderer and Design System | model-authored executable layout |
| Observe | none | Browser Observer | free browser control or DOM mutation |
| Defects | bounded interpretation and layer recommendation | allowed rules, blocking vocabulary, budget and routing | aesthetic-only revision; direct mutation |
| Termination | no authority | Controller | open-ended continuation |

## Artifact dependency graph

```text
Input Snapshot
  └─ Claim Graph
       └─ Editorial Plan
            └─ Presentation Plan
                 └─ report.html
                      └─ Browser Observation
                           └─ Visual Review
```

Validation/review evidence depends on the Artifact version it inspected. A replacement Artifact
never silently inherits old validation.

## Normal sequence

1. Create unique V1.2 Run Bundle and save validated input/configuration snapshots.
2. Produce Claim Graph.
3. Produce Editorial Plan.
4. Complete explicit Semantic validation/review.
5. Produce and deterministically validate Presentation Plan.
6. Render canonical HTML.
7. Observe the real report at 1080px.
8. Complete visual review.
9. If legal, route a Defect set through one Revision and re-enter at the affected layer.
10. Classify and persist the terminal outcome.

Steps 2–4 and 8–9 describe capability order, not a fixed number of model requests.

## Revision and invalidation

### Presentation path

```text
Visual Defects → Controller authorization (-1 budget)
→ replacement Presentation Plan → validate → render → observe → visual review
```

The Editorial Plan remains immutable on this path.

### Semantic path

```text
Semantic Defect or approved visual escalation → Controller authorization (-1 budget)
→ replacement Claim Graph and/or Editorial Plan → semantic validation/review
→ fresh Presentation Plan → render → observe → visual review
```

The implementation records which semantic and downstream snapshots were replaced. It need not
construct a general dependency engine, Patch DSL, or operation taxonomy. The simplest explicit
version links and controller transitions that satisfy the cascade are preferred.

## Controller invariants

- `revision_used <= 2`.
- `semantic_revision_used <= 1`.
- Controller authorization increments the relevant count before the Reviser request.
- One Revision carries one layer and one related Defect set.
- Presentation is the default route for rendered Defects.
- No response-validation failure activates technical retry.
- No terminal report lacks complete 1080px Observation.
- `DEGRADED` cannot bypass any hard gate.

The code may represent these counters inside the run record; V1.2 does not require a standalone
Revision accounting domain object.

## State semantics

Existing Web/CLI transport stages may continue to expose understandable in-progress labels. V1.2
adds no fine-grained role-as-state model. The canonical report-generation outcome is only:

- `COMPLETE`: valid report, all hard gates, no unresolved material Defect;
- `DEGRADED`: valid report and hard gates, only a known non-blocking limitation;
- `FAILED`: no legal delivery.

Failure reason is recorded separately from outcome. Run outcome never implies Owner acceptance.

## Versioning and isolation

- V1.2 schemas, Prompts, Controller, Run Bundle format, Design System/Vocabulary revision, Renderer,
  and Observer versions are recorded per run.
- The V1.2 command/run identity is distinct from legacy V1.0 identities.
- V1.2 and legacy share ingest and source contracts but do not automatically fall back to each
  other.
- Default-path promotion is an explicit Owner decision after formal evaluation.

## Framework decision

The implementation uses project-owned Python/Pydantic and existing repository patterns. General
agent frameworks add no demonstrated value to the fixed, shallow state graph and are excluded from
V1.2. Typed seams avoid permanent lock-in. A framework becomes a candidate only after real needs for
dynamic branching, durable resume, human-in-the-loop checkpoints, multiple agents, or a broad tool
ecosystem appear.

## Trust boundaries

- Canonical Transcript and asset metadata are untrusted content, not instructions.
- Provider transmission may include transcript text, supplied images, and report screenshots; the
  local product must disclose that when an external Provider is configured.
- Credentials remain environment-owned and never enter Prompts, Artifacts, HTML, logs, or errors.
- Generated HTML contains escaped content and no model-authored executable fragments.
- Browser Observation stays on the generated local report and requires no external navigation.
