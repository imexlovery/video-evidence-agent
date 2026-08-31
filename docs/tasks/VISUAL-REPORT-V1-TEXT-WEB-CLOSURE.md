# Video Visual Report — Text Runtime Closure + Local Web MVP Goal

## Task identity

| Field | Value |
|---|---|
| Task ID | `VR-V1-TEXT-WEB-CLOSURE-007` |
| Grade | `G1 PROTOTYPE` |
| Goal mode | One continuous gated Goal; automatically repair ordinary in-scope engineering defects |
| Design authority | `DEC-VR1A-062`, `DEC-VR1A-063`, `DEC-VR1A-064` |
| Execution status | `EXECUTED — STOPPED_AT_TEXT_CONTENT_INSUFFICIENT`; Owner review required |
| Canonical repository | `/Users/tristana/Develop/video-evidence-agent` |
| Task-card worktree | `/Users/tristana/.codex/worktrees/9299/video-evidence-agent` |
| Expected branch/baseline | `codex/visual-report-semantic-v2` at `844978f08d07775b650467e31e221a969ddef3e3`; canonical `visual-report` currently points to the same commit; recheck and do not switch/reinitialize before work |
| Primary completion | `READY_FOR_OWNER_V1_WEB_MVP_REVIEW — TEXT_AND_WEB_LOOP_READY` |

When created, this was a documentation-only task definition: that design session
did not change product code or dependencies, start a server, call a model, create
runtime artifacts, commit, push, publish, or deploy. The later Owner-authorized
construction session is recorded below as append-only execution evidence.

## Product outcome

Complete the smallest usable text-first product loop:

```text
authorized timestamped transcript
  -> Topic Mapper semantic proposal
  -> deterministic Topic Resolver
  -> Report Planner semantic proposal
  -> deterministic V0 compiler
  -> current text-first report.html
  -> localhost Web UI
  -> select source, start run, observe state, open report
```

The Goal deliberately does not automate images. V1-B keyframes are no longer
on the immediate critical path. V1-C MP4/ASR composition also remains deferred.

## User-visible success

At completion, the local Owner can open one localhost page, select one of the
three authorized transcript fixtures, start a fresh report run, see its current
stage and terminal outcome, and open the rendered report without using the CLI.
The API key remains server-side. Every click creates or resolves exactly one
auditable run identity; failures stay visible and no partial report is labeled
successful.

## Fixed scope

### Text runtime closure

- Keep Topic Mapper and Report Planner as two independent sequential semantic
  calls over the complete authorized transcript.
- Keep semantic-v2 proposals, non-semantic normalization only, deterministic
  source binding/compiler, empty `assets.json`, and the existing V0 renderer.
- Do not alter the frozen Mapper/Planner prompts, semantic proposal shapes,
  compiler semantics, block budgets, content density, or renderer design merely
  to improve provider completion.
- Preserve all historical failures, runs, manifests, review packages, rubrics,
  screenshots, and commits. New evidence uses new IDs and paths.

### Local Web MVP

- One local Owner, one process, one active generation run, localhost only.
- The browser selects an allowlisted `video_id`; it never submits arbitrary
  filesystem paths or transcript bodies.
- The initial allowlist contains exactly:
  `p0b-kling-2024`, `p0b-rlinf-2026`, and `p0b-wuyi-goals`.
- The server resolves those IDs to the existing read-only manifest/transcript
  pairs and invokes the same V1-A runtime used by the CLI.
- `run.json` and the existing run directory remain canonical state/artifact
  authority. The Web layer must not create a competing job/report model.
- Secrets remain in the local server environment and are never serialized to
  HTML, JavaScript, API responses, logs, screenshots, or report artifacts.
- No frontend framework is required. The implementer may choose the smallest
  project-owned browser surface compatible with this repository. A new
  dependency requires a concrete need, normal lockfile update, and regression
  evidence; architecture work for its own sake is prohibited.

## Frozen Provider configuration

The next real revision must use exactly:

