# Engineering Context

## Repository snapshot

Repository: `/Users/tristana/Develop/video-evidence-agent`  
Branch during Design Baseline drafting: `visual-report`  
Accepted V1.1 product baseline: `2bce883`  
Documentation starting HEAD: `2eae3545d659b03fb2da0a6f7490e32c70e2ab18`

`2eae354` contains V1.1 status/delivery documentation after the accepted product baseline. V1.2
must build on the current working tree chosen by the Owner while preserving `2bce883` as the recorded
V1.1 product baseline. This package itself is uncommitted until the Owner requests a commit.

## Required context load for a future implementation agent

Read in this order:

1. `AGENTS.md`;
2. `docs/visual-report/V1-STATUS.md`;
3. `docs/visual-report/V1-ROADMAP.md`;
4. this package from `00-handoff.md` through `12-engineering-context.md`;
5. `CONTEXT.md` and `docs/adr/0001-integrated-bounded-visual-editorial-harness.md`;
6. only the directly affected source and tests listed below.

Historical V0/V1-A requirement packages are read-only compatibility evidence. They are not the V1.2
contract and should be opened only when a touched legacy seam requires it.

## Language and dependency workflow

- Python `>=3.12,<3.13`.
- Build backend: Hatchling.
- Pydantic `>=2.13.4` is already present and is the required typed-Artifact foundation.
- OpenAI Python SDK `>=3.3.1` is already present behind OpenAI-compatible Provider code.
- Use the project-local `.venv` and `uv run`; update `pyproject.toml` and `uv.lock` together for an
  authorized dependency change.
- Ruff targets Python 3.12 with 100-character lines.
- Pytest uses `tests/`.
- No browser automation library is currently declared; adding the smallest suitable local Browser
  Observer dependency requires future product/dependency authorization.

## Existing source contracts

### V1.1 Canonical Transcript

`src/video_evidence_agent/transcript_foundation.py`

- `TranscriptUnit` is the source-facing record with `unit_id`, `start_ms`, `end_ms`,
  `canonical_text`, retained ASR/OCR/subtitle text, `resolution`, `flags`, and `provenance`.
- `TranscriptManifest` records video/duration/mode, source status, counts, versions, warnings, and
  transcript status.
- `build_canonical_transcript` owns V1.1 source fusion.

V1.2 consumes this contract read-only. It must use Canonical Transcript units directly for Claim
evidence rather than treating the legacy 45–60 second `VideoSegment` projection as the new factual
authority. Existing ingest may still provide metadata and orchestration.

### Legacy report contract

`src/video_evidence_agent/visual_report/models.py`

- `ReportPlan` is the V0 contract.
- It couples final content to `Section` and seven visual block types.
- `SourceRef` references projected segment IDs.
- Current field length and section/block cardinality limits are legacy limits.

V1.2 must not extend this class as its public contract. Reusing small data validators or renderer
primitives is allowed only behind independent V1.2 models.

### Legacy semantic planning

`src/video_evidence_agent/visual_report/planning.py`

- Current semantic-v2 defines Topic Mapper and Report Planner proposals, prompt versions,
  normalization, adaptive planning budgets, compilation into legacy `ReportPlan`, and related
  validation.
- Current compiler enforces 3–5 sections, a maximum 32 blocks, and an 8,000-character visible-content
  ceiling.

Those prompts, Topic Map, budgets, compiler limits, and block selection are evidence for what exists,
not V1.2 compatibility requirements. They may inform calibration but must not leak visual component
selection into Editorial.

### Legacy planning runtime and RunRecorder

`src/video_evidence_agent/visual_report/planning_runtime.py`

- `RunRecorder` already provides unique run directories, state transitions, Artifact registration,
  call evidence, and retained failure handling.
- `OpenAIPlanningProvider` already snapshots public non-secret configuration, disables SDK retries,
  and uses an OpenAI-compatible client.
- `_semantic_v2_call_stage` owns current response capture and retry behavior.
- `build_from_transcript_v2` orchestrates the current semantic-v2 product path and calls the legacy
  Renderer.

Important difference: current semantic-v2 tests and call logic allow retry for some incomplete or
malformed returned outputs. V1.2 expressly forbids hidden resampling after any complete response.
Do not reuse that method without isolating and changing the V1.2 contract. Historical behavior and
tests remain untouched.

The existing `RunRecorder` is a strong reuse candidate, but V1.2 needs versioned Artifact snapshots,
Revision consumption, observation evidence, and only three canonical report outcomes. Prefer a small
V1.2 wrapper/extension over changing legacy event semantics in place.

### Renderer

`src/video_evidence_agent/visual_report/renderer.py`

- `render_report` validates the legacy plan/assets, emits self-contained HTML with inline CSS, and
  uses atomic file replacement.
- It has a desktop `.report-page` design and mobile media rules.
- Current HTML contains V0-specific fixed labels, attribution language, and a hard-coded speaker;
  these cannot be carried into a general V1.2 report unless sourced through Editorial/metadata.

Reuse escaping, asset resolution, atomic write, typography/layout tokens, or component code only
after separating them from legacy semantic assumptions. The V1.2 Renderer must consume the new
Presentation Plan and emit traceable element identities for Observation.

### CLI and Web

`src/video_evidence_agent/visual_report/__main__.py`

