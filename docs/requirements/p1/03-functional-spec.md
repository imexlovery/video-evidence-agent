# P1 Functional Specification

## 1. Capability inventory

| Capability | Contract | P1 state |
| --- | --- | --- |
| Baseline/asset freeze | Hash source, dependency, dataset and historical artifacts | required |
| Headroom construction and B1 run | Freeze before B2; preserve every result | required, first critical path |
| Search Tool | Existing R2/R3 retrieval wrapped read-only | required after Headroom pass |
| Inspect Tool | Ordinal-bounded neighbor lookup | required after Headroom pass |
| Trace and Evidence Gate | Run-local provenance and fail-closed validation | required |
| Dynamic loop | Native Python, max calls=3 | required after offline Tool/Gate tests |
| Formal comparison and H4 | One run per method/question; one terminal decision | required after Owner provider authorization |

## 2. Semantic input contracts

### IN-P1-001 v1 — QuestionRunRequest

- Producer/authority: frozen evaluation manifest; local Owner approves revision.
- Purpose/channel: start one local B1 or B2 CLI/library run.
- Required fields: `run_id`, `eval_revision`, `method` (`B1|B2`), `video_id`, `question_id`,
  non-empty `question`, `segment_source_sha256`, `question_set_sha256`, `gold_set_sha256`.
- Conditional fields: provider contract snapshot for answer runs; Gold path is scorer-only and must
  not enter retrieval/model context.
- Locale/encoding: UTF-8; Chinese question, limited Chinese/English technical terms; milliseconds.
- Limits: exactly one video and one question; normalized question length 1..500 Unicode codepoints;
  B2 Top-K=5 and max calls=3 are invariant, not caller fields.
- Validation: manifest hashes exist and match; IDs belong to same frozen revision; no cross-video
  segment source; method recognized; provider authorization matched before provider use.
- Duplicate/order/cancel: same `run_id` cannot be committed twice; formal run order is manifest
  order; cancellation makes the run terminal and rejects late output.
- Sensitivity: public/authorized technical content only; secrets never in input or Trace.
- Invalid outcome: `INVALID_RUN_REQUEST` or specific hash/scope error, no provider/Tool call.

Examples: valid `{"run_id":"p1-r1-b2-q01","method":"B2","video_id":"rlinf-2026","question_id":"p1-c01","question":"仿真与真机分别有哪些关键约束？"}`;
boundary is 500 codepoints; invalid is empty question or a second `video_id`.

### IN-P1-002 v1 — HeadroomCandidateSet

- Producer: Engineer drafts from recorded P0 failure taxonomy; Owner approves Gold before B2 work.
- Shape: 1..4 unique candidates; each has `question_id`, one `video_id`, Chinese `question`,
  `failure_taxonomy_ref`, `answerable=true`, Gold evidence units and immutable source hashes.
- Authority: candidate question is input; Gold is scoring authority; transcript is not a query-authoring
  source. No candidate may duplicate the existing 12 questions.
- Validation: every Gold segment exists in the same video snapshot; each failure taxonomy ref points
  to frozen P0 evidence; freeze timestamp precedes any B2 prompt/tool implementation commit.
- Correction: before freeze, Owner may edit/reject; after freeze, any change creates a new revision.
- Invalid outcome: `CANDIDATE_FREEZE_INVALID`; none of the set enters B1.

### IN-P1-003 v1 — OwnerProviderAuthorization

- Producer/authority: local Owner via an explicit later message or signed local approval artifact.
- Required: exact `eval_revision`, manifest hash, methods, question count, one-run policy, allowed
  provider configuration names, call/token ceilings, expiry; never secret values.
- Scope: authorizes only formal provider calls for that revision, not code changes or re-runs.
- Duplicate/revocation: latest valid non-expired record wins before first call; revocation stops new
  calls and marks unfinished runs cancelled. Authorization cannot be broadened by runtime.
- Invalid/missing outcome: `WAITING_OWNER_PROVIDER_AUTHORIZATION` without external call.

## 3. Semantic output contracts

### OUT-P1-001 v1 — AnswerResult

Reuses P0 `AnswerResult`: `status`, nullable `answer`, `evidence[]` with authoritative
`segment_id/start_ms/end_ms/quote`. Consumer is Owner/scorer. `ANSWERED` requires non-empty answer
and evidence; `INSUFFICIENT_EVIDENCE` requires null answer and empty evidence. Complete output has
Gate status and run linkage; degraded output is only the explicit refusal. Malformed, cancelled or
failed runs do not fabricate an `AnswerResult`. Owner may inspect/export but may not edit a frozen
formal output. Retention is local revision lifetime; no external side effect.

