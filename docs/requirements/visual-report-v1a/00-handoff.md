# Video Visual Report V1-A — Engineering Handoff

Package drafted: 2026-08-30

The Owner confirmed the original model/measurement checkpoint on 2026-08-30
and the current semantic-v2 product-prototype contract on 2026-08-31.
Authoritative readiness is still assigned only by the validator-generated
`requirements-readiness.json`; this document does not assign its own READY state.

## Current continuation handoff

The original V1-A implementation and two recovery attempts now exist as
historical evidence. The latest exhausted snapshot is frozen at
`4ba28bf1b3288a6fb77bcc27378a45a69cd2b895` and is classified
`FAILED_EXPERIMENT / DO_NOT_PROMOTE`: it retained 22 candidate manifests,
20 failed Kling canaries, and `36/36` provider/model calls, but no passing
cross-video gate or new formal measurement.

The Owner-authorized `VR-V1A-PROVIDER-CONFORMANCE-004` continuation restored the
canonical content/anti-template contract, executed both frozen DeepSeek
Responses strategies, and closed at
`READY_FOR_OWNER_V1A_REVIEW — V1A_PROVIDER_CONFORMANCE_NO_GO`. Its complete
state is frozen at `e72503f5b20831c1e86a1b72c93fb4c4f7debe2a`; its strategy,
canary, and call authority are closed.

The later direct-official-OpenAI proposal
[`VR-V1A-BOUNDARY-ISOLATION-005`](../../tasks/VISUAL-REPORT-V1A-BOUNDARY-ISOLATION.md)
was never authorized or executed. The Owner has no OpenAI API key, does not
want to purchase one, and explicitly redirected work away from Route A.

The current Owner-confirmed product contract is
[`VR-V1A-CONTRACT-SIMPLIFICATION-006`](../../tasks/VISUAL-REPORT-V1A-CONTRACT-SIMPLIFICATION.md).
It keeps the two independent calls and the current V0 compiler/renderer
boundary, uses only the already available DeepSeek provider, and replaces the
strict model-facing v1 schemas with shallow semantic v2 proposals plus an
observable deterministic compiler and Topic Resolver. It validates a
three-video product prototype, permits one explicit technical retry per run,
and evaluates content and real rendered views rather than provider conformance.
GLM/Qwen remain future options rather than current requirements or fallback.
Execution has not started in this documentation session.

## Product definition

V1-A is a local G1 prototype that turns one already-ingested Chinese technical
video transcript into a source-linked Topic Map and then a renderer-compatible
Report Plan using two deliberately separate LLM calls. Deterministic code binds
model-selected segment IDs to canonical timestamps, validates content and block
budgets, and hands the resulting plan to the existing V0 renderer. The product
hypothesis is content planning quality, not MP4 ingest, keyframe selection, or
production operation.

## Target implementation grade and promotion

| Field | Decision |
|---|---|
| Grade | `G1 PROTOTYPE` |
| Selection method | AI recommended; Owner explicitly confirmed on 2026-08-30 |
| User-confirmation evidence | “V1-A 按 G1 PROTOTYPE 继续设计” |
| Rationale and approver | Owner is validating feasibility and content quality with three local research fixtures |
| Permitted users/data/environments | One Owner; the three authorized P0-B transcripts; local macOS checkout; full transcript text may be sent to the configured external OpenAI-compatible provider |
| Permitted integrations/actions/scale/reliance | Two semantic stages per run, at most one recorded technical retry per run, deterministic compilation, one local report at a time, three-video product prototype only |
| Prohibited use | Production reliance, public service, public redistribution of restricted fixtures, media upload, MP4/ASR automation, automatic keyframes, OCR/VLM, Agent/LangGraph/RAG, database/queue, accounts, deployment |
| Grade-independent safety floor | Treat transcript as data, require source-linked claims, reject unknown refs and unsupported metrics, keep renderer/layout deterministic, preserve every failed run, never expose credentials |
| Next grade and horizon | `G2 CONTROLLED_PILOT`, only after V1-A quality acceptance and separate Owner authorization; no date committed |
| Promotion triggers/evidence/approvers | Owner accepts three grounded and visually usable prototype reports, provider/data policy remains acceptable, and a later G2 workload/support design is separately approved |

## Deferred-by-grade items

