# VR-V1A-ADAPTIVE-BUDGET-WEB-CLOSURE-008

## Task control

| Field | Value |
|---|---|
| Grade | `G1 PROTOTYPE` |
| Task status | `READY_FOR_OWNER_V1A_REVIEW — EXTERNAL_BLOCKED` |
| Repository | `/Users/tristana/Develop/video-evidence-agent` |
| Product-code baseline | `visual-report` at `bb8f6f75aa2e4ae91ab6688a7f16ed87caec7741`; preserve the documentation-only Task 008 overlay if it is still uncommitted |
| Design authority | `DEC-VR1A-061`–`066`; current budget amendment is `DEC-VR1A-065/066` |
| Execution mode | One continuous bounded Goal; no intermediate Owner checkpoint for ordinary in-scope engineering errors |
| Primary completion | `READY_FOR_OWNER_V1_WEB_MVP_REVIEW — ADAPTIVE_TEXT_AND_WEB_LOOP_READY` |
| Owner-only boundary | The implementer must not record V1-A acceptance, start V1-B/V1-C, deploy, publish, commit, push, or create a PR unless separately authorized |

## Outcome

Close the current text-to-Web G1 loop without redesigning VEA:

```text
full transcript
  -> Topic Mapper
  -> deterministic Topic Resolver
  -> adaptive planning budget
  -> Report Planner
  -> non-semantic deterministic compiler
  -> current V0 Renderer
  -> existing localhost Web MVP
  -> Owner review
```

The task answers two product questions:

1. Does replacing the obsolete fixed 14-block ceiling with a source-derived
   soft budget let all three videos render without weakening grounding or
   turning the compiler into a semantic editor?
2. Once all three reports exist, does the already-implemented loopback Web
   surface provide a usable minimum local workflow for choosing a source,
   starting a run, observing canonical state, and opening the report?

This is not a Provider/Schema experiment, a six-run formal measurement, a VEA
redesign, or a production Web release.

## Baseline facts that must remain evidence

- The Owner-confirmed merged product-code baseline is the commit above. The
  requirements/status/task-card edits that define Task 008 may be present as
  an expected uncommitted documentation overlay; preserve them and do not
  reinitialize/reset the checkout.
- Historical strict-schema, recovery, provider-conformance, semantic-v2, and
  text/Web-closure attempts remain immutable.
- Latest frozen product revision `vr1a-semantic-v2-56340249c6f9` used `6/6`
  calls with no retry:
  - Kling: `RENDERED`, 10 compiled blocks;
  - RLinf: `RENDERED`, 11 compiled blocks; and
  - Wu Yi: `FAILED — PLAN_BUDGET_ERROR` after a valid 17-unit Planner proposal
    exceeded the inherited 14-block ceiling.
- Wu Yi's retained raw Planner proposal is under
  `artifacts/visual-report/v1a/p0b-wuyi-goals-semantic-v2-98d9af23a9/`.
- The existing Web module, CLI command, loopback API/UI, and five fake-provider
  tests are merged. No real server/browser/Web smoke was executed because the
  previous 3/3 text gate failed.
- Current successful/retained proposals are approximately 99–103 visible
  authored characters per block under the existing counter, below the new
  180–260 advisory density. This is product-review evidence, not a compile
  failure.

Never relabel, overwrite, backfill, delete, or selectively promote these
artifacts. A replay output or new revision uses new identities and directories.

## Owner-confirmed adaptive budget

### Deterministic formula

Compute after the canonical semantic-v2 Topic Map and before the Planner call:

```text
duration_term = duration_ms / 60_000 * 0.6
topic_term = primary_topic_count * 2
recommended_block_budget = clamp(
  ceil(max(duration_term, topic_term, 6)),
  6,
  24
)
```

- `duration_ms` comes from the validated source manifest.
- `primary_topic_count` counts canonical semantic-v2 topics whose importance is
  exactly `primary`.
