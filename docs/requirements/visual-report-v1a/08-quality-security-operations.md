# Video Visual Report V1-A — Quality, Security, and Operations

## Grade boundary and service model

V1-A is a one-owner `G1 PROTOTYPE`. It supports one local three-video product
prototype and Owner review only. It does not promise production availability, customer
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
| Model calls | 2 base calls on success; at most 3 when one eligible technical retry is spent; 0 on pre-call failure | attempt-level `model-calls.jsonl` |
| Completed provider-conformance canary | At most 2 strategies × 3 videos × 2 calls = 12 calls | Frozen strategy registry + canary manifest |
| Cancelled boundary isolation | Never executed; `0` requests | Cancelled task/status evidence |
| Current semantic-v2 product Goal | 3 videos × 2 base calls + at most one retry per run = `6` base / `9` maximum | Frozen product-set manifest + attempt ledger + three reports/screenshots |
| Historical Development measurement | 3 videos × 2 runs = 6 runs, 12 planned calls | Retained historical aggregate only |
| Output size | 3–5 sections, 8–14 blocks, ≤2,600 visible authored characters | Compiler validation |
| Stored data | Small JSON/JSONL/HTML per run | Local owner-controlled root |

No growth, burst, queue, or multi-user scale claim is made.

The completed provider-conformance continuation had a ceiling of 24 new
transcript-bearing calls: 12 across two possible complete canary sets and 12 in
the one formal revision after the first passing strategy. It closed at
`V1A_PROVIDER_CONFORMANCE_NO_GO` after retained `8/8` calls, so that authority
cannot be reused. The later official-OpenAI boundary-isolation proposal was
cancelled before execution. The current Owner-confirmed DeepSeek semantic-v2
product Goal is capped at nine calls; execution has not started in this
documentation session.

## Responsiveness, timeout, and cost

- Per provider call timeout: 120 seconds by default and explicitly recorded.
- Ordinary two-stage run target: at most 180 seconds for the fixed workload;
  two bounded calls have a 240-second hard provider envelope, while a run that
  spends its one technical retry has a 360-second hard provider envelope.
- Local validation/compilation/rendering should complete in under five seconds
  excluding provider time; above ten seconds triggers diagnosis.
- SDK retry remains disabled. The application may make one identical,
  attempt-recorded technical retry per run for the enumerated API/JSON failures.
- Cost is bounded by two base calls/three maximum per run and the input/output envelopes. Token usage is
  recorded when supplied. Monetary cost remains `unavailable` unless an
  authoritative price snapshot and usage permit deterministic calculation.

These latency bounds are implementation-delegated G1 diagnostic targets; they
are not service SLOs or part of the Owner-confirmed semantic quality threshold.

## Quality indicators and Owner-confirmed release rules

| ID | Indicator/workload | Target | Measurement | Owner | Miss consequence |
|---|---|---|---|---|---|
| `SLO-VR1A-001` | Pre-call validation on all invalid fixtures | `provider_calls/model_calls=0/0` | Fake-adapter tests | Implementer | Block implementation completion |
| `SLO-VR1A-002` | Successful fixed run | `2` base calls or `3` with one eligible, identical, recorded retry; never more | Attempt trace | Implementer | Product set invalid |
| `SLO-VR1A-003` | Historical v1 Topic Map segment accounting | 100% input segments mapped or explicitly excluded | Deterministic validator | Implementer | Historical v1 run fails |
| `SLO-VR1A-004` | Must-cover topic recall on each product report | ≥90% and no must-cover topic absent | Human review card | Owner | Owner quality concern/rejection |
| `SLO-VR1A-005` | Block source-reference validity | 100% valid IDs/times | Compiler/test | Implementer | Run fails |
| `SLO-VR1A-006` | Major unsupported claim/metric | 0 across all three product reports | Human entailment + metric gate | Owner | Owner quality concern/rejection |
| `SLO-VR1A-007` | Editorial prioritization/narrative/block appropriateness | Target ≥4/5 per video | Human rubric | Owner | Owner quality concern/rejection |
| `SLO-VR1A-008` | Historical v1 first-pass schema/render success | 6/6 measured runs | Run states | Owner | Historical v1 stability claim fails |
| `SLO-VR1A-009` | Anti-template check | Three normalized structures are not all identical | Evaluation harness + review | Owner | Generic-output review/failure |
| `SLO-VR1A-010` | V0 compatibility | Current renderer/tests remain green | Regression suite | Implementer | Block completion |
| `SLO-VR1A-011` | Current v2 product output | 3/3 canonical HTML reports plus six viewport screenshots; a successful technical retry remains eligible | Run/call/render/visual manifests | Owner | Classify a missing report as technical-inconclusive or content-insufficient from its retained first-failing layer |
| `SLO-VR1A-012` | Compiler authority | 0 semantic rewrite/merge/split/synthesis; all whole-unit omissions visible | Rule ledger + raw/final deltas | Owner | Contract-change stop or quality concern |
| `SLO-VR1A-013` | Visual usability | Each report reviewed at 1080 px and approximately 390 px; no critical clipping, overlap, unreadable source text, or horizontal overflow | Browser screenshots + visual rubric | Owner | Owner quality concern/rejection |

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
- This authorization is purpose-bound to V1-A product-prototype work. It does not
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
| Model emits executable/layout content | Semantic-v2 allowlist discards and records unknown structural fields; final canonical schemas reject executable/layout values | Contract and governance-ledger tests |
| Invented source/timestamp | Model selects IDs only; binder uses canonical source | Unknown-ID/time tests |
| Unsupported numeric polish | Metric value must appear in cited transcript; human review for meaning | Metric tests/rubric |
| Credential leakage | Environment-only secrets; redacted trace/error | Boolean config tests |
| Hidden retry/fallback | SDK retry disabled; application retry limited to one identical technical attempt per run; exact attempt trace | Failure/retry tests |
| Evidence cherry-picking | Three predeclared product runs and every attempt remain; no video-specific replacement | Product-set manifest audit |
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
| Prototype review package | Three reports, screenshots, diagnostics and pending human rubrics | Missing report or quality concern | Owner accepts, rejects, or requests a new revision |

No remote telemetry, dashboard, alert, trace backend, or on-call operation is
added. CLI/run artifacts are sufficient for G1.

## Accessibility and compatibility

The existing renderer continues to own semantic HTML, local fonts, desktop/
mobile behavior, and escaping. V1-A inspects every generated report in a real
browser at the 1080 px desktop design viewport and approximately 390 px mobile
viewport, retaining screenshots and any clipping/overflow/hierarchy findings.

## Release, rollback, maintenance, and support

- Release/go-live: not applicable; result is a local three-report product review.
- Rollback: revert V1-A-specific code/docs/prompts and preserve V0 `render`.
- Prompt/model/semantic-contract/compiler changes make the three-video product
  set stale; another complete set requires new Owner authority, while old
  attempts/results remain.
- Inside `VR-V1A-PROVIDER-CONFORMANCE-004`, the experiment freezes before the
  first transcript call: a post-freeze change cannot trigger a same-strategy
  rerun or second formal revision under that task.
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
