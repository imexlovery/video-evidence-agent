# Video Visual Report V0 — Functional Specification

## Capability inventory

| Capability | Requirements | Owner component |
|---|---|---|
| Validate report plan | `REQ-VR0-001`, `002`, `007`, `008` | Pydantic plan models |
| Validate/resolve assets | `REQ-VR0-003`, `008`, `011` | Asset models/resolver |
| Render structure | `REQ-VR0-004`, `005`, `006`, `009`, `010` | Deterministic document renderer |
| Render typed content | `REQ-VR0-002`, `004`, `006` | Seven block components |
| Preserve traceability | `REQ-VR0-007` | Source-ref/timestamp component |
| Local CLI | `REQ-VR0-001`, `005`, `008` | Module entry point |
| Visual review | `REQ-VR0-009`, `010`, `013`, `014` | Local browser and task evidence |

## Semantic input contracts

| Input ID/version | Producer/purpose | Shape/required fields | Limits | Validation/consent | Duplicate/order | Invalid behavior | Examples |
|---|---|---|---|---|---|---|---|
| `IN-REPORT-PLAN/visual-report.v0-prototype` | Human/assisted author; report content | Report metadata, video metadata, Hero content, ordered sections, typed blocks, source refs | 3–5 report modules for fixture; bounded strings/lists set from final component needs | Pydantic; local non-sensitive research content | Section/block IDs unique; array order is canonical | Non-zero exit; no fallback | Example below |
| `IN-ASSETS/visual-report-assets.v0-prototype` | Human-selected assets | Asset ID, `keyframe`, timestamp, relative local path, alt, caption | 2–4 used keyframes in final report | Pydantic, path containment, file readable, time in video range | Asset IDs unique; list order is not layout authority | Non-zero exit | Example below |

### Report-plan shape

```json
{
  "schema_version": "visual-report.v0-prototype",
  "report_id": "v0-rlinf",
  "video": {
    "video_id": "p0b-rlinf-2026",
    "title": "面向具身智能的高灵活大规模强化学习框架 RLinf",
    "duration_ms": 2093120,
    "source_url": "https://www.bilibili.com/video/BV1KNjz6cEeR/?p=1",
    "attribution": "2026 北京智源大会；于超；《面向具身智能的高灵活大规模强化学习框架 RLinf》；Bilibili BV1KNjz6cEeR p1。"
  },
  "hero": {
    "eyebrow": "VIDEO VISUAL REPORT · RL SYSTEMS",
    "title": "从训练速度到算法驱动的系统设计",
    "tldr": "RLinf 的核心不是单点加速，而是让仿真与真机强化学习共享一套可扩展、可组合的系统基础。"
  },
  "sections": [
    {
      "section_id": "why-rl",
      "kicker": "01 · WHY",
      "title": "为什么具身智能需要在线强化学习",
      "timestamp_ms": 60000,
      "blocks": [
        {
          "block_id": "offline-online",
          "type": "comparison_card",
          "headline": "离线数据给起点，在线交互补能力边界",
          "left": {"label": "OFFLINE", "items": ["使用既有数据训练"]},
          "right": {"label": "ONLINE", "items": ["与环境交互并持续更新"]},
          "asset_id": "frame-0060",
          "source_refs": [
            {"segment_id": "p0b-rlinf-2026-seg-001", "start_ms": 46400, "end_ms": 94000}
          ]
        }
      ]
    }
  ]
}
```

### Asset-manifest shape

```json
{
  "schema_version": "visual-report-assets.v0-prototype",
  "assets": [
    {
      "asset_id": "frame-0060",
      "type": "keyframe",
      "timestamp_ms": 60000,
      "path": "assets/frame-0060.jpg",
      "alt": "演示文稿比较离线强化学习与在线强化学习",
      "caption": "离线学习使用既有数据，在线学习通过环境交互扩展能力边界。"
    }
  ]
}
```

Asset paths are relative to the directory containing `assets.json`, may not be
URLs or absolute paths, and after resolution must remain inside that artifact
directory. The implementation may narrow string/list budgets after the first
visual iteration; it may not introduce layout fields.

## Typed block payloads

Every block has `block_id`, `type`, and one or more `source_refs`. Every block may
have `asset_id`; `image_caption` must have one.

| Type | Required content | Renderer intent |
|---|---|---|
| `insight_card` | `headline`, `body` | One dominant thesis or consequence |
| `bullet_group` | `headline`, 2–5 items | Parallel supporting facts without card spam |
| `metric_row` | 2–4 items of `value`, `label`, optional `context` | Verified numbers or concise milestones only |
| `comparison_card` | `headline`, left/right labels and 1–4 items per side | Meaningful contrast, stacked on mobile |
| `process_flow` | `headline`, 3–6 ordered steps with title/body | Renderer-owned SVG/vertical mobile flow |
| `image_caption` | `headline`, optional `body`, required `asset_id` | Evidence frame with timestamp and caption |
| `takeaway_box` | `headline`, 2–5 takeaways | Final synthesis and memorable conclusions |

