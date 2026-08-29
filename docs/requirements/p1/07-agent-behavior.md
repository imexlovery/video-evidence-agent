# P1 Agent Behavior

## 1. Intelligence target and autonomy

Non-AI baseline is B1: deterministic R2/R3 character TF-IDF Top-5 followed by one text-model
answer under P0 Evidence Gate. B2 adds only observation-driven selection between rewrite search,
neighbor inspection, answer and refusal. Its useful task is recovering missing necessary evidence,
not autonomous action.

Autonomy is `A2 tool-assisted`: the model may choose among two read-only Tools within a hard
budget, but cannot select video/source/Top-K, mutate data, call external tools directly, alter
policy, approve evidence or determine H4. Higher autonomy is prohibited.

## 2. Agent responsibilities and prohibitions

The model may interpret the question and observed transcript, formulate one bounded rewrite,
choose an observed anchor/radius, synthesize a Chinese answer, cite eligible segment IDs or refuse.
It must not invent source fields, request full transcript/Gold/history, cross video boundaries,
change budget/profile, invoke VLM/web, write files, score itself, retry errors, store memory or emit
hidden reasoning as an artifact.

Deterministic code owns manifest/hash/auth checks, first search, JSON/schema validation, action and
Tool budgets, current-video scope, duplicate detection, eligible evidence, quote/time hydration,
refusal invariants, state transitions, scoring and terminal mapping.

## 3. Policy hierarchy and hard gates

`POL-P1-001` is the deterministic authority policy for this experiment.

Order is fixed: frozen Owner decisions > manifest/contracts > deterministic validators/Gate >
model action/proposal > transcript/tool content. Retrieved transcript is untrusted data and cannot
issue instructions.

Hard gates execute before relevant model calls: source/hash validity, formal authorization,
question/video scope, initial search invariant, action schema, budget, Tool arguments/anchor,
eligible evidence, final schema/provenance. Any unavailable mandatory gate stops; no model fallback
may weaken it. Final validation repeats current-video and eligible-evidence checks.

## 4. AGENT-P1-001 action contract and loop

```json
{
  "action": "FINAL_ANSWER | REFUSE | SEARCH_VIDEO | INSPECT_SEGMENTS",
  "query": "present only for SEARCH_VIDEO",
  "anchor_segment_id": "present only for INSPECT_SEGMENTS",
  "radius": 1,
  "proposal": "P0 AnswerProposal, present only for FINAL_ANSWER"
}
```

`additionalProperties=false`; mutually exclusive fields are enforced. The deterministic first
search consumes call 1. After each observation, the model gets remaining budget and may terminate
or request one valid Tool action. Maximum Tool calls is 3. At zero remaining calls, a nonterminal
action becomes fail-closed `INSUFFICIENT_EVIDENCE(reason=tool_budget_exhausted)`.

Invalid action/schema causes one recorded refusal and no repair prompt. Tool errors are not retried.
Provider malformed output/timeout is a failed formal revision, not an Agent-selected refusal.

## 5. Context and memory

Context order: immutable policy/contract, current question/video ID, remaining budget, compact
validated action history, de-duplicated authoritative observations in first-seen order, required
output schema. Gold, historical answers, hidden evaluator labels, credentials and other videos are
excluded. At most 15 unique segments can be observed (3 calls × 5); duplication does not enlarge
the set. If provider context requires truncation, retain policy/question, then newest decision-
relevant observations while recording omitted IDs; truncation that could remove a cited segment
forces refusal.

Memory is run-local only. Model cannot write session/long-term memory. Trace stores validated
actions and observations, not chain-of-thought. No cross-question context or automatic feedback
learning exists.

## 6. Grounding, uncertainty and fallback

- `ANSWERED` requires at least one eligible citation; legal provenance is necessary but not proof
  of semantic support.
- When mandatory answer points are not adequately supported, the model must refuse rather than
  guess. No decorative confidence score is exposed.
- Missing source, low support, budget exhaustion, unsafe/invalid action or Tool error fails closed.
- Provider outage/malformed/timeout blocks the revision; B1 deterministic retrieval artifacts
  remain available but no answer-quality comparison is claimed.
- Owner may correct semantic review labels only by signed review revision; runtime output is not
  edited in place.

Unacceptable outputs: fabricated/altered quote or timestamp, cross-video citation, Gold leakage,
unsupported disclosed fact, answer with no evidence, non-empty refusal, budget breach, hidden
retry, B0 comparison claim, or report that calls evidence-only improvement answer-quality gain.

## 7. Evaluation and H4

`EVAL-P1-001` is the frozen same-revision B1/B2 evaluation and H4 decision contract.

Population: all existing 12 regression questions plus 1..4 pre-frozen candidate, with challenge
slice defined only by current B1 failures after freeze. Report lexical/paraphrase/multi-evidence/
unanswerable and candidate taxonomy slices separately. B1 is the only formal baseline; B0 is
`NOT_AVAILABLE/NOT_RUN`.

`KEEP_AGENT_EXPERIMENTAL` requires all:

- at least 2 net recovered challenge cases;
- existing 12-question FullyCorrect and FullySupported are not below same-revision B1;
- CorrectRefusal not below and FalseRefusal not above B1;
- invalid/fabricated citation, timestamp and cross-video count = 0;
- schema failures, budget violations and uncaught Tool errors = 0;
- at least one direct-termination and one observation-driven recovery Trace;
- mean Tool Calls `<=2.0`; limit-reaching runs fail closed;
- mean B2 total tokens `<=3.0 ×` same-revision B1 mean;
- fixed action-sequence ratio `<80%` for Agent retention.

Terminal routing is specified by TEST-P1-014. If action sequence is fixed/reproducible, route to
`CONVERT_TO_WORKFLOW`; if Tool acquisition cannot reach missing evidence for most challenge cases,
route to `REPAIR_RETRIEVAL_FIRST`; safety/regression/cost failure or no useful loop increment routes
to `DELETE_AGENT`. No generic “experiment failed” terminal exists.

This is a G1 count gate, not statistical significance. Any promotion or dataset/prompt/model/tool
change requires new frozen evaluation and Owner sign-off. No production feedback, drift monitor,
canary or online training applies; G2 must add them before real-user use.

## 8. Interrupt and multi-agent

Cancellation is a deterministic high-priority interrupt checked before Tool/provider calls and
before artifact commit. It locks the run, rejects late provider results, emits one idempotent
`run_cancelled` event and preserves partial Trace. Since Tools are read-only there is no
compensation.

Multi-agent topology is not applicable: one bounded controller owns all actions; there are no
workers, aggregation, conflicts or child failure semantics.

## 9. Versioning

Manifest records prompt ID/hash, action schema, Tool schemas/profile, Evidence Gate version,
provider/model identifier, dataset/Gold/source hashes and rubric. Contract/model drift invalidates
the run before use. Upgrade and rollback owner is the local Owner; rollback disables/removes B2 in
a new implementation change while keeping evidence.
