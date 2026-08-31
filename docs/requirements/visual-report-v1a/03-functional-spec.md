# Video Visual Report V1-A — Functional Specification

## Capability inventory

| Capability | Owner component | Requirements |
|---|---|---|
| Load/validate transcript | Existing `VideoSegment` loader adapter | `REQ-VR1A-001`, `006` |
| Build Mapper context | Deterministic context builder | `REQ-VR1A-002`–`004` |
| Generate Topic Map proposal | Topic Mapper model adapter | `REQ-VR1A-002`–`004` |
| Bind/validate Topic Map | Topic Map validator/binder | `REQ-VR1A-003`, `006`, `008` |
| Generate Report Plan proposal | Report Planner model adapter | `REQ-VR1A-002`, `005`, `007` |
| Compile renderer plan | Proposal validator/compiler | `REQ-VR1A-006`–`011` |
| Trace run/model calls | Local run recorder | `REQ-VR1A-012`, `013` |
| Render HTML | Existing V0 renderer | `REQ-VR1A-010`, `015` |
| Review three product reports | V1-A prototype reviewer + human cards | `REQ-VR1A-021`, `022` |

## Task catalog

| Task ID | Trigger | Input → output | Side effect | Completion | Failure/retry | Evidence |
|---|---|---|---|---|---|---|
| `TASK-VR1A-BUILD` | Explicit CLI | Manifest + segments → complete run directory | External text calls; local files | Two semantic stages, validated plan, rendered HTML | At most one eligible identical technical retry per run | Run/attempt manifest, call trace, artifacts |
| `TASK-VR1A-MAP` | Build enters mapping | Full transcript → semantic Topic Map proposal/canonical map | One model call, or two when the run spends its technical retry here | At least one grounded usable topic; diagnostics emitted | Semantic failure stops before Planner; eligible technical failure may retry once | Raw/canonical map + normalization/attempt evidence |
| `TASK-VR1A-PLAN` | Canonical map exists | Full transcript + map → semantic proposal/compiled V0 plan | One model call, or two when the run's unused retry is spent here | Grounding/current V0 contract passes without semantic rewriting/merge/split | Semantic failure stops before renderer; eligible technical failure may retry once | Raw proposal/compiler ledger/compiled plan |
| `TASK-VR1A-RENDER` | Compiled plan exists | Plan + empty assets → HTML | Reuses local renderer | Renderer exits successfully | Existing renderer failure semantics | HTML + render summary |
| `TASK-VR1A-REVIEW` | Frozen config + review cards | Three run directories + HTML/screenshots → prototype review package | Local review files only | All attempts/diagnostics retained; three content/visual rubrics pending Owner | No schema-first-hit promotion or selective replacement | Prototype aggregate, rubrics, screenshots |

## Semantic input contracts

| Input ID/version | Producer/purpose | Required shape | Limits | Validation/authorization | Duplicate/order | Invalid behavior |
|---|---|---|---|---|---|---|
| `IN-VR1A-TRANSCRIPT/VideoSegment-v1` | Existing ingest; decision source | JSONL rows with video/segment IDs, consecutive ordinal, `[start_ms,end_ms)`, text, ASR provenance | Chinese technical/knowledge video; ≤80 segments and ≤50,000 Unicode characters; named fixture exceptions within these limits | Existing Pydantic + `validate_video_segments`; full external processing Owner-authorized | Unique IDs/ordinals; chronological non-overlap | Fail before model call |
| `IN-VR1A-MANIFEST/ingest-v1` | Existing ingest; metadata/rights | Video ID, duration, title/source/attribution/use basis | Exactly one video matching transcript | JSON object and cross-file ID/duration checks | One manifest | Fail before model call |
| `IN-VR1A-MODEL-CONFIG/v1` | Local operator/environment | Explicit provider endpoint if non-default, model, API/response mode, timeout, prompt versions, credential-present boolean | One frozen tuple for all three product runs; `thinking.type=enabled`; `reasoning_effort=high`; `max_tokens=32768`; SDK retry zero; application retry budget one per run | Secrets remain environment-only; the adapter must send and trace the actual DeepSeek controls; temperature may be recorded but is not stability evidence because Thinking mode ignores it | Immutable inside the three-video product set and both attempts | Configuration error or request/config snapshot mismatch |
| `IN-VR1A-REVIEW-CARD/v1` | Human reviewer before product build | Must-cover topics, optional topics, known ASR traps, prohibited claims, source IDs, content/visual rubric | One card per fixed video | Source IDs validated; card revision frozen before product runs | Unique video ID | Product set cannot start |

