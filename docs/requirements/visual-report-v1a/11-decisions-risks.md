# Video Visual Report V1-A — Decisions and Risks

## Implementation-grade and promotion decision

| Field | Decision |
|---|---|
| Current grade | `G1 PROTOTYPE`, explicitly confirmed by the Owner |
| Allowed/prohibited use | One local Owner, three authorized transcript fixtures, two sequential semantic stages plus at most one technical retry per run, product-prototype review only; no production/public use, media upload, V1-B/C, or excluded infrastructure |
| Safety floor | Final source IDs/refs are strict, deterministic timestamps/IDs/compiler and current typed renderer remain authoritative, the only retry is explicit/identical/attempt-recorded, no fallback or semantic rewrite/merge/split/fabrication, every structural rule is logged, failures are retained, credentials are not disclosed |
| Deferred risks | End-to-end MP4 quality, visual-only information, asset selection, service resilience, tenancy, support, and publishing rights remain untested |
| Next grade/horizon | `G2 CONTROLLED_PILOT` only after V1-A quality acceptance and a separate Owner decision; no target date |
| Promotion evidence/approvers | The complete three-video product set passes Owner content/visual review; any later repeat-stability or G2 claim requires a newly authorized measurement plus workload, source-rights, operating/support, and recovery evidence; Owner approves |

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
| `DEC-VR1A-051 / USER_CONFIRMED` | Replace repeated manual construction sessions with one Goal session that diagnoses, repairs, verifies, measures, and hands off V1-A | Owner message after v3 failure | Reduce coordination overhead while finishing the already-approved V1-A scope | One task per failure; stop after diagnosis | More implementation autonomy, bounded by exact V1-A invariants and hard stops | Owner may interrupt or issue a new scope decision | Goal task evidence and terminal status |
| `DEC-VR1A-052 / USER_DELEGATED` | Automatic recovery occurs only across new immutable candidates/revisions, with three-video canaries, at most two new formal measurements, and at most 36 admitted calls | Goal-recovery delivery design under Owner delegation | Allow ordinary engineering repair without hiding retries or consuming unbounded calls | Unlimited loop; no repair; same-run retry | May stop before success, but preserves evidence and cost control | New Owner authorization for any further formal attempt | Run/revision inventory and call-count audit |
| `DEC-VR1A-053 / USER_CONFIRMED` | Freeze the exhausted experiment, restore canonical V1-A/anti-template behavior, then evaluate at most two schema-constrained strategies in one Goal | Owner continuation message | Stop manual task-card churn and end prompt micro-version overfitting | Continue the 36-call loop; abandon V1-A; unrestricted provider search | Stronger experiment discipline may produce an honest no-go sooner | New Owner decision | Frozen commit, strategy registry, complete canary sets, exact terminal |
| `DEC-VR1A-054 / USER_DELEGATED` | Predeclare both materially distinct tuples and prompt bundles; require native schema-constrained output; run all three canaries once; cap at 24 new calls and one formal revision | Owner explicitly allowed the Goal draft to be improved | Make provider comparison causal, bounded, and cross-video | JSON-object mode; per-video tuning; repair-and-rerun after canary | Ordinary fixes must finish before freeze; post-freeze defects consume a strategy | New Owner authorization for another experiment | Static anti-overfit tests, hashes, call ledger, manifests |
| `DEC-VR1A-055 / USER_CONFIRMED` | Design the next diagnostic as a minimal, continuous Goal-driven isolation experiment | Owner message after provider-conformance no-go | Avoid another oversized three-video run before the failing boundary is known | Immediately redesign V1-A; repeat the same DeepSeek strategy | Adds one focused design checkpoint while reducing calls and causal ambiguity | Owner may reject or revise the proposed card | `VR-V1A-BOUNDARY-ISOLATION-005` |
| `DEC-VR1A-056 / SYSTEM_RECOMMENDED` | Use one direct strict-output control provider, two independent synthetic stage calls, then at most one RLinf Mapper/Planner chain; cap at four requests and create no formal measurement | Requirements design | Separate schema/adapter, Mapper accounting, and Planner compiler pressure | Two-provider/full-cross-video comparison; synthetic-only test | One video cannot prove product quality, but is sufficient to locate the next design boundary | Owner execution checkpoint | Frozen call ledger and first-failing-layer result |
| `DEC-VR1A-057 / SYSTEM_RECOMMENDED` | Keep canonical Pydantic models unchanged and derive an auditable provider-facing strict schema using only the documented provider subset | Repository schema inspection plus current official OpenAI documentation | Current adapter omits `strict=true`; current generated objects contain optional fields and Planner emits nested `oneOf + discriminator` | Weaken canonical schema; rely on prompt-only JSON; send raw Pydantic schema unchanged | Small adapter work and equivalence tests; avoids confusing schema dialect with semantic failure | Remove the projection if a later provider accepts the canonical schema directly | Request-shape, schema-diff, equivalence, and synthetic canary evidence |
| `DEC-VR1A-058 / USER_CONFIRMED` | Cancel the official OpenAI Route A experiment; do not obtain/pay for an OpenAI key; proceed to V1-A contract-simplification design with the existing DeepSeek key; GLM/Qwen are optional alternatives only | Owner message | Avoid new provider cost/credential work and stop repeating strict-provider conformance | Purchase OpenAI access; immediately acquire GLM/Qwen; stop V1-A | Changes the product proposal contract rather than only transport; requires a new version and Owner checkpoint | A later explicit provider decision | Cancelled isolation card, no-call evidence, new task card |
| `DEC-VR1A-059 / SYSTEM_RECOMMENDED` | Keep two calls but use shallow semantic-v2 Mapper/Planner proposals plus an observable deterministic Topic Resolver/normalizer/compiler | Requirements design after frozen DeepSeek failures | Failures were dominated by exact topic count, unique segment accounting, typed-union counts and source bounds rather than proven content quality | Keep strict v1; merge calls; free-form Markdown | More compiler governance and normalization metrics; much lower provider schema pressure | Preserve v1 schemas and switch task version | V2 fixtures, repair ledger, replay, canary and rubric |
| `DEC-VR1A-060 / SYSTEM_RECOMMENDED` | Use one frozen DeepSeek Chat Completions JSON-object tuple, one 3-video canary, and one gated 6-run formal revision with an 18-call ceiling | Current DeepSeek access plus official JSON Output contract | Reuse available credential while retaining cross-video and repeat evidence | GLM/Qwen comparison; RLinf-only test; unbounded tune loop | No provider comparison; empty JSON remains a visible failure; 20% discard ceiling is a proposed quality bound | Owner may revise before authorization | Frozen manifests, exact call ledger, normalization-aware evaluator |
| `DEC-VR1A-061 / USER_CONFIRMED` | Reposition semantic v2 as a three-video product prototype: non-semantic compiler only, no semantic rewrite/merge/split, one explicit recorded technical retry, content/visual quality primary, schema-first-hit diagnostic | Owner message superseding `DEC-VR1A-059/060` | Test the actual Visual Report product hypothesis without letting incidental API/JSON faults or provider conformance dominate | Keep compliance experiment; no retry; semantic normalizer; six-run formal | Loses repeat-stability evidence but produces the smallest direct product proof; retry evidence and Owner judgment become essential | New Owner revision may reopen formal stability work later | Three reports, six viewport screenshots, attempt ledger, content/visual rubrics and cross-video review |
| `DEC-VR1A-062 / USER_CONFIRMED` | Freeze DeepSeek Chat Completions with Thinking enabled, reasoning effort high, `max_tokens=32768`, SDK retry zero, and one identical application retry; temperature is not stability evidence | Owner message after semantic-v2 product run | The failed/successful attempts all spent material output budget on reasoning; the next revision must test the intended Thinking path with enough combined reasoning/output headroom | Disable Thinking; retain 8192; rely on temperature zero | Higher bounded latency/token exposure, but directly tests the Owner-selected quality-oriented configuration | New complete three-video revision; historical run unchanged | Request-shape test, exact trace, three new retained runs and call-budget audit |
| `DEC-VR1A-063 / USER_CONFIRMED` | Put V1-B keyframes off the critical path; close text generation first, then build a local Web MVP before optional V1-B/V1-C | Owner product-priority message | Complete the smallest usable product loop before automating low-priority media assets | Follow A→B→C order; enter full MP4 pipeline | Text-only Web reports remain visually sparse but become directly usable in a browser | Later roadmap decision | Three text reports plus local Web workflow review |
| `DEC-VR1A-064 / USER_DELEGATED` | Use one continuous gated Goal: 3/3 text closure first, then a single-user localhost Web surface over the same run/runtime contracts | Owner request to set the next Goal | Avoid another manual session chain and avoid duplicating planning logic in a UI-specific path | Separate Goals; hosted service; static report browser only | Adds a small local HTTP/UI boundary, but no account/database/queue/deployment | Remove the Web slice without changing V1-A artifacts | Task card, provider-free Web integration, browser checks, real-report opening and protected-path review |
| `DEC-VR1A-065 / USER_CONFIRMED` | Replace semantic-v2's fixed aggregate budget with `max(minutes × 0.6, primary topics × 2, 6)`, recommended 6–24 blocks, 180–260 visible characters per block, and hard protection only above 32/8,000 | Owner supplied the exact budget direction after Wu Yi failed at 17 units | Scale editorial space with duration and semantic breadth; keep recommendations distinct from corruption limits | Retain fixed 14/2,600 for current v2; remove all limits; let model choose unbounded output | Amends semantic-v2 aggregate budgeting only; historical v1 and V0 lower-level contracts remain | Revert the new semantic-v2 budget version; retain all revision evidence | Formula/boundary/replay tests, budget artifacts, diagnostics, three-video product and visual review |
| `DEC-VR1A-066 / USER_DELEGATED` | Deliver adaptive budgeting and the already-built Web closure as one bounded G1 Goal on merged `visual-report@bb8f6f7` | Owner confirmed the workspace was committed/merged and requested the next modification plan | Avoid another partial task chain while preserving replay-first and post-freeze causal boundaries | Immediate real rerun; Web redesign; VEA redesign | Uses `ceil`, soft diagnostics, one new complete set, gated Web smoke, twelve-call maximum | Stop at an exact Owner-review terminal without acceptance | New task card, readiness package, frozen revision/call ledger, Web/browser evidence and status |
| `DEC-VR1A-067 / USER_CONFIRMED` | For the single DeepSeek network diagnostic, set only process-level `NO_PROXY=api.deepseek.com` and `no_proxy=api.deepseek.com` on the `uv` child process | Owner message for Task 009 | Test proxy reachability without changing global environment or product contracts | Global proxy/profile/.env change; provider/model/API change; alternate provider | Adds transport metadata and one controlled diagnostic path; does not prove provider or product quality | Remove the override in a later authorized task; preserve all canary evidence | Child-process environment and run snapshot |
| `DEC-VR1A-068 / USER_DELEGATED` | Publish `VR-V1A-NETWORK-RECOVERY-CANARY-009` as one Kling diagnostic-only full pipeline with an absolute three-call ceiling | Owner requested the minimum network-recovery test design and delegated the single-canary/3-call detail | Isolate network reachability after Task 008's external block while preserving the frozen product evidence | Continue Task 008's remaining videos; launch a new three-video measurement; tune or repair | A passing canary is useful transport evidence but cannot enter a product denominator or acceptance claim | Only a separately authorized new complete three-video revision may use recovery evidence | New run identity, `diagnostic_only` marker, attempt ledger, exact terminal |
| `DEC-VR1A-069 / USER_CONFIRMED` | Replace URL Web's active-run rejection with one explicit in-memory FIFO queue while retaining single-process, single-active-run execution and unique run evidence | Owner message after Task 011 local closure | A second browser tab must observe the active task and its own waiting state, then start automatically | Keep `409 RUN_ACTIVE`; add a database/durable worker queue; run requests concurrently | Queued work is visible and sequential but is not restart-durable; process exit leaves retained run directories without automatic resumption | Revert URL scheduling to active-only rejection without changing canonical run artifacts | Two-request API test, queue-position/status mapping, automatic handoff, and two-tab browser review |

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
| `ASM-VR1A-004` | The existing DeepSeek account exposes one text model whose JSON-object path fits both full-context calls | Owner has a DeepSeek key; official documentation covers JSON Output but warns of occasional empty content | Product set is externally blocked or remains technical-inconclusive after retry | Non-secret configuration/context preflight, frozen model/API snapshot, retained attempt evidence |
| `ASM-VR1A-005` | Three videos are sufficient for a G1 directional decision | Owner requested at least three different videos | Results do not generalize to arbitrary content | Scope conclusion to these fixtures and require new evidence for promotion |
| `ASM-VR1A-006` | The current V0 3–5-section/per-section schema can express useful reports within the new 32-block aggregate hard ceiling without a renderer/schema redesign | V0 permits up to five sections and seven blocks per section; current Wu Yi proposal has 17 units | Some larger valid semantic proposal may still fail a lower-level V0 limit or look visually poor | Replay all three saved proposals and inspect 1080/390 layouts before any new provider call; stop on required V0 contract change |

