# Video Visual Report V1-A — Engineering Context

## Documentation and implementation separation

- This skill output is requirements, technical design, decisions, evaluation
  protocol, and implementation handoff documentation only.
- The separate implementation phase uses the repository's approved builder
  workflow after a bounded implementation task is published and authorized.
- Entry requires validator-generated readiness plus an explicit Owner message
  authorizing V1-A implementation. Neither condition authorizes V1-B/C.

## Selected grade and implementation/runtime boundary

- Grade: `G1 PROTOTYPE`.
- Selection method: AI recommendation explicitly confirmed by the Owner.
- User-confirmation evidence: “V1-A 按 G1 PROTOTYPE 继续设计。”
- Permitted implementation/runtime scope: one local foreground transcript-to-HTML
  path; three fixed transcripts, one product run each; one accepted Mapper and
  one accepted Planner proposal per successful run; at most one identical,
  recorded technical retry shared by the run; deterministic compilation and
  desktop/mobile product review.
- Prohibited scope: product code changes in this design phase; and in later
  V1-A implementation, MP4/ASR orchestration, frames/assets, OCR/VLM, Agent,
  LangGraph, RAG, database/queue/service/API/UI/deployment, public publishing,
  multi-template/free-layout work, or V1-B/C.
- Next-grade compatibility constraints: keep source and run identities stable,
  version schemas/prompts, preserve current renderer contracts, and make later
  adapters addable without turning proposals into canonical authority.

## Downstream framework contract

- Status: `NOT_APPLICABLE` for an Agent framework; required repository/runtime
  primitives are fixed below.
- Framework/version: project-owned Python `>=3.12,<3.13`, Pydantic 2 contracts,
  current OpenAI Python SDK, and existing deterministic visual-report renderer.
- Hypha recommendation disposition: `NOT_APPLICABLE` because V1-A is not an
  Agent, has no tools, graph, runtime memory, workspace execution, or multi-agent
  topology.
- Product implementation strategy: `FRAMEWORKLESS` project-owned orchestration.
- Required public capabilities: explicit provider configuration,
  one accepted DeepSeek JSON-object proposal per stage, versioned shallow
  semantic proposals, observable non-semantic normalization/source resolution,
  one explicit technical retry budget, append-oriented local artifacts,
  replay/compiler, screenshots, and the current V0 render command.
- Compatibility envelope: existing `VideoSegment`, ingest `manifest.json`,
  `visual-report.v0-prototype`, `visual-report-assets.v0-prototype`, uv lock, and
  existing `video-evidence` commands remain compatible.
- Prohibited private copies or assumptions: do not copy P0-B answer/evidence
  semantics, alter frozen evaluation, depend on provider-specific hidden retry,
  or introduce framework-private types into public artifacts.
- Target repository/output: this repository; ignored local
  `artifacts/visual-report/v1a/<run-id>/` plus versioned evaluation contracts.

## Agent module adoption matrix

Although the package includes AI generation, it is explicitly not an Agent.
Routes below make that non-adoption and each project-owned seam explicit.