### Valid, boundary, and invalid transcript examples

- Valid: one of the three existing JSONL files with 38–46 ordered segments.
- Boundary: 80 valid segments and exactly 50,000 Unicode characters.
- Invalid: overlapping segments, missing provenance, mixed video IDs, blank text,
  50,001 characters, or an absent/contradictory manifest.

## Topic Mapper output contract

### Raw model contract: `OUT-VR1A-TOPIC-PROPOSAL/v1a-prototype`

The model emits JSON only. It does not emit topic IDs, timestamps, report
importance, renderer block types, layout, or confidence percentages.

```json
{
  "schema_version": "visual-topic-map-proposal.v1a-prototype",
  "topics": [
    {
      "title": "为什么真实交互不可替代",
      "summary": "离线数据存在部署分布偏差，在线交互用于继续更新策略。",
      "source_segment_ids": [
        "p0b-rlinf-2026-seg-001",
        "p0b-rlinf-2026-seg-002"
      ],
      "subtopics": [
        {
          "title": "离线与在线",
          "summary": "两种学习数据来源承担不同作用。",
          "source_segment_ids": ["p0b-rlinf-2026-seg-001"]
        }
      ]
    }
  ],
  "exclusions": [
    {
      "segment_id": "p0b-rlinf-2026-seg-045",
      "reason": "closing_housekeeping"
    }
  ]
}
```

Rules:

- `topics`: 4–12, ordered by first source ordinal.
- Each topic title: 1–60 characters; summary: 1–240 characters.
- Each topic owns 1–12 consecutive primary segment IDs. If a theme returns
  later, emit a new ordered topic instance.
- `subtopics`: 0–5; their IDs must be a subset of their parent topic IDs.
- Every input segment appears exactly once in a primary topic or exclusion.
- Exclusion reason is one of `opening_housekeeping`, `closing_housekeeping`,
  `off_topic`, `duplicate`, or `unintelligible`.
- A segment with substantive technical content may not be excluded merely to
  reduce topic count.

### Canonical contract: `OUT-VR1A-TOPIC-MAP/v1a-prototype`

Deterministic binding generates `topic-001` style IDs, replaces each selected
segment ID with the exact stored `SourceRef`, computes topic boundaries from
those refs, and records coverage counts. No model-authored timestamp survives.

```json
{
  "schema_version": "visual-topic-map.v1a-prototype",
  "video_id": "p0b-rlinf-2026",
  "topics": [
    {
      "topic_id": "topic-001",
      "title": "为什么真实交互不可替代",
      "summary": "离线数据存在部署分布偏差，在线交互用于继续更新策略。",
      "start_ms": 46400,
      "end_ms": 142300,
      "source_refs": [
        {"segment_id": "p0b-rlinf-2026-seg-001", "start_ms": 46400, "end_ms": 94000},
        {"segment_id": "p0b-rlinf-2026-seg-002", "start_ms": 94000, "end_ms": 142300}
      ],
      "subtopics": []
    }
  ],
  "exclusions": [],
  "coverage": {"input_segment_count": 46, "mapped_count": 46, "excluded_count": 0}
}
```

## Report Planner output contract

### Raw model contract: `OUT-VR1A-PLAN-PROPOSAL/v1a-prototype`

