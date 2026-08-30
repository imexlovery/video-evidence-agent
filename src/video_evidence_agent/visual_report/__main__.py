"""Command line entry point for the local Video Visual Report V0 renderer."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .evaluation import (
    evaluate_measurement,
    finalize_provider_conformance,
    freeze_measurement,
    freeze_provider_conformance,
    load_provider_conformance_strategy,
)
from .planning import PlanningError
from .planning_runtime import build_from_transcript
from .renderer import RenderError, render_report


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m video_evidence_agent.visual_report")
    commands = parser.add_subparsers(dest="command", required=True)
    render = commands.add_parser("render", help="render one validated report plan")
    render.add_argument("--plan", required=True, type=Path)
    render.add_argument("--assets", required=True, type=Path)
    render.add_argument("--output", required=True, type=Path)
    build = commands.add_parser(
        "build-from-transcript", help="build one V1-A report from an ingested transcript"
    )
    build.add_argument("--manifest", required=True, type=Path)
    build.add_argument("--segments", required=True, type=Path)
    build.add_argument("--run-id", required=True)
    build.add_argument("--output-root", required=True, type=Path)
    build.add_argument("--strategy-manifest", required=True, type=Path)
    build.add_argument("--strategy-id", required=True)
    conformance = commands.add_parser(
        "freeze-provider-conformance",
        help="freeze eligible native provider strategies and canary identities",
    )
    conformance.add_argument("--repository-root", type=Path, default=Path("."))
    conformance.add_argument(
        "--artifact-root", type=Path, default=Path("artifacts/visual-report/v1a")
    )
    conformance.add_argument(
        "--card-root", type=Path, default=Path("eval/visual-report-v1a/review-cards")
    )
    conformance.add_argument(
        "--output",
        type=Path,
        default=Path("eval/visual-report-v1a/provider-conformance-manifest.json"),
    )
    finalize = commands.add_parser(
        "finalize-provider-conformance",
        help="record immutable canary outcomes without changing the frozen manifest",
    )
    finalize.add_argument("--manifest", required=True, type=Path)
    finalize.add_argument("--artifact-root", required=True, type=Path)
    finalize.add_argument("--output", required=True, type=Path)
    freeze = commands.add_parser(
        "freeze-measurement", help="freeze V1-A sources, cards, configuration, and six run IDs"
    )
    freeze.add_argument("--repository-root", type=Path, default=Path("."))
    freeze.add_argument("--artifact-root", type=Path, default=Path("artifacts/visual-report/v1a"))
    freeze.add_argument(
        "--card-root", type=Path, default=Path("eval/visual-report-v1a/review-cards")
    )
    freeze.add_argument(
        "--output", type=Path, default=Path("eval/visual-report-v1a/measurement-manifest.json")
    )
    freeze.add_argument("--strategy-manifest", type=Path)
    freeze.add_argument("--strategy-id")
    evaluate = commands.add_parser(
        "evaluate", help="evaluate every declared V1-A run and emit deterministic/rubric artifacts"
    )
    evaluate.add_argument("--measurement-manifest", required=True, type=Path)
    evaluate.add_argument(
        "--output-root", type=Path, default=Path("artifacts/visual-report/v1a/evaluation")
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "render":
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
    if args.command == "freeze-measurement":
        if (args.strategy_manifest is None) != (args.strategy_id is None):
            print(
                "CONFIGURATION_ERROR: strategy manifest and strategy ID must be provided together",
                file=sys.stderr,
            )
            return 2
        try:
            manifest = freeze_measurement(
                repository_root=args.repository_root,
                artifact_root=args.artifact_root,
                card_root=args.card_root,
                output_path=args.output,
                strategy_manifest_path=args.strategy_manifest,
                strategy_id=args.strategy_id,
            )
        except PlanningError as exc:
            print(f"{exc.category}: {exc.message}", file=sys.stderr)
            return 2
        print(
            f"Frozen {manifest.revision_id}: status={manifest.status}, "
            f"declared_runs={len(manifest.runs)}, output={args.output}"
        )
        return 0
    if args.command == "freeze-provider-conformance":
        try:
            manifest = freeze_provider_conformance(
                repository_root=args.repository_root,
                artifact_root=args.artifact_root,
                card_root=args.card_root,
                output_path=args.output,
            )
        except PlanningError as exc:
            print(f"{exc.category}: {exc.message}", file=sys.stderr)
            return 2
        print(
            f"Frozen provider conformance {manifest['revision_id']}: "
            f"status={manifest['status']}, strategies={len(manifest['strategies'])}, "
            f"output={args.output}"
        )
        return 0
    if args.command == "finalize-provider-conformance":
        try:
            result = finalize_provider_conformance(
                manifest_path=args.manifest,
                artifact_root=args.artifact_root,
                output_path=args.output,
            )
        except PlanningError as exc:
            print(f"{exc.category}: {exc.message}", file=sys.stderr)
            return 2
        print(
            f"Provider conformance {result['terminal_status']}: "
            f"conclusion={result['conclusion']}, output={args.output}"
        )
        return 0
    if args.command == "evaluate":
        try:
            aggregate = evaluate_measurement(
                measurement_path=args.measurement_manifest,
                output_root=args.output_root,
            )
        except PlanningError as exc:
            print(f"{exc.category}: {exc.message}", file=sys.stderr)
            return 2
        print(
            f"Evaluated {aggregate['revision_id']}: "
            f"measurement_valid={aggregate['measurement_valid']}, "
            f"conclusion={aggregate['conclusion']}, "
            f"output={args.output_root / str(aggregate['revision_id'])}"
        )
        return 0
    try:
        strategy = load_provider_conformance_strategy(args.strategy_manifest, args.strategy_id)
        summary = build_from_transcript(
            manifest_path=args.manifest,
            segments_path=args.segments,
            run_id=args.run_id,
            output_root=args.output_root,
            strategy=strategy,
        )
    except PlanningError as exc:
        print(f"{exc.category}: {exc.message}", file=sys.stderr)
        return 130 if exc.category == "CANCELLED" else 2
    print(
        f"Built {summary.run_id}: state={summary.state}, "
        f"provider_calls/model_calls={summary.provider_calls}/{summary.model_calls}, "
        f"sections={summary.section_count}, blocks={summary.block_count}, "
        f"report={summary.report_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