## Risk register

| ID | Risk | Probability | Impact | Trigger | Prevention/mitigation | Owner | Verification |
|---|---|---|---|---|---|---|---|
| `RISK-VR1A-001` | Simplified Mapper omits substantive content because exact segment accounting is no longer required | Medium | High | Missing review-card must-cover item, large uncovered span, or discarded topic | Expose uncovered/overlap diagnostics; ≥90% must-cover recall; no hidden topic synthesis | Owner | Mapper rubric, source refs and normalization ledger |
| `RISK-VR1A-002` | Planner turns a minor point into a polished core claim | Medium | High | Human entailment/priority miss | Source-bound blocks, explicit omissions, zero-major-overclaim rule | Owner | Block-level rubric |
| `RISK-VR1A-003` | Unsupported or ASR-corrupted metric appears authoritative | Medium | High | Value absent/contradicted in cited text | Lexical metric gate; known-ASR trap card; omit uncertain metrics | Implementer/Owner | Metric fixtures and review |
| `RISK-VR1A-004` | Every video receives the same visual structure | Medium | Medium | Three normalized signatures identical or affordance mismatch | No block quota; content-affordance prompt; cross-video review | Owner | Signature plus block score |
| `RISK-VR1A-005` | Provider/JSON-output drift masks product quality | Medium | Medium | Empty/invalid/truncated JSON, model/API version change | Frozen snapshot, explicit JSON-object mode/example/output limit, one identical recorded technical retry, separate technical-inconclusive terminal | Implementer | Attempt traces, retry fixtures and run manifest |
| `RISK-VR1A-006` | Full context exceeds provider capability | Low for fixed set | High | Rejection/truncation or missing tail content | Explicit model capability check; fixed size limit; no hidden chunking | Implementer | Request manifest and tail-source coverage |
| `RISK-VR1A-007` | Prompt injection inside transcript alters policy | Low | High | Output contains instructions/layout or attempts authority expansion | Delimit data, declare it inert, shallow allowlisted v2 parsing plus final canonical validation | Implementer | Adversarial fixture |
| `RISK-VR1A-008` | Selective reruns or tuning overstate prototype quality | Medium | High | Prompt/model/compiler changes, failed attempts disappear, or one video is replaced selectively | Predeclare three product-run IDs; freeze one tuple/prompt/compiler; retain every attempt; any material change requires a new complete product set | Owner | Three-run inventory, snapshots and attempt audit |
| `RISK-VR1A-009` | Restricted source/report is published | Low | High | Upload, deploy, public URL, redistribution | Local-only paths, no hosting, explicit rights boundary | Owner | Artifact and deployment diff review |
| `RISK-VR1A-010` | Credentials or transcript content leak through logs/errors | Low | High | Raw request/secret appears in diagnostics | Log credential presence only; bounded response/request metadata; local permissions | Implementer | Failure-log inspection |
| `RISK-VR1A-011` | V1-A changes the V0 renderer or frozen P0-B history | Low | High | Protected path diff or regression | Adapter boundary, protected-path review, full regression | Implementer | Git diff and pytest |
| `RISK-VR1A-012` | Human content/visual review is inconsistent across the three videos or viewports | Medium | Medium | Scores lack cited blocks/sources/screenshots or desktop/mobile judgments disagree without explanation | Versioned product rubric, evidence citations, six required screenshots and one Owner reviewer | Owner | Completed three-report review package |
| `RISK-VR1A-013` | The explicit retry becomes hidden regeneration or inflates the two-stage claim | Low | High | More than one retry/run, changed prompt/input, ambiguous stage/attempt trace, SDK retry | SDK retry zero; application retry budget one per run; identical request hash; distinguish two semantic stages from 2–3 wire attempts | Implementer | Injected timeout/JSON failure tests and exact attempt ledger |
| `RISK-VR1A-014` | Product Goal becomes an unbounded retry/tuning loop | Realized in the exhausted experiment | High | Prompt micro-versions, valid-semantic retries, selective video replacements, or >9 calls | Freeze one v2 tuple/prompt/compiler and three identities; one technical retry per run; no replacement/formal loop | Implementer/Owner | Frozen manifest, traces, run inventory and exact call ledger |
| `RISK-VR1A-015` | Valid JSON mode is mistaken for proof of V1-A product quality | High after v3 evidence | High | Provider returns parseable but weak semantic fields, or schema success becomes the headline | Treat JSON as transport envelope only; shallow allowlisted parse, observable non-semantic normalizer/resolver and unchanged final V0 validation remain authoritative; judge the rendered reports | Implementer/Owner | Raw/normalized/final artifacts, product runs and content/visual review |
| `RISK-VR1A-016` | Recovery hard-codes one structure and passes schema while destroying the content/anti-template hypothesis | Realized in the exhausted experiment | High | Exact-four topics, empty subtopics, exact 3/8 report, fixed topic assignment or block sequence appears in prompt/payload/helper | Restore canonical ranges; static anti-overfit tests; classify baseline `DO_NOT_PROMOTE`; cross-video signature gate | Implementer/Owner | Prompt/payload inspection, tests, three-video signatures |
| `RISK-VR1A-017` | Historical multi-provider comparison encourages a second adaptive arm after observing DeepSeek | Low under the current product prototype | High | GLM/Qwen or a second DeepSeek tuple is added after product evidence | `DEC-VR1A-058/061` keep this task on one tuple; any alternative requires a new Owner decision and a new complete product set | Implementer/Owner | Frozen single-tuple manifest and provider/model inventory |
| `RISK-VR1A-018` | Three rendered files are mistaken for product quality or Owner acceptance | Medium | High | Schema/render success becomes the headline; human rubrics are auto-filled | Require content/grounding/cross-video and real desktop/mobile review; leave rubrics pending Owner; stop before acceptance | Owner | Three-report review package, screenshots and status labels |
| `RISK-VR1A-019` | A JSON transport failure is mislabeled as product-route failure | Medium under semantic v2 | High | Request rejection, empty content, truncation, or invalid JSON occurs before shallow parsing | Record transport/finish/parse failures separately; allow the one identical technical retry; do not normalize invalid JSON or infer content quality; use the technical-inconclusive terminal if exhausted | Implementer | Provider trace, finish metadata and attempt result |
| `RISK-VR1A-020` | Historical synthetic, one-video, or provider-conformance evidence is promoted as current V1-A product evidence | Medium | High | Status claims product quality without three rendered reports and six viewport screenshots | Keep historical diagnostics labeled; require the complete three-video product set and Owner content/visual review | Owner | Artifact inventory and terminal conclusion review |
| `RISK-VR1A-021` | Deterministic compiler becomes hidden semantic author | Medium | High | A rule rewrites/truncates text, merges/splits units, moves claims, invents evidence, or cannot replay | Closed rule registry; ordered before/after ledger; whole-unit omission only; explicit no rewrite/merge/split tests; Owner inspects deltas | Implementer/Owner | Raw-normalized-final diff and 0/0 replay |
| `RISK-VR1A-022` | Compiler omits weak or invalid whole units and a thin report is called success | Medium | High | Must-cover loss, an unexplained omission pattern, or too little grounded material for an editorial report | Record every whole-unit omission with reason; prohibit semantic reconstruction; require grounding, content sufficiency and Owner quality review; a compilable thin report does not pass | Owner | Omission ledger, final-source audit and product rubric |
| `RISK-VR1A-023` | Thinking consumes the 32,768-token ceiling before a complete JSON answer | Medium until measured | High | `finish_reason=length`, reasoning tokens approach the ceiling, or content is absent/truncated | Send and trace the real Thinking/high controls; preserve one identical retry; freeze and run all three videos; stop honestly if any exhausts | Implementer/Owner | Request mock assertion, per-attempt usage/finish trace and 3/3 gate |
| `RISK-VR1A-024` | A new Web surface hides or duplicates the canonical planning state | Medium | High | UI invents states, retries independently, exposes secrets/paths, or writes reports outside the run recorder | `run.json` remains authority; Web invokes the same runtime; one retry owner; localhost/allowlisted IDs only; no client secret | Implementer | API/state mapping, duplicate-submit, path traversal, failure and browser tests |
| `RISK-VR1A-025` | The soft adaptive recommendation becomes a new exact template target | Medium | High | Reports cluster at the formula count, repeat filler, or use fixed distributions despite different sources | Prompt labels the value soft; no exact-count validation; record undershoot/overshoot; anti-template and redundancy review | Implementer/Owner | Prompt/payload inspection, cross-video signatures, density/redundancy rubric |
| `RISK-VR1A-026` | Raising the hard cap hides thin content or creates an unreadable long page | Medium | Medium/High | Blocks average far below 180 characters, hierarchy collapses, mobile overflow appears, or larger reports are called success solely because they compile | Aggregate density diagnostics, replay-first six-viewport gate, current-revision screenshots, Owner content/visual review; soft miss never auto-accepted | Owner | Character/block evidence, desktop/mobile screenshots and human rubric |
| `RISK-VR1A-027` | A process-scoped proxy override is mistaken for a provider, model, or product repair | Low | High | A canary changes request tuple, prompt/schema/compiler, or claims provider capability from transport recovery alone | Permit only inline `NO_PROXY/no_proxy`; record the labels; compare the request/config snapshot to Task 008; stop on any contract drift | Implementer/Owner | Task 009 environment and request audit |
| `RISK-VR1A-028` | A diagnostic canary is promoted into Task 008 or treated as product-quality evidence | Medium | High | Canary is added to a denominator, replaces the retained Kling failure, continues to another video, or triggers a new rubric/evaluator claim | `diagnostic_only=true`, separate run ID, explicit product-set exclusion, immediate-stop matrix, new Owner authorization for any complete revision | Owner | Manifest/run/aggregate immutability and status review |
| `RISK-VR1A-029` | The local URL queue is mistaken for a durable or concurrent service | Medium | Medium | UI hides queue position, two workers overlap, restart is claimed to resume work, or queued runs overwrite active evidence | One in-memory FIFO, one active worker, immediate unique run creation, explicit `QUEUED` display, automatic terminal handoff, and no restart-resume claim | Implementer/Owner | Sequential start-order test, retained run paths, API fields, and two-tab browser review |

