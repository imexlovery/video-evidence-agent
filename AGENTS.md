# Repository Working Contract

These instructions apply to the entire repository.

## Visual Report V0 context load

Before any work whose scope includes `visual-report`, `Video Map`, `Video Visual
Report`, `report-plan`, or the V0 renderer, read these files in order:

1. `docs/visual-report/V0-STATUS.md`
2. `docs/requirements/visual-report-v0/00-handoff.md`
3. `docs/requirements/visual-report-v0/12-engineering-context.md`
4. `docs/tasks/VISUAL-REPORT-V0-RENDERER.md`
5. The task-relevant canonical specifications, especially `03`, `04`, `06`,
   `09`, `10`, and `11` in `docs/requirements/visual-report-v0/`

Treat that package as the durable source of truth for V0. A later explicit user
message overrides it; record any material override in the decision package and
`V0-STATUS.md` before implementing the changed scope.

## V0 hard boundary

- V0 is renderer-first: hand-authored structured content and manually selected
  frames are valid inputs.
- Keep content blocks separate from assets. Blocks may reference `asset_id`;
  keyframe acquisition is not a content block.
- Use typed blocks and one deterministic renderer. Do not add an LLM layout
  planner or allow models to emit HTML, CSS, SVG paths, coordinates, type sizes,
  colors, or arbitrary grids.
- `report.html` is canonical. It is 1080 px wide at the desktop design viewport
  and has natural height. Any PNG is derived later from the HTML.
- Do not add automatic ASR, Topic Mapper, Report Planner, automatic final
  keyframe selection, OCR, VLM, RAG, Agent, LangGraph, vector storage, URL input,
  multi-template support, accounts, services, or deployment in V0.
- Do not modify or reinterpret frozen P0-B evaluation inputs, outputs, evidence,
  or conclusions. Retrieval, answering, Evidence Gate, and P0-B Eval are outside
  this experiment.

## Fixture and publication boundary

The V0 fixture `p0b-rlinf-2026` and frames derived from it are authorized only
for local, non-public research. Never upload, publish, deploy, redistribute, or
include those media assets in a public artifact. Preserve the required source
attribution in the local report.

## Long-session completion rule

`docs/tasks/VISUAL-REPORT-V0-RENDERER.md` is one bounded implementation task.
Complete its phases in one session when possible. Update both the task evidence
section and `docs/visual-report/V0-STATUS.md` in the same session whenever the
implementation status changes. Stop at `READY_FOR_OWNER_VISUAL_REVIEW`; only the
owner may record visual acceptance or authorize V1 automation.
