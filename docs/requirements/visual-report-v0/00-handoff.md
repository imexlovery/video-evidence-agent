# Video Visual Report V0 — Engineering Handoff

Package generated: 2026-08-30

Machine-generated readiness, confidence, evaluated-file hashes, and blockers are
authoritative in `requirements-readiness.json`. This document does not assign
its own readiness state.

## Product definition

Video Visual Report V0 is a local prototype for one technical-video learner. It
turns an existing timestamped transcript, a hand-authored structured plan, and
manually selected source frames into one polished, offline, single-page visual
report. Its primary outcome is evidence that deterministic information design
can create substantially more save value than a transcript or Markdown summary
before any video automation is built.

## Target implementation grade and promotion

| Field | Decision |
|---|---|
| Grade | `G1 PROTOTYPE` |
| Selection method | User selected by explicitly defining `V0 — Visual Prototype` |
| User-confirmation evidence | 2026-08-30 V0 renderer constraints |
| Rationale and approver | Owner prioritizes visual proof over pipeline completeness |
| Permitted users/data/environments | One owner, local macOS checkout, fixed local RLinf fixture |
| Permitted integrations/actions/scale/reliance | Local files, FFmpeg frame extraction, synchronous deterministic rendering, one report at a time |
| Prohibited use | Public sharing of the fixture, deployment, production reliance, accounts, external providers, automated content planning |
| Grade-independent safety floor | Escape authored text, reject unsafe paths and invalid references, make zero external requests, preserve media rights and frozen P0-B history |
| Next grade and horizon | `V1 — Automated Video Report`, only after owner accepts V0 visual quality |
| Promotion triggers/evidence/approvers | Owner accepts report quality; then separately authorizes Topic Mapper, Report Planner, ASR and Asset Resolver work |

## Deferred-by-grade items

| Capability | Rationale | Current boundary/workaround | Risk | Owner | Upgrade trigger | Future acceptance |
|---|---|---|---|---|---|---|
| Automatic ASR | Not part of the visual hypothesis | Reuse existing transcript | Low for V0 | Owner | V0 accepted | One local MP4 produces usable timestamped text |
| Topic Mapper | Coverage automation follows renderer proof | Hand map source content | Manual effort | Owner | Stable schema | Coverage map is complete and independent from selection |
| Report Planner | Compression automation follows component proof | Hand-author plan | Authoring bias | Owner | Stable component budgets | Structured plan meets visual and source-reference constraints |
| Asset Resolver | Best-frame ranking is a separate experiment | Human selects 2–4 frames | Does not prove automation | Owner | Renderer benefits from frames | Automated candidates match human-selected value |
| OCR/VLM | No demonstrated V0 need | Human inspects frames | Some image semantics remain manual | Owner | Repeated asset-selection failure | Clear measured improvement on report assets |
| Multiple templates / publishing | Premature before one visual language works | One local theme and HTML | Narrow applicability | Owner | Repeated accepted reports | New format has an explicit user and acceptance target |

## Customer/service model and commitments within this grade

There is no customer, tenant, account, hosted service, billing, support promise,
or production availability commitment. The owner runs and reviews one local
prototype. The only commitment is a reproducible local render and honest visual
review evidence.

## Primary inputs, outputs, and data sources

| Scenario | Producers/inputs | Decision-relevant sources | Outputs/side effects | Consumers |
|---|---|---|---|---|
| First report | Owner-authored plan, selected frames, existing transcript | RLinf `segments.jsonl`, ingest manifest, inspected source frames | Local `report.html`, plan, asset manifest, screenshots | Owner |
| Re-render after edit | Edited plan or assets | Same immutable source material | Replaced prototype HTML and new review screenshots | Owner |
| Invalid render | Malformed plan or asset manifest | Pydantic contracts and local path policy | Non-zero exit and concise error; no successful artifact claim | Implementer/owner |

## Existing data, database, and creative assets

| Asset ID/type | Availability/readiness | Location/access | Rights/change decision | Gap and delivery owner |
|---|---|---|---|---|
| `DATA-RLINF-TRANSCRIPT` | Available; 46 timestamped segments | `artifacts/p0b-ingest/p0b-rlinf-2026/segments.jsonl` | Read-only reuse; do not modify P0-B lineage | Content mapping by implementer |
| `MEDIA-RLINF` | Available; about 34:53 | `eval/p0b/media/...RLinf...mp4` | Local research only; no publication or redistribution | Manual frame selection by implementer |
| `META-RLINF` | Available | `artifacts/p0b-ingest/p0b-rlinf-2026/manifest.json` and `eval/p0b/corpus.jsonl` | Read-only attribution and rights authority | None |
| `REF-TUGEKUAI` | Available for visual direction | `/Users/tristana/Desktop/"图个快"效果图.png` | Inspect locally; do not copy as a product asset | Translate direction into original design |
| Selected frames | Not yet materialized | `artifacts/visual-report/v0-rlinf/assets/` | Derived local-only assets | Implementation task extracts and reviews them |
| Database | Not applicable | None | Do not add one | None |

## Commercial-grade maturity summary

| Axis | Target | Measurement/release evidence | Owner | Link |
|---|---|---|---|---|
| Intelligent behavior | A0 deterministic renderer | No runtime model/provider calls | Implementer | [Agent behavior](07-agent-behavior.md) |
| System completeness | One end-to-end structured-plan render | Required command and artifact | Implementer | [Acceptance](09-test-acceptance.md) |
| Production resilience | Not a V0 claim | Local validation and visible failure only | Owner | [Quality](08-quality-security-operations.md) |
| Commercial operation | Not applicable | No service, account, billing, or publication | Owner | [Quality](08-quality-security-operations.md) |