| Module | Route | Dependency/ref | Why | Customization boundary | Canonical owner | Compatibility contract | Tests/evidence | Upgrade owner | Rollback/fallback |
|---|---|---|---|---|---|---|---|---|---|
| Domain/workflow | `PROJECT_OWNED` | Existing V1-A `visual_report` planning modules | Two fixed sequential stages are simpler than a workflow framework | Restore canonical mapping/planning; deterministic compilation only | V1-A planning module | `TASK-VR1A-*` order/states | Integration/state tests | Repository Owner | Revert new changes while preserving failed evidence; no runtime fallback |
| Runtime/FSM | `PROJECT_OWNED` | `run.json` state enum | Persist terminal evidence and prevent implicit success | One foreground run; no scheduler | Run recorder | States in `03-functional-spec.md` | Transition/cancellation tests | Implementer | Preserve run evidence; start new run after fix |
| Events/trace/replay | `PROJECT_OWNED` | Local JSON/JSONL artifacts | Honest call and failure evidence | Non-secret metadata and saved proposals | Run recorder/evaluator | Versioned event/call shapes | Replay and failure fixtures | Implementer | Reader supports only declared versions |
| Tools/MCP | `NOT_APPLICABLE` | None | Models have no tool authority | No tool calls | None | None | Scope review | Owner | None |
| Memory/context | `PROJECT_OWNED` | Deterministic full-transcript context builders | Two bounded request contexts, no persistent model memory | Current transcript/map only | Planning module | Limits and prompt versions | Boundary/prompt-injection tests | Implementer | Reject oversize input |
| Execution/workspace | `NOT_APPLICABLE` | None | Model cannot execute code or mutate files | Local Python process owns writes | Local operator | Explicit artifact root | Side-effect review | Owner | None |
| Prompt/inference/models | `PROJECT_OWNED` | Existing OpenAI-compatible SDK + DeepSeek endpoint + two versioned role prompts | Product-specific roles and semantic-v2 schemas | One accepted shallow JSON proposal per stage; normalization is project-owned and logged | Planning provider adapter | Existing IDs only; no semantic fabrication or provider fallback; at most one identical recorded technical retry per run | JSON request, attempt, normalization/replay and product-run evidence | Implementer/Owner | Technical-inconclusive after retry; GLM/Qwen/other model not used inside the task |
| Storage/data/artifacts | `PROJECT_OWNED` | Local filesystem | G1 needs inspectable runs, not a database | Unique immutable run paths | Run recorder | Layout in `05-data-memory.md` | Duplicate/retention/replay checks | Owner | Owner-controlled archive/delete |
| Serving Cache/WorkCache | `NOT_APPLICABLE` | None | No service or cache | None | None | None | Dependency review | Owner | None |
| Policy/identity/approval | `PROJECT_OWNED` | CLI preconditions + Owner gates | Enforce scope/phase authority without account system | Local operator; Owner accepts/promotes | Owner | No publish/deploy/V1-B/C | Status/diff review | Owner | Stop |
| Evaluation/testing | `PROJECT_OWNED` | Pytest, fake adapter, product review cards and browser screenshots | V1-A quality needs deterministic and human evidence | Three fixed videos × one product run, reviewed at 1080 px and about 390 px | Implementer + Owner | Protocol in `09-test-acceptance.md` | Tests, three reports, six screenshots and Owner rubric | Owner | New complete three-video product revision after change |
| Product surface | `PROJECT_OWNED` | Existing `build-from-transcript` subcommand + existing HTML | Smallest local surface | No API/UI | Visual-report module | Existing render output | CLI/render tests | Owner | Existing V0 render remains |
| Operations | `NOT_APPLICABLE` | Foreground local process only | No hosted operation | Timeout and visible failure only | Local operator | No SLO/support promise | Failure trace | Owner | Explicit new run |

## Required framework capability map

| Capability | Required public contract | Requirements | Acceptance evidence |
|---|---|---|---|
| Input/output contracts | Versioned shallow raw v2 schemas, normalization ledger, canonical Pydantic/V0 schemas and stable JSON artifacts | Existing IDs only; provider extras discarded visibly; final lists/text bounded | Contract examples, normalization rules and invalid fixtures |
| Source adapters and lineage | Read-only manifest/segments adapter and deterministic Topic Resolver/compiler | Exact final ID/time/source propagation plus overlap/uncovered diagnostics | Source-resolution and replay |
| Tasks, state, and recovery | Sequential local FSM with terminal failure/cancel states | No successful partial output; at most one eligible identical technical retry per run, with both attempts retained | Transition, retry eligibility/exhaustion, cancellation and duplicate-ID tests |
| Policy, permissions, and approval | Owner phase gates plus local CLI scope | No publish/deploy/V1-B/C; model has no actions | Task/status and protected-diff review |
| Memory and artifacts | Current-run contexts and unique local artifact directory | No conversation/vector/database memory; retain failures | Layout and retention tests |
| Evaluation and versioning | Frozen prompts/model/source/compiler/cards and three declared product runs | New complete three-video revision after any material change | Product manifest, artifact inventory and review audit |
| Observability and operations | Non-secret config, stage, call, usage, latency, and error records | Cost `unavailable` unless authoritative; no uptime claim | Trace/failure inspection |
| Tenant/customer lifecycle | Not applicable | One Owner/local prototype | Scope review |

