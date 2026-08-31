# Video Visual Report V1-A — Strict Boundary Minimal Isolation Goal

## Task identity

| Field | Value |
|---|---|
| Task ID | `VR-V1A-BOUNDARY-ISOLATION-005` |
| Product stage | `V1-A — Automated Content Planning Prototype` |
| Grade | `G1 PROTOTYPE` |
| Design status | `CANCELLED_BY_OWNER — NEVER_AUTHORIZED / NEVER_EXECUTED` |
| Execution authorization | `CLOSED` — the Owner declined the official OpenAI Route A experiment and redirected design to `VR-V1A-CONTRACT-SIMPLIFICATION-006` |
| Execution mode after authorization | One continuous Goal; no routine Owner checkpoint |
| Frozen starting baseline | `e72503f5b20831c1e86a1b72c93fb4c4f7debe2a` on branch `visual-report` |
| Provider candidates | Exactly one direct provider/model/API tuple with documented strict Structured Outputs; no comparison arm |
| Maximum generation requests | `4` total; every generation endpoint request consumes the ceiling even if rejected before model execution |
| Real-transcript scope | Only `p0b-rlinf-2026`, and only after both synthetic stage canaries pass |
| Formal measurement/evaluator/rubrics | Prohibited |
| Normal completion | `READY_FOR_OWNER_V1A_REVIEW — MINIMAL_ISOLATION_COMPLETE` |
| Other honest stops | `READY_FOR_OWNER_V1A_REVIEW — EXTERNAL_BLOCKED`, `READY_FOR_OWNER_V1A_REVIEW — CONTRACT_CHANGE_REQUIRED`, or `READY_FOR_OWNER_V1A_REVIEW — EXPERIMENT_INVALID` |

## Owner request and current authority

> Historical note: after this proposal was drafted, the Owner stated that no
> OpenAI API key would be purchased and directed the work to V1-A contract
> simplification. All execution sections below are retained as rejected design
> evidence only and provide no current authority.

The Owner requested a minimal isolation design that remains Goal-driven:

> “设计最小实验隔离方案，依旧以Go驱动的方式。”

This confirms the documentation objective and continuous-Goal operating style.
It does **not** yet confirm a new provider, credential, billing authority, or
permission to transmit the RLinf transcript to a provider other than the
previously configured DeepSeek-compatible endpoint. Those two execution items
are the only planned Owner checkpoint at the end of this card.

## Goal

Produce one causal answer with no more than four generation requests:

> When the V1-A prompts and canonical Pydantic contracts are carried over a
> genuinely strict provider boundary, does failure remain structural, move to
> Mapper semantic accounting, move to Planner semantic compilation, or
> disappear for one representative full video?

This Goal is diagnostic. It does not prove three-video quality, does not reopen
formal Development measurement, and does not select Route B or Route C
automatically.

## Why this is the smallest useful experiment

The frozen DeepSeek experiment already proved that its two selected models over
the same Responses `json_schema` mechanism did not satisfy the V1-A boundary.
It did not prove that the two-stage architecture is invalid. Repeating a full
three-video canary would mix four questions:

1. whether the endpoint truly enforces a submitted schema;
2. whether the provider accepts the schema dialect emitted by Pydantic;
3. whether Mapper can satisfy cross-field segment accounting; and
4. whether Planner can satisfy semantic source/budget/compiler rules.

This task separates those layers before spending calls on multiple videos.

## Fixed product contract

This experiment must not change the canonical V1-A behavior:

- Topic Mapper and Report Planner remain two independent roles and calls.
- Both real stages receive the complete authorized transcript; Planner also
  receives the canonical Topic Map.
- Models select existing IDs and semantic content only.
- Deterministic code owns canonical IDs, timestamps, `SourceRef`, segment/topic
  accounting, budgets, metric checks, compilation, state, and rendering.
- Canonical ranges remain 4–12 topics, 0–5 subtopics, 3–5 sections, 2–4 blocks
  per section, 8–14 blocks total, and at most 2,600 visible characters.