## Intelligence, source-data, stability, customer-operation, vendor, compliance, and support risks

- Intelligence is `A1` draft generation only. A valid schema is not evidence of
  correct coverage, priority, or entailment; human evaluation remains required.
- Source ASR errors and absent visual facts bound the conclusion. V1-A may
  diagnose these gaps but cannot add OCR/VLM or silently use outside knowledge.
- Model outputs remain non-deterministic in Thinking mode, and DeepSeek ignores
  temperature there. This G1 product prototype does not claim repeat stability:
  deterministic compilation/replay, three different videos and explicit
  attempt traces separate product evidence from transport anomalies. Repeat
  measurement is deferred.
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
  temperature-zero, no-fallback, exact-snapshot boundary. Its historical
  JSON-object allowance was narrowed for the completed provider-conformance
  continuation by `DEC-VR1A-053/054`, which required native
  schema-constrained output.
- `DEC-VR1A-049`: Development measurement is three videos × two repeats, using
  the thresholds in `09-test-acceptance.md` for coverage, grounding,
  first-response success, human quality, repeat stability, and anti-template
  variation.

No Owner checkpoint remains open for the original requirements handoff. The
independent validator, not this narrative, decides that package's readiness.
The later boundary-isolation proposal was cancelled before execution.

After the v3 execution failure, the Owner separately authorized the unified
Goal recovery recorded as `DEC-VR1A-051`. `DEC-VR1A-052` translates that
authorization into a bounded engineering loop without changing the two-call,
strict-schema, fixed-denominator, quality-threshold, or Owner-acceptance rules.

