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
| Measure three videos | V1-A evaluation harness + human cards | `REQ-VR1A-014`, `016` |

## Task catalog

| Task ID | Trigger | Input → output | Side effect | Completion | Failure/retry | Evidence |
|---|---|---|---|---|---|---|
| `TASK-VR1A-BUILD` | Explicit CLI | Manifest + segments → complete run directory | External text calls; local files | Two calls, validated plan, rendered HTML | No automatic retry; explicit new run ID | Run manifest/call trace/artifacts |
| `TASK-VR1A-MAP` | Build enters mapping | Full transcript → Topic Map proposal/canonical map | One model call | Segment accounting passes | Failure stops before Planner | Raw/canonical map + validation |
| `TASK-VR1A-PLAN` | Canonical map exists | Full transcript + map → proposal/compiled V0 plan | One model call | Grounding/budget/V0 schema pass | Failure stops before renderer | Raw proposal/compiled plan |
| `TASK-VR1A-RENDER` | Compiled plan exists | Plan + empty assets → HTML | Reuses local renderer | Renderer exits successfully | Existing renderer failure semantics | HTML + render summary |
| `TASK-VR1A-MEASURE` | Frozen config + review cards | Six run directories → evaluation report | Local evaluation files only | All attempts scored and retained | No selective replacement | Measurement JSON/Markdown |

## Semantic input contracts

| Input ID/version | Producer/purpose | Required shape | Limits | Validation/authorization | Duplicate/order | Invalid behavior |
|---|---|---|---|---|---|---|
| `IN-VR1A-TRANSCRIPT/VideoSegment-v1` | Existing ingest; decision source | JSONL rows with video/segment IDs, consecutive ordinal, `[start_ms,end_ms)`, text, ASR provenance | Chinese technical/knowledge video; ≤80 segments and ≤50,000 Unicode characters; named fixture exceptions within these limits | Existing Pydantic + `validate_video_segments`; full external processing Owner-authorized | Unique IDs/ordinals; chronological non-overlap | Fail before model call |
| `IN-VR1A-MANIFEST/ingest-v1` | Existing ingest; metadata/rights | Video ID, duration, title/source/attribution/use basis | Exactly one video matching transcript | JSON object and cross-file ID/duration checks | One manifest | Fail before model call |
| `IN-VR1A-MODEL-CONFIG/v1` | Local operator/environment | Explicit provider endpoint if non-default, model, timeout, prompt versions, credential-present boolean | One provider/model; temperature 0; no hidden retry | Secrets remain environment-only; model must support the input envelope and JSON object output | Immutable inside one run | Configuration error |
| `IN-VR1A-REVIEW-CARD/v1` | Human reviewer before measurement | Must-cover topics, optional topics, known ASR traps, prohibited claims, source IDs | One card per fixed video | Source IDs validated; card revision frozen before measurement | Unique video ID | Measurement cannot start |

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

## Semantic output contracts

| Output ID | Consumer/purpose | Completion/quality | Provenance/control | Partial/failure behavior |
|---|---|---|---|---|
| `OUT-VR1A-TOPIC-MAP` | Planner/reviewer; complete source map | Canonical schema; all segments accounted | Full refs + prompt/model/run versions | No successful partial map |
| `OUT-VR1A-PLAN-PROPOSAL` | Compiler/reviewer; model's editorial proposal | Valid proposal schema and topic accounting | Raw response retained; source IDs visible | Diagnostic only if compile fails |
| `OUT-VR1A-REPORT-PLAN` | Existing renderer | Current V0 schema; budgets/refs pass | Deterministic compiler version | Absent on invalid proposal |
| `OUT-VR1A-HTML` | Owner; local reading | Existing renderer succeeds | Plan/assets/run lineage | Absent on any upstream failure |
| `OUT-VR1A-RUN-MANIFEST` | Operator/evaluator | Terminal state, versions, counts, timings, usage, paths | Append-oriented run identity | Always present after run creation when filesystem permits |
| `OUT-VR1A-ERROR` | Operator | Stable category + affected stage/ID, no credential/content dump | Retained in manifest/diagnostics | Non-zero exit |

## Canonical state authority and transitions

`run.json` inside the unique run directory is the authority for one execution.
Artifacts cannot advance state merely by existing.

| State | Allowed work | Exit guard | Failure destination |
|---|---|---|---|
| `CREATED` | Validate config/source | Inputs/config valid | `FAILED`/`CANCELLED` |
| `MAPPING` | One Mapper call | Canonical Topic Map passes | `FAILED`/`CANCELLED` |
| `TOPIC_MAPPED` | Assemble Planner context | Planner request admitted | `FAILED` |
| `PLANNING` | One Planner call | Proposal compiles to V0 plan | `FAILED`/`CANCELLED` |
| `PLAN_VALIDATED` | Render through V0 | Renderer succeeds | `FAILED` |
| `RENDERED` | Record completion | Call count exactly 2 and artifacts complete | `FAILED` |
| `FAILED` | Preserve diagnostics | Terminal | None |
| `CANCELLED` | Preserve any completed stage | Terminal | None |

Measurement acceptance is a separate human-owned status; a `RENDERED` run is
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

All failures are non-retryable inside the run. The operator decides whether to
create a new run after correcting the cause.

## Configuration, ordering, concurrency, and idempotency

- Prompt versions, model, endpoint label, temperature, timeout, and maximum
  input envelope are fixed at run creation.
- Calls are sequential and one run owns at most two admitted calls.
- Concurrency is one local run. No lock/queue is added beyond rejecting an
  existing run directory.
- Repeating the command requires a new run ID; model output is not claimed to be
  byte-deterministic.
- The compiler and renderer remain deterministic for identical validated inputs.

## Roles and permissions

| Action | Role | Allowed | Condition |
|---|---|---|---|
| Read the three transcript/manifests | Owner/implementer | Yes | Read-only |
| Send full transcript text to configured provider | Local operator | Yes | Explicit V1-A authorization; no private data expected |
| Change prompt/model/config | Implementer | Yes before a new revision | Invalidates current measurement; rerun all fixtures |
| Publish media/report | Any | No for current restricted fixtures | Separate rights authorization required |
| Accept V1-A / authorize V1-B | Owner only | Yes | After reviewing evidence; separate decisions |

## Notifications, background behavior, and feature flags

Not applicable — all work is one foreground CLI invocation. There is no worker,
callback, notification, feature flag, provider fallback, or hidden retry.
