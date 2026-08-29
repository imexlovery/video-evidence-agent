# P1 Test and Acceptance Contract

## 1. Levels and environments

- Static/contract: JSONL/JSON/schema/ID/reference/manifest/hash checks in local `.venv`.
- Unit: Tool validators, budget, state transitions, eligibility, Gate, terminal mapping.
- Integration: frozen segment source → Tool → Trace → P0 answer contract → scorer, provider faked.
- Offline replay: one success and one failure/recovery fixture; zero external call.
- Formal local evaluation: later, only after Headroom/offline/freeze/Owner provider gates.
- Security/fault/load/regression: current-video isolation, injection/malformed/timeout/duplicate,
  sequential full population, P0 regression.
- UI/API/migration/backup-restore/accessibility/multi-agent tests: not applicable because those
  surfaces/stores/topologies do not exist. CLI output readability and exit codes remain applicable.

Test data is limited to frozen public/authorized technical-video segments and synthetic malformed
fixtures. Gold is scorer-only. Tests must not print secrets or call provider unless explicitly in
the later authorized formal task.

## 2. Acceptance cases

| ID | Given / When / Then | Acceptance evidence |
| --- | --- | --- |
| TEST-P1-001 | Given frozen candidates, when B1 has fewer than 2 qualifying failures, then report all results and terminate `NO_GO_INSUFFICIENT_HEADROOM` before B2 code | Headroom report + task-state inspection |
| TEST-P1-002 | Given >=2 answerable B1 runs with `AllNecessaryEvidence@5=false`, when scorer-only oracle identifies a missing Gold unit reachable by allowed rewrite/neighbor action without provider, then Headroom passes | Owner review + Gold delta evidence + zero-call counter |
| TEST-P1-003 | Given any search request, when executed, then current video/profile/Top-K=5 are invariant and max five authoritative hits return | Tool unit/contract tests |
| TEST-P1-004 | Given observed anchor and radius 1/2 including start/end boundaries, when inspect runs, then ordered same-video neighbors <=5 return | boundary tests |
| TEST-P1-005 | Given unknown/unobserved/cross-video anchor, invalid radius or duplicate action, when validated, then stable error and no source read/model retry occurs | negative Tool Trace |
| TEST-P1-006 | Given a fourth Tool request, when validated, then it is not executed and run refuses with budget reason | budget test |
| TEST-P1-007 | Given dependency/static inspection, when P1 is built, then no LangGraph/Hypha/VLM/framework runtime/import/config exists | lock/import/source scan |
| TEST-P1-008 | Given answered/refused/malformed proposal, when Gate runs, then exact P0 answer-level schema and invariants hold; no claim schema required | schema tests |
| TEST-P1-009 | Given valid, fabricated, stale, duplicate and cross-video citations, when Gate runs, then only unique eligible current-run IDs hydrate authoritative quote/time and all others fail closed | provenance tests |
| TEST-P1-010 | Given success/failure/cancel runs, when Trace closes, then required events/versions/budgets/IDs exist and chain-of-thought/secrets/Gold do not | JSON schema + redaction inspection |
| TEST-P1-011 | Given committed revision, when duplicate run/correction/replay occurs, then old files remain byte-identical and new work gets new ID | hash/idempotency test |
| TEST-P1-012 | Given formal manifest, when B1/B2 run, then shared inputs/source/provider/answer/Gate/rubric hashes match and only dynamic actions differ | manifest comparison |
| TEST-P1-013 | Given any final report, when claims are validated, then B0 is `NOT_AVAILABLE/NOT_RUN`, no three-way claim appears, and evidence-only gain is labeled accurately | report contract inspection |
| TEST-P1-014 | Given valid Headroom/H4 metrics, when decision rules run, then exactly one terminal follows the priority matrix below and generic failure label is impossible | parameterized decision tests |
| TEST-P1-015 | Given no, expired, revoked or mismatched authorization, when formal command starts, then zero provider calls occur and state waits/stops | adapter fake/call counter |
| TEST-P1-016 | Given malformed/oversized/duplicate/out-of-order/late/cancelled/provider-failed inputs, when run executes, then the defined fail/partial/cancel state and no fabricated answer result occur | fault/recovery tests |
| TEST-P1-017 | Given candidate set, when freeze validates, then count <=4, unique questions, source taxonomy refs and Gold-before-B2 timestamps/hashes all pass | freeze validation |
| TEST-P1-018 | Given B2 run, when first Tool event is inspected, then it is `search_video` with normalized original question; later rewrites must differ and reference prior observation | Trace behavior test |
| TEST-P1-019 | Given injection text inside transcript, when model proposes policy/tool override, then validator rejects it and preserves trusted policy | adversarial fixture |
| TEST-P1-020 | Given full offline workload and a concurrent duplicate process, when soak/spike tests run, then one sequence completes within declared bounds and duplicate is rejected | workload evidence |
| TEST-P1-021 | Given success Trace fixture, when replay runs offline, then observations/eligibility/Gate/terminal reproduce with zero provider calls | replay hash comparison |
| TEST-P1-022 | Given cross-video/budget failure fixture, when replay/recovery runs, then same error/terminal reproduces and a new revision can start without modifying old files | failure/recovery evidence |
| TEST-P1-023 | Given source/prompt/tool/provider contract hash drift, when preflight runs, then formal execution stops before external call | drift test |
| TEST-P1-024 | Given existing P0 suite, when implementation completes, then P0 tests/reports/contracts remain unchanged and tests pass | regression diff/test evidence |

