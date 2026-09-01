"""Loopback-only Web MVP for the current semantic-v2 visual report runtime."""

from __future__ import annotations

import json
import re
import threading
import uuid
from collections import deque
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable
from urllib.parse import unquote, urlsplit

from ..transcript_foundation import OcrError, parse_roi
from .evaluation import FIXED_SOURCES, load_semantic_v2_product_freeze
from .planning import PlanningError
from .planning_runtime import (
    SEMANTIC_V2_CALL_SCHEMA_VERSION,
    SEMANTIC_V2_EVENT_SCHEMA_VERSION,
    SEMANTIC_V2_RUN_SCHEMA_VERSION,
    RunRecorder,
    build_from_transcript_v2,
    load_source,
)
from .url_ingest import (
    URL_INGEST_SCHEMA_VERSION,
    DownloadResult,
    IngestResult,
    UrlIngestError,
    download_bilibili_video,
    ingest_downloaded_video,
    validate_bilibili_url,
)

ALLOWED_VIDEO_IDS = tuple(video_id for video_id, _, _ in FIXED_SOURCES)
_SOURCE_PATHS = {
    video_id: (manifest_rel, segments_rel)
    for video_id, manifest_rel, segments_rel in FIXED_SOURCES
}
_SAFE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_MAX_REQUEST_BYTES = 16 * 1024
_TERMINAL_STATES = {"RENDERED", "FAILED", "CANCELLED"}

ProviderFactory = Callable[[], Any]
RunBuilder = Callable[..., Any]


@dataclass
class _WebRun:
    video_id: str
    client_request_id: str
    run_id: str
    recorder: RunRecorder
    input_url: str | None = None
    display_stage: str | None = None
    transcript_mode: str = "fused"
    ocr_mode: str = "auto"
    ocr_roi: str | None = None
    subtitle_file: str | None = None


def _safe_int(value: object) -> int:
    return value if isinstance(value, int) and value >= 0 else 0


def _safe_bool(value: object) -> bool:
    return value if isinstance(value, bool) else False


def _json_bytes(payload: object) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )


