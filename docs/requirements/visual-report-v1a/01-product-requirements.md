# Video Visual Report V1-A — Product Requirements

## Problem and evidence

V0 established that structured content, typed blocks, and one deterministic
renderer can produce a product-quality visual report. The remaining manual
bottleneck is the Report Plan. V1-A asks whether full timestamped transcripts
can be mapped for coverage and then compressed into renderer-ready content at
approximately the quality of the hand-authored V0 plan.

## Selected implementation grade and boundary

`G1 PROTOTYPE`, confirmed by the Owner. One local user may run the three
authorized transcripts through the configured external OpenAI-compatible text
model. The results are local candidates and Development measurement evidence,
not production, public, or commercially reliable outputs.

## Users and service model

| Actor | Situation | Need | Access/authority |
|---|---|---|---|
| Owner/learner | Wants a report without hand-authoring JSON | Accurate structure, prioritization, traceability, useful rendered result | Local files; accepts/rejects quality |
| Implementer | Builds and evaluates V1-A | Fixed schemas, prompts, deterministic gates, bounded test population | Local repository; cannot self-promote |
| External text provider | Executes exactly two configured calls per successful run | Bounded transcript/task payload | Receives authorized transcript text; no media or credentials in prompts |

There are no customers, tenants, accounts, hosted users, entitlements, billing,
support promises, or service-level commitments.

## Goals and success measures

| ID | Goal | Measure | Owner-confirmed G1 target |
|---|---|---|---|
| `GOAL-VR1A-001` | Map the whole transcript before selection | Human coverage card and deterministic segment accounting | Every segment accounted for; ≥90% required-topic recall; no must-cover miss |
| `GOAL-VR1A-002` | Produce a useful compressed Report Plan | Owner prioritization and narrative rubric | 3–5 sections, 8–14 blocks, ≥4/5 prioritization per video |
| `GOAL-VR1A-003` | Prevent hallucination/overclaim | Source validation and human entailment review | 100% block refs valid; zero major unsupported claim/metric |
| `GOAL-VR1A-004` | Avoid a generic fixed template | Cross-video structural signature and block-affordance review | Not all three plans share one normalized structure; every special block is justified |
| `GOAL-VR1A-005` | Preserve the V0 rendering contract | Existing `ReportPlan` validation and renderer | All accepted plans render without V0 schema/renderer change |
| `GOAL-VR1A-006` | Make the experiment auditable | Run manifests, call traces, retained failures | Two repeat runs per video; all attempts remain in evidence |

The Owner confirmed these targets through `DEC-VR1A-049`; changes require a new
append-only decision and a new measurement revision.

## First-release scope

### Included

- Input: one existing ingest manifest and ordered `VideoSegment` JSONL.
- Topic Mapper: one full-transcript, coverage-oriented model call.
- Deterministic Topic Map validation, segment accounting, and timestamp binding.
- Report Planner: one full-transcript + Topic Map, compression-oriented model call.
- Deterministic proposal validation and compilation into the existing V0 plan.
- Text-only report output using an empty `assets.json`; no `image_caption` block.
- Append-only local run artifacts and a three-video Development measurement.

### Explicit non-goals

MP4/ASR, keyframes/assets, OCR/VLM, retrieval/RAG, Agent/LangGraph/tools,
multi-agent execution, database/cache/queue, background processing, API/UI,
URL download, multi-video synthesis, free layout, new renderer/template,
publishing, production hardening, online learning, or prompt self-modification.

## Product requirements

