# Video Visual Report V1-A — Test and Acceptance

## Evidence label and stop boundary

Current real-model results are `G1 product-prototype evidence`. They are not a
Provider/Schema conformance result, formal Development measurement, Freeze,
Locked Eval, release, or production evidence. Implementation must stop at a
declared `READY_FOR_OWNER_V1A_REVIEW` terminal; only the Owner may accept V1-A
or authorize V1-B/C.

## Test levels and environments

| Level | Environment | Required evidence |
|---|---|---|
| Unit | Local fake adapter | Proposal models, binders, compiler, budgets, state transitions |
| Contract | Synthetic Chinese transcripts | Valid/invalid Mapper and Planner schemas; exact source binding |
| Integration | Current renderer + fake adapter | Complete transcript-to-HTML flow, exactly controlled calls |
| Failure/recovery | Fake errors/malformed outputs/cancellation | Retained attempts; exact one-retry eligibility/budget; no overwrite or hidden recovery |
| Security | Prompt-injection and secret-redaction fixtures | Transcript remains data; extra executable/layout fields rejected |
| Replay | Fixed synthetic raw responses | Same canonical Topic Map/plan/HTML for identical inputs |
| Regression | Repository checks | Current V0 render and protected P0-B paths unchanged |
| Real product prototype | Configured provider; three fixed transcripts | Three runs/reports plus six viewport screenshots, three human review cards and cross-video review |
| Performance/cost | Same three runs | Attempt/call/latency/usage/size evidence within the nine-call ceiling; no unsupported monetary cost |

Spike, soak, backup-restore, service incident, customer lifecycle, migration, and
commercial go-live tests are not applicable to one foreground G1 prototype.

## Fixed three-video population

| Fixture | Role/slice | Why it matters | Source size |
|---|---|---|---|
| `p0b-rlinf-2026` | Known development/reference slice | Architecture/process/comparison content; hand-authored V0 plan exists | 46 segments, ~34:53 |
| `p0b-kling-2024` | New technical presentation slice | Product/model evolution, capabilities, metrics, and examples | 43 segments, ~33:42 |
| `p0b-wuyi-goals` | New conversational/argument slice | Interview-style reasoning and fewer obvious system blocks | 38 segments, ~29:23 |

The RLinf V0 plan may inform prompt development and qualitative comparison but
must never enter model context. Before the product revision, a reviewer creates
one source-linked card for each fixture:

```json
{
  "schema_version": "visual-report-review-card.v1a-prototype",
  "video_id": "p0b-rlinf-2026",
  "must_cover": [
    {"label": "在线交互的必要性", "source_segment_ids": ["p0b-rlinf-2026-seg-001"]}
  ],
  "optional": [],
  "known_asr_traps": [],
  "prohibited_overclaims": [],
  "reviewer": "owner-or-designated-human"
}
```

Cards name concepts and source refs, not preferred report block sequences. This
avoids turning the evaluation into template matching.

## Historical v1 measurement protocol

The following seven-step protocol records the original v1 denominator and is
not the current semantic-v2 execution authority.

1. Finish fake/contract/integration tests before any measured provider call.
2. Freeze source snapshots, review-card revisions, Mapper/Planner prompts,
   schemas, compiler, provider/model, temperature, timeout, and response mode.
3. Create two unique runs for every video. Run order may be shuffled; all six
   are part of the declared denominator before execution.
4. Do not tune prompts between the six runs. Preserve every failure/cancellation.
5. Score deterministic rules first, then human coverage, grounding,
   prioritization, redundancy, block appropriateness, and narrative quality.
6. Aggregate per run, per video, and overall. Report `provider_calls`,
   `model_calls`, usage, latency, and `cost` separately.
7. If a prompt/model/policy changes, create a new measurement revision and rerun
   all six identities; never replace or selectively rerun the earlier revision.

## Historical exhausted Goal recovery protocol

After `vr1a-dev-10f4334c8026` produced one provider failure and five first-stage
schema failures, the Owner authorized `VR-V1A-GOAL-RECOVERY-003` as one
continuous diagnose–repair–verify session. The following gates apply before a
new formal measurement:

