# VR-V1-URL-INGEST-LOCAL-MVP-011 — Public Bilibili URL Local Closure

## Task metadata

| Field | Value |
|---|---|
| Task ID | `VR-V1-URL-INGEST-LOCAL-MVP-011` |
| Target grade | `G1 PROTOTYPE` |
| Frozen baseline | branch `visual-report`, commit `ba7d851` |
| Authorization | Scope approved; execution reserved for a separately published Goal session |
| Task status | `DOCUMENTATION_HANDOFF_READY — IMPLEMENTATION_NOT_STARTED` |
| Required stop | `READY_FOR_OWNER_V1_URL_LOCAL_MVP_REVIEW` |

## Objective

Connect exactly one new local path:

```text
public single Bilibili BV URL
→ yt-dlp download
→ existing video-evidence ingest
→ existing semantic-v2 visual-report build
→ existing canonical report.html shown by the loopback Web surface
```

This is a wiring task. It does not revise the frozen Task 010 planning,
compiler, renderer, adaptive-budget, provider, or report-content contracts.
This document is a handoff only; its publication performs no construction or
external call.

## Owner-confirmed boundary

- Accept a public `https://www.bilibili.com/video/BV...` URL and normalize it
  before download, retaining only the BVID and an optional numeric `p` value.
- Download one video only; pass `--no-playlist` and do not load user or system
  yt-dlp configuration.
- Use the existing local `video-evidence ingest` command and its current
  FFmpeg/MLX Whisper path. Do not add or replace an ASR backend.
- Use the existing `build_from_transcript_v2` runtime and V0 renderer unchanged.
- Keep one active in-memory Web run and unique local run directories.
- Keep downloaded media, ingest artifacts, planning artifacts, and the final
  report inside the run directory for local inspection and manual deletion.
- Bind the Web server to `127.0.0.1` only.

## Explicit exclusions

- No Planner, normalizer, compiler, typed-block, renderer, prompt, model, or
  adaptive-budget redesign.
- No database, durable queue, multi-worker scheduler, account, authentication,
  Cookie login, browser-cookie extraction, playlist, multi-part orchestration,
  short-link expansion, upload, multi-platform input, cloud deployment, public
  hosting, new ASR provider, keyframes, OCR, VLM, Agent, LangGraph, or RAG.
- No V1-B or broader production-hardening work.

## Decision and authority boundary

| Decision class | Authority in Task 011 |
|---|---|
| Frozen by Owner | Single public canonical BV URL, yt-dlp, existing ingest, existing semantic-v2 report path, loopback Web, one active run, local artifacts, and the exclusions above |
| Delegated to the construction Goal | The smallest compatible module/function split, targeted test shape, and final URL-Web CLI command name, provided every acceptance criterion and exclusion remains unchanged |
| Automatic repair allowed | Ordinary in-scope wiring defects and test failures, subject to the bounded real-run rule below |
| Owner-only change | Cookies/login, another platform/downloader/ASR/provider, new dependencies not required by an observed in-scope defect, Planner/Renderer/content changes, database/queue, public deployment, or a broader product contract |
| Owner-only acceptance | Report content quality, semantic quality, layout quality, public-release approval, and progression beyond this local MVP |

This card records an approved scope and a publishable construction Goal. It is
not an independent requirements-readiness certification and does not start the
implementation by itself.

## Minimal contracts

### URL admission

- Scheme must be `https`.
- Host must be `www.bilibili.com` or `bilibili.com`.
- Path must contain exactly one `BV` identifier in `/video/<BVID>` form.
- The server canonicalizes the accepted input to
  `https://www.bilibili.com/video/<BVID>/[?p=<digits>]` before invoking yt-dlp.
- Any rejected URL fails before a run directory, download, ingest, or model call.

### Download adapter

The project calls the installed `yt-dlp` executable with an argument array, not
through a shell. The frozen option set is:

```text
--ignore-config
--no-playlist
-P <run-dir>/download
-o source.%(ext)s
-S res:1080,vcodec:h264,acodec:aac
--merge-output-format mp4
--write-info-json
--print after_move:filepath
<canonical-url>
```

