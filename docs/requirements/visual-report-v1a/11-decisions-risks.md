# Video Visual Report V1-A — Decisions and Risks

## Implementation-grade and promotion decision

| Field | Decision |
|---|---|
| Current grade | `G1 PROTOTYPE`, explicitly confirmed by the Owner |
| Allowed/prohibited use | One local Owner, three authorized transcript fixtures, two sequential OpenAI-compatible text calls per run, Development measurement only; no production/public use, media upload, V1-B/C, or excluded infrastructure |
| Safety floor | Strict source IDs, deterministic timestamps/IDs/compiler, current typed renderer, no hidden retry/fallback/repair, append-oriented failure retention, no credential disclosure |
| Deferred risks | End-to-end MP4 quality, visual-only information, asset selection, service resilience, tenancy, support, and publishing rights remain untested |
| Next grade/horizon | `G2 CONTROLLED_PILOT` only after V1-A quality acceptance and a separate Owner decision; no target date |
| Promotion evidence/approvers | Six-run evidence passes the Owner-approved rubric; workload, source rights, operating/support owner, and recovery boundaries are newly defined; Owner approves |

## Decision log

The append-only evidence records named below are canonical for confirmation
state. This table explains consequences; it does not upgrade a recommendation
into Owner confirmation.

| ID/status | Decision | Source | Drivers | Alternatives | Tradeoffs | Reversal | Verification |
|---|---|---|---|---|---|---|---|
| `DEC-VR1A-001 / USER_CONFIRMED` | Target `G1 PROTOTYPE` | Owner message | Validate feasibility and content quality before operational maturity | G0 mockup; G2 pilot | Real provider behavior, deliberately narrow operation | New grade decision | Grade/use review |
| `DEC-VR1A-003 / USER_CONFIRMED` | V1-A is transcript-to-plan only | Owner handoff | Isolate the largest uncertainty | Build full V1 pipeline | No automatic media/assets, faster causal learning | Separate V1-B/C authorization | Scope/diff review |
| `DEC-VR1A-004 / USER_CONFIRMED` | Mapper and Planner remain two independent calls | Owner handoff and product brief | Coverage and compression optimize different goals | One prompt; iterative Agent | Two calls cost more but omissions are visible | New product decision | Call trace equals `2/2` |
| `DEC-VR1A-005 / USER_CONFIRMED` | Both calls may receive the complete authorized transcript | Owner authorization/handoff | Avoid chunk-merge loss in the fixed small envelope | Chunking; retrieval | Higher context cost, simpler provenance | New input-envelope decision | Request snapshots and limits |
| `DEC-VR1A-006 / USER_CONFIRMED` | Models select existing IDs; code binds IDs/times/refs | Owner-approved core design | Prevent invented timestamps and identity drift | Model emits full plan refs | More compiler code, much stronger lineage | Schema-version change | Unknown-ref and replay tests |
| `DEC-VR1A-007 / USER_CONFIRMED` | No semantic repair, third call, hidden retry, or provider fallback | Owner-approved core design | Preserve two-call and failure evidence claims | Repair model; retry policy | Lower first-pass success, honest failures | New measured revision and Owner approval | Failure fixtures and call counts |
| `DEC-VR1A-008 / USER_CONFIRMED` | Compile current V0 plan and use empty assets | Owner-approved core design | Reuse proven renderer without V1-B | Generate captions/assets | Text-only output in V1-A | Separate V1-B design | Current schema and renderer tests |
| `DEC-VR1A-009 / USER_CONFIRMED` | Use three fixed transcripts | Owner handoff | Structural diversity and bounded evidence | RLinf only; larger corpus | Small denominator but avoids single-video overfit | New measurement revision | Source manifest and review cards |
| `DEC-VR1A-010 / USER_CONFIRMED` | Every run gets a unique retained directory | Owner-approved core design | Prevent selective evidence replacement | Mutable latest directory | More local artifacts, auditable denominator | Owner-managed archival only | Duplicate-ID and failure tests |
| `DEC-VR1A-011 / USER_DELEGATED` | Use strict proposal schemas and deterministic budgets/compiler | Requirements design authority | Bound model creativity at semantic layer | Free-form Markdown/HTML | Schema failures become visible | New schema revision | Contract/adversarial tests |
| `DEC-VR1A-012 / USER_DELEGATED` | One synchronous local CLI, no worker/service | G1 scope | Smallest usable surface | API/UI/queue | No concurrent or remote use | G2 design | CLI integration test |
| `DEC-VR1A-013 / USER_DELEGATED` | `run.json` is state authority; `RENDERED` is not quality acceptance | Requirements design authority | Separate execution success from product judgment | Infer success from files | Explicit status writing required | New lifecycle version | State-transition tests |
| `DEC-VR1A-014 / USER_DELEGATED` | Full-context limits are 80 segments and 50,000 Unicode characters | Fixed fixture envelope | Prove whole-transcript design without premature chunking | Unlimited input; chunk pipeline | Rejects larger videos in G1 | Evidence-backed scope expansion | Boundary tests |
| `DEC-VR1A-015 / USER_DELEGATED` | Planner budget is 3–5 sections, 8–14 blocks, at most 2,600 visible characters | V0 visual capacity and compression goal | Prevent transcript-shaped output | Unbounded plan | Some useful details must be omitted explicitly | New measured revision | Schema/budget tests and review |
| `DEC-VR1A-016 / NOT_APPLICABLE` | No runtime identity, accounts, or tenancy | G1 local boundary | One Owner/local checkout | Account system | No product access control | G2 requirements | Scope review |
| `DEC-VR1A-017 / NOT_APPLICABLE` | No runtime high-impact external action | Local output boundary | Only configured model calls and local writes | Publish/deploy/message actions | Publication remains manual and prohibited for fixtures | New authority | Side-effect inventory |
| `DEC-VR1A-018 / NOT_APPLICABLE` | No end-user consent/revocation product flow | No end users or personal-data collection | Owner controls source authorization | Consent service | Withdrawal is manual stop/delete of derived runs | G2/privacy design | Data lifecycle review |
| `DEC-VR1A-019 / USER_DELEGATED` | External dependency is explicit config with timeout and no fallback | Existing OpenAI-compatible boundary | Avoid implicit provider behavior | Hard-code provider; reuse P0 variable silently | More configuration, clearer isolation | New config version | Config/provider-failure tests |
| `DEC-VR1A-020 / USER_DELEGATED` | Frameworkless project-owned Python/Pydantic; Hypha not applicable | Non-Agent product boundary | Existing repo already supplies required primitives | Agent framework/LangGraph/Hypha | Less framework machinery, project owns orchestration | Separate architecture decision | Dependency/diff review |
| `DEC-VR1A-021 / USER_DELEGATED` | Transcript content is inert untrusted data | Prompt-injection risk | Video speech must not change policy or output schema | Trust transcript instructions | Some transcripts may cause model failure, never authority expansion | New safety contract | Adversarial transcript test |
| `DEC-VR1A-022 / USER_DELEGATED` | One foreground run, no successful degraded output | G1 reliability boundary | Simple failure semantics | Partial report; background retry | Less availability, no ambiguous success | G2 recovery design | Cancellation/partial tests |
| `DEC-VR1A-023 / USER_DELEGATED` | Record usage/latency; cost stays `unavailable` without authoritative pricing | Evidence accuracy | Avoid fabricated cost | Estimate price | Cost conclusion can remain incomplete | Add versioned price source | Trace/evaluator test |
| `DEC-VR1A-024 / USER_CONFIRMED` | V1-A stops for Owner review and cannot start V1-B/C | Owner scope | Preserve phase authority | Automatic continuation | Extra checkpoint | New Owner message | Status and diff review |
| `DEC-VR1A-025 / SYSTEM_RECOMMENDED` | Later implementer selects an explicit compatible text model inside the fixed boundary | Historical recommendation | Provider capability varies; repository must not silently choose | Freeze a model in requirements | Allows pragmatic selection but makes run snapshot essential | Superseded by Owner confirmation | `DEC-VR1A-048` |
| `DEC-VR1A-026 / SYSTEM_RECOMMENDED` | Measure 3 videos × 2 repeats and apply the quality rubric thresholds | Historical recommendation | Need repeat stability and a predeclared denominator | One run each; more repetitions | Twelve calls are bounded but quality scoring costs human time | Superseded by Owner confirmation | `DEC-VR1A-049` |
| `DEC-VR1A-048 / USER_CONFIRMED` | Exact model identity is implementation-delegated inside the explicit compatibility/configuration boundary | Owner checkpoint confirmation | Preserve provider flexibility without implicit choice or fallback | Fixed model named in requirements | Implementer must preflight and snapshot the selected model | New Owner decision before measurement freeze | Run manifest and config tests |
| `DEC-VR1A-049 / USER_CONFIRMED` | Fix 3 videos × 2 repeats and the coverage, grounding, first-pass, human-quality, stability, and anti-template thresholds | Owner checkpoint confirmation | Predeclare the denominator and acceptance rule | Fewer/more repeats or different thresholds | Twelve planned calls plus human scoring | New measurement revision; historical revision retained | Six-run aggregate and rubrics |

