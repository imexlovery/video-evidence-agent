# Video Visual Report V1-A — Engineering Handoff

Package drafted: 2026-08-30

The Owner confirmed the final model/measurement checkpoint on 2026-08-30.
Authoritative readiness is still assigned only by the validator-generated
`requirements-readiness.json`; this document does not assign its own READY state.

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
| Permitted integrations/actions/scale/reliance | Two sequential model calls per run, deterministic validation/compilation, one local report at a time, Development measurement only |
| Prohibited use | Production reliance, public service, public redistribution of restricted fixtures, media upload, MP4/ASR automation, automatic keyframes, OCR/VLM, Agent/LangGraph/RAG, database/queue, accounts, deployment |
| Grade-independent safety floor | Treat transcript as data, require source-linked claims, reject unknown refs and unsupported metrics, keep renderer/layout deterministic, preserve every failed run, never expose credentials |
| Next grade and horizon | `G2 CONTROLLED_PILOT`, only after V1-A quality acceptance and separate Owner authorization; no date committed |
| Promotion triggers/evidence/approvers | Three-video Development measurement passes, provider/data policy remains acceptable, bounded workload and support owner are defined; Owner approves promotion |

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
reproducible, inspectable Development measurement with honest failures and no
claim beyond the three fixtures.

## Primary inputs, outputs, and data sources

| Scenario | Producers/inputs | Decision-relevant sources | Outputs/side effects | Consumers |
|---|---|---|---|---|
| Build from transcript | Existing ingest manifest + `VideoSegment` JSONL | Full ordered transcript and fixed planning contracts | Topic Map, Report Plan, empty assets manifest, `report.html`, run trace | Owner/implementer |
| Invalid or failed run | Same inputs plus provider/model result | Schema/source/budget validators | Preserved failed run directory and non-zero error; no successful report claim | Implementer |
| Three-video measurement | Frozen prompt/model/config + three fixed transcripts + human review cards | Kling, RLinf, and Wu Yi transcript snapshots | Six repeat runs, evaluation matrix, retained failures | Owner |

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
| Intelligent behavior | `A1` draft Topic Map and Report Plan with grounded sources | Three-video evaluation, two repeats each, zero major unsupported claim | Owner | [Agent behavior](07-agent-behavior.md) |
| System completeness | One foreground transcript-to-HTML path with explicit artifacts and failures | CLI/contract/integration/replay tests | Implementer | [Functional specification](03-functional-spec.md) |
| Production resilience | Not claimed | Bounded timeouts, no hidden retry, preserved failures | Owner | [Quality](08-quality-security-operations.md) |
| Commercial operation | Not applicable — no service or customers | Scope review | Owner | [Quality](08-quality-security-operations.md) |

## Implementation objective

Add the smallest project-owned V1-A planning path that performs exactly one
Topic Mapper call and one Report Planner call, compiles the validated proposal
into the existing V0 `ReportPlan`, renders local HTML, and supplies a repeatable
three-video Development measurement.

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
| No semantic auto-repair | Invalid or ungrounded model output fails and is retained | [Functional specification](03-functional-spec.md) |
| Text-only V1-A | No image blocks; empty assets manifest feeds existing renderer | [Interfaces](06-interfaces-integrations.md) |
| Three-video Development measurement | RLinf development reference; Kling and Wu Yi broaden structure | [Acceptance](09-test-acceptance.md) |

## Top risks and mitigations

| Risk | Impact | Mitigation | Link |
|---|---|---|---|
| Mapper omission becomes invisible | Planner cannot recover missing content | Every input segment must map to a topic or explicit exclusion | [Risks](11-decisions-risks.md) |
| Polished unsupported conclusion | Misleading report | Source-ID binding, metric lexical gate, human entailment review | [Agent behavior](07-agent-behavior.md) |
| Same template across videos | Product feels generic | Content-affordance rules, no block quota, cross-video signature review | [Acceptance](09-test-acceptance.md) |
| Provider/schema drift | Run becomes non-reproducible | Explicit model/config snapshot, strict validation, fail closed | [Quality](08-quality-security-operations.md) |

## Delivery and ownership

- Surface: local foreground CLI and offline `report.html`.
- Target environment: current Python 3.12/uv macOS checkout.
- Operating owner: repository Owner.
- Implementation owner: one bounded later implementation session.
- Release/measurement acceptance owner: repository Owner.

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
| Quality thresholds/repeat plan | fixed constraint, Owner-confirmed | Owner | Values in `09-test-acceptance.md` | Self-acceptance or selective rerun by implementer | `DEC-VR1A-049`; frozen measurement |
| V1-B/C start | prohibited | Owner | Separate later authorization | Automatic continuation | New Owner instruction |

## Readiness gate

The checkpoint is closed by `DEC-VR1A-048` and `DEC-VR1A-049`. The independent
validator now determines the package status in `requirements-readiness.json`.

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
