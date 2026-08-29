# P1 Engineering Context

## 1. Repository baseline

- Target repository/output: `/Users/tristana/Develop/video-evidence-agent`
- Baseline at requirements audit: branch `main`, `HEAD=fc9b29c`
- P0 R3 frozen source baseline recorded by its manifest: `7cedce5`; do not conflate with closeout HEAD
- Runtime/toolchain: Python `>=3.12,<3.13`, uv project `.venv`, `pyproject.toml`, committed `uv.lock`
- Production surface for this G1 project: local `video-evidence` CLI and project Python modules;
  no deployed service exists
- Existing provider boundary: `src/video_evidence_agent/answering.py`, OpenAI-compatible text only
- Canonical P0 contracts: `schemas.py`, `segments.py`, `retrieval.py`, `evidence.py`,
  `p0b_eval.py`; P0-B R2/R3 retrieval profile is the B1 source

Current tests at design audit: `uv run pytest` passed 28 tests; `uv run ruff check .` and
`git diff --check` passed. These are checkout-time facts and TASK-P1-000 must refresh them.

## 2. Existing capability fit

| Capability | State / evidence | Gap / change layer | Owner / acceptance |
| --- | --- | --- | --- |
| VideoSegment/current-video source | SUPPORTED: `schemas.py`, P0 ingest, 127 segments | none; protected contract | Data Owner; P0 tests |
| B1 Top-5 retrieval | SUPPORTED: `retrieve_transcript_r2`, R3 report | wrap as read-only IF-P1-001; project adapter | Engineer; TEST-P1-003 |
| Neighbor lookup | PARTIAL: stable ID/ordinal exists | bounded IF-P1-002 missing; project behavior | Engineer; TEST-P1-004/005 |
| Answer-level schema/Gate | SUPPORTED: `AnswerProposal`, `AnswerResult`, Evidence Gate | add run-local eligible set without claim schema | Engineer; TEST-P1-008/009 |
| Immutable eval/report | PARTIAL: P0 manifests/results exist | P1 Trace/action/terminal fields missing | Engineer/Data Owner; TEST-P1-010/011 |
| Headroom workflow | MISSING | P1-only candidate freeze/B1 Gate | Owner; TEST-P1-001/002/017 |
| Bounded Agent loop | MISSING | project-owned Native Python | Engineer; TEST-P1-007/016/018 |
| H4 evaluator | MISSING | P1-only deterministic mapping + review | Owner; TEST-P1-014 |
| B0 Direct Multimodal | unavailable by confirmed scope | not a gap; prohibited in P1 | Product Owner; TEST-P1-013 |

No competing runtime or shared framework authority exists. A narrative README may lag a frozen
report; raw manifest/artifact and canonical P1 package win for evaluation state.

## 3. Grade/framework disposition

Selected grade: `G1 PROTOTYPE`; allowed/prohibited use and G2 compatibility are in `00-handoff.md`.
Downstream-framework status: `NOT_APPLICABLE`. Product strategy: `FRAMEWORKLESS`.

The requirements process describes Hypha with the project-team positioning “super-useful Agent
Native framework, jointly developed by CodeSoul × University of Electronic Science and Technology
of China, intended for demo/system/commercial delivery.” That positioning is not repository
evidence and is not used as a quality claim here. Owner explicitly chose `REJECTED_FOR_P1`: a
single bounded read-only loop has no need for its runtime/memory/MCP/multi-agent capabilities.
No Hypha version/package/source dependency or fallback is allowed in P1.

## 4. Module adoption matrix