## Implementation authority matrix

| Decision | Class | Decision owner | Allowed envelope | Prohibited | Acceptance evidence |
|---|---|---|---|---|---|
| Grade, stage, fixtures, two semantic roles | fixed constraint | Owner | G1 V1-A product prototype over three videos | Merge roles, broaden stages, or present it as a stability measurement | User evidence and call trace |
| Full transcript external processing | fixed constraint | Owner | Three named transcripts to configured text provider | Media upload or public redistribution | Source/run manifest |
| Source IDs/timestamps/lineage | required invariant | Owner | Model selects existing IDs; code binds canonical values | Model-created IDs/times or unknown refs | Binder/contract tests |
| Renderer/layout authority | required invariant | Owner | Existing typed semantic blocks and deterministic renderer | Model HTML/CSS/SVG/style/layout/assets | Schema and render tests |
| Failure/evidence behavior | required invariant | Owner | Unique runs, terminal state, all attempts and every allowed normalization retained; one explicit identical technical retry per run | Hidden/additional retry, valid-semantic regeneration, semantic repair, fallback, or overwrite | Raw-normalized-final attempt/replay evidence |
| Exact model identity | implementation-delegated | Owner sets envelope; implementer selects | Explicit compatible text model, frozen and recorded | Implicit default, insufficient context, fallback | `DEC-VR1A-048` + run snapshot |
| Internal module/function names | implementation-delegated | Implementer | Small project-owned code within approved paths | Framework/service abstraction | Code review and tests |
| Prompt wording before freeze | implementation-delegated | Implementer | One versioned prompt per role satisfying contracts | Role merge or post-freeze selective tuning | Prompt snapshot and product revision |
| Historical six-run thresholds/protocol | closed historical constraint; not current prototype acceptance | None | Preserve prior requirements and evidence unchanged | Reuse it as the current denominator or overwrite it | `DEC-VR1A-049` plus historical manifests |
| Historical Goal recovery after v3 failure | closed historical authority | None | Preserve its 22 candidates, 20 failed runs, and 36/36 calls | Continue or relabel the exhausted loop | `DEC-VR1A-051/052`, frozen commit `4ba28bf1b3288a6fb77bcc27378a45a69cd2b895` |
| Canonical provider-conformance continuation | closed historical authority | None | Preserve the completed two-strategy no-go and its artifacts | Continue calls, mutate results, or treat it as current product acceptance | `DEC-VR1A-053/054`, strategy registry, manifests, call ledger and terminal |
| Strict-boundary isolation | rejected/cancelled | None | Retain card as never-executed design evidence | Official OpenAI credential/call or use as current authority | `DEC-VR1A-058`, cancelled task/status |
| Current semantic-v2 product prototype | Owner-confirmed contract; execution not authorized by this design session | Implementer after separate Owner execution instruction | Two independent semantic stages; existing DeepSeek JSON-object tuple; Mapper spans and Planner content units; logged non-semantic normalization; one product run per video; one shared technical retry per run; 9-call max; six screenshots | Semantic rewrite/merge/split, valid-semantic retry, fallback/provider comparison, per-video tuning, canary/formal loop | `DEC-VR1A-061`, task card, product manifest, attempt ledger and Owner content/visual review |
| V1-B/C, G2, production, publishing | prohibited | Owner | Separate future requirements and authorization | Automatic continuation | New Owner decision |

