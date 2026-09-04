# Test, Calibration, and Acceptance Contract

## Evidence layers

V1.2 uses distinct evidence layers. Passing one never implies the next:

1. documentation coverage/readiness validation;
2. implementation tests with fake/local deterministic inputs;
3. real-run implementation calibration on historical samples;
4. Architecture Ablation evidence;
5. Owner freeze of the Final V1.2 Spec;
6. formal locked evaluation;
7. Owner product acceptance;
8. Owner default-path promotion.

This Design Baseline authorizes only layer 1. It does not authorize model calls, browser runs, or
construction.

## Contract and unit tests

### Input

- accepts a valid complete V1.1 Canonical Transcript;
- rejects malformed manifest/unit references before model use;
- accepts exactly 50,000 Unicode characters;
- rejects 50,001 as `INPUT_TOO_LARGE` with zero model calls;
- proves no truncation, chunking, partial Claim Graph, or source mutation;
- accepts an empty Visual Asset Set.

### Claim Graph

- accepts only `claim_id`, atomic `claim_text`, `STATED`/`SYNTHESIS`, and evidence-unit identities as
  Claim domain fields;
- rejects duplicate/missing Claim IDs and absent/cross-run evidence;
- deterministically derives time, source status, and `SourceRef`;
- rejects a key Claim supported only by `UNRESOLVED` evidence;
- rejects external-knowledge and unsupported synthesis fixtures.

### Editorial Plan

- validates the fixed Editorial Objective and stable Report Shell;
- supports varying chapter counts and content structures;
- verifies every substantive Editorial Content Unit has Claim provenance;
- represents semantic comparison/process/sequence/grouping in Editorial rather than Presentation;
- rejects visual component selection inside Editorial;
- verifies limitation handling for uncertain evidence.

### Presentation Plan

- accepts only active controlled-vocabulary choices;
- rejects HTML, CSS, colors, coordinates, SVG paths, executable fragments, and unknown components;
- rejects reader-facing semantic copy or relationships absent from Editorial;
- verifies content-unit coverage and ordered placement;
- accepts text-only composition;
- validates supplied asset identities and rejects unbound/unreadable assets;
- verifies Presentation Profile is not a required field.

### Renderer and Observer

- same validated inputs and versions produce byte-identical HTML;
- reader content is escaped and local asset resolution is bounded;
- Renderer emits trace identifiers and deterministic non-semantic labels only;
- Observer loads the actual local report at 1080px and captures a full-page screenshot;
- geometry, overflow, and clipping outputs correspond to controlled fixtures;
- Observer exposes no external navigation or DOM mutation;
- mobile output never influences `COMPLETE`.

### Controller

- maximum two Revision authorizations and maximum one Semantic Revision;
- two Presentation Revisions are legal;
- authorization spends budget before Reviser result;
- invalid/over-authority Reviser response leaves budget spent;
- one Revision cannot mix layers;
- aesthetic-only review cannot spend budget;
- Semantic Revision invalidates all downstream Artifacts;
- Presentation Revision invalidates Render/Observation/visual review only;
- affected output is revalidated before terminal classification;
- no open loop remains after budget exhaustion.

### Retry

- transport error, timeout, 429, and 5xx without a complete response may consume the one shared
  run-wide identical model retry;
- a second eligible failure anywhere later in the run terminates the mandatory capability;
- complete malformed JSON, schema-invalid, ungrounded, or authority-invalid output allows zero
  hidden retries;
- retry request equality covers Prompt, Artifact snapshot, Schema, model/provider, and parameters;
- no model/provider/legacy fallback occurs.

### Terminal outcomes

- `COMPLETE` requires every hard gate, current Observation, and no material Defect;
- `DEGRADED` requires every hard gate and only known non-blocking limitations;
- any blocking Defect with no legal repair yields `FAILED`;
- missing mandatory Observation yields `FAILED`;
- status never records Owner acceptance.

## Integration tests

1. **Text-only happy path:** fake typed model outputs → semantic review → Presentation → actual local
   Render/Observe → `COMPLETE`.
2. **Asset path:** valid supplied image selected and rendered; unrelated image omitted; no new Claim
   created from pixels.
3. **Presentation repair:** injected clipping Defect → one Presentation Revision → fresh
   Render/Observe/review.
4. **Semantic escalation:** rendered density caused by Editorial redundancy → Controller-approved
   Semantic Revision → fresh complete downstream chain.
