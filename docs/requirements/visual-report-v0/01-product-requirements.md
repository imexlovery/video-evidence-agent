# Video Visual Report V0 — Product Requirements

## Problem and evidence

The P0-B project already has stable local video ingest and timestamped
transcripts, but those artifacts are optimized for retrieval/evaluation, not
learning or sharing. A transcript and Markdown summary flatten hierarchy and
usually omit visual evidence and relationships. V0 isolates the higher-risk
product question: can a bounded structured plan and deterministic renderer make
one report that the owner genuinely wants to keep?

## Selected implementation grade and allowed/prohibited use

`G1 PROTOTYPE`. Allowed use is one local, private design experiment on the fixed
RLinf fixture. Public sharing, deployment, production reliance, provider calls,
and automated planning are prohibited. V1 is a separate promotion that requires
explicit owner authorization after visual acceptance.

## Customer, tenant, account, and service model

There is one local owner and no customer, tenant, account, role service, hosted
surface, entitlement, billing, support contract, or public release.

## Users and access context

| Actor | Situation | Need | Access |
|---|---|---|---|
| Owner/learner | Revisiting a long Chinese technical talk | Grasp thesis, structure, evidence images, and takeaways in 60–90 seconds | Local files and browser |
| Implementer | Building and visually iterating the first report | Fixed requirements, source data, component language, and stop boundary | Local repository only |

## Goals and success measures

| ID | Goal | Measure | Target |
|---|---|---|---|
| `GOAL-VR0-001` | Prove visual value | Owner comparison against transcript/Markdown | Clearly preferred for later review |
| `GOAL-VR0-002` | Preserve accurate content structure | Owner identifies thesis, progression, one key relationship, and takeaways | All found in about 60–90 seconds without the transcript |
| `GOAL-VR0-003` | Prove a bounded component system | Real report plus component/contract tests | Hero, Section Header, and required content types render deterministically |
| `GOAL-VR0-004` | Prove cross-viewport editorial quality | Desktop and mobile screenshots | No clipping/overflow; readable hierarchy at 1080 px and about 390 px |
| `GOAL-VR0-005` | Preserve traceability without Evidence-product overhead | Source refs and timestamped frame captions | Every factual block has at least one valid source ref |

## Non-goals

End-to-end MP4 automation; automatic ASR, Topic Mapper, Report Planner, keyframe
selection, OCR or VLM; RAG, Agent or LangGraph; free layout; multiple templates;
URL input; accounts; storage services; hosted web app; public distribution; PNG
or PDF renderer; production, commercial, or scale claims.

## First-release scope

### Included

- One hand-authored RLinf report plan and separate asset manifest.
- Two to four manually selected video frames.
- One provisional typed schema and deterministic renderer.
- Hero, Section Header, Insight Card, Bullet Group, Metric Row, Comparison Card,
  Process Flow, Image + Caption, and Takeaway Box components.
- One offline `report.html` with source timestamps, responsive behavior, and
  local review screenshots.
- Targeted tests and explicit invalid-input behavior.

### Excluded or later

Everything in Non-goals plus automatic conversion from transcript to plan. Topic
Mapper and Report Planner remain separate future stages: the former optimizes
coverage/recall, the latter optimizes compression, hierarchy, narrative, and
block choice.

## Product requirements

| ID | Requirement | Rationale | Priority | Evidence | Acceptance |
|---|---|---|---|---|---|
| `REQ-VR0-001` | Accept a local versioned report plan and separate asset manifest | Enables renderer-first validation | P0 | User decision | Valid fixture renders via the required command |
| `REQ-VR0-002` | Model content as a discriminated union of seven bounded block types | Stabilizes rendering without free layout | P0 | User block decision | Contract tests accept each type and reject unknown types |
| `REQ-VR0-003` | Keep keyframes in an Asset layer and resolve them only by `asset_id` | Separates information from acquisition | P0 | User decision | Unknown/duplicate asset refs fail visibly |
| `REQ-VR0-004` | Make layout, type, spacing, colors, line breaks, grids, image ratios, and SVG placement deterministic renderer concerns | Prevents model-controlled visual drift | P0 | User decision | Plan contains no style/layout primitives; same input yields equivalent HTML |
| `REQ-VR0-005` | Generate one canonical offline `report.html` at a 1080 px desktop design width and natural height | Preserves one rendering source | P0 | User decision | Browser opens the artifact with no external request |
| `REQ-VR0-006` | Render a thesis-led Hero, 3–5 coherent modules, a relationship/process view, 2–4 useful frames, timestamps, and takeaways | Defines the first useful product shape | P0 | User success target | Owner rubric confirms presence and usefulness |
| `REQ-VR0-007` | Require timestamped `source_refs` for every factual block | Supports correction and video return without importing Evidence Gate | P0 | Design constraint | Schema validation and report labels preserve refs |
| `REQ-VR0-008` | Escape all authored text and reject invalid JSON, unsafe asset paths, invalid timestamps, missing assets, and duplicate IDs | Prevents broken or unsafe local output | P0 | Safety floor | Failure tests produce non-zero exits and no false success |
| `REQ-VR0-009` | Use an original editorial visual identity and one argument-spine signature element | Makes the output recognizably designed | P0 | Visual design decision | Desktop screenshot meets visual rubric |
| `REQ-VR0-010` | Adapt to an approximately 390 px viewport without horizontal overflow | Keeps the canonical HTML usable beyond one screenshot size | P0 | User future HTML rationale | Mobile screenshot and browser check pass |
| `REQ-VR0-011` | Preserve attribution and local-only restrictions for the RLinf fixture and all derived frames | Honors existing media use basis | P0 | P0-B corpus manifest | No publication path; attribution visible in report |
| `REQ-VR0-012` | Keep frozen P0-B evaluation and retrieval paths unchanged | Prevents experiment scope contamination | P0 | Owner direction/current baseline | Diff review shows no historical artifact or frozen behavior changes |
| `REQ-VR0-013` | Iterate from actual full-page screenshots before stabilizing schema | Visual quality is the hypothesis | P0 | User phase order | Final desktop/mobile screenshots correspond to final HTML |
| `REQ-VR0-014` | Update durable task/status evidence and stop at owner visual review | Prevents compaction drift and unauthorized V1 start | P0 | User continuity request | Status is `READY_FOR_OWNER_VISUAL_REVIEW`, not owner accepted |

## Constraints and dependencies

- Existing Python `>=3.12,<3.13`, uv environment, Pydantic, FFmpeg/ffprobe, and
  local browser.
- No network, provider, external font, CDN, database, or new service.
- Prefer no new dependency. Any exception must be required by an observed V0
  failure and recorded in task evidence.
- `artifacts/` is gitignored; report review is local and must use correctly
  resolved local asset paths from the artifact root.
- The fixed video is longer than the future product range; it is a renderer-only
  stress-fixture exception.

## Glossary

- **Content block:** typed information unit such as insight, comparison, or
  process; it does not describe arbitrary layout.
- **Asset:** reusable local media metadata referenced by `asset_id`.
- **Report plan:** ordered, source-linked editorial content consumed by the renderer.
- **Argument spine:** renderer-owned vertical chapter/timestamp rail that makes
  the video's logical progression visible.
- **Canonical artifact:** `report.html`; screenshots are derived review evidence.
- **Topic Mapper:** future coverage-oriented understanding stage.
- **Report Planner:** future compression and block-selection stage, kept separate
  from Topic Mapper.