```json
{
  "schema_version": "visual-report-plan-proposal.v1a-prototype",
  "hero": {
    "title": "从交互必要性到算法驱动的系统设计",
    "tldr": "报告先解释在线强化学习为何必要，再说明系统如何承接算法和真实世界约束。",
    "source_segment_ids": [
      "p0b-rlinf-2026-seg-001",
      "p0b-rlinf-2026-seg-012"
    ]
  },
  "sections": [
    {
      "title": "为什么离线学习仍不够",
      "topic_ids": ["topic-001"],
      "blocks": [
        {
          "type": "comparison_card",
          "headline": "离线给起点，在线补能力边界",
          "left": {"label": "离线", "items": ["使用既有数据", "部署存在分布偏差"]},
          "right": {"label": "在线", "items": ["持续环境交互", "根据新反馈更新策略"]},
          "source_segment_ids": ["p0b-rlinf-2026-seg-001"]
        },
        {
          "type": "insight_card",
          "headline": "无交互，不理解",
          "body": "真实环境中的试错是具身策略扩展能力边界的必要来源。",
          "source_segment_ids": ["p0b-rlinf-2026-seg-002"]
        }
      ]
    }
  ],
  "omitted_topics": [
    {"topic_id": "topic-010", "reason": "secondary_detail"}
  ]
}
```

### Allowed Planner block payloads

Every block has `type` and 1–4 `source_segment_ids`. The allowed content fields
match the current V0 schema:

| Type | Required content | Affordance gate |
|---|---|---|
| `insight_card` | `headline`, `body` | One source-supported central inference/consequence |
| `bullet_group` | `headline`, 2–5 parallel items | Items share one level and are not a disguised process |
| `metric_row` | `headline`, 2–4 value/label/context items | Every displayed value appears in cited transcript text after whitespace normalization |
| `comparison_card` | `headline`, left/right labels and 1–4 items | Source contains a real two-sided contrast |
| `process_flow` | `headline`, 3–6 ordered title/body steps | Source supports temporal, causal, or operational order |
| `takeaway_box` | `headline`, 2–5 takeaways | Final synthesis only; each takeaway is grounded |

`image_caption` is prohibited in V1-A. No type is required merely for visual
variety.

### Planner budgets and completeness

- 3–5 sections; 2–4 blocks per section; 8–14 blocks total.
- Exactly one final `takeaway_box`; no more than one `insight_card` per section.
- Report-visible authored content is at most 2,600 Unicode characters before
  renderer metadata.
- Every Topic Map topic is included in a section or appears once in
  `omitted_topics` with `secondary_detail`, `redundant`, `housekeeping`, or
  `out_of_budget`.
- Section topic IDs are unique across sections; a cross-topic synthesis may cite
  multiple topics inside one section.
- Every block source segment belongs to one of its section's topics.
- Hero sources may span selected topics; hero fields are retained in the
  proposal evidence even though the current renderer Hero has no source field.

## Deterministic compilation contract

The compiler must:

1. validate raw JSON with `extra="forbid"` contracts;
2. resolve every topic/segment ID against canonical inputs;
3. generate sequential `section-01`/`block-01-01` IDs and numeric kickers;
4. set each section timestamp to the earliest cited block source;
5. copy video metadata from the manifest, never the model;
6. bind every block to exact stored `SourceRef` values;
7. enforce current field/list/string budgets and the V1-A aggregate budgets;
8. reject metric values absent from cited transcript text;
9. create the current `visual-report.v0-prototype` plan and
   `visual-report-assets.v0-prototype` empty manifest;
10. validate both through the current V0 Pydantic models before rendering.

It may normalize JSON serialization and surrounding whitespace. It may not
rewrite claims, invent a ref, remove an invalid block, change a block type,
truncate content, add a third model call, or substitute a manual plan.

## Current semantic-v2 product contract

The v1 contracts above remain the frozen meaning of every historical run. The
Owner cancelled the unexecuted official-OpenAI isolation proposal and then
confirmed a DeepSeek-first product-prototype contract in `DEC-VR1A-061`. The
full normative task is
[`VR-V1A-CONTRACT-SIMPLIFICATION-006`](../../tasks/VISUAL-REPORT-V1A-CONTRACT-SIMPLIFICATION.md);
it was subsequently implemented at `844978f08d07775b650467e31e221a969ddef3e3`.
Its first frozen product set rendered RLinf and Wu Yi but exhausted Kling's
single retry on `finish=length`, so it remains
`PROTOTYPE_EXECUTION_INCONCLUSIVE`. `DEC-VR1A-062` now controls only the next
complete three-video runtime revision: Thinking enabled, reasoning effort
high, `max_tokens=32768`, and one identical retained retry. It does not rewrite
the earlier attempt or change the semantic-v2/compiler contract below.

