"""Command line entry point for the local Video Visual Report V0 renderer."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .evaluation import (
    evaluate_measurement,
    finalize_provider_conformance,
    freeze_measurement,
    freeze_provider_conformance,
    freeze_semantic_v2_product_prototype,
    load_provider_conformance_strategy,
    review_semantic_v2_product_prototype,
)
from .planning import PlanningError
from .planning_runtime import (
    build_from_transcript,
    build_from_transcript_v2,
    replay_semantic_v2_proposals,
)
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
    build_v2 = commands.add_parser(
        "build-from-transcript-v2",
        help="build one current semantic-v2 product-prototype report",
    )
    build_v2.add_argument("--manifest", required=True, type=Path)
    build_v2.add_argument("--segments", required=True, type=Path)
    build_v2.add_argument("--run-id", required=True)
    build_v2.add_argument("--output-root", required=True, type=Path)
    freeze_product = commands.add_parser(
        "freeze-product-prototype",
        aliases=["freeze-semantic-v2-product"],
        help="freeze the current three-video semantic-v2 product prototype set",
    )
    freeze_product.add_argument("--repository-root", type=Path, default=Path("."))
    freeze_product.add_argument("--source-root", type=Path)
    freeze_product.add_argument(
        "--artifact-root", type=Path, default=Path("artifacts/visual-report/v1a")
    )
    freeze_product.add_argument(
        "--card-root", type=Path, default=Path("eval/visual-report-v1a/review-cards")
    )
    freeze_product.add_argument(
        "--output",
        type=Path,
        default=Path("eval/visual-report-v1a/semantic-v2-product-manifest.json"),
    )
    review_product = commands.add_parser(
        "review-product-prototype",
        help="emit deterministic semantic-v2 review artifacts and pending Owner rubrics",
    )
    review_product.add_argument("--manifest", required=True, type=Path)
    review_product.add_argument(
        "--output-root", type=Path, default=Path("artifacts/visual-report/v1a/evaluation")
    )
    replay_v2 = commands.add_parser(
        "replay-semantic-v2",
        help="replay two accepted semantic-v2 proposals with zero provider calls",
    )
    replay_v2.add_argument("--manifest", required=True, type=Path)
    replay_v2.add_argument("--segments", required=True, type=Path)
    replay_v2.add_argument("--topic-proposal", required=True, type=Path)
    replay_v2.add_argument("--plan-proposal", required=True, type=Path)
    replay_v2.add_argument("--output-dir", required=True, type=Path)
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
    if args.command in {"freeze-product-prototype", "freeze-semantic-v2-product"}:
        try:
            manifest = freeze_semantic_v2_product_prototype(
                repository_root=args.repository_root,
                source_root=args.source_root,
                artifact_root=args.artifact_root,
                card_root=args.card_root,
                output_path=args.output,
            )
        except PlanningError as exc:
            print(f"{exc.category}: {exc.message}", file=sys.stderr)
            return 2
        print(
            f"Frozen {manifest.revision_id}: status={manifest.status}, "
            f"declared_runs={len(manifest.runs)}, output={args.output}"
        )
        return 0
    if args.command == "review-product-prototype":
        try:
            aggregate = review_semantic_v2_product_prototype(
                manifest_path=args.manifest,
                output_root=args.output_root,
            )
        except PlanningError as exc:
            print(f"{exc.category}: {exc.message}", file=sys.stderr)
            return 2
        print(
            f"Reviewed {aggregate['manifest_revision_id']}: "
            f"status={aggregate['stop_state']}, conclusion={aggregate['conclusion']}, "
            f"output={args.output_root / str(aggregate['manifest_revision_id'])}"
        )
        return 0
    if args.command == "replay-semantic-v2":
        try:
            topic_payload = json.loads(args.topic_proposal.read_text(encoding="utf-8"))
            plan_payload = json.loads(args.plan_proposal.read_text(encoding="utf-8"))
            if not isinstance(topic_payload, dict) or not isinstance(plan_payload, dict):
                raise PlanningError("INPUT_ERROR", "proposal files must contain JSON objects")
            summary = replay_semantic_v2_proposals(
                manifest_path=args.manifest,
                segments_path=args.segments,
                topic_proposal_payload=topic_payload,
                plan_proposal_payload=plan_payload,
                output_dir=args.output_dir,
            )
        except (OSError, json.JSONDecodeError) as exc:
            print(f"INPUT_ERROR: {exc}", file=sys.stderr)
            return 2
        except PlanningError as exc:
            print(f"{exc.category}: {exc.message}", file=sys.stderr)
            return 2
        print(
            f"Replayed semantic-v2: provider_calls/model_calls={summary.provider_calls}/"
            f"{summary.model_calls}, report={args.output_dir / 'report.html'}"
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
    if args.command == "build-from-transcript-v2":
        try:
            summary = build_from_transcript_v2(
                manifest_path=args.manifest,
                segments_path=args.segments,
                run_id=args.run_id,
                output_root=args.output_root,
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
