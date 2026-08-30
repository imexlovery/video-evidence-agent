# Video Visual Report V1-A — Quality, Security, and Operations

## Grade boundary and service model

V1-A is a one-owner `G1 PROTOTYPE`. It may support a local Development
measurement only. It does not promise production availability, customer
support, public output, contractual quality, or unattended background service.

Safety floors remain mandatory: explicit provider/model, authorized inputs,
source-linked output, deterministic validation, no model layout/tool authority,
credential secrecy, retained failures, and protected V0/P0-B artifacts.

## Workload envelope

| Dimension | Normal/peak G1 workload | Measurement |
|---|---|---|
| Concurrent users/runs | 1 / 1 | Foreground CLI only |
| Videos per run | 1 | One manifest + JSONL |
| Transcript | 38–46 segments for fixed set; hard max 80/50,000 chars | Pre-call validation |
| Model calls | 2 on success; 1 if Mapper succeeds and Planner fails; 0 on pre-call failure | `model-calls.jsonl` |
| Development measurement | 3 videos × 2 runs = 6 runs, 12 planned calls | Aggregate report |
| Output size | 3–5 sections, 8–14 blocks, ≤2,600 visible authored characters | Compiler validation |
| Stored data | Small JSON/JSONL/HTML per run | Local owner-controlled root |

No growth, burst, queue, or multi-user scale claim is made.

## Responsiveness, timeout, and cost

- Per provider call timeout: 120 seconds by default and explicitly recorded.
- Successful two-stage run target: at most 180 seconds for the fixed workload;
  the hard elapsed ceiling is 240 seconds from two bounded calls plus local work.
- Local validation/compilation/rendering should complete in under five seconds
  excluding provider time; above ten seconds triggers diagnosis.
- No automatic retry. A timeout/error fails the run.
- Cost is bounded by two calls and the input/output envelopes. Token usage is
  recorded when supplied. Monetary cost remains `unavailable` unless an
  authoritative price snapshot and usage permit deterministic calculation.

These latency bounds are implementation-delegated G1 diagnostic targets; they
are not service SLOs or part of the Owner-confirmed semantic quality threshold.

## Quality indicators and Owner-confirmed release rules

| ID | Indicator/workload | Target | Measurement | Owner | Miss consequence |
|---|---|---|---|---|---|
| `SLO-VR1A-001` | Pre-call validation on all invalid fixtures | `provider_calls/model_calls=0/0` | Fake-adapter tests | Implementer | Block implementation completion |
| `SLO-VR1A-002` | Successful fixed run | Exactly `2/2`; no hidden retry | Call trace | Implementer | Run fails |
| `SLO-VR1A-003` | Topic Map segment accounting | 100% input segments mapped or explicitly excluded | Deterministic validator | Implementer | Run fails |
| `SLO-VR1A-004` | Must-cover topic recall on each video/repeat | ≥90% and no must-cover topic absent | Human review card | Owner | Measurement fails |
| `SLO-VR1A-005` | Block source-reference validity | 100% valid IDs/times | Compiler/test | Implementer | Run fails |
| `SLO-VR1A-006` | Major unsupported claim/metric | 0 across all accepted runs | Human entailment + metric gate | Owner | Measurement fails |
| `SLO-VR1A-007` | Editorial prioritization/block appropriateness | ≥4/5 per video average; no category below 3 | Human rubric | Owner | Measurement fails |
| `SLO-VR1A-008` | First-pass schema/render success | 6/6 measured runs | Run states | Owner | Stability claim fails |
| `SLO-VR1A-009` | Anti-template check | Three normalized structures are not all identical | Evaluation harness + review | Owner | Generic-output review/failure |
| `SLO-VR1A-010` | V0 compatibility | Current renderer/tests remain green | Regression suite | Implementer | Block completion |

There is no availability percentage, production error budget, RPO, or RTO.
The equivalent G1 operating rule is: any retained failure counts; no conclusion
is accepted until all hard gates and Owner-owned quality thresholds pass.

## Capacity, dependencies, and accepted single points of failure