| Parameter | Required value |
|---|---|
| Provider | `https://api.deepseek.com` |
| Model | `deepseek-v4-flash-vision-exp` |
| API | OpenAI-compatible Chat Completions |
| Response envelope | `response_format={"type":"json_object"}` |
| Thinking | `extra_body={"thinking":{"type":"enabled"}}` |
| Reasoning effort | `high` |
| Output ceiling | `max_tokens=32768` |
| SDK retry | `0` |
| Application retry | At most one identical, explicit, retained retry per pipeline run |
| Temperature | May be sent/recorded for compatibility, but must not be used as stability evidence because Thinking mode ignores it |

The manifest and attempt trace must record the submitted values rather than
static intentions. A request mock/spy must prove that the actual SDK call
contains the Thinking, effort, and token fields above. Snapshot/request drift is
a configuration failure and blocks real calls.

DeepSeek currently documents a maximum output above 32,768 tokens for this
model family. Capability documentation is admission evidence only; the real
attempt trace remains authoritative for accepted parameters, usage, and finish
behavior.

## Provider call and cost boundary

| Work | Runs | Base calls | Retry ceiling | Maximum calls |
|---|---:|---:|---:|---:|
| New three-video text set | 3 | 6 | 3 | 9 |
| Provider-free Web/API/browser checks | N/A | 0 | 0 | 0 |
| One real Web-trigger smoke on Kling | 1 | 2 | 1 | 3 |
| Goal maximum | 4 | 8 | 4 | 12 |

The Web smoke identity is predeclared before the first real call and is not part
of the three-video product-quality denominator. It exists only to prove the
actual browser-to-runtime path on the previously failing fixture. It uses the
same frozen tuple and prompt/compiler revision; it cannot be tuned separately.

The maximum allocated output-token ceiling is `12 × 32768 = 393216` tokens.
Actual usage may be lower and must be recorded per attempt. Do not invent a
currency cost when no frozen authoritative price snapshot is included.

## Continuous Goal plan

### G0 — Baseline, preservation, and contract synchronization

1. Read `AGENTS.md`, `docs/visual-report/V0-STATUS.md`,
   `docs/visual-report/V1A-STATUS.md`, the current V1-A requirements package,
   `VISUAL-REPORT-V1A-CONTRACT-SIMPLIFICATION.md`, and this card.
2. Verify the expected branch/HEAD and inspect the worktree. Preserve unrelated
   or Owner-owned changes; do not reset or reinitialize anything.
3. Inventory all existing semantic-v2 product runs and review packages. Record
   that they are immutable historical evidence.
4. Synchronize future-facing configuration facts without rewriting historical
   manifests or claiming that old runs used the new tuple.

### G1 — Provider request correction and provider-free admission

1. Make the smallest provider-adapter/configuration change that sends the
   frozen Thinking/high/32768 tuple.
2. Ensure the public run/call snapshot reports actual submitted controls.
3. Add or update focused tests for:
   - exact Chat Completions request shape;
   - snapshot/request equality;
   - Thinking-mode usage fields and `finish_reason` capture;
   - identical-request retry hash;
   - one-retry exhaustion;
   - malformed/empty/incomplete JSON;
   - successful and failed `0/0` replay.
4. Run targeted V1-A tests, Ruff, V0 renderer regression, full pytest, diff
   hygiene, and protected-path checks before any real call.
5. Automatically repair ordinary in-scope defects until these provider-free
   gates pass. Do not alter prompts or semantic/compiler contracts to make them
   pass.

### G2 — Freeze and execute one new complete three-video text set

1. Freeze one new revision containing exact provider/model/API/request fields,
   prompt/compiler/schema hashes, source hashes, review-card revisions, three
   product run IDs, and the later Kling Web-smoke ID.
2. Execute Kling, RLinf, and Wu Yi exactly once each. Continue the complete set
   after an individual failure when credentials and configuration remain
   available.
3. Each run may spend its one identical technical retry only under the current
   eligible categories. Never retry valid but weak semantic output.
4. Retain every raw attempt, usage record, finish reason, normalized proposal,
   compiler ledger, state, error, plan, report, and screenshot produced.
5. Do not replace a failed identity, selectively rerun one video, change the
   prompt/configuration, or begin a second product revision inside this Goal.

### Gate A — Text path

The Web implementation may begin only if all three new product identities:

- reach `RENDERED`;
- contain a valid canonical Topic Map and V0 `ReportPlan`;
- use empty current asset manifests;
- have valid final source references and no major unsupported metric detected
  by deterministic checks;
