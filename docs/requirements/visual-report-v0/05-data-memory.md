# Video Visual Report V0 — Data and Memory

## Data principles and source of truth

- Reuse existing P0-B media/transcript read-only; never mutate frozen evidence.
- Separate report content (`report-plan.json`) from media metadata (`assets.json`).
- Keep factual copy traceable through segment IDs and timestamps.
- Keep all new runtime artifacts local under one deletable root.
- Do not add a database, cache, conversation store, or agent memory.
- Rights restrictions travel with every derived frame and report.

## Existing data assets and databases/stores

| Asset ID/status | Asset/database and role | Location/environment/access | Owner | Type/engine/schema/version/format/scale | Quality/sensitivity/rights | Reuse/change/preparation/migration | Backup/restore/lifecycle/delivery |
|---|---|---|---|---|---|---|---|
| `DATA-RLINF-TRANSCRIPT / AVAILABLE` | Authoring evidence | `artifacts/p0b-ingest/p0b-rlinf-2026/segments.jsonl`; local read | Owner | 46 `VideoSegment` JSONL rows; `2093120` ms video | MLX Whisper transcript; public technical talk; wording/numbers may need source verification | Reuse read-only; no migration | Existing P0-B lineage remains unchanged |
| `META-RLINF / AVAILABLE` | Duration, source, attribution, rights | `artifacts/p0b-ingest/p0b-rlinf-2026/manifest.json`, `eval/p0b/corpus.jsonl` | Owner | JSON/JSONL | Authoritative local-use boundary; no open license found | Read-only | Preserve with P0-B corpus |
| `MEDIA-RLINF / AVAILABLE` | Frame source | `eval/p0b/media/2026北京智源大会丨强化学习 p01 面向具身智能的高灵活大规模强化学习框架 RLinf：于超 [BV1KNjz6cEeR_p1].mp4` | Owner | Local MP4, about 34:53 | No expected sensitive personal data; local non-public research only; no redistribution | FFmpeg may create local derived frames; source stays unchanged | Existing local copy; do not duplicate outside bounded artifacts |
| `REF-TUGEKUAI / AVAILABLE` | Visual-direction reference | `/Users/tristana/Desktop/"图个快"效果图.png` | Owner | PNG, 844×3753 original | Reference only; not a distributable asset | Inspect, do not copy into report | Remains outside repository |
| `DATA-REPORT-PLAN / TO_CREATE` | Canonical report content/order | `artifacts/visual-report/v0-rlinf/report-plan.json` | Implementer then owner | Versioned JSON | Hand-authored from source refs; non-sensitive; local | Create/edit/rerender | Retain with prototype or delete root |
| `DATA-ASSETS / TO_CREATE` | Canonical selected-frame metadata | `artifacts/visual-report/v0-rlinf/assets.json` | Implementer then owner | Versioned JSON plus 2–4 JPEGs | Derived from rights-restricted media | Create only selected local frames | Retain/delete with prototype |
| `STORE-DATABASE / NOT_APPLICABLE` | Database | None | None | None | No V0 need | Must not create | None |

## Conceptual data model

```text
VideoMetadata 1 ── 1 ReportPlan
ReportPlan    1 ── * Section
Section       1 ── * ContentBlock
ContentBlock  1 ── * SourceRef
ContentBlock  0..1 ── 1 Asset (by asset_id)
AssetManifest 1 ── * Asset
Asset         1 ── 1 LocalFrame
```

Hero is top-level report metadata. Section Header is derived from each section.
Neither is a free content block. Assets are reusable; an asset may be referenced
by more than one block, although the first report should avoid redundant use.

## Data dictionary

| ID | Entity/field | Type | Owner/tenant | Sensitivity | Source of truth |
|---|---|---|---|---|---|
| `DD-001` | `schema_version` | fixed string | Implementer / no tenant | None | Plan or asset manifest |
| `DD-002` | `report_id` | stable slug | Owner | None | Report plan |
| `DD-003` | `video.duration_ms` | positive integer | P0-B source owner | None | Ingest manifest |
| `DD-004` | `section_id`, `block_id`, `asset_id` | unique stable slug in collection | Implementer | None | Validated JSON |
| `DD-005` | `source_refs[]` | segment ID + `[start_ms,end_ms)` | Content author | None | Plan, checked against transcript/video duration |
| `DD-006` | `asset.path` | contained relative path | Asset author | Local path | Asset manifest |
| `DD-007` | `asset.timestamp_ms` | integer in video range | Asset author | None | Asset manifest/frame extraction |
| `DD-008` | text fields | bounded Unicode string | Content author | Public-talk content | Report plan |
| `DD-009` | report status | enum | Owner/status maintainer | None | `docs/visual-report/V0-STATUS.md` |

## Data-source register

| Source ID/category | Owner/authority/rights | Acquisition/contract | Coverage/quality/trust | Freshness | Transformation/lineage | Failure/reconciliation | Lifecycle |
|---|---|---|---|---|---|---|---|
| `SRC-RLINF-VIDEO / media` | Owner local copy; no open license; local non-public research only | Existing P0-B corpus | Primary visual/audio source | Frozen | MP4 → FFmpeg frame at recorded time | Reinspect source; never infer missing visual fact | Read-only |
| `SRC-RLINF-SEGMENTS / transcript` | Existing P0-B ingest | `VideoSegment` JSONL | Complete ASR coverage but may contain recognition/numeric errors | Frozen | Segment IDs/times → report source refs | Prefer clear frame or cross-segment evidence; omit ambiguous metric | Read-only |
| `SRC-RLINF-MANIFEST / metadata` | P0-B manifest/corpus | JSON/JSONL | Authority for duration, source URL, attribution, rights | Frozen | Copied attribution into report | Manifest overrides authored copy on conflict | Read-only |
| `SRC-HUMAN-PLAN / editorial` | Implementer under owner requirements | Hand author and review | Compression is deliberate, not coverage-complete | Changes per iteration | Source refs → typed blocks → HTML | Owner review; edit plan and rerender | Mutable V0 artifact |