All implementation-facing decisions now have a fixed, invariant,
implementation-delegated, or prohibited classification. The independent
validator remains the sole readiness authority.

## Project mode

- Greenfield or existing system: existing system; new bounded V1-A capability.
- Project/repository root: `/Users/tristana/Develop/video-evidence-agent`.
- Branch: `visual-report`.
- Original requirements baseline: `6576d1e8a0df3aa7288a6b9c84b6615114d9decc`.
- Current frozen code/evidence baseline after
  `VR-V1A-PROVIDER-CONFORMANCE-004`:
  `e72503f5b20831c1e86a1b72c93fb4c4f7debe2a`.
- Dependency/lock baseline: `pyproject.toml` with Python
  `>=3.12,<3.13`, `openai>=3.3.1`, `pydantic>=2.13.4`; existing `uv.lock`.
- Source status at the start of the current requirements redesign: branch
  `visual-report` was clean at commit
  `e72503f5b20831c1e86a1b72c93fb4c4f7debe2a`. The current requirements/task
  edits are documentation-only work; preserve them rather than resetting or
  reinitializing.

## Supplied asset locations and implementation change permissions

| Asset ID | Location/access method | Delivery owner/date | May reuse/transform/migrate/replace/create | Protected or prohibited changes | Acceptance evidence |
|---|---|---|---|---|---|
| `ASSET-VR1A-KLING-TRANSCRIPT` | `artifacts/p0b-ingest/p0b-kling-2024/{manifest.json,segments.jsonl}` | Existing P0-B / available | Read and snapshot only | No rewrite, relabel, publish, or media upload | 43 segments; manifest match |
| `ASSET-VR1A-RLINF-TRANSCRIPT` | `artifacts/p0b-ingest/p0b-rlinf-2026/{manifest.json,segments.jsonl}` | Existing P0-B / available | Read and snapshot only | Same; V0 plan is not automatic Gold | 46 segments; manifest match |
| `ASSET-VR1A-WUYI-TRANSCRIPT` | `artifacts/p0b-ingest/p0b-wuyi-goals/{manifest.json,segments.jsonl}` | Existing P0-B / available | Read and snapshot only | No rewrite, relabel, publish, or media upload | 38 segments; manifest match |
| `ASSET-VR1A-V0-CONTRACTS` | `src/video_evidence_agent/visual_report/{models.py,renderer.py,__main__.py}` | V0 / current baseline | Import/reuse public contracts; modify only for an observed regression that cannot be handled in the new adapter and is separately evidenced | No aesthetic redesign, new template, image automation, or schema reinterpretation | Existing visual-report tests and required render command |
| `ASSET-VR1A-PROVIDER-PATTERN` | `src/video_evidence_agent/answering.py` | P0 / current baseline | Reuse SDK/config/trace lessons, not module semantics | Do not alter answer path or reuse P0 model variable implicitly | P0 tests unchanged |
| `ASSET-VR1A-REVIEW-CARDS` | Existing `eval/visual-report-v1a/review-cards/` | Implementer-created; Owner review pending | Derive and snapshot an explicit semantic-v2 product card covering content, grounding, cross-video fit and both viewports | No post-run target editing inside the product revision; no auto-filled Owner score | Existing card validation plus new product revision snapshot |
| `ASSET-VR1A-RUNS` | Existing ignored `artifacts/visual-report/v1a/<run-id>/` | Historical implementation/recovery plus future Goal | Create only three new unique product directories and their derived artifacts | Never overwrite or selectively delete any historical or new attempt | Run inventory/product-set audit |

## Real entry points and runtime path

Current real visual-report entry point:

```bash
uv run python -m video_evidence_agent.visual_report render \
  --plan PATH --assets PATH --output PATH
```

Current V1-A entry point:

```bash
uv run python -m video_evidence_agent.visual_report build-from-transcript \
  --manifest PATH --segments PATH --run-id RUN_ID --output-root artifacts/visual-report/v1a
```

Runtime composition:

```text
CLI
 -> config/source validation
 -> unique run recorder
 -> full transcript context -> Topic Mapper provider adapter (call 1)
 -> strict proposal -> deterministic Topic Map binder
 -> full transcript + canonical Topic Map -> Report Planner adapter (call 2)
 -> strict proposal -> deterministic V0 plan compiler
 -> empty current AssetManifest -> existing render_report
 -> terminal run.json + report.html
```

The current implementation supplies this path. The next Goal may make the
smallest changes inside its existing modules, but the semantic boundaries,
public command behavior, artifacts, calls, and states remain fixed.

## Canonical state owner and status mappings

| Concept | Authority | UI/DB/queue/provider/external mapping | Conflict rule |
|---|---|---|---|
| Source text/time | Existing manifest + segments snapshot | Provider sees a serialized copy; no database | Source artifact wins; mismatch fails before call |
| One run's execution state | `<run-id>/run.json` | No UI/DB/queue; provider success does not advance state by itself | Recorder transition guard wins |
| Topic identity/time | Canonical Topic Map from deterministic binder | Proposal contains source IDs only | Binder output wins; unknown/missing IDs fail |
| Report IDs/time/refs | Compiled V0 `report-plan.json` | Proposal is retained but non-canonical | Compiler output wins; compile failure means no success plan |
| HTML completion | `run.json=RENDERED` plus current renderer success | File presence alone is insufficient | State and artifact completeness must agree or run fails |
| Product quality | Versioned product-review output + Owner content/visual rubric and decision | `RENDERED` or schema success is only execution evidence | Owner acceptance evidence wins |
| Package readiness | Validator-generated `requirements-readiness.json` | Narrative docs cannot self-declare it | Generated report wins |

## Mocks, stubs, deprecated paths, duplicates, and contract drift

- Unit/integration tests use a local fake provider implementing the same two
  call boundary; it must expose admitted/provider/model call counts.
- Saved raw proposal fixtures support deterministic replay with
  `provider_calls/model_calls=0/0`.
- Existing `answering.py` is not a V1-A adapter and must not be modified into
  one; its question/Top-K contract and `VIDEO_EVIDENCE_MODEL` setting remain P0.
- The hand-authored V0 plan remains reference evidence, not a fallback/stub for
  a failed Planner.
- Duplicate schemas or compatibility shims are not added. Contract drift
  creates a new explicit schema/prompt/product revision.

## Capability-fit matrix

| Capability | State | Baseline evidence | Gap | Change layer | Owner | Acceptance |
|---|---|---|---|---|---|---|
| Timestamped transcript source | `SUPPORTED` | Three validated `VideoSegment` JSONL fixtures and implemented read-only loader | None in current scope | Reuse unchanged | Existing source owner | Contract/boundary tests |
| DeepSeek provider transport | `PARTIAL` | Existing Responses JSON-Schema adapter and retained DeepSeek calls work as transport, but strict proposal conformance failed; official DeepSeek docs provide Chat Completions JSON Output and warn of occasional empty content | Add one frozen Chat Completions `json_object` v2 path using the existing credential and one run-scoped identical technical retry for eligible transport/JSON failures | Existing provider adapter | Implementer | Exact request, retry eligibility/exhaustion and three-product-run attempt evidence |
| Topic Mapper | `PARTIAL` | V1 strict schema/binder and historical failures exist | Add v2 approximate topic spans/importance/representatives plus deterministic Topic Resolver and coverage diagnostics; preserve v1 | Existing planning module | Owner/implementer | V2 raw-normalized-canonical fixtures, replay and product evidence |
| Report Planner | `PARTIAL` | V1 typed proposal/compiler exists; no DeepSeek conformance run rendered | Add v2 flat semantic content units/advisory types and observable non-semantic normalizer; preserve current V0 compiler/renderer authority | Existing planning module | Owner/implementer | V2 normalization, grounding, compile/render and three-report rubric evidence |
| Deterministic plan compiler | `PARTIAL` | Existing compiler owns IDs, times, refs, metrics, empty assets, and V0 contracts | Extend with closed non-semantic v2 normalization rules and ledger; never rewrite, merge or split semantic units | Existing planning module | Implementer | Raw-normalized-final diff, 0/0 replay, V0 regression |
| V0 renderer and typed plan | `SUPPORTED` | Current models/renderer/tests and local report | V1-A adapter only | Reuse unchanged | V0 module | Existing + integration regression |
| Run evidence/state | `SUPPORTED` | Unique retained run directories, state/call traces, replay, and 20 historical failed canaries exist | Three new product identities, attempt ordinals/reasons and prototype revision fields | Existing recorder/runtime | Implementer | State/retry/product-set tests and preservation audit |
| Quality evaluation | `SUPPORTED_NO_CURRENT_PRODUCT_RESULT` | Historical cards/evaluator exist; v3 aggregate is invalid and no automated report has reached Owner review | Versioned product review package centered on three reports, grounding, cross-video structure and six screenshots | Existing evaluator/review package | Owner/implementer | Three-report package or explicit technical-inconclusive/content-insufficient/contract-change stop |
| Hosting/accounts/operations | `MISSING` but prohibited | No service | None in G1 | No change | Owner | Not applicable review |