| Capability | Rationale | Current boundary/workaround | Risk | Owner | Upgrade trigger | Future acceptance |
|---|---|---|---|---|---|---|
| MP4/ASR input | Isolate content planning | Reuse existing `VideoSegment` JSONL | Not end-to-end | Owner | Planner passes | One local MP4 produces the same validated transcript contract |
| Asset Resolver/keyframes | Do not confound content quality | V1-A emits no `image_caption` blocks and uses an empty asset manifest | Visual reports have no new images | Owner | Content plan accepted | V1-B measured candidate selection |
| OCR/VLM | No demonstrated transcript-only failure yet | Transcript only | Important visual facts may be absent | Owner | Repeated, evidenced transcript gap | Targeted OCR/frame VLM improves named cases |
| Service/database/queue | One foreground local run | Append-only local run directories | No multi-user resilience | Owner | Named pilot users or background need | G2 workload, recovery, and access tests |
| Multiple templates/publishing | Existing renderer already proves visual grammar | One renderer and local HTML | Narrow presentation envelope | Owner | Licensed publishing scenario | Separate product and rights acceptance |

## Customer/service model and commitments within this grade

There is one local Owner and no customer, tenant, account, hosted service,
billing, support promise, or availability commitment. The only commitment is a
reproducible, inspectable three-video product review package with honest
failures and no claim beyond the three fixtures.

## Primary inputs, outputs, and data sources

| Scenario | Producers/inputs | Decision-relevant sources | Outputs/side effects | Consumers |
|---|---|---|---|---|
| Build from transcript | Existing ingest manifest + `VideoSegment` JSONL | Full ordered transcript and fixed planning contracts | Topic Map, Report Plan, empty assets manifest, `report.html`, run trace | Owner/implementer |
| Invalid or failed run | Same inputs plus provider/model result | Schema/source/budget validators | Preserved failed run directory and non-zero error; no successful report claim | Implementer |
| Three-video product prototype | Frozen prompt/model/config + three fixed transcripts + human review cards | Kling, RLinf, and Wu Yi transcript snapshots | Three reports, desktop/mobile screenshots, content/visual rubrics, retained attempts | Owner |

## Existing data, database, and creative assets

| Asset ID/type | Availability/readiness | Location/access | Rights/change decision | Gap and delivery owner |
|---|---|---|---|---|
| `ASSET-VR1A-KLING-TRANSCRIPT` | Available; 43 segments | `artifacts/p0b-ingest/p0b-kling-2024/` | Read-only; external model processing authorized; no public redistribution | Human review card to be created in implementation |
| `ASSET-VR1A-RLINF-TRANSCRIPT` | Available; 46 segments | `artifacts/p0b-ingest/p0b-rlinf-2026/` | Read-only; external model processing authorized; V0 plan is a reference | None |
| `ASSET-VR1A-WUYI-TRANSCRIPT` | Available; 38 segments | `artifacts/p0b-ingest/p0b-wuyi-goals/` | Read-only; external model processing authorized; no public redistribution | Human review card to be created in implementation |
| `ASSET-VR1A-V0-PLAN` | Available; 4 sections/13 blocks | `artifacts/visual-report/v0-rlinf/report-plan.json` | Read-only development reference, never automatic Gold | None |
| Existing renderer | Available and tested | `src/video_evidence_agent/visual_report/` | Reuse unchanged contract | None |
| Database/brand assets | Not applicable | None | Do not add | None |

## Commercial-grade maturity summary

| Axis | Target | Measurement/release evidence | Owner | Link |
|---|---|---|---|---|
| Intelligent behavior | `A1` draft Topic Map and Report Plan with grounded sources | Three-video content review, zero major unsupported claim, useful editorial structure | Owner | [Agent behavior](07-agent-behavior.md) |
| System completeness | One foreground transcript-to-HTML path with explicit artifacts and failures | CLI/contract/integration/replay tests | Implementer | [Functional specification](03-functional-spec.md) |
| Production resilience | Not claimed | Bounded timeouts, one explicit technical retry, preserved attempt evidence | Owner | [Quality](08-quality-security-operations.md) |
| Commercial operation | Not applicable — no service or customers | Scope review | Owner | [Quality](08-quality-security-operations.md) |

## Implementation objective

Add the smallest project-owned V1-A planning path that performs one Topic
Mapper stage and one Report Planner stage, compiles semantic proposals without
rewriting/merging/splitting semantics, renders local HTML, and supplies three
content- and visually reviewable product prototypes. A run may make one
identical technical retry when an eligible API/JSON anomaly occurs.

## Documentation-only phase boundary

- This package specifies a later implementation session.
- This phase changes no product code, dependency, runtime data, model call,
  infrastructure, or deployment.

## Explicit non-goals

MP4 input, ASR, keyframe extraction or final selection, `image_caption` planning,
OCR, VLM, RAG, Agent, LangGraph, tool loops, multi-agent work, database, queue,
service/API/UI, URL download, multiple videos in one report, multiple templates,
free layout, public publishing, prompt self-improvement, fine-tuning, and V1-B/C.

