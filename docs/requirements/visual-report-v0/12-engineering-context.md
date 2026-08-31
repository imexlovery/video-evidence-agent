# Video Visual Report V0 — Engineering Context

## Documentation and implementation separation

- This package contains requirements and technical design only.
- Separate implementation task: `docs/tasks/VISUAL-REPORT-V0-RENDERER.md`.
- Implementation entry condition: validator-generated readiness file has
  `ready: true`, the mandatory context files are read, and no later owner message
  supersedes the V0 boundary.
- Implementation stop: `READY_FOR_OWNER_VISUAL_REVIEW`; do not self-accept V0.

## Selected grade and implementation/runtime boundary

- Grade: `G1 PROTOTYPE`.
- Selection method: user-confirmed `V0 — Visual Prototype`.
- Permitted implementation/runtime scope: local typed JSON validation,
  deterministic HTML/CSS/SVG components, FFmpeg development-time frame extraction,
  one real report, tests, browser screenshots, task/status updates.
- Prohibited scope: automatic ASR/mapping/planning/frame selection, OCR, VLM,
  RAG, Agent, external providers, services, databases, deployment, public sharing,
  multiple templates, and any frozen P0-B change.
- Next-grade compatibility: preserve separate future Topic Mapper and Report
  Planner contracts; keep content/assets separate; keep renderer deterministic.

## Downstream framework contract

- Status: `NOT_APPLICABLE`.
- Framework/version: none.
- Hypha recommendation disposition: `NOT_APPLICABLE` because V0 has no Agent,
  LLM workflow, tools, memory, or server runtime.
- Product implementation strategy: `FRAMEWORKLESS` project-owned module.
- Required public capabilities: none beyond existing Python/Pydantic and the
  versioned local JSON/CLI contract.
- Compatibility envelope: Python `>=3.12,<3.13`, uv, existing lockfile,
  offline/local macOS, semantic HTML/CSS/limited inline SVG.
- Prohibited assumptions: no hidden Hypha/private framework contract, model,
  browser automation runtime, external CDN, or hosted service.
- Target repository/output: `/Users/tristana/Develop/video-evidence-agent` and
  `artifacts/visual-report/v0-rlinf/`.

## Agent module adoption matrix

| Module | Route | Dependency/ref | Why | Customization boundary | Canonical owner | Compatibility contract | Tests/evidence | Upgrade owner | Rollback/fallback |
|---|---|---|---|---|---|---|---|---|---|
| Domain/workflow | `NOT_APPLICABLE` | None | One synchronous render, no workflow engine | Do not add FSM/orchestrator | Owner | Status docs only | Task/status review | Owner | None |
| Runtime/FSM | `NOT_APPLICABLE` | None | A0 CLI process | No Agent runtime | Owner | Foreground command | CLI test | Owner | None |
| Events/trace/replay | `NOT_APPLICABLE` | None | No event system | Task evidence only | Owner | Repeat render determinism | Tests | Owner | None |
| Tools/MCP | `NOT_APPLICABLE` | None | No runtime tools | FFmpeg/browser are development tools | Owner | No product tool contract | Scope review | Owner | None |
| Memory/context | `NOT_APPLICABLE` | None | No runtime memory | Repo docs hold engineering context | Owner | Mandatory read order | AGENTS/status | Owner | None |
| Execution/workspace | `PROJECT_OWNED` | Existing uv Python project | Reuses repository | New visual-report module only | Repository | Required module CLI | Integration test | Owner | Revert V0 module |
| Prompt/inference/models | `NOT_APPLICABLE` | None | Runtime AI excluded | No provider/model call | Owner | A0 | Offline/source review | Owner | None |
| Storage/data/artifacts | `PROJECT_OWNED` | Local JSON/JPEG/HTML | Small transparent artifact contract | No DB/cache | Renderer module | Versioned schemas/local root | Contract tests | Owner | Delete/regenerate root |
| Serving Cache/WorkCache | `NOT_APPLICABLE` | None | No server/cache | Do not add | Owner | None | Scope review | Owner | None |
| Policy/identity/approval | `NOT_APPLICABLE` | Local owner boundary | No accounts/actions | Owner visual gate in docs | Owner | Explicit status authority | Status review | Owner | None |
| Evaluation/testing | `PROJECT_OWNED` | pytest/Ruff/browser | Existing project workflow plus visual rubric | No P0-B eval reuse | Repository/owner | Tests + owner gate | Acceptance package | Owner | Revert V0 changes |
| Product surface | `PROJECT_OWNED` | Offline HTML | Canonical product artifact | One fixed theme | Renderer/owner | UI contract | Screenshots | Owner | Rerender prior plan |
| Operations | `NOT_APPLICABLE` | None | No service | Local command evidence only | Owner | No SLA/support | Task evidence | Owner | None |