## Business, integration, and platform gap decisions

| Gap | Baseline evidence | Classification | Why adapter/overlay is insufficient | Reuse evidence | Owner | Acceptance |
|---|---|---|---|---|---|---|
| Topic Mapper | No planning model exists in `visual_report/` | Project-owned capability | This is the product hypothesis, not a provider transport concern | Reuse `VideoSegment`, OpenAI SDK, Pydantic | Implementer | Coverage and failure tests |
| Report Planner/compiler | Existing V0 plan is hand-authored | Project-owned capability | Generic summarization cannot guarantee typed blocks/source budgets | Reuse V0 `ReportPlan`/renderer | Implementer | Compile/render and quality rubric |
| Provider adapter | `answering.py` proves explicit OpenAI-compatible JSON transport but is P0 answer-specific | Project adapter | Reusing answer prompt/schema/config names would couple frozen P0-B behavior | Reuse installed SDK and transport pattern, not P0 answer semantics | Implementer | Fake/real trace contract; no P0 diff |
| Run/evaluation evidence | Existing P0-B evidence is a different experiment | Project-owned capability | Adapting frozen P0-B results would contaminate both claims | Reuse append-only discipline only | Implementer/Owner | Six declared run identities and rubric |
| Shared framework/platform | No Agent/service need | Not applicable | A framework adds topology and lifecycle outside V1-A | Existing direct Python modules are sufficient | Owner | Dependency review shows no framework addition |