- `ceil` is the deterministic integer translation of the Owner's formula.
- The current retained snapshots should produce Kling `21`, RLinf `21`, and
  Wu Yi `18`; tests must derive these values rather than hard-code by video ID.

### Soft recommendation versus hard protection

- The 6–24 result is an editorial recommendation, not an exact output count.
- Planner receives the recommendation, per-block density guidance, and hard
  limits. It is explicitly told not to pad, repeat, or force a fixed block
  distribution.
- A compiled count below or above the recommendation remains valid and emits a
  visible undershoot/overshoot diagnostic.
- Exactly 32 compiled blocks may pass; more than 32 fails
  `PLAN_BUDGET_ERROR`.
- Existing minimum usable-content, 3–5-section, per-section block, field/list,
  source, metric, typed-block, and V0 validation rules remain unchanged.
- The compiler may not omit an otherwise usable semantic unit merely to reach
  either the recommendation or hard limit.

### Character budget

Use the existing visible-authored Unicode counter: Hero title/TLDR, section
titles, and user-visible block strings count; IDs, refs, timestamps, type names,
asset metadata, and renderer-generated labels do not.

For `n = actual_compiled_block_count`:

```text
recommended_min = n * 180
recommended_max = min(n * 260, 8_000)
```

- The range is aggregate guidance, not a per-block validation quota.
- Below/above range at or below 8,000 characters is diagnostic only.
- Exactly 8,000 may pass; more than 8,000 fails `PLAN_BUDGET_ERROR`.
- No truncation, rewrite, merge, split, padding, or budget-driven semantic
  omission is allowed.

### Versioned evidence

Every new run must retain an equivalent of:

- `planning-budget.json`: formula version, duration, primary-topic count,
  recommendation, density guidance, and hard limits; and
- `budget-diagnostics.json`: actual compiled blocks/visible characters,
  recommended ranges, soft diagnostic states, hard checks, and compiler
  version.

The exact budget object must also appear in the frozen Planner request snapshot.
Budget diagnostics are validation evidence, not normalization events.

## Hard boundaries

### Preserve

- Topic Mapper and Report Planner remain two sequential independent semantic
  stages; both receive the full authorized transcript and Planner also receives
  the canonical Topic Map.
- DeepSeek `deepseek-v4-flash-vision-exp`, Chat Completions JSON object,
  Thinking enabled, reasoning effort high, `max_tokens=32768`, SDK retry zero,
  and at most one identical retained application retry per run remain frozen.
- Models select semantics and existing source IDs only. Code owns canonical
  identity, time, refs, adaptive budget, typed-block compatibility, validation,
  state, evidence, and rendering.
- Normalization remains non-semantic: no rewrite, merge, split, expansion,
  shortening, fabrication, or hidden model repair.
- Existing V0 `ReportPlan`, empty `AssetManifest`, Renderer, and `report.html`
  remain canonical.
- Every success, failure, retry, cancellation, replay, revision, screenshot,
  and review artifact is retained under a unique identity.

### Do not add

- MP4/ASR, keyframes, OCR/VLM, RAG, Agent, LangGraph, tool calling, memory,
  database, queue, account, multi-user service, hosted/public Web, deployment,
  V1-B, or V1-C;
- a second provider/model, provider fallback, per-video prompt/configuration,
  prompt micro-version loop, chunking fallback, or third semantic stage;
- new dependencies, renderer redesign, new template system, or V0 schema
  expansion merely to consume the larger aggregate budget; or
- formal three-video × two-repeat measurement, auto-filled human rubric,
  Owner acceptance, or release claims.

## Allowed implementation surface

Modify the smallest existing surface required:

- `src/video_evidence_agent/visual_report/planning.py` for semantic-v2-only
  budget constants, formula, Planner payload/prompt version, diagnostics, and
  hard checks while preserving historical strict-v1 constants;
- `planning_runtime.py` for run/request snapshots and budget artifact writing;
- `evaluation.py` only for budget/density fields in the current product review;
- `web.py` and `__main__.py` only when an observed real defect prevents the
  already-designed local workflow; do not redesign the UI/API;