## Required framework capability map

| Capability | Required public contract | Requirements | Acceptance evidence |
|---|---|---|---|
| Input/output contracts | Project-owned Pydantic + CLI | Versioned plan/assets, canonical HTML, stable errors | Contract/integration tests |
| Source adapters and lineage | Existing files plus source refs | Read-only transcript/media, attribution, timestamps | Content/rights review |
| Tasks, state, and recovery | Foreground command + durable status docs | Safe replacement, explicit retry, owner gate | Recovery test/status |
| Policy, permissions, and approval | Local scope and owner decision | No publication; owner accepts V0 | Diff/status review |
| Memory and artifacts | Local artifact root | No DB/memory; contained files | Data contract/tests |
| Evaluation and versioning | pytest/Ruff/schema version/browser rubric | Deterministic tests and visual screenshots | Acceptance evidence |
| Observability and operations | CLI result/task log | Exit/count/path/time; no service telemetry | Task evidence |
| Tenant/customer lifecycle | Not applicable | No customers/accounts | Scope review |

## Implementation authority matrix

| Decision | Class | Decision owner | Allowed envelope | Prohibited | Acceptance evidence |
|---|---|---|---|---|---|
| V0 product boundary | Fixed constraint | Owner | Renderer prototype | V1/automation expansion | Diff/task review |
| Schema content/asset separation | Required invariant | Owner | Closed block union + optional asset refs | Keyframe acquisition block/free layout | Contract tests |
| Internal file/function split | Implementation-delegated | Implementer | Small testable module under allowed path | New generic framework | Code review |
| Copy and block selection | Implementation-delegated | Implementer | Fixed RLinf story, verified facts, 3–5 modules | Unsupported facts/coverage claim | Source/owner review |
| Exact visual tuning | Implementation-delegated | Implementer | Fixed identity, palette, type roles, argument spine | New theme/free layout/generic card wall | Screenshots |
| Dependency exception | Prohibited unless observed blocker | Owner/implementer evidence | Existing dependencies first | Convenience dependency/toolchain migration | Explicit task evidence and lock update if truly needed |
| Visual acceptance | Fixed constraint | Owner | Accept/request iteration | Implementer self-approval | Owner message/status |
| V1 start | Prohibited | Owner | Separate later task | Automatic continuation | New authorization |

## Project mode

- Greenfield or existing system: existing system, isolated new product experiment.
- Repository root: `/Users/tristana/Develop/video-evidence-agent`.
- Branch at design time: `visual-report`.
- Baseline version/commit: `p0b-stable` at
  `fc9b29ce387f52d5da92be8fc68ce171727f872a`.
- Dependency/lock baseline: `pyproject.toml` + committed `uv.lock`; Python
  `>=3.12,<3.13`; existing Pydantic/Ruff/pytest.
- Source status before design publication: clean. The documentation package is
  the only intended change from this design session.

## Supplied asset locations and implementation change permissions

