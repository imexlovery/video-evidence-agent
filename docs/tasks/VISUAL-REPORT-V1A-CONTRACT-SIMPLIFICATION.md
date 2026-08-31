# Video Visual Report V1-A — Product Prototype Goal

## Task identity

| Field | Value |
|---|---|
| Task ID | `VR-V1A-CONTRACT-SIMPLIFICATION-006` |
| Product stage | `V1-A — Automated Content Planning Product Prototype` |
| Grade | `G1 PROTOTYPE` |
| Contract status | `OWNER_CONFIRMED` via `DEC-VR1A-061` |
| Execution status | `NOT_STARTED` — this documentation session does not implement or call a model |
| Execution mode | One continuous Goal; automatically repair ordinary in-scope engineering defects and stop only at the terminal states below |
| Frozen starting baseline | `e72503f5b20831c1e86a1b72c93fb4c4f7debe2a` on branch `visual-report`, plus the current documentation package |
| Provider boundary | One existing Owner-provisioned DeepSeek text-model/API tuple |
| Product sample | Kling, RLinf, and Wu Yi; one retained product-prototype run per video |
| Base/maximum provider calls | `6 / 9`: two stage calls per run plus at most one technical retry per run |
| Normal completion | `READY_FOR_OWNER_V1A_REVIEW — PROTOTYPE_REPORTS_READY` |

## Product positioning

V1-A is a product-prototype validation, not a Provider/Schema conformance
experiment. It must answer:

> Can `Semantic Proposal → Deterministic Compiler → V0 Renderer` automatically
> produce three grounded, useful, visually reviewable reports whose editorial
> structure fits three different videos?

Provider transport, JSON parsing, schema-first-hit rate, and normalization
counts remain diagnostic evidence. They do not replace product evidence and do
not by themselves decide whether the Visual Report direction is viable.

Historical strict-schema, recovery, provider-conformance, and cancelled Route A
artifacts remain immutable. Their conclusions describe those experiments only.

## User-visible prototype flow

```text
three authorized transcript fixtures
  -> Call 1: Topic Mapper semantic proposal
  -> deterministic Topic Resolver
  -> canonical Topic Map + coverage diagnostics
  -> Call 2: Report Planner semantic proposal
  -> deterministic non-semantic compiler
  -> current V0 ReportPlan + empty AssetManifest
  -> unchanged V0 Renderer
  -> report.html
  -> desktop/mobile screenshots + content/visual review package
  -> Owner product-prototype review
```

The target outputs are three complete local reports, not proof that DeepSeek
can satisfy a complex provider-side JSON Schema on its first response.

## Fixed invariants

- Topic Mapper and Report Planner remain two sequential, independent semantic
  model stages.
- Both stages receive the complete authorized transcript. Planner also receives
  the canonical Topic Map.
- Model output is advisory semantic content. It may select only existing source
  segment IDs and canonical Topic Map IDs.
- Deterministic code owns canonical IDs, timestamps, `SourceRef`, final block
  compatibility, V0 validation, compilation, run state, evidence, and renderer
  invocation.
- Final output remains the current V0 `ReportPlan`, an empty current
  `AssetManifest`, and the existing deterministic renderer. V1-A creates no
  image asset.
- Every run and every attempt has a unique retained identity. Raw output,
  normalized structure, compiler omissions, failures, retries, screenshots,
  and review artifacts remain inspectable.
- No alternate provider/model fallback, third semantic stage, model repair
  call, per-video prompt, prompt micro-version loop, hidden transcript
  truncation/chunking, manual fallback plan, or V0 content leakage is allowed.
- Historical V0/P0-B/V1-A evidence and protected paths remain unchanged.

## Semantic-v2 proposal contracts

### Topic Mapper proposal

```json
{
  "schema_version": "visual-topic-map-proposal.v1a-semantic-v2",
  "topics": [
    {
      "title": "内容驱动的主题标题",
      "summary": "仅由 transcript 支持的主题摘要",
      "importance": "primary",
      "start_segment_id": "p0b-example-seg-003",
      "end_segment_id": "p0b-example-seg-008",
      "representative_segment_ids": [
        "p0b-example-seg-004",
        "p0b-example-seg-007"
      ]
    }
  ]
}
```

Mapper performs semantic topic recognition, grounded summarization, importance
judgment, approximate span selection, and representative-evidence selection.
It does not create an exact segment partition, exclusions, subtopics, report
blocks, timestamps, or canonical IDs.