The current version adds:

- `OUT-VR1A-TOPIC-PROPOSAL/visual-topic-map-proposal.v1a-semantic-v2`, whose
  topics contain title, summary, importance, start/end segment IDs, and
  representative segment IDs without exact partition/exclusion/subtopic rules;
- a deterministic Topic Resolver that removes unknown/duplicate IDs, expands
  valid spans, generates IDs/times/refs, and reports overlap/uncovered segments;
- `OUT-VR1A-PLAN-PROPOSAL/visual-report-plan-proposal.v1a-semantic-v2`, whose
  sections contain flat content units and advisory block-type hints rather than
  the final discriminated typed-block union; and
- `OUT-VR1A-NORMALIZATION/visual-report-normalization.v1a-semantic-v2`, an
  ordered raw-to-canonical governance ledger recording rule, path,
  before/after counts or hashes, reason, and whether a whole unit was omitted
  or structurally mapped.

Allowed v2 normalization is syntactic, referential, or structural only: trim
whitespace, apply optional empty presentation defaults, discard unknown fields,
deduplicate/remove unknown IDs, resolve topic spans, assign canonical
identity/time/refs, map complete supplied shapes to compatible existing block
types, omit whole unusable units with evidence, and validate current V0 limits.
It may not truncate semantic text or rewrite, merge, split, shorten, expand, or
synthesize semantic units. No usable topic, fewer than three grounded content
units, fewer than three or more than five usable supplied sections, or any need
for semantic transformation remains a product-pipeline failure.
At the product-set level, valid transport/JSON followed by this insufficiency
maps to `PROTOTYPE_CONTENT_INSUFFICIENT`, not to a technical-inconclusive state.

The v2 compiler must not fabricate a claim, source, metric, comparison side,
process meaning, or missing block. Every final block and Hero retain at least
one valid model-selected segment ID; topic spans cannot silently replace all
missing block evidence. Historical v1 `no repair` evidence is not relabeled.
One identical technical retry per run is allowed only for the API/JSON anomaly
categories in the task card; valid semantic output is never retried for quality.

## Semantic output contracts

| Output ID | Consumer/purpose | Completion/quality | Provenance/control | Partial/failure behavior |
|---|---|---|---|---|
| `OUT-VR1A-TOPIC-MAP` | Planner/reviewer; global semantic map | At least one usable topic; span/representative coverage, uncovered and overlap diagnostics | Full refs + prompt/model/run versions | No usable map stops before Planner |
| `OUT-VR1A-PLAN-PROPOSAL` | Compiler/reviewer; model's editorial proposal | Shallow semantic sections/units with grounded IDs | Raw response retained; source IDs visible | Diagnostic only if compile fails |
| `OUT-VR1A-REPORT-PLAN` | Existing renderer | Current V0 schema; budgets/refs pass | Deterministic compiler version | Absent on invalid proposal |
| `OUT-VR1A-HTML` | Owner; local reading | Existing renderer succeeds | Plan/assets/run lineage | Absent on any upstream failure |
| `OUT-VR1A-VISUAL-REVIEW` | Owner; product judgment | 1080 px and approximately 390 px screenshots plus visible QA observations | HTML/run/viewport lineage | Absent when report does not render |
| `OUT-VR1A-PROTOTYPE-REVIEW` | Owner; V1-A product decision | Three reports, content/visual rubrics and cross-video comparison | All attempts and diagnostics retained | Technical absence is technical-inconclusive; valid but unusable semantic output is content-insufficient |
| `OUT-VR1A-RUN-MANIFEST` | Operator/evaluator | Terminal state, versions, counts, timings, usage, paths | Append-oriented run identity | Always present after run creation when filesystem permits |
| `OUT-VR1A-ERROR` | Operator | Stable category + affected stage/ID, no credential/content dump | Retained in manifest/diagnostics | Non-zero exit |