- Existing commands include `render`, `build-from-transcript`, `build-from-transcript-v2`, replay,
  evaluation, and local Web serving.

`src/video_evidence_agent/visual_report/web.py`

- `VisualReportWebApp` and `UrlIngestWebApp` provide loopback execution, status/report endpoints,
  URL ingest, and an in-memory single-worker FIFO queue.
- Current Web pages already avoid exposing `OPENAI_API_KEY` and translate several backend stages.

Add an explicit V1.2 selection/path with the smallest change. Do not redesign the Web Shell or
duplicate ingest/queue code.

### Shared model configuration

`src/video_evidence_agent/llm_config.py` defines:

- `OPENAI_API_KEY_ENV = "OPENAI_API_KEY"`;
- `OPENAI_BASE_URL_ENV = "OPENAI_BASE_URL"`;
- `OPENAI_MODEL_ENV = "VIDEO_EVIDENCE_MODEL"`;
- endpoint normalization for OpenAI-compatible clients.

`.env.example` currently points `OPENAI_BASE_URL` to the Zhipu OpenAI-compatible endpoint, sets
`VIDEO_EVIDENCE_MODEL=glm-5.3-flash`, and sets the visual-report timeout to 120 seconds. V1.2 should
reuse these names and one shared configuration, while keeping the stage code behind one
ModelClient/Provider Adapter.

## Suggested minimal code placement

The exact filenames are implementation-owned. The smallest isolation is a `visual_report/v1_2/`
package (or equivalently clear `v1_2_*` modules) containing:

- typed Artifacts and validators;
- Controller and run-record adaptation;
- role Prompt/Schema definitions and unified ModelClient seam;
- Presentation Vocabulary/Design System mapping;
- deterministic Renderer adapter;
- Browser Observer adapter;
- terminal classification and test fakes.

Keep the number of modules proportional to these real authority boundaries. Do not create one class
or service per role merely because the role appears in the conceptual workflow.

## Reuse matrix

| Existing capability | V1.2 action | Reason |
|---|---|---|
| V1.1 Canonical Transcript and ingest | reuse | accepted source foundation |
| projected `VideoSegment` | compatibility metadata only | Claim provenance should bind source units |
| `RunRecorder` primitives | adapt behind V1.2 identity | retained Artifact/failure behavior is useful |
| shared LLM env/config | reuse | matches single-model architecture |
| current semantic-v2 call loop | do not reuse unchanged | complete-response retry conflicts with V1.2 |
| Topic Map/ReportPlan compiler | legacy only | couples semantics to old visual blocks |
| V0 Pydantic `ReportPlan` | legacy only | explicitly not V1.2 contract |
| renderer escaping/atomic write/tokens | selective reuse | deterministic foundations are useful |
| seven component implementations | calibration candidates | no compatibility quota or requirement |
| Web/CLI/URL ingest/FIFO | minimally extend | shared product infrastructure |
| evaluation manifest patterns | adapt conceptually | unique identities/full denominator are useful |
| frozen V0/V1-A evidence | preserve | historical truth; no mutation |

## New dependency disposition

No agent framework is allowed. The only likely new dependency is a local browser automation/runtime
library for screenshot and DOM geometry collection. The future implementation agent must first
check whether an existing installed executable/library can satisfy the narrow contract. If a new
package is necessary and authorized, pin it through `uv`, record its browser/runtime version, and
avoid exposing a general browser-control abstraction.

## Test seams

Existing tests relevant to shared behavior:

- `tests/test_transcript_foundation.py`;
- `tests/test_visual_report.py`;
- `tests/test_visual_report_planning.py`;
- `tests/test_visual_report_semantic_v2.py`;
- `tests/test_visual_report_web.py`;
- `tests/test_visual_report_url_ingest.py`.

Add focused V1.2 tests rather than rewriting legacy fixtures. Fake ModelClient outputs should cover
schema, grounding, authority, retry, and Revision control. Browser tests must use a real rendered
local page for Observer behavior; a fake Observer proves Controller plumbing only.

Minimum commands for an authorized implementation are expected to follow repository conventions:

```bash
uv run pytest tests/<focused-v1-2-tests>
uv run pytest tests/test_visual_report.py tests/test_visual_report_web.py
uv run ruff check src tests
git diff --check
```

Run the full suite when shared modules or entry points change and before Owner implementation review.

## Implementation prohibitions

- Do not modify V1.1 fusion or accepted transcript behavior.
- Do not edit frozen evaluation results or selectively rerun a failed identity.
- Do not make V1.2 the default path.
- Do not add arbitrary document input, chunking, RAG, frame extraction, VLM search, or image
  generation.
- Do not add role-specific model configuration, model fallback, or general tools.
- Do not add a Patch DSL, generic workflow/state/invalidation framework, database, account system,
  deployment, or product-service infrastructure.
- Do not let Presentation or Renderer invent semantic content.
- Do not treat fake tests as real report-quality evidence.

## Handoff stopping rule

A future engineering goal stops at the state explicitly named by the Owner. A complete fake/local
vertical loop does not authorize real Provider calibration. Calibration does not authorize
Architecture Ablation beyond its declared goal, Final Spec freeze, formal locked evaluation,
product acceptance, default promotion, or deployment. Each transition needs its own recorded Owner
authority.
