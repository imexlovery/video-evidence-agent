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
  path; three fixed transcripts; exactly one Mapper and one Planner call per
  successful run; deterministic compilation; local Development measurement.
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
  provider-native schema-constrained completion for the active continuation,
  strict proposal validation, append-oriented local artifacts, deterministic
  replay/compiler, current V0 render command.
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
| Prompt/inference/models | `PROJECT_OWNED` | OpenAI-compatible SDK transport + two versioned role prompts | Product-specific roles and schemas | At most two predeclared native-schema provider/model/API strategies | Planning provider adapter | One call per stage; schema-constrained output; temperature zero; no retry/fallback | Capability evidence, fake tests, full cross-video canary | Implementer/Owner | Fail run; only the already-frozen next strategy may be evaluated |
| Storage/data/artifacts | `PROJECT_OWNED` | Local filesystem | G1 needs inspectable runs, not a database | Unique immutable run paths | Run recorder | Layout in `05-data-memory.md` | Duplicate/retention/replay checks | Owner | Owner-controlled archive/delete |
| Serving Cache/WorkCache | `NOT_APPLICABLE` | None | No service or cache | None | None | None | Dependency review | Owner | None |
| Policy/identity/approval | `PROJECT_OWNED` | CLI preconditions + Owner gates | Enforce scope/phase authority without account system | Local operator; Owner accepts/promotes | Owner | No publish/deploy/V1-B/C | Status/diff review | Owner | Stop |
| Evaluation/testing | `PROJECT_OWNED` | Pytest, fake adapter, review cards/evaluator | V1-A quality needs deterministic and human evidence | Three fixed videos × two repeats | Implementer + Owner | Protocol in `09-test-acceptance.md` | Tests plus frozen measurement | Owner | New full revision after change |
| Product surface | `PROJECT_OWNED` | Existing `build-from-transcript` subcommand + existing HTML | Smallest local surface | No API/UI | Visual-report module | Existing render output | CLI/render tests | Owner | Existing V0 render remains |
| Operations | `NOT_APPLICABLE` | Foreground local process only | No hosted operation | Timeout and visible failure only | Local operator | No SLO/support promise | Failure trace | Owner | Explicit new run |

## Required framework capability map

| Capability | Required public contract | Requirements | Acceptance evidence |
|---|---|---|---|
| Input/output contracts | Versioned strict Pydantic schemas and stable JSON artifacts | Existing IDs only; bounded lists/text; extra fields forbidden | Contract examples and invalid fixtures |
| Source adapters and lineage | Read-only manifest/segments adapter and deterministic binder | Exact ID/time/source propagation | Source accounting and replay |
| Tasks, state, and recovery | Sequential local FSM with terminal failure/cancel states | No successful partial output or in-run retry | Transition, cancellation, duplicate-ID tests |
| Policy, permissions, and approval | Owner phase gates plus local CLI scope | No publish/deploy/V1-B/C; model has no actions | Task/status and protected-diff review |
| Memory and artifacts | Current-run contexts and unique local artifact directory | No conversation/vector/database memory; retain failures | Layout and retention tests |
| Evaluation and versioning | Frozen prompts/model/source/compiler/cards and six declared runs | New revision after any material change | Revision manifest and denominator audit |
| Observability and operations | Non-secret config, stage, call, usage, latency, and error records | Cost `unavailable` unless authoritative; no uptime claim | Trace/failure inspection |
| Tenant/customer lifecycle | Not applicable | One Owner/local prototype | Scope review |

## Implementation authority matrix