## Business, project adapter/overlay, and shared platform boundaries

All new behavior belongs to the project-owned visual-report module and its
evaluation package. Reuse public source/renderer/provider-library contracts;
do not change a shared framework or retrofit retrieval, answering, Evidence
Gate, or P0-B Eval into V1-A. No platform exception or shared-framework work is
required.

## File and module change scope

The initial create envelope has already been delivered. The continuation should
modify the few existing V1-A modules and avoid a new subsystem.

### Existing implementation to modify when evidence requires it

- `src/video_evidence_agent/visual_report/planning.py` for canonical prompts,
  payloads, examples, schemas, binders, and compiler behavior.
- `planning_runtime.py` for the frozen DeepSeek JSON-object transport, product
  snapshots, explicit technical retry, raw/normalized artifacts, and non-secret
  attempt evidence.
- `evaluation.py` only for the current product-review artifact and rubric gaps.
- `tests/test_visual_report_planning.py` for v2 normalization, anti-fabrication,
  exact transport, replay, and regression coverage; split only if materially clearer.
- One versioned three-video product manifest, review cards/screenshots and new
  ignored run outputs under the existing V1-A eval/artifact roots.

### Modify

- `src/video_evidence_agent/visual_report/__main__.py` only if the existing
  subcommand needs a reproduced, task-required strategy argument or evidence fix.
- `src/video_evidence_agent/visual_report/__init__.py` only if public constants
  genuinely need export.
- V1-A task/status/evidence documents in the same implementation session when
  status changes.
- Existing V0 renderer/models only for a reproduced compatibility defect that
  cannot be solved in the V1-A adapter; record and test the exception.

### Protected or prohibited

- `eval/p0b/**`, existing `artifacts/p0b-*/**`, frozen P0-B evidence/history,
  retrieval, answering, Evidence Gate, and evaluation conclusions.
- V0 report content/assets/screenshots and visual redesign unrelated to an
  observed V1-A compatibility defect.
- `pyproject.toml` and `uv.lock` unless an observed blocker proves the existing
  OpenAI/Pydantic stack insufficient; convenience dependencies are prohibited.
- MP4/ASR/keyframe/OCR/VLM/RAG/Agent/LangGraph/database/queue/service/API/UI,
  deployment/hosting, publishing, V1-B, and V1-C code.

### Cross-module contract owners

- Source ingest owns `VideoSegment` and manifests.
- V1-A binder/compiler owns new proposal/canonical planning schemas.
- V0 owns the current renderer plan/asset contracts and HTML behavior.
- V1-A recorder owns run lifecycle; evaluator/Owner owns quality conclusions.
- Owner alone owns stage promotion and fixture publication rights.