def _read_json(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PlanningError("OUTPUT_IO_ERROR", "run status is unavailable") from exc
    if not isinstance(payload, dict):
        raise PlanningError("OUTPUT_IO_ERROR", "run status is unavailable")
    return payload


def _run_relative_path(path: Path, run_dir: Path) -> str:
    """Keep run-local paths compact while allowing an explicit external input."""

    resolved_path = path.resolve()
    try:
        return str(resolved_path.relative_to(run_dir.resolve()))
    except ValueError:
        return str(resolved_path)


def _html_page() -> str:
    return r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Video Visual Report</title>
  <style>
    :root {
      color-scheme: dark;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    * { box-sizing: border-box; }
    html, body {
      margin: 0; min-height: 100%; background: #111827; color: #f8fafc;
      overflow-x: hidden;
    }
    body { padding: clamp(20px, 5vw, 72px) 16px; }
    main { width: min(760px, 100%); margin: 0 auto; }
    .eyebrow {
      color: #67e8f9; font-size: 12px; font-weight: 700; letter-spacing: .14em;
      text-transform: uppercase;
    }
    h1 {
      margin: 10px 0 12px; font-size: clamp(30px, 7vw, 56px);
      line-height: 1.05; letter-spacing: -.04em;
    }
    .intro { color: #cbd5e1; max-width: 620px; line-height: 1.65; }
    .card {
      margin-top: 28px; padding: clamp(18px, 4vw, 30px); border: 1px solid #334155;
      border-radius: 18px; background: #1e293b; box-shadow: 0 18px 50px #02061766;
    }
    label { display: block; margin-bottom: 9px; color: #cbd5e1; font-size: 14px; font-weight: 650; }
    select, button { width: 100%; min-height: 48px; border-radius: 11px; font: inherit; }
    select { border: 1px solid #475569; padding: 0 13px; color: #f8fafc; background: #0f172a; }
    button {
      margin-top: 16px; border: 0; padding: 0 18px; color: #082f49;
      background: #67e8f9; font-weight: 750; cursor: pointer;
    }
    button:disabled { cursor: wait; opacity: .52; }
    :focus-visible { outline: 3px solid #facc15; outline-offset: 3px; }
    .source-info {
      min-height: 24px; margin-top: 12px; color: #94a3b8; font-size: 13px;
      line-height: 1.5; overflow-wrap: anywhere;
    }
    .status { margin-top: 24px; padding-top: 20px; border-top: 1px solid #334155; }
    .status-title {
      display: flex; align-items: baseline; justify-content: space-between;
      gap: 12px; flex-wrap: wrap;
    }
    .status-label { color: #f8fafc; font-size: 18px; font-weight: 750; }
    .status-code {
      color: #67e8f9; font-size: 12px;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    }
    .status-detail { margin: 9px 0 0; color: #cbd5e1; line-height: 1.55; overflow-wrap: anywhere; }
    .report-link { display: inline-block; margin-top: 14px; color: #67e8f9; font-weight: 700; }
    [hidden] { display: none !important; }
    @media (max-width: 520px) {
      body { padding-top: 28px; }
      .card { margin-top: 22px; border-radius: 14px; }
      .status-title { display: block; }
      .status-code { display: block; margin-top: 5px; }
    }
  </style>
</head>
<body>
  <main>
    <div class="eyebrow">Video Visual Report</div>
    <h1>从完整文字到可追溯报告</h1>
    <p class="intro">选择一个已授权的视频。规划、编译和渲染会在本地连续运行，报告中的每个
      内容块都保留来源引用。</p>
    <section class="card" aria-labelledby="source-label">
      <label id="source-label" for="source">选择视频</label>
      <select id="source" name="video_id" aria-describedby="source-info"></select>
      <div id="source-info" class="source-info" aria-live="polite">正在读取已授权来源…</div>
      <button id="generate" type="button">生成 Visual Report</button>
      <div class="status" aria-live="polite" aria-atomic="true" aria-busy="false">
        <div class="status-title">
          <span id="status-label" class="status-label">尚未开始</span>
          <span id="status-code" class="status-code">READY</span>
        </div>
        <p id="status-detail" class="status-detail">页面加载和刷新不会触发模型调用。</p>
        <a id="report-link" class="report-link" href="#" target="_blank"
           rel="noreferrer" hidden>打开 canonical report.html</a>
      </div>
    </section>
  </main>
  <script>
    (() => {
      const source = document.querySelector('#source');
      const sourceInfo = document.querySelector('#source-info');
      const generate = document.querySelector('#generate');
      const statusBox = document.querySelector('.status');
      const statusLabel = document.querySelector('#status-label');
      const statusCode = document.querySelector('#status-code');
      const statusDetail = document.querySelector('#status-detail');
      const reportLink = document.querySelector('#report-link');
      const labels = {
        CREATED: '已创建 run', TRANSCRIBING: '正在生成文字稿', OCR: '正在识别字幕',
        FUSING: '正在融合文字稿', READY: '已完成', DEGRADED: '文字稿已降级但可继续',
        MAPPING: '正在映射主题', TOPIC_MAPPED: '主题已绑定',
        PLANNING: '正在规划报告', PLAN_VALIDATED: '计划已验证', RENDERED: '报告已生成',
        FAILED: '运行失败', CANCELLED: '运行已取消'
      };
      let currentRunId = null;
      let polling = false;

      function showStatus(data) {
        const state = data.state || 'UNKNOWN';
        const displayStage = data.stage || state;
        statusLabel.textContent = labels[displayStage] || '状态更新';
        statusCode.textContent = displayStage;
        statusBox.dataset.state = state;
        statusDetail.textContent =
          `模型调用 ${data.provider_calls ?? 0} 次；` +
          `技术重试 ${data.retry_used ? '已使用' : '未使用'}。` +
          (data.error_category ? ` 错误类别：${data.error_category}。` : '');
        reportLink.hidden = !data.report_url;
        if (data.report_url) reportLink.href = data.report_url;
        statusBox.setAttribute('aria-busy', !['RENDERED', 'FAILED', 'CANCELLED'].includes(state));
        if (['RENDERED', 'FAILED', 'CANCELLED'].includes(state)) {
          generate.disabled = false;
          polling = false;
        }
      }

      async function loadSources() {
        const response = await fetch('/api/visual-report/sources', {
          headers: { 'Accept': 'application/json' }
        });
        if (!response.ok) throw new Error('sources_unavailable');
        const data = await response.json();
        source.replaceChildren();
        for (const item of data.sources || []) {
          const option = document.createElement('option');
          option.value = item.video_id;
          option.textContent = item.title;
          option.dataset.duration = item.duration_ms;
          option.dataset.segments = item.segment_count;
          source.append(option);
        }
        updateSourceInfo();
      }

      function updateSourceInfo() {
        const option = source.selectedOptions[0];
        if (!option) { sourceInfo.textContent = '没有可用来源。'; return; }
        const duration = Math.round(Number(option.dataset.duration || 0) / 1000);
        sourceInfo.textContent =
          `${option.textContent} · ${duration} 秒 · ${option.dataset.segments} 个文字片段`;
      }

      async function pollRun() {
        if (!currentRunId || polling) return;
        polling = true;
        try {
          const response = await fetch(
            `/api/visual-report/runs/${encodeURIComponent(currentRunId)}`,
            { headers: { 'Accept': 'application/json' } }
          );
          if (!response.ok) throw new Error('run_unavailable');
          const data = await response.json();
          showStatus(data);
          if (!['RENDERED', 'FAILED', 'CANCELLED'].includes(data.state)) {
            polling = false;
            window.setTimeout(pollRun, 500);
          }
        } catch (error) {
          polling = false;
          statusLabel.textContent = '状态暂时不可用';
          statusCode.textContent = 'WEB_ERROR';
          statusDetail.textContent = '请保留当前页面并稍后重试。';
          generate.disabled = false;
        }
      }

      async function generateReport() {
        if (generate.disabled || !source.value) return;
        generate.disabled = true;
        reportLink.hidden = true;
        const clientRequestId = `web-${crypto.randomUUID ? crypto.randomUUID() :
          `${Date.now()}-${Math.random()}`}`;
        try {
          const response = await fetch('/api/visual-report/runs', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
            body: JSON.stringify({ video_id: source.value, client_request_id: clientRequestId })
          });
          const data = await response.json();
          if (!response.ok) throw new Error(data.error_category || 'run_rejected');
          currentRunId = data.run_id;
          showStatus(data);
          polling = false;
          pollRun();
        } catch (error) {
          statusLabel.textContent = '无法开始运行';
          statusCode.textContent = String(error.message || 'REQUEST_ERROR');
          statusDetail.textContent = '没有产生新的模型调用。请稍后重试。';
          generate.disabled = false;
        }
      }

      source.addEventListener('change', updateSourceInfo);
      generate.addEventListener('click', generateReport);
      loadSources().catch(() => {
        sourceInfo.textContent = '已授权来源读取失败。';
        generate.disabled = true;
      });
      const initialRunId = new URLSearchParams(window.location.search).get('run_id');
      if (initialRunId) { currentRunId = initialRunId; pollRun(); }
    })();
  </script>
</body>
</html>
"""


def _url_html_page() -> str:
    return r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Video Visual Report · Bilibili</title>
  <style>
    :root {
      color-scheme: light;
      font-family: "Avenir Next", "PingFang SC", "Microsoft YaHei", sans-serif;
      --ink: #172033; --muted: #667085; --line: #dce5f2; --blue: #4776ee;
      --pink: #ed72b6; --blue-soft: #eef4ff; --pink-soft: #fff0f8;
    }
    * { box-sizing: border-box; }
    html, body {
      margin: 0; min-height: 100%; color: var(--ink);
      background:
        radial-gradient(circle at 8% 5%, #eaf1ff 0, transparent 34%),
        radial-gradient(circle at 92% 18%, #ffedf7 0, transparent 30%), #f8fbff;
      overflow-x: hidden;
    }
    body { padding: clamp(20px, 5vw, 72px) 16px; }
    main { width: min(760px, 100%); margin: 0 auto; }
    .eyebrow {
      color: var(--blue); font-size: 12px; font-weight: 750; letter-spacing: .14em;
      text-transform: uppercase;
    }
    h1 {
      margin: 10px 0 12px; font-size: clamp(30px, 7vw, 56px);
      line-height: 1.05; letter-spacing: -.04em;
    }
    .intro { color: var(--muted); max-width: 650px; line-height: 1.7; }
    .card {
      margin-top: 28px; padding: clamp(20px, 4vw, 34px); border: 1px solid #e3eaf5;
      border-radius: 24px; background: #ffffffd9;
      box-shadow: 0 22px 60px #526b9c1c; backdrop-filter: blur(12px);
    }
    label { display: block; margin-bottom: 9px; color: #344054; font-size: 14px; font-weight: 700; }
    input, button { width: 100%; min-height: 48px; border-radius: 11px; font: inherit; }
    input {
      border: 1px solid #cbd6e6; padding: 0 14px; color: var(--ink); background: #fff;
      box-shadow: inset 0 1px 2px #1018280a;
    }
    button {
      margin-top: 16px; border: 0; padding: 0 18px; color: white;
      background: linear-gradient(100deg, var(--blue), #8177ed 52%, var(--pink));
      box-shadow: 0 10px 24px #6978e934; font-weight: 750; cursor: pointer;
    }
    button:disabled { cursor: wait; opacity: .52; }
    :focus-visible { outline: 3px solid #7aa2ff; outline-offset: 3px; }
    .source-info {
      min-height: 24px; margin-top: 12px; color: var(--muted); font-size: 13px;
      line-height: 1.5; overflow-wrap: anywhere;
    }
    .status { margin-top: 28px; padding-top: 24px; border-top: 1px solid var(--line); }
    .status-title {
      display: flex; align-items: baseline; justify-content: space-between;
      gap: 12px; flex-wrap: wrap;
    }
    .status-label { color: var(--ink); font-size: 18px; font-weight: 750; }
    .status-code {
      color: var(--blue); font-size: 13px; font-weight: 700;
    }
    .status-detail {
      margin: 10px 0 0; color: var(--muted); line-height: 1.55; overflow-wrap: anywhere;
    }
    .progress-track {
      height: 6px; margin: 22px 9px 0; border-radius: 99px; background: #e9eef7;
      overflow: hidden;
    }
    .progress-fill {
      width: 0; height: 100%; border-radius: inherit;
      background: linear-gradient(90deg, var(--blue), var(--pink));
      transition: width .45s ease;
    }
    .progress-steps {
      display: grid; grid-template-columns: repeat(4, 1fr); margin-top: -12px;
      list-style: none; padding: 0;
    }
    .progress-step { position: relative; text-align: center; color: #98a2b3; font-size: 12px; }
    .step-dot {
      display: grid; width: 20px; height: 20px; margin: 0 auto 9px; place-items: center;
      border: 4px solid #fff; border-radius: 50%; background: #d5ddea;
      box-shadow: 0 0 0 1px #d5ddea; transition: background .25s, box-shadow .25s;
    }
    .progress-step.is-current, .progress-step.is-complete { color: #344054; font-weight: 700; }
    .progress-step.is-complete .step-dot {
      background: var(--blue); box-shadow: 0 0 0 1px var(--blue);
    }
    .progress-step.is-current .step-dot {
      background: var(--pink); box-shadow: 0 0 0 4px var(--pink-soft), 0 0 0 5px #ef9dca;
    }
    .report-link {
      display: inline-block; margin-top: 16px; padding: 10px 15px; border-radius: 10px;
      color: #315dcd; background: var(--blue-soft); font-weight: 700; text-decoration: none;
    }
    [hidden] { display: none !important; }
    @media (max-width: 520px) {
      body { padding-top: 28px; }
      .card { margin-top: 22px; border-radius: 14px; }
      .status-title { display: block; }
      .status-code { display: block; margin-top: 5px; }
      .progress-step { font-size: 11px; }
    }
    @media (prefers-reduced-motion: reduce) { .progress-fill, .step-dot { transition: none; } }
  </style>
</head>
<body>
  <main>
    <div class="eyebrow">Video Visual Report · Local MVP</div>
    <h1>把一个公开 BV 视频变成报告</h1>
    <p class="intro">
      输入一个公开的 Bilibili BV 视频地址。本地会依次下载视频、生成文字稿、完成语义规划，
      最后生成一份带来源引用的视频报告。
    </p>
    <section class="card" aria-labelledby="url-label">
      <label id="url-label" for="url">公开 Bilibili BV URL</label>
      <input id="url" name="url" type="url" inputmode="url"
             placeholder="https://www.bilibili.com/video/BV..." autocomplete="off">
      <label for="ocr-mode" style="margin-top:16px">字幕 OCR 模式</label>
      <select id="ocr-mode" name="ocr_mode">
        <option value="auto" selected>Auto ROI（不稳定时自动降级）</option>
        <option value="roi">显式 ROI（可靠主路径）</option>
        <option value="off">关闭 OCR</option>
      </select>
      <label for="ocr-roi" style="margin-top:16px">显式 ROI（可选，x1,y1,x2,y2）</label>
      <input id="ocr-roi" name="ocr_roi" inputmode="decimal" placeholder="0.05,0.72,0.95,0.98">
      <label for="subtitle-file" style="margin-top:16px">本地字幕文件（可选，SRT/VTT/ASS）</label>
      <input id="subtitle-file" name="subtitle_file" placeholder="/path/to/subtitle.srt">
      <div id="source-info" class="source-info" aria-live="polite">
        仅支持公开的 Bilibili BV 视频链接。
      </div>
      <button id="generate" type="button">生成 Visual Report</button>
      <div class="status" aria-live="polite" aria-atomic="true" aria-busy="false">
        <div class="status-title">
          <span id="status-label" class="status-label">尚未开始</span>
          <span id="status-code" class="status-code">准备就绪</span>
        </div>
        <p id="status-detail" class="status-detail">粘贴视频链接后，点击上方按钮开始生成。</p>
        <div id="progress" role="progressbar" aria-label="报告生成进度"
             aria-valuemin="0" aria-valuemax="4" aria-valuenow="0">
          <div class="progress-track"><div id="progress-fill" class="progress-fill"></div></div>
          <ol class="progress-steps">
            <li class="progress-step" data-step="1"><span class="step-dot"></span>下载视频</li>
            <li class="progress-step" data-step="2"><span class="step-dot"></span>生成文字稿</li>
            <li class="progress-step" data-step="3"><span class="step-dot"></span>理解内容</li>
            <li class="progress-step" data-step="4"><span class="step-dot"></span>生成报告</li>
          </ol>
        </div>
        <a id="report-link" class="report-link" href="#" target="_blank"
           rel="noreferrer" hidden>查看生成的报告</a>
      </div>
    </section>
  </main>
  <script>
    (() => {
      const url = document.querySelector('#url');
      const generate = document.querySelector('#generate');
      const statusBox = document.querySelector('.status');
      const statusLabel = document.querySelector('#status-label');
      const statusCode = document.querySelector('#status-code');
      const statusDetail = document.querySelector('#status-detail');
      const progress = document.querySelector('#progress');
      const progressFill = document.querySelector('#progress-fill');
      const progressSteps = [...document.querySelectorAll('.progress-step')];
      const reportLink = document.querySelector('#report-link');
      const ocrMode = document.querySelector('#ocr-mode');
      const ocrRoi = document.querySelector('#ocr-roi');
      const subtitleFile = document.querySelector('#subtitle-file');
      const labels = {
        QUEUED: '等待处理',
        DOWNLOADING: '正在下载视频', TRANSCRIBING: '正在生成文字稿', OCR: '正在识别字幕',
        FUSING: '正在融合文字稿', READY: '已完成', DEGRADED: '文字稿已降级但可继续',
        CREATED: '已创建 run', MAPPING: '正在映射主题', TOPIC_MAPPED: '主题已绑定',
        PLANNING: '正在规划报告', PLAN_VALIDATED: '计划已验证',
        RENDERED: '报告已生成', FAILED: '运行失败', CANCELLED: '运行已取消'
      };
      let currentRunId = null;
      let polling = false;

      function updateProgress(displayStage, state) {
        const stepByStage = {
          QUEUED: 0, DOWNLOADING: 1, TRANSCRIBING: 2, OCR: 2, FUSING: 2,
          DEGRADED: 2, READY: 4, CREATED: 1,
          MAPPING: 3, TOPIC_MAPPED: 3, PLANNING: 4, PLAN_VALIDATED: 4, RENDERED: 4
        };
        const step = stepByStage[displayStage] || 0;
        const completed = state === 'RENDERED' ? 4 : Math.max(0, step - 1);
        progress.setAttribute('aria-valuenow', String(state === 'RENDERED' ? 4 : step));
        const progressPercent = state === 'RENDERED' ? 100 :
          completed * 25 + (step ? 12.5 : 0);
        progressFill.style.width = `${progressPercent}%`;
        for (const item of progressSteps) {
          const itemStep = Number(item.dataset.step);
          item.classList.toggle('is-complete', itemStep <= completed);
          item.classList.toggle('is-current', itemStep === step && state !== 'RENDERED');
        }
      }

      function showStatus(data) {
        const displayStage = data.stage || data.state || 'UNKNOWN';
        statusLabel.textContent = labels[displayStage] || '状态更新';
        statusCode.textContent = displayStage;
        statusBox.dataset.state = data.state || displayStage;
        updateProgress(displayStage, data.state || displayStage);
        const step = Number(progress.getAttribute('aria-valuenow'));
        const queued = displayStage === 'QUEUED';
        statusCode.textContent = data.state === 'RENDERED' ? '已完成' :
          (queued ? `排队第 ${data.queue_position || 1} 位` : `第 ${step || 1}/4 步`);
        statusDetail.textContent = queued ?
          `当前正在处理任务 ${data.active_run_id || '未知'}；` +
          `前面还有 ${data.queue_position || 1} 个任务。完成后会自动开始。` :
          ((data.state === 'RENDERED' ? '报告已经生成，可以立即查看。' :
            '进度会随处理状态自动更新。') +
          (data.error_category ? ` 错误类别：${data.error_category}。` : ''));
        reportLink.hidden = !data.report_url;
        if (data.report_url) reportLink.href = data.report_url;
        const terminal = ['RENDERED', 'FAILED', 'CANCELLED'].includes(data.state);
        statusBox.setAttribute('aria-busy', !terminal);
        if (terminal) {
          generate.disabled = false;
          polling = false;
        }
      }

      async function pollRun() {
        if (!currentRunId || polling) return;
        polling = true;
        try {
          const response = await fetch(
            `/api/visual-report/runs/${encodeURIComponent(currentRunId)}`,
            { headers: { 'Accept': 'application/json' } }
          );
          if (!response.ok) throw new Error('run_unavailable');
          const data = await response.json();
          showStatus(data);
          if (!['RENDERED', 'FAILED', 'CANCELLED'].includes(data.state)) {
            polling = false;
            window.setTimeout(pollRun, 500);
          }
        } catch (error) {
          polling = false;
          statusLabel.textContent = '状态暂时不可用';
          statusCode.textContent = 'WEB_ERROR';
          statusDetail.textContent = '请保留当前页面并稍后重试。';
          generate.disabled = false;
        }
      }

      async function generateReport() {
        const submittedUrl = url.value.trim();
        if (generate.disabled || !submittedUrl) return;
        generate.disabled = true;
        reportLink.hidden = true;
        const clientRequestId = `web-${crypto.randomUUID ? crypto.randomUUID() :
          `${Date.now()}-${Math.random()}`}`;
        try {
          const response = await fetch('/api/visual-report/runs', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
            body: JSON.stringify({
              url: submittedUrl,
              client_request_id: clientRequestId,
              transcript_mode: 'fused',
              ocr_mode: ocrMode.value,
              ocr_roi: ocrRoi.value.trim() || null,
              subtitle_file: subtitleFile.value.trim() || null
            })
          });
          const data = await response.json();
          if (!response.ok) throw new Error(data.error_category || 'run_rejected');
          currentRunId = data.run_id;
          showStatus(data);
          polling = false;
          pollRun();
        } catch (error) {
          statusLabel.textContent = '无法开始运行';
          statusCode.textContent = String(error.message || 'REQUEST_ERROR');
          statusDetail.textContent = '没有产生新的模型调用。请检查 URL 后重试。';
          generate.disabled = false;
        }
      }

      generate.addEventListener('click', generateReport);
      url.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') generateReport();
      });
      const initialRunId = new URLSearchParams(window.location.search).get('run_id');
      if (initialRunId) { currentRunId = initialRunId; pollRun(); }
    })();
  </script>
</body>
</html>
"""


class VisualReportWebApp:
    """Own one in-memory loopback Web session and its single active run."""

    def __init__(
        self,
        *,
        source_root: Path,
        artifact_root: Path,
        provider_factory: ProviderFactory | None = None,
        run_builder: RunBuilder = build_from_transcript_v2,
        product_manifest: Path | None = None,
    ) -> None:
        self.source_root = source_root.resolve()
        self.artifact_root = artifact_root.resolve()
        self.provider_factory = provider_factory
        self.run_builder = run_builder
        self._lock = threading.Lock()
        self._runs: dict[str, _WebRun] = {}
        self._request_ids: dict[str, str] = {}
        self._active_run_id: str | None = None
        self._web_smoke_run_id: str | None = None
        self._web_smoke_claimed = False
        if product_manifest is not None:
            freeze = load_semantic_v2_product_freeze(product_manifest)
            self._assert_product_gate(freeze)
            if freeze.web_smoke is None:
                raise PlanningError(
                    "WEB_GATE_NOT_READY", "product manifest has no Web smoke identity"
                )
            self._web_smoke_run_id = freeze.web_smoke.run_id

    def page_html(self) -> str:
        return _html_page()

    def _assert_product_gate(self, freeze: Any) -> None:
        if freeze.status != "FROZEN":
            raise PlanningError("WEB_GATE_NOT_READY", "product freeze is not provider-ready")
        if Path(freeze.artifact_root).resolve() != self.artifact_root:
            raise PlanningError(
                "WEB_GATE_NOT_READY", "Web artifact root differs from product freeze"
            )
        for declaration in freeze.runs:
            run_dir = self.artifact_root / declaration.run_id
            try:
                payload = _read_json(run_dir / "run.json")
            except PlanningError as exc:
                raise PlanningError(
                    "WEB_GATE_NOT_READY", "all product runs must be rendered"
                ) from exc
            if payload.get("state") != "RENDERED" or not (run_dir / "report.html").is_file():
                raise PlanningError("WEB_GATE_NOT_READY", "all product runs must be rendered")

    def sources(self) -> dict[str, object]:
        rows: list[dict[str, object]] = []
        for video_id in ALLOWED_VIDEO_IDS:
            manifest_rel, segments_rel = _SOURCE_PATHS[video_id]
            source = load_source(self.source_root / manifest_rel, self.source_root / segments_rel)
            rows.append(
                {
                    "video_id": source.video_id,
                    "title": source.title,
                    "duration_ms": source.duration_ms,
                    "segment_count": len(source.segments),
                }
            )
        return {"sources": rows}

    def _next_run_id(self, video_id: str) -> str:
        if (
            video_id == "p0b-kling-2024"
            and self._web_smoke_run_id is not None
            and not self._web_smoke_claimed
        ):
            self._web_smoke_claimed = True
            return self._web_smoke_run_id
        token = threading.get_native_id()
        suffix = f"{token:x}-{len(self._runs) + 1:02d}"
        return f"web-{video_id}-{suffix}"

    def _status(self, item: _WebRun) -> dict[str, object]:
        payload = _read_json(item.recorder.run_path)
        state = str(payload.get("state", "CREATED"))
        display_stage = (
            state if state in _TERMINAL_STATES else item.display_stage or state
        )
        error = payload.get("error")
        error_category = error.get("category") if isinstance(error, dict) else None
        report_url = None
        if state == "RENDERED" and (item.recorder.run_dir / "report.html").is_file():
            report_url = f"/visual-report/runs/{item.run_id}/report"
        return {
            "run_id": item.run_id,
            "video_id": item.video_id,
            "state": state,
            "stage": display_stage,
            "provider_calls": _safe_int(payload.get("provider_calls")),
            "model_calls": _safe_int(payload.get("model_calls")),
            "retry_used": _safe_bool(payload.get("retry_used")),
            "error_category": error_category if isinstance(error_category, str) else None,
            "report_url": report_url,
        }

    def _run_worker(self, item: _WebRun) -> None:
        try:
            provider = self.provider_factory() if self.provider_factory is not None else None
            manifest_rel, segments_rel = _SOURCE_PATHS[item.video_id]
            self.run_builder(
                manifest_path=self.source_root / manifest_rel,
                segments_path=self.source_root / segments_rel,
                run_id=item.run_id,
                output_root=self.artifact_root,
                provider=provider,
                recorder=item.recorder,
            )
        except KeyboardInterrupt:
            item.recorder.fail(
                PlanningError("CANCELLED", "run cancelled by operator"), state="CANCELLED"
            )
        except PlanningError:
            pass
        except Exception as exc:
            item.recorder.fail(PlanningError("OUTPUT_IO_ERROR", type(exc).__name__))
        finally:
            with self._lock:
                if self._active_run_id == item.run_id:
                    self._active_run_id = None

    def create_run(
        self, video_id: object, client_request_id: object
    ) -> tuple[int, dict[str, object]]:
        if not isinstance(video_id, str) or video_id not in ALLOWED_VIDEO_IDS:
            return 400, {"error_category": "VIDEO_NOT_ALLOWLISTED"}
        if not isinstance(client_request_id, str) or _SAFE_ID.fullmatch(client_request_id) is None:
            return 400, {"error_category": "REQUEST_ID_INVALID"}
        with self._lock:
            existing = self._request_ids.get(client_request_id)
            if existing is not None:
                item = self._runs[existing]
                if item.video_id != video_id:
                    return 409, {"error_category": "REQUEST_ID_CONFLICT"}
                return 200, {**self._status(item), "duplicate": True}
            if self._active_run_id is not None:
                return 409, {"error_category": "RUN_ACTIVE"}
            run_id = self._next_run_id(video_id)
            try:
                recorder = RunRecorder.create(
                    self.artifact_root,
                    run_id,
                    schema_version=SEMANTIC_V2_RUN_SCHEMA_VERSION,
                    event_schema_version=SEMANTIC_V2_EVENT_SCHEMA_VERSION,
                    call_schema_version=SEMANTIC_V2_CALL_SCHEMA_VERSION,
                )
            except PlanningError as exc:
                return 500, {"error_category": exc.category}
            item = _WebRun(video_id, client_request_id, run_id, recorder)
            self._runs[run_id] = item
            self._request_ids[client_request_id] = run_id
            self._active_run_id = run_id
            thread = threading.Thread(target=self._run_worker, args=(item,), daemon=True)
            thread.start()
        return 202, {**self._status(item), "duplicate": False}

    def get_run(self, run_id: str) -> tuple[int, dict[str, object]]:
        if _SAFE_ID.fullmatch(run_id) is None:
            return 404, {"error_category": "RUN_NOT_FOUND"}
        with self._lock:
            item = self._runs.get(run_id)
        if item is None:
            return 404, {"error_category": "RUN_NOT_FOUND"}
        try:
            return 200, self._status(item)
        except PlanningError as exc:
            return 500, {"error_category": exc.category}

    def get_report(self, run_id: str) -> tuple[int, bytes | dict[str, object]]:
        if _SAFE_ID.fullmatch(run_id) is None:
            return 404, {"error_category": "REPORT_NOT_FOUND"}
        with self._lock:
            item = self._runs.get(run_id)
        if item is None:
            return 404, {"error_category": "REPORT_NOT_FOUND"}
        try:
            status = self._status(item)
        except PlanningError as exc:
            return 500, {"error_category": exc.category}
        if status["state"] != "RENDERED":
            return 409, {"error_category": "REPORT_NOT_READY"}
        run_dir = item.recorder.run_dir.resolve()
        report_path = (run_dir / "report.html").resolve()
        if report_path.parent != run_dir or not report_path.is_file():
            return 404, {"error_category": "REPORT_NOT_FOUND"}
        try:
            return 200, report_path.read_bytes()
        except OSError:
            return 500, {"error_category": "OUTPUT_IO_ERROR"}

    def handle_get(self, request: BaseHTTPRequestHandler) -> None:
        path = urlsplit(request.path).path
        if path == "/visual-report/":
            _send_html(request, 200, self.page_html())
            return
        if path == "/api/visual-report/sources":
            try:
                _send_json(request, 200, self.sources())
            except PlanningError as exc:
                _send_json(request, 500, {"error_category": exc.category})
            return
        prefix = "/api/visual-report/runs/"
        if path.startswith(prefix):
            run_id = unquote(path[len(prefix) :])
            status, payload = self.get_run(run_id)
            _send_json(request, status, payload)
            return
        report_prefix = "/visual-report/runs/"
        report_suffix = "/report"
        if path.startswith(report_prefix) and path.endswith(report_suffix):
            run_id = unquote(path[len(report_prefix) : -len(report_suffix)])
            status, payload = self.get_report(run_id)
            if isinstance(payload, bytes):
                _send_html_bytes(request, status, payload)
            else:
                _send_json(request, status, payload)
            return
        _send_json(request, 404, {"error_category": "NOT_FOUND"})

    def handle_post(self, request: BaseHTTPRequestHandler) -> None:
        if urlsplit(request.path).path != "/api/visual-report/runs":
            _send_json(request, 404, {"error_category": "NOT_FOUND"})
            return
        length_raw = request.headers.get("Content-Length", "")
        try:
            length = int(length_raw)
        except ValueError:
            length = -1
        if length < 0 or length > _MAX_REQUEST_BYTES:
            _send_json(request, 400, {"error_category": "REQUEST_TOO_LARGE"})
            return
        try:
            body = request.rfile.read(length)
            payload = json.loads(body.decode("utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            _send_json(request, 400, {"error_category": "REQUEST_INVALID"})
            return
        if not isinstance(payload, dict):
            _send_json(request, 400, {"error_category": "REQUEST_INVALID"})
            return
        if set(payload) != {"video_id", "client_request_id"}:
            _send_json(request, 400, {"error_category": "REQUEST_INVALID"})
            return
        status, response = self.create_run(
            payload.get("video_id"), payload.get("client_request_id")
        )
        _send_json(request, status, response)


class UrlIngestWebApp(VisualReportWebApp):
    """Loopback Web mode with one active URL run and an in-memory FIFO queue."""

    def __init__(
        self,
        *,
        artifact_root: Path,
        provider_factory: ProviderFactory | None = None,
        run_builder: RunBuilder = build_from_transcript_v2,
        downloader: Callable[..., DownloadResult] | None = None,
        ingestor: Callable[..., IngestResult] | None = None,
    ) -> None:
        super().__init__(
            source_root=Path("."),
            artifact_root=artifact_root,
            provider_factory=provider_factory,
            run_builder=run_builder,
        )
        self.downloader = downloader
        self.ingestor = ingestor
        self._pending_run_ids: deque[str] = deque()

    def page_html(self) -> str:
        return _url_html_page()

    def _next_run_id(self, video_id: str) -> str:
        return f"url-{video_id}-{uuid.uuid4().hex[:12]}"

    def _record_url(self, item: _WebRun, **values: object) -> None:
        metadata = item.recorder.payload.setdefault("url_ingest", {})
        if isinstance(metadata, dict):
            metadata.update(values)
        item.recorder.save()

    def _status(self, item: _WebRun) -> dict[str, object]:
        status = super()._status(item)
        status["transcript_mode"] = item.transcript_mode
        status["ocr_mode"] = item.ocr_mode
        pending = tuple(self._pending_run_ids)
        if item.run_id in pending:
            status["stage"] = "QUEUED"
            status["queue_position"] = pending.index(item.run_id) + 1
            status["active_run_id"] = self._active_run_id
        else:
            status["queue_position"] = 0
            status["active_run_id"] = None
        return status

    def _start_worker(self, item: _WebRun) -> None:
        item.display_stage = "DOWNLOADING"
        self._record_url(item, status="STARTED")
        thread = threading.Thread(target=self._run_worker, args=(item,), daemon=True)
        thread.start()

    def _finish_and_start_next(self, item: _WebRun) -> None:
        next_item: _WebRun | None = None
        with self._lock:
            if self._active_run_id == item.run_id:
                self._active_run_id = None
                if self._pending_run_ids:
                    next_run_id = self._pending_run_ids.popleft()
                    next_item = self._runs[next_run_id]
                    self._active_run_id = next_run_id
        if next_item is not None:
            self._start_worker(next_item)

    def _run_worker(self, item: _WebRun) -> None:
        stage = "download"
        try:
            source = validate_bilibili_url(item.input_url)
            item.display_stage = "DOWNLOADING"
            if self.downloader is not None:
                download = self.downloader(source, item.recorder.run_dir)
            else:
                download = download_bilibili_video(
                    source,
                    item.recorder.run_dir,
                    request_subtitles=True,
                )
            self._record_url(
                item,
                status="DOWNLOADED",
                download={
                    "status": "SUCCEEDED",
                    "media_path": _run_relative_path(
                        download.media_path, item.recorder.run_dir
                    ),
                    "info_path": _run_relative_path(
                        download.info_path, item.recorder.run_dir
                    ),
                    "title": download.title,
                    "uploader": download.uploader,
                    "attribution": download.attribution,
                    "subtitle_file": (
                        _run_relative_path(download.subtitle_file, item.recorder.run_dir)
                        if download.subtitle_file is not None
                        else None
                    ),
                    "command": list(download.command),
                },
            )

            stage = "ingest"
            item.display_stage = "TRANSCRIBING"
            if self.ingestor is not None:
                ingest = self.ingestor(download, item.recorder.run_dir)
            else:
                ingest = ingest_downloaded_video(
                    download,
                    item.recorder.run_dir,
                    transcript_mode=item.transcript_mode,
                    ocr_mode=item.ocr_mode,
                    ocr_roi=item.ocr_roi,
                    subtitle_file=(
                        Path(item.subtitle_file).expanduser()
                        if item.subtitle_file
                        else None
                    ),
                )
            transcript_manifest = ingest.artifact_root / "transcript-manifest.json"
            if transcript_manifest.is_file():
                try:
                    transcript_payload = json.loads(
                        transcript_manifest.read_text(encoding="utf-8")
                    )
                except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                    transcript_payload = {}
                transcript_status = transcript_payload.get("status")
                item.display_stage = (
                    "DEGRADED" if transcript_status == "DEGRADED" else "FUSING"
                )
            else:
                item.display_stage = "FUSING"
            self._record_url(
                item,
                status="INGESTED",
                ingest={
                    "status": "SUCCEEDED",
                    "video_id": ingest.video_id,
                    "artifact_root": _run_relative_path(
                        ingest.artifact_root, item.recorder.run_dir
                    ),
                    "manifest_path": _run_relative_path(
                        ingest.manifest_path, item.recorder.run_dir
                    ),
                    "segments_path": _run_relative_path(
                        ingest.segments_path, item.recorder.run_dir
                    ),
                    "transcript_manifest_path": (
                        _run_relative_path(transcript_manifest, item.recorder.run_dir)
                        if transcript_manifest.is_file()
                        else None
                    ),
                    "command": list(ingest.command),
                },
            )

            stage = "planning"
            item.display_stage = None
            provider = self.provider_factory() if self.provider_factory is not None else None
            self.run_builder(
                manifest_path=ingest.manifest_path,
                segments_path=ingest.segments_path,
                run_id=item.run_id,
                output_root=self.artifact_root,
                provider=provider,
                recorder=item.recorder,
            )
            self._record_url(item, status="RENDERED")
        except UrlIngestError as exc:
            try:
                self._record_url(
                    item,
                    status="FAILED",
                    failure={"stage": stage, "category": exc.category},
                )
            finally:
                item.recorder.fail(PlanningError(exc.category, "url ingest failed"))
        except KeyboardInterrupt:
            error = PlanningError("CANCELLED", "run cancelled by operator")
            item.recorder.fail(error, state="CANCELLED")
        except PlanningError as exc:
            item.recorder.fail(exc)
        except Exception as exc:
            item.recorder.fail(PlanningError("OUTPUT_IO_ERROR", type(exc).__name__))
        finally:
            self._finish_and_start_next(item)

    def create_run(
        self,
        url: object,
        client_request_id: object,
        *,
        transcript_mode: object = "fused",
        ocr_mode: object = "auto",
        ocr_roi: object = None,
        subtitle_file: object = None,
    ) -> tuple[int, dict[str, object]]:
        try:
            source = validate_bilibili_url(url)
        except UrlIngestError as exc:
            return 400, {"error_category": exc.category}
        if not isinstance(client_request_id, str) or _SAFE_ID.fullmatch(client_request_id) is None:
            return 400, {"error_category": "REQUEST_ID_INVALID"}
        if transcript_mode not in {"asr-only", "fused"}:
            return 400, {"error_category": "TRANSCRIPT_MODE_INVALID"}
        if ocr_mode not in {"off", "roi", "auto"}:
            return 400, {"error_category": "OCR_MODE_INVALID"}
        if ocr_mode == "roi":
            if not isinstance(ocr_roi, str) or not ocr_roi.strip():
                return 400, {"error_category": "OCR_ROI_REQUIRED"}
            try:
                parse_roi(ocr_roi)
            except OcrError:
                return 400, {"error_category": "OCR_ROI_INVALID"}
        if ocr_roi is not None and not isinstance(ocr_roi, str):
            return 400, {"error_category": "OCR_ROI_INVALID"}
        if subtitle_file is not None and (
            not isinstance(subtitle_file, str)
            or not subtitle_file.strip()
            or len(subtitle_file) > 1024
            or "\x00" in subtitle_file
        ):
            return 400, {"error_category": "SUBTITLE_FILE_INVALID"}
        start_now = False
        with self._lock:
            existing = self._request_ids.get(client_request_id)
            if existing is not None:
                item = self._runs[existing]
                if item.input_url != source.canonical_url:
                    return 409, {"error_category": "REQUEST_ID_CONFLICT"}
                return 200, {**self._status(item), "duplicate": True}
            run_id = self._next_run_id(source.video_id)
            try:
                recorder = RunRecorder.create(
                    self.artifact_root,
                    run_id,
                    schema_version=SEMANTIC_V2_RUN_SCHEMA_VERSION,
                    event_schema_version=SEMANTIC_V2_EVENT_SCHEMA_VERSION,
                    call_schema_version=SEMANTIC_V2_CALL_SCHEMA_VERSION,
                )
            except PlanningError as exc:
                return 500, {"error_category": exc.category}
            recorder.payload["url_ingest"] = {
                "schema_version": URL_INGEST_SCHEMA_VERSION,
                "submitted_url": source.submitted_url,
                "canonical_url": source.canonical_url,
                "bvid": source.bvid,
                "video_id": source.video_id,
                "status": "QUEUED" if self._active_run_id is not None else "STARTED",
                "transcript_mode": transcript_mode,
                "ocr_mode": ocr_mode,
                "ocr_roi": ocr_roi.strip() if isinstance(ocr_roi, str) else None,
                "subtitle_file": subtitle_file.strip() if isinstance(subtitle_file, str) else None,
            }
            recorder.save()
            item = _WebRun(
                video_id=source.video_id,
                client_request_id=client_request_id,
                run_id=run_id,
                recorder=recorder,
                input_url=source.canonical_url,
                display_stage="QUEUED" if self._active_run_id is not None else "DOWNLOADING",
                transcript_mode=str(transcript_mode),
                ocr_mode=str(ocr_mode),
                ocr_roi=ocr_roi.strip() if isinstance(ocr_roi, str) else None,
                subtitle_file=subtitle_file.strip() if isinstance(subtitle_file, str) else None,
            )
            self._runs[run_id] = item
            self._request_ids[client_request_id] = run_id
            if self._active_run_id is None:
                self._active_run_id = run_id
                start_now = True
            else:
                self._pending_run_ids.append(run_id)
        if start_now:
            self._start_worker(item)
        return 202, {**self._status(item), "duplicate": False}

    def handle_get(self, request: BaseHTTPRequestHandler) -> None:
        path = urlsplit(request.path).path
        if path == "/api/visual-report/sources":
            _send_json(request, 404, {"error_category": "NOT_FOUND"})
            return
        super().handle_get(request)

    def handle_post(self, request: BaseHTTPRequestHandler) -> None:
        if urlsplit(request.path).path != "/api/visual-report/runs":
            _send_json(request, 404, {"error_category": "NOT_FOUND"})
            return
        length_raw = request.headers.get("Content-Length", "")
        try:
            length = int(length_raw)
        except ValueError:
            length = -1
        if length < 0 or length > _MAX_REQUEST_BYTES:
            _send_json(request, 400, {"error_category": "REQUEST_TOO_LARGE"})
            return
        try:
            body = request.rfile.read(length)
            payload = json.loads(body.decode("utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            _send_json(request, 400, {"error_category": "REQUEST_INVALID"})
            return
        allowed = {
            "url",
            "client_request_id",
            "transcript_mode",
            "ocr_mode",
            "ocr_roi",
            "subtitle_file",
        }
        if not isinstance(payload, dict) or not {"url", "client_request_id"} <= set(payload):
            _send_json(request, 400, {"error_category": "REQUEST_INVALID"})
            return
        if set(payload) - allowed:
            _send_json(request, 400, {"error_category": "REQUEST_INVALID"})
            return
        status, response = self.create_run(
            payload.get("url"),
            payload.get("client_request_id"),
            transcript_mode=payload.get("transcript_mode", "fused"),
            ocr_mode=payload.get("ocr_mode", "auto"),
            ocr_roi=payload.get("ocr_roi"),
            subtitle_file=payload.get("subtitle_file"),
        )
        _send_json(request, status, response)


class _LoopbackServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, app: VisualReportWebApp, port: int) -> None:
        self.app = app
        super().__init__(("127.0.0.1", port), _handler_type())


def _handler_type() -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        server: _LoopbackServer

        def do_GET(self) -> None:  # noqa: N802
            self.server.app.handle_get(self)

        def do_POST(self) -> None:  # noqa: N802
            self.server.app.handle_post(self)

        def log_message(self, format: str, *args: object) -> None:
            return

    return Handler


def _send_json(request: BaseHTTPRequestHandler, status: int, payload: object) -> None:
    body = _json_bytes(payload)
    request.send_response(status)
    request.send_header("Content-Type", "application/json; charset=utf-8")
    request.send_header("Content-Length", str(len(body)))
    request.send_header("Cache-Control", "no-store")
    request.end_headers()
    request.wfile.write(body)


def _send_html(request: BaseHTTPRequestHandler, status: int, body: str) -> None:
    _send_html_bytes(request, status, body.encode("utf-8"))


def _send_html_bytes(request: BaseHTTPRequestHandler, status: int, body: bytes) -> None:
    request.send_response(status)
    request.send_header("Content-Type", "text/html; charset=utf-8")
    request.send_header("Content-Length", str(len(body)))
    request.send_header("Cache-Control", "no-store")
    request.end_headers()
    request.wfile.write(body)


def create_web_server(app: VisualReportWebApp, *, port: int = 0) -> ThreadingHTTPServer:
    """Bind a Web MVP server to loopback only; port 0 is useful for tests."""
    if not isinstance(port, int) or not 0 <= port <= 65535:
        raise PlanningError("CONFIGURATION_ERROR", "port must be between 0 and 65535")
    return _LoopbackServer(app, port)


def serve_web(
    *,
    source_root: Path,
    artifact_root: Path,
    port: int,
    product_manifest: Path | None = None,
) -> None:
    """Run the loopback Web MVP until the operator stops it."""
    app = VisualReportWebApp(
        source_root=source_root,
        artifact_root=artifact_root,
        product_manifest=product_manifest,
    )
    server = create_web_server(app, port=port)
    actual_port = server.server_address[1]
    print(f"Visual Report Web MVP listening on http://127.0.0.1:{actual_port}/visual-report/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def serve_url_web(*, artifact_root: Path, port: int) -> None:
    """Run the public-Bilibili URL MVP on loopback only."""
    app = UrlIngestWebApp(artifact_root=artifact_root)
    server = create_web_server(app, port=port)
    actual_port = server.server_address[1]
    print(
        f"Video Visual Report URL Web MVP listening on "
        f"http://127.0.0.1:{actual_port}/visual-report/"
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


__all__ = [
    "ALLOWED_VIDEO_IDS",
    "VisualReportWebApp",
    "UrlIngestWebApp",
    "create_web_server",
    "serve_web",
    "serve_url_web",
]
