# Video Visual Report V1-A — Data and Memory

## Data principles

- Existing manifests and `VideoSegment` JSONL are read-only sources of truth.
- Models select existing IDs; deterministic code owns canonical identity/time.
- Topic Map, model proposal, compiled plan, and renderer output are different
  artifact classes and may not impersonate one another.
- Every run has a unique local identity; failures remain in evidence.
- No database, cache, conversation memory, vector index, or Agent memory exists.
- Full transcript external processing is explicitly authorized and contains no
  expected private data; current publication restrictions still apply.

## Existing asset and store inventory

| Asset ID/status | Location/access | Owner | Format/scale/status | Rights/privacy/change | Reuse/gap/lifecycle |
|---|---|---|---|---|---|
| `ASSET-VR1A-KLING-TRANSCRIPT / AVAILABLE` | `artifacts/p0b-ingest/p0b-kling-2024/segments.jsonl` | Owner/P0-B ingest | 43 `VideoSegment` rows; 2,022,421 ms; about 21k JSONL chars | No expected private data; full text external processing authorized; media/report remain local/non-public | Reuse read-only; create review card; preserve source |
| `ASSET-VR1A-RLINF-TRANSCRIPT / AVAILABLE` | `artifacts/p0b-ingest/p0b-rlinf-2026/segments.jsonl` | Owner/P0-B ingest | 46 rows; 2,093,120 ms; about 25k JSONL chars | Same authorization; no source overwrite | Reuse read-only; V0 plan is development reference |
| `ASSET-VR1A-WUYI-TRANSCRIPT / AVAILABLE` | `artifacts/p0b-ingest/p0b-wuyi-goals/segments.jsonl` | Owner/P0-B ingest | 38 rows; 1,763,207 ms; about 19k JSONL chars | Same authorization; no source overwrite | Reuse read-only; create review card |
| `ASSET-VR1A-MANIFESTS / AVAILABLE` | Matching `manifest.json` plus `eval/p0b/corpus.jsonl` | P0-B corpus | JSON/JSONL metadata, attribution, use basis | Authority for title/duration/rights; read-only | Reuse; conflict blocks run |
| `ASSET-VR1A-V0-PLAN / AVAILABLE` | `artifacts/visual-report/v0-rlinf/report-plan.json` | V0 Owner | 4 sections, 13 blocks | Local development reference; not automatic Gold | Human comparison only |
| `ASSET-VR1A-RENDERER / AVAILABLE` | `src/video_evidence_agent/visual_report/` | Repository | Current V0 Pydantic/HTML contract | Preserve behavior | Reuse unchanged |
| `ASSET-VR1A-REVIEW-CARDS / AVAILABLE` | `eval/visual-report-v1a/review-cards/` | Implementer created; Owner reviews | Three versioned small JSON cards; current human rubrics remain pending | Derived locally from authorized transcripts | Validate and snapshot unchanged into any new formal revision |
| `ASSET-VR1A-HISTORICAL-RUNS / AVAILABLE_IMMUTABLE` | `artifacts/visual-report/v1a/` plus `eval/visual-report-v1a/` manifests | V1-A recorder/evaluator | Three historical formal revisions, 22 recovery candidate manifests, 20 failed recovery canaries | Local restricted evidence; no public redistribution | Preserve every identity/aggregate/rubric; create only new unique strategy/canary/formal identities |
| `STORE-VR1A-DATABASE / NOT_APPLICABLE` | None | None | None | No G1 need | Must not add |
| Brand/creative assets | Not applicable | None | None | V1-A creates no visual identity | Existing renderer retained |

Comma-free duration values in source manifests are authoritative. Human-readable
formatting must not alter stored values.

## Conceptual data model

```text
VideoManifest 1 ── 1 TranscriptSnapshot
TranscriptSnapshot 1 ── * VideoSegment
PlanningRun 1 ── 2 ModelCallTrace
PlanningRun 1 ── 1 TopicMapProposal ──compile──> TopicMap
TopicMap 1 ── 1 ReportPlanProposal ──compile──> V0 ReportPlan
V0 ReportPlan + EmptyAssetManifest ──render──> report.html
PlanningRun 1 ── * RunEvent
MeasurementRevision 1 ── 6 PlanningRun
MeasurementRevision 1 ── 3 ReviewCard
```

## Data dictionary

| ID | Field/entity | Type/owner | Sensitivity | Authority |
|---|---|---|---|---|
| `DATA-VR1A-RUN-ID` | Explicit unique slug | Operator/run recorder | None | Run directory name + `run.json` |
| `DATA-VR1A-SOURCE-REF` | Existing segment ID + exact stored times | Source binder | None | Transcript snapshot |
| `DATA-VR1A-TOPIC-ID` | Sequential `topic-NNN` | Binder | None | Canonical Topic Map |
| `DATA-VR1A-PLAN-ID` | Sequential section/block IDs | Compiler | None | Compiled V0 plan |
| `DATA-VR1A-PROMPT-REV` | Mapper/Planner prompt version | Repository | None | Versioned prompt source |
| `DATA-VR1A-MODEL-REV` | Provider label + explicit model name | Run config | Operational | `run.json` |
| `DATA-VR1A-USAGE` | Provider token/usage payload when present | Provider trace | None | `model-calls.jsonl`; absence is `{}` |
| `DATA-VR1A-COST` | Monetary cost | Derived only with authoritative price | None | `unavailable` when pricing/usage cannot prove it |
| `DATA-VR1A-MEASUREMENT` | Per-run deterministic/human scores | Evaluation harness/Owner | None | Versioned evaluation report |