`key_insight`, `process`, `comparison`, `metric`, and similar semantic labels are
represented by these fixed discriminants; aliases are not accepted in V0.

## Semantic output contracts

| Output ID/version | Consumer/purpose | Shape/channel | Completion/quality | Evidence/uncertainty | User control/lifecycle | Side effects | Examples |
|---|---|---|---|---|---|---|---|
| `OUT-REPORT-HTML/v0` | Owner; visual review and later study | Offline UTF-8 HTML with local CSS/SVG/assets | All validated sections rendered; no broken refs; natural height | Visible timestamps, attribution, and source-linked metadata | Owner may edit inputs, rerender, delete local root | Replaces requested local output only after successful render | `artifacts/visual-report/v0-rlinf/report.html` |
| `OUT-RENDER-ERROR/v0` | Implementer; correction | Stderr plus non-zero exit | Identifies category and affected field/ID/path | Does not claim an output success | Correct input/code and explicitly rerun | No remote side effect | `unknown asset_id: frame-x` |
| `OUT-VISUAL-CHECK/v0` | Owner; visual acceptance | Desktop and mobile PNG screenshots | Captured from final HTML | Viewport named in task evidence | Regenerated after material visual change | Local only | `visual-check/desktop.png` |

## Task contracts

| Task ID | Trigger | Input/output | Side effect | Review | Completion | Failure/retry | Evidence/artifacts |
|---|---|---|---|---|---|---|---|
| `TASK-VR0-RENDER` | Explicit local CLI invocation | Plan + assets → HTML | Writes one requested local file | Automated contracts + browser | Exit 0 and complete HTML | No auto retry; fix then rerun | Command output and artifact |
| `TASK-VR0-VISUAL-REVIEW` | Final HTML exists | HTML → screenshots + owner decision | Local screenshots/status only | Human owner | Owner accepts or gives bounded feedback | Iterate within V0 | Screenshots, task/status entries |

## Detailed rules

| Rule ID | Inputs/preconditions | Required behavior | Output/error | Verification |
|---|---|---|---|---|
| `RULE-VR0-001` | Identical normalized plan/assets and renderer version | Render equivalent HTML order/content/styles | Deterministic output | Repeat render comparison excluding documented generated metadata; preferably emit no current time |
| `RULE-VR0-002` | Authored text includes `<`, `&`, quotes, or script markup | Escape as text in every component | Safe visible text | Escaping tests |
| `RULE-VR0-003` | Valid asset ref | Resolve within assets manifest directory and verify readable | Local image URL in HTML | Path tests |
| `RULE-VR0-004` | Missing/unknown data | Fail closed at validation | Non-zero and useful error | Failure tests |
| `RULE-VR0-005` | Factual block | Render human-readable timestamp from earliest source ref and retain all refs in semantic markup/data attributes | Visible time/source metadata | Component tests |
| `RULE-VR0-006` | Process flow | Renderer computes placement and mobile fallback | SVG desktop, vertical flow mobile | Screenshot/component test |
| `RULE-VR0-007` | Final report | Render attribution and local prototype notice | Footer/source module | Integration test |
| `RULE-VR0-008` | Ambiguous numeric content | Author omits number or labels uncertainty explicitly; renderer never invents | No unsupported metric | Content review |
| `RULE-VR0-009` | Output already exists | Validate/render into a temporary sibling then replace successful output | Previous valid file survives validation failure | Recovery test |

## Canonical state authority and status mappings

| Concept | Authority | Other representations | Reconciliation rule |
|---|---|---|---|
| Product/implementation stage | `docs/visual-report/V0-STATUS.md` under owner decisions | Task evidence and artifact existence | Higher source-of-truth wins; artifact existence alone never advances state |
| Requirements readiness | Validator-generated `requirements-readiness.json` | Prose package | Generated file is sole machine state |
| Report content/order | Validated `report-plan.json` | Rendered DOM | Re-render from plan; do not hand-edit canonical HTML |
| Asset metadata | Validated `assets.json` | Image tags/captions | Manifest wins; missing files fail |
| Visual implementation | Renderer source/design tokens | HTML/CSS output | Source wins; do not maintain a second renderer |

## State model and transitions

