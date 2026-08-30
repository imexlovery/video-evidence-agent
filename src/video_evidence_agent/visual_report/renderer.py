"""Deterministic HTML renderer and bounded local asset resolver for V0."""

# Embedded CSS is intentionally authored as a readable design-token stylesheet.
# Its visual source lines do not need Python's 100-character wrapping rule.
# ruff: noqa: E501

from __future__ import annotations

import html
import json
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from .models import (
    ASSET_SCHEMA_VERSION,
    PLAN_SCHEMA_VERSION,
    AssetManifest,
    AssetRecord,
    Block,
    BulletGroupBlock,
    ComparisonCardBlock,
    ImageCaptionBlock,
    InsightCardBlock,
    MetricRowBlock,
    ProcessFlowBlock,
    ReportPlan,
    Section,
    TakeawayBoxBlock,
)


class RenderError(Exception):
    """A user-facing, stable renderer failure category."""

    def __init__(self, category: str, message: str) -> None:
        self.category = category
        self.message = message
        super().__init__(f"{category}: {message}")


@dataclass(frozen=True)
class ResolvedAsset:
    metadata: AssetRecord
    path: Path


@dataclass(frozen=True)
class RenderSummary:
    report_id: str
    section_count: int
    block_count: int
    used_asset_count: int
    output_path: Path


_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def _escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def _format_timestamp(milliseconds: int) -> str:
    total_seconds = milliseconds // 1000
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"


def _validation_detail(error: ValidationError) -> str:
    first = error.errors()[0]
    location = ".".join(str(part) for part in first.get("loc", ())) or "document"
    message = str(first.get("msg", "invalid value"))
    return f"{location}: {message}"