## Assumption register

| ID | Assumption | Evidence state | Impact if wrong | Validation |
|---|---|---|---|---|
| `ASM-VR1A-001` | Each fixed transcript fits both full-context calls with output headroom | Repository sizes are within the declared 50k-character envelope; provider tokenizer varies | Chosen model may reject or truncate context | Implementer verifies advertised/model-observed context before admitting a measured run; no truncation fallback |
| `ASM-VR1A-002` | Existing ASR is adequate to judge planning quality | Three transcripts exist; known recognition/numeric traps remain | Model may be penalized for source errors | Freeze review cards with known ASR traps and distinguish source defect from planner defect |
| `ASM-VR1A-003` | Empty assets are valid for every compiled V1-A plan | Existing `AssetManifest` permits zero assets; V1-A forbids image blocks | Renderer could have an undocumented empty-manifest regression | Integration and existing renderer tests before real calls |
| `ASM-VR1A-004` | Current OpenAI-compatible endpoint supports JSON object output at temperature zero | Existing P0 transport uses this shape; exact V1-A model is not yet fixed | First call can fail before semantic evaluation | Capability/config preflight without transcript payload; visible configuration failure |
| `ASM-VR1A-005` | Three videos are sufficient for a G1 directional decision | Owner requested at least three different videos | Results do not generalize to arbitrary content | Scope conclusion to these fixtures and require new evidence for promotion |

## Risk register

| ID | Risk | Probability | Impact | Trigger | Prevention/mitigation | Owner | Verification |
|---|---|---|---|---|---|---|---|
| `RISK-VR1A-001` | Mapper omits substantive content | Medium | High | Missing review-card must-cover item or invalid exclusion | Exact segment accounting, exclusion review, ≥90% recall proposal | Owner | Mapper rubric and source citations |
| `RISK-VR1A-002` | Planner turns a minor point into a polished core claim | Medium | High | Human entailment/priority miss | Source-bound blocks, explicit omissions, zero-major-overclaim rule | Owner | Block-level rubric |
| `RISK-VR1A-003` | Unsupported or ASR-corrupted metric appears authoritative | Medium | High | Value absent/contradicted in cited text | Lexical metric gate; known-ASR trap card; omit uncertain metrics | Implementer/Owner | Metric fixtures and review |
| `RISK-VR1A-004` | Every video receives the same visual structure | Medium | Medium | Three normalized signatures identical or affordance mismatch | No block quota; content-affordance prompt; cross-video review | Owner | Signature plus block score |
| `RISK-VR1A-005` | Provider/schema drift lowers first-pass validity | Medium | Medium | Extra fields, Markdown wrapper, missing JSON, model version change | Strict schema, frozen snapshot, fail closed, new revision after change | Implementer | Contract failures and run manifest |
| `RISK-VR1A-006` | Full context exceeds provider capability | Low for fixed set | High | Rejection/truncation or missing tail content | Explicit model capability check; fixed size limit; no hidden chunking | Implementer | Request manifest and tail-source coverage |
| `RISK-VR1A-007` | Prompt injection inside transcript alters policy | Low | High | Output contains instructions/layout/unknown fields | Delimit data, declare it inert, strict output schema | Implementer | Adversarial fixture |
| `RISK-VR1A-008` | Selective reruns or tuning overstate quality | Medium | High | Prompt/model/compiler changes or failed runs disappear | Predeclare six IDs; freeze revision; retain all failures; new full revision after change | Owner | Denominator audit |
| `RISK-VR1A-009` | Restricted source/report is published | Low | High | Upload, deploy, public URL, redistribution | Local-only paths, no hosting, explicit rights boundary | Owner | Artifact and deployment diff review |
| `RISK-VR1A-010` | Credentials or transcript content leak through logs/errors | Low | High | Raw request/secret appears in diagnostics | Log credential presence only; bounded response/request metadata; local permissions | Implementer | Failure-log inspection |
| `RISK-VR1A-011` | V1-A changes the V0 renderer or frozen P0-B history | Low | High | Protected path diff or regression | Adapter boundary, protected-path review, full regression | Implementer | Git diff and pytest |
| `RISK-VR1A-012` | Human rubric is inconsistent between repeats | Medium | Medium | Per-category delta >1 without content explanation | Versioned rubric, block/source citations for low scores, one Owner reviewer | Owner | Repeat comparison |
| `RISK-VR1A-013` | Two-call claim is inflated by SDK/provider retry | Low | High | More wire attempts than admitted calls or ambiguous trace | Configure SDK retry count to zero for this adapter and record admitted/provider attempt counts | Implementer | Injected timeout/failure test |