### Topic Resolver

The deterministic resolver may:

- trim non-semantic whitespace and remove blank optional values;
- remove unknown or duplicate IDs and restore transcript order;
- bind valid start/end IDs to one inclusive span;
- derive missing span endpoints from the earliest/latest valid representative
  ID selected by the model;
- assign canonical topic IDs, timestamps, and `SourceRef` values;
- sort topics by first source ordinal while preserving stable tie order;
- remove byte-for-byte duplicate topic objects; and
- expose proposed/usable topic counts, representative/span coverage, uncovered
  segments, overlap, and every rule application.

It may not add, rewrite, combine, split, or infer a topic title, summary,
importance judgment, or new evidence ID. A topic with no semantic content or no
valid model-selected source ID is omitted with evidence. No usable topic stops
the run before Planner.

### Report Planner proposal

```json
{
  "schema_version": "visual-report-plan-proposal.v1a-semantic-v2",
  "hero": {
    "title": "报告标题",
    "tldr": "核心判断",
    "source_segment_ids": ["p0b-example-seg-007"]
  },
  "sections": [
    {
      "title": "章节标题",
      "topic_ids": ["topic-001"],
      "content_units": [
        {
          "suggested_block_type": "bullet_group",
          "headline": "这一部分讲什么",
          "body": null,
          "items": ["要点一", "要点二"],
          "left_label": null,
          "left_items": [],
          "right_label": null,
          "right_items": [],
          "metrics": [],
          "source_segment_ids": ["p0b-example-seg-007"]
        }
      ]
    }
  ]
}
```

Planner performs editorial selection, narrative organization, wording,
evidence selection, and block-affordance suggestion. It does not emit final
section/block IDs, timestamps, `SourceRef`, layout, style, HTML/CSS/SVG,
assets, or final canonical typed-block objects.

## Deterministic compiler boundary

Every compiler transformation must be replayable and written in order to
`normalization.json`. The compiler governs structure; it does not edit the
model's semantics.

### Allowed non-semantic governance

- Parse exactly one JSON object; trim whitespace; ignore unknown fields; apply
  empty defaults only to optional presentation lists/null fields.
- Remove blank optional list entries and exact duplicate IDs/objects.
- Remove unknown source/topic IDs, restore source order, and cap final source
  refs at the current V0 maximum of four.
- Require Hero and every retained content unit to keep at least one valid
  model-selected segment ID.
- Assign canonical IDs, timestamps, `SourceRef`, metadata, and compiler-owned
  omission reasons.
- Map a complete model-supplied content shape to the safest compatible current
  V0 block type without changing its text:
  - cited values that occur verbatim in cited transcript text may become
    `metric_row`;
  - two complete supplied sides may become `comparison_card`;
  - supplied ordered process items may become `process_flow`, with only
    deterministic ordinal labels such as `步骤 1`;
  - supplied item lists may become `bullet_group` or a final
    `takeaway_box`;
  - supplied body text may become `insight_card`.
- Omit an unusable topic, section, or content unit as one whole semantic unit
  and record the exact reason. Omission is visible evidence and counts against
  content quality.
- Preserve model section/unit order. Admit only values already within current
  V0 field and aggregate limits; an over-limit semantic value is not silently
  truncated or rewritten.

### Prohibited semantic transformation

The resolver/compiler must not:

- paraphrase, correct, expand, shorten, or otherwise rewrite semantic text;
- merge two topics, sections, claims, item lists, or content units;
- split one topic, section, claim, item list, or content unit into several;
- create a missing title, summary, claim, item, metric, comparison side,
  process step, source ID, topic, section, or block;
- move text between semantic units to satisfy a count or budget;
- use the hand-authored V0 plan as generated content; or
- call a model to repair or continue another response.

After whole-unit omission, the proposal must already provide 3–5 usable,
nonempty sections and at least three grounded content units. Otherwise it is a
product-pipeline failure, not something the compiler may repair semantically.

## Explicit single technical retry

The application, not the SDK, owns one retry budget per pipeline run. SDK
automatic retries remain disabled.

The current failed stage may be attempted one additional time only when the
first attempt ends in one of these technical categories:

- connection failure, timeout, HTTP `429`, or provider `5xx`;
- empty response content;
- provider-declared incomplete/truncated generation; or
- malformed/non-decodable JSON where no semantic object can be admitted.