### OUT-P1-002 v1 — RunTrace

Append-oriented JSONL/file artifact for one run: contract versions, run/question/video IDs,
validated actions, tool status, observation segment IDs, newly seen IDs/Gold delta for scorer,
budget before/after, model/provider metadata without secrets, token/latency, final proposal, Gate
decision, errors and terminal state. It must not contain hidden chain-of-thought. Partial Trace is
valid only when labeled cancelled/failed and must never look complete.

### OUT-P1-003 v1 — HeadroomReport

Contains frozen candidate inventory, B1 results for all candidates, primary metric per candidate,
answerability, dynamic-recovery-path review, count and Gate result. Empty/no-headroom is a complete
valid report with terminal `NO_GO_INSUFFICIENT_HEADROOM`; missing cases/hashes is failure.

### OUT-P1-004 v1 — TerminalDecisionReport

Contains revision/manifest hashes, B0 status, B1/B2 population, metric table, H4 Gate rows,
action-sequence distribution, cost, failures, Owner review link and exactly one applicable terminal:
`KEEP_AGENT_EXPERIMENTAL`, `CONVERT_TO_WORKFLOW`, `DELETE_AGENT`,
`REPAIR_RETRIEVAL_FIRST`, `NO_GO_INSUFFICIENT_HEADROOM`, or pre-H4
`EVALUATION_BLOCKED_PROVIDER_FAILURE`. The report is advisory project evidence; it creates no
external action. It is immutable once accepted.

## 4. Task catalog and contracts

| Task | Trigger / preconditions | Output / completion | Errors, retry, review, evidence |
| --- | --- | --- | --- |
| TASK-P1-000 Baseline freeze | implementation authorization; clean identification of HEAD and P0 R3 | `ART-P1-001 BaselineManifest`; hashes/tests recorded | mismatch blocks; no provider; Owner inspects |
| TASK-P1-010 Candidate freeze | TASK-P1-000 pass | `IN-P1-002` and `ART-P1-002 CandidateManifest`; 1..4 candidates frozen | invalid Gold/source blocks; new revision for edits; Owner approves |
| TASK-P1-020 B1 Headroom | candidate manifest frozen | `OUT-P1-003`; existing hard case和所有 candidates 只跑 B1 retrieval；`AllNecessaryEvidence@5=false` 为 primary failure | zero provider；失败全保留；scorer-only oracle 仅验证允许动作能新增缺失 Gold；Owner reviews path |
| TASK-P1-030 Tool layer | Headroom `>=2` | two Tool contracts implemented and offline tests pass | scope/arg/source errors non-retryable per call; no model required |
| TASK-P1-040 Trace + Gate | TASK-P1-030 | run-local provenance, artifact schema and replay fixtures pass | malformed/cross-video/budget fail closed; no provider |
| TASK-P1-050 Bounded loop | TASK-P1-040 | action schema, deterministic first search, max 3 calls, terminal behavior pass fixtures | invalid model action refuses; no automatic repair loop |
| TASK-P1-060 Formal freeze | offline suite green | `ART-P1-003 FormalManifest` hashes dataset/source/prompt/model/tool/policy | hash drift blocks; Owner inspection |
| TASK-P1-070 Provider approval | TASK-P1-060 | valid `IN-P1-003` bound to manifest | missing/revoked/expired pauses; never infer permission |
| TASK-P1-080 Formal B1/B2 run | approval valid | every method/question has one immutable result/Trace | no selective retry; failure revision preserved |
| TASK-P1-090 Score/review/decide | complete valid formal artifacts, or Headroom No-Go | `OUT-P1-004` with one terminal | semantic review by Owner; deterministic Gate rows machine-derived |

All tasks are idempotent only before official commit: rerunning validation may reproduce identical
checks, but a formal run ID cannot be overwritten. There are no external mutations, compensation
or undo; correction after freeze always creates a new revision.

## 5. Canonical state authority

The append-oriented revision manifest plus task state records are authoritative. Model messages,
CLI display and provider responses are observations, never state authorities.