## Canonical state authority and transitions

`run.json` inside the unique run directory is the authority for one execution.
Artifacts cannot advance state merely by existing.

| State | Allowed work | Exit guard | Failure destination |
|---|---|---|---|
| `CREATED` | Validate config/source | Inputs/config valid | `FAILED`/`CANCELLED` |
| `MAPPING` | Mapper attempt 1 and, if eligible, attempt 2 | Canonical Topic Map passes; run retry budget ≤1 | `FAILED`/`CANCELLED` |
| `TOPIC_MAPPED` | Assemble Planner context | Planner request admitted | `FAILED` |
| `PLANNING` | Planner attempt 1 and, if the run budget remains and failure is eligible, attempt 2 | Proposal compiles to V0 plan without semantic transformation | `FAILED`/`CANCELLED` |
| `PLAN_VALIDATED` | Render through V0 | Renderer succeeds | `FAILED` |
| `RENDERED` | Record completion | Call count is 2 or 3; retry ledger is consistent; artifacts complete | `FAILED` |
| `FAILED` | Preserve diagnostics | Terminal | None |
| `CANCELLED` | Preserve any completed stage | Terminal | None |

Product acceptance is a separate human-owned status; a `RENDERED` run is
not automatically a quality pass.

## Error taxonomy

- `CONFIGURATION_ERROR`
- `SOURCE_NOT_FOUND`
- `TRANSCRIPT_SCHEMA_ERROR`
- `MANIFEST_MISMATCH`
- `INPUT_TOO_LARGE`
- `PROVIDER_ERROR`
- `PROVIDER_TIMEOUT`
- `MODEL_OUTPUT_PARSE_ERROR`
- `TOPIC_MAP_SCHEMA_ERROR`
- `SEGMENT_ACCOUNTING_ERROR`
- `UNKNOWN_SOURCE_REFERENCE`
- `PLAN_PROPOSAL_SCHEMA_ERROR`
- `TOPIC_SELECTION_ERROR`
- `UNSUPPORTED_METRIC`
- `PLAN_BUDGET_ERROR`
- `V0_PLAN_COMPILATION_ERROR`
- `RENDER_ERROR`
- `OUTPUT_IO_ERROR`
- `CANCELLED`

Only connection/timeout/HTTP `429`/provider `5xx`, empty content,
provider-declared incomplete/truncated output, or malformed non-decodable JSON
may spend the run's single technical retry. The retry repeats the current stage
with identical request/configuration and retains both attempts. Valid JSON with
weak/invalid semantics, grounding, or V0 incompatibility is non-retryable.

## Configuration, ordering, concurrency, and idempotency

- Prompt versions, model, endpoint label, Thinking controls, reasoning effort,
  output ceiling, timeout, temperature trace value, and maximum input envelope
  are fixed at run creation. Temperature is not stability evidence in the
  frozen Thinking mode.
- Calls are sequential and one run owns two base calls plus at most one
  eligible technical retry, for at most three admitted calls.
- Concurrency is one local run. No lock/queue is added beyond rejecting an
  existing run directory.
- Repeating the whole command requires a new run ID; the one in-run retry keeps
  the same run and gains a distinct attempt ID. Model output is not claimed to
  be byte-deterministic.
- The compiler and renderer remain deterministic for identical validated inputs.

## Roles and permissions

| Action | Role | Allowed | Condition |
|---|---|---|---|
| Read the three transcript/manifests | Owner/implementer | Yes | Read-only |
| Send full transcript text to configured provider | Local operator | Yes | Explicit V1-A authorization; no private data expected |
| Change prompt/model/config | Implementer | Yes before a new product-set revision | Invalidates the current three-video set; rerun all fixtures only under new Owner authority |
| Publish media/report | Any | No for current restricted fixtures | Separate rights authorization required |
| Accept V1-A / authorize V1-B | Owner only | Yes | After reviewing evidence; separate decisions |

## Notifications, background behavior, and feature flags

Not applicable — all work is one foreground CLI invocation. There is no worker,
callback, notification, feature flag, provider fallback, or hidden retry. The
single explicit application retry is synchronous and attempt-recorded.