## Intelligence, source-data, stability, customer-operation, vendor, compliance, and support risks

- Intelligence is `A1` draft generation only. A valid schema is not evidence of
  correct coverage, priority, or entailment; human evaluation remains required.
- Source ASR errors and absent visual facts bound the conclusion. V1-A may
  diagnose these gaps but cannot add OCR/VLM or silently use outside knowledge.
- Model outputs are non-deterministic even at temperature zero; deterministic
  compilation/replay and two measured repeats separate transport/schema
  stability from semantic stability.
- The configured provider is a single external dependency. Outage fails the run
  visibly; there is no availability promise or alternate provider.
- There are no customers or support obligations. The Owner operates, reviews,
  archives, and decides whether to run again.
- Full transcript processing is authorized and no expected private data exists;
  credentials remain secret and the non-public source-rights boundary persists.

## Resolved contradictions

| Apparent conflict | Resolution |
|---|---|
| V0 status says V1 automation is not authorized; Owner now requests V1-A design | The later explicit Owner message authorizes V1-A requirements design only. It does not authorize implementation. V0 evidence/status remains historical. |
| The product brief describes full V1 MP4 input, while V1-A excludes MP4/ASR | Full V1 is a staged vision. V1-A starts from existing transcript artifacts; V1-C owns MP4/ASR composition. |
| Planner chooses content but current V0 plan contains renderer-facing block types | Planner may choose from existing semantic block types; it may not choose visual layout, style, coordinates, or assets. |
| Full transcripts may be sent externally, while fixtures remain non-public | Processing authorization is not redistribution/publication authorization. Text may go only to the configured provider for V1-A; media and public artifacts remain prohibited. |
| V0 was visually successful, but V1-A uses no images | V1-A isolates content planning and renders with empty assets. Automatic image selection is deliberately deferred to V1-B. |

## Resolved Owner checkpoint

On 2026-08-30 the Owner replied “确认以上两项” to the two-item checkpoint. The
append-only ledger therefore retains the historical recommendations
`DEC-VR1A-025` and `DEC-VR1A-026`, and records separate confirmations:

- `DEC-VR1A-048`: the later implementer may select the exact
  OpenAI-compatible text model only inside the explicit full-context,
  JSON-object, temperature-zero, no-fallback, exact-snapshot boundary.
- `DEC-VR1A-049`: Development measurement is three videos × two repeats, using
  the thresholds in `09-test-acceptance.md` for coverage, grounding,
  first-response success, human quality, repeat stability, and anti-template
  variation.

No Owner checkpoint remains open in this requirements package. The independent
validator, not this narrative, decides handoff readiness.

## Residual non-blocking questions

| Question | Why non-blocking | Owner | Default | Decision deadline |
|---|---|---|---|---|
| Should successful local HTML be visually screenshot-reviewed at both 1080 px and about 390 px during S7? | V1-A measures content planning; current renderer already has responsive evidence | Owner | Inspect all six HTML files for overflow and screenshot one representative report per video if layout anomalies appear | Before S7 review handoff |
| Should raw provider response bodies be retained indefinitely? | Schema/debug evidence can be separated from long-term retention | Owner | Retain inside local run directories through Owner review, then archive/delete only by explicit Owner action | Before any G2 promotion |
| Which prompt wording revision wins after pre-measurement fake/manual calibration? | Prompt text can be refined before the frozen measurement without changing the contract | Implementer | Freeze exactly one Mapper and one Planner revision before declaring the six IDs | Before S6 |