The adapter validates the final media path is inside the run download
directory and reads the generated info JSON for title/uploader attribution.
Missing executable, non-zero exit, missing media, or invalid metadata fails
visibly; no fallback downloader or Cookie mode is attempted.

### Existing ingest composition

Invoke the existing module CLI with the downloaded media, a deterministic
`bilibili-<BVID>` video ID, the run-local ingest root, canonical source URL,
and source attribution. Success requires the existing `manifest.json` and
`segments.jsonl`; the Task does not duplicate ASR or segment-building code.

### Intelligence and deterministic boundary

Task 011 adds no new model decision or intelligence layer. URL admission,
download invocation, path checks, run state, and composition are deterministic.
The only model behavior remains the already implemented two-stage DeepSeek
Mapper/Planner path. A provider-free test double proves the wiring contract but
is not evidence of report quality and is never exposed as a product fallback.
The manual comparison path is the same media passed through the existing ingest
and visual-report CLIs; Task 011 only removes that manual handoff.

### Web state

The canonical planning `run.json` remains unchanged. Before planning starts,
the Web layer exposes only two additional display stages in memory:
`DOWNLOADING` and `TRANSCRIBING`. Planning then exposes its existing states.
Failures use the existing terminal `FAILED` state with one safe category:
`URL_INVALID`, `DOWNLOAD_ERROR`, or `INGEST_ERROR` as applicable.

### Data lifecycle and disclosure

| Data | Destination and retention |
|---|---|
| Submitted public BV URL and yt-dlp metadata | Stored only in the local run evidence needed for inspection |
| Downloaded media, extracted audio, and ASR artifacts | Stored under the unique local run directory; never uploaded or published by Task 011 |
| Complete generated transcript | Sent only to the already configured DeepSeek endpoint for the existing Mapper and Planner calls after ingest succeeds |
| Planning artifacts and `report.html` | Stored under the same local run directory and served only from `127.0.0.1` |
| Cleanup | No automatic deletion in this prototype; the Owner may manually delete the run directory after review |

Credentials remain server-side environment configuration and must never appear
in browser payloads, logs, safe errors, task evidence, or committed files.

## Allowed change scope

- `src/video_evidence_agent/visual_report/url_ingest.py`
- minimal composition changes in
  `src/video_evidence_agent/visual_report/web.py` and
  `src/video_evidence_agent/visual_report/__main__.py`
- targeted tests under `tests/`
- this task card and `docs/visual-report/V1A-STATUS.md`

Do not modify Task 010 historical artifacts or frozen Task 008/009 evidence.

## Current local prerequisites

Read-only inspection on the frozen baseline found:

| Item | Current evidence |
|---|---|
| Branch / baseline | `visual-report` / `ba7d8512699ad04f5a9137bb9cfb7e62971263b2` |
| yt-dlp | `/opt/homebrew/bin/yt-dlp`, version `2026.08.19` |
| FFmpeg / ffprobe | `/opt/homebrew/bin/ffmpeg`, `/opt/homebrew/bin/ffprobe` |
| Existing ASR | Current `video-evidence ingest` MLX Whisper implementation |
| Existing report path | Current semantic-v2 `build_from_transcript_v2` and V0 renderer |
| Existing Web boundary | Fixed three-source allowlist; no URL/download/ingest orchestration yet |
| Artifact hygiene | `artifacts/` and `*.mp4` are already ignored by Git |

These are checkout-time facts, not deployment guarantees. The construction
session must recheck command availability without installing or upgrading
anything unless a missing prerequisite is the observed blocker and the Owner
separately authorizes that change.

## Delivery slices

### S0 — Admission and preservation

- Verify branch `visual-report`, baseline ancestor `ba7d851`, dirty state, and
  Task 010 preservation.
- Re-read this card plus the V1-A/V0 status and engineering contracts required
  by `AGENTS.md`.
- Confirm yt-dlp, ffmpeg, ffprobe, the current uv environment, and only the
  presence—not the value—of required provider configuration.
- Do not call Bilibili or the model in S0.

### S1 — URL/download adapter