def _load_json(path: Path, category: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RenderError(category, f"file not found: {path}") from exc
    except (OSError, UnicodeDecodeError) as exc:
        raise RenderError(category, f"cannot read UTF-8 JSON: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RenderError(category, f"invalid JSON at line {exc.lineno}, column {exc.colno}") from exc


def load_plan(path: Path) -> ReportPlan:
    payload = _load_json(path, "PLAN_PARSE_ERROR")
    if not isinstance(payload, dict):
        raise RenderError("PLAN_SCHEMA_ERROR", "top-level value must be an object")
    if payload.get("schema_version") != PLAN_SCHEMA_VERSION:
        raise RenderError(
            "UNSUPPORTED_SCHEMA_VERSION",
            f"plan schema_version must be {PLAN_SCHEMA_VERSION}",
        )
    try:
        return ReportPlan.model_validate(payload)
    except ValidationError as exc:
        raise RenderError("PLAN_SCHEMA_ERROR", _validation_detail(exc)) from exc


def load_assets(path: Path) -> AssetManifest:
    payload = _load_json(path, "ASSET_SCHEMA_ERROR")
    if not isinstance(payload, dict):
        raise RenderError("ASSET_SCHEMA_ERROR", "top-level value must be an object")
    if payload.get("schema_version") != ASSET_SCHEMA_VERSION:
        raise RenderError(
            "UNSUPPORTED_SCHEMA_VERSION",
            f"asset schema_version must be {ASSET_SCHEMA_VERSION}",
        )
    try:
        return AssetManifest.model_validate(payload)
    except ValidationError as exc:
        raise RenderError("ASSET_SCHEMA_ERROR", _validation_detail(exc)) from exc


def _unsafe_relative_path(raw_path: str) -> bool:
    path = Path(raw_path)
    return (
        path.is_absolute()
        or raw_path.startswith(("/", "\\", "//", "~"))
        or _SCHEME_RE.match(raw_path) is not None
        or "\\" in raw_path
        or ".." in path.parts
    )


def resolve_assets(
    manifest_path: Path,
    manifest: AssetManifest,
    duration_ms: int,
) -> dict[str, ResolvedAsset]:
    base_dir = manifest_path.resolve().parent
    resolved: dict[str, ResolvedAsset] = {}
    for asset in manifest.assets:
        if asset.timestamp_ms > duration_ms:
            raise RenderError(
                "INVALID_SOURCE_REFERENCE",
                f"asset {asset.asset_id} timestamp_ms exceeds video duration",
            )
        if _unsafe_relative_path(asset.path):
            raise RenderError("UNSAFE_ASSET_PATH", f"asset {asset.asset_id} path is not a safe relative path")
        candidate = (base_dir / asset.path).resolve()
        try:
            candidate.relative_to(base_dir)
        except ValueError as exc:
            raise RenderError("UNSAFE_ASSET_PATH", f"asset {asset.asset_id} escapes artifact root") from exc
        if not candidate.is_file() or not os.access(candidate, os.R_OK):
            raise RenderError("ASSET_NOT_FOUND", f"asset {asset.asset_id} file not found: {asset.path}")
        resolved[asset.asset_id] = ResolvedAsset(metadata=asset, path=candidate)
    return resolved


def _source_trace(block: Block) -> str:
    refs = [
        {"segment_id": ref.segment_id, "start_ms": ref.start_ms, "end_ms": ref.end_ms}
        for ref in block.source_refs
    ]
    timestamps = " · ".join(_format_timestamp(ref.start_ms) for ref in block.source_refs)
    segment_text = " · ".join(ref.segment_id.rsplit("-", 1)[-1] for ref in block.source_refs)
    encoded_refs = _escape(json.dumps(refs, ensure_ascii=False, separators=(",", ":")))
    return (
        f'<div class="source-trace" data-source-refs="{encoded_refs}">'
        f'<span class="source-label">证据</span>'
        f'<span class="source-times">{_escape(timestamps)}</span>'
        f'<span class="source-segments">seg { _escape(segment_text) }</span>'
        "</div>"
    )


def _render_insight(block: InsightCardBlock) -> str:
    return (
        f'<article class="block insight-card" data-block-type="{block.type}" id="{_escape(block.block_id)}">'
        '<div class="insight-label"><span class="signal-dot"></span><span>INSIGHT</span></div>'
        '<div class="insight-copy">'
        f'<h3>{_escape(block.headline)}</h3>'
        f'<p>{_escape(block.body)}</p>'
        f"{_source_trace(block)}"
        "</div></article>"
    )


def _render_bullets(block: BulletGroupBlock) -> str:
    items = "".join(f'<li>{_escape(item)}</li>' for item in block.items)
    return (
        f'<article class="block bullet-group" data-block-type="{block.type}" id="{_escape(block.block_id)}">'
        f'<div class="block-heading"><span class="block-index">A /</span><h3>{_escape(block.headline)}</h3></div>'
        f'<ul>{items}</ul>'
        f"{_source_trace(block)}"
        "</article>"
    )


def _render_metrics(block: MetricRowBlock) -> str:
    items: list[str] = []
    for item in block.items:
        context = f'<p>{_escape(item.context)}</p>' if item.context else ""
        items.append(
            '<div class="metric-item">'
            f'<strong>{_escape(item.value)}</strong>'
            f'<span>{_escape(item.label)}</span>'
            f"{context}"
            "</div>"
        )
    return (
        f'<article class="block metric-row" data-block-type="{block.type}" id="{_escape(block.block_id)}">'
        f'<div class="metric-heading"><span class="block-index">FIELD NOTE</span><h3>{_escape(block.headline)}</h3></div>'
        f'<div class="metric-items">{"".join(items)}</div>'
        f"{_source_trace(block)}"
        "</article>"
    )


def _render_comparison(block: ComparisonCardBlock) -> str:
    def side_markup(side: object, tone: str) -> str:
        label = _escape(side.label)  # type: ignore[attr-defined]
        items = "".join(f'<li>{_escape(item)}</li>' for item in side.items)  # type: ignore[attr-defined]
        return (
            f'<div class="comparison-side comparison-side--{tone}">'
            f'<div class="comparison-label">{label}</div>'
            f'<ul>{items}</ul>'
            "</div>"
        )

    return (
        f'<article class="block comparison-card" data-block-type="{block.type}" id="{_escape(block.block_id)}">'
        f'<div class="comparison-intro"><span class="block-index">THE FIRST TURN</span><h3>{_escape(block.headline)}</h3></div>'
        '<div class="comparison-columns">'
        f'{side_markup(block.left, "left")}'
        '<div class="comparison-arrow" aria-hidden="true">→</div>'
        f'{side_markup(block.right, "right")}'
        '</div>'
        f"{_source_trace(block)}"
        "</article>"
    )


def _render_process(block: ProcessFlowBlock) -> str:
    step_count = len(block.steps)
    positions = [round(70 + index * (820 / max(step_count - 1, 1))) for index in range(step_count)]
    circles = "".join(
        f'<circle cx="{x}" cy="75" r="8" class="process-node" />' for x in positions
    )
    arrows = "".join(
        f'<path d="M {positions[index] + 16} 75 H {positions[index + 1] - 16}" class="process-arrow" />'
        for index in range(step_count - 1)
    )
    steps = "".join(
        f'<li class="process-step"><span class="process-number">{index + 1:02d}</span>'
        f'<h4>{_escape(step.title)}</h4><p>{_escape(step.body)}</p></li>'
        for index, step in enumerate(block.steps)
    )
    svg_title_id = f"{_escape(block.block_id)}-title"
    return (
        f'<article class="block process-block" data-block-type="{block.type}" id="{_escape(block.block_id)}">'
        f'<div class="process-heading"><span class="block-index">SYSTEM SHIFT</span><h3>{_escape(block.headline)}</h3></div>'
        '<div class="process-visual">'
        f'<svg class="process-flow-svg" viewBox="0 0 960 150" role="img" aria-labelledby="{svg_title_id}">'
        f'<title id="{svg_title_id}">{_escape(block.headline)}</title>'
        '<line x1="70" y1="75" x2="890" y2="75" class="process-line" />'
        '<defs><marker id="process-arrowhead" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" class="process-arrowhead" /></marker></defs>'
        f'{arrows}{circles}'
        '</svg>'
        f'<ol class="process-steps">{steps}</ol>'
        '</div>'
        f"{_source_trace(block)}"
        '</article>'
    )


def _render_image(
    block: ImageCaptionBlock,
    assets: dict[str, ResolvedAsset],
    output_path: Path,
) -> str:
    asset = assets.get(block.asset_id)
    if asset is None:
        raise RenderError("UNKNOWN_ASSET_REFERENCE", f"block {block.block_id} references {block.asset_id}")
    relative_src = os.path.relpath(asset.path, output_path.resolve().parent).replace(os.sep, "/")
    body = f'<p>{_escape(block.body)}</p>' if block.body else ""
    return (
        f'<figure class="block image-evidence" data-block-type="{block.type}" id="{_escape(block.block_id)}">'
        '<div class="image-frame">'
        f'<img src="{_escape(relative_src)}" alt="{_escape(asset.metadata.alt)}" loading="eager">'
        f'<span class="image-time">{_escape(_format_timestamp(asset.metadata.timestamp_ms))}</span>'
        '</div>'
        '<figcaption>'
        f'<div><span class="block-index">FRAME / {_escape(asset.metadata.asset_id)}</span><h3>{_escape(block.headline)}</h3>{body}</div>'
        f'<p class="asset-caption">{_escape(asset.metadata.caption)}</p>'
        f"{_source_trace(block)}"
        '</figcaption>'
        '</figure>'
    )


def _render_takeaways(block: TakeawayBoxBlock) -> str:
    items = "".join(f'<li><span>→</span>{_escape(item)}</li>' for item in block.takeaways)
    return (
        f'<article class="block takeaway-box" data-block-type="{block.type}" id="{_escape(block.block_id)}">'
        f'<div><span class="block-index">KEEP THIS</span><h3>{_escape(block.headline)}</h3></div>'
        f'<ul>{items}</ul>'
        f"{_source_trace(block)}"
        '</article>'
    )


def _render_block(
    block: Block,
    assets: dict[str, ResolvedAsset],
    output_path: Path,
) -> str:
    if block.asset_id is not None and block.asset_id not in assets:
        raise RenderError("UNKNOWN_ASSET_REFERENCE", f"block {block.block_id} references {block.asset_id}")
    if isinstance(block, InsightCardBlock):
        return _render_insight(block)
    if isinstance(block, BulletGroupBlock):
        return _render_bullets(block)
    if isinstance(block, MetricRowBlock):
        return _render_metrics(block)
    if isinstance(block, ComparisonCardBlock):
        return _render_comparison(block)
    if isinstance(block, ProcessFlowBlock):
        return _render_process(block)
    if isinstance(block, ImageCaptionBlock):
        return _render_image(block, assets, output_path)
    if isinstance(block, TakeawayBoxBlock):
        return _render_takeaways(block)
    raise RenderError("UNKNOWN_BLOCK_TYPE", f"unsupported block type: {type(block).__name__}")


def _render_spine(sections: tuple[Section, ...]) -> str:
    node_markup: list[str] = []
    count = len(sections)
    for index, section in enumerate(sections):
        top = 8 if count == 1 else 8 + (index / (count - 1)) * 84
        node_markup.append(
            f'<div class="spine-node" style="top: {top:.2f}%">'
            f'<span class="spine-dot"></span>'
            f'<span class="spine-node-label">{_escape(_format_timestamp(section.timestamp_ms))}</span>'
            '</div>'
        )
    return (
        '<aside class="argument-spine" aria-label="视频论证脉络">'
        '<svg class="spine-svg" viewBox="0 0 32 1000" preserveAspectRatio="none" aria-hidden="true">'
        '<path d="M16 0 V1000" class="spine-path" />'
        '</svg>'
        f'<div class="spine-labels">{"".join(node_markup)}</div>'
        '</aside>'
    )


def _render_section(
    section: Section,
    index: int,
    assets: dict[str, ResolvedAsset],
    output_path: Path,
) -> str:
    blocks = "".join(_render_block(block, assets, output_path) for block in section.blocks)
    return (
        f'<section class="story-section" id="{_escape(section.section_id)}" data-section-id="{_escape(section.section_id)}">'
        '<header class="section-heading">'
        '<div class="section-marker">'
        f'<span class="section-number">{index + 1:02d}</span>'
        f'<time datetime="PT{section.timestamp_ms / 1000:.0f}S">{_escape(_format_timestamp(section.timestamp_ms))}</time>'
        '</div>'
        '<div>'
        f'<p class="section-kicker">{_escape(section.kicker)}</p>'
        f'<h2>{_escape(section.title)}</h2>'
        '</div>'
        '</header>'
        f'<div class="section-blocks">{blocks}</div>'
        '</section>'
    )


CSS = """
:root {
  --ink: #14213D;
  --canvas: #F5F7FB;
  --paper: #FFFFFF;
  --purple: #6D4AFF;
  --blue: #2878FF;
  --coral: #FF6B4A;
  --line: #D8DEEA;
  --muted: #66728A;
  --soft-purple: #F2EFFF;
  --soft-blue: #F1F6FF;
  --soft-coral: #FFF3EE;
  --serif: "Songti SC", "STSong", "Noto Serif CJK SC", serif;
  --sans: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  --mono: "SFMono-Regular", "SF Mono", "Cascadia Code", monospace;
}

* { box-sizing: border-box; }
html { background: var(--canvas); }
body {
  margin: 0;
  color: var(--ink);
  background: var(--canvas);
  font-family: var(--sans);
  font-size: 16px;
  line-height: 1.65;
  overflow-x: hidden;
}
body, p, h1, h2, h3, h4, ul, ol, figure { margin: 0; }
ul, ol { padding: 0; list-style: none; }
img { max-width: 100%; }
a { color: inherit; }
a:focus-visible { outline: 3px solid var(--coral); outline-offset: 4px; }
time, .block-index, .eyebrow, .hero-meta, .source-trace, .image-time, .section-marker time { font-family: var(--mono); }

.report-page {
  width: min(1080px, 100%);
  min-height: 100vh;
  margin: 0 auto;
  background: var(--paper);
  box-shadow: 0 16px 60px rgba(20, 33, 61, .08);
}

.hero {
  position: relative;
  padding: 68px 88px 58px;
  color: var(--paper);
  background: var(--ink);
  border-top: 7px solid var(--coral);
  overflow: hidden;
}
.hero::before, .hero::after {
  position: absolute;
  content: "";
  pointer-events: none;
}
.hero::before {
  width: 160px;
  height: 160px;
  right: 46px;
  top: 42px;
  border: 1px solid rgba(255,255,255,.18);
  border-left: 0;
  border-bottom: 0;
}
.hero::after {
  width: 8px;
  height: 8px;
  right: 194px;
  top: 96px;
  background: var(--blue);
  box-shadow: 22px 0 0 var(--purple), 44px 0 0 var(--coral);
}
.hero-topline, .hero-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
}
.eyebrow {
  color: #B9C8E9;
  font-size: 11px;
  letter-spacing: .16em;
  line-height: 1.3;
}
.hero-stamp {
  color: var(--coral);
  font-size: 11px;
  letter-spacing: .12em;
}
.hero h1 {
  max-width: 720px;
  margin-top: 42px;
  font-family: var(--serif);
  font-size: clamp(42px, 5.2vw, 62px);
  font-weight: 700;
  letter-spacing: -.045em;
  line-height: 1.12;
  text-wrap: balance;
}
.hero-thesis {
  max-width: 700px;
  margin-top: 30px;
  padding-left: 20px;
  color: #E9EEFA;
  border-left: 3px solid var(--coral);
  font-size: 20px;
  line-height: 1.75;
}
.hero-meta {
  max-width: 790px;
  margin-top: 48px;
  padding-top: 18px;
  color: #AEBBD8;
  border-top: 1px solid rgba(255,255,255,.22);
  font-size: 11px;
  letter-spacing: .04em;
  line-height: 1.5;
}
.hero-meta strong { color: var(--paper); font-weight: 500; }
.hero-meta span { min-width: 0; }

.report-body {
  display: grid;
  grid-template-columns: 78px minmax(0, 1fr);
  gap: 18px;
  padding: 44px 66px 70px 32px;
}
.argument-spine { position: relative; min-height: 100%; }
.spine-svg { position: absolute; inset: 18px 25px 18px 25px; width: 28px; height: calc(100% - 36px); }
.spine-path { fill: none; stroke: var(--line); stroke-width: 2; stroke-dasharray: 2 10; }
.spine-labels { position: absolute; inset: 18px 0; }
.spine-node {
  position: absolute;
  left: 0;
  display: flex;
  align-items: center;
  gap: 9px;
  transform: translateY(-50%);
}
.spine-dot { width: 10px; height: 10px; flex: 0 0 auto; background: var(--purple); border: 3px solid var(--paper); outline: 1px solid var(--purple); }
.spine-node:nth-child(2) .spine-dot { background: var(--blue); outline-color: var(--blue); }
.spine-node:nth-child(3) .spine-dot { background: var(--coral); outline-color: var(--coral); }
.spine-node:nth-child(4) .spine-dot { background: var(--ink); outline-color: var(--ink); }
.spine-node-label { color: var(--muted); font: 10px/1 var(--mono); writing-mode: vertical-rl; transform: rotate(180deg); }

.story { min-width: 0; }
.reading-note {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 24px;
  padding: 0 0 25px;
  color: var(--muted);
  border-bottom: 1px solid var(--line);
  font-size: 13px;
}
.reading-note strong { color: var(--ink); font-weight: 600; }
.reading-note .note-tag { color: var(--purple); font: 10px var(--mono); letter-spacing: .12em; white-space: nowrap; }
.story-section { padding: 52px 0 62px; border-bottom: 1px solid var(--line); }
.story-section:last-child { padding-bottom: 22px; border-bottom: 0; }
.section-heading { display: grid; grid-template-columns: 72px minmax(0, 1fr); gap: 16px; align-items: start; }
.section-marker { display: flex; flex-direction: column; gap: 7px; padding-top: 7px; }
.section-number { color: var(--purple); font: 700 22px/1 var(--mono); letter-spacing: -.1em; }
.section-marker time { color: var(--coral); font-size: 11px; line-height: 1.2; }
.section-kicker { color: var(--blue); font: 11px/1.4 var(--mono); letter-spacing: .13em; text-transform: uppercase; }
.section-heading h2 { max-width: 670px; margin-top: 10px; font: 700 clamp(27px, 3vw, 39px)/1.25 var(--serif); letter-spacing: -.035em; }
.section-blocks { margin-top: 31px; }
.section-blocks > * + * { margin-top: 32px; }
.block { min-width: 0; }
.block h3 { color: var(--ink); font-size: 21px; line-height: 1.35; letter-spacing: -.02em; }
.block-index { display: block; color: var(--purple); font-size: 10px; letter-spacing: .12em; line-height: 1.4; }

.source-trace {
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 8px 12px;
  margin-top: 19px;
  color: var(--muted);
  font-size: 10px;
  line-height: 1.5;
  letter-spacing: .02em;
}
.source-label { color: var(--coral); font-weight: 700; letter-spacing: .1em; }
.source-times { color: var(--ink); }
.source-segments { color: #8A94A8; }

.insight-card { display: grid; grid-template-columns: 145px minmax(0, 1fr); gap: 28px; padding: 28px 0 0; border-top: 2px solid var(--coral); }
.insight-label { display: flex; align-items: baseline; gap: 9px; color: var(--coral); font: 11px var(--mono); letter-spacing: .12em; }
.signal-dot { display: inline-block; width: 7px; height: 7px; background: var(--coral); }
.insight-copy h3 { max-width: 640px; font-size: 28px; font-family: var(--serif); }
.insight-copy > p { max-width: 660px; margin-top: 13px; color: #3F4B63; font-size: 16px; line-height: 1.85; }

.comparison-card { padding: 27px 30px 25px; background: var(--soft-purple); border-left: 4px solid var(--purple); }
.comparison-intro { display: flex; align-items: baseline; gap: 18px; }
.comparison-intro h3 { font-family: var(--serif); }
.comparison-columns { display: grid; grid-template-columns: minmax(0, 1fr) 45px minmax(0, 1fr); gap: 18px; align-items: stretch; margin-top: 25px; }
.comparison-side { padding: 19px 20px 17px; border: 1px solid var(--line); background: var(--paper); }
.comparison-side--right { border-color: #C8BFFF; background: #FBFAFF; }
.comparison-label { color: var(--purple); font: 700 12px var(--mono); letter-spacing: .12em; }
.comparison-side--right .comparison-label { color: var(--coral); }
.comparison-side ul { margin-top: 13px; }
.comparison-side li { position: relative; padding-left: 17px; color: #3F4B63; font-size: 15px; line-height: 1.65; }
.comparison-side li + li { margin-top: 8px; }
.comparison-side li::before { position: absolute; left: 0; top: .72em; width: 6px; height: 2px; content: ""; background: var(--purple); }
.comparison-side--right li::before { background: var(--coral); }
.comparison-arrow { display: grid; place-items: center; color: var(--purple); font: 24px var(--mono); }

.bullet-group { padding: 25px 28px 23px; background: var(--soft-blue); border-left: 3px solid var(--blue); }
.block-heading { display: flex; align-items: baseline; gap: 17px; }
.bullet-group ul { margin-top: 17px; }
.bullet-group li { position: relative; padding-left: 28px; color: #33405A; font-size: 16px; line-height: 1.7; }
.bullet-group li + li { margin-top: 10px; }
.bullet-group li::before { position: absolute; left: 0; top: .78em; width: 10px; height: 10px; content: ""; border: 2px solid var(--blue); }

.metric-row { padding: 25px 0 23px; border-top: 1px solid var(--ink); border-bottom: 1px solid var(--line); }
.metric-heading { display: flex; align-items: baseline; gap: 18px; }
.metric-heading h3 { font-family: var(--serif); }
.metric-items { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); margin-top: 22px; }
.metric-item { padding: 3px 20px 2px 0; border-right: 1px solid var(--line); }
.metric-item + .metric-item { padding-left: 20px; }
.metric-item:last-child { border-right: 0; }
.metric-item strong { display: block; color: var(--purple); font: 700 34px/1.1 var(--mono); letter-spacing: -.08em; }
.metric-item span { display: block; margin-top: 9px; color: var(--ink); font-size: 14px; font-weight: 600; line-height: 1.45; }
.metric-item p { margin-top: 5px; color: var(--muted); font-size: 12px; line-height: 1.45; }

.process-block { padding: 27px 28px 24px; border: 1px solid var(--line); border-top: 3px solid var(--purple); }
.process-heading { display: flex; align-items: baseline; gap: 18px; }
.process-heading h3 { font-family: var(--serif); }
.process-visual { position: relative; margin-top: 23px; padding-top: 38px; }
.process-flow-svg { position: absolute; top: 0; left: 0; width: 100%; height: 105px; overflow: visible; }
.process-line { stroke: #B8C0D2; stroke-width: 2; stroke-dasharray: 1 7; }
.process-arrow { fill: none; stroke: var(--purple); stroke-width: 2; marker-end: url(#process-arrowhead); }
.process-arrowhead { fill: var(--purple); }
.process-node { fill: var(--paper); stroke: var(--purple); stroke-width: 4; }
.process-steps { position: relative; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 15px; }
.process-step { min-width: 0; padding: 25px 13px 0; border-top: 1px solid var(--line); }
.process-number { color: var(--coral); font: 12px var(--mono); }
.process-step h4 { margin-top: 8px; font-size: 16px; line-height: 1.4; }
.process-step p { margin-top: 8px; color: var(--muted); font-size: 13px; line-height: 1.65; overflow-wrap: anywhere; }

.image-evidence { padding: 12px; background: var(--ink); }
.image-frame { position: relative; }
.image-frame img { display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border: 1px solid rgba(255,255,255,.25); }
.image-time { position: absolute; right: 12px; bottom: 12px; padding: 5px 8px; color: var(--paper); background: var(--coral); font-size: 11px; line-height: 1; }
.image-evidence figcaption { display: grid; grid-template-columns: minmax(0, 1fr) 220px; gap: 24px; padding: 20px 4px 3px; color: var(--paper); }
.image-evidence .block-index { color: #B9C8E9; }
.image-evidence h3 { margin-top: 7px; color: var(--paper); font-family: var(--serif); }
.image-evidence figcaption p { color: #C5CEE0; font-size: 13px; line-height: 1.6; }
.image-evidence figcaption .asset-caption { padding-left: 18px; border-left: 1px solid rgba(255,255,255,.28); }
.image-evidence .source-trace { grid-column: 1 / -1; color: #9EABC7; }
.image-evidence .source-label { color: var(--coral); }
.image-evidence .source-times { color: var(--paper); }

.takeaway-box { display: grid; grid-template-columns: 190px minmax(0, 1fr); gap: 28px; padding: 28px 30px 26px; background: var(--soft-coral); border-left: 4px solid var(--coral); }
.takeaway-box h3 { margin-top: 9px; font-family: var(--serif); }
.takeaway-box ul { padding-top: 1px; }
.takeaway-box li { display: grid; grid-template-columns: 22px minmax(0, 1fr); gap: 8px; color: #3F4B63; font-size: 15px; line-height: 1.7; }
.takeaway-box li + li { margin-top: 12px; }
.takeaway-box li span { color: var(--coral); font: 18px/1.5 var(--mono); }
.takeaway-box .source-trace { grid-column: 1 / -1; }

.report-footer { padding: 28px 88px 34px; color: #C5CEE0; background: var(--ink); }
.footer-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
.report-footer h2 { color: var(--paper); font: 700 19px var(--serif); }
.report-footer p { margin-top: 9px; font-size: 12px; line-height: 1.7; overflow-wrap: anywhere; }
.footer-label { color: var(--coral); font: 10px var(--mono); letter-spacing: .12em; }
.footer-bottom { display: flex; justify-content: space-between; gap: 20px; margin-top: 25px; padding-top: 14px; color: #8592AD; border-top: 1px solid rgba(255,255,255,.2); font: 10px/1.5 var(--mono); }

@media (max-width: 700px) {
  html, body { background: var(--paper); }
  .report-page { width: 100%; box-shadow: none; }
  .hero { padding: 42px 24px 38px; border-top-width: 5px; }
  .hero::before { right: -70px; top: 26px; }
  .hero::after { right: 48px; top: 77px; }
  .hero-topline { align-items: flex-start; }
  .hero h1 { max-width: 100%; margin-top: 34px; font-size: 43px; line-height: 1.15; }
  .hero-thesis { margin-top: 24px; padding-left: 15px; font-size: 17px; line-height: 1.7; }
  .hero-meta { align-items: flex-start; flex-wrap: wrap; margin-top: 32px; font-size: 10px; }
  .hero-meta span { flex: 1 1 38%; }
  .report-body { display: block; padding: 26px 24px 44px; }
  .argument-spine { display: none; }
  .reading-note { display: block; padding-bottom: 20px; font-size: 12px; }
  .reading-note .note-tag { display: block; margin-bottom: 8px; }
  .story-section { padding: 38px 0 48px; }
  .section-heading { display: block; }
  .section-marker { flex-direction: row; align-items: baseline; gap: 12px; padding-top: 0; }
  .section-number { font-size: 19px; }
  .section-heading h2 { margin-top: 9px; font-size: 31px; }
  .section-blocks { margin-top: 25px; }
  .section-blocks > * + * { margin-top: 26px; }
  .block h3 { font-size: 19px; }
  .insight-card { display: block; padding-top: 21px; }
  .insight-copy { margin-top: 17px; }
  .insight-copy h3 { font-size: 25px; }
  .insight-copy > p { font-size: 15px; line-height: 1.8; }
  .comparison-card { padding: 22px 18px 20px; }
  .comparison-intro { display: block; }
  .comparison-intro h3 { margin-top: 8px; }
  .comparison-columns { display: block; margin-top: 18px; }
  .comparison-side { padding: 16px; }
  .comparison-side + .comparison-side { margin-top: 12px; }
  .comparison-arrow { display: block; height: 23px; text-align: center; line-height: 23px; transform: rotate(90deg); }
  .bullet-group { padding: 21px 18px 19px; }
  .block-heading, .metric-heading, .process-heading { display: block; }
  .block-heading h3, .metric-heading h3, .process-heading h3 { margin-top: 8px; }
  .metric-row { padding: 21px 0 19px; }
  .metric-items { grid-template-columns: repeat(2, minmax(0, 1fr)); margin-top: 17px; }
  .metric-item { padding: 5px 14px 10px 0; border-right: 0; border-bottom: 1px solid var(--line); }
  .metric-item + .metric-item { padding-left: 0; }
  .metric-item:nth-child(even) { padding-left: 14px; border-left: 1px solid var(--line); }
  .metric-item:nth-last-child(-n + 2) { border-bottom: 0; padding-bottom: 0; }
  .metric-item strong { font-size: 27px; letter-spacing: -.07em; }
  .metric-item span { font-size: 13px; }
  .process-block { padding: 22px 17px 20px; }
  .process-visual { margin-top: 18px; padding: 0 0 0 18px; border-left: 2px solid var(--purple); }
  .process-flow-svg { display: none; }
  .process-steps { display: block; }
  .process-step { padding: 0 0 19px 13px; border-top: 0; }
  .process-step + .process-step { padding-top: 18px; border-top: 1px solid var(--line); }
  .image-evidence { padding: 8px; }
  .image-time { right: 8px; bottom: 8px; }
  .image-evidence figcaption { display: block; padding: 17px 2px 2px; }
  .image-evidence figcaption .asset-caption { margin-top: 13px; padding: 12px 0 0; border-top: 1px solid rgba(255,255,255,.28); border-left: 0; }
  .takeaway-box { display: block; padding: 22px 18px 20px; }
  .takeaway-box ul { margin-top: 19px; }
  .takeaway-box li { font-size: 14px; }
  .report-footer { padding: 26px 24px 30px; }
  .footer-grid { display: block; }
  .footer-grid > div + div { margin-top: 22px; }
  .footer-bottom { display: block; }
  .footer-bottom span { display: block; }
  .footer-bottom span + span { margin-top: 7px; }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; transition-duration: .01ms !important; scroll-behavior: auto !important; }
}
"""


def render_report(
    plan_path: Path,
    assets_path: Path,
    output_path: Path,
) -> RenderSummary:
    plan = load_plan(plan_path)
    manifest = load_assets(assets_path)
    assets = resolve_assets(assets_path, manifest, plan.video.duration_ms)
    used_asset_ids: set[str] = set()
    for section in plan.sections:
        for block in section.blocks:
            if block.asset_id is not None:
                used_asset_ids.add(block.asset_id)

    section_markup = "".join(
        _render_section(section, index, assets, output_path)
        for index, section in enumerate(plan.sections)
    )
    duration = _format_timestamp(plan.video.duration_ms)
    title = _escape(plan.video.title)
    attribution = _escape(plan.video.attribution)
    source_url = _escape(plan.video.source_url)
    html_document = f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{_escape(plan.hero.tldr)}">
  <title>{title} · Video Visual Report</title>
  <style>{CSS}</style>
</head>
<body>
  <div class="report-page">
    <header class="hero">
      <div class="hero-topline">
        <p class="eyebrow">{_escape(plan.hero.eyebrow)}</p>
        <p class="hero-stamp">V0 / FIELD NOTEBOOK</p>
      </div>
      <h1>{_escape(plan.hero.title)}</h1>
      <p class="hero-thesis">{_escape(plan.hero.tldr)}</p>
      <div class="hero-meta">
        <span>讲者 / <strong>于超</strong></span>
        <span>视频 / <strong>{title}</strong></span>
        <span>时长 / <strong>{duration}</strong></span>
      </div>
    </header>
    <div class="report-body">
      {_render_spine(plan.sections)}
      <main class="story">
        <div class="reading-note">
          <span><strong>读法：</strong>沿着左侧论证脉络，从「为什么」走到「怎样支撑真实世界」。</span>
          <span class="note-tag">{_escape(plan.report_id)} / {len(plan.sections)} CHAPTERS</span>
        </div>
        {section_markup}
      </main>
    </div>
    <footer class="report-footer">
      <div class="footer-grid">
        <div>
          <span class="footer-label">SOURCE / ATTRIBUTION</span>
          <h2>一份本地、可追溯的视觉笔记</h2>
          <p>{attribution}</p>
        </div>
        <div>
          <span class="footer-label">USE / BOUNDARY</span>
          <h2>仅限本地非公开研究</h2>
          <p>本页复用既有 timestamped transcript 与人工选择的本地关键帧；不自动访问来源链接，不构成公开发布或性能结论。来源：{source_url}</p>
        </div>
      </div>
      <div class="footer-bottom">
        <span>VIDEO VISUAL REPORT · RENDERER-FIRST V0</span>
        <span>{_escape(plan.video.video_id)} · {len(used_asset_ids)} local evidence frames</span>
      </div>
    </footer>
  </div>
</body>
</html>
'''

    output_path = output_path.resolve()
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=output_path.parent,
            prefix=f".{output_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_path = Path(handle.name)
            handle.write(html_document)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, output_path)
    except OSError as exc:
        if "temp_path" in locals():
            temp_path.unlink(missing_ok=True)
        raise RenderError("OUTPUT_IO_ERROR", f"cannot write {output_path}") from exc

    block_count = sum(len(section.blocks) for section in plan.sections)
    return RenderSummary(
        report_id=plan.report_id,
        section_count=len(plan.sections),
        block_count=block_count,
        used_asset_count=len(used_asset_ids),
        output_path=output_path,
    )
