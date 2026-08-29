# P1 Delivery Plan

本文件是非可执行施工计划。本 requirements 阶段不执行任何源码、依赖、runtime、数据、
基础设施、provider 或部署动作。后续施工必须获得单独授权，并在每个 Gate 停止条件处
按本合同执行。

## 1. Critical path

```text
TASK-P1-000 Baseline freeze
 -> TASK-P1-010 Candidate/Gold pre-freeze
 -> TASK-P1-020 Current B1 Headroom run
    -> NO_GO_INSUFFICIENT_HEADROOM [stop]
    -> HEADROOM_PASSED
       -> TASK-P1-030 Two read-only Tools
       -> TASK-P1-040 Trace + Evidence Gate
       -> TASK-P1-050 Native bounded loop
       -> TASK-P1-060 Formal manifest freeze
       -> TASK-P1-070 Owner provider authorization [pause]
       -> TASK-P1-080 One formal B1/B2 comparison
       -> TASK-P1-090 Score, review and terminal decision [stop]
```

No downstream step may start merely because code is convenient to write. `TASK-P1-020` is the
first Go/No-Go boundary and precedes Agent source construction.

## 2. Vertical slices and Definition of Done

| Slice / owner | Deliverables | Dependencies | Definition of Done / evidence | Stop rule |
| --- | --- | --- | --- | --- |
| TASK-P1-000 Baseline freeze / Engineer | ART-P1-001 with HEAD, uv.lock, P0 R3, 12 questions, 127 segments hashes; command baseline | implementation authorization | hashes resolve; P0 `pytest`/Ruff green; no frozen file changed | mismatch blocks |
| TASK-P1-010 Candidate freeze / Engineer + Owner | 1..4 candidate questions, Gold, taxonomy refs, ART-P1-002 | 000 | TEST-P1-017; Owner approval timestamp precedes B2 work | invalid/unapproved set blocks |
| TASK-P1-020 B1 Headroom / Engineer + Owner | current B1 retrieval artifacts for existing hard case and all candidates, OUT-P1-003 | 010 | zero provider; `AllNecessaryEvidence@5=false` + allowed-action Gold delta; TEST-P1-001/002; all attempts retained | qualifying count <2 => No-Go and skip 030..090 except closeout |
| TASK-P1-030 Tool layer / Engineer | IF-P1-001/002 behavior, offline unit/contract evidence | Headroom pass | TEST-P1-003..006; Top-K/calls/scope immutable; zero provider | failure blocks 040 |
| TASK-P1-040 Trace + Gate / Engineer | OUT-P1-002 schema, eligibility, Gate, success/failure replay | 030 | TEST-P1-008..011/019/021/022; zero provider | any provenance escape blocks 050 |
| TASK-P1-050 Bounded loop / Engineer | AGENT-P1-001 controller and fake-provider integration | 040 | TEST-P1-007/016/018/020; max calls 3; zero framework/VLM/provider | offline failure blocks freeze |
| TASK-P1-060 Formal freeze / Engineer + Owner | ART-P1-003 with source/data/Gold/prompt/model/tool/policy/budget hashes | all offline tests | TEST-P1-012/023/024; diff review clean | drift/change requires new manifest |
| TASK-P1-070 Provider approval / Owner | IN-P1-003 | 060 | TEST-P1-015; exact revision/hash/count/budget/expiry | absent/revoked => wait with zero calls |
| TASK-P1-080 Formal comparison / Engineer | immutable B1/B2 RunBundles for every manifest row | 070 | one attempt/method/question; artifact completeness and usage totals | failure preserves revision; no selective retry |
| TASK-P1-090 Review/decision / Owner | automatic metrics, semantic review, OUT-P1-004/ART-P1-005 | valid 080 or Headroom No-Go | TEST-P1-013/014; exactly one terminal and accurate claim | terminal reached; no adjacent phase |

## 3. Formal Go/No-Go gates

| Gate | Entry evidence | Pass | Fail destination |
| --- | --- | --- | --- |
| GATE-P1-0 Documentation | canonical package + evidence/coverage | independent validator report passes | return to documents only |
| GATE-P1-1 Baseline | P0/lock/source hashes and existing tests | all fixed assets/commands reproducible | stop for baseline repair; do not edit history |
| GATE-P1-2 Headroom | pre-frozen candidates + all current B1 results | >=2 answerable primary failures with auditable allowed-Tool recovery | `NO_GO_INSUFFICIENT_HEADROOM` |
| GATE-P1-3 Offline safety | Tool/Gate/loop/replay/regression tests | 100% mandatory tests pass; no provider/framework/VLM | stop for code repair before freeze |
| GATE-P1-4 Formal freeze | exact manifest and clean diff | every input/config/budget/version hashed | new manifest required |
| GATE-P1-5 Provider authority | IN-P1-003 | exact revision approval valid and ceilings sufficient | `WAITING_OWNER_PROVIDER_AUTHORIZATION` |
| GATE-P1-6 Formal validity | complete one-shot artifacts | all planned B1/B2 results complete with no infrastructure failure | `EVALUATION_BLOCKED_PROVIDER_FAILURE` revision |
| GATE-P1-H4 Retention | valid metrics + Owner semantic/Trace review | route by `09-test-acceptance.md` matrix | one non-generic terminal |

## 4. Parallelizable work

Before Headroom pass, only baseline hashing, candidate contract validation and non-source review may
proceed; no B2 implementation. After Headroom pass, Tool schema test fixtures and report schema/
offline scorer fixtures may be prepared in parallel, but Trace/Gate integration waits for working
Tools and bounded loop waits for Trace/Gate. Provider authorization cannot be requested against a
moving manifest.

## 5. Change, compatibility and rollback

- No database/API/schema migration exists. New P1 artifacts use new versioned paths; P0 remains
  readable and tests must stay green.
- Implementation may add an experimental CLI/library surface without changing existing P0 command
  semantics. Feature enablement is by explicit P1 command/manifest, default off for P0 paths.
- Any question/Gold/source/prompt/tool/model/Gate/rubric change after freeze creates a new revision.
- Rollback disables or removes B2 only in a later authorized change; evidence pack remains.
- No deployment. Formal run is local; no customer communication, billing, entitlements or
  offboarding tasks apply.

## 6. Completion commands and evidence

Existing mandatory commands:

```bash
uv run pytest
uv run ruff check .
git diff --check
```

Later implementation must add documented non-provider commands equivalent to contract validation,
offline replay and Headroom/report validation, runnable with `uv run`. Formal provider command must
require an explicit manifest and authorization artifact and support a dry preflight that proves
zero external calls. Exact internal module names are implementation-delegated; observable IN/OUT/
exit-code contracts are fixed.

## 7. Current release and G2 path

G1 DoD is one evidence-backed terminal, not necessarily retained Agent code. Deferred identity,
consent, durable recovery, concurrent workload, service operations, monitoring/alerting, support,
customer lifecycle and deployment each require a G2 requirements revision, migration/compatibility
plan and acceptance evidence listed in `08-quality-security-operations.md`. No G2 task is smuggled
into P1.

Excluded future work remains B0/VLM, claim-level schema, retrieval-model upgrades, multi-agent,
frameworks, server/UI, persistent/shared state, production and commercial operation.