The local Mac, source files, configured provider/model, network connection, and
Owner review are accepted G1 single points of failure. Missing or degraded
dependencies stop the current run. No queue, cache, alternate provider, stale
result, model fallback, or reduced-quality plan is introduced.

## Privacy, rights, and consent

- The Owner explicitly authorized all three full transcripts for external model
  processing and stated there is no privacy concern.
- This authorization is purpose-bound to V1-A design/measurement. It does not
  authorize media/frame upload, publication, redistribution, customer use, or
  model training by this project.
- Current source manifests still require local/non-public handling of media and
  derived reports.
- Provider-side handling follows the configured provider; V1-A makes no data-
  residency, zero-retention, or regulated-data claim.
- Authorization withdrawal stops new processing and triggers Owner-directed
  deletion of related V1-A run artifacts.

## Authentication, authorization, secrets, and audit

Local filesystem access is the product authorization boundary. Provider
credentials come from environment variables; logs/artifacts record only
credential presence. There are no accounts, roles, tenants, support access, or
runtime admin surface. `events.jsonl`, `model-calls.jsonl`, run manifests, and
version-controlled task/status history provide prototype evidence, not a
production audit service.

## Threat model and controls

| Threat | Control | Verification |
|---|---|---|
| Transcript prompt injection | JSON data delimiter + explicit system policy + no tools | Adversarial transcript fixture |
| Model emits executable/layout content | Closed schemas reject extra/type/layout fields | Contract tests |
| Invented source/timestamp | Model selects IDs only; binder uses canonical source | Unknown-ID/time tests |
| Unsupported numeric polish | Metric value must appear in cited transcript; human review for meaning | Metric tests/rubric |
| Credential leakage | Environment-only secrets; redacted trace/error | Boolean config tests |
| Hidden retry/fallback | SDK/application retry disabled; exact call trace | Failure tests |
| Evidence cherry-picking | Unique append-only runs; all six runs in denominator | Measurement audit |
| V0/P0-B contamination | Read-only protected paths + regression/diff review | Git/test checks |
| Unauthorized publication | No publish/deploy/export surface | Scope/diff review |

There are no financial, destructive, privileged, or irreversible product
actions.

## Observability

| Signal | Content | Trigger | Owner action |
|---|---|---|---|
| Run state/events | State transitions, stage, error category, artifact path | Non-terminal/inconsistent transition | Diagnose; do not call success |
| Model call trace | Stage, provider/model, prompt rev, latency, usage, schema status | Missing/extra call, timeout, malformed output | Fail run |
| Validator summary | Segment/topic/ref/block counts and rule outcomes | Any hard rule fails | Preserve and stop |
| Renderer summary | Report/section/block/asset counts | Non-zero or unexpected asset use | Fail and repair implementation |
| Measurement report | Per-run and aggregate deterministic/human scores | Threshold miss | Owner rejects or authorizes new revision |

No remote telemetry, dashboard, alert, trace backend, or on-call operation is
added. CLI/run artifacts are sufficient for G1.

## Accessibility and compatibility

The existing renderer continues to own semantic HTML, local fonts, desktop/
mobile behavior, and escaping. V1-A specifically verifies that generated copy
passes current field budgets and renders without overflow-causing schema
violations. Broad browser certification is not repeated unless Planner content
reveals a concrete renderer defect.

## Release, rollback, maintenance, and support

- Release/go-live: not applicable; result is a local Development measurement.
- Rollback: revert V1-A-specific code/docs/prompts and preserve V0 `render`.
- Prompt/model/schema changes are versioned and require a complete new six-run
  measurement; old failures/results remain.
- Support/incident response: not applicable — local Owner and implementer
  collaborate directly, with visible failure and explicit rerun.
- Backup/restore: no service commitment; code/docs are version controlled and
  local runs are owner-managed.

## Commercial-operation applicability

Customer/tenant provisioning, invitations, entitlements, quotas, metering,
billing/refunds, trials, contractual SLAs, regulated-region operation, status
pages, support hours/severity, maintenance windows, deprecation notices, data
portability, and offboarding workflows are not applicable because V1-A is a
single-owner local feasibility prototype with no service or customer.