| Asset ID | Location/access method | Delivery owner/date | May reuse/transform/migrate/replace/create | Protected or prohibited changes | Acceptance evidence |
|---|---|---|---|---|---|
| `DATA-RLINF-TRANSCRIPT` | `artifacts/p0b-ingest/p0b-rlinf-2026/segments.jsonl` | Existing P0-B / 2026-08-26 | Read only for content mapping | No overwrite/rescore/resegment | Source refs validate |
| `META-RLINF` | `artifacts/p0b-ingest/p0b-rlinf-2026/manifest.json`, `eval/p0b/corpus.jsonl` | Existing P0-B | Read attribution/duration/rights | No modification | Footer and rights review |
| `MEDIA-RLINF` | Fixed MP4 under `eval/p0b/media/` | Existing P0-B | Read and derive local frames | No upload, redistribution, transcoded replacement, or source edit | Asset manifest/contact review |
| `REF-TUGEKUAI` | `/Users/tristana/Desktop/"图个快"效果图.png` | Owner / 2026-08-30 | Inspect visual principles | Do not copy/distribute as output asset | Original design review |
| `V0-ARTIFACTS` | `artifacts/visual-report/v0-rlinf/` | Implementer | Create/replace bounded plan/assets/HTML/screenshots | Must stay local/ignored | Definition of done |

## Real production entry points and runtime path

There is no production path. The real V0 entry point is:

```bash
uv run python -m video_evidence_agent.visual_report render \
  --plan artifacts/visual-report/v0-rlinf/report-plan.json \
  --assets artifacts/visual-report/v0-rlinf/assets.json \
  --output artifacts/visual-report/v0-rlinf/report.html
```

Runtime path: CLI → JSON read → Pydantic/cross-reference/path validation → closed
component mapping → document composition → safe local replace → stdout summary.

## Canonical state owner and status mappings

| Concept | Authority | UI/DB/queue/provider/external mapping | Conflict rule |
|---|---|---|---|
| V0 stage/status | `docs/visual-report/V0-STATUS.md` under owner authority | None | Latest explicit owner message wins; then update docs |
| Requirements gate | Validator-generated `requirements-readiness.json` | None | Generated file wins |
| Report semantics | Valid current plan/assets | Rendered HTML | Rerender; do not hand-edit HTML |
| Visual rules | Renderer source | Rendered CSS/SVG | Source wins; screenshot review validates |

## Mocks, stubs, deprecated paths, duplicates, and contract drift

Synthetic unit fixtures are allowed; the real integration artifact uses the
actual local transcript/frames. No provider mock or pipeline stub is needed.
P0-A/P0-B CLI/retrieval/eval paths are existing and out of V0 scope, not
deprecated. There must be no second HTML/PNG renderer or duplicate schema model.
Schema drift is caught by version and fixtures.

## Capability-fit matrix

| Capability | State | Baseline evidence | Gap | Change layer | Owner | Acceptance |
|---|---|---|---|---|---|---|
| Local video/transcript ingest | `SUPPORTED` | FFmpeg/MLX Whisper/VideoSegment P0-B artifacts | None for V0 | Reuse read-only | Existing project | Fixed fixture readable |
| Structured report plan | `MISSING` | No current Visual Report schema | Bounded contracts | New visual-report module | Implementer | Contract tests |
| Deterministic visual renderer | `MISSING` | No current report renderer | Components/design system/CLI | New visual-report module | Implementer | Real HTML + screenshots |
| Manual keyframes | `PARTIAL` | FFmpeg exists; no V0 asset manifest | Extract/select/record | Local artifacts | Implementer | 2–4 useful assets |
| Topic mapping/planning automation | `MISSING` | Explicit V0 exclusion | Deferred V1 | None in V0 | Owner | Separate future acceptance |
| Hosting/accounts/operations | `MISSING` | No service | Not needed/prohibited | None | Owner | Not applicable |

## Business, project adapter/overlay, and shared platform boundaries

The new module is a project-owned visual-report experiment. It may reuse generic
local ingest artifacts but must not adapt retrieval/evidence/eval into the new
product. No shared framework/platform change is required.

## File and module change scope

### Create

- `src/video_evidence_agent/visual_report/` with the smallest models, renderer,
  components/design tokens, error handling, and `__main__.py` required.