- No semantic repair, third product call, SDK retry, provider/model fallback,
  manual plan, block deletion, truncation, chunking, or successful degraded
  report is allowed.
- V0 renderer, P0-B evidence, historical V1-A runs, review cards, aggregates,
  prompts, and quality thresholds remain unchanged.

## Isolation layers and authority

Every attempted stage records the first failing layer. Later layers must not
hide or relabel an earlier failure.

| Layer | Question | Authority | Pass evidence |
|---|---|---|---|
| `L0 CONFIG` | Is the exact provider/model/API tuple available and authorized? | Frozen experiment manifest | Non-secret endpoint/model/access snapshot |
| `L1 SCHEMA_ADMISSION` | Does the provider accept the submitted strict schema dialect? | Provider response + submitted schema hash | Request admitted without schema error |
| `L2 TRANSPORT_SHAPE` | Did a completed, non-refusal response obey the submitted types/required/enums/no-extra contract? | Strict provider schema + raw response | Transport-schema validation passes without cleanup |
| `L3 CANONICAL_SCHEMA` | Does the raw object satisfy unchanged `TopicMapProposal` or `ReportPlanProposal`? | Existing Pydantic models | Canonical validation passes without coercion/repair |
| `L4 SEMANTIC_BINDER` | Are existing IDs, chronology, unique coverage, and topic disposition valid? | Existing deterministic binder | Canonical Topic Map or selected/omitted accounting passes |
| `L5 COMPILER` | Do source affordances, refs, metrics, budgets, current V0 plan, and empty assets pass? | Existing compiler/models | Current plan/assets validate |
| `L6 RENDERER` | Can the unchanged V0 renderer produce the local report? | Existing renderer | Terminal `RENDERED` plus complete artifacts |

## G0 — Baseline and historical preservation

Before editing or calling a provider:

1. Read `AGENTS.md`, `docs/visual-report/V1A-STATUS.md`, the V1-A readiness,
   handoff, engineering context, canonical `03/06/07/09/10/11`, the completed
   provider-conformance card, and this card.
2. Confirm branch `visual-report`, HEAD
   `e72503f5b20831c1e86a1b72c93fb4c4f7debe2a`, and preserve all unrelated or
   later Owner work.
3. Inventory and retain the frozen DeepSeek manifest/result, six failed
   provider-conformance canaries, historical recovery candidates/runs, all
   formal revisions, aggregates, reports, and pending rubrics.
4. Do not read, print, copy, or commit secret values. Do not put transcript or
   raw provider-response bodies in chat commentary.

## G1 — Provider-free strict-boundary admission

Complete and repair all ordinary engineering work before the first external
generation request.

### G1.1 Control-provider boundary

The recommended control is the **direct official OpenAI Responses API**, not an
OpenAI-compatible proxy. The exact accessible base model remains selected by
the implementer inside `DEC-VR1A-048`, but it must:

- be a non-fine-tuned model whose current official documentation supports
  Responses Structured Outputs for the exact API surface;
- fit the complete RLinf input and current output budget;
- use `text.format.type="json_schema"` with `strict=true`;
- use temperature zero when supported, one explicit output limit and timeout,
  and SDK retry zero; and
- be frozen with provider, exact model/version, base URL label, SDK version,
  prompt/schema/code hashes, and non-secret parameters before Call 1.

Official OpenAI documentation distinguishes Structured Outputs from JSON mode,
requires `strict: true`, requires all object fields, requires
`additionalProperties: false`, documents nested `anyOf`, and notes refusal or
incomplete output as explicit edge cases:
[Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs).

The installed OpenAI Python SDK `3.3.1` already exposes the Responses text
format `strict` field. No dependency update is expected or authorized merely
for this experiment.

### G1.2 Deterministic provider-schema projection

Do not modify the canonical Pydantic models or their validators. Derive one
provider-facing schema per stage and record both canonical and submitted hashes.
For the recommended OpenAI control, the projection must:

- set `strict=true` at the Responses format boundary;
- make every object property required;
- require Mapper `subtopics` and root `exclusions`, with empty arrays allowed;
- require Planner root `omitted_topics`; require metric `context` while keeping
  its existing string-or-null meaning;