- contain no semantic normalization rewrite/merge/split/synthesis event;
- retain exact call/retry/usage evidence; and
- produce reviewable desktop/mobile HTML evidence without critical overflow.

This gate proves technical product-loop admission, not repeat stability or
Owner semantic acceptance. Human content rubrics remain pending until the final
combined review.

If any product identity does not render, skip all Web construction and stop at
the matching terminal state below.

### G3 — Implement the local Web MVP

Implement the smallest local surface with these observable contracts:

| Route/operation | Contract |
|---|---|
| `GET /visual-report/` | Single responsive page with source selection, generate action, current state, failure details, and report viewer/link |
| `GET /api/visual-report/sources` | Return only allowlisted IDs plus non-sensitive title/duration/segment metadata |
| `POST /api/visual-report/runs` | Accept `video_id` and client request ID; create one unique run or return the existing run for an identical duplicate request |
| `GET /api/visual-report/runs/{run_id}` | Return canonical state/stage, call/retry counts, safe error category, and report URL only when `RENDERED` |
| `GET /visual-report/runs/{run_id}/report` | Serve only the canonical local `report.html` belonging to that known run |

Required behavior:

- bind to `127.0.0.1` by default and do not expose a remote/public host mode;
- validate `video_id`, `run_id`, and request ID; prevent traversal and arbitrary
  artifact reads;
- allow one active run; a different concurrent request returns a visible
  `RUN_ACTIVE` conflict without a provider call;
- prevent double-click/network replay from creating duplicate paid calls;
- do not make model calls on page load, refresh, report open, or status polling;
- closing or refreshing the browser does not cancel the server-side run; the
  user can reopen it from its run ID while the local server remains available;
- show `CREATED`, `MAPPING`, `TOPIC_MAPPED`, `PLANNING`, `PLAN_VALIDATED`,
  `RENDERED`, `FAILED`, and `CANCELLED` using mappings from canonical state;
- never show a report URL for a failed, incomplete, or cancelled run;
- make the primary flow usable at approximately 1080 px and 390 px, with
  keyboard-operable controls, visible focus, status text not conveyed by color
  alone, and no horizontal overflow;
- reuse the current report HTML unchanged; do not redesign content density or
  renderer components in this Goal.

No database, queue, account/auth system, upload service, arbitrary-path API,
service worker, cloud storage, analytics, telemetry, or deployment is allowed.

### G4 — Prove the Web loop and close evidence

1. Provider-free contract/integration tests prove the API, single-active-run,
   duplicate request, failure mapping, secret redaction, traversal rejection,
   and success/failure replay paths with `0/0` calls.
2. Browser-check the responsive UI against a retained successful real report at
   1080 px and approximately 390 px.
3. From the real browser UI, start the predeclared Kling Web-smoke identity once
   under the same frozen tuple. It may use its one identical technical retry.
4. Require the UI status to match `run.json`, then open the resulting report in
   the Web surface and inspect it at both viewports.
5. Run targeted Web/V1-A checks, full pytest, Ruff, `git diff --check`, V0
   renderer regression, replay checks, and protected/history preservation.
6. Update this card, V1-A status, the new combined review evidence, and any
   operator instructions needed to start/stop the local Web surface.
7. Stop for Owner review. Do not self-record V1-A or Web acceptance.

## Automatic repair and immutable-freeze rules

- Before the first real call, ordinary adapter, state, test, local Web, and
  documentation defects may be repaired automatically within this card.
- After the real revision is frozen, provider inputs and semantic contracts are
  immutable. A defect whose fix changes provider input, prompt, model, token or
  reasoning controls, compiler semantics, or source snapshots invalidates the
  set and stops; it does not silently begin another revision.
- Provider-free Web defects discovered after the 3/3 text gate may be repaired
  and retested without new model calls when they do not alter the planning
  runtime or retained outputs.
- Never normalize incomplete JSON into success, continue a truncated response,
  add a second retry, fall back to another model/provider, or create a manual
  report inside an automated run.

## Terminal states