1. Preserve the v3 manifest, all six run directories, aggregate, and pending
   rubrics unchanged.
2. Reproduce and classify the contract failure without weakening the strict
   Mapper/Planner schemas.
3. Add provider-free tests for the observed wrong shapes and prove the runtime
   request exposes the exact required schema/valid example, output-token limit,
   and explicit reasoning/thinking setting.
4. Run one fresh canary per fixed video. All three must reach `RENDERED` on the
   first Mapper and Planner responses with `2/2` calls each. Canary IDs are
   diagnostic evidence and never enter the six-run denominator.
5. Freeze six new IDs only after the canary gate passes; execute all six once
   and evaluate the complete revision once.
6. If an in-scope execution defect remains, preserve the failed revision,
   repair it, and repeat the complete gate with new identities. At most two new
   formal revisions and 36 new admitted provider/model calls are allowed.

Automatic recovery is allowed only across new immutable identities and
revisions. It never authorizes SDK retry, a third call, semantic repair,
selective formal rerun, provider fallback inside a run, or optimization against
an execution-valid six-report set. Credentials/account/billing/source-rights
blocks and any required V1-B/V1-C expansion stop for Owner action.

The latest formal revision is execution-valid only when all six declared runs
reach `RENDERED`, observed calls equal `12/12`, both first responses validate in
every run, compilation/render/source refs pass, and six report paths plus six
pending Owner rubrics exist. Human quality acceptance remains Owner-only.

`VR-V1A-GOAL-RECOVERY-003` ended at
`READY_FOR_OWNER_V1A_REVIEW — GOAL_RECOVERY_EXHAUSTED`: 22 candidate manifests,
20 failed Kling canaries, `36/36` calls, no rendered canary, and no new formal
revision. The loop and its two-formal/36-call authority are closed.

## Completed canonical provider-conformance protocol

`VR-V1A-PROVIDER-CONFORMANCE-004` was authorized after the exhausted recovery
without changing the canonical product or quality contract. It has now closed
at `V1A_PROVIDER_CONFORMANCE_NO_GO`; the protocol below is frozen historical
evidence, not reusable call authority.

1. Preserve the frozen failed-experiment commit and all historical identities.
2. Restore the 4–12-topic/0–5-subtopic Mapper and 3–5-section/8–14-block,
   content-affordance Planner. Provider-free tests must reject exact-count,
   fixed-assignment, fixed-sequence, or fixture-specific prompt/payload logic.
3. Predeclare and freeze at most two materially distinct provider/model/API
   strategies before the first transcript call. Each must use official
   provider-native schema-constrained output; JSON-object/instruction-only
   output does not qualify.
4. Freeze one prompt bundle per strategy (one Mapper prompt plus one Planner
   prompt). Strategy B is frozen before Strategy A runs and may not incorporate
   Strategy A observations.
5. For each eligible strategy, execute the complete three-video canary set once:
   Kling, RLinf, then Wu Yi. Continue the set even after an earlier failure.
   Each run allows one Mapper call and, only after valid mapping, one Planner
   call; SDK retry is zero.
6. A strategy passes only when all three runs reach `RENDERED` from the first
   two responses, report `2/2` calls, pass all deterministic gates, and the
   three normalized structure signatures are not all identical.
7. Stop strategy comparison after the first pass. Freeze one wholly new
   six-run formal revision under that exact winning tuple, execute every run
   once regardless of failures, and invoke the evaluator exactly once.
8. Do not repair or rerun a strategy after its first transcript call and do not
   create a second formal revision. The maximum is 24 new transcript-bearing
   provider calls and 24 model calls.

Terminal conclusions are mutually exclusive:

| Condition | Required state |
|---|---|
| First passing strategy yields a complete execution-valid six-run revision | `READY_FOR_OWNER_V1A_REVIEW — PENDING_OWNER_REVIEW` |
| A strategy passes canary but the single formal revision is incomplete/invalid | `READY_FOR_OWNER_V1A_REVIEW — FORMAL_MEASUREMENT_FAILED` |
| Both predeclared candidates fail capability admission or complete canary conformance | `READY_FOR_OWNER_V1A_REVIEW — V1A_PROVIDER_CONFORMANCE_NO_GO` |
| Remaining eligible strategy cannot execute because of credential/billing/quota/access/network/source authorization | `READY_FOR_OWNER_V1A_REVIEW — EXTERNAL_BLOCKED` |
| Continuing requires a V1-A contract/threshold/two-call change or excluded scope | `READY_FOR_OWNER_V1A_REVIEW — CONTRACT_CHANGE_REQUIRED` |

A capability no-go contains no transcript call. An external block is never
relabelled as conformance evidence. Canary reports are not inserted into the
formal six-run denominator, and no human rubric score is inferred from canary
or automated results.

## Current semantic-v2 product-prototype protocol

The Owner cancelled the unexecuted official-OpenAI isolation proposal and
confirmed `VR-V1A-CONTRACT-SIMPLIFICATION-006` as a DeepSeek-backed product
prototype in `DEC-VR1A-061`. That implementation now exists. Its first frozen
product set rendered RLinf and Wu Yi, while Kling remained incomplete after
the one eligible retry; the retained result is
`PROTOTYPE_EXECUTION_INCONCLUSIVE`, not a route No-Go. `DEC-VR1A-062` defines
one new complete set using the same semantic-v2 contracts with Thinking
enabled, reasoning effort high, `max_tokens=32768`, SDK retry zero, and one
identical retained application retry. Temperature may be traced but cannot be
used to claim stability in Thinking mode.

Provider-free acceptance must cover every v2 compiler rule using raw,
normalized and final artifacts. Tests must prove that allowed rules never add,
rewrite, merge, split, shorten, or expand semantic words/units; prohibited
transformations fail; and identical raw/input/compiler versions replay to
identical final artifacts with `0/0` calls.

One frozen DeepSeek JSON-object tuple runs Kling, RLinf and Wu Yi once each.
Each run has two base calls and may spend one identical, explicit, recorded
technical retry for an eligible API/JSON anomaly, so the whole product set is
capped at nine calls. Valid semantic output is never retried for quality. A
technical failure after retry makes the set `PROTOTYPE_EXECUTION_INCONCLUSIVE`,
not a product-route No-Go.

If transport and JSON parsing succeed but the frozen non-semantic compiler
cannot obtain a usable grounded map/report from the supplied semantics, the
set is `PROTOTYPE_CONTENT_INSUFFICIENT`. This is product evidence, not a
technical outage and not permission to rewrite, tune, or selectively rerun.

The deliverable is three canonical reports plus one 1080 px desktop and one
approximately 390 px mobile screenshot per report. Content/grounding,
editorial usefulness, cross-video structure fit, and visual usability drive
Owner review. First-attempt JSON success, retry rate, schema shape, and
normalization count are diagnostics only. No six-run formal measurement is
created in this prototype.

## Owner-confirmed historical v1 quality rubric

### Topic Mapper

| Metric | Method | Pass threshold |
|---|---|---|
| Segment accounting | Deterministic IDs | 100% mapped or explicit exclusion |
| Required-topic recall | Review-card must-cover concepts | ≥90% per run and no must-cover item completely absent |
| Unsupported topic | Human source review | 0 material unsupported topic |
| Exclusion validity | Human review of excluded technical content | 0 substantive topic excluded as housekeeping |
| Chronological coherence | Topic refs/order inspection | All topic instances ordered; primary refs contiguous |

### Report Planner

| Metric | Method | Pass threshold |
|---|---|---|
| Source-ref validity | Deterministic compiler | 100% |
| Major overclaim/unsupported metric | Human entailment + lexical metric gate | 0 across accepted runs |
| Required-topic retention | Included report vs review card | No must-cover topic completely lost |
| Prioritization | Human 1–5 rubric | ≥4 average per video; neither repeat below 3 |
| Narrative coherence | Human 1–5 rubric | ≥4 average per video; neither repeat below 3 |
| Block appropriateness | Human 1–5 rubric using source affordances | ≥4 average per video; no special block scored 1 |
| Redundancy/compression | Human 1–5 rubric | ≥4 average; no major repeated claim |
| Schema/render stability | Run states | 6/6 first responses validate/compile/render without repair |
| Repeat stability | Must-cover retention and rubric delta | Both repeats pass; per-video rubric-category delta ≤1 point |
| Anti-template | Normalized section/block signature + review | All three signatures are not identical; semantic structure fits source |