| State ID | Canonical name |
| --- | --- |
| STATE-P1-001 | `DESIGN_VALIDATED` |
| STATE-P1-002 | `BASELINE_FROZEN` |
| STATE-P1-003 | `CANDIDATES_FROZEN` |
| STATE-P1-004 | `B1_HEADROOM_RUNNING` |
| STATE-P1-005 | `HEADROOM_PASSED` |
| STATE-P1-006 | `NO_GO_INSUFFICIENT_HEADROOM` |
| STATE-P1-007 | `OFFLINE_IMPLEMENTING` |
| STATE-P1-008 | `OFFLINE_VERIFIED` |
| STATE-P1-009 | `FORMAL_MANIFEST_FROZEN` |
| STATE-P1-010 | `WAITING_OWNER_PROVIDER_AUTHORIZATION` |
| STATE-P1-011 | `FORMAL_EVAL_RUNNING` |
| STATE-P1-012 | `EVALUATION_BLOCKED_PROVIDER_FAILURE` |
| STATE-P1-013 | `REVIEW_PENDING` |
| STATE-P1-014 | `CANCELLED` |
| STATE-P1-015 | `KEEP_AGENT_EXPERIMENTAL` |
| STATE-P1-016 | `CONVERT_TO_WORKFLOW` |
| STATE-P1-017 | `DELETE_AGENT` |
| STATE-P1-018 | `REPAIR_RETRIEVAL_FIRST` |

```text
DESIGN_VALIDATED
  -> BASELINE_FROZEN
  -> CANDIDATES_FROZEN
  -> B1_HEADROOM_RUNNING
      -> NO_GO_INSUFFICIENT_HEADROOM [terminal]
      -> HEADROOM_PASSED
  -> OFFLINE_IMPLEMENTING
  -> OFFLINE_VERIFIED
  -> FORMAL_MANIFEST_FROZEN
  -> WAITING_OWNER_PROVIDER_AUTHORIZATION
  -> FORMAL_EVAL_RUNNING
      -> EVALUATION_BLOCKED_PROVIDER_FAILURE [terminal revision]
      -> REVIEW_PENDING
  -> one H4 terminal [terminal]
```

Entry/exit guards are the Task completions above. No state has an automatic timeout retry. Owner
cancellation moves any nonterminal pre-provider state to `CANCELLED`; during provider execution it
also rejects late results. `PARTIAL` only describes preserved failed artifacts and cannot advance.

## 6. Business rules and errors

1. First B2 action is deterministic `search_video(original question)`.
2. The runtime counts attempted validated Tool calls; max is 3. A rejected malformed model action
   consumes no Tool call but ends fail-closed, preventing retry gaming.
3. Eligible evidence is the union of successful current-run observations; no Gold/history/full
   transcript enters model context.
4. Tool output is untrusted data for the model and cannot override system policy.
5. Gate may preserve or downgrade proposal status, never upgrade it.
6. Failed formal revisions are immutable; recovery uses a new revision and authorization.

Stable errors and destinations:

| Error | Destination / visible behavior |
| --- | --- |
| `INVALID_RUN_REQUEST`, `HASH_MISMATCH`, `CANDIDATE_FREEZE_INVALID` | remain pre-run; diagnostic artifact |
| `INVALID_QUERY`, `DUPLICATE_QUERY`, `INVALID_RADIUS`, `UNKNOWN_SEGMENT_ID`, `ANCHOR_NOT_OBSERVED` | Trace error + `INSUFFICIENT_EVIDENCE` |
| `VIDEO_SCOPE_VIOLATION`, `INVALID_CITATION_PROVENANCE` | safety event + fail-closed refusal |
| `RETRIEVAL_UNAVAILABLE`, `SEGMENT_SOURCE_UNAVAILABLE` | failed/partial Trace; no model continuation |
| `TOOL_BUDGET_EXHAUSTED`, `INVALID_AGENT_ACTION` | fail-closed refusal |
| `PROVIDER_AUTHORIZATION_REQUIRED` | `WAITING_OWNER_PROVIDER_AUTHORIZATION` |
| `PROVIDER_TIMEOUT`, `PROVIDER_MALFORMED_OUTPUT` | preserved `EVALUATION_BLOCKED_PROVIDER_FAILURE` revision |
| `CANCELLED`, `LATE_RESULT_REJECTED` | terminal cancellation/failed Trace; output not scored as answer |

Roles: Owner alone approves Gold/provider/semantic review; Engineer may implement and run offline
checks; Runtime may only read frozen local assets and write new revision artifacts.