- Add the smallest project-owned adapter for URL validation and the frozen
  yt-dlp argv contract.
- Use an argv list with `shell=False`; never concatenate the submitted URL into
  a shell command.
- Return structured BVID, canonical URL, final media path, title, uploader, and
  attribution. Preserve a safe download failure without attempting Cookies or
  another extractor path.

### S2 — Existing-pipeline composition

- Invoke the existing `video-evidence ingest` surface rather than copying its
  FFmpeg, MLX Whisper, or segmentation implementation.
- Pass the resulting run-local manifest and segments into the existing
  semantic-v2 builder.
- Reuse the current provider configuration, two-stage Mapper/Planner behavior,
  one existing technical retry, compiler, empty-assets behavior, and renderer.
- Do not change any prompt, schema, budget, block mapping, or HTML/CSS.

### S3 — URL Web mode

- Add a separate local URL-input mode/command so the frozen fixed-source Web
  mode continues to behave as before.
- Accept `{url, client_request_id}`, display the two pre-planning stages, then
  map to existing planning states and the canonical report endpoint.
- Keep one in-memory active run, duplicate-request reuse, traversal protection,
  server-side credentials, and `127.0.0.1` binding.

### S4 — Verification and local review handoff

- Complete provider-free unit/contract/integration/failure tests first.
- Re-run the existing fixed-source Web and V0 regressions.
- Then exercise one Owner-supplied public BV URL through the actual browser
  page when prerequisites permit. This external execution authorizes the
  transcript derived from that public video to be sent only to the existing
  configured DeepSeek endpoint for the current Mapper and Planner stages.
- Preserve any failed run. Do not tune content or layout in response.
- Leave the successful localhost command and report link ready for Owner review.

## Suggested artifact layout

```text
artifacts/visual-report/url-ingest/<run-id>/
├── run.json / events.jsonl / model-calls.jsonl
├── download/
│   ├── source.<media-ext>
│   └── source.info.json
├── ingest/<video-id>/
│   ├── manifest.json
│   ├── segments.jsonl
│   ├── asr.json
│   └── audio.wav
├── topic-map*.json / report-plan*.json / normalization*.json
├── assets.json
└── report.html
```

Exact filenames already owned by ingest or visual-report must remain those
components' existing names. Do not create a second canonical plan or report.

## Acceptance

1. Existing fixed-source Web behavior and tests remain green.
2. URL validation rejects non-HTTPS, non-Bilibili, non-BV, and extra request
   shapes before any side effect.
3. A provider-free integration test proves download adapter → existing-ingest
   boundary → existing semantic-v2 build → canonical report while faking only
   the external download, ASR execution, and model boundaries.
4. Duplicate request IDs reuse the same run; a second active URL is rejected.
5. Download, ingest, and planning failures expose safe categories and no
   credential or transcript body.
6. Ruff, targeted tests, full tests, V0 renderer regression, and
   `git diff --check` pass.
7. One Owner-supplied public BV URL is exercised locally when network, yt-dlp,
   FFmpeg, cached/available MLX model, and DeepSeek configuration permit it.
   An external/configuration block is reported honestly and does not trigger
   scope expansion.

## Stop rule

Stop at `READY_FOR_OWNER_V1_URL_LOCAL_MVP_REVIEW`. Do not commit Task 011,
push, deploy, record content acceptance, or begin content/layout improvement
unless the Owner separately requests it.

## Terminal matrix

| Condition | Exact terminal |
|---|---|
| One public BV completes download → ingest → existing visual-report → browser report | `READY_FOR_OWNER_V1_URL_LOCAL_MVP_REVIEW — PUBLIC_BV_LOOP_READY` |
| Bilibili/network/yt-dlp/provider/credential/model access prevents the real run after code/tests pass | `READY_FOR_OWNER_V1_URL_LOCAL_MVP_REVIEW — EXTERNAL_BLOCKED` |
| An in-scope implementation defect remains after bounded automatic repair | `READY_FOR_OWNER_V1_URL_LOCAL_MVP_REVIEW — IMPLEMENTATION_INCOMPLETE` |
| Continuing requires Cookies, another platform/ASR/provider, Planner/Renderer changes, database/queue, or deployment | `READY_FOR_OWNER_V1_URL_LOCAL_MVP_REVIEW — SCOPE_CHANGE_REQUIRED` |