| Module | Route / dependency | Reason and customization boundary | Canonical owner / compatibility / tests | Upgrade, rollback, fallback |
| --- | --- | --- | --- | --- |
| Domain/workflow | PROJECT_OWNED; repo source at implementation commit | P1 state/tasks only; preserve P0 | Engineer; STATE/TASK v1; TEST-P1-001/014 | Owner checkpoint; remove B2; No-Go |
| Runtime/FSM | PROJECT_OWNED; Python 3.12 + uv.lock | small explicit state machine; no graph | Engineer; state vocabulary; TEST-P1-007/016 | new revision; deterministic workflow fallback |
| Events/replay | PROJECT_OWNED; JSON/JSONL | Trace/events only, no broker | Data Owner; OUT-P1-002; TEST-P1-010/021/022 | additive version; retain old reader/files |
| Tools/MCP | PROJECT_OWNED; existing retrieval/segment modules | in-process IF-P1-001/002; no MCP server | Engineer; JSON schema v1; TEST-P1-003..006 | breaking change needs checkpoint; fail closed |
| Memory/context | PROJECT_OWNED run state; no durable dependency | run-local only; no cross-run memory | Engineer; DATA-P1-002/004; TEST-P1-010 | discard at end; refusal fallback |
| Execution/workspace | PROJECT_OWNED; local filesystem/uv | atomic new-revision artifacts; no queue | Engineer; manifests; TEST-P1-011/020 | new revision; manual recovery |
| Prompt/inference/models | PROJECT_OWNED adapter; existing `openai>=3.3.1`, exact uv.lock | text structured decisions only; model identifier frozen later | AI Owner; IF-P1-003; TEST-P1-015/023 | no silent switch; block revision |
| Storage/artifacts | PROJECT_OWNED; local files | manifests/RunBundles only; no DB/object store | Data Owner; ART v1; TEST-P1-011 | preserve history; export pack |
| Caches | NOT_APPLICABLE beyond replaceable process-local compute | no Redis/shared cache | Engineer; deterministic results | recompute; no fallback dependency |
| Policy/identity/approval | PROJECT_OWNED deterministic gates; local OS owner | manifest/provider approval only; no tenancy | Owner; IN-P1-003; TEST-P1-009/015 | revoke stops; G2 redesign |
| Evaluation/testing | PROJECT_OWNED; pytest/Ruff/existing scorer | B1/B2/H4 and semantic review | AI/Data Owner; TEST-P1-001..024 | new frozen revision; B1 fallback |
| Product surface | PROJECT_OWNED existing CLI/library | local only; no Web/API | Engineer; exit contracts; contract tests | disable experimental command |
| Operations | PROJECT_OWNED local runbooks | no service/on-call/deploy | local Owner; SLO-P1-001..007 | stop/quarantine/new revision |

Package/source availability fallback is uniformly fail-closed: exact uv.lock/project source must be
available; no alternate Agent framework/package is selected automatically.

## 5. Implementation authority matrix

| Decision | Class | Owner | Allowed envelope | Prohibited | Acceptance |
| --- | --- | --- | --- | --- | --- |
| Grade/scope/B0 | fixed constraint | Owner | exact G1/B1-vs-B2 boundary | production, B0 restore/claim | TEST-P1-013 |
| Headroom/H4 thresholds | fixed constraint | Owner | exact counts/ratios and terminal priority | tuning after B2 | TEST-P1-001/014 |
| Tool surface/budget/framework | fixed constraint | Owner | two read-only Tools, Top-5, max3, Native Python | extra Tool, LangGraph/Hypha/VLM | TEST-P1-003..007 |
| Provenance/history | required invariant | Data/Engineering Owner | current-run/video eligibility, immutable revision | fabricated/cross-video/overwrite | TEST-P1-009/011 |
| Internal module/function layout | implementation-delegated | Engineer | simplest project-owned code, existing style/uv | new framework/server/DB | full tests + review |
| CLI subcommand names | implementation-delegated | Engineer | stable documented equivalents for Tasks | changing P0 command semantics | contract/regression tests |
| Provider model/config value | implementation-delegated at freeze | Owner | same B1/B2, text only, manifest-bound | VLM/silent fallback | TEST-P1-012/015/023 |
| Provider execution | prohibited until exact approval | Owner | calls only after TASK-P1-070 | current requirements phase or selective rerun | TEST-P1-015 |
| Claim schema/retrieval upgrade/G2 | prohibited in P1 | Owner | new phase/checkpoint only | hidden scope expansion | source/diff inspection |

There is no `blocking unknown`. Runtime provider approval is a designed checkpoint with a safe
waiting state, exact input contract and zero-call default.

## 6. Asset/change boundary

Later implementation may create new P1 source modules/tests/fixtures/CLI surface and new versioned
P1 eval/report/artifact paths after authorization. It may minimally reuse/extend public P0 helpers
without changing their existing behavior. It must not change or delete P0 questions, Gold,
segments, media, manifests, R1/R2/R3 artifacts/reports, historical labels, `uv.lock` without an
approved dependency need, or unrelated user changes. New P1 data is created only by TASK-P1-010
under Owner Gold approval. No assets are moved, transcoded or uploaded.

## 7. Required commands and evidence

Existing:

```bash
uv run pytest
uv run ruff check .
git diff --check
```

Implementation must preserve these and add `uv run` documented commands/tests for JSONL/schema
validation, Headroom freeze/grade, offline success/failure replay, formal preflight, B1/B2 run,
H4 report and frozen-history diff. Provider-call tests use fakes unless TASK-P1-070 is satisfied.
Secret checks report only presence booleans.

## 8. Handoff trigger

This package contains documentation only. Application code, scaffolding, dependency changes,
migrations, infrastructure and deployment remain outside this phase. Separate implementation may
begin only after validator success and explicit Owner construction authorization; it must still
pause at Headroom No-Go and provider-authorization gates exactly as `10-delivery-plan.md` states.