## Existing public contracts and dependency policy

Keep the installed `video-evidence` script and all existing commands unchanged.
Use the existing `openai`, Pydantic, dotenv, pytest, and Ruff dependencies. New
schema versions are provisional but explicit. If a demonstrated dependency gap
requires a change, use `uv add`/`uv add --dev`, update `uv.lock`, explain the
observed need, and keep `.venv` untracked; the default V1-A plan adds none.

## Environment and external resources

| Variable/resource name | Purpose | Required environments | Provisioning owner | Secret |
|---|---|---|---|---|
| `OPENAI_API_KEY` | Authenticate the existing DeepSeek endpoint through the installed compatible SDK; does not require an OpenAI account | Real Development runs only | Local Owner | Yes; log presence only |
| `OPENAI_BASE_URL` | Exact DeepSeek endpoint | Semantic-v2 product runs | Local Owner | Treat query/embedded credentials as secret; log normalized label only |
| `VISUAL_REPORT_MODEL` | One explicit accessible DeepSeek text model | Every semantic-v2 product run | Implementer selects inside `DEC-VR1A-048/058/061`; Owner provisions access | No, but operational metadata |
| `VISUAL_REPORT_TIMEOUT_SECONDS` | Per-call timeout; current default 120 | Real and failure tests | Implementer | No |
| Python 3.12 + project `.venv` | Source/tests/CLI | Local development | Existing project/Owner | No |
| Local artifact root | Unique run/evidence output | All V1-A runs | Operator | No; may contain full transcript/model response |
| Network | Two base provider requests per successful run, with at most one eligible retry shared by that run | Real product runs only | Owner | Not applicable |

No secret values belong in documentation, commands, status files, logs, or
model prompts.

## Local, fake, sandbox, and test-provider setup

- Use the existing project-local uv environment and a writable project-specific
  `UV_CACHE_DIR` if the default cache is unavailable.
- All source/schema/compiler/CLI/replay/failure tests run with a local fake
  adapter. Provider-free paths must prove `provider_calls/model_calls=0/0`.
- The completed DeepSeek provider-conformance strategies are closed historical
  evidence and the official-OpenAI isolation proposal is cancelled.
- Current v2 may admit one existing DeepSeek Chat Completions JSON-object tuple
  only after local normalization/replay/retry tests pass, configuration
  validates, and all three product identities freeze. There is no canary-to-
  formal loop in this G1 product prototype.
- Diagnostics check credential presence only and never print/read secret values.

## Commands

These are later implementation commands; they are not executed during this
requirements-only phase.

| Check | Command | Working directory | Expected evidence |
|---|---|---|---|
| Format | No separate formatter is configured; keep edits Ruff-compatible | Repository root | Clean diff |
| Lint | `UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run ruff check .` | Repository root | Exit 0 |
| Typecheck | Not configured | Repository root | Not applicable |
| Build | Module import and CLI parser tests | Repository root | Exit 0; no packaging change |
| Unit/contract | `UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q tests/test_visual_report_planning.py` | Repository root | Exit 0; fake call counts exact |
| Integration | Same targeted suite plus synthetic `build-from-transcript` CLI case | Repository root | Plan/assets/HTML and terminal state |
| Failure/recovery | Targeted malformed/ref/timeout/cancel/duplicate/replay and retry-budget cases | Repository root | Stable categories; exactly one eligible identical retry at most; no overwrite |
| Replay/regression | `UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q` | Repository root | All tests pass; V0/P0 behavior preserved |
| Diff hygiene | `git diff --check` and protected-path diff review | Repository root | No whitespace/protected changes |
| Product prototype | Three explicit `build-from-transcript` invocations plus product-review and screenshot commands | Repository root | Three retained runs, three HTML reports, six screenshots and pending Owner rubrics; or an exact non-success terminal |

## Migration, compatibility, feature flags, rollout, and rollback

