# Video Visual Report V0 — Delivery Plan

## Documentation-only notice

This file describes the later implementation session. The requirements/design
phase does not execute any slice, code change, dependency change, migration,
infrastructure action, runtime-data creation, or deployment.

## Current-grade delivery boundary

Deliver one original, local, product-quality RLinf visual report from a manually
authored plan and manually selected frames. Build only the typed contracts,
deterministic components, CLI, tests, and visual-review evidence needed for that
report. Stop for owner visual review.

## Deferred-by-grade promotion path

| Capability | Current boundary/workaround | Risk | Owner | Upgrade trigger | Promotion implementation/test/sign-off |
|---|---|---|---|---|---|
| Transcript mapping | Human reads existing transcript | Manual effort | Owner | V0 visual acceptance + schema stabilization | Separate Topic Mapper with coverage tests |
| Report planning | Human authors plan | Human bias | Owner | Stable component language | Separate Report Planner with compression/traceability eval |
| MP4 ingest | Reuse existing P0-B transcript | Not end-to-end | Owner | Planner succeeds on existing input | Connect existing FFmpeg/MLX Whisper ingest in V1 |
| Asset selection | Human reviews candidate frames | Not automated | Owner | Frames prove visual value | Candidate extraction + Asset Resolver measured against human choice |
| OCR/VLM | Human inspects source images | Semantics not machine-readable | Owner | Repeated measured asset/content miss | Add only the lowest-cost component that fixes the miss |
| Export/publishing | Local HTML only | No public share test | Owner | Licensed/user-owned future fixture | Screenshot/PDF/web path from the same HTML renderer |

## Implementation principles

- Optimize for the first finished report, not framework completeness.
- Tune components against real content before stabilizing content budgets.
- Keep Topic Mapper and Report Planner conceptually separate even while both are
  manual in V0.
- Prefer existing Python/Pydantic and no new dependency.
- Make invalid inputs loud; do not add retries, fallbacks, compatibility layers,
  plugin systems, or generic theming.
- Visual review is an implementation phase, not post-release polish.
- Preserve local media rights and frozen P0-B evidence.

## Dependency and critical path

```text
durable handoff
→ source/frame inspection
→ provisional typed contracts
→ deterministic component system
→ real report plan/assets
→ canonical report.html
→ desktop/mobile visual iteration
→ schema/test tightening
→ owner visual review
```

No automation slice may enter this critical path.

## Vertical slices

| Slice | User value | Scope | Dependencies | Verification | Definition of done |
|---|---|---|---|---|---|
| `S0 Context/baseline` | Prevents compaction drift and P0 contamination | Read mandated docs; record branch/dirty state; protect paths | Requirements gate | Git/status review | Implementation state set to `IMPLEMENTING`; no unrelated change |
| `S1 Evidence assets` | Provides meaningful visual material | Read transcript near 60/600/1200/1800 s; FFmpeg frames; contact-sheet review; select 2–4 | Fixed local fixture | Human visual inspection and asset metadata | Every kept frame has an intentional block role, timestamp, alt, caption |
| `S2 Contracts` | Gives content a stable, inspectable shape | Small Pydantic union, section/Hero/source refs, separate assets, validation errors | S1 informs real needs | Valid/invalid contract tests | Seven types supported; no layout/style fields; invalid refs fail |
| `S3 Renderer/design system` | Produces the first visual language | Hero, Section Header, seven content components, tokens, argument spine, process SVG, responsive rules | S2 | Component fixture and browser smoke | All components render offline and adapt without overflow |
| `S4 Real report` | Creates actual product output | Hand-author RLinf plan/assets and render HTML | S1–S3 | Required CLI and content review | Thesis, 3–5 modules, relation/process, frames, timestamps, takeaways |
| `S5 Visual iteration` | Turns working output into save-worthy output | Repeated desktop/mobile screenshot critique and focused edits | S4 | Final full-page screenshots | Hierarchy, rhythm, type, density, frames, process, mobile meet rubric |
| `S6 Stabilize/verify` | Makes the result repeatable | Remove unused abstraction, calibrate budgets, tests, full checks, docs/status evidence | S5 | Ruff, pytest, CLI, offline/browser, diff check | All checks pass and status stops at owner review |

## Parallel work

None is required or preferred. One session owns content, components, and visual
iteration to preserve coherent judgment. Tool calls may run concurrently only
when independent and without splitting product authority across agents.

## Shared contracts, module owners, and review boundaries

The V0 implementation session owns project code, provisional schema, plan, local
assets, and screenshots. Existing P0-B modules/artifacts remain owned by the
stable baseline. The repository owner owns content/visual acceptance and V1
authorization.

## Schema, API, and data migration order

There is no API or migration. Implement the provisional contracts only far
enough to render all components, create the real report, then tighten budgets and
remove unused fields after screenshot iteration. Update fixtures/tests/docs with
every breaking V0 schema change.

## Environments, fixtures, and test data

- Runtime: project-local uv Python 3.12 environment.
- Integration fixture: local rights-restricted RLinf media/transcript/artifacts.
- Unit fixtures: synthetic Chinese content and tiny local placeholder images.
- Visual reference: local long-image example for principles, never copied.
- Browser: installed local browser at 1080 px and about 390 px, no external load.

## Rollout, feature flags, compatibility, and rollback

No rollout or feature flag. V0 is an isolated new module and ignored local
artifact root. Rollback is removal/reversion of V0-specific source/test/docs and
local artifacts; protected P0-B paths are never part of rollback. The provisional
schema has no external compatibility promise.

## Operational readiness

For G1: required command works, failures are visible, output replacement is safe,
the page is offline, elapsed time is recorded, tests pass, screenshots exist, and
the owner can open the local HTML. No service runbook or monitoring is needed.

## Commercial go-live, customer communication, support, incident, entitlement/usage, and offboarding readiness

Not applicable. This fixture cannot be publicly released. Local deletion is the
only offboarding action.

## Release definition of done

- The bounded task definition of done and all `ACC-VR0-*` implementation cases
  pass or are explicitly owner-only.
- `report.html`, plan, assets, selected frames, and final desktop/mobile
  screenshots exist at the fixed local root.
- The report is offline, source-traceable, attributed, and contains no unsupported
  metric.
- Existing Ruff/tests pass and protected P0-B behavior/history are unchanged.
- Task evidence records commands, results, files, screenshot viewport details,
  elapsed time, and residual issues.
- V0 status is `READY_FOR_OWNER_VISUAL_REVIEW`.
- Only after the owner sees the report may status become `OWNER_ACCEPTED`.

## Explicitly excluded future work

V1 MP4 pipeline, ASR integration, Topic Mapper, Report Planner, Asset Resolver,
automatic final frame choice, OCR, VLM, RAG, Agent, LangGraph, vector/database
infrastructure, URL input, multi-video, multi-template, cover/condensed poster,
PNG/PDF renderer, hosting, accounts, analytics, and public distribution.