| Condition | Required terminal |
|---|---|
| Credentials, balance/quota, permissions, network, or documented model access prevents execution | `READY_FOR_OWNER_V1_REVIEW — EXTERNAL_BLOCKED` |
| Provider rejects Thinking/high/32768 or the request cannot be proven equal to the frozen snapshot | `READY_FOR_OWNER_V1A_REVIEW — PROVIDER_CONFIGURATION_REJECTED` |
| Any of the three product runs exhausts its retry on transport/empty/truncated/malformed output | `READY_FOR_OWNER_V1A_REVIEW — TEXT_RUNTIME_INCONCLUSIVE` |
| Provider transport succeeds but semantic content cannot compile without prohibited repair | `READY_FOR_OWNER_V1A_REVIEW — TEXT_CONTENT_INSUFFICIENT` |
| A post-freeze fix would change provider input, semantics, compiler behavior, or source snapshot | `READY_FOR_OWNER_V1A_REVIEW — PRODUCT_SET_INVALID` |
| Text gate passes but local Web work requires excluded infrastructure/product scope | `READY_FOR_OWNER_V1_WEB_REVIEW — WEB_CONTRACT_CHANGE_REQUIRED` |
| Text gate and provider-free Web checks pass but the real Web Kling smoke exhausts its retry | `READY_FOR_OWNER_V1_WEB_MVP_REVIEW — WEB_RUNTIME_INCONCLUSIVE` |
| Text 3/3, Web real smoke, regressions, responsive checks, and review package all pass | `READY_FOR_OWNER_V1_WEB_MVP_REVIEW — TEXT_AND_WEB_LOOP_READY` |

An ordinary implementation/test defect is not a terminal until the Goal has
attempted an in-scope repair. Provider/model behavior after the bounded retry is
evidence, not permission for an unbounded repair loop.

## Required evidence

- clean baseline record and protected historical artifact inventory;
- request-shape and snapshot-equality tests for Thinking/high/32768;
- one frozen revision with three product IDs and one separate Web-smoke ID;
- exact attempt/call/token/finish/retry ledger and maximum-call audit;
- three new canonical text reports plus their review evidence;
- local Web API contract, state mapping, fake/replay integration evidence, and
  real Web-smoke run;
- desktop/mobile screenshots of the Web shell and opened report;
- full test/Ruff/diff/V0/protected-path results;
- updated status/task/operator docs;
- pending Owner content/Web rubrics with no fabricated score.

## Explicit non-goals

- content-density or report-style redesign;
- prompt tuning, per-video branches, a second model/provider, or formal six-run
  repeat measurement;
- MP4 upload, FFmpeg/ASR orchestration, keyframe candidate extraction,
  Asset Resolver, OCR/VLM, image captions/assets, V1-B, or V1-C;
- Agent, LangGraph, tools/MCP, RAG/vector search, database, durable queue,
  accounts, multi-user concurrency, cloud hosting, deployment, public sharing,
  PDF/PNG publishing, analytics, billing, or commercial service controls.

## Commit and publication boundary

Do not commit, push, create a PR, publish, or deploy unless the Owner separately
asks. Local real transcript/report/media rights remain unchanged. Never expose
the restricted RLinf media or report through a non-loopback interface.

## Construction-session handoff

The future construction session should execute this entire bounded Goal in one
continuation, automatically repair ordinary in-scope defects, avoid routine
Owner checkpoints, and stop only at one terminal state above. It must not treat
the Web slice as authorization for V1-B/V1-C or treat a green technical run as
Owner content acceptance.

## Construction-session execution evidence — 2026-08-31

The Owner explicitly authorized this entire bounded Goal, including the
provider-free checks, DeepSeek calls, local loopback surface, browser checks,
runtime evidence, and status-document updates. The Goal stopped at the first
applicable non-Web terminal after the complete frozen product set was executed.

### G0/G1 — preservation and provider-free admission

- Baseline remained branch `codex/visual-report-semantic-v2` at
  `844978f08d07775b650467e31e221a969ddef3e3`. Existing requirement-document
  edits, historical manifests, failed runs, review packages, rubrics, and
  screenshots were preserved; no protected `eval/`, `artifacts/p0b-ingest/`,
  answering, or retrieval path was changed.
- The historical V1 provider path remains unchanged. The current semantic-v2
  provider now constructs one exact Chat Completions request containing model,
  system message plus full transcript payload, `temperature=0`,
  `max_tokens=32768`, `response_format={"type":"json_object"}`,
  `reasoning_effort="high"`, and
  `extra_body={"thinking":{"type":"enabled"}}`; SDK retries remain zero.