## Read order

1. This handoff and [engineering context](12-engineering-context.md)
2. [Product requirements](01-product-requirements.md), [scenarios](02-user-scenarios.md), and [functional specification](03-functional-spec.md)
3. [System design](04-system-design.md), [data](05-data-memory.md), and [interfaces](06-interfaces-integrations.md)
4. [Model behavior](07-agent-behavior.md), [quality](08-quality-security-operations.md), and [acceptance](09-test-acceptance.md)
5. [Delivery plan](10-delivery-plan.md) and [decisions/risks](11-decisions-risks.md)

## Top user pain points

- A high-quality renderer still depends on a manually authored Report Plan.
- A single “summarize this transcript” prompt tends to mix coverage and
  selection, hiding omissions and overclaim.
- Green JSON is not evidence that a generated report chose the right story or
  grounded its claims.

## Top engineering challenges

- Preserve full-video coverage in Topic Mapper without forcing one generic topic template.
- Let Report Planner compress aggressively without losing must-cover material or inventing conclusions.
- Bind every model-selected source deterministically to existing transcript IDs/timestamps.
- Measure quality across structurally different videos without tuning selectively on failures.

## Key decisions

| Decision | Summary | Link |
|---|---|---|
| Two calls, two roles | Topic Mapper optimizes coverage; Planner optimizes compression | [Model behavior](07-agent-behavior.md) |
| Model emits IDs, not timestamps | Deterministic binder owns canonical `SourceRef` values | [Functional specification](03-functional-spec.md) |
| Proposal then compiler | Model output is not the renderer contract until validated and compiled | [System design](04-system-design.md) |
| Non-semantic compiler only | It may bind/validate/map structure but cannot rewrite, merge, or split semantic content | [Functional specification](03-functional-spec.md) |
| One technical retry | One identical, explicit, attempt-recorded retry per run is allowed only for eligible API/JSON anomalies | [Interfaces](06-interfaces-integrations.md) |
| Adaptive semantic-v2 budget | Duration and primary-topic breadth produce a soft 6–24 recommendation; only more than 32 blocks or 8,000 visible characters is an aggregate hard failure | [Functional specification](03-functional-spec.md) |
| Text-only V1-A | No image blocks; empty assets manifest feeds existing renderer | [Interfaces](06-interfaces-integrations.md) |
| Three-video product prototype | RLinf development reference; Kling and Wu Yi broaden content and visual structure | [Acceptance](09-test-acceptance.md) |

## Top risks and mitigations

| Risk | Impact | Mitigation | Link |
|---|---|---|---|
| Mapper omission becomes invisible | Planner cannot recover missing content | Coverage diagnostics plus must-cover human review; no hidden topic synthesis | [Risks](11-decisions-risks.md) |
| Polished unsupported conclusion | Misleading report | Source-ID binding, metric lexical gate, human entailment review | [Agent behavior](07-agent-behavior.md) |
| Same template across videos | Product feels generic | Content-affordance rules, no block quota, cross-video signature review | [Acceptance](09-test-acceptance.md) |
| Technical API/JSON anomaly masks product quality | Prototype set becomes inconclusive | One identical recorded retry; technical failure separated from product judgment | [Quality](08-quality-security-operations.md) |

## Delivery and ownership

- Surface: local foreground CLI and offline `report.html`.
- Target environment: current Python 3.12/uv macOS checkout.
- Operating owner: repository Owner.
- Implementation owner: one bounded later implementation session.
- Product-prototype acceptance owner: repository Owner.

## Downstream implementation contract

- Framework status: `NOT_APPLICABLE`.
- Product strategy: `FRAMEWORKLESS`, project-owned Python/Pydantic orchestration
  using the already-installed OpenAI-compatible SDK.
- Hypha disposition: `NOT_APPLICABLE`; V1-A is explicitly not an Agent, has no
  tools, runtime memory, multi-agent graph, or framework need.
- Compatibility: existing `VideoSegment`, V0 `ReportPlan`/renderer, Python
  `>=3.12,<3.13`, uv lock, current OpenAI SDK provider boundary.
- Target repository/output: this repository and local
  `artifacts/visual-report/v1a/<run-id>/` directories.
- Implementation begins only after validator-generated readiness is true and
  the Owner separately authorizes the bounded implementation task.

## Decision-authority summary