| Decision | Class | Decision owner | Allowed envelope | Prohibited | Acceptance evidence |
|---|---|---|---|---|---|
| Grade, stage, fixtures, two roles/calls | fixed constraint | Owner | G1 V1-A Development measurement | Merge calls or broaden stages | User evidence and call trace |
| Full transcript external processing | fixed constraint | Owner | Three named transcripts to configured text provider | Media upload or public redistribution | Source/run manifest |
| Source IDs/timestamps/lineage | required invariant | Owner | Model selects existing IDs; code binds canonical values | Model-created IDs/times or unknown refs | Binder/contract tests |
| Renderer/layout authority | required invariant | Owner | Existing typed semantic blocks and deterministic renderer | Model HTML/CSS/SVG/style/layout/assets | Schema and render tests |
| Failure/evidence behavior | required invariant | Owner | Unique runs, terminal state, all failures retained | Hidden retry/repair/fallback/overwrite | Failure/replay evidence |
| Exact model identity | implementation-delegated | Owner sets envelope; implementer selects | Explicit compatible text model, frozen and recorded | Implicit default, insufficient context, fallback | `DEC-VR1A-048` + run snapshot |
| Internal module/function names | implementation-delegated | Implementer | Small project-owned code within approved paths | Framework/service abstraction | Code review and tests |
| Prompt wording before freeze | implementation-delegated | Implementer | One versioned prompt per role satisfying contracts | Role merge or post-freeze selective tuning | Prompt snapshot and measurement revision |
| Six-run thresholds/protocol | fixed constraint | Owner | Values in `09-test-acceptance.md` | Implementer self-approval or selective rerun | `DEC-VR1A-049` + frozen measurement |
| Historical Goal recovery after v3 failure | closed historical authority | None | Preserve its 22 candidates, 20 failed runs, and 36/36 calls | Continue or relabel the exhausted loop | `DEC-VR1A-051/052`, frozen commit `4ba28bf1b3288a6fb77bcc27378a45a69cd2b895` |
| Canonical provider-conformance continuation | implementation-delegated within fixed constraints | Implementer | Restore canonical variable content contract; predeclare at most two native-schema strategies; one full three-video canary each; first passing strategy gets one six-run formal revision; at most 24 calls | JSON-object-only admission, prompt micro-version, per-video tuning, post-freeze repair/rerun, second formal revision | `DEC-VR1A-053/054`, strategy registry, manifests, call ledger, exact terminal |
| V1-B/C, G2, production, publishing | prohibited | Owner | Separate future requirements and authorization | Automatic continuation | New Owner decision |

All implementation-facing decisions now have a fixed, invariant,
implementation-delegated, or prohibited classification. The independent
validator remains the sole readiness authority.

## Project mode

- Greenfield or existing system: existing system; new bounded V1-A capability.
- Project/repository root: `/Users/tristana/Develop/video-evidence-agent`.
- Branch: `visual-report`.
- Original requirements baseline: `6576d1e8a0df3aa7288a6b9c84b6615114d9decc`.
- Current frozen code/evidence baseline for
  `VR-V1A-PROVIDER-CONFORMANCE-004`:
  `4ba28bf1b3288a6fb77bcc27378a45a69cd2b895`.
- Dependency/lock baseline: `pyproject.toml` with Python
  `>=3.12,<3.13`, `openai>=3.3.1`, `pydantic>=2.13.4`; existing `uv.lock`.
- Source status after the failed-experiment freeze: branch `visual-report` was
  clean at commit `4ba28bf1b3288a6fb77bcc27378a45a69cd2b895`. The current requirements/task
  edits are documentation-only handoff work and may remain uncommitted when the
  next Goal begins; preserve them rather than resetting or reinitializing.

## Supplied asset locations and implementation change permissions

| Asset ID | Location/access method | Delivery owner/date | May reuse/transform/migrate/replace/create | Protected or prohibited changes | Acceptance evidence |
|---|---|---|---|---|---|
| `ASSET-VR1A-KLING-TRANSCRIPT` | `artifacts/p0b-ingest/p0b-kling-2024/{manifest.json,segments.jsonl}` | Existing P0-B / available | Read and snapshot only | No rewrite, relabel, publish, or media upload | 43 segments; manifest match |
| `ASSET-VR1A-RLINF-TRANSCRIPT` | `artifacts/p0b-ingest/p0b-rlinf-2026/{manifest.json,segments.jsonl}` | Existing P0-B / available | Read and snapshot only | Same; V0 plan is not automatic Gold | 46 segments; manifest match |
| `ASSET-VR1A-WUYI-TRANSCRIPT` | `artifacts/p0b-ingest/p0b-wuyi-goals/{manifest.json,segments.jsonl}` | Existing P0-B / available | Read and snapshot only | No rewrite, relabel, publish, or media upload | 38 segments; manifest match |
| `ASSET-VR1A-V0-CONTRACTS` | `src/video_evidence_agent/visual_report/{models.py,renderer.py,__main__.py}` | V0 / current baseline | Import/reuse public contracts; modify only for an observed regression that cannot be handled in the new adapter and is separately evidenced | No aesthetic redesign, new template, image automation, or schema reinterpretation | Existing visual-report tests and required render command |
| `ASSET-VR1A-PROVIDER-PATTERN` | `src/video_evidence_agent/answering.py` | P0 / current baseline | Reuse SDK/config/trace lessons, not module semantics | Do not alter answer path or reuse P0 model variable implicitly | P0 tests unchanged |
| `ASSET-VR1A-REVIEW-CARDS` | Existing `eval/visual-report-v1a/review-cards/` | Implementer-created; Owner review pending | Reuse and snapshot exact version for a new formal revision | No post-run target editing inside revision | Existing card validation plus new revision snapshot |
| `ASSET-VR1A-RUNS` | Existing ignored `artifacts/visual-report/v1a/<run-id>/` | Historical implementation/recovery plus future Goal | Create only new unique directories and derived artifacts | Never overwrite or selectively delete any historical or new failure | Run inventory/denominator audit |

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
| Measurement quality | Versioned evaluator output + Owner rubric/decision | `RENDERED` is only execution success | Owner acceptance evidence wins |
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
  creates a new explicit schema/prompt/measurement revision.