- focused existing visual-report tests, one new versioned product manifest,
  review artifacts/screenshots, this task evidence, and V1-A status/docs.

Do not change dependencies or protected P0-B/V0 artifacts. Existing V0 code may
change only if a reproduced incompatibility proves the semantic-v2 adapter
cannot satisfy the already-supported V0 contract; that condition normally
stops as contract change rather than broadening this task.

## Continuous Goal sequence

### G0 — Baseline and preservation

1. Read repository instructions plus current V0/V1-A status and canonical
   contracts in their prescribed order.
2. Verify branch, HEAD/ancestry, known worktree state, merged Web source,
   current tests, manifests, and retained run directories. Treat this task's
   documentation-only diff as expected user work rather than a dirty-tree
   blocker.
3. Inventory the three latest product identities and prove the Wu Yi raw
   proposal has 17 usable content units and failed at the old aggregate cap.
4. Record the baseline and protected-path inventory in the task evidence.

Gate: no file or artifact is overwritten; no provider call occurs.

### G1 — Implement semantic-v2 adaptive budgeting

1. Add a semantic-v2-specific budget version and deterministic formula. Do not
   mutate global historical `8–14 / 2,600` constants used by strict-v1 replay.
2. Compute the budget after Topic Resolver and before Planner; include it in the
   Planner payload/prompt and frozen request/run snapshots.
3. Change only semantic-v2 aggregate hard limits to 32 blocks and 8,000 visible
   characters. Keep every existing V0/per-field/per-section/grounding/metric
   rule.
4. Emit soft block/density diagnostics without changing proposal semantics.
5. Add deterministic budget artifacts and product-review fields.
6. Add boundary and regression tests before any real call.

Ordinary code/test/evidence defects are repaired automatically inside G1. No
Owner checkpoint is needed while work remains provider-free and within this
contract.

### G2 — Zero-call replay and visual admission

Provider/model calls must remain `0/0`.

1. Test formula inputs, `ceil`, lower/upper clamp, zero primary topics, duration
   dominance, topic dominance, and current three expected results.
2. Test soft undershoot/overshoot and density states without retry or semantic
   mutation.
3. Test aggregate boundaries: 32/8,000 accepted at the budget layer; 33/8,001
   fail. Where a complete V0 object cannot express a synthetic boundary because
   of an unchanged lower-level field limit, test the counter/hard-budget unit
   directly and separately prove V0 validation remains authoritative.
4. Replay the retained Kling, RLinf, and Wu Yi semantic proposals into new
   output directories. All three must compile/render with `0/0` calls; Wu Yi's
   17 usable units must survive without budget-driven semantic deletion,
   rewrite, merge, or split.
5. Capture/inspect each replay report at 1080 px and 390 px. Retain six
   screenshots and verify no critical horizontal overflow, clipping, overlap,
   unreadable source text, or broken hierarchy.

Gate A passes only when all formula/boundary/replay tests pass, all three replay
reports render, Wu Yi retains its semantics, and all six replay viewport checks
are usable. If the larger report exposes a layout problem, make the smallest
in-scope deterministic CSS/adapter repair only when it preserves the V0
contract; otherwise stop before any model call.

### G3 — Freeze and execute one new three-video product set

After Gate A only:

1. Freeze one wholly new revision containing source hashes, review-card hashes,
   prompt/budget/schema/compiler/evaluator versions, exact DeepSeek runtime
   tuple, three unique product run IDs, and one gated Web-smoke ID.
2. Run Kling, RLinf, and Wu Yi once each under the same frozen revision. Execute
   the complete predeclared set; do not tune or selectively replace a video.
3. Each run owns two base calls and at most one identical eligible technical
   retry, so the product-set ceiling is nine provider/model calls.
4. A soft budget/density miss does not fail the run and does not trigger retry.
   Grounding, unsupported metric, invalid semantics/V0 shape, and aggregate hard
   limits remain visible non-retryable failures.