That recovery ended at its frozen 36-call ceiling. The Owner then authorized
the next continuation in `DEC-VR1A-053` and explicitly allowed the draft Goal to
be improved. `DEC-VR1A-054` narrows the delegated implementation protocol:
native schema-constrained strategies only, both predeclared before any real
transcript call, one complete cross-video canary set per strategy, no
cross-strategy prompt learning, at most 24 new calls, and at most one formal
measurement. These rules restore the canonical V1-A content contract; they do
not change its quality thresholds or Owner-only acceptance.

## Task 009 Owner checkpoint

On 2026-08-31 the Owner confirmed the process-scoped DeepSeek network override
in `DEC-VR1A-067` and delegated the minimum diagnostic design in
`DEC-VR1A-068`. The resulting Task 009 card is ready for a separately started
construction session, but remains `READY_FOR_OWNER_V1A_REVIEW — NOT_STARTED`.
No new run, artifact, provider/model call, evaluator result, or acceptance
claim exists in this documentation session.

On 2026-08-31, `DEC-VR1A-061` superseded the unconfirmed semantic-v2
recommendations `DEC-VR1A-059/060`. The current contract is a three-video G1
product prototype, not a provider-conformance or six-run measurement. It keeps
semantic-v2 proposals, permits only non-semantic deterministic governance,
allows one identical and recorded technical retry per run, and makes report
content plus desktop/mobile visual review the primary evidence. This confirms
the product contract but does not itself authorize implementation or provider
calls.