## Data-source register

| Source ID/category | Owner/authority/rights | Contract/coverage/quality | Trust/freshness | Transformation/lineage | Failure/reconciliation | Lifecycle |
|---|---|---|---|---|---|---|
| `SRC-VR1A-SEGMENTS / first-party artifact` | Owner; external text processing explicitly authorized | Complete ASR coverage, 38–46 stable segments; recognition/numeric errors possible | Frozen local snapshot; transcript text is untrusted data | JSONL → validated segment list → two prompt contexts → bound refs | Invalid source stops; source artifact overrides model | Read-only |
| `SRC-VR1A-MANIFEST / first-party metadata` | P0-B corpus authority for identity/duration/attribution/use | One per video | Frozen; conflict blocks | Manifest fields copied deterministically into final plan/run | Corpus/manifest outrank model/proposal | Read-only |
| `SRC-VR1A-MODEL / derived proposal` | Configured provider; advisory only | Variable structured output | Prompt/model/provider revision recorded | Raw JSON → strict schema → bind/compile | Never outranks transcript; invalid output fails | Retained with run |
| `SRC-VR1A-REVIEW-CARD / human evaluation` | Implementer drafts; Owner is acceptance authority | Must-cover/optional/prohibited cases for one source snapshot | Frozen before measured prompt runs | Source IDs → evaluation labels → aggregate report | Card/source mismatch blocks measurement | Version controlled |
| `SRC-VR1A-V0-PLAN / development reference` | V0 Owner | One high-quality RLinf plan; authoring bias acknowledged | Fixed reference revision | Human comparison only | Never copied as generated output or universal Gold | Read-only |

## Primary lineage

```text
manifest + VideoSegment JSONL
→ source validation and snapshot hashes
→ full ordered Mapper context
→ raw Topic Map proposal
→ deterministic segment accounting and SourceRef binding
→ canonical topic-map.json
→ full ordered Planner context + Topic Map + renderer grammar
→ raw Report Plan proposal
→ deterministic topic/source/budget/metric validation
→ current V0 report-plan.json + empty assets.json
→ existing renderer
→ report.html
→ deterministic metrics + human review cards
→ Development measurement conclusion
```

## Run artifact layout

```text
artifacts/visual-report/v1a/<run-id>/
├── run.json
├── events.jsonl
├── model-calls.jsonl
├── topic-map.raw.json
├── topic-map.json
├── report-plan.raw.json
├── report-plan.json
├── assets.json
├── validation.json
└── report.html
```

- `run.json` records source paths/hashes, schema/prompt/model versions, state,
  call counts, artifact paths, timings, usage, and `cost` or `unavailable`.
- SHA-256 is required only for the exact source/prompt/structured artifacts used
  by a measured run so results can be tied to a snapshot; it is not a general
  repository-integrity exercise.
- Raw response files may be absent when a provider fails before returning body.
- `report.html` exists only for a successfully validated/rendered run.
- No transcript duplicate or complete rendered prompt is stored; the source
  hash, prompt revision, and structured context contract reconstruct the input.

## State and memory classification

| Class | Content | Lifetime/store | Policy |
|---|---|---|---|
| Request context | Parsed CLI paths/config/segments | One process | Discard at exit |
| Session state | Current validated objects/provider response | One process | Discard after artifacts are written |
| Durable application data | Run artifacts and evaluation reports | Owner-controlled local directories | Create once per run; delete by Owner |
| Cache | None | Not applicable | Do not add |
| Audit history | `events.jsonl`, `model-calls.jsonl`, task/status evidence | Repository/run lifetime | Append-oriented; preserve failure |
| Conversation history | None | Not applicable | Do not store |
| Agent working/long-term memory | None | Not applicable | V1-A has no Agent/memory |

## Consistency, correction, and versioning

- A run binds one immutable source/prompt/model/config snapshot at creation.
- Canonical structured artifacts are written atomically and not edited after a
  terminal state. Corrections create a new run.
- A prompt/model/schema/policy change creates a new revision; comparison across
  revisions names both rather than replacing old results.
- If a measured revision changes, all three videos and both repeats are rerun;
  no selective replacement is allowed.
- Existing V0 HTML remains canonical only for V0; each V1-A run's HTML is
  derived from that run's compiled plan.

## Authorization, locality, privacy, and provider lifecycle

The Owner explicitly authorized all three complete transcripts for the external
provider and stated they contain no privacy concern. Credentials remain local.
Provider-side retention is governed by the configured provider and is outside
this local prototype's control; this is an accepted G1 risk, not a privacy or
production claim. Media, frames, reports, and raw artifacts are not publicly
redistributed under current source-use restrictions.

## Retention, deletion, export, backup, and withdrawal

- No automatic expiry. Owner may delete any V1-A run or the entire V1-A artifact
  root; source transcripts remain protected.
- Version-controlled review cards/design/evidence remain unless Owner separately
  directs removal.
- No public export. Local review is allowed.
- No service backup/restore. Code/docs use version control; ignored runs are
  owner-backed-up or reproducible subject to provider/model availability.
- If source processing authorization is withdrawn, stop new runs and delete
  derived V1-A run artifacts for that source; preserve non-content decision
  history where required.

## Information deliberately not stored

Credentials, full request prompts, provider account details, media bytes,
frames, embeddings, retrieval indexes, tool calls, conversation memory,
customer/user profiles, analytics, billing records, or model-training data.
