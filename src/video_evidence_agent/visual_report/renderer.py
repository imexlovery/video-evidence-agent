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


def _source_refs_data(block: Block) -> str:
    refs = [
        {"segment_id": ref.segment_id, "start_ms": ref.start_ms, "end_ms": ref.end_ms}
        for ref in block.source_refs
    ]
    return _escape(json.dumps(refs, ensure_ascii=False, separators=(",", ":")))


def _source_trace(block: Block) -> str:
    timestamps = " · ".join(_format_timestamp(ref.start_ms) for ref in block.source_refs)
    return (
        f'<div class="source-trace" data-source-refs="{_source_refs_data(block)}">'
        f'<span class="source-label">出处</span>'
        f'<span class="source-times">{_escape(timestamps)}</span>'
        "</div>"
    )


def _render_insight(block: InsightCardBlock) -> str:
    return (
        f'<article class="block insight-card" data-block-type="{block.type}" id="{_escape(block.block_id)}">'
        f'<h3>{_escape(block.headline)}</h3>'
        f'<p>{_escape(block.body)}</p>'
        f"{_source_trace(block)}"
        "</article>"
    )


def _render_bullets(block: BulletGroupBlock) -> str:
    items = "".join(f'<li>{_escape(item)}</li>' for item in block.items)
    return (
        f'<article class="block bullet-group" data-block-type="{block.type}" id="{_escape(block.block_id)}">'
        f'<h3>{_escape(block.headline)}</h3>'
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
        f'<h3>{_escape(block.headline)}</h3>'
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
        f'<h3>{_escape(block.headline)}</h3>'
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
        f'<h3>{_escape(block.headline)}</h3>'
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
    return (
        f'<figure class="block image-evidence" data-block-type="{block.type}" '
        f'data-source-refs="{_source_refs_data(block)}" id="{_escape(block.block_id)}">'
        '<div class="image-frame">'
        f'<img src="{_escape(relative_src)}" alt="{_escape(asset.metadata.alt)}" loading="eager">'
        f'<span class="image-time">{_escape(_format_timestamp(asset.metadata.timestamp_ms))}</span>'
        '</div>'
        '</figure>'
    )


def _render_takeaways(block: TakeawayBoxBlock) -> str:
    items = "".join(f'<li><span>→</span>{_escape(item)}</li>' for item in block.takeaways)
    return (
        f'<article class="block takeaway-box" data-block-type="{block.type}" id="{_escape(block.block_id)}">'
        f'<h3>{_escape(block.headline)}</h3>'
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
        f'<span class="section-number">{index + 1}</span>'
        f'<time datetime="PT{section.timestamp_ms / 1000:.0f}S">{_escape(_format_timestamp(section.timestamp_ms))}</time>'
        '</div>'
        f'<h2>{_escape(section.title)}</h2>'
        '</header>'
        f'<div class="section-blocks">{blocks}</div>'
        '</section>'
    )


CSS = """
:root {
  --ink: #17233B;
  --text: #3C485E;
  --canvas: #EEF2F6;
  --paper: #FFFFFF;
  --purple: #6857C8;
  --blue: #3478C4;
  --coral: #EF6A43;
  --line: #E0E5EC;
  --muted: #758095;
  --soft-purple: #F5F2FF;
  --soft-blue: #F2F7FC;
  --soft-coral: #FFF7EC;
  --radius: 7px;
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
  font-size: 15px;
  line-height: 1.7;
  overflow-x: hidden;
}
body, p, h1, h2, h3, h4, ul, ol, figure { margin: 0; }
ul, ol { padding: 0; list-style: none; }
img { max-width: 100%; }
a { color: inherit; }
a:focus-visible { outline: 3px solid var(--coral); outline-offset: 4px; }
time, .hero-meta, .source-trace, .image-time, .section-marker time { font-family: var(--mono); }

.report-page {
  width: min(1080px, 100%);
  min-height: 100vh;
  margin: 12px auto;
  background: var(--paper);
  border-radius: 10px;
  box-shadow: 0 12px 42px rgba(23, 35, 59, .08);
  overflow: hidden;
}

.hero {
  position: relative;
  padding: 46px 72px 34px;
  color: var(--ink);
  background: var(--paper);
  border-top: 4px solid var(--coral);
  border-bottom: 1px solid var(--line);
}
.hero h1 {
  max-width: 800px;
  font-family: var(--serif);
  font-size: clamp(34px, 4vw, 46px);
  font-weight: 700;
  letter-spacing: -.035em;
  line-height: 1.2;
  text-wrap: balance;
}
.hero-thesis {
  max-width: 820px;
  margin-top: 13px;
  color: var(--text);
  font-size: 17px;
  line-height: 1.75;
}
.hero-meta {
  display: grid;
  grid-template-columns: 130px minmax(0, 1fr) 120px;
  gap: 22px;
  margin-top: 23px;
  padding-top: 14px;
  color: var(--muted);
  border-top: 1px solid var(--line);
  font-size: 10px;
  line-height: 1.5;
}
.hero-meta strong { color: var(--ink); font-weight: 600; }
.hero-meta span { min-width: 0; }

.report-body {
  padding: 0 72px 48px;
}
.story { min-width: 0; }
.story-section { padding: 34px 0 38px; border-bottom: 1px solid var(--line); }
.story-section:last-child { padding-bottom: 10px; border-bottom: 0; }
.section-heading { display: grid; grid-template-columns: 78px minmax(0, 1fr); gap: 15px; align-items: start; }
.section-marker { display: flex; align-items: center; gap: 9px; padding-top: 4px; }
.section-number {
  display: grid;
  place-items: center;
  width: 23px;
  height: 23px;
  flex: 0 0 auto;
  color: var(--paper);
  background: var(--ink);
  border-radius: 50%;
  font: 700 11px/1 var(--mono);
}
.section-marker time { color: var(--coral); font-size: 10px; line-height: 1.2; }
.section-heading h2 { max-width: 700px; font: 700 clamp(23px, 2.8vw, 29px)/1.35 var(--serif); letter-spacing: -.025em; }
.section-blocks { margin-top: 21px; }
.section-blocks > * + * { margin-top: 20px; }
.block { min-width: 0; }
.block h3 { color: var(--ink); font-size: 18px; line-height: 1.45; letter-spacing: -.015em; }

.source-trace {
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 7px;
  margin-top: 11px;
  color: var(--muted);
  font-size: 9px;
  line-height: 1.5;
}
.source-label { color: var(--coral); font-weight: 700; }
.source-times { color: var(--muted); }

.insight-card { padding: 17px 0 1px; border-top: 2px solid var(--coral); }
.insight-card h3 { max-width: 720px; font: 700 22px/1.4 var(--serif); }
.insight-card > p { max-width: 760px; margin-top: 7px; color: var(--text); font-size: 14px; line-height: 1.8; }

.comparison-card { padding: 19px 20px 17px; background: var(--soft-purple); border: 1px solid #E3DCF9; border-radius: var(--radius); }
.comparison-card > h3 { font-family: var(--serif); }
.comparison-columns { display: grid; grid-template-columns: minmax(0, 1fr) 32px minmax(0, 1fr); gap: 12px; align-items: stretch; margin-top: 15px; }
.comparison-side { padding: 14px 15px 13px; border: 1px solid var(--line); border-radius: 6px; background: var(--paper); }
.comparison-side--right { border-color: #D7CEF8; background: #FCFBFF; }
.comparison-label { color: var(--purple); font: 700 11px var(--mono); letter-spacing: .04em; }
.comparison-side--right .comparison-label { color: var(--coral); }
.comparison-side ul { margin-top: 9px; }
.comparison-side li { position: relative; padding-left: 14px; color: var(--text); font-size: 13px; line-height: 1.65; }
.comparison-side li + li { margin-top: 5px; }
.comparison-side li::before { position: absolute; left: 0; top: .72em; width: 5px; height: 2px; content: ""; background: var(--purple); }
.comparison-side--right li::before { background: var(--coral); }
.comparison-arrow { display: grid; place-items: center; color: var(--purple); font: 20px var(--mono); }

.bullet-group { padding: 18px 20px 16px; background: var(--soft-blue); border: 1px solid #DCE8F4; border-radius: var(--radius); }
.bullet-group ul { margin-top: 10px; }
.bullet-group li { position: relative; padding-left: 17px; color: var(--text); font-size: 14px; line-height: 1.7; }
.bullet-group li + li { margin-top: 6px; }
.bullet-group li::before { position: absolute; left: 2px; top: .72em; width: 6px; height: 6px; content: ""; background: var(--blue); border-radius: 50%; }

.metric-row { padding: 18px 20px 16px; border: 1px solid var(--line); border-radius: var(--radius); box-shadow: 0 4px 15px rgba(23, 35, 59, .04); }
.metric-row > h3 { font-family: var(--serif); }
.metric-items { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); margin-top: 14px; }
.metric-item { padding: 1px 16px 0 0; border-right: 1px solid var(--line); }
.metric-item + .metric-item { padding-left: 16px; }
.metric-item:last-child { border-right: 0; }
.metric-item strong { display: block; color: var(--coral); font: 700 clamp(20px, 2.6vw, 28px)/1.15 var(--sans); letter-spacing: -.035em; overflow-wrap: anywhere; }
.metric-item span { display: block; margin-top: 5px; color: var(--ink); font-size: 12px; font-weight: 600; line-height: 1.45; }
.metric-item p { margin-top: 3px; color: var(--muted); font-size: 10px; line-height: 1.45; }

.process-block { padding: 19px 20px 17px; border: 1px solid #E3DCF9; border-radius: var(--radius); background: #FDFDFF; }
.process-block > h3 { font-family: var(--serif); }
.process-visual { position: relative; margin-top: 15px; padding-top: 27px; }
.process-flow-svg { position: absolute; top: -8px; left: 0; width: 100%; height: 88px; overflow: visible; }
.process-line { stroke: #B8C0D2; stroke-width: 2; stroke-dasharray: 1 7; }
.process-arrow { fill: none; stroke: var(--purple); stroke-width: 2; marker-end: url(#process-arrowhead); }
.process-arrowhead { fill: var(--purple); }
.process-node { fill: var(--paper); stroke: var(--purple); stroke-width: 4; }
.process-steps { position: relative; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; }
.process-step { min-width: 0; padding: 19px 8px 0; border-top: 1px solid var(--line); }
.process-number { color: var(--coral); font: 10px var(--mono); }
.process-step h4 { margin-top: 5px; font-size: 14px; line-height: 1.4; }
.process-step p { margin-top: 5px; color: var(--muted); font-size: 11px; line-height: 1.6; overflow-wrap: anywhere; }

.image-evidence { border: 1px solid #CDD5E0; border-radius: var(--radius); background: var(--ink); overflow: hidden; }
.image-frame { position: relative; }
.image-frame img { display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: contain; }
.image-time { position: absolute; right: 9px; bottom: 9px; padding: 5px 8px; color: var(--paper); background: var(--coral); border-radius: 5px; font-size: 10px; line-height: 1; box-shadow: 0 2px 8px rgba(23, 35, 59, .18); }

.takeaway-box { display: grid; grid-template-columns: 150px minmax(0, 1fr); gap: 22px; padding: 19px 20px 17px; background: var(--soft-coral); border: 1px solid #F2DFC2; border-radius: var(--radius); }
.takeaway-box h3 { font-family: var(--serif); }
.takeaway-box li { display: grid; grid-template-columns: 17px minmax(0, 1fr); gap: 6px; color: var(--text); font-size: 13px; line-height: 1.7; }
.takeaway-box li + li { margin-top: 7px; }
.takeaway-box li span { color: var(--coral); font: 15px/1.6 var(--mono); }
.takeaway-box .source-trace { grid-column: 1 / -1; }

.report-footer { padding: 24px 72px 27px; color: var(--muted); background: #F7F9FB; border-top: 1px solid var(--line); }
.footer-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
.report-footer h2 { color: var(--ink); font: 700 15px var(--serif); }
.report-footer p { margin-top: 5px; font-size: 10.5px; line-height: 1.65; overflow-wrap: anywhere; }
.footer-bottom { display: flex; justify-content: space-between; gap: 20px; margin-top: 18px; padding-top: 11px; color: #8D96A7; border-top: 1px solid var(--line); font: 9px/1.5 var(--mono); }

@media (max-width: 700px) {
  html, body { background: var(--paper); }
  .report-page { width: 100%; margin: 0; border-radius: 0; box-shadow: none; }
  .hero { padding: 29px 22px 24px; border-top-width: 4px; }
  .hero h1 { max-width: 100%; font-size: 33px; line-height: 1.23; }
  .hero-thesis { margin-top: 10px; font-size: 15px; line-height: 1.72; }
  .hero-meta { grid-template-columns: 1fr; gap: 5px; margin-top: 17px; padding-top: 11px; font-size: 9px; }
  .report-body { padding: 0 20px 35px; }
  .story-section { padding: 29px 0 32px; }
  .section-heading { grid-template-columns: 1fr; gap: 8px; }
  .section-marker { padding-top: 0; }
  .section-heading h2 { font-size: 24px; line-height: 1.38; }
  .section-blocks { margin-top: 18px; }
  .section-blocks > * + * { margin-top: 17px; }
  .block h3 { font-size: 17px; }
  .insight-card { padding-top: 14px; }
  .insight-card h3 { font-size: 20px; }
  .insight-card > p { font-size: 13.5px; line-height: 1.75; }
  .comparison-card { padding: 16px 15px 14px; }
  .comparison-columns { display: block; margin-top: 12px; }
  .comparison-side { padding: 12px 13px; }
  .comparison-side + .comparison-side { margin-top: 9px; }
  .comparison-arrow { display: block; height: 20px; text-align: center; line-height: 20px; transform: rotate(90deg); }
  .bullet-group { padding: 15px 16px 14px; }
  .bullet-group li { font-size: 13.5px; }
  .metric-row { padding: 15px 14px 13px; }
  .metric-items { margin-top: 11px; }
  .metric-item { padding-right: 9px; }
  .metric-item + .metric-item { padding-left: 9px; }
  .metric-item strong { font-size: 18px; }
  .metric-item span { font-size: 10.5px; }
  .metric-item p { font-size: 9px; }
  .process-block { padding: 16px 15px 14px; }
  .process-visual { margin-top: 12px; padding: 0 0 0 15px; border-left: 2px solid var(--purple); }
  .process-flow-svg { display: none; }
  .process-steps { display: block; }
  .process-step { padding: 0 0 13px 10px; border-top: 0; }
  .process-step + .process-step { padding-top: 12px; border-top: 1px solid var(--line); }
  .process-step p { font-size: 11.5px; }
  .image-time { right: 7px; bottom: 7px; }
  .takeaway-box { display: block; padding: 16px 15px 14px; }
  .takeaway-box ul { margin-top: 10px; }
  .takeaway-box li { font-size: 12.5px; }
  .report-footer { padding: 21px 22px 24px; }
  .footer-grid { display: block; }
  .footer-grid > div + div { margin-top: 15px; }
  .footer-bottom { display: block; }
  .footer-bottom span { display: block; }
  .footer-bottom span + span { margin-top: 5px; }
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
      <h1>{_escape(plan.hero.title)}</h1>
      <p class="hero-thesis">{_escape(plan.hero.tldr)}</p>
      <div class="hero-meta">
        <span>讲者 / <strong>于超</strong></span>
        <span>视频 / <strong>{title}</strong></span>
        <span>时长 / <strong>{duration}</strong></span>
      </div>
    </header>
    <div class="report-body">
      <main class="story">
        {section_markup}
      </main>
    </div>
    <footer class="report-footer">
      <div class="footer-grid">
        <div>
          <h2>来源与署名</h2>
          <p>{attribution}</p>
        </div>
        <div>
          <h2>使用边界</h2>
          <p>本页复用既有 timestamped transcript 与人工选择的本地关键帧；不自动访问来源链接，不构成公开发布或性能结论。来源：{source_url}</p>
        </div>
      </div>
      <div class="footer-bottom">
        <span>本地视频视觉报告 · Renderer-first V0</span>
        <span>{_escape(plan.video.video_id)} · {len(used_asset_ids)} 张关键帧</span>
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