## Implementation objective

Create `artifacts/visual-report/v0-rlinf/report.html` with a thesis-led Hero,
3–5 coherent content modules, at least one relation/process visualization, 2–4
informative source frames, timestamps, and decisive takeaways. It must be a
finished editorial artifact at desktop and mobile review sizes, not merely a
schema demo.

## Documentation-only phase boundary

- This package specifies a separate implementation session.
- This design phase changes no application code, dependency, migration,
  infrastructure, runtime data, or deployment.

## Explicit non-goals

Automatic ASR, Topic Mapper, Report Planner, keyframe ranking, OCR, VLM, RAG,
Agent, LangGraph, vector database, reranker, multi-agent workflow, URL download,
multiple videos, multiple templates, accounts, hosted UI, public sharing, PNG
renderer, PDF renderer, production hardening, and V1 implementation.

## Read order

1. This handoff and [engineering context](12-engineering-context.md)
2. [Product requirements](01-product-requirements.md), [scenarios](02-user-scenarios.md), and [functional specification](03-functional-spec.md)
3. [System](04-system-design.md), [data](05-data-memory.md), and [interfaces](06-interfaces-integrations.md)
4. [Agent boundary](07-agent-behavior.md), [quality](08-quality-security-operations.md), and [acceptance](09-test-acceptance.md)
5. [Delivery plan](10-delivery-plan.md), [decisions/risks](11-decisions-risks.md), then the bounded task in `docs/tasks/`

## Top user pain points

- A transcript is accurate but slow to revisit and visually flat.
- A generic summary loses relationships, evidence frames, and information hierarchy.
- Pipeline success can conceal an output that nobody wants to save.

## Top engineering challenges

- Encoding enough content variety without creating a generic layout language.
- Maintaining readable density and rhythm across 1080 px and 390 px viewports.
- Keeping every claim and frame traceable while avoiding evidence-product machinery.
- Iterating against actual screenshots until the result feels authored.

## Key decisions

| Decision | Summary | Link |
|---|---|---|
| Renderer-first | Manual content and frame selection are allowed | [Delivery plan](10-delivery-plan.md) |
| Typed content blocks | Seven bounded content types; structural layout remains renderer-owned | [Functional specification](03-functional-spec.md) |
| Separate assets | Blocks reference assets by ID; acquisition requests are outside the block union | [Data](05-data-memory.md) |
| Canonical HTML | One 1080 px natural-height report; PNG is a later screenshot derivative | [Interfaces](06-interfaces-integrations.md) |
| One visual identity | Research field notebook meets systems blueprint | [Quality](08-quality-security-operations.md) |
| Human visual gate | Implementation stops before owner acceptance | [Acceptance](09-test-acceptance.md) |

## Top risks and mitigations

| Risk | Impact | Mitigation | Link |
|---|---|---|---|
| Generic card output | Fails the product hypothesis | Fixed editorial direction, argument spine, screenshot iteration | [Risks](11-decisions-risks.md) |
| Rights-restricted fixture is shared | License boundary violation | Local-only assets, no deployment, explicit attribution | [Data](05-data-memory.md) |
| Schema drives design too early | Over-abstraction and weak visual output | Provisional schema; stabilize only after the real report | [Delivery](10-delivery-plan.md) |
| Unsupported metrics | Polished misinformation | Require source refs; omit ambiguous numbers | [Functional spec](03-functional-spec.md) |

## Delivery and ownership

- Surface: local, offline single-page HTML.
- Target environment: existing Python 3.12/uv macOS project and local browser.
- Operating owner: repository owner.
- Implementation owner: one bounded Codex implementation session.
- Release owner: repository owner after visual inspection.

## Downstream implementation contract

- Framework status: `NOT_APPLICABLE`
- Product strategy: frameworkless, project-owned Python/Pydantic renderer.
- Required capabilities: typed validation, deterministic components, local
  assets, safe escaping, simple renderer-owned SVG, responsive offline HTML.
- Compatibility envelope: existing Python `>=3.12,<3.13`, uv workflow, no new
  infrastructure, no modification of frozen P0-B contracts.
- Target repository/output: this repository and
  `artifacts/visual-report/v0-rlinf/`.
- Implementation phase begins by executing
  `docs/tasks/VISUAL-REPORT-V0-RENDERER.md`.

## Decision-authority summary

| Decision | Class | Owner | Allowed envelope | Prohibited | Acceptance evidence |
|---|---|---|---|---|---|
| Product goal and V0 exclusions | Fixed constraint | Owner | Renderer prototype only | V1 automation | Requirements trace and artifact scope |
| Content/asset separation | Required invariant | Owner | Optional asset refs on blocks | Keyframe request block | Contract tests |
| Visual tokens and component internals | Implementation-delegated | Implementer | Fixed identity and seven content types | New template system/free layout | Screenshots and owner review |
| Content wording | Implementation-delegated | Implementer | Compress verified RLinf content | Invented or unsupported claims | Source refs and owner review |
| Visual acceptance | Fixed constraint | Owner | Accept or request iteration | Implementer self-approval | Owner decision |
| V1 start | Prohibited in this task | Owner | Separate later authorization | Automatic continuation | New explicit instruction |

## Readiness gate

All checklist evaluation is generated from `decision-evidence.jsonl` and
`coverage.json` by the requirements validator. The implementation agent must use
`requirements-readiness.json` as the machine-readable gate and must not infer
permission from this prose alone.

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