| ID | Requirement | Rationale | Priority | Evidence | Acceptance |
|---|---|---|---|---|---|
| `REQ-VR1A-001` | The system must accept one validated manifest and ordered `VideoSegment` JSONL without changing them | Reuse the stable transcript contract | P0 | Repository baseline | `TEST-VR1A-001` |
| `REQ-VR1A-002` | Topic Mapper and Report Planner must remain separate, exactly one admitted model call each on a successful run | Coverage and compression have different objectives | P0 | Owner document | `TEST-VR1A-002` |
| `REQ-VR1A-003` | Topic Mapper must account for every input segment through one primary topic or an explicit exclusion | Makes omission visible | P0 | Owner-approved design | `TEST-VR1A-003` |
| `REQ-VR1A-004` | Topic Mapper must not choose renderer block types, report priority, or final omissions | Preserves role separation | P0 | Owner document | `TEST-VR1A-004` |
| `REQ-VR1A-005` | Planner must receive the canonical Topic Map and full transcript, select/omit topics explicitly, and emit only typed semantic content | Prevents lossy handoff and hidden omission | P0 | Owner-approved design | `TEST-VR1A-005` |
| `REQ-VR1A-006` | Models must select existing segment IDs only; deterministic code must supply timestamps and IDs | Eliminates invented time ranges | P0 | Source-traceability goal | `TEST-VR1A-006` |
| `REQ-VR1A-007` | Every factual block must compile to one to four canonical `source_refs` | Matches V0 contract | P0 | Existing schema | `TEST-VR1A-007` |
| `REQ-VR1A-008` | Unknown IDs, incomplete segment accounting, unsupported metrics, extra fields, invalid budgets, or incompatible blocks must fail visibly | Prevents polished invalid reports | P0 | Safety floor | `TEST-VR1A-008` |
| `REQ-VR1A-009` | V1-A must not semantically auto-repair invalid model output or silently make a third call | Preserves evidence and two-call claim | P0 | Owner-approved design | `TEST-VR1A-009` |
| `REQ-VR1A-010` | The compiler must emit the current `visual-report.v0-prototype` plan and an empty current asset manifest | Reuses renderer unchanged | P0 | Existing contract | `TEST-VR1A-010` |
| `REQ-VR1A-011` | The model must not emit HTML, CSS, SVG, layout, colors, coordinates, type sizes, asset paths, or arbitrary grids | Renderer remains authoritative | P0 | Owner document | `TEST-VR1A-011` |
| `REQ-VR1A-012` | Prompt and model configuration, usage, latency, call count, schema status, and failure category must be recorded without credentials | Makes runs inspectable | P0 | G1 evidence need | `TEST-VR1A-012` |
| `REQ-VR1A-013` | Every run, including failure/cancellation, must have a unique directory and must not overwrite another run | Honest evidence denominator | P0 | Owner-approved design | `TEST-VR1A-013` |
| `REQ-VR1A-014` | V1-A quality must be measured on Kling, RLinf, and Wu Yi using one frozen prompt/model/config, with two runs per video | Tests stability and content variation | P0 | Owner three-video request | `TEST-VR1A-014` |
| `REQ-VR1A-015` | The implementation must preserve V0 renderer behavior and frozen P0-B inputs/evaluation history | Avoids experiment contamination | P0 | Repository contract | `TEST-VR1A-015` |
| `REQ-VR1A-016` | Implementation must stop for Owner review and must not start V1-B/C | Maintains phase authority | P0 | Owner scope | `TEST-VR1A-016` |

## Constraints and dependencies

- Existing Python `>=3.12,<3.13`, uv, Pydantic, OpenAI SDK, V0 models/renderer.
- Explicit model configuration; no implicit provider/model fallback.
- Full transcript payload is authorized and has no expected private data.
- Source media and generated reports remain local/non-public where current rights require it.
- Intended input is Chinese technical/knowledge content around 10–30 minutes;
  Kling and RLinf are named approximately 34-minute G1 exceptions.
- One foreground run at a time; no queue or concurrent execution contract.

## Glossary

- **Topic Map:** coverage-oriented, ordered source structure in which every
  transcript segment is accounted for.
- **Report Plan Proposal:** model output containing semantic content and source
  segment IDs; not yet a renderer contract.
- **Canonical binding:** deterministic replacement of selected segment IDs with
  exact stored timestamps and generated stable IDs.
- **Compilation:** deterministic conversion from validated proposal to current
  V0 `ReportPlan`.
- **Development measurement:** versioned local experimental evidence; not
  Freeze, Locked Eval, release, or production acceptance.
- **Major overclaim:** a central, numeric, causal, comparative, or evaluative
  assertion not supported by its cited transcript segments.