5. Render every valid report and capture 1080 px plus 390 px screenshots.
6. Generate one append-only product review package with human rubric fields
   still pending Owner review.

Gate B is exactly 3/3 new product identities in `RENDERED` with valid lineage,
empty assets, current V0 reports, six current-revision screenshots, and no hard
budget/security/contract failure. Advisory density misses are recorded for
Owner judgment but do not keep the local Web gate closed.

After freeze, a prompt, budget formula, hard limit, compiler semantic behavior,
source, model, or review-target change invalidates the product set. Preserve it
and stop for a new revision; do not patch-and-rerun inside this frozen set.

### G4 — Exercise the existing local Web MVP

After Gate B only:

1. Re-run provider-free Web/API/fake-provider tests and fix ordinary observed
   Web-only defects without changing planning semantics or the frozen product
   set.
2. Start the real loopback server on `127.0.0.1`; never bind a public interface.
3. In a real browser at 1080 px and 390 px, verify source selection, unique-run
   submission, canonical state display, error display, duplicate-submit
   protection, and opening the three frozen reports.
4. Execute the one predeclared Kling Web-smoke identity through the UI once. It
   may use two base calls plus the same one eligible technical retry, for a
   three-call Web ceiling.
5. Confirm credentials remain server-only, arbitrary paths/traversal are
   rejected, one active run remains the concurrency policy, and the Web state
   exactly maps `run.json`.

The absolute Goal ceiling is twelve provider/model calls: nine for the product
set plus three for the gated Web smoke. Replay, tests, evaluator, screenshots,
and opening existing reports use `0/0` calls.

### G5 — Evaluate, regress, and close documentation

1. Run the product evaluator once for the new revision; do not create a formal
   six-run measurement or fill Owner rubric scores.
2. Run focused planning/runtime/Web tests, full pytest, Ruff, V0 renderer
   regression, replay `0/0`, `git diff --check`, protected-path/history checks,
   and artifact/call inventory.
3. Record per-video formula inputs, recommendations, actual blocks, visible
   character counts/density diagnostics, state, calls, retry, report, and both
   screenshot paths.
4. Update this task and `docs/visual-report/V1A-STATUS.md` with the exact
   terminal state. Preserve all previous status history.
5. Stop for Owner content/visual/Web review. Do not self-accept or continue to
   V1-B/V1-C.

## Acceptance matrix

| ID | Required evidence | Pass condition |
|---|---|---|
| `ABW-001` | Baseline and history inventory | Correct branch/commit; all frozen identities/artifacts preserved |
| `ABW-002` | Formula unit tests | Exact formula, `ceil`, clamp, source authorities, and current 21/21/18 results |
| `ABW-003` | Budget artifact/request snapshot | Same versioned inputs/result/limits before Planner; no secret/transcript duplication |
| `ABW-004` | Soft-budget tests | Undershoot/overshoot compiles with diagnostics and no retry/semantic change |
| `ABW-005` | Hard-budget tests | 32 and 8,000 accepted by budget layer; 33 and 8,001 fail predictably |
| `ABW-006` | Historical compatibility | Strict-v1 8–14/2,600 artifacts and tests remain unchanged |
| `ABW-007` | Three saved-proposal replays | `0/0` calls; 3/3 render; Wu Yi retains 17 usable units without budget repair |
| `ABW-008` | Replay visual admission | Six 1080/390 screenshots; no critical layout defect before real calls |
| `ABW-009` | Frozen real product set | Three new identities, one tuple, complete execution, ≤9 calls |
| `ABW-010` | Product reports | 3/3 `RENDERED`; valid refs/metrics/V0 plans; empty assets; six current screenshots |
| `ABW-011` | Density evidence | Actual counts/ranges/status recorded; soft miss remains pending Owner judgment |
| `ABW-012` | Existing Web runtime | Fake/API tests pass; real loopback server and both browser widths verified |
| `ABW-013` | Real Web smoke | One predeclared Kling UI run, ≤3 calls, canonical state/report, no duplicate call |
| `ABW-014` | Regression/protection | Focused/full/Ruff/V0/diff/protected/history/replay checks pass |
| `ABW-015` | Owner boundary | Rubrics pending; no acceptance, V1-B/C, deployment, commit, push, or PR |