- `tests/test_visual_report.py` and minimal synthetic fixtures, split only if the
  file becomes harder to understand.
- Local ignored `artifacts/visual-report/v0-rlinf/` outputs.

### Modify

- `docs/tasks/VISUAL-REPORT-V0-RENDERER.md` implementation evidence.
- `docs/visual-report/V0-STATUS.md` implementation state/history.
- Existing package `__init__.py` only if Python import exposure genuinely requires
  it. The required module entry point should avoid modifying the existing global
  CLI or `pyproject.toml`.

### Protected or prohibited

- `eval/p0b/**`, existing `artifacts/p0b-*/**`, and P0-B task/history evidence.
- Existing retrieval, answering, Evidence Gate, P0-B schemas/eval/reporting.
- `pyproject.toml`/`uv.lock` for convenience-only dependencies.
- Media publication, hosting config, database, queue, service, Agent/model/RAG,
  automatic ASR/mapping/planning/keyframe modules, multiple themes/exporters.

### Cross-module contract owners

Existing `VideoSegment` and ingest manifest contracts remain owned by stable
P0-B code. The V0 module reads their serialized artifacts as authoring evidence
but does not change or re-export those contracts. V0 plan/asset schemas are owned
only by the V0 renderer until owner acceptance and later stabilization.

## Existing public contracts and dependency policy

The installed project script `video-evidence` and existing P0 commands remain
unchanged. The V0 public prototype contract is the documented module command and
schema versions. Use existing dependencies; follow uv for any proven dependency
exception and update `uv.lock` in the same change. Do not commit `.venv`.

## Environment and external resources

| Variable/resource name | Purpose | Required environments | Provisioning owner | Secret |
|---|---|---|---|---|
| Python 3.12 + project `.venv` | Run source/tests | Local implementation | Existing project/owner | No |
| `ffmpeg`, `ffprobe` on PATH | Extract candidate frames | Implementation Phase S1 | Owner | No |
| Local browser | Visual check/screenshots | Implementation Phase S5 | Owner | No |
| Network/provider credentials | None | None | None | Not applicable |

## Local, fake, sandbox, and test-provider setup

Use the existing local uv environment. Unit tests use synthetic text and tiny
local image fixtures. The real RLinf assets remain ignored/local. No fake or real
model/provider setup is allowed or needed.

## Commands

| Check | Command | Working directory | Expected evidence |
|---|---|---|---|
| Format | No new formatter gate; keep edited Python Ruff-compatible | Repository root | Clean diff and lint |
| Lint | `uv run ruff check .` | Repository root | Exit 0 |
| Typecheck | Not configured in current project | Repository root | Not applicable |
| Build | Not required for local module prototype | Repository root | Import/CLI tests cover entry point |
| Unit/contract/failure/recovery | `uv run pytest -q tests/test_visual_report.py` | Repository root | Exit 0 |
| Full regression | `uv run pytest -q` | Repository root | Exit 0 |
| Integration | Required render command shown above | Repository root | Exit 0 and output summary |
| Offline visual | Open final HTML at 1080 px and about 390 px | Local browser | Screenshots; zero external requests |
| Diff hygiene | `git diff --check` | Repository root | Exit 0 |

## Migration, compatibility, feature flags, rollout, and rollback

No migration, feature flag, or deployment. The V0 schema is explicitly
provisional. Roll back V0 source/docs through version control and delete/regenerate
the bounded local artifact root. Never roll back or rewrite frozen P0-B history.

## Baseline-preservation checks

- Review `git status --short` before and after work; preserve unrelated user changes.
- Review `git diff --name-only` for protected paths.
- Run full pytest and Ruff.
- Confirm no P0-B manifest/result/eval artifact changed.
- Confirm no provider call, external URL load, deployment config, or dependency
  was added outside a documented observed need.

## External blockers and required shared-framework changes

None. If fixed source media or a local browser is unavailable, record the exact
blocker and stop the visual acceptance path; do not expand scope or fetch a remote
replacement. No shared-framework change is authorized.