| State | Goal | Allowed operations/tools | Data access | Exit guard | Timeout/retry | Human action | Failure destination |
|---|---|---|---|---|---|---|---|
| `DESIGN_HANDOFF_PUBLISHED` | Durable design exists | Read docs; begin bounded task | Read source assets | Implementation begins | Not applicable | None | `FAILED` only if package conflict found |
| `IMPLEMENTING` | Build and iterate | Edit allowed scope, FFmpeg, tests, browser screenshots | Local fixture | Definition of done passes | Explicit reruns only | None | `FAILED` with evidence |
| `READY_FOR_OWNER_VISUAL_REVIEW` | Present final local artifact | View/read only; bounded owner feedback | Final HTML/screenshots | Owner decision | Iteration returns to `IMPLEMENTING` | Accept or request revision | `IMPLEMENTING` or `FAILED` |
| `OWNER_ACCEPTED` | Close V0 | Preserve artifact/status | Local artifact | Explicit owner acceptance | No auto next phase | Owner only | Not applicable |
| `FAILED` | Preserve observed failure | Diagnose within V0 scope | Relevant local evidence | Successful rerun returns to `IMPLEMENTING` | Manual only | Needed only for scope/authority change | Remain `FAILED` if unresolved |

## Draft, candidate, approval, commit, reject, and undo lifecycle

Plan/assets are editable drafts until a successful render. The resulting HTML is
a candidate until desktop/mobile checks pass. Passing implementation checks moves
the task to owner review; only explicit owner acceptance commits the V0 product
decision. Rejection returns to visual iteration. Undo means restoring a prior
plan/source version through normal version control or retained local copy, never
rewriting historical task evidence.

## User control matrix

| Stage | Edit | Approve | Reject | Cancel | Retry | Undo/withdraw | Required evidence |
|---|---|---|---|---|---|---|---|
| Inputs | Owner/implementer | Not applicable | Owner may reject content | Yes | Yes | Replace local drafts | Validation output |
| Render candidate | Implementer | No | Owner may request revision | Yes | Explicit | Re-render prior valid inputs | Commands/screenshots |
| Visual gate | Only bounded iteration | Owner only | Owner only | Owner | After changes | Owner may withdraw acceptance by new instruction | Owner message/status |

## Validation and error taxonomy

- `PLAN_PARSE_ERROR`
- `PLAN_SCHEMA_ERROR`
- `ASSET_SCHEMA_ERROR`
- `UNSUPPORTED_SCHEMA_VERSION`
- `DUPLICATE_ID`
- `UNKNOWN_BLOCK_TYPE`
- `UNKNOWN_ASSET_REFERENCE`
- `UNSAFE_ASSET_PATH`
- `ASSET_NOT_FOUND`
- `INVALID_SOURCE_REFERENCE`
- `OUTPUT_IO_ERROR`

Errors include the stable category and offending field/ID/path without dumping
full media content.

## Ordering, concurrency, idempotency, and duplicates

Array order in the plan is canonical. IDs are unique. V0 is single-process and
one report at a time. A successful repeat with identical inputs is idempotent at
the artifact level. No concurrency lock or queue is added.

## Edit, deletion, cancellation, retry, timeout, and recovery

Edits happen to plan/assets or renderer source, followed by explicit rerender.
Deletion is local artifact-root removal by the owner. Ctrl-C cancels the current
process. No automatic retry exists. A prior valid HTML is preserved when new
input validation or rendering fails.

## Roles and permissions

| Action/resource | Role | Allowed | Conditions | Audit event |
|---|---|---|---|---|
| Read fixed transcript/media | Local owner/implementer | Yes | Local research only | Task evidence, not runtime audit |
| Render local report | Implementer | Yes | Bounded paths and no network | Command result |
| Publish/upload fixture or frames | Any | No | Rights restriction | Prevented by scope; any attempt is a failure |
| Accept V0 | Owner | Yes | After viewing final artifact | Status update |
| Start V1 | Implementer | No | Requires new explicit owner authorization | Separate future task |

## Notifications and background behavior

None. Rendering and review are foreground local actions.

## Configuration and feature flags

No runtime feature flag. The schema version and fixed theme identify V0. Design
tokens are renderer source, not plan configuration.

## Edge cases

| Case | Expected behavior | Linked requirement | Test |
|---|---|---|---|
| Chinese punctuation and long unbroken Latin identifier | Wrap without overflow | `REQ-VR0-010` | Desktop/mobile fixture |
| Section with no blocks | Reject | `REQ-VR0-008` | Contract test |
| Optional asset omitted from non-image block | Render text component normally | `REQ-VR0-003` | Component test |
| Image block without asset | Reject | `REQ-VR0-003` | Failure test |
| Source start equals/end exceeds video bounds | Reject invalid range | `REQ-VR0-007` | Boundary test |
| Very long authored copy | Enforce schema budget after visual calibration; reject rather than shrink typography | `REQ-VR0-009` | Overflow/contract test |
| HTML/script in copy | Escape as text | `REQ-VR0-008` | Security test |
| Network URL in asset path | Reject | `REQ-VR0-011` | Security test |
