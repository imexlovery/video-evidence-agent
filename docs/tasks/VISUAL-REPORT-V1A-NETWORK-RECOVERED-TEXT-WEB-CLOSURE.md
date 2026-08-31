# VR-V1A-NETWORK-RECOVERED-TEXT-WEB-CLOSURE-010

## Task control

| Field | Value |
|---|---|
| Grade | `G1 PROTOTYPE` |
| Task status | `READY_FOR_OWNER_V1_WEB_MVP_REVIEW — ADAPTIVE_TEXT_AND_WEB_LOOP_READY` |
| Repository | `/Users/tristana/Develop/video-evidence-agent` |
| Branch | `visual-report` |
| Execution mode | One continuous bounded Goal; stop at the first exact terminal boundary |
| Product scope | One new three-video semantic-v2 text set, then the existing loopback Web MVP only after 3/3 text render |
| Provider scope | DeepSeek `deepseek-v4-flash-vision-exp` only; product ceiling 9 calls, Goal ceiling 12 calls |
| Owner-only boundary | No Owner acceptance, V1-B/V1-C, deployment, publication, commit, push, or PR |

## Objective

Execute a wholly new, source-grounded semantic-v2 text-to-Web product loop after
the Task 009 network-recovery diagnostic, without resuming or replacing Task
008/009:

```text
full authorized transcript
  -> Topic Mapper
  -> deterministic Topic Resolver
  -> adaptive planning budget
  -> Report Planner
  -> deterministic V0 compiler
  -> existing V0 renderer
  -> existing localhost Web MVP
  -> Owner review
```

The product set is exactly one new run for each of Kling, RLinf, and Wu Yi. The
predeclared Web smoke is exactly one new Kling run and is permitted only after
the three product runs render successfully.

## Preserved history and hard boundaries

- Task 008's frozen manifest, failed Kling product run, evaluator package, and
  all retained evidence remain immutable and excluded from this denominator.
- Task 009's successful `diagnostic_only` Kling canary remains diagnostic-only;
  it is neither a product run nor a replacement for the new three-video set.
- Topic Mapper and Report Planner remain two sequential independent calls. Both
  receive the full authorized transcript; Planner additionally receives the
  canonical Topic Map.
- The sole frozen provider tuple is DeepSeek Chat Completions JSON object,
  Thinking enabled, reasoning effort `high`, temperature `0`,
  `max_tokens=32768`, SDK retry `0`, and at most one identical eligible
  application retry per run.
- Models select semantic content and existing source IDs only. Deterministic
  code owns canonical IDs, timestamps, `SourceRef`, normalization, adaptive
  budget, compilation, validation, state, evidence, and renderer invocation.
- Normalization is non-semantic. No semantic rewrite, merge, split, synthesis,
  truncation, padding, hidden chunking, third model call, provider fallback,
  selective rerun, or manual plan substitution is allowed.
- Existing V0 `ReportPlan`, empty `AssetManifest`, `report.html`, and Renderer
  remain canonical. No MP4/ASR, keyframes, OCR/VLM, RAG, Agent, LangGraph,
  database, queue, service redesign, public hosting, V1-B, or V1-C.

## Adaptive budget contract

```text
duration_term = duration_ms / 60_000 * 0.6
topic_term = primary_topic_count * 2
recommended = clamp(ceil(max(duration_term, topic_term, 6)), 6, 24)
```

The recommendation and 180–260 visible authored characters per compiled block
are soft diagnostics. Only more than 32 compiled blocks or more than 8,000
visible authored characters is a hard aggregate failure. No budget miss may
trigger semantic repair or retry.

## Bounded sequence

### G0 — provider-free admission

Run the focused semantic/Web tests, formula and boundary checks, and a fresh
zero-call replay of the retained accepted proposal pairs. Capture and inspect
all six replay viewports at 1080×1440 and 390×1440. Do not call the provider.

### G1 — freeze and execute the new product set

Freeze a new manifest with source/card/prompt/schema/runtime/compiler/evaluator
hashes, the exact provider tuple, three new product identities, and one new Web
smoke identity. Run Kling, RLinf, and Wu Yi once each under that revision. Each
run may consume two base calls plus one identical eligible technical retry.

### G2 — gated Web MVP