## Capability-fit matrix

| Capability | State | Baseline evidence | Gap | Change layer | Owner | Acceptance |
|---|---|---|---|---|---|---|
| Timestamped transcript source | `SUPPORTED` | Three validated `VideoSegment` JSONL fixtures and implemented read-only loader | None in current scope | Reuse unchanged | Existing source owner | Contract/boundary tests |
| OpenAI-compatible provider transport | `IMPLEMENTED_NOT_CONFORMANT` | Existing V1-A adapter records two stages with retry zero, but the exhausted path used JSON-object mode | Add exact native schema-constrained strategy transport and capability snapshot | Existing provider adapter | Implementer | Capability evidence, runtime request tests, cross-video canary |
| Topic Mapper | `IMPLEMENTED_CONTRACT_DRIFT` | Strict schema/binder/coverage exist; frozen failed prompt/payload forces exactly four topics and empty subtopics | Restore canonical 4–12 topics and 0–5 content-derived subtopics; anti-overfit tests | Existing planning module | Implementer | Mapper contracts, prompt inspection, three-video canary |
| Report Planner | `IMPLEMENTED_CONTRACT_DRIFT` | Strict proposal/compiler exist; frozen failed prompt/payload forces exact 3/8 structure, topic assignment, and block sequence | Restore canonical ranges and content-affordance/anti-template behavior | Existing planning module | Implementer | Planner/static tests, structure signatures, rubric |
| Deterministic plan compiler | `SUPPORTED` | Existing binder/compiler enforces IDs, times, refs, budgets, metrics, empty assets, and V0 contracts | Preserve; repair only reproduced defects | Existing planning module | Implementer | Compile/replay/render tests |
| V0 renderer and typed plan | `SUPPORTED` | Current models/renderer/tests and local report | V1-A adapter only | Reuse unchanged | V0 module | Existing + integration regression |
| Run evidence/state | `SUPPORTED` | Unique retained run directories, state/call traces, replay, and 20 historical failed canaries exist | New identities and strategy fields for the bounded continuation | Existing recorder/runtime | Implementer | State/failure/denominator tests and preservation audit |
| Quality evaluation | `SUPPORTED_NO_VALID_FORMAL_RESULT` | Three versioned cards and evaluator exist; v3 aggregate is invalid and rubrics remain pending | One new gated formal revision and honest aggregate | Existing evaluator package | Owner/implementer | Six-run result or explicit no-go/failure |
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
- `planning_runtime.py` for exact native schema transport, strategy snapshots,
  and non-secret call evidence.
- `evaluation.py` only for reproduced strategy/formal aggregation gaps.
- `tests/test_visual_report_planning.py` for anti-overfit, exact transport,
  replay, and regression coverage; split only if materially clearer.