Later on 2026-08-31, `DEC-VR1A-062` replaced only the future runtime
configuration portion of that contract: the next complete product revision uses
Thinking enabled, reasoning effort high, `max_tokens=32768`, and one identical
application retry. Temperature remains trace metadata but is not a stability
control. `DEC-VR1A-063/064` put keyframe automation off the critical path and
delegate a gated local Web MVP after a clean 3/3 text-report result. The Web
slice is not retroactively part of V1-A and does not authorize V1-B, V1-C,
MP4/ASR, hosting, or production use.

Also on 2026-08-31, the Owner confirmed `DEC-VR1A-065`: semantic-v2 report
capacity is guided by duration and canonical primary-topic breadth, with 6–24
as the recommended block range and 180–260 visible characters per compiled
block as aggregate density guidance. Only values above 32 blocks or 8,000
visible authored characters are aggregate hard failures. `DEC-VR1A-066`
delegates the deterministic translation and one continuous replay-first,
three-video, gated-Web Goal on the merged baseline. These decisions do not
authorize semantic budget repair, exact-count prompting, V1-B/C, deployment,
or Owner acceptance.

## Residual non-blocking questions

| Question | Why non-blocking | Owner | Default | Decision deadline |
|---|---|---|---|---|
| Should the six required screenshots use a browser/device preset beyond exact 1080 px and approximately 390 px widths? | Both viewports are fixed, but the capture engine and height policy do not change the product judgment | Implementer | Use the existing browser capture path, full natural page height, and record exact viewport metadata | Before product Run 1 |
| Should raw provider response bodies be retained indefinitely? | Schema/debug evidence can be separated from long-term retention | Owner | Retain inside local run directories through Owner review, then archive/delete only by explicit Owner action | Before any G2 promotion |