- preserve all required fields, types, literal/enumerated discriminants,
  `additionalProperties=false`, string limits, array limits, and definitions;
- project the Planner's nested Pydantic `oneOf + discriminator` representation
  to documented nested `anyOf` branches while retaining mutually exclusive
  block `type` literals; and
- emit a machine-readable transformation manifest. It may remove transport
  metadata that has no validation meaning, but it may not drop a product
  constraint or make an invalid canonical proposal valid.

Provider-free equivalence tests must prove that all six block variants and the
current valid fixtures pass both the submitted structural schema and canonical
Pydantic validation, while missing/extra/wrong-type/wrong-enum cases fail.
Pydantic/binder/compiler validation remains mandatory after every response.

### G1.3 Provider-free gates

Before freeze, run and automatically repair ordinary failures in:

- exact request-shape tests (`strict=true`, schema hash, retry zero);
- schema-subset/equivalence tests and all current invalid fixtures;
- direct synthetic Mapper and Planner replay with `0/0` provider/model calls;
- targeted planning tests, full pytest, Ruff, `git diff --check`;
- saved-response replay, V0 renderer regression, and protected/history diff;
- manifest validation and four-ID call-ledger completeness.

No provider call is allowed until every applicable gate passes.

## Experiment freeze

Before Call 1, freeze one immutable experiment revision containing:

- baseline commit and exact code diff;
- exact provider/model/API tuple and authorization state;
- canonical and provider-facing Mapper/Planner schema hashes;
- Mapper/Planner prompt and payload-builder hashes;
- synthetic fixture and RLinf input snapshot hashes;
- timeout, temperature, reasoning, output-token, SDK, and retry settings;
- four unique predeclared call identities; and
- maximum counts: `provider_requests=4`, `model_calls<=4`.

After Call 1, prompt, schema projection, adapter, model/API settings, binders,
compiler, fixtures, and pass rules are immutable. A different value creates a
new experiment and is not authorized by this Goal.

## G2 — Two independent synthetic stage canaries

Use the existing eight-segment synthetic fixture. These are independent calls,
not a synthetic pipeline:

1. **Call 1 — Synthetic Topic Mapper:** current Mapper prompt, synthetic full
   transcript, submitted strict Mapper schema. Validate through `L1`–`L4`.
2. **Call 2 — Synthetic Report Planner:** current Planner prompt, the frozen
   synthetic transcript and deterministic canonical synthetic Topic Map, not
   Call 1 output. Validate through `L1`–`L6`.

Run both stage canaries when the endpoint remains available, even if one has a
schema/content failure; their independence identifies whether complexity is
Mapper-specific or Planner-specific. Stop immediately instead for credential,
billing, quota, access, network, or provider-outage failure.

Synthetic output need not match the saved fixture text or exact structure. It
passes only by satisfying the unchanged allowed ranges and deterministic gates.
Do not turn the fixture's four topics/eight blocks into prompt targets.

If either synthetic call fails `L1`–`L5`, do not send a real transcript. Keep
both independent stage observations and select the applicable conclusion from
the matrix below. If a canonically valid compiled synthetic plan alone fails
`L6`, use the `EXPERIMENT_INVALID` stop defined below rather than blaming the
provider or semantic contract.

## G3 — One representative real-video chain

Enter G3 only when both synthetic stage canaries pass. Use
`p0b-rlinf-2026` because both frozen DeepSeek strategies produced a 13-topic
Mapper result on this 46-segment input, and a hand-authored V0 plan exists as a
read-only comparison reference. The V0 plan must not enter model context.

3. **Call 3 — RLinf Topic Mapper:** complete authorized transcript and unchanged
   canonical Mapper prompt. Validate `L1`–`L4`. If raw structure passes but
   segment accounting/chronology fails, stop; do not call Planner.
4. **Call 4 — RLinf Report Planner:** only after Call 3 produces a canonical
   Topic Map. Send the same full transcript plus that map and validate
   `L1`–`L6`.

