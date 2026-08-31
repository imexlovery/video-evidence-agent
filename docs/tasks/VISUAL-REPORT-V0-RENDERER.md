# VR-V0-RENDERER-001 — First Product-Quality Visual Report

## Mission

In one implementation session, create the first product-quality local Video
Visual Report for the fixed RLinf fixture. The outcome is a visually reviewed
`report.html`, not an automated video pipeline.

The session ends at `READY_FOR_OWNER_VISUAL_REVIEW`. It must not authorize its
own visual acceptance and must not begin V1.

## Mandatory context

Read, in this order, before editing:

1. `AGENTS.md`
2. `docs/visual-report/V0-STATUS.md`
3. `docs/requirements/visual-report-v0/00-handoff.md`
4. `docs/requirements/visual-report-v0/03-functional-spec.md`
5. `docs/requirements/visual-report-v0/04-system-design.md`
6. `docs/requirements/visual-report-v0/06-interfaces-integrations.md`
7. `docs/requirements/visual-report-v0/09-test-acceptance.md`
8. `docs/requirements/visual-report-v0/12-engineering-context.md`

The decisions are already bounded. Do not ask the owner to select a framework,
template, fixture, block list, palette, or output format.

## Allowed change scope

Create or modify only what the implementation needs under:

- `src/video_evidence_agent/visual_report/`
- `tests/` for targeted visual-report tests
- `artifacts/visual-report/v0-rlinf/`
- this task's implementation-evidence section
- `docs/visual-report/V0-STATUS.md`

A minimal existing CLI integration may be changed only if required for the
specified command. Prefer a module entry point and existing dependencies. Do not
add a dependency unless the implementation cannot satisfy the contract with the
standard library and installed Pydantic; record and justify any such exception.

## Protected scope

Do not change frozen P0-B media metadata, manifests, Gold, results, reports,
retrieval behavior, answering, Evidence Gate, or historical status. Do not add
ASR, Topic Mapper, Report Planner, automatic keyframe ranking, OCR, VLM, RAG,
Agent, provider calls, database, queue, service, deployment, URL input, or a
second template.

## Fixed inputs

- Media: `eval/p0b/media/2026北京智源大会丨强化学习 p01 面向具身智能的高灵活大规模强化学习框架 RLinf：于超 [BV1KNjz6cEeR_p1].mp4`
- Transcript: `artifacts/p0b-ingest/p0b-rlinf-2026/segments.jsonl`
- Manifest: `artifacts/p0b-ingest/p0b-rlinf-2026/manifest.json`
- Reference direction only: `/Users/tristana/Desktop/"图个快"效果图.png`
- Candidate frame times: `60`, `600`, `1200`, `1800` seconds.

Keep the report and derived frames local. Preserve this attribution in the
report: `2026 北京智源大会；于超；《面向具身智能的高灵活大规模强化学习框架 RLinf》；Bilibili BV1KNjz6cEeR p1。`

## Fixed outputs

```text
artifacts/visual-report/v0-rlinf/
├── report.html
├── report-plan.json
├── assets.json
├── assets/
│   ├── frame-0060.jpg
│   ├── frame-0600.jpg
│   ├── frame-1200.jpg
│   └── frame-1800.jpg
└── visual-check/
    ├── desktop.png
    └── mobile.png
```

Only the 2–4 frames actually used by the final plan need remain in `assets/`.
`report.html` is canonical; screenshots are review evidence, not alternate
renderers. A report PNG is not required.

## Required render contract

The completed implementation must support:

```bash
uv run python -m video_evidence_agent.visual_report render \
  --plan artifacts/visual-report/v0-rlinf/report-plan.json \
  --assets artifacts/visual-report/v0-rlinf/assets.json \
  --output artifacts/visual-report/v0-rlinf/report.html
```

The command is synchronous, deterministic for identical local inputs, performs
no network or model call, writes the requested HTML, prints a concise success
summary, and exits non-zero with a useful error on invalid input.

## Provisional schema and component set

