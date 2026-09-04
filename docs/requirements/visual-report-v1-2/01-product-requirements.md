# Product Requirements

## Problem

The current V1.0 path turns transcript segments into a fixed `ReportPlan` and deterministic report.
It can produce a valid page, but content selection and presentation are too tightly coupled to a
small, fixed block contract. A general coding agent can often create an attractive one-off report,
yet repeated runs vary and its reasoning, browser inspection, and repair behavior are not governed
as a reusable product workflow.

V1.2 must capture the useful editorial and visual-review loop of that experience while making the
quality floor, authority boundaries, evidence, and stopping behavior explicit.

## User and allowed use

The primary user is the named local Owner operating the repository on a bounded machine. The target
grade is `G2 CONTROLLED_PILOT`: real local video/transcript data is allowed under close oversight,
but no public or multi-user service promise is made.

Permitted use:

- generate and inspect a private local report from supported MP4 or public Bilibili ingest;
- compare V1.2 with the existing local V1.0 path;
- use development samples for calibration and untuned samples for later formal evaluation;
- manually accept, reject, export, or delete local artifacts.

Prohibited release claims and uses:

- public publishing or redistribution by the Harness;
- arbitrary document-to-report conversion;
- multilingual product-quality claims;
- autonomous external actions;
- public API, accounts, multi-tenancy, hosted service, or commercial availability;
- treating a run status as factual or visual Owner acceptance.

## Job to be done

Given a valid V1.1 Canonical Transcript, produce a coherent visual report that a reader who did not
watch the video can understand independently, while retaining a complete source trail and exposing
whether the run completed normally, delivered with a bounded limitation, or failed.

## Fixed Editorial Objective

> 让未观看原视频的读者能够独立理解视频的主要结论、论证脉络、关键依据和重要限制。

V1.2 exposes no Editorial Brief and does not request audience, reading goal, depth, content style,
or visual style before generation. An optional free-text Editorial Instruction is only a future
V1.3 candidate.

## Product principles

1. **Source before fluency.** Plausible unsupported prose is worse than a visible omission.
2. **Editorial before presentation.** The report's meaning is settled before visual expression.
3. **Controlled variety.** The model may compose legal presentation primitives, but may not design
   an arbitrary page language.
4. **Observe reality.** Visual review reads an actual browser render, not only a plan.
5. **Repair locally and stop.** Revisions are defect-routed and finite, not open-ended polishing.
6. **Retain the process.** Every model and deterministic stage consumes and emits inspectable
   Artifacts.
7. **Optimize the floor.** Reproducibility means stable contracts and reduced unacceptable-run
   rate, not byte-identical prose.

## In-scope capabilities

- consume one complete V1.1 Canonical Transcript of at most 50,000 Unicode characters;
- build a minimal evidence-backed Claim Graph;
- turn Claims into final reader-facing Editorial Content and an adaptive ordered narrative;
- validate/review Semantic output explicitly;
- turn Editorial Content into a Presentation Plan using one Design System and controlled
  Presentation Vocabulary;
- optionally bind supplied local images without discovering or generating images;
- deterministically render the fixed-width 1080px desktop Canonical Report;
- collect a real screenshot and minimum DOM geometry/overflow/clipping evidence;
- visually review the actual result;
- perform at most two same-layer Revisions, including no more than one Semantic Revision;
- retain the full Run Bundle and a terminal outcome.

## Explicit non-goals

- transcript repair, hidden transcript normalization, long-transcript chunking, or external RAG;
- automatic keyframe extraction, full-video visual understanding, image search, or image generation;
- free ReAct, browser-control, tool-selection, or multi-agent behavior;
- arbitrary HTML/CSS/SVG paths, colors, coordinates, or user-authored page DSL;
- multiple named styles or Presentation Profiles;
- mobile visual-quality certification;
- redesigning the Web Shell;
- role-specific models, model routing, model fallback, or provider fallback;
- LangGraph, Hypha, MCP orchestration, or general workflow infrastructure;
- database, remote storage, authentication, authorization, tenancy, billing, deployment, or support
  operation.

## User-visible contract

The user starts a V1.2 run from an existing local entry point, sees understandable progress, and can
open the Candidate Report when the run is `COMPLETE` or `DEGRADED`. A `FAILED` run exposes a concise
reason and retains diagnostic Artifacts without presenting an invalid report as deliverable.

The Web Shell remains an entry/status/open surface. Its appearance is not part of V1.2 report
quality. The Canonical Report is the 1080px desktop HTML page; mobile rendering is best-effort and
does not affect `COMPLETE`.

## Success definition

A successful V1.2 design and implementation must demonstrate:

- end-to-end provenance for every substantive reader-facing unit;
- no Presentation-authored semantic content;
- valid adaptive report structure without mandatory component quotas;
- deterministic rendering and mandatory 1080px Browser Observation;
- finite, auditable retry and Revision behavior;
- no hidden resampling or fallback;
- lower worst-case failure and unacceptable-run behavior than the no-Revision ablation, without
  sacrificing source trust;
- an inspectable difference from a prompt-only system: typed Artifacts, deterministic validators,
  real rendered evidence, bounded control, and replayable Run Bundles.

Exact vocabulary breadth, safety ceilings, evaluation sample count, repeat count, and the numerical
quality threshold are calibration-owned Final Spec parameters. Formal evaluation cannot begin
until the Owner freezes those values.

## Promotion path

The Design Baseline authorizes no construction. After separate implementation authority, the path
is minimal vertical loop → calibration → Architecture Ablation → Owner Final Spec freeze → locked
evaluation → Owner product acceptance → optional Owner default-path promotion. V1.3 may then assess
Editorial Instruction, productization, public-service boundaries, mobile commitments, and any
evidence-backed Presentation Profiles.