No second attempt is allowed for either stage. No three-video canary, repeat,
formal measurement, evaluator aggregate, or human rubric is created.

## Call budget

| Path | Synthetic requests | Real requests | Maximum total |
|---|---:|---:|---:|
| External/configuration block | `0–1` | `0` | `1` |
| Synthetic boundary no-go | `2` | `0` | `2` |
| Synthetic pass; RLinf Mapper fails | `2` | `1` | `3` |
| Complete one-video chain | `2` | `2` | `4` |

Every request to a generation endpoint consumes the provider-request ceiling,
including a request rejected for schema syntax. Record provider requests,
actual model executions, usage, latency, refusal, incomplete status, and cost
availability separately. Never infer monetary cost.

## Conclusion matrix

The task terminal is normally
`READY_FOR_OWNER_V1A_REVIEW — MINIMAL_ISOLATION_COMPLETE`; the result artifact
must contain exactly one conclusion:

| First decisive observation | Conclusion | What it means | Next work not authorized here |
|---|---|---|---|
| Either synthetic stage fails `L1` schema admission | `SCHEMA_DIALECT_OR_ADAPTER_NO_GO` | Provider-facing schema/adapter is not an admitted strict boundary | Another provider or schema-boundary design |
| Completed synthetic output fails `L2`/`L3` | `STRICT_TRANSPORT_NO_GO` | Claimed strict transport is not reliable for the frozen stage contract | Another genuine strict provider strategy |
| Only synthetic Mapper passes raw `L2`/`L3` but fails `L4` | `MAPPER_SEMANTIC_CONTRACT_PRESSURE_OBSERVED` | Strict shape worked; Mapper accounting already fails on the simple fixture | Route C/B requirements design |
| Only synthetic Planner passes raw `L2`/`L3` but fails `L4`/`L5` | `PLANNER_SEMANTIC_CONTRACT_PRESSURE_OBSERVED` | Strict shape worked; Planner semantics or compilation already fail on the simple fixture | Route B requirements design |
| Both synthetic stages pass raw `L2`/`L3` but fail their semantic/binder/compiler layers | `BOTH_STAGE_SEMANTIC_CONTRACT_PRESSURE_OBSERVED` | Transport is not the first failure; both stage contracts exert pressure before real data | Route B/C requirements design |
| Both synthetic calls pass; either RLinf stage fails `L1`/`L2`/`L3` | `STRICT_TRANSPORT_AT_REAL_SCALE_NO_GO` | Strict behavior did not hold at real payload complexity | Provider boundary investigation |
| RLinf Mapper passes raw schema but fails `L4` | `MAPPER_SEMANTIC_CONTRACT_PRESSURE_OBSERVED` | Structured Output worked; unique coverage/chronology remains the pressure point | Route C/B requirements design |
| RLinf Planner passes raw schema but fails `L4`/`L5` | `PLANNER_SEMANTIC_CONTRACT_PRESSURE_OBSERVED` | Structured Output worked; topic/source/budget/affordance compilation remains the pressure point | Route B requirements design |
| RLinf reaches `L6 RENDERED` with exact `2/2` real calls | `STRICT_BOUNDARY_ONE_VIDEO_PASS` | Route A is plausible on one representative video only | Separate Owner decision on three-video canary |

For two independent synthetic failures, the conclusion uses the lowest failing
layer (`L1` before `L2/L3` before `L4/L5`). When both first fail at their
semantic layers, use the combined conclusion. The result still records each
stage separately so the single conclusion never erases a secondary failure.

None of these conclusions is `OWNER_ACCEPTED`, a formal V1-A quality result, or
authority to redesign/implement Route B/C.

## Automatic repair boundary inside the Goal

- **Before Call 1:** automatically diagnose, fix, and revalidate ordinary
  in-scope code, schema-projection, test, CLI, serialization, manifest, replay,
  trace, and documentation defects.
- **After Call 1:** do not change or rerun the frozen experiment tuple. A purely
  evidence-writing defect may be fixed and the already-retained response may be
  replayed with `0/0` calls only when pass/fail semantics are unchanged.