Keep `report-plan.json` and `assets.json` separate. Use a discriminated union for
these seven content block types:

1. `insight_card`
2. `bullet_group`
3. `metric_row`
4. `comparison_card`
5. `process_flow`
6. `image_caption`
7. `takeaway_box`

Hero and Section Header are renderer-owned structural components. Blocks carry
content, ordering, source references, and an optional `asset_id`; only
`image_caption` requires an asset. Assets carry `asset_id`, `type`, timestamp,
local path, alt text, and caption. Do not introduce `keyframe_request` as a block.

Every factual block must include at least one timestamped `source_ref`. Unknown
block types, duplicate IDs, missing assets, unknown asset references, unsafe
paths, invalid timestamps, and invalid JSON fail visibly. Escape all authored
text before writing HTML.

The V0 schema is provisional and renderer-owned. Do not turn it into a generic
plugin system or public compatibility layer.

## Fixed content story

Use the transcript and frames to tell one compressed argument:

1. Why embodied intelligence needs reinforcement learning, including offline
   versus online learning.
2. How RLinf moved from a speed problem to flexible, algorithm-driven system
   design.
3. The process and architecture needed to coordinate simulation and real-world
   training constraints.
4. What the framework enables, where its evidence is strongest, and the final
   takeaways.

The report may omit secondary topics. Do not invent or silently repair facts.
Any numeric metric must be verified against a clear source frame or transcript
evidence; omit an ambiguous number instead of polishing it into a claim.

## Fixed visual direction

Create a single editorial identity: **research field notebook meets systems
blueprint**. It should feel technical, calm, and authored—not like generic AI
cards or a marketing poster.

- Palette tokens: ink navy `#14213D`, cool canvas `#F5F7FB`, paper `#FFFFFF`,
  RL purple `#6D4AFF`, data blue `#2878FF`, signal coral `#FF6B4A`.
- Type roles: `Songti SC`/`STSong` for the display thesis;
  `PingFang SC`/`Hiragino Sans GB` for body; `SFMono-Regular` for timestamps and
  data labels. Use local fallbacks only.
- Signature element: one vertical **argument spine** that connects chapter
  markers and real timestamps through the report.
- Desktop artboard: 1080 px wide, natural height, approximately 96 px side
  gutters. Body copy must remain comfortably readable.
- Mobile check: approximately 390 px viewport; one column, stacked comparison,
  vertical process flow, no horizontal overflow.
- Treat frames as evidence: preserve 16:9 content, add timestamp and caption,
  avoid decorative blur or arbitrary crops.
- Build rhythm with full-width insight, comparison, process, image breaks, and a
  decisive takeaway. Do not wrap every paragraph in a card.
- Avoid external fonts, gradients, glassmorphism, neon, excessive rounding,
  arbitrary decoration, and uncontrolled animation.

## One-session execution plan

### Phase 1 — Baseline and source selection

- Confirm the branch and clean/dirty state; preserve all existing user changes.
- Read the fixed transcript around the selected timestamps.
- Extract the four candidate frames with FFmpeg, inspect them as a contact sheet,
  and keep the strongest 2–4.
- Record exact asset metadata and local-use attribution.

Exit evidence: selected frames exist locally and each has an intentional report
role.

### Phase 2 — Typed schema and deterministic renderer

- Implement the smallest Pydantic contracts needed by the seven block types and
  assets.
- Implement deterministic structural and block components with one design-token
  layer.
- Use simple renderer-owned SVG only for the process flow and argument spine.
- Implement the required CLI contract and visible validation failures.

Exit evidence: a minimal fixture containing every component renders offline.

### Phase 3 — First real report

- Hand-author `report-plan.json` from the fixed story and source references.
- Create `assets.json` for selected frames.
- Render the canonical RLinf `report.html`.

Exit evidence: the report contains a thesis-led Hero, 3–5 content modules, at
least one relation/process component, 2–4 informative frames, takeaways, and
timestamps.

### Phase 4 — Visual iteration

