# P1 evidence ledger

## TASK-P1-000 takeover

- Session date: 2026-08-26.
- Current branch: `main`.
- Current HEAD at takeover: `fc9b29ce387f52d5da92be8fc68ce171727f872a`.
- Pre-existing untracked paths: `docs/requirements/p1/`, `docs/tasks/P1.md`; preserved.
- Project-to-Act: absent by the P1 contract; no parallel governance system was initialized.
- Requirements validator: `READY_FOR_ENGINEERING_HANDOFF`, confidence `100.0`.
- Provider calls: `0`; video upload: `false`; formal evaluation: not started.

The P1 canonical package, P1 design background, P0-B task ledgers, P0-B R3 manifest,
final report, retrieval report, and reused P0 source contracts were read before
construction. This file records only facts verified in this session; each subsequent
Gate appends a command, exit status, input/source hash, result summary, artifact path,
and timestamp. Frozen history is never rewritten.

## TASK-P1-000 baseline freeze — `EVID-P1-000-BASELINE-001`

- Gate: `GATE-P1-1 Baseline`.
- Status: `PASSED`.
- HEAD/source revision: `main` / `fc9b29ce387f52d5da92be8fc68ce171727f872a`.
- Commands: `uv run pytest` exit 0 (`28 passed`); `uv run ruff check .` exit 0;
  `git diff --check` exit 0; P1 JSON ledgers and required JSONL/JSON validation exit 0.
- P0 R3 verification: exit 0; manifest/input/source/media/ingest/report pins verified;
  R3 remains `P0B_PASSED_OWNER_ACCEPTED` and explicitly says P1 unstarted/unauthorized.
- Population: 3 videos, 12 questions, 12 Gold rows, 127 valid non-overlapping timestamped
  `VideoSegment` objects; all Gold segment/time mappings passed.
- Protected snapshot: 181 historical files hashed; snapshot SHA-256
  `d068dad5cce78baaa29c6ec42ad26ca966213ef691f575c13a2d2692b7f6f3e3`.
- P0 R3 files: 50 files hashed; P0 R3 manifest/report hashes cross-checked.
- Artifact: `eval/p1/revisions/p1-baseline-r1/baseline-manifest.json`;
  SHA-256 `d2171330a5a60261189f8e46fe20e5fbdb234aa4a3c7853a4eae0742602e6958`.
- Provider calls: `0`; video upload: `false`; Mock/formal provider evaluation: not used.

TASK-P1-000 is complete. The next state is the mandatory Owner checkpoint for
TASK-P1-010 candidate/Gold freeze.

## TASK-P1-010 candidate / Gold draft — `EVID-P1-010-DRAFT-001`

- Status: `PENDING_OWNER_CONFIRMATION`; this is not `ART-P1-002` and is not frozen.
- Validation command: `uv run python /private/tmp/p1_candidate_validate.py`, exit 0.
- Draft: `eval/p1/revisions/p1-candidate-draft-r1/candidate-draft.json`;
  SHA-256 `e7dc08dc78881e0c35262635460e297c8f0347facaebaca7f919b355e8346567`.
- Review material: `docs/tasks/p1/candidate-gold-review.md`.
- Candidates: `p1-c01-kling-creative-001`, `p1-c02-kling-signal-quality-001`,
  `p1-c03-rlinf-simulation-001`, `p1-c04-rlinf-real-system-001`.
- Validation result: 4 candidates within the `1..4` limit; new unique IDs; one video each;
  all `answerable=true`; source segment IDs and Gold intervals resolve against frozen P0
  snapshots; no transcript text embedded.
- Historical basis: P0 R1 failure taxonomy only; existing hard case
  `p0b-r1-rlinf-m` is retained separately and is not counted as a new candidate.