Valid input, 500-codepoint boundary and empty/501-codepoint invalid question are included under
TEST-P1-016. Empty/no-change Tool results, partial failure Trace, refusal, cancellation, stale hash,
unauthorized call and late result all have explicit fixtures. Gold/source rights and corpus license
metadata are inspected in TEST-P1-017/023; poisoning and correction/reprocessing are covered by
TEST-P1-019/011.

## 3. H4 terminal priority matrix

| Condition, evaluated top to bottom | Required terminal |
| --- | --- |
| Headroom qualifying count `<2` | `NO_GO_INSUFFICIENT_HEADROOM` |
| Formal revision incomplete due provider/runtime infrastructure failure | `EVALUATION_BLOCKED_PROVIDER_FAILURE`; H4 not claimed |
| Any invalid citation/timestamp/cross-video, uncaught error, budget breach, regression/refusal Gate failure, or token ratio >3 | `DELETE_AGENT` |
| Allowed Tools fail to add missing Gold evidence in >50% of challenge cases | `REPAIR_RETRIEVAL_FIRST` |
| A deterministic fixed recipe reproduces observed benefit, or one action sequence covers >=80% | `CONVERT_TO_WORKFLOW` |
| Net recovered challenge cases >=2 and all H4 gates pass with fixed-sequence ratio <80% | `KEEP_AGENT_EXPERIMENTAL` |
| Remaining valid result with net recovery <2 | `DELETE_AGENT` |

“Benefit” in the workflow row must be evidenced by at least one predeclared primary metric gain
without safety regression; otherwise the last row applies. This mapping permits non-Agent outcomes
without hiding why the Agent was not retained.

## 4. Requirement traceability

| Goal | Scenario | Requirements | Design | Tests | Operating signal |
| --- | --- | --- | --- | --- | --- |
| GOAL-P1-001 | SCN-P1-001 | REQ-P1-001/013 | Headroom builder/B1 runner | TEST-P1-001/002/017 | SLO-P1-007 |
| GOAL-P1-002 | SCN-P1-002/003/004 | REQ-P1-002..007/011/012/014 | Tool/controller/Gate | TEST-P1-003..012/015/016/018/019/023 | SLO-P1-001..005 |
| GOAL-P1-003 | SCN-P1-004 | REQ-P1-009/010 | Evaluator/terminal mapper | TEST-P1-013/014 | H4 rows |
| GOAL-P1-004 | all | REQ-P1-006/008 | manifest/artifact writer | TEST-P1-009..011/021/022/024 | SLO-P1-002/006 |

## 5. Release acceptance

For each vertical slice, machine tests plus listed artifact hashes are required. Formal B1/B2
release additionally needs Owner semantic review of answer correctness/support/refusal and Trace
dynamicity. A checker cannot infer semantic support from provenance alone.

| Acceptance domain | Owner | Required evidence / applicability |
| --- | --- | --- |
| Product/business | local Owner | Headroom/H4 terminal and claim wording |
| Data | local Owner | source/Gold rights, hashes, lineage, immutable manifests |
| AI quality | local Owner | same-revision B1/B2 metrics + semantic review |
| Security/privacy | local Owner | no secret/Gold leakage; scope/provenance adversarial tests |
| Performance/reliability | local Owner | SLO-P1-001..007 evidence |
| Operations/support | local Owner | local runbooks; external support not applicable |
| Legal/compliance | local Owner | source license/authorized-use inspection; regulated use prohibited |
| Commercial | not applicable | no customer, payment or service promise |

G2 promotion acceptance is separate: identity/consent/audit/recovery/support/load/export/deletion/
rollback evidence plus new Owner sign-off. Passing G1 tests does not imply pilot or production use.