| Decision | Class | Owner | Allowed envelope | Prohibited | Acceptance evidence |
|---|---|---|---|---|---|
| G1 scope and two-stage separation | fixed constraint | Owner | V1-A transcript planning only | Merge stages or expand to V1-B/C | Scope/diff review |
| Canonical source binding | required invariant | Owner | Model selects existing IDs; code supplies times | Model-generated timestamps/unknown IDs | Contract tests |
| Renderer/layout authority | required invariant | Owner | Existing typed plan and deterministic renderer | LLM HTML/CSS/layout | Plan/schema review |
| Internal module/function split | implementation-delegated | Later implementer | Small project-owned code under approved paths | New framework/service | Code review |
| Exact provider model | implementation-delegated, Owner-confirmed envelope | Owner/implementer | Explicit configured text model with sufficient context and JSON output | Implicit model or hidden fallback | `DEC-VR1A-048`; run manifest |
| Product quality and visual review | fixed constraint, Owner-confirmed | Owner | Three reports; content/grounding/structure plus desktop/mobile review | Schema-first-hit as primary outcome or implementer self-acceptance | `DEC-VR1A-049/061`; prototype review package |
| Provider-conformance continuation | closed historical experiment | None | Preserve its completed no-go evidence | Reopen calls, mutate results, or reuse it as current product acceptance | `DEC-VR1A-053/054`; strategy/canary/formal manifests |
| Minimal strict-boundary isolation design | rejected/cancelled before execution | Owner | Retain as historical design evidence only | Official OpenAI credential/provider call or use as current authority | `DEC-VR1A-055/056/057/058`; cancelled isolation card |
| V1-A semantic-v2 product prototype | fixed constraint; Owner-confirmed | Owner | Two semantic stages; non-semantic compiler; one recorded technical retry per run; one three-video product set; content/visual review | Semantic rewrite/merge/split, model repair, provider fallback, six-run formal, schema compliance as product goal | `DEC-VR1A-061`; contract-simplification card |
| Semantic-v2 adaptive aggregate budget | fixed constraint; Owner-confirmed | Owner | Soft block/density recommendations, hard protection at >32 blocks or >8,000 visible characters, observable diagnostics | Exact-count prompting, budget-driven semantic deletion/rewrite/merge/split, mutation of historical v1 artifacts | `DEC-VR1A-065/066`; adaptive-budget Goal card |
| Network-recovery diagnostic canary | Owner-confirmed process override and delegated diagnostic design | Owner/implementer | One new Kling diagnostic-only canary on the frozen Task 008 tuple; process-scoped `NO_PROXY/no_proxy` only; 3-call total ceiling | Selective Task 008 continuation, product-set denominator change, provider/model/prompt/compiler change, quality claim | `DEC-VR1A-067/068`; Task 009 card |
| V1-B/C start | prohibited | Owner | Separate later authorization | Automatic continuation | New Owner instruction |

## Readiness gate

The original implementation/measurement checkpoint is historical. The latest
product contract is `DEC-VR1A-061`. The independent validator determines this
package's documentation readiness in `requirements-readiness.json`; this
documentation session still performs no implementation or provider call.

The current merged engineering baseline is branch `visual-report` at
`bb8f6f75aa2e4ae91ab6688a7f16ed87caec7741`. Task 008 is now closed at
`READY_FOR_OWNER_V1A_REVIEW — EXTERNAL_BLOCKED`: the frozen revision is
`vr1a-semantic-v2-29d077aa0bdc`, and the Kling run retained two identical
`APIConnectionError` attempts (`2/2`). RLinf, Wu Yi, and Web smoke did not
continue. Its revision, run, aggregate, manifest, and historical evidence
remain immutable. Task 009 is the next documentation-ready, independent
network-recovery diagnostic; it is `READY_FOR_OWNER_V1A_REVIEW — NOT_STARTED`
and this session has made zero provider/model calls.

Task 009 may be executed only in a separately started construction session
using the exact task card and process-scoped proxy override. It cannot resume
Task 008's remaining videos, alter the frozen product denominator, or authorize
a new three-video revision.

## Package index

- [Product requirements](01-product-requirements.md)
- [User scenarios](02-user-scenarios.md)
- [Functional specification](03-functional-spec.md)
- [System design](04-system-design.md)
- [Data and memory](05-data-memory.md)
- [Interfaces and integrations](06-interfaces-integrations.md)
- [Agent behavior](07-agent-behavior.md)
- [Quality, security, and operations](08-quality-security-operations.md)
- [Test and acceptance](09-test-acceptance.md)
- [Delivery plan](10-delivery-plan.md)
- [Decisions and risks](11-decisions-risks.md)
- [Engineering context](12-engineering-context.md)