- Provider calls: `0`; B1 Headroom run: `false`; B2 prompt/tool design: `false`.
- Pause: Owner must accept/reject exact candidate IDs and confirm Gold mappings before
  `ART-P1-002` can be frozen or `TASK-P1-020` can start. Any correction requires a new
  draft revision; this draft remains preserved.

## TASK-P1-010 Owner review and candidate / Gold draft r2 — `EVID-P1-010-R2-DRAFT-001`

- Owner decision ledger: `DEC-P1-032`, appended to the canonical decision ledger.
- r1 preservation: `eval/p1/revisions/p1-candidate-draft-r1/candidate-draft.json` remains
  unchanged; its SHA-256 is `e7dc08dc78881e0c35262635460e297c8f0347facaebaca7f919b355e8346567`.
- r2 artifact: `eval/p1/revisions/p1-candidate-draft-r2/candidate-draft.json`;
  SHA-256 `fce132bde0ca044a5aa6186512607d874c71bbfe4a6480b7430c3a0d2c989456`.
- r2 review material: `docs/tasks/p1/candidate-gold-review-r2.md`.
- r2 evidence: `docs/tasks/p1/candidate-draft-r2-evidence.json`.
- Generation and source/mapping validation: `uv run python /private/tmp/p1_candidate_r2_generate.py`,
  exit 0. The validator confirmed 2 active candidates, frozen source snapshots, valid
  segment-matched Gold intervals, and no embedded transcript text.
- Active candidates pending final r2 confirmation: `p1-c02-kling-signal-quality-001` and
  `p1-c03-rlinf-simulation-001`.
- c02 Gold is split exactly into `u1 1237400..1282920 / p0b-kling-2024-seg-026` and
  `u2 1282920..1330200 / p0b-kling-2024-seg-027`.
- c01 is rejected as a duplicate of `p0b-r1-kling-p`; c04 is rejected as highly correlated
  with fixed hard case `p0b-r1-rlinf-m`. Neither is in the active r2 set or eligible for
  Headroom counting.
- `ART-P1-002`: not frozen. `TASK-P1-020`: not run. B2 design: not started.
- Provider calls: `0`; video upload: `false`.
- Current state remains `WAITING_CANDIDATE_GOLD_OWNER_FREEZE`; Owner must confirm the exact
  r2 active set and Gold mappings before the CandidateManifest freeze. No later Gate was run.

## TASK-P1-010 Owner-authorized CandidateManifest freeze — `EVID-P1-010-FREEZE-001`

- Final Owner authorization: `DEC-P1-033`.
- Authorized draft: `eval/p1/revisions/p1-candidate-draft-r2/candidate-draft.json`;
  SHA-256 `fce132bde0ca044a5aa6186512607d874c71bbfe4a6480b7430c3a0d2c989456`.
- Frozen artifact: `eval/p1/revisions/p1-candidate-freeze-r2/candidate-manifest.json`;
  SHA-256 `d523c22fdfbfb8d1ff55a2d5620d94bd6cdfac5368472995f1317b857f495cf2`.
- Freeze evidence: `docs/tasks/p1/candidate-freeze-evidence.json`.
- Active set: exactly `p1-c02-kling-signal-quality-001` and
  `p1-c03-rlinf-simulation-001`.
- `p1-c02` Gold units remain the two exact Owner-confirmed units:
  `u1 1237400..1282920 / p0b-kling-2024-seg-026` and
  `u2 1282920..1330200 / p0b-kling-2024-seg-027`.
- Existing fixed hard case: `p0b-r1-rlinf-m`; it is included once in the Headroom workload
  and is not double-counted with rejected `p1-c04`.
- Rejected history: `p1-c01-kling-creative-001` and `p1-c04-rlinf-real-system-001` remain
  outside the active set and outside all Headroom numerator/denominator/pass counts. Their
  r1 records are not modified or deleted.
- Freeze validation: `uv run python /private/tmp/p1_candidate_freeze_r2.py`, exit 0;
  readiness was revalidated as `READY_FOR_ENGINEERING_HANDOFF` after the append-only Owner
  authorization record.