Human scores must cite the offending block/topic/source when below threshold.
Source refs are necessary but not sufficient: a claim can cite a real segment
and still overstate it.

For current v2, replace the historical execution-oriented rows with:

| Metric | Current v2 method | Current product threshold |
|---|---|---|
| Segment accounting | Topic Resolver span/representative diagnostics | Diagnostic only; at least one usable topic, with uncovered IDs/overlap exposed |
| Exclusion validity | Not applicable to model-facing v2; no exclusion field | Must-cover/unsupported-topic review remains authoritative |
| Product-path completion | Semantic proposals → non-semantic compiler → current V0 renderer | 3/3 canonical HTML reports; 2 base calls or 3 with one eligible retry per run |
| Compiler authority | Raw-to-final event ledger | Zero semantic rewrite/merge/split/synthesis; every whole-unit omission visible and reviewed |
| Source integrity | Final refs plus raw model-selected IDs | 100% final refs valid; every Hero/block retains ≥1 valid model-selected source ID |
| Visual usability | Real-browser desktop/mobile review | Six screenshots; no critical clipping, overlap, unreadable source text, or horizontal overflow |
| Schema/retry diagnostics | Attempt and parser ledger | Recorded, but never the primary product acceptance score |

## Acceptance cases

`TEST-VR1A-001` through `022` retain the implemented/historical v1 and
provider-conformance acceptance record. `TEST-VR1A-023` through `028` define
the current Owner-confirmed semantic-v2 product prototype and its runtime
closure.