## Primary lineage paths

```text
RLinf MP4 → FFmpeg timestamp extraction → selected JPEG → assets.json
RLinf VideoSegments → manual coverage/read → report selection → source_refs
report-plan.json + assets.json → validation → deterministic renderer → report.html
report.html → browser viewport review → desktop/mobile screenshots → owner decision
```

## State and memory classification

| Class | Content | Lifetime | Store | Read/write policy |
|---|---|---|---|---|
| Request context | CLI paths | One render | Process memory | Read only after parsing |
| Session state | Validated plan/assets and rendered string | One render | Process memory | Discard at exit |
| Durable application data | Plan, assets, HTML, screenshots | Until owner deletes local root | `artifacts/visual-report/v0-rlinf/` | Explicit local create/replace |
| Cache | None | Not applicable | None | Do not add |
| Audit history | Task evidence and V0 status history | Repository lifetime | Version-controlled Markdown | Append status/evidence; preserve failures |
| Conversation history | None at runtime | Not applicable | None | Do not store |
| Agent working memory | None at runtime | Not applicable | None | V0 is A0 |
| Long-term agent memory | None at runtime | Not applicable | None | Durable repo docs replace implicit session memory |

## Read/write paths and consistency

The renderer reads plan/assets fully, validates cross-references and local files,
then renders. The output is written to a temporary sibling and replaces the
requested `report.html` only after success. There is one writer and no database
transaction. The status document changes only after verification; output
existence alone cannot advance status.

## Sources, snapshots, freshness, and authorization

| Source ID | Fact/data | Source/revision | Freshness rule | Stale/unavailable behavior |
|---|---|---|---|---|
| `SRC-RLINF-VIDEO` | Visual frame/audio | Fixed local MP4 from P0-B | Frozen for V0 | Stop; do not download a replacement |
| `SRC-RLINF-SEGMENTS` | Text/timestamps | P0-B ingest manifest using `mlx-community/whisper-small-mlx` | Frozen | Stop or author only from directly inspected source; do not rerun ASR |
| `SRC-RLINF-MANIFEST` | Duration/rights/attribution | Current frozen P0-B corpus | Frozen | Stop if missing or contradictory |
| `SRC-HUMAN-PLAN` | Editorial claims/order | Current validated plan | Rerender after every edit | Old HTML is stale and cannot support a new completion claim |

## Source coverage, quality, bias, conflict, poisoning, and correction propagation

ASR may misrecognize names and numbers; source refs are not proof that wording is
perfect. Verify numeric metrics against a clear frame or multiple transcript
segments. The report may compress and omit secondary topics but must not reverse
the source argument. Authored JSON is untrusted for HTML/path purposes. A
correction updates the plan/assets, rerenders HTML, refreshes screenshots, and
records the new review evidence.

## Artifact manifest and lifecycle

| Artifact ID/type | Source run/input | Producer versions | Hash/validation | Access | Retention/deletion |
|---|---|---|---|---|---|
| `ART-VR0-PLAN / JSON` | Human mapping | Schema `visual-report.v0-prototype` | Pydantic + cross-ref validation; checksum not required | Local owner | Retain/delete with root |
| `ART-VR0-ASSETS / JSON+JPEG` | Fixed MP4/timestamps | Schema `visual-report-assets.v0-prototype`, local FFmpeg | Schema/path/readability and visual inspection; checksum not required | Local owner only | Retain/delete with root; no redistribution |
| `ART-VR0-HTML / HTML` | Valid plan/assets + renderer source | Repository revision recorded in task evidence | Render/test/browser checks | Local owner only | Canonical artifact; reproducible |
| `ART-VR0-SCREENSHOTS / PNG` | Final HTML + named viewports | Local browser version recorded when practical | Visual inspection | Local owner only | Review evidence; regenerate after material change |

## Ownership, tenancy, sharing, and access

One owner, no tenants. Local filesystem permissions govern access. The report,
frames, and screenshots must not be uploaded, deployed, or publicly shared
because the source media is approved only for local non-public research.

## Retention, expiry, deletion, and export

No automated retention or expiry. The owner may delete the entire V0 artifact
root. That deletion is recoverable only if local backups exist, but the report can
be regenerated while fixed sources and implementation remain. Export beyond the
local artifact root is prohibited for this fixture.

## Consent revisions, withdrawal propagation, and protected records

No personal-data consent workflow is applicable. If source-use authorization is
withdrawn, delete the derived V0 artifact root and stop using the fixture while
preserving only non-media project decision history as required.

## Encryption, locality, privacy, and compliance

No new encryption layer is added. Existing local disk protections apply. Media,
frames, content, and HTML remain local. No telemetry, remote model, remote font,
or network storage is used.

## Backup, restore, migration, versioning, and conflict resolution

No migration or service backup is required. Schema versions are explicit. Source
code/docs are version controlled; `artifacts/` is intentionally local/ignored.
The owner message and P0-B manifest outrank authored plan metadata on conflict.
Regenerate derived artifacts after compatible changes rather than hand-editing
the HTML.

## Cache keys, validity, and invalidation

No cache exists. A plan, asset manifest, asset file, or renderer change requires
an explicit rerender and refreshed visual screenshots.

## Information deliberately not stored

User accounts, credentials, analytics, viewing history, raw audio duplicates,
model prompts/responses, embeddings, retrieval indexes, OCR text, VLM captions,
agent traces, queues, and report-publication metadata.