No migration, backfill, feature flag, deployment, or online rollout. The new
subcommand is additive and local. Existing V0 plan/asset schema versions and
render command remain stable. Roll back source/docs with version control while
preserving historical and current run directories; after a prompt/model/source/
compiler/reviewer change, issue a new complete three-video product revision
rather than mutate or selectively replace the prior set.

## Baseline-preservation checks

- Confirm branch and baseline before implementation; preserve unrelated user
  work and the requirements package.
- Compare changed paths against the create/modify/protected lists above.
- Run targeted tests first, then full pytest and Ruff because the new CLI and
  provider boundary touch a shared package.
- Re-run the existing V0 render contract with an empty and the existing real
  asset manifest as applicable; confirm current HTML behavior.
- Confirm no existing transcript, manifest, P0-B result/eval/history, V0 report
  artifact, dependency, or deployment configuration changed unexpectedly.
- Verify test/replay paths made no provider call and product paths reported one
  accepted Mapper and one accepted Planner proposal per successful run, with
  two base attempts and no more than one eligible retry across the run.

## External blockers and required shared-framework changes

No shared-framework change is required. The official-OpenAI isolation is
cancelled, so no new OpenAI credential or transcript-egress authority is
needed. The semantic-v2 product contract is Owner-confirmed by
`DEC-VR1A-061`; a separate instruction is still required to authorize the
implementation/model-running session. Existing DeepSeek credential, balance,
model access and network are execution dependencies, not documentation
blockers.

## Current post-provider-conformance context

The exhausted recovery remains frozen historical `FAILED_EXPERIMENT /
DO_NOT_PROMOTE` evidence: 22 candidate manifests, 20 failed Kling canaries, and
`36/36` calls. The later provider-conformance Goal restored the canonical
content/anti-template prompts, passed provider-free regression, and evaluated
two DeepSeek Responses `json_schema` model strategies across all three videos.
All six canaries failed, `8/8` calls were retained, and no formal measurement,
evaluator aggregate, report, or rubric was created. The complete state is
frozen at `e72503f5b20831c1e86a1b72c93fb4c4f7debe2a`.

Repository inspection and retained canaries show that v1 asks the model to
satisfy exact topic limits, unique full-segment accounting, nested typed-block
unions, section/block/source bounds, global budget and cross-field topic
disposition in one response. Observed failures include 13 topics against the
12-topic cap, duplicate segment assignment, non-JSON Planner output, five
source IDs against a four-ID cap, and section/block-count validation. These are
not evidence that final source binding or V0 validation should disappear; they
show that the model-facing proposal carries too much canonical responsibility.

The Owner has no OpenAI API key and does not want to purchase one. Therefore
`VR-V1A-BOUNDARY-ISOLATION-005` is cancelled without execution. GLM/Qwen remain
optional future providers, not current dependencies.

`DEC-VR1A-061` confirms `VR-V1A-CONTRACT-SIMPLIFICATION-006` as the next
product-prototype Goal:

```text
provider-free semantic-v2 contracts and normalization/replay
  -> freeze one existing DeepSeek JSON-object tuple, prompts, compiler and three identities
  -> one product run per video, two semantic stages per complete run
  -> at most one identical recorded technical retry shared by each run
  -> compile/render three reports and capture 1080 px plus about 390 px screenshots
  -> product review, full regression, Owner review
```

Mapper v2 provides approximate spans and representative IDs instead of exact
partition; Planner v2 provides flat semantic content units instead of final V0
typed objects. The Topic Resolver/normalizer may apply only the closed,
observable non-semantic rules in the task card. It never invents or rewrites
content, merges or splits semantic units, and every final Hero/block retains a
valid model-selected source ID. The product set has six base calls and a
nine-call absolute maximum. Schema-first-hit and retry counts are diagnostics;
content, grounding, cross-video structure fit and real desktop/mobile visual
results determine the Owner review. The current edits are documentation-only;
implementation and provider execution remain `NOT_STARTED` until a separate
Owner instruction starts the Goal session.
