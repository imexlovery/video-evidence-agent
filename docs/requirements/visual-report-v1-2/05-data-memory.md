# Data, State, Provenance, and Memory

## Data inventory

| Data or asset | Authority | Use in V1.2 | Persistence | Change rule |
|---|---|---|---|---|
| V1.1 Canonical Transcript | authoritative source text | all factual/semantic grounding | snapshotted into or referenced by Run Bundle | read-only; never repaired by V1.2 |
| V1.1 transcript manifest/provenance | authority for source status and derivation | uncertainty, time, and `SourceRef` derivation | retained with input snapshot | read-only |
| video metadata | existing ingest contract | title, duration, source attribution, shell metadata | retained per run | deterministic validation only |
| supplied Visual Asset Set | optional user-supplied local input | possible image placement | manifest and used asset references retained | use/omit/bind only; no discovery |
| Claim Graph | generated semantic Artifact | source-facing propositions | every accepted/replaced version retained | model-generated, deterministically validated |
| Editorial Plan | generated semantic Artifact | authority for reader-facing meaning | every accepted/replaced version retained | model-generated, semantically reviewed |
| Presentation Plan | generated presentation Artifact | authority for legal visual choices | every accepted/replaced version retained | model-generated, deterministically validated |
| `report.html` | deterministic canonical user artifact | local reading | each render version retained or version-addressable | Renderer only |
| screenshot/DOM Observation | deterministic sensor evidence | visual review and delivery gate | retained per observed render | Observer only |
| Defect/review evidence | generated assessment Artifact | routing and terminal decision | retained per reviewed snapshot | review may report; Controller decides |
| run record | canonical execution record | state, versions, budget, diagnostics | retained in unique run directory | Controller only |

V1.2 adds no operational database, vector store, remote object store, or shared memory service.

## Source authority and lineage

Canonical Transcript units remain the highest factual authority. Claim text is derived interpretation,
Editorial content is reader-facing interpretation, and Presentation is non-semantic expression.
Conflicts resolve toward the source: a fluent Claim or paragraph cannot override its evidence.

Required lineage:

```text
Canonical Transcript snapshot
  → Claim and evidence-unit IDs
  → Editorial Content Unit and Claim IDs
  → Presentation placement and Editorial Content Unit IDs
  → rendered element trace
  → Browser Observation and visual-review references
```

Time, source status, and `SourceRef` are deterministically projected from evidence units. They are
not separate model judgments.

## Artifact snapshot contract

Every model-mediated or deterministic capability MUST receive an explicit Artifact snapshot. The
snapshot identity MUST make it possible to determine:

- which source and upstream Artifact version was read;
- which Prompt, Schema, model/provider, and relevant parameter version applied;
- which output and validation/review evidence resulted;
- whether a later Revision invalidated it.

The implementation may use hashes, monotonically increasing local versions, or another simple
deterministic identity mechanism. It must preserve the relationships above without creating a
general event-sourcing or dependency framework.

## Run Bundle logical contents

One unique local Run Bundle contains these logical groups; exact directory names follow the
repository's implementation conventions:

```text
run metadata and non-secret configuration
input snapshots
semantic artifacts and reviews
presentation artifacts and validations
rendered HTML versions
browser screenshots and structured observations
visual reviews and defects
retry and revision evidence
terminal outcome and failure/limitation reasons
```

Artifacts are written atomically where existing repository primitives support it. A Revision
creates a new version rather than silently overwriting the evidence used by an earlier review.
Terminal bundles are treated as historical evidence and are not edited to improve a result.

## State authority

The Controller's run record is authoritative for:

- current upstream/downstream Artifact identities;
- total and Semantic Revision units used;
- technical retry evidence;
- active in-progress phase exposed through Web/CLI;
- terminal `COMPLETE`, `DEGRADED`, or `FAILED` outcome;
- blocking/non-blocking limitation and failure reason.

An HTML file's existence, a screenshot, or a model response cannot independently declare run
completion.

## Memory boundary

V1.2 has no conversational working-memory dependency and no persistent model memory. Each role sees
only its Prompt and explicit authorized Artifacts. The model cannot rely on an earlier chat turn,
hidden scratchpad, browser history, or another run's output.

Run Bundles are evidence and replay inputs, not autonomous memory. No retrieval system searches
prior reports to influence a new run.

## Invalidation

- A replacement Presentation Plan invalidates only its Render, Observation, and visual review.
- Any successful Semantic Revision invalidates Presentation Plan, Render, Observation, and visual
  review.
- A failed or rejected replacement remains evidence but does not become the current valid Artifact.
- Validation/review results are valid only for their referenced snapshot.

The implementation records this cascade directly in Controller logic. It does not need a generic
invalidation graph.

## Replay and reproducibility

The system MUST support model-free revalidation and re-rendering from retained valid Artifacts.
Browser Observation SHOULD be reproducible under the recorded browser/runtime and viewport. Replay
produces new evidence linked to the source snapshots and never rewrites the original run.

Model outputs are not expected to be byte-identical across fresh runs. Reproducibility is assessed
through invariant compliance, report-quality floors, unacceptable-run rate, and cross-run variance.

## Retention, access, export, and deletion

For the local G2 pilot, the named Owner controls filesystem access. Run Bundles remain local and are
retained until the Owner manually removes or archives them. V1.2 adds no automatic expiry,
cross-user sharing, publication, or product-level delete API. Deleting local evidence is an Owner
filesystem action and cannot be undone by the Harness.

Formal evaluation bundles and frozen historical evidence are append-only within their evaluation
process. Calibration output is clearly labeled and cannot be promoted into locked evaluation
evidence.

## Privacy and provider transmission

The Run Bundle MUST record the Provider endpoint label, model, and whether a credential was present,
but never the key. If the configured Provider is external, the product surface must disclose that
the Canonical Transcript, supplied images, and rendered report screenshot may be transmitted to that
Provider. V1.2 does not add a rights taxonomy, consent service, or local/external dual workflow.

The Owner remains responsible for choosing inputs and assets they are permitted to process. Public
release, redistribution, and broader privacy/copyright policy are outside this local V1.2 product
boundary.

## Freshness and correction

Each run binds a fixed input snapshot. If V1.1 later produces a corrected Canonical Transcript, the
Owner starts a new V1.2 run identity; the old report and lineage remain unchanged. V1.2 does not
poll, refresh, or reconcile sources automatically.
