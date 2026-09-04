# Repository Working Contract

These instructions apply to the entire repository.

## Visual Report current context

The active product naming and roadmap are now:

- `V1.0`: the runnable local MP4/Bilibili URL → ASR → semantic-v2 → renderer
  baseline that was historically developed under `V1-A` and related task IDs;
- `V1.1`: frozen Transcript Foundation accepted at commit `2bce883`;
- `V1.2`: integrated Visual Editorial Agent / Harness Design Baseline spanning
  Semantic, Presentation, deterministic Renderer, Browser Observation, and
  bounded Revision; implementation is not authorized;
- `V1.3`: post-Harness evolution selected from V1.2 evidence, deferred.

Before current Visual Report work, read this package in order:

1. `docs/visual-report/V1-STATUS.md`
2. `docs/visual-report/V1-ROADMAP.md`
3. `docs/requirements/visual-report-v1-2/requirements-readiness.json`,
   `00-handoff.md`, and `12-engineering-context.md` when V1.2 is in scope
4. The task-relevant V1.2 canonical specifications, especially `03`, `04`,
   `06`, `07`, `09`, `10`, and `11`
5. `docs/tasks/VISUAL-REPORT-V1-1-TRANSCRIPT-FOUNDATION.md` or
   `docs/tasks/VISUAL-REPORT-V1-1-MODEL-UPGRADE.md` only when frozen V1.1
   behavior or evidence is directly in scope
6. The directly affected source and tests

The V1.2 package is a complete Design Baseline, not the Final V1.2 Spec and not
standing implementation authorization. Product code, dependency changes,
Provider calls, Browser Observer execution, calibration, formal evaluation,
default-path promotion, and deployment begin only after the corresponding new
explicit Owner Goal message.

For an authorized V1.2 Goal, the V1.2 package overrides historical V0/V1-A bans
on Agent, presentation planning, and Browser Observation only inside the
versioned V1.2 path. It does not rewrite legacy contracts or frozen evidence.
Use project-owned Python/Pydantic and typed Artifact boundaries; do not add a
general Agent framework, multi-Agent runtime, free ReAct/browser/tool loop,
Patch DSL, hidden chunking, image discovery/generation, database, accounts,
multi-tenancy, hosting, or deployment.

V1.1 is frozen. Further Transcript Foundation or source-model work requires an
explicit scope reopen and must preserve its historical evidence.

## Visual Report V0 context load

Before work that modifies the V0 renderer, `report-plan`, its visual contracts,
or frozen V0 evidence, read these files in order:

1. `docs/visual-report/V0-STATUS.md`
2. `docs/requirements/visual-report-v0/00-handoff.md`
3. `docs/requirements/visual-report-v0/12-engineering-context.md`
4. `docs/tasks/VISUAL-REPORT-V0-RENDERER.md`
5. The task-relevant canonical specifications, especially `03`, `04`, `06`,
   `09`, `10`, and `11` in `docs/requirements/visual-report-v0/`

Treat that package as the durable source of truth for V0. A later explicit user
message overrides it; record any material override in the decision package and
`V0-STATUS.md` before implementing the changed scope.

V1.1 leaves the semantic and renderer contracts unchanged. Its execution reads
the current V1 package above and inspects only the V0 compatibility code/tests it
actually touches; it does not reopen the full V0 design package.

## Historical Visual Report V1-A context load

Before any work whose scope includes V1-A, Topic Mapper, Report Planner,
`build-from-transcript`, `visual-report-v1a`, or the three-video planning
measurement, read these files in order:

1. `docs/visual-report/V1A-STATUS.md`
2. `docs/requirements/visual-report-v1a/requirements-readiness.json`
3. `docs/requirements/visual-report-v1a/00-handoff.md`
4. `docs/requirements/visual-report-v1a/12-engineering-context.md`
5. The task-relevant canonical specifications, especially `03`, `06`, `07`,
   `09`, `10`, and `11` in `docs/requirements/visual-report-v1a/`
6. `docs/tasks/VISUAL-REPORT-V1A-PLANNING.md`

The V1-A package is ready for engineering handoff, but readiness is not
implementation authorization. Do not change product code or call a model until
the Owner explicitly authorizes `VR-V1A-PLANNING-001`.

This read order applies when changing or auditing the historical V1-A semantic
planning contract or its evidence. It is not a prerequisite for bounded V1.1
Transcript Foundation work, which uses the current read order above and must
leave the semantic-v2 prompt/planner and renderer behavior unchanged.

## Historical V1-A hard boundary

- Keep Topic Mapper and Report Planner as two sequential independent calls;
  both receive the full authorized transcript, and Planner also receives the
  canonical Topic Map.
- Models select existing IDs and semantic content only. Deterministic code owns
  canonical IDs, timestamps, `SourceRef`, validation, budgets, compilation,
  state, and renderer invocation.
- Use one explicit compatible model, temperature zero, SDK retry disabled, no
  alternate provider/model fallback, and record the exact run snapshot.
- Do not semantically repair invalid output, make a third model call, truncate
  or chunk as a hidden fallback, delete invalid blocks, or substitute a manual
  plan inside a run.
- Compile the current V0 plan, emit an empty current asset manifest, and reuse
  the existing deterministic renderer. V1-A creates no image block or asset.
- Give every run a unique directory and retain failures/cancellations. The
  fixed Development measurement is three videos × two repeats under one frozen
  revision; never tune selectively or remove a failure from the denominator.
- Do not add MP4/ASR, keyframes, OCR/VLM, Agent, LangGraph, RAG, database,
  queue, service/API/UI, deployment, V1-B, or V1-C.
- Stop implementation at `READY_FOR_OWNER_V1A_REVIEW`. Only the Owner may
  accept V1-A or authorize the next phase.

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