Only after 3/3 product runs are `RENDERED`, start the existing loopback server
on `127.0.0.1`, inspect the real UI at 1080×1440 and 390×1440, verify source
selection, canonical status/report opening, duplicate protection, traversal
rejection, server-only credentials, and the single active-run policy. Submit
the one predeclared Kling Web smoke once, with a maximum of three calls.

### G3 — evaluation and close

Run the product evaluator once, retain pending Owner rubrics, execute focused
and full regressions, Ruff, V0 regression, replay/call/artifact inventory,
protected-history checks, and `git diff --check`. Append the exact terminal to
this card and `docs/visual-report/V1A-STATUS.md`; stop for Owner review.

## Exact terminals

Use exactly one terminal for this Task 010 execution:

```text
READY_FOR_OWNER_V1_WEB_MVP_REVIEW — ADAPTIVE_TEXT_AND_WEB_LOOP_READY
```

If an earlier boundary is genuinely unmet, use only the matching contract
terminal from the V1-A status/task package and preserve all evidence; do not
claim the success terminal.

## Execution evidence — 2026-08-31

### G0 provider-free admission

Completed before any Task 010 provider call. The focused planning, semantic-v2,
and Web test set passed `55` tests. The first sandbox attempt exposed only the
known loopback bind restriction; the same provider-free set passed after
controlled loopback permission. No API key or transcript was sent.

Fresh replay output is under
`artifacts/visual-report/v1a/vr-v1a-network-recovered-text-web-closure-010-replay/`.
Kling, RLinf, and Wu Yi each rendered with `provider_calls/model_calls=0/0`.
All three replay normalizers report zero semantic rewrite, merge, split, and
synthesis events. The replay metrics were:

| Video | Recommendation | Compiled blocks | Visible chars | Hard failure |
|---|---:|---:|---:|---|
| `p0b-kling-2024` | 21 | 10 | 1,024 | false |
| `p0b-rlinf-2026` | 21 | 11 | 1,080 | false |
| `p0b-wuyi-goals` | 18 | 17 | 1,634 | false |

Each replay has `screenshots/desktop.png`, `screenshots/mobile.png`, and
`viewport-check.json`. Real-browser checks at 1080×1440 and 390×1440 recorded
five ordered sections and zero horizontal-overflow nodes. Natural page heights
were 2,839/3,424 px (Kling), 3,131/3,636 px (RLinf), and 3,734/4,530 px
(Wu Yi). Wu Yi's 17 usable retained units were not budget-deleted or repaired.

### G1 freeze

The new product manifest is
`eval/visual-report-v1a/semantic-v2-network-recovered-text-web-closure-010-manifest.json`
with SHA-256
`0a003cd17d808c7d07c25036c3e3cb664c2d35a4610bc8c64f3bfcb374020d45` and
revision `vr1a-semantic-v2-e33c28c6a662`. It is `FROZEN` and `READY` for the
DeepSeek provider tuple. The manifest declares these new product identities:

- `p0b-kling-2024-semantic-v2-0b3956f2ad`
- `p0b-rlinf-2026-semantic-v2-0b3956f2ad`
- `p0b-wuyi-goals-semantic-v2-0b3956f2ad`
- Web smoke: `p0b-kling-2024-semantic-v2-0b3956f2ad-web-smoke`

The frozen source, review-card, prompt/schema, runtime/evaluator, adaptive
budget, compiler, and current V0 renderer evidence was checked before the
first call. The renderer SHA-256 is
`68354e187bfb224882ab6c3a330314605c23bcbf371ec6e094c8cab341d04d15`.

No historical Task 008/009 artifact was rewritten or counted as Task 010.

### G2 real provider execution

Waiting for explicit authorization to send the full local transcript-derived
payload to `https://api.deepseek.com`. The first authorized run command was
rejected before process start because that specific data export was not
explicitly authorized. Current Task 010 provider/model calls remain `0/0`.

### G2 continuation after explicit authorization

The Owner then explicitly authorized sending the Kling, RLinf, and Wu Yi
full transcript-derived payloads to `https://api.deepseek.com`. The frozen
manifest was not recreated and the reserved identities were used exactly once
each:

| Video | Run identity | State | Calls | Retry | Blocks | Visible chars | Budget status |
|---|---|---|---:|---|---:|---:|---|
| `p0b-kling-2024` | `p0b-kling-2024-semantic-v2-0b3956f2ad` | `RENDERED` | 2/2 | false | 9 | 1,251 | block/density undershoot; hard pass |
| `p0b-rlinf-2026` | `p0b-rlinf-2026-semantic-v2-0b3956f2ad` | `RENDERED` | 2/2 | false | 6 | 624 | block/density undershoot; hard pass |
| `p0b-wuyi-goals` | `p0b-wuyi-goals-semantic-v2-0b3956f2ad` | `RENDERED` | 2/2 | false | 14 | 988 | block/density undershoot; hard pass |

The deterministic recommendations were Kling `21` (5 primary topics), RLinf
`21` (8 primary topics), and Wu Yi `18` (5 primary topics). All three runs
retained valid source snapshots, empty asset manifests, current V0 reports,
Planner request snapshots frozen before the call, and zero semantic
rewrite/merge/split/synthesis normalization events. All six calls were ordered
Mapper then Planner and ended with `finish_reason=stop`.

### G3 gated Web MVP smoke

Text Gate 3/3 opened the existing Web MVP. It was served only on
`http://127.0.0.1:8772/visual-report/` with the Task 010 artifact root and
manifest. Through the real browser, source selection worked at 1080×1440 and
390×1440; the UI retained `scrollWidth == innerWidth`, displayed the canonical
`RENDERED` state, and exposed the predeclared Web report link. While the smoke
run was active, the Generate button remained disabled at both `MAPPING` and
`PLANNING`, with observed calls `1` and `2`; the provider-free/API test set
also passed the same active-run and duplicate-request protections.

The sole Web smoke identity
`p0b-kling-2024-semantic-v2-0b3956f2ad-web-smoke` completed through the UI as
`RENDERED`, `2/2`, no retry, 21 blocks, 1,665 visible characters, and no hard
budget failure. Its canonical report was opened from the Web MVP endpoint.
The Web sources endpoint returned the three allowlisted IDs; traversal returned
`404 RUN_NOT_FOUND`. The browser-visible page did not contain the
`OPENAI_API_KEY` name. Web UI desktop/mobile screenshots and the check record
are retained under the Web smoke directory.

Product provider calls are `6/9`; Web smoke calls are `2/3`; total Goal usage
is `8/12`. No second Web smoke, retry, formal six-run measurement, or
selective rerun was performed.

As a provider-free supplementary browser check, the same Web MVP was served on
`127.0.0.1:8773` and opened with a nonexistent run id. The real mobile page
displayed `WEB_ERROR`, `状态暂时不可用`, and `请保留当前页面并稍后重试。`; the
Generate button was enabled again and no provider call was created. The
corresponding screenshot and check record are
`web-ui-error.png` and `web-ui-check.json` under the Web smoke directory.

### G4 evaluator and regression close

The append-only evaluator package is
`artifacts/visual-report/v1a/evaluation/vr1a-semantic-v2-e33c28c6a662/`.
Its aggregate records `technical_status=PASS`, all three deterministic rows
as `PASS`, `stop_state=READY_FOR_OWNER_V1A_REVIEW`,
`conclusion=PROTOTYPE_REPORTS_READY`, and `quality_status=PENDING_OWNER_REVIEW`.
All three Owner rubrics remain pending with no human scores or acceptance.

Final provider-free and protection checks passed:

- focused planning + semantic-v2 + Web tests: `55 passed`;
- full pytest: `93 passed`;
- Ruff: `All checks passed!`;
- V0 renderer regression: `10 passed`;
- fresh replay inventory: all three `provider_calls/model_calls=0/0`;
- `git diff --check`: passed;
- Task 008 and Task 009 protected evidence SHA-256 values: unchanged from the
  pre-execution inventory;
- no V0/P0-B protected source or artifact path was changed by Task 010.

The exact Task 010 terminal is:

`READY_FOR_OWNER_V1_WEB_MVP_REVIEW — ADAPTIVE_TEXT_AND_WEB_LOOP_READY`

This is an Owner-review handoff, not Owner acceptance. The current product,
content, visual, and Web judgments remain for Owner review. No commit, push,
PR, deployment, publication, V1-B, or V1-C action was performed.
