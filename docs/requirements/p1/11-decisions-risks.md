# P1 Decisions and Risks

## 1. Accepted decisions

| Decision | Source/status | Choice and drivers | Alternatives / tradeoff / reversal | Verification |
| --- | --- | --- | --- | --- |
| DEC-P1-001 | Owner confirmed | G1 local prototype; feasibility only | G2+ rejected now; narrow use lowers operational scope; promotion is separate | grade boundary tests |
| DEC-P1-014/018 | Owner confirmed | Conditional Go, Headroom >=2 before B2 | unconditional build rejected; No-Go preserves time | TEST-P1-001/002 |
| DEC-P1-015 | Owner confirmed | two read-only Tools, Top-K=5, max calls=3 | universal retriever/free K rejected; bounded causal attribution | TEST-P1-003..006 |
| DEC-P1-016 | Owner confirmed | Native Python `FRAMEWORKLESS`; no LangGraph/Hypha/VLM | frameworks/modal path rejected as confounders; reversible by new phase | TEST-P1-007 |
| DEC-P1-017 | Owner confirmed | P0 answer-level output | claim-level deferred until observed need; avoids changing both groups | TEST-P1-008 |
| DEC-P1-019 | Owner confirmed | H4 net recovery >=2 strong retention Gate; evidence-specific terminals | generic success/failure rejected; may remove Agent | TEST-P1-014 |
| DEC-P1-020 | Owner confirmed | B0 absent, not restored, no three-way claim | fabricating/reconstructing baseline rejected | TEST-P1-013 |
| DEC-P1-021/029 | Owner confirmed | current phase docs only, no provider; later exact approval | implicit credential permission rejected | TEST-P1-015 |
| DEC-P1-022 | Owner delegated | reversible internal task/schema/test details inside fixed envelope | user-visible/threshold/framework/provider changes excluded | package + tests |
| DEC-P1-030 | Owner delegated | G2 promotion contract only after P1 evidence/new approval | no automatic maturity upgrade | promotion checklist |

Historical `SYSTEM_RECOMMENDED` records remain append-only in `decision-evidence.jsonl`; Owner
confirmation records supersede the matching recommendations without rewriting history.

## 2. Grade decision and deferred risk

G1 permits one local Owner, public/authorized data, read-only actions and no service promise. Safety
floors are provenance, scope/budget validation, secret redaction, immutable evidence and failure
visibility. Deferred production/customer controls create no current release gap because prohibited
use is enforceable; their risk is accidental scope expansion. Triggering real users/data/shared
operation immediately blocks use pending G2 review and tests.

## 3. Platform/capability classification

The problem is product-specific experimental behavior plus project-owned integration. No shared
platform/framework gap is claimed. Existing retrieval/segment/answer contracts are reused through
public project modules; new Tool/controller/Trace/eval behavior belongs only in this repository.
Changing a shared framework is prohibited and no cross-project reuse claim exists.

## 4. Risk register

| ID | Risk | Prob. | Impact | Trigger | Prevention / mitigation | Owner | Test |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RISK-P1-001 | current B1 has insufficient Headroom | high | high | qualifying count <2 | pre-freeze/B1-first; terminate No-Go | Product Owner | TEST-P1-001 |
| RISK-P1-002 | candidate selection leaks Gold or overfits | medium | high | question wording derives from Gold transcript or post-B2 edits | taxonomy provenance, timestamp/hash freeze, retain all | Data Owner | TEST-P1-017 |
| RISK-P1-003 | cross-video/fabricated evidence | low | critical | citation outside eligible set | trusted executor/Gate/current-video source | Engineering Owner | TEST-P1-009 |
| RISK-P1-004 | Agent is disguised fixed workflow | medium | medium | sequence ratio >=80% or deterministic replay reproduces benefit | action distribution + workflow terminal | AI-quality Owner | TEST-P1-014 |
| RISK-P1-005 | B2 harms correct/refusal baseline | medium | high | any H4 regression | same revision B1, no-regression Gate, delete Agent | AI-quality Owner | TEST-P1-014 |
| RISK-P1-006 | cost/latency expansion | medium | medium | mean tokens >3×, calls/timeout bounds crossed | hard budgets, report usage, fail closed | Product Owner | TEST-P1-006/014/020 |
| RISK-P1-007 | provider drift/outage invalidates comparison | medium | high | contract/hash/timeout/malformed output | snapshot, preflight, no fallback/retry, preserve revision | Engineering Owner | TEST-P1-015/023 |
| RISK-P1-008 | immutable P0/P1 history is overwritten | low | critical | duplicate run/path or correction in place | atomic new revision, hash/idempotency checks | Data Owner | TEST-P1-011/024 |
| RISK-P1-009 | provenance is mistaken for semantics | medium | high | automated report calls citation valid answer correct | Owner semantic rubric and scoped claims | AI-quality Owner | TEST-P1-013/014 |
| RISK-P1-010 | secret or hidden reasoning leaks to Trace | low | high | env/prompt internals appear in artifacts | whitelist fields, redaction scan, boolean credential presence | Security Owner | TEST-P1-010 |
| RISK-P1-011 | local device loss removes untracked eval assets | low | medium | file unavailable/hash mismatch | accepted G1 SPOF; stop, reacquire authorized asset, new revision | Operations Owner | TEST-P1-023 |
| RISK-P1-012 | P1 is presented as B0/B1/B2 proof | medium | high | report/README claim drift | B0 fixed status contract and claim check | Product Owner | TEST-P1-013 |

## 5. Assumptions

| Assumption | Evidence state | Impact if wrong / resolution |
| --- | --- | --- |
| P0 local segment/media artifacts remain readable at implementation start | non-critical, verified at prior design audit but driftable | TASK-P1-000 fails before construction; asset recovery/new baseline requires Owner review |
| Existing provider supports required structured text response at formal time | non-critical external dependency | preflight/fixture contract failure blocks calls; no provider substitution |
| Local disk has capacity for one new revision | non-critical operational assumption | preflight blocks before formal run; Owner frees/chooses storage without altering frozen history |

No assumption may override a Gate. There are no residual blocking questions.

## 6. Resolved contradictions

- “Direct Model baseline” is resolved as absent, not incomplete work to restore.
- “Agent experiment failure” is resolved into evidence-specific terminals.
- A provider credential existing locally does not equal call authorization.
- P0 legal provenance validation does not equal semantic correctness; Owner review remains.
- A while-loop alone does not prove dynamicity; Trace distribution and recoveries do.