- Inspect full-page desktop and mobile screenshots in a browser.
- Iterate typography, whitespace, information density, hierarchy, image
  treatment, process legibility, and chapter rhythm.
- Repeat until no clipping, overflow, accidental card grid, weak hierarchy, or
  obviously generic styling remains.

Exit evidence: `visual-check/desktop.png` and `visual-check/mobile.png` show the
final HTML at both viewports.

### Phase 5 — Stabilize and verify

- Tighten the schema to what the final renderer actually uses; remove unused
  abstractions.
- Add targeted contract, component, failure, escaping, and integration tests.
- Run the commands below and record results.
- Update `docs/visual-report/V0-STATUS.md` to
  `READY_FOR_OWNER_VISUAL_REVIEW` and append the evidence section below.

Do not mark `OWNER_ACCEPTED` and do not start automation.

## Required verification

```bash
uv run ruff check .
uv run pytest -q
uv run python -m video_evidence_agent.visual_report render \
  --plan artifacts/visual-report/v0-rlinf/report-plan.json \
  --assets artifacts/visual-report/v0-rlinf/assets.json \
  --output artifacts/visual-report/v0-rlinf/report.html
git diff --check
```

Also verify in-browser at 1080 px and approximately 390 px, with network disabled
or by confirming that the page makes zero external requests.

## Definition of done

- All required files and the render command exist and work locally.
- The output uses all required structural components and only the bounded block
  family needed for the final story.
- Every factual claim is traceable to a timestamped source reference.
- Two to four selected frames add information rather than decoration.
- Desktop and mobile screenshots have no clipping or horizontal overflow.
- The report opens with no external network dependency and contains no provider
  call, runtime AI, tracking, or publication path.
- Targeted validation and the existing test suite pass.
- Status and evidence are updated in the same session.
- The session stops at owner visual review.

## Owner visual review rubric

The owner decides acceptance after viewing the artifact. Acceptance requires:

- **Content quality:** the central argument and material caveats are correct;
  no important contradiction or unsupported metric remains.
- **Information architecture:** a reader can identify the thesis, progression,
  system relationship, and takeaways in about 60–90 seconds.
- **Visual quality:** hierarchy, type, spacing, frames, and diagrams feel like a
  finished editorial product and are clearly more useful than Markdown.
- **Save value:** the owner would keep the local report for later review. Public
  shareability is not tested with this rights-restricted fixture.

## Implementation evidence

Status: `READY_FOR_OWNER_VISUAL_REVIEW`

### 2026-08-30 — Owner visual revision 1 completed

- Result: revised the generic deterministic renderer and the RLinf plan; the
  canonical report now contains 4 semantic sections, 13 typed blocks, and the
  same 4 manually selected keyframes.
- Information architecture: section starts now follow transcript topic turns at
  `00:00`, `03:54`, `19:21`, and `27:06`, independent of the candidate-frame
  times. Added one compact supporting block explaining why existing frameworks
  fail to absorb changing algorithms and system boundaries.
- Visual system: replaced the oversized field-notebook/poster composition with
  a compact Chinese editorial article; removed the reading note, argument spine,
  section kickers, decorative block labels, and dark image-caption panels;
  tightened typography/spacing; added restrained small radii; and changed bullet
  groups to small round dots.
- Keyframes: every figure visibly contains only its source image and one
  bottom-right asset timestamp (`01:00`, `10:00`, `20:00`, or `30:00`). Authored
  source refs remain machine-readable in `data-source-refs`; no visible
  `figcaption` or competing source timestamp remains.
- Commands and results:
  - focused Ruff: passed.
  - focused pytest: `10 passed`.
  - full Ruff: passed.
  - full pytest: `38 passed in 1.06s`.
  - real render: `4 sections, 13 blocks, 4 used assets`.
  - structural/offline check: 27,163-byte HTML, 4 images, no scripts, no remote
    asset markup, no decorative labels/reading note/argument spine, and exactly
    one visible timestamp inside every figure.
  - requirements readiness validator: `READY_FOR_ENGINEERING_HANDOFF` after
    recording `DEC-VR0-053` and refreshing coverage/fingerprints.
  - `git diff --check`: passed.
