# Video Visual Report V0 — Agent and Model Behavior

## Applicability

Not applicable at runtime. V0 is intentionally a deterministic renderer for
human-authored structured content. It contains no LLM, Agent, RAG, retrieval,
provider, prompt, tool loop, or model-controlled layout.

## Non-AI baseline, intelligent task value, and autonomy level

- **Baseline:** transcript or ordinary Markdown summary plus manually viewed
  video frames.
- **V0-added value:** consistent information hierarchy, semantic component
  choice already encoded in the plan, visual relationships, evidence frames,
  timestamps, and editorial polish.
- **Autonomy:** `A0` deterministic execution.
- **Justification:** the experiment asks whether the rendering grammar creates
  value before testing automated understanding/planning.

## Responsibilities and prohibited responsibilities

The runtime validates structured input, resolves local assets, escapes content,
maps known block types to components, calculates process/spine layout, and writes
HTML. It must not summarize, rank importance, select facts, infer relationships,
choose block types, acquire media, call a model, retrieve context, or repair
invalid content.

## Deterministic versus model-controlled decisions

| Decision | V0 authority | Future V1 authority boundary |
|---|---|---|
| What the complete video covers | Human mapping | Topic Mapper model, coverage/recall oriented |
| What the report should emphasize/omit | Human plan | Report Planner model, compression oriented |
| Block type and order | Human plan | Report Planner may propose typed values only |
| Asset need/reference | Human plan/selection | Planner may request semantic need; Asset Resolver resolves it |
| Font, size, spacing, grid, color, line break, image ratio | Deterministic renderer | Always deterministic renderer |
| SVG paths, node placement, x/y coordinates | Deterministic renderer | Always deterministic renderer |
| HTML/CSS output | Deterministic renderer | Always deterministic renderer |

Topic Mapper and Report Planner are permanently distinct responsibilities. V1
must not merge them merely to reduce a model call.

## Hard constraints and safety gates

| Gate | Runs before | Evidence | Failure behavior | Final-output recheck |
|---|---|---|---|---|
| Schema/version gate | Rendering | Pydantic validation | Non-zero; no fallback | Integration test |
| Source/asset reference gate | Component render | ID, bounds, path containment, file checks | Non-zero with offending ID | Final plan validation |
| HTML escaping gate | Markup insertion | Escaping tests | Treat content as text | Security fixture inspection |
| Local-only/network gate | Browser acceptance | HTML dependency inspection/network panel | Reject candidate | Final browser check |
| Owner visual gate | V0 acceptance | Final HTML and screenshots | Return to visual iteration | Owner only |

## Model capability and provider constraints

No model or provider is permitted in V0 runtime or render verification. Human or
LLM-assisted drafting may occur outside the product, but the committed renderer
input must be explicit validated JSON and the render command must make zero model
calls.

## Instruction and policy hierarchy

For implementation sessions: latest owner message → root `AGENTS.md` → V0
readiness/handoff package → bounded task → existing project docs/code. Source
media rights and frozen P0-B invariants are hard constraints. Untrusted transcript
or plan text never becomes an instruction to the runtime.

## Context construction, provenance, freshness, and budget

There is no runtime AI context. The human content-authoring context is the fixed
RLinf transcript, inspected frames, manifest, and explicit source refs. String,
list, and section budgets are schema constraints calibrated against the first
visual report rather than token budgets.

## Tool catalog, loop limits, permission, approval, and side effects

The runtime has no tool catalog. Its only side effect is replacing the explicit
local output after success. FFmpeg and browser usage belong to the bounded
implementation task, not to an autonomous product loop. Public upload/deployment
is prohibited.

## Multi-agent topology and result aggregation

Not applicable. The V0 product has no Agent or multi-agent topology. The
implementation task is intentionally executable by one session to keep visual
judgment coherent.

## Memory read, write, retrieval, correction, and deletion

No runtime memory. The validated plan/assets are request data; task/status docs
are durable engineering context. Correction means edit inputs/source, rerender,
and refresh review evidence. Local output deletion is owner-controlled.

## Structured output and validation

The input, not a model output, is structured. Closed Pydantic discriminated unions
reject unknown blocks and extra style/layout primitives. Renderer output is HTML,
validated through structural tests and real browser inspection.

## Grounding, evidence, uncertainty, abstention, and escalation

Every factual block has timestamped source refs. Ambiguous ASR wording or numbers
are omitted or rewritten without unsupported precision. The renderer does not
assert epistemic confidence. A content conflict stops authoring for direct source
inspection; it is not routed through P0-B Evidence Gate.

## Untrusted-content and prompt-injection defenses

Transcript, plan, captions, and source metadata are data, not executable
instructions. Escape all authored strings, reject URL/escaping asset paths, use
no `innerHTML` insertion from raw content, and load no remote scripts/styles.

## High-priority interruption, cancellation propagation, and late-output rejection

Ctrl-C cancels the foreground process. Validation/rendering uses a temporary
output so cancellation or late failure cannot replace a prior valid report. There
is no background result that can arrive after cancellation.

## Fallback and escalation

| Failure | Required behavior | User-visible result | Operational signal |
|---|---|---|---|
| Invalid plan/assets | Reject | Stable error with ID/path | Non-zero exit |
| Missing optional asset reference on a non-image block | Render text-only component | Normal report | Component test |
| Required image missing | Reject | Asset error | Non-zero exit |
| Ambiguous fact | Omit/rewrite before plan acceptance | No unsupported claim | Content review note |
| Visual defect | Iterate deterministic renderer/plan | Updated screenshots | Task evidence |
| Rights conflict | Stop use and remove derived local assets if authorization is withdrawn | No report release | Status/risk update |

No automatic generic-component, provider, remote asset, or second-template
fallback is allowed.

## Evaluation, thresholds, and release gates

| Evaluation slice/case | Baseline | Metric | Threshold | Unacceptable outcome | Owner |
|---|---|---|---|---|---|
| Determinism | Same plan/assets | Equivalent HTML | Repeat passes | Random/current-time drift | Implementer |
| Contract safety | Invalid fixtures | Rejection rate | All defined invalid cases rejected | Silent fallback or broken HTML | Implementer |
| Content traceability | Transcript/frames | Factual blocks with source refs | 100% | Unsupported factual block | Owner/implementer |
| Visual comprehension | Transcript/Markdown | Owner 60–90 second review | Thesis/progression/relation/takeaways recovered | Pretty but structurally unclear | Owner |
| Save value | Transcript/Markdown | Owner preference | Report preferred | Owner would not retain it | Owner |

## Production feedback, quality/drift monitoring, promotion, rollback, and re-evaluation

Not applicable to G1 production operations. Material plan/renderer changes require
new screenshots and owner review. V1 promotion requires a separate decision; V0
does not auto-promote based on passing tests.

## Versioning and reproducibility

Version the plan and asset schemas; record repository revision and commands in
task evidence. Avoid generated time/random data. Local artifact hashes are not a
requirement. Preserve failed task evidence rather than rewriting history.

## User control and explanation

The owner can inspect/edit structured inputs, view exact timestamps and source
attribution, delete local artifacts, reject visual output, and authorize or deny
the next phase. The renderer must remain explainable as a direct typed-block to
component mapping.
