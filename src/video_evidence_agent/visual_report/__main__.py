"""Command line entry point for the local Video Visual Report V0 renderer."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .renderer import RenderError, render_report


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m video_evidence_agent.visual_report")
    commands = parser.add_subparsers(dest="command", required=True)
    render = commands.add_parser("render", help="render one validated report plan")
    render.add_argument("--plan", required=True, type=Path)
    render.add_argument("--assets", required=True, type=Path)
    render.add_argument("--output", required=True, type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command != "render":
        return 2
    try:
        summary = render_report(args.plan, args.assets, args.output)
    except RenderError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(
        f"Rendered {summary.report_id}: "
        f"{summary.section_count} sections, {summary.block_count} blocks, "
        f"{summary.used_asset_count} used assets -> {summary.output_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