The retry must use the identical provider, model, API surface, prompt,
transcript, Topic Map when applicable, parameters, and compiler version. It
must record the original failure, stage, trigger category, attempt numbers,
latency, usage, and both raw responses. It may not include corrective semantic
instructions or learn from the failed body.

No retry is allowed for a valid JSON semantic proposal that is weak,
unsupported, poorly organized, missing valid evidence, outside V0 product
limits, or rejected by the semantic compiler. Retry exhaustion yields a
technical-inconclusive run, not a product-route No-Go.

Per run:

- ordinary success: Mapper + Planner = `2` calls;
- one eligible technical retry at either stage = at most `3` calls;
- no run can retry both stages or exceed `3` provider calls.

## Continuous Goal execution

### G0 — Preserve and implement the confirmed contract

1. Preserve every historical revision/run/result and the cancelled Route A
   card.
2. Add versioned semantic-v2 proposal models, Topic Resolver, deterministic
   compiler/normalization ledger, stable error/retry categories, and replay.
3. Keep v1 schemas and historical results immutable.
4. Synchronize V1-A task/status/requirements evidence in the same Goal.

### G1 — Provider-free product-path admission

Before a real call, automatically repair ordinary in-scope engineering defects
until:

- valid/boundary/invalid Mapper and Planner fixtures pass;
- every allowed structural rule and every prohibited semantic transformation
  has an exact test;
- retry eligibility, single-budget enforcement, identical-request replay, and
  both-attempt evidence pass with local fakes;
- saved successful and failed responses replay with `0/0` calls;
- a synthetic semantic proposal compiles/renders through the current V0 path;
- current V0 regression, protected/history preservation, targeted/full pytest,
  Ruff, and diff hygiene pass; and
- one DeepSeek/model/API/prompt/compiler/source snapshot and three product-run
  IDs are frozen.

### G2 — Build the three-video product prototype

Execute Kling, RLinf, and Wu Yi once each with the same frozen configuration.
Each retained run may use its one technical retry under the rules above. Do not
tune or change prompt/model/compiler behavior between videos.

Continue the remaining predeclared videos after an individual technical or
content failure when credentials, source authority, and configuration remain
available. A failed earlier video is retained, never replaced.

An implementation-only defect discovered after a provider response may be
fixed and the retained raw response replayed with `0/0` calls only when the fix
does not alter provider input or semantic content. A change that would alter
the prompt, model request, semantic proposal, or retry eligibility invalidates
the frozen product set and stops for Owner direction; it does not silently
start a new experiment.

### G3 — Render and visually inspect the product

For every successful run:

1. validate the current V0 `ReportPlan` and empty `AssetManifest`;
2. render canonical `report.html` through the existing renderer;
3. inspect a real browser view at the 1080 px desktop design viewport;
4. inspect an approximately 390 px mobile viewport;
5. retain desktop/mobile screenshots and record clipping, overlap, horizontal
   overflow, typography, hierarchy, density, source readability, and block
   affordance observations; and
6. fix only ordinary renderer/compiler defects inside the allowed V1-A/V0
   compatibility boundary, without rewriting report semantics.

### G4 — Product review package and stop

Create one prototype review package containing:

- all three Topic Maps, final plans, reports, and six viewport screenshots;
- source validity, must-cover recall, unsupported-claim/metric, omission,
  normalization, call/retry, and structure-signature diagnostics;
- one content/visual rubric per video, left `PENDING_OWNER_REVIEW` for human
  scoring;
- a cross-video comparison focused on editorial usefulness and visual fit;
- exact technical failures separated from content-quality observations; and
- full regression/evidence results and current status.

Do not create or label a six-run formal Development measurement. Do not let
the implementation agent record Owner acceptance.

## Product acceptance emphasis

The prototype package is reviewable only when all three videos produce
canonical local `report.html` files. Technical/schema diagnostics remain
visible, but the Owner's decision is driven primarily by:

1. **Content coverage and grounding** — must-cover recall ≥90%, no must-cover
   concept completely absent, 100% final source refs valid, and zero major
   unsupported claim or metric.
2. **Editorial usefulness** — prioritization, narrative coherence, and block
   appropriateness target at least 4/5 per video under the existing review-card
   rubric.
3. **Cross-video fit** — the three reports must not all share one normalized
   section/block signature, and their structures must reflect source content.
4. **Visual usability** — desktop and mobile views must have no critical
   clipping, overlap, unreadable source text, or horizontal overflow; hierarchy,
   density, typography, and block affordance are Owner-reviewed.