## Terminal matrix

Use one exact terminal; never invent a success report or score.

| First unmet boundary | Required terminal |
|---|---|
| Formula, boundary, replay, semantic preservation, or replay-layout Gate A fails before real calls | `READY_FOR_OWNER_V1A_REVIEW — ADAPTIVE_BUDGET_REPLAY_FAILED` |
| Credential, balance/quota, permission, network, or configured model access blocks the frozen set | `READY_FOR_OWNER_V1A_REVIEW — EXTERNAL_BLOCKED` |
| Product set exhausts an eligible API/JSON retry and cannot produce 3/3 reports | `READY_FOR_OWNER_V1A_REVIEW — ADAPTIVE_TEXT_RUNTIME_INCONCLUSIVE` |
| Valid semantic output cannot produce 3/3 reports because of grounding, V0 incompatibility, or a hard budget without prohibited repair | `READY_FOR_OWNER_V1A_REVIEW — ADAPTIVE_BUDGET_CONTENT_INSUFFICIENT` |
| Continuing requires prompt/formula/hard-limit/compiler/source/model or V0 product-contract change after freeze | `READY_FOR_OWNER_V1A_REVIEW — ADAPTIVE_PRODUCT_SET_INVALID` |
| Text gate passes but the existing Web surface requires excluded API/service/infrastructure scope | `READY_FOR_OWNER_V1_WEB_REVIEW — WEB_CONTRACT_CHANGE_REQUIRED` |
| Text gate passes but real loopback/browser/Web smoke remains incomplete after allowed Web-only repair or eligible retry | `READY_FOR_OWNER_V1_WEB_MVP_REVIEW — WEB_RUNTIME_INCONCLUSIVE` |
| 3/3 text, Web smoke, regressions, responsive checks, and review package pass | `READY_FOR_OWNER_V1_WEB_MVP_REVIEW — ADAPTIVE_TEXT_AND_WEB_LOOP_READY` |

## Verification commands

Use the existing project-local uv environment and task-specific cache path.
Exact focused test selectors may follow the implementation's existing test
layout, but the final evidence must include:

```bash
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run ruff check .
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q tests/test_visual_report_planning.py
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q
git diff --check
```

Also run the existing semantic-v2 replay command for all three retained
proposal pairs, the V0 renderer regression, focused Web tests, protected-path
diff review, and exact call/artifact inventory. Do not print `.env` or secret
values in commands or evidence.

## Implementation evidence

The design snapshot originally declared `NOT_STARTED`. The execution record
below appends observed evidence without changing the requirements or deleting
the design record.

## Execution evidence — 2026-08-31

### G0 baseline and preservation

- The checkout remained on branch `visual-report` at
  `bb8f6f75aa2e4ae91ab6688a7f16ed87caec7741`, the requested product-code
  baseline. The existing Task 008 requirements/status/task-card overlay was
  preserved; no reset, reinitialization, commit, push, PR, or deployment was
  performed.
- The three latest 007 product identities and their artifacts remain intact:
  Kling `RENDERED 2/2`, RLinf `RENDERED 2/2`, and Wu Yi `FAILED 2/2` at the
  former 14-block cap. The 007 run directories and frozen inputs were not
  overwritten.

### G1/G2 adaptive budget and zero-call admission

- The semantic-v2-only implementation changed `planning.py`,
  `planning_runtime.py`, `evaluation.py`, and focused semantic-v2 tests. The
  historical strict-v1 `8–14` and `2,600` limits remain unchanged. The new
  budget formula, soft diagnostics, `32` compiled-block/`8,000` visible-
  character hard limits, run artifacts, and frozen Planner request snapshot
  are versioned under the semantic-v2 adaptive contract.