| Test ID | Given | When | Then | Links |
|---|---|---|---|---|
| `TEST-VR1A-001` | Valid manifest/ordered segments | Build starts | Source validates without mutation | `REQ-VR1A-001` |
| `TEST-VR1A-002` | Successful run | Trace inspected | One Mapper + one Planner call; total `2/2` | `REQ-VR1A-002` |
| `TEST-VR1A-003` | Mapper accounts for every segment | Binder runs | Canonical map has exact refs/counts | `REQ-VR1A-003` |
| `TEST-VR1A-004` | Mapper emits block/importance/layout field | Schema validates | Run fails before Planner | `REQ-VR1A-004`, `008` |
| `TEST-VR1A-005` | Valid map/full transcript | Planner runs | Every topic is selected or explicitly omitted | `REQ-VR1A-005` |
| `TEST-VR1A-006` | Model emits unknown ID/time | Binder/compiler runs | Unknown ID fails; model time field rejected | `REQ-VR1A-006` |
| `TEST-VR1A-007` | Valid proposal | Compiler runs | Every factual block has 1–4 exact refs | `REQ-VR1A-007` |
| `TEST-VR1A-008` | Invalid refs/budgets/fields/metric | Validation runs | Stable non-zero failure; no success artifact | `REQ-VR1A-008` |
| `TEST-VR1A-009` | Invalid model response | Run handles failure | No semantic repair, third call, retry, or silent block deletion | `REQ-VR1A-009` |
| `TEST-VR1A-010` | Valid proposal | Compiler/renderer run | Current V0 plan + empty asset manifest validate and render | `REQ-VR1A-010` |
| `TEST-VR1A-011` | Model emits `image_caption`, asset, HTML/CSS/layout | Schema validates | Plan fails | `REQ-VR1A-011` |
| `TEST-VR1A-012` | Success/provider failure | Trace inspected | Non-secret config/usage/latency/status recorded accurately | `REQ-VR1A-012` |
| `TEST-VR1A-013` | Existing/failed/cancelled run IDs | Command invoked | Existing ID rejected; failures preserved; no overwrite | `REQ-VR1A-013` |
| `TEST-VR1A-014` | Frozen six-run measurement | Evaluator runs | Every declared run appears in denominator and rubric | `REQ-VR1A-014` |
| `TEST-VR1A-015` | Final diff/test run | Regression checks run | V0 renderer command and P0-B frozen artifacts remain unchanged | `REQ-VR1A-015` |
| `TEST-VR1A-016` | All implementation/evaluation checks complete | Session concludes | Status stops for Owner review; no V1-B/C work | `REQ-VR1A-016` |
| `TEST-VR1A-017` | Canonical prompts/payloads/examples | Static and contract tests run | No exact-four topic, empty-subtopic, exact 3/8, fixed assignment/sequence, or fixture-specific steering remains | `REQ-VR1A-003`, `005`, `014` |
| `TEST-VR1A-018` | Candidate provider/model/API tuple | Capability admission runs | Official native schema-constrained support and exact frozen hashes exist; JSON-object-only mode is rejected | `REQ-VR1A-002`, `009`, `012` |
| `TEST-VR1A-019` | One eligible frozen strategy | Canary manifest executes | All three videos execute once and remain retained; no per-video change or early-set abort | `REQ-VR1A-009`, `013`, `014` |
| `TEST-VR1A-020` | Strategy A fails | Strategy B is considered | Only the already-frozen materially distinct tuple may run; no prompt learning/micro-version | `REQ-VR1A-009`, `014` |
| `TEST-VR1A-021` | First strategy passes 3/3 | Formal manifest freezes and executes | Six fresh runs execute once, evaluator runs once, and calls remain within the 24-call ceiling | `REQ-VR1A-012`–`016` |
| `TEST-VR1A-022` | No strategy passes or formal fails | Goal closes | Exact honest terminal is recorded without fake report, score, retry, or acceptance | `REQ-VR1A-009`, `013`, `014`, `016` |
| `TEST-VR1A-023` | Valid/invalid v2 Mapper proposals | Topic Resolver runs | Valid spans bind; unknown/duplicate IDs and uncovered/overlap diagnostics are exact; no semantic text is created | `REQ-VR1A-017`, `018` |
| `TEST-VR1A-024` | Flat v2 Planner content units | Compiler runs | Compatible V0 blocks/refs are deterministic; whole unusable units are visible; no text/unit is rewritten, merged, or split | `REQ-VR1A-019`, `020` |
| `TEST-VR1A-025` | Eligible technical failure then success/failure | V2 stage runs | Exactly one identical retry is attempt-recorded; success remains reviewable; exhaustion is technical-inconclusive | `REQ-VR1A-021` |
| `TEST-VR1A-026` | Valid JSON with weak semantics or V0 incompatibility | Compiler rejects it | No retry, model repair, fabricated content, provider fallback, or hidden new run occurs | `REQ-VR1A-020`, `021` |
| `TEST-VR1A-027` | Frozen three-video product set renders | Browser/content review runs | Three HTML reports, six viewport screenshots, content/grounding/structure/visual evidence exist; total calls ≤9; schema-first-hit remains diagnostic | `REQ-VR1A-022` |
| `TEST-VR1A-028` | Next product revision is admitted | Request spy, manifest, and attempt trace are compared | Actual DeepSeek Chat Completions request and snapshot agree on `deepseek-v4-flash-vision-exp`, JSON object, Thinking enabled, reasoning effort high, `max_tokens=32768`, SDK retry zero, and one identical application retry; temperature is excluded from stability claims | `REQ-VR1A-021`, `022` |

## Invalid, partial, stale, and adversarial cases

- malformed UTF-8/JSON; blank/mixed/duplicate/out-of-order/overlapping segments;
  manifest mismatch; oversized transcript;
- missing model/config credential; provider timeout/error; empty choices;
- JSON wrapped in Markdown, extra field, unknown discriminant, wrong topic ID;
- one unaccounted segment, duplicate primary assignment, invalid exclusion,
  non-contiguous topic source run;
- too few/many topics/sections/blocks/items, overlong copy, invalid final
  takeaway, `image_caption`, layout/style/asset fields;
- metric value absent from all cited text; source ref outside selected topics;
- transcript text that says “ignore previous instructions” or imitates JSON
  policy; it must remain inert source content;