First-attempt JSON success, retry count, normalization count, and raw-schema
shape are diagnostics. A report that succeeds after its one eligible technical
retry is fully eligible for content/visual review and is not downgraded solely
for needing that retry.

## Call budget

| Work | Runs | Base calls | Retry allowance | Maximum |
|---|---:|---:|---:|---:|
| Provider-free tests/replay | N/A | `0` | `0` | `0` |
| Three-video product set | `3` | `6` | At most one per run | `9` |
| Six-run formal measurement | Not part of this prototype | `0` | `0` | `0` |
| Goal total | `3` | `6` | `3` | `9` |

## Terminal states

| Condition | Required terminal |
|---|---|
| Credential, balance, model access, network, or source authorization blocks work | `READY_FOR_OWNER_V1A_REVIEW — EXTERNAL_BLOCKED` |
| At least one video cannot produce a report after its eligible retry because of API/JSON transport failure | `READY_FOR_OWNER_V1A_REVIEW — PROTOTYPE_EXECUTION_INCONCLUSIVE` |
| Provider transport/JSON succeeds, but at least one video supplies no usable grounded Topic Map or insufficient/incompatible semantic report content under the frozen non-semantic compiler | `READY_FOR_OWNER_V1A_REVIEW — PROTOTYPE_CONTENT_INSUFFICIENT` |
| Producing a report requires semantic rewriting/merge/split, a contract change, another provider/model, or excluded scope | `READY_FOR_OWNER_V1A_REVIEW — CONTRACT_CHANGE_REQUIRED` |
| Three reports and the complete review package exist, with quality concerns clearly retained | `READY_FOR_OWNER_V1A_REVIEW — PROTOTYPE_REPORTS_READY` |
| A post-freeze defect would alter provider input/semantics or cannot be replayed honestly | `READY_FOR_OWNER_V1A_REVIEW — PROTOTYPE_SET_INVALID` |

Only the Owner may subsequently record
`OWNER_ACCEPTED_V1A_PRODUCT_PROTOTYPE`,
`OWNER_REJECTED_V1A_PRODUCT_PROTOTYPE`, or
`OWNER_REQUESTED_V1A_REVISION`.

## Allowed implementation surface after separate execution authorization

- existing V1-A planning/runtime/evaluation/CLI modules only as required for
  semantic-v2 models, Topic Resolver, compiler, explicit retry evidence,
  replay, product review, and screenshot orchestration;
- narrowly scoped V1-A tests and synthetic fixtures;
- three new unique prototype run identities and their ignored local outputs;
- V1-A requirements/task/status/evidence documents; and
- existing V0 renderer only for a reproduced compatibility defect, without
  changing its public plan/asset/HTML contract.

No new dependency is expected. `pyproject.toml` and `uv.lock` remain protected
unless a reproduced blocker proves the current stack insufficient and the Goal
stops for Owner direction before changing them.

## Required evidence

- exact baseline and frozen provider/model/API/prompt/compiler/source snapshot;
- raw/normalized/canonical artifacts and `normalization.json` per run;
- attempt-level trace proving at most one identical technical retry per run;
- successful and failed `0/0` replay;
- three canonical HTML reports plus 1080 px and approximately 390 px screenshots;
- product-quality diagnostics and pending Owner content/visual rubrics;
- targeted/full/Ruff/diff/V0/protected/history validation; and
- synchronized status/requirements evidence without self-acceptance.

## Explicit exclusions

No Provider/Schema conformance experiment, official OpenAI API, GLM/Qwen
acquisition/comparison, provider fallback, six-run formal measurement,
fine-tuning, Agent, LangGraph, RAG, database, service, deployment, MP4/ASR,
keyframe, OCR/VLM, image asset, V1-B, or V1-C.

## Construction-session handoff

The future implementation session must read this card after the canonical V1-A
package, treat `DEC-VR1A-061` as the latest product authority, implement the
entire bounded Goal continuously, automatically repair ordinary in-scope
engineering defects, retain all attempts, and stop at exactly one terminal
state above. It must not reinterpret a technical retry as prompt tuning or a
technical anomaly as a product-route No-Go.

## Completed execution evidence — 2026-08-31

The bounded Goal was executed continuously after the Owner's explicit
`DEC-VR1A-061` authorization. The implementation is frameworkless and keeps the
two independent semantic stages, with deterministic Topic Resolver/compiler,
empty V0 asset manifests, and no semantic repair, fallback, third call, formal
six-run measurement, or V1-B/V1-C scope.