- Provider-free semantic-v2 checks passed: `10` focused tests, including public
  snapshot equality, request-shape/hash equality, one-retry exhaustion,
  malformed and incomplete output retention, and `0/0` replay. Full regression
  passed `79` tests when run with the canonical checkout as the read-only source
  root; full Ruff and `git diff --check` passed. The worktree-only full test
  attempt had `76` passes and the three expected historical-source misses before
  the canonical-source rerun.
- Provider-free loopback Web contract tests passed `5`; they covered the exact
  allowlist, page/API no-call behavior, duplicate request reuse, one active run,
  safe failure/report mapping, secret redaction, and traversal rejection. These
  tests used fake providers only and consumed `0` external calls.

### G2 — one frozen revision and the complete three-video product set

The new append-only manifest is
`eval/visual-report-v1a/text-web-closure-007-product-manifest.json` with
revision `vr1a-semantic-v2-56340249c6f9` and manifest SHA-256
`d14211b92fb3b09d4b40e404bdd714b7ab4a916c13b542ad8fc8cb1628c9cb78`.
It records exact provider/request controls, prompt/schema/compiler/runtime
evidence, source hashes, review-card hashes, three product identities, and the
separate predeclared Web smoke identity
`p0b-kling-2024-semantic-v2-98d9af23a9-web-smoke`. No second product revision
was created.

| Video | Run result | Calls | Retained evidence |
|---|---|---:|---|
| `p0b-kling-2024` | `RENDERED` | `2/2` | Mapper and Planner both `finish_reason=stop`; usage, raw responses, request hashes, empty assets, report, and run state retained |
| `p0b-rlinf-2026` | `RENDERED` | `2/2` | Mapper and Planner both `finish_reason=stop`; 5 sections / 11 blocks, source lineage, empty assets, report, and run state retained |
| `p0b-wuyi-goals` | `FAILED — PLAN_BUDGET_ERROR` | `2/2` | Mapper and Planner both `finish_reason=stop`; compiler rejected the model-selected plan at more than 14 blocks; raw responses, usage, failure, and no-report state retained |

The product denominator observed `6/6` provider/model calls, all base calls,
with no technical retry used. The predeclared Web smoke remained unexecuted
(`0/3`); Goal usage was therefore `6/12`. The Kling run's event ledger retains
an operator cancellation marker that was appended while its already-admitted
Planner request was still completing; its final canonical `run.json` is
`RENDERED`, `2/2`, `retry_used=false`, with two successful call records. The
marker is preserved rather than deleted or relabeled.

The retained attempt token totals were Kling `15803/19506` (Mapper/Planner),
RLinf `20754/25788`, and Wu Yi `15795/23303`, for `120949` total tokens across
the six product calls. Every provider attempt recorded `finish_reason=stop`.

The append-only review package is
`artifacts/visual-report/v1a/evaluation/text-web-closure-007/vr1a-semantic-v2-56340249c6f9/`.
Its aggregate records `technical_status=FAILED`,
`stop_state=PROTOTYPE_CONTENT_INSUFFICIENT`, observed calls `6/6`, and three
pending Owner rubrics. This is technical evidence, not semantic acceptance.

### Gate A / G3 / G4 terminal

Gate A requires all three product identities to reach `RENDERED`; Wu Yi did not.
Its provider transport succeeded, but the existing deterministic V0 compiler
rejected more than fourteen blocks. Deleting blocks, changing prompts, tuning a
video, adding a third call, or rerunning the identity was prohibited, so the
matching terminal is:

`READY_FOR_OWNER_V1A_REVIEW — TEXT_CONTENT_INSUFFICIENT`

Because Gate A failed, the Web MVP was not admitted for real execution: no
loopback server was started, no browser session or screenshots were created for
this Goal, and the predeclared Kling Web smoke received no provider call. The
Web code and provider-free contract tests remain local, unaccepted engineering
changes; they do not constitute a Web runtime proof or Owner acceptance. No
MP4/ASR, keyframe, OCR/VLM, V1-B, V1-C, database, queue, account, deployment,
public hosting, commit, push, PR, or publication was performed.

The Owner must review the retained successful reports and the Wu Yi failure,
then separately authorize any new revision or Web attempt. This task records
no Owner acceptance.