- cancellation after Mapper and before/during Planner; no rendered success;
- prior product set after prompt/model/source/compiler change; it remains
  historical and is labeled stale for current conclusions.
- automatic truncation, rewriting, semantic merge/split, or content movement to
  satisfy V0 limits; these are prohibited rather than normalized.

There is no successful partial/degraded report. Earlier-stage artifacts in a
failed run are diagnostics, not a partial product result.

## Replay and recovery fixtures

- Successful replay: synthetic three-topic Chinese transcript + saved valid raw
  Mapper/Planner JSON. Replaying without provider calls must produce identical
  canonical Topic Map, current V0 plan, empty assets, and HTML.
- Failure replay: saved Mapper proposal with one missing segment and saved
  Planner proposal with an unsupported metric. Each must deterministically reach
  its exact failure category with `provider_calls/model_calls=0/0` during replay.

## Required implementation verification commands

```bash
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run ruff check .
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q tests/test_visual_report_planning.py
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q
git diff --check
```

The implementation task must run `build-from-transcript` once for each fixed
fixture under one frozen product-set revision, permit only its one eligible
technical retry per run, render all successful reports, capture both required
viewports, and generate the documented prototype review package.

## Traceability

| Goal | Scenario | Requirement | Component | Tests/signal |
|---|---|---|---|---|
| `GOAL-VR1A-001` | `SCN-VR1A-002` | `REQ-VR1A-003`, `004` | Mapper/binder | `TEST-VR1A-003`, `004`; coverage rubric |
| `GOAL-VR1A-002` | `SCN-VR1A-003` | `REQ-VR1A-005`, `010` | Planner/compiler | `TEST-VR1A-005`, `010`; prioritization rubric |
| `GOAL-VR1A-003` | `SCN-VR1A-004` | `REQ-VR1A-006`–`009` | Source/metric/schema gates | `TEST-VR1A-006`–`009`; overclaim metric |
| `GOAL-VR1A-004` | `SCN-VR1A-006` | `REQ-VR1A-014` | Evaluation harness | `TEST-VR1A-014`; signatures/rubric |
| `GOAL-VR1A-005` | `SCN-VR1A-001` | `REQ-VR1A-010`, `015` | Compiler/renderer | `TEST-VR1A-010`, `015` |
| `GOAL-VR1A-006` | `SCN-VR1A-004`, `006` | `REQ-VR1A-012`–`014` | Run recorder/evaluator | `TEST-VR1A-012`–`014` |
| `GOAL-VR1A-001` current v2 | `SCN-VR1A-009` | `REQ-VR1A-017`, `018` | Mapper/Topic Resolver | `TEST-VR1A-023`; coverage diagnostics/rubric |
| `GOAL-VR1A-002/003` current v2 | `SCN-VR1A-010`, `011` | `REQ-VR1A-019`, `020` | Planner/compiler | `TEST-VR1A-024`, `026`; grounding/product-quality signals |
| `GOAL-VR1A-006` current v2 | `SCN-VR1A-013` | `REQ-VR1A-021` | Model adapter/run recorder | `TEST-VR1A-025`; attempt/call ledger |
| `GOAL-VR1A-004/005` current v2 | `SCN-VR1A-012` | `REQ-VR1A-022` | Renderer/prototype reviewer | `TEST-VR1A-027`; content/visual rubrics/screenshots |

## Acceptance ownership

| Area | Owner | Required evidence |
|---|---|---|
| Product/content planning | Owner | Three reports, Topic Maps, content/visual rubrics, cross-video conclusion |
| Data/source/rights | Owner + implementer | Authorized fixed sources, validated refs, no publication |
| AI quality | Owner | Coverage, grounding, overclaim, prioritization, variation thresholds |
| Contract/security | Implementer | Unit/failure/adversarial/replay tests |
| Performance/cost | Implementer | Latency/call/usage/size report; honest unavailable cost |
| Operations/support/commercial/legal | Not applicable for G1 service | Explicit no-service/no-public claim |

Passing automated checks can only produce `READY_FOR_OWNER_V1A_REVIEW`.