5. **Invalid Reviser:** budget remains spent and current valid Artifact remains authoritative.
6. **Uncertain source:** safe omission produces `DEGRADED`; unsupported core produces `FAILED`.
7. **Provider outage:** one identical retry, retained evidence, then failure without fallback.
8. **Observer outage:** no successful delivery despite valid HTML.
9. **Legacy isolation:** V1.2 failure never invokes V1.0 and never writes a legacy run directory.
10. **Web/CLI identity:** explicit version selection, understandable status, and correct report-open
    behavior.

Fake model responses prove control and validation, not editorial quality. At least one separately
authorized real end-to-end run is required for implementation calibration.

## Security tests

- Prompt-injection text inside transcript remains quoted data and cannot change stage/tool behavior;
- model output containing script/style/event-handler content is rejected or escaped before render;
- path traversal and unsupported asset URLs are rejected;
- API key does not appear in Run Bundle, Web responses, HTML, screenshot text, test snapshots, or
  errors;
- Observer never requests the report's external source links;
- one run cannot reference another run's Claim/content/asset identities;
- frozen historical evidence remains byte-untouched by all V1.2 tests.

## Calibration protocol

Historical samples are used only after separate implementation authority. Calibration evaluates:

- initial Presentation Vocabulary candidates;
- report-length, component-count, density, and asset ceilings;
- independent Semantic Critic call versus validated construction in one call;
- split Critic/Reviser versus combined bounded revision call;
- minimum useful Observer fields;
- simplest sufficient stable-ID and Semantic scope-check mechanics;
- material quality gain from one and two Revision opportunities;
- per-run cost, elapsed time, and observed variance.

Prompts, schemas, and mechanisms may change during calibration, but every change creates a new
version identity. Calibration cannot loosen source authority, semantic ownership, Renderer/Observer
boundaries, the two-Revision/one-Semantic ceiling, or terminal semantics.

## Architecture Ablation

After calibration, run controlled comparisons that remove or combine each non-core mechanism. Keep
it only when evidence shows direct contribution to report quality, source trust, or finite
self-repair. The ablation result records:

- candidate mechanism and simpler alternative;
- same-source comparison conditions;
- quality, failure, variance, cost, and latency effect;
- retain/remove decision;
- resulting Prompt/Schema/Design System/Observer version.

The ablation must specifically challenge separate Critic/Reviser calls, separate semantic review
call, vocabulary breadth, Observer detail, safety-ceiling complexity, and semantic scope-check
complexity.

## Final Spec freeze gate

Before the Owner can freeze the Final V1.2 Spec, calibration and ablation must provide:

- one working full vertical loop with retained Run Bundles;
- passing contract, integration, and security tests;
- real 1080px rendered/observed reports with no unresolved blocking defect;
- chosen Presentation Vocabulary and deterministic safety ceilings;
- chosen model-call topology;
- chosen Observer contract and simple semantic revision guard;
- an explicit human quality rubric and unacceptable-run definition;
- a locked evaluation sample count and repeat count justified by observed cost, variance, and review
  burden;
- a frozen Prompt/Schema/Design System/Renderer/Observer revision for formal evaluation.

Only the Owner records that freeze. Implementation completion or green tests cannot do so.

## Formal locked evaluation

After Final Spec freeze, use samples excluded from all calibration. Compare:

1. legacy V1.0;
2. V1.2 with Revision disabled;
3. full V1.2.

Run every condition repeatedly under the frozen configuration. All initiated results, including
technical and model failures, remain in the denominator. No best-of-N selection, selective rerun,
Prompt/parameter change, failed-run deletion, or mid-evaluation repair is allowed.

Report at least:

- hard-failure count/rate;
- worst-case human quality;
- unacceptable-run count/rate;
- cross-run variance by rubric dimension;
- source-grounding violations;
- `COMPLETE`/`DEGRADED`/`FAILED` distribution;
- Revision frequency, route, and success;
- cost and elapsed time;
- blind or order-balanced human quality ratings where practical.

The numerical acceptance thresholds, locked sample count, and repeats are values frozen in the
Final Spec, not values retrofitted after results are visible.

## Product acceptance and promotion

The Owner reviews the complete formal denominator and either accepts or rejects V1.2. Acceptance
does not automatically replace V1.0. Default-path promotion is a separate Owner decision based on
same-source quality, reliability, cost, limitations, and rollback evidence. The legacy path remains
available until that explicit switch decision; V1.2 never uses it as runtime fallback.

## Smallest implementation validation commands

The implementation task should run the narrow new V1.2 tests first, followed by affected legacy
visual-report tests and Ruff. The full repository suite is required only after the vertical path
touches shared ingest/Web/CLI/renderer seams or before Owner implementation review.