- Visual-review boundary: the in-app browser refused automated refresh of the
  local `file://` page under its URL safety policy. No alternate browser channel
  was used. Per the owner's instruction, the two prior PNGs were not regenerated
  and remain historical evidence for the rejected first candidate. The revised
  `report.html` therefore awaits direct Owner inspection; acceptance remains
  `PENDING`, and V1 remains unauthorized.

### 2026-08-30 — Owner visual revision 1 requested

- The first candidate was not accepted. The owner requested a renderer-level
  revision rather than a hand edit of `report.html`.
- Required changes: remove the reading-note strip and decorative English/index
  labels; replace the argument-spine/poster composition with a denser Chinese
  editorial flow; give colored components small corner radii; use round bullet
  dots; show each keyframe as the self-explanatory image plus its own bottom-right
  timestamp only; and set section timestamps from semantic topic boundaries
  rather than the four sampled frame times.
- The existing desktop/mobile PNGs remain historical evidence for the rejected
  first candidate and are not regenerated in this bounded iteration. Owner
  acceptance remains `PENDING`; V1 remains unauthorized.

### 2026-08-30 — VR-V0-RENDERER-001 implementation

- Result: completed the renderer-first V0 for `p0b-rlinf-2026`. The canonical
  report contains 4 sections, 12 typed blocks, and 4 manually selected keyframes
  at approximately 60, 600, 1200, and 1800 seconds.
- Changed files: added the typed schema, deterministic renderer, CLI, focused
  tests, real `report-plan.json`, `assets.json`, local keyframes, canonical
  `report.html`, and desktop/mobile visual evidence. Updated this evidence and
  `docs/visual-report/V0-STATUS.md`. Existing uncommitted requirement documents
  were preserved. No `eval/p0b/**`, frozen P0-B artifacts, retrieval, answering,
  Evidence Gate, or evaluation files were changed.
- Commands and results:
  - `UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run ruff check src/video_evidence_agent/visual_report tests/test_visual_report.py`: passed.
  - `UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q tests/test_visual_report.py`: `10 passed`.
  - `UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run ruff check .`: exit 0, `All checks passed!`, measured `real 0.05s`.
  - `UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q`: exit 0, `38 passed in 1.45s`, measured `real 5.10s` including uv startup.
  - `UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run python -m video_evidence_agent.visual_report render --plan artifacts/visual-report/v0-rlinf/report-plan.json --assets artifacts/visual-report/v0-rlinf/assets.json --output artifacts/visual-report/v0-rlinf/report.html`: exit 0, `4 sections, 12 blocks, 4 used assets`, measured `real 0.08s`.
  - Offline artifact check: `report.html` is 35,643 bytes with 4 sections, 12
    block markers, 4 local images, and 4 visible section timestamps; no runtime
    script, external stylesheet, or remote asset markup was present.
  - `git diff --check`: exit 0.
- Browser visual evidence: at a 1080px viewport, `innerWidth=1080`,
  `scrollWidth=1065`, `scrollHeight=6516`, and all 4 images loaded; at a 390px
  viewport, `innerWidth=390`, `scrollWidth=375`, `scrollHeight=7043`, and all 4
  images loaded. Desktop process flow/arrows and mobile comparison/process
  stacking were inspected, including top, middle, process, and bottom regions.
  The final PNGs are 1:1 stitched normal-viewport captures with the browser
  scrollbar strip removed: desktop `1050x6516`, mobile `360x7042`.
- Screenshot paths:
  `artifacts/visual-report/v0-rlinf/visual-check/desktop.png` and
  `artifacts/visual-report/v0-rlinf/visual-check/mobile.png`.
- Source attribution and the local, non-public research notice are present in
  the report. The source URL was not fetched.
- Residual and stop state: owner visual acceptance remains `PENDING`; no V1
  automation, public publication, or performance claim was started. Stop at
  `READY_FOR_OWNER_VISUAL_REVIEW`.
