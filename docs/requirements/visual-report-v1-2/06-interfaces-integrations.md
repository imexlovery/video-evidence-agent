# Interfaces and Integrations

## Integration map

| Interface | Direction | V1.2 contract | Failure behavior |
|---|---|---|---|
| V1.1 Canonical Transcript | input | complete validated transcript and manifest | reject before model use |
| existing MP4/Bilibili ingest | upstream shared infrastructure | may produce the V1.1 input; not redesigned | preserve upstream failure and do not start V1.2 |
| local CLI | user control | explicitly select V1.2, start run, report path/outcome | non-zero result with concise reason |
| local Web | user control/status | start/select V1.2, show understandable progress/outcome, open report | show failure/limitation; never expose key |
| Provider Adapter | model I/O | one run-level configuration and typed role calls | one shared run-level eligible identical retry; no fallback |
| local filesystem | Artifact I/O | unique Run Bundle and validated supplied assets | atomic failure evidence; no partial delivery |
| Renderer | internal deterministic | valid Presentation Plan to HTML | `FAILED` after finite identical operation retry |
| Browser Observer | internal deterministic | local HTML to 1080px screenshot/DOM evidence | `FAILED` after finite identical operation retry |

## User entry points

V1.2 MUST be an explicit versioned run choice. It MUST NOT silently replace `build-from-transcript-v2`
or current Web behavior during implementation calibration. CLI command/flag spelling and the
smallest Web selector are implementation mechanics, but they must satisfy:

- legacy and V1.2 run identities cannot collide;
- the selected path is recorded in the Run Bundle and visible to the Owner;
- no automatic fallback occurs in either direction;
- Web copy uses user-understandable stages rather than internal role names where possible;
- `COMPLETE` and `DEGRADED` expose the Candidate Report; `FAILED` exposes diagnostics but no invalid
  report as deliverable;
- the Web Shell itself is outside the report visual-quality gate.

Existing single-process FIFO behavior may remain shared for URL ingestion. V1.2 introduces no new
concurrency service, distributed queue, or background orchestration system.

## Input contract: Canonical Transcript

| Property | Contract |
|---|---|
| Producer | V1.1 Transcript Foundation or compatible retained V1.1 Artifact |
| Required | yes |
| Encoding | UTF-8 JSONL plus manifest according to the current V1.1 schema |
| Locale | current product target is Chinese long-form video |
| Envelope | complete content, maximum 50,000 Unicode characters |
| Validation | manifest/schema, unit IDs, non-empty canonical text, source status/provenance availability |
| Invalid input | fail before model call; oversize uses `INPUT_TOO_LARGE` |
| Ordering | unit order and timestamps come from V1.1 and are not reordered in the source snapshot |
| Mutation | prohibited |

V1.2 reads `TranscriptUnit.unit_id`, `start_ms`, `end_ms`, `canonical_text`, `resolution`, `flags`,
and `provenance`. It may retain `asr_text`, `ocr_text`, and `subtitle_text` for inspection, but source
selection remains the V1.1 Canonical Transcript decision.

## Input contract: Visual Asset Set

| Property | Contract |
|---|---|
| Producer | named local Owner or existing local workflow |
| Required | no; empty is valid |
| Content | local supported image files plus stable ID, media type, source context, and semantic description/binding |
| Validation | manifest schema, unique IDs, safe local path resolution, readable supported format |
| Allowed influence | placement, binding, and visual weight for existing Editorial content |
| Forbidden influence | new factual Claim, automatic discovery, extraction, search, or generation |
| Invalid asset | reject that supplied set before Presentation; do not guess or fetch a replacement |

## Model Provider interface

The existing environment contract is reused:

- `OPENAI_API_KEY`: required secret; value never persisted or displayed;
- `OPENAI_BASE_URL`: OpenAI-compatible endpoint;
- `VIDEO_EVIDENCE_MODEL`: the single run model;
- `VISUAL_REPORT_TIMEOUT_SECONDS`: call timeout.

The current reference configuration points to the Zhipu OpenAI-compatible endpoint and
`glm-5.3-flash`. V1.2 code MUST depend on the unified project ModelClient/Provider Adapter, not SDK
calls inside stage implementations.

Each logical call supplies:

- role/capability name;
- Prompt version and system instruction;
- explicit input Artifact snapshot;
- requested response Schema;
- the shared run model configuration;
- multimodal parts only when supplied assets or the rendered screenshot are authorized inputs.

Each result records complete/incomplete response status, raw response in the protected local Run
Bundle when safe, parsed Artifact or validation error, token/usage metadata when supplied by the
Provider, timing, and retry linkage. A complete invalid response is not retried or replaced.

## Renderer interface

Input:

- one valid Editorial Plan snapshot;
- one valid Presentation Plan that references it;
- the active Design System/Vocabulary version;
- validated referenced assets and report metadata.

Output:

- canonical UTF-8 `report.html`;
- deterministic render summary and trace from rendered regions to Presentation placements and
  Editorial Content Units.

The Renderer accepts no free-form executable model output. Content is escaped. It must not access
the network.

## Browser Observer interface

Input:

- local canonical `report.html`;
- exactly the supported desktop viewport configuration, width 1080px;
- stable element trace identifiers emitted by the Renderer.

Output:

- full-page screenshot;
- viewport/page dimensions;
- basic traced-element geometry;
- overflow and clipping indicators;
- observation runtime/version and success evidence.

The Observer API exposes no click, navigation, external URL, script-injection, DOM-mutation, or
repair command to the model. The repository currently has no browser automation dependency in
`pyproject.toml`; selection and addition of the smallest suitable local dependency belongs to the
separately authorized implementation.

## Run status interface

User-facing status MUST distinguish:

- accepted/queued or currently running;
- the broad capability in progress;
- terminal `COMPLETE`, `DEGRADED`, or `FAILED`;
- concise limitation/failure reason;
- whether a Candidate Report can be opened.

Internal role calls need not become product states. The canonical status comes from the Controller
run record, not from thread liveness, file existence, or browser success alone.

## External data and outage behavior

The model Provider is V1.2's only new external processing boundary. A model outage may consume the
one shared eligible identical retry and then fails the run; there is no offline model substitution. Local
Renderer and Browser Observer failures cannot be masked by stale HTML or stale Observation.

The local Web server, filesystem, and browser process are bounded-owner dependencies rather than
production services. V1.2 makes no availability or latency service promise.

## Compatibility and version negotiation

- V1.2 rejects an unsupported Canonical Transcript schema rather than coercing it.
- Every V1.2 Artifact carries or is bound to a schema/version identity.
- The legacy `ReportPlan` and seven block union are not accepted as V1.2 Presentation contracts.
- Reused legacy component code remains private to the Renderer and does not constrain the new
  public Artifact shape.
- A later schema migration must be explicit; silent legacy fallback is forbidden.