- Versioned strategy/canary/formal manifests and new ignored run outputs under
  the existing V1-A eval/artifact roots.

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
| `OPENAI_API_KEY` | Authenticate configured OpenAI-compatible provider | Real Development runs only | Local Owner | Yes; log presence only |
| `OPENAI_BASE_URL` | Optional compatible endpoint override | Real Development runs when non-default | Local Owner | Treat query/embedded credentials as secret; log normalized label only |
| `VISUAL_REPORT_MODEL` | Explicit V1-A model identity for one declared strategy | Every real V1-A run | Implementer selects inside `DEC-VR1A-048/053/054`; Owner provisions access | No, but operational metadata |
| `VISUAL_REPORT_TIMEOUT_SECONDS` | Per-call timeout; proposed default 120 | Real and failure tests | Implementer | No |
| Python 3.12 + project `.venv` | Source/tests/CLI | Local development | Existing project/Owner | No |
| Local artifact root | Unique run/evidence output | All V1-A runs | Operator | No; may contain full transcript/model response |
| Network | Two configured provider requests per successful run | Real Development runs only | Owner | Not applicable |

No secret values belong in documentation, commands, status files, logs, or
model prompts.

## Local, fake, sandbox, and test-provider setup

- Use the existing project-local uv environment and a writable project-specific
  `UV_CACHE_DIR` if the default cache is unavailable.
- All source/schema/compiler/CLI/replay/failure tests run with a local fake
  adapter. Provider-free paths must prove `provider_calls/model_calls=0/0`.
- A real provider strategy is admitted only after local tests pass,
  credentials/config validate, official evidence proves the exact model/API
  meets the fixed input and native schema-constrained boundary, both strategy
  tuples/prompt bundles freeze, and all applicable canary identities are
  predeclared. Six formal identities are declared only after a 3/3 canary pass.
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
| Failure/recovery | Targeted malformed/ref/timeout/cancel/duplicate/replay cases | Repository root | Stable categories; no retry/overwrite |
| Replay/regression | `UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q` | Repository root | All tests pass; V0/P0 behavior preserved |
| Diff hygiene | `git diff --check` and protected-path diff review | Repository root | No whitespace/protected changes |
| Development measurement | Six explicit `build-from-transcript` invocations plus the implemented V1-A evaluation command | Repository root | Six retained terminal runs and aggregate evidence |

## Migration, compatibility, feature flags, rollout, and rollback

No migration, backfill, feature flag, deployment, or online rollout. The new
subcommand is additive and local. Existing V0 plan/asset schema versions and
render command remain stable. Roll back source/docs with version control while
preserving historical measured run directories; after a prompt/model/source/
compiler/evaluator change, issue a new measurement revision rather than mutate
or selectively rerun the prior one.

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
- Verify test/replay paths made no provider call and measured paths reported
  exactly one Mapper and one Planner call per admitted successful run.

## External blockers and required shared-framework changes

No shared-framework change or requirements blocker remains. Later
implementation needs a configured compatible model/credential, but missing
runtime credentials block only real Development execution, not code
construction or provider-free verification.

## Current post-implementation provider-conformance context

The complete exhausted-recovery state is frozen on branch `visual-report` at
`4ba28bf1b3288a6fb77bcc27378a45a69cd2b895`. It preserves all original formal
revisions plus 22 recovery candidate manifests, 20 failed Kling canary runs,
and `36/36` provider/model calls. No recovery canary rendered and no new formal
revision was created. The final Planner response had two simultaneous strict
schema errors: six source IDs in one block and only two sections.

The same commit contains useful deterministic binders/compiler, lifecycle,
replay, evaluator, strict schemas, and provider diagnostics, but its operative
prompts/payloads force exactly four topics, empty subtopics, exactly three
sections/eight blocks, fixed section/topic allocation, and a fixed block
sequence. Therefore the commit is a historical `FAILED_EXPERIMENT /
DO_NOT_PROMOTE` baseline, not the canonical V1-A prompt contract.

`VR-V1A-PROVIDER-CONFORMANCE-004` is the active Owner-authorized continuation.
It first restores the canonical variable content/anti-template behavior, then
predeclares at most two exact native-schema provider/model/API strategies. Both
strategy adapters and prompt bundles freeze before the first transcript call;
each admitted strategy receives one full three-video canary set, never a
per-video tuning loop. The first 3/3 pass immediately gates one new six-run
formal revision. The maximum is 24 new transcript-bearing calls and one formal
revision; all hard stops and terminal states are in the task card and
`09-test-acceptance.md`.

Requirements-package edits made after the baseline commit are documentation
handoff work. The next session must preserve them and may begin product changes
only under the new task. The strict two-call/binder/compiler/renderer boundary,
fixed fixtures and quality thresholds, historical evidence retention, and
Owner-only acceptance remain unchanged.
