# P1 Quality, Security and Operations

## 1. Grade and operating model

`GRADE-P1-001` is a single-owner local prototype. There is no tenant, service tier, trial,
entitlement, metering, billing/refund, contractual SLA, regulated region, status page, maintenance
window or external support. Local Owner is product/data/AI-quality/security/reliability/operations
acceptance owner. Use beyond public/authorized technical videos and portfolio evaluation is blocked
until G2 design and sign-off.

Grade-independent floors remain: secrets are never logged; inputs are validated; tools are
read-only/current-video; provenance and budgets are deterministic; formal history is immutable;
provider use is explicit and bounded.

## 2. Workload and measurable service objectives

Declared formal workload is `N=13..16` questions (12 regression plus 1..4 candidates), two methods,
sequential execution, one active run/provider request, B1 one search, B2 at most 3 Tool calls.

Non-functional contracts: `NFR-P1-001` immutable evidence, `NFR-P1-002` fail-closed provenance,
`NFR-P1-003` bounded cost/runtime, and `NFR-P1-004` P0 backward compatibility. The SLO rows below
are their measurable acceptance.

| ID | Indicator / workload | Target and measurement | Source/rationale | Owner / consequence |
| --- | --- | --- | --- | --- |
| SLO-P1-001 | Offline contract correctness across full fixture suite | 100% pass before formal freeze | fail-closed G1 floor | Engineering Owner; no formal manifest |
| SLO-P1-002 | Evidence safety across all formal answers | 0 invalid/fabricated/cross-video citations/timestamps | H4 confirmed | AI-quality Owner; `DELETE_AGENT` |
| SLO-P1-003 | Runtime bounds across all B2 runs | max Tool calls 3; mean <=2.0; 0 uncaught errors | Owner checkpoint/H4 | Engineering Owner; Agent not retained |
| SLO-P1-004 | Cost on same-revision population | mean B2 total tokens <=3× B1; report calls/tokens/latency | H4 confirmed; prices may drift | Product Owner; Agent not retained |
| SLO-P1-005 | Provider wait per decision and run | manifest timeout <=60 s/call; bounded run <=180 s, excluding review | 3-decision G1 loop; delegated internal bound | Engineering Owner; abort/preserve revision |
| SLO-P1-006 | Artifact durability | 0 overwrite of accepted revision; 100% official files hash-listed | frozen-evidence policy | Data Owner; stop/reconstruct new revision |
| SLO-P1-007 | Headroom decision | 100% candidate B1 results retained; >=2 qualifying failures to proceed | Owner checkpoint | Product Owner; No-Go below threshold |

Availability percentage, production RPO/RTO and error budget are not applicable to a manually
started local G1 CLI. Equivalent operating rule: any mandatory offline, hash, provenance, budget or
formal-artifact failure spends the entire revision budget and blocks advancement. Recovery is a new
revision; accepted data loss is zero for committed manifests/results. The local device is an
explicit accepted single point of failure for G1.

Spike test: reject a second concurrent formal process/reused run ID. Soak test: run full offline
population/fixtures without provider and show stable memory/artifact counts. Scaling trigger is any
request for concurrency, background execution, >16-question formal batch or shared users; that
requires new design, not an implicit queue.

## 3. Security, privacy and threat model

- Identity is the local OS/process owner; no application authentication/tenant boundary.
- Authorized data is public/non-sensitive technical-video evidence only. Sensitive/regulated,
  personal customer or confidential inputs are prohibited and rejected by declared-use policy.
- `OPENAI_API_KEY` is provisioned locally; only boolean presence is logged. No secret enters
  manifest, prompt, Trace or report.
- Transcript/question/provider content is untrusted; JSON schemas, max lengths, current-video IDs,
  path resolution and output encoding are validated at the trusted boundary.
- Prompt injection in transcript cannot change Tool catalog, policy, budget, video or Gold access.
- No mutating/high-impact action exists; approval/undo/compensation and break-glass support access
  are therefore not applicable.
- Consent/withdrawal and protected-record handling are not applicable under prohibited-sensitive-
  data/single-owner scope. G2 must introduce purpose-bound consent and deletion propagation if real
  user data appears.

Primary threats are Gold leakage, path/video scope traversal, prompt injection, fabricated
provenance, secret leakage, duplicate/selective rerun and manifest drift. Controls are source-path
allowlists, stable IDs, hashes, schema validation, run-local eligibility, redaction, idempotent IDs
and immutable evidence.

## 4. Observability and events

Every run must correlate `revision_id/run_id/question_id/video_id/method`. Canonical events:
`run_started`, `tool_requested`, `tool_validated`, `tool_succeeded`, `tool_failed`,
`model_requested`, `model_failed`, `proposal_received`, `evidence_gate_decided`, `run_cancelled`,
`late_result_rejected`, `run_terminal`. Logs/Trace record latency, call count, tokens, observation
IDs, evidence delta, error/terminal reason and contract versions, with no secret/hidden reasoning.

Local reports act as dashboard. Alerting is manual: any nonzero safety/runtime Gate, hash mismatch,
missing artifact or authorization mismatch stops the command with nonzero exit and an Owner-readable
diagnostic. Owner response is to quarantine the revision, inspect Trace and either accept its
failure or authorize a new revision; there is no silent retry.

## 5. Runbooks and lifecycle

`OPS-P1-001` is the local formal-run operating policy: preflight, one-shot execution, quarantine on
failure, no selective retry, new-revision recovery, and Owner-owned evidence export.

- Preflight: verify checkout/lock/data hashes, clean revision target, offline suite, boolean
  credential presence and exact authorization.
- Dependency outage: stop, persist failure, mark revision blocked; never switch provider/model.
- Artifact corruption: compare manifest hashes, quarantine, regenerate only in a new revision.
- Security/provenance violation: stop entire formal revision; choose `DELETE_AGENT` after review if
  violation is attributable to B2.
- Rollback: disable/remove experimental Agent path in later authorized change; keep all evidence.
- Export/offboarding: copy complete evidence pack with manifest; project Owner controls local
  cleanup. Accepted frozen evidence is not deleted as routine recovery.

Support channel/hours/response/restoration are not applicable because there are no external users
or commitments. Local Owner performs best-effort maintenance with no promised response time.
Release communication, compatibility and deprecation are repository documentation only; breaking
contract changes require a new revision and explicit checkpoint.

## 6. G2 promotion

Trigger: named non-owner user, non-public/real user data, shared environment, repeated reliance,
background/concurrent workload or any external action. Required evidence: access/consent tests,
audited durable task state, recovery/rollback, bounded pilot load and latency, dependency
degradation, support severity/owner, incident drill, export/deletion, compatibility and pilot exit
criteria. Until all pass, current CLI must continue to enforce the G1 boundary.