- Provider calls: `0`; video upload: `false`; B2 design: `false`; P0 history mutation: `false`.
- State advanced only to `TASK-P1-020 RUNNING_B1_HEADROOM`; only the authorized 3-case B1
  retrieval plus deterministic scorer-only oracle is permitted next.

## TASK-P1-020 preserved partial harness attempt — `EVID-P1-020-HARNESS-FAIL-001`

- Command: `uv run python /private/tmp/p1_headroom_r2.py`; exit `1`.
- Failure boundary: the three authorized B1 retrieval calls and all three case artifacts were
  written; Markdown rendering then raised `KeyError: top_k` because the report stores Top-K
  under `workload.retrieval_parameters.top_k`.
- This was a harness/reporting failure, not a B1 retrieval failure. The partial report and all
  case artifacts are preserved; no B1 call was repeated and no existing artifact was overwritten.
- Failure record: `docs/tasks/p1/headroom-harness-failure-r2.json`;
  SHA-256 `e6d039fd23e153653a6b20275c6eb824bc7f4a8927dea9b64e5181b1dc64f3e0`.
- Preserved partial report: `reports/p1-headroom-r2.json`;
  SHA-256 `c415ee5c5b8ef1fa0ea863e2777cdda626d8b8e86b352ae163d08eb0e91ebdd7`.
- Preserved B1 case artifacts and hashes:
  `p0b-r1-rlinf-m.json` / `df68b88f649bef3aa69bd55a7f6729595c941587bb3cec75ea434c498c8825c1`,
  `p1-c02-kling-signal-quality-001.json` /
  `d2b5889b91a161b46911bfcb46a197520cba1e8af39072d9433e60a17c6ba486`,
  `p1-c03-rlinf-simulation-001.json` /
  `3aad2e276c407abdbba99e2fd416d86ac41cc51c731da70e46541601f310f910`.
- A subsequent read-only assembly validation caught and corrected a temporary c03 expected-hash
  constant typo before any retry output was written; the successful assembly made no retrieval
  or provider call.

## TASK-P1-020 B1 Headroom terminal — `EVID-P1-020-HEADROOM-002`

- ART-P1-002 was already frozen from the exact Owner-confirmed r2 draft:
  `eval/p1/revisions/p1-candidate-freeze-r2/candidate-manifest.json`, SHA-256
  `d523c22fdfbfb8d1ff55a2d5620d94bd6cdfac5368472995f1317b857f495cf2`.
- Authorized active set: `p1-c02-kling-signal-quality-001` and
  `p1-c03-rlinf-simulation-001`; rejected `c01` and `c04` remain history only and are not in
  the workload or any Headroom denominator, numerator, or pass count.
- B1 method: current `char_tfidf_2_4_query_views_v1`, Top-K `5`; exactly one preserved B1
  retrieval per each of the three authorized cases. Deterministic oracle was scorer-only,
  restricted to same-video `inspect_segments` radius `1/2`; Gold was not runtime context.
- Assembly command: `uv run python /private/tmp/p1_headroom_r2_finalize.py`; exit `0`.
  The assembly used the preserved case artifacts and did not rerun B1.
- Final report: `reports/p1-headroom-r2-retry-1.json`;
  SHA-256 `f5d542fba755034f9ec7ecb63367af5a7108907c555ff2e67a7beaf6a2326d88`.
- Markdown report: `reports/p1-headroom-r2-retry-1.md`;
  SHA-256 `c0e2a15e19ca244a6c6ea961b8202f6b88316aebf8efb5b6c8b89714cb78529d`.
- Report assembly metadata: `eval/p1/revisions/p1-headroom-r2-retry-1/report-assembly.json`;
  SHA-256 `7c0c7d6d6c95c3b5900de0f40f76574570a9f9812ca421225e78923a37b9ad5d`.