- Provider-free formula/boundary/soft-diagnostic tests and the current
  retained-source derivation passed. The derived recommendations are Kling
  `21`, RLinf `21`, and Wu Yi `18`. The focused planning plus semantic-v2
  suite passed `50` tests before the final full-suite rerun.
- New replay outputs are under
  `artifacts/visual-report/v1a/vr-v1a-adaptive-budget-web-closure-008-replay/`.
  All three are `provider_calls/model_calls=0/0`, render successfully, and
  have zero semantic rewrite/merge/split/synthesis normalization events:

  | Video | Recommended blocks | Compiled blocks | Visible chars | Soft diagnostics | Hard failure |
  |---|---:|---:|---:|---|---|
  | `p0b-kling-2024` | 21 | 10 | 1,024 | block/density undershoot | false |
  | `p0b-rlinf-2026` | 21 | 11 | 1,080 | block/density undershoot | false |
  | `p0b-wuyi-goals` | 18 | 17 | 1,634 | block/density undershoot | false |

- Wu Yi's retained raw Planner proposal contains 17 usable content units and
  the adaptive replay compiles all 17; no budget-driven semantic deletion,
  rewrite, merge, split, truncation, or padding occurred.
- Each replay has `screenshots/desktop.png`, `screenshots/mobile.png`, and
  `viewport-check.json`. Real-browser checks at 1080×1440 and 390×1440
  recorded five ordered sections, zero horizontal-overflow nodes, and the
  natural page heights 2,839/3,424 px (Kling), 3,131/3,637 px (RLinf), and
  3,734/4,531 px (Wu Yi). Gate A passed before any new model call.

### G3 frozen product set and external stop

- Gate A produced the new manifest
  `eval/visual-report-v1a/semantic-v2-adaptive-budget-web-closure-008-manifest.json`
  with revision `vr1a-semantic-v2-29d077aa0bdc` and SHA-256
  `13e7784d161f101c1e75bbdd104db722d61a72beff56ef65caf45d35431e81b3`.
  Its single tuple remains DeepSeek
  `deepseek-v4-flash-vision-exp`, Chat Completions JSON object, Thinking
  enabled, reasoning effort `high`, `max_tokens=32768`, temperature `0`, SDK
  retry `0`, and one identical application retry per run.
- The new Kling product identity
  `p0b-kling-2024-semantic-v2-e3d720ac27` made two identical provider attempts;
  both were retained as `PROVIDER_ERROR` with
  `provider request failed: APIConnectionError`, and the run ended
  `FAILED`, `2/2`, with the eligible retry exhausted. No additional model
  call was made. RLinf and Wu Yi were not started after this external block,
  so the product-set total is `2/9` and the Goal total is `2/12`.

### G4/G5 Web and final regressions

- Gate B was not reached. The existing localhost Web MVP was not started and
  the predeclared Kling Web smoke remained `0/3`; the temporary loopback
  static server used for the G2 replay screenshots was not the Web MVP.
- The append-only evaluator package is
  `artifacts/visual-report/v1a/evaluation-008/vr1a-semantic-v2-29d077aa0bdc/`.
  It records `technical_status=FAILED`,
  `stop_state=PROTOTYPE_EXECUTION_INCONCLUSIVE`, observed `2/2` calls, and
  all Owner rubrics pending. This is not Owner acceptance.
- Final provider-free focused planning/semantic/Web tests passed `55`, the
  full suite passed `93`, full Ruff passed, V0 renderer regression passed
  `10`, replay inventory remained `0/0`, and `git diff --check` passed. The
  final diff contains only the allowed semantic-v2 source/test surface, the
  expected Task 008 documentation overlay, and the new frozen manifest; no
  protected P0-B/V0 inputs or historical 007 artifacts changed.

The exact Task 008 terminal is:

`READY_FOR_OWNER_V1A_REVIEW — EXTERNAL_BLOCKED`

The next action remains Owner review of the retained evidence. No Owner
acceptance, V1-B/V1-C, deployment, publication, commit, push, or PR was
performed.