### G0 — contract and freeze

- Added semantic-v2 contracts and runtime/evaluator/CLI support in
  `planning.py`, `planning_runtime.py`, `evaluation.py`, and `__main__.py`.
- Frozen product manifest: `vr1a-semantic-v2-758187ce10bd`, DeepSeek
  `https://api.deepseek.com`, model `deepseek-v4-flash-vision-exp`, Chat
  Completions JSON object, temperature `0`, SDK retries `0`, one identical
  technical retry per run, three videos × one run, six base calls and maximum
  nine calls. `formal_six_run_measurement=false`.
- The original frozen manifest remains preserved at
  `eval/visual-report-v1a/semantic-v2-product-manifest.json`. After a
  deterministic evaluator terminal-state correction, the append-only review
  revision is
  `eval/visual-report-v1a/semantic-v2-product-review-manifest-003.json`; it
  keeps the exact source/provider/run identities and made no provider call.

### G1 — provider-free validation

The semantic-v2 tests passed `6`; the combined semantic-v2 plus existing
planning tests passed `34` with `3` historical provider-conformance tests
deselected. The full suite passed `69`, the V0 regression passed `10`, Ruff
passed, `git diff --check` passed, and protected P0-B/history paths were
unchanged. The current source was tested from the original artifact checkout
with the worktree source on `PYTHONPATH` because ignored historical P0-B
artifacts are not present in this worktree. A real accepted-proposal replay
returned `provider_calls/model_calls=0/0`; an explicit malformed-proposal replay
failed as `TOPIC_MAP_SCHEMA_ERROR` with `provider_calls/model_calls=0/0`.

### G2 — three-video product run

| Video | Result | Calls | Output evidence |
|---|---|---:|---|
| `p0b-kling-2024` | `FAILED` after the one eligible Mapper retry | `2/2` | `MODEL_OUTPUT_INCOMPLETE` with `finish=length`; no report; retained raw attempts and trace |
| `p0b-rlinf-2026` | `RENDERED` | `3/3` | 5 sections, 12 blocks; one recovered identical Mapper retry |
| `p0b-wuyi-goals` | `RENDERED` | `3/3` | 5 sections, 11 blocks; one recovered identical Planner retry |

The product set consumed `8/9` permitted provider/model calls. Both successful
runs have valid Topic Maps, valid source refs, empty asset manifests, zero
semantic rewrite/merge/split/synthesis ledger counts, and must-cover proxy
recall `1.0`. No product identity was tuned or rerun, and the remaining call
budget was not used.

### G3 — render and visual evidence

The two successful identities produced canonical `report.html` files and four
retained screenshots at the required 1080 px desktop and 390 px mobile viewports:

- `artifacts/visual-report/v1a/p0b-rlinf-2026-semantic-v2-02a1aecd92/report.html`
- `artifacts/visual-report/v1a/p0b-rlinf-2026-semantic-v2-02a1aecd92/screenshots/{desktop,mobile}.png`
- `artifacts/visual-report/v1a/p0b-wuyi-goals-semantic-v2-02a1aecd92/report.html`
- `artifacts/visual-report/v1a/p0b-wuyi-goals-semantic-v2-02a1aecd92/screenshots/{desktop,mobile}.png`

Browser inspection found five sections per successful report and no mobile
horizontal overflow; the report title, Chinese source text, hierarchy, and
block affordances were visible. Desktop/mobile content-quality and visual
rubrics remain `PENDING_OWNER_REVIEW`. The failed Kling identity has no report
or screenshots, so this Goal cannot claim a complete three-report/six-screenshot
set.

### G4 — review package and terminal

The append-only review package is
`artifacts/visual-report/v1a/evaluation-review-003/vr1a-semantic-v2-758187ce10bd-review/review-package.json`,
with aggregate diagnostics in the adjacent `aggregate.json`, cross-video
comparison, three pending Owner rubrics, and exact technical/content status
separation. The package records:

`READY_FOR_OWNER_V1A_REVIEW — PROTOTYPE_EXECUTION_INCONCLUSIVE`
with conclusion `TECHNICAL_EXECUTION_FAILURE`: the Kling video still could not
produce a report after its eligible JSON/output retry. This is not Owner
acceptance. The earlier `evaluation-review-002` package is preserved; `-003`
is the current review revision after the deterministic evaluator mapping fix.
No commit, push, PR, deployment, formal six-run measurement, or V1-B/V1-C work
was performed.