Ordinary in-scope engineering errors may be diagnosed and fixed continuously
within the construction Goal. Provider-free checks may be rerun as needed. Do
not loop real external executions: after the first real end-to-end attempt, at
most one fresh rerun is allowed only for a demonstrated wiring defect; preserve
both run directories. The existing one-retry planning rule remains inside each
run and no additional model-repair call is introduced.

## Construction-session verification

```bash
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run ruff check .
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q tests/test_visual_report_url_ingest.py
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q tests/test_visual_report.py
git diff --check
```

The implementation must expose a concise loopback launch command equivalent to:

```bash
NO_PROXY=api.deepseek.com \
no_proxy=api.deepseek.com \
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache \
uv run python -m video_evidence_agent.visual_report serve-url-web \
  --artifact-root artifacts/visual-report/url-ingest \
  --port 8765
```

The exact new command name may differ only when the existing CLI structure
demonstrably requires a smaller compatible shape; record the final command.

## Documentation-session evidence

- Task 010 baseline committed as `ba7d851` after Ruff passed and the full suite
  passed `93` tests with localhost binding permitted.
- This documentation session made no product-code, dependency, runtime-data,
  infrastructure, download, provider/model, browser, commit, push, or deployment
  change after that freeze.
- Task 011 implementation and external execution remain `NOT_STARTED`.

## Copy-ready Goal text

The Owner should publish the following in a new local, same-checkout session:

```text
/goal

在 /Users/tristana/Develop/video-evidence-agent 的当前 visual-report 分支上，
完整执行 docs/tasks/VISUAL-REPORT-V1-URL-INGEST-LOCAL-MVP.md 定义的
VR-V1-URL-INGEST-LOCAL-MVP-011。

冻结基线是 ba7d8512699ad04f5a9137bb9cfb7e62971263b2。先保留并核对当前工作树，
不得覆盖本任务文档或任何既有失败/测量/Task 008–010 证据。

目标严格限定为：公开单个 Bilibili BV URL → yt-dlp 下载 → 调用现有
video-evidence ingest → 调用现有 semantic-v2 visual-report → 在 127.0.0.1
Web 页面展示 canonical report.html。

实现最小接线即可。不要重构或调整 Topic Mapper、Report Planner、Normalizer、
Compiler、adaptive budget、V0 Renderer、Prompt、模型或内容排版；不要引入数据库、
队列、Cookie/登录、合集、多平台、上传、关键帧、OCR/VLM、Agent、LangGraph、RAG、
云部署、公开托管或新的 ASR 后端。状态管理保持一个进程、一个 active run、独立
本地 run 目录。

先完成全部 provider-free 测试与现有 Web/V0 回归，再用 Owner 提供的公开 BV URL
做一次真实浏览器端到端验证。Owner 授权把该公开视频产生的完整 transcript 仅发送
给当前已配置的 DeepSeek Mapper/Planner 两阶段；继续沿用现有一次相同请求技术重试，
不得增加模型修复调用或 fallback。运行 DeepSeek 子进程时保留
NO_PROXY=api.deepseek.com 和 no_proxy=api.deepseek.com。

普通范围内工程错误在一个连续 Goal 中自动诊断、修复和验证，不请求中间 checkpoint。
第一轮真实端到端失败后，只允许在确认属于接线缺陷时保留失败 run 并再做一次全新 run；
外部网络、Bilibili、yt-dlp、凭据、权限、模型访问或任何需要扩大范围的情况直接按任务卡
terminal matrix 停止。

完成后更新任务卡证据和 docs/visual-report/V1A-STATUS.md，给出本地启动命令、
localhost URL、run ID、下载/ingest/report 路径、调用次数和测试结果。停在
READY_FOR_OWNER_V1_URL_LOCAL_MVP_REVIEW，不 commit、不 push、不部署、不记录内容质量
acceptance，也不开始后续内容、语义或排版优化。
```