- If a post-freeze defect changes the request or could change a pass/fail
  decision, preserve all calls and stop at
  `READY_FOR_OWNER_V1A_REVIEW — EXPERIMENT_INVALID`.
- Never ask the Owner for routine checkpoints. Stop only for external authority,
  contract changes, or an invalid frozen experiment.

## Required artifacts

- one versioned isolation manifest with all four possible identities;
- canonical and submitted schema snapshots plus a transformation/diff manifest;
- one retained directory per attempted call with non-secret request metadata,
  raw response, parsed object when present, first failing layer, and counts;
- one append-only isolation result with the exact conclusion matrix value;
- provider-free replay evidence proving `0/0` calls;
- targeted/full/Ruff/V0/protected/history validation evidence; and
- synchronized updates to this card and `docs/visual-report/V1A-STATUS.md`.

Do not create or modify a formal measurement manifest, evaluation aggregate,
human rubric, historical run, or Owner-acceptance record.

## Allowed change envelope after execution authorization

Use the smallest existing V1-A surface:

- `src/video_evidence_agent/visual_report/planning_runtime.py` for the strict
  format boundary and provider-safe response classification;
- `planning.py` only for a pure provider-schema projection helper or manifest
  metadata; canonical models/prompts/validators may not change;
- the existing CLI/evaluation module only if a reproduced requirement cannot be
  expressed by the current command/artifact path;
- narrowly scoped V1-A tests and synthetic fixtures;
- new versioned isolation manifest/result artifacts and V1-A task/status docs.

`pyproject.toml` and `uv.lock` are protected: SDK `3.3.1` already exposes the
required `strict` field, so dependency change is not expected. Any demonstrated
need would require a separate Owner-visible stop before editing dependencies.

## Prohibited changes

- changing canonical topic/section/block/source/length/count/affordance rules;
- simplifying Topic Mapper, adding Source Resolver, or implementing deterministic
  semantic projection/repair in this task;
- adding another provider/model strategy, same-stage rerun, prompt micro-version,
  fallback, SDK retry, third product call, semantic repair, or post-freeze tune;
- sending Kling or Wu Yi transcripts, running cross-video or formal measurement,
  evaluator, or human scoring;
- modifying V0 renderer/content/assets, P0-B source/eval/history, or historical
  V1-A runs/results;
- MP4/ASR, keyframes, OCR/VLM, RAG, Agent/LangGraph, database, queue, API/UI,
  service, deployment, publishing, V1-B, or V1-C; and
- commit, push, PR, deployment, or `OWNER_ACCEPTED` unless separately requested.

## Hard stops

Use `READY_FOR_OWNER_V1A_REVIEW — EXTERNAL_BLOCKED` when the remaining work
requires a credential, billing/quota/account access, network permission,
provider availability, or explicit authorization to send RLinf to the selected
new provider.

Use `READY_FOR_OWNER_V1A_REVIEW — CONTRACT_CHANGE_REQUIRED` when continuing
requires changing the V1-A product contract, thresholds, two-call topology,
source population, no-retry rule, dependency baseline, or excluded scope.

## Required verification after implementation

```bash
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run ruff check .
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q tests/test_visual_report_planning.py
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q
git diff --check
```

Also run provider-free strict-schema equivalence tests, saved-response replay,
the V0 renderer regression, protected/history path checks, manifest/result
validation, and exact call-ledger reconciliation.

## Owner execution checkpoint

Before this card can become `AUTHORIZED`, the Owner must explicitly confirm:

1. the experiment may use one **direct official OpenAI Responses** strict-output
   strategy, with the exact accessible base model selected and frozen by the
   implementer under the constraints above, and the complete
   `p0b-rlinf-2026` transcript may be sent to that provider after both synthetic
   calls pass; and
2. the maximum is four generation requests, no formal measurement, with the
   conclusion/stop matrix in this card.

Confirmation authorizes this bounded experiment only. It does not authorize a
three-video canary, Route B/C redesign, V1-A acceptance, or V1-B/V1-C.