### Per-case B1 and deterministic-oracle evidence

- `p0b-r1-rlinf-m` (existing fixed hard case): answerable `true`. B1 Top-5 was
  `seg-010` (rank 1, `0.0855067460646253`), `seg-011` (rank 2,
  `0.08359113727403547`), `seg-032` (rank 3, `0.034175141222227284`),
  `seg-026` (rank 4, `0.027861932640742985`), `seg-022` (rank 5,
  `0.02625856754634591`). Gold units `u2/u3` hit; `u1` was missing. B1 recall was
  `2/3 = 0.6666666666666666`; `AllNecessaryEvidence@5=false`; primary failure `true`.
  The deterministic oracle's best action inspected around observed `seg-010` at radius `2`,
  adding Gold `u1` through `seg-008`, `seg-009`, and `seg-012`. It was same-video,
  scorer-only, did not read Gold at runtime, and made no provider call. Dynamic recoverable
  `true`; qualifying `true`.
- `p1-c02-kling-signal-quality-001`: answerable `true`. With the Owner-confirmed Gold split,
  B1 Top-5 was `seg-027` (rank 1, `0.05996495182397634`), `seg-026` (rank 2,
  `0.05544290525932389`), `seg-004` (rank 3, `0.03769407278071571`), `seg-031`
  (rank 4, `0.03268242564722136`), `seg-002` (rank 5, `0.03212952938378714`).
  Both independent units `u1=1237400..1282920 / seg-026` and
  `u2=1282920..1330200 / seg-027` hit; recall `2/2 = 1.0`;
  `AllNecessaryEvidence@5=true`; primary failure `false`. No oracle recovery was needed;
  dynamic recoverable `false`; qualifying `false`.
- `p1-c03-rlinf-simulation-001`: answerable `true`. B1 Top-5 was `seg-009` (rank 1,
  `0.2017283563140097`), `seg-022` (rank 2, `0.0905912445881536`), `seg-000`
  (rank 3, `0.04879350504034671`), `seg-024` (rank 4, `0.04626625326526533`),
  `seg-003` (rank 5, `0.043024676479501485`). Gold `u1=seg-009` hit; recall
  `1/1 = 1.0`; `AllNecessaryEvidence@5=true`; primary failure `false`. No oracle recovery
  was needed; dynamic recoverable `false`; qualifying `false`.

### Headroom Gate and stop boundary

- Qualifying Headroom count: `1/3`; required minimum: `2`.
- Final Gate: `NO_GO_INSUFFICIENT_HEADROOM`.
- Provider calls: `0`; video upload: `false`; B2 design/implementation/execution: `false`;
  `TASK-P1-030`: not started; B0: `NOT_AVAILABLE/NOT_RUN`.
- P0 historical evidence and the protected 181-file snapshot remain unchanged. All three B1
  case artifacts and both report attempts are retained.
- `TASK-P1-020` terminates at this No-Go boundary. No later Gate, `TASK-P1-030`, or B2 work
  is authorized or started.

### Final closeout verification

- `uv run pytest`: exit `0`, `28 passed`.
- `uv run ruff check .`: exit `0`, all checks passed.
- `git diff --check`: exit `0`; the protected P0 path diff remained empty.
- `jq -c . docs/requirements/p1/decision-evidence.jsonl`: exit `0`; all decision records parse.
- Requirements validator: `uv run python /Users/tristana/.codex/skills/agent-native-requirements/scripts/validate_readiness.py /Users/tristana/Develop/video-evidence-agent/docs/requirements/p1 --output /Users/tristana/Develop/video-evidence-agent/docs/requirements/p1/requirements-readiness.json`; exit `0`, `READY_FOR_ENGINEERING_HANDOFF`.
- Current readiness SHA-256: `ade9c3b8e807ab5230c8bef37cdd28e3b95cd52c68831dc2d6ce39e49b82cdef`.