## Construction-session evidence — 2026-08-31

This append-only section records the completed construction Goal. The earlier
documentation-session evidence and all Task 008–010 evidence remain preserved.

- Baseline and preservation: branch `visual-report`, frozen baseline
  `ba7d8512699ad04f5a9137bb9cfb7e62971263b2`; the pre-existing dirty
  `docs/visual-report/V1A-STATUS.md` change and this task card were retained.
  No Task 008–010 artifact, failure, measurement, evaluator, or acceptance
  record was overwritten.
- Implementation scope: added the bounded Bilibili URL/download adapter,
  existing-ingest composition, separate URL Web command/page, minimal display
  stages, and targeted provider-free tests. Topic Mapper, Report Planner,
  Normalizer, Compiler, adaptive budget, V0 Renderer, prompts, model
  configuration, and content layout were not changed.
- Provider-free verification: Ruff passed; Task 011 targeted tests passed
  `5 passed`; full pytest passed `98 passed`; existing V0/Web regression passed
  `10 passed`; `git diff --check` passed.
- Local launch command and URL:

  ```bash
  NO_PROXY=api.deepseek.com \
  no_proxy=api.deepseek.com \
  UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache \
  uv run python -m video_evidence_agent.visual_report serve-url-web \
    --artifact-root artifacts/visual-report/url-ingest \
    --port 8766
  ```

  `8765` was already occupied by the preserved static preview, so this Goal
  used `http://127.0.0.1:8766/visual-report/`.
- Real browser run: the existing Owner-confirmed public URL
  `https://www.bilibili.com/video/BV1RxWnzbE7g` was submitted through the URL
  page. The browser observed `DOWNLOADING` → `TRANSCRIBING` → `PLANNING` →
  `RENDERED`, then opened the canonical report endpoint in a browser tab.
- Run and artifacts: run ID
  `url-bilibili-BV1RxWnzbE7g-73fb6cd3f6c5`; download
  `artifacts/visual-report/url-ingest/url-bilibili-BV1RxWnzbE7g-73fb6cd3f6c5/download/source.mp4`
  and `source.info.json`; ingest
  `.../ingest/bilibili-BV1RxWnzbE7g/manifest.json` and
  `segments.jsonl`; canonical report
  `.../report.html`. The run ended `RENDERED` with no error.
- Provider/model evidence: exactly `2` provider/model calls, Mapper then
  Planner, both attempt 1, model
  `deepseek-v4-flash-vision-exp` at `https://api.deepseek.com`; the existing
  technical retry was not used. No additional model call or fallback ran.
- This is technical loop evidence only. No content-quality, semantic-quality,
  layout-quality, public-release, or Owner acceptance was recorded.

The exact Task 011 terminal is:

`READY_FOR_OWNER_V1_URL_LOCAL_MVP_REVIEW — PUBLIC_BV_LOOP_READY`

## Task 012 follow-up — local FIFO queue — 2026-08-31

The Owner's later explicit instruction supersedes only Task 011's active-run
rejection and no-queue statements for `serve-url-web`. URL submissions now
create unique retained run directories immediately and enter one in-memory
FIFO when another URL run is active. Only one worker executes at a time; a
terminal active run automatically starts the next item. This is not a durable
queue and does not resume queued work after process restart.

The browser/API display contract adds `stage=QUEUED`, `queue_position`, and
`active_run_id`. The waiting tab shows the active run and waiting position,
continues polling, and automatically advances through the existing download,
transcription, planning, and rendered states without another submission.

Verification completed with local fake boundaries only:

- URL targeted tests: `7 passed`;
- fixed-source plus URL Web regression: `12 passed`;
- full pytest: `102 passed`;
- Ruff and `git diff --check`: passed;
- two-tab browser review: the first tab showed active processing, the second
  showed `等待处理 / 排队第 1 位` and the active run ID, and both reached
  `报告已生成` automatically;
- external download/provider/model calls during this follow-up review: `0/0`.

No historical run, Task 011 real-loop evidence, Planner/Compiler/Renderer,
provider/model/retry contract, dependency, database, account, deployment, or
public-hosting boundary changed.
