# Visual Report V1 — Current Status

Updated: 2026-09-04

This is the short resume point for current Visual Report work. Historical V0,
V1-A task IDs, schema names, paths, and evidence remain valid records, but they
are not the active roadmap vocabulary.

## Current state

| Field | Value |
|---|---|
| Current product baseline | `V1.1 — TRANSCRIPT_FOUNDATION_FROZEN_BASELINE` |
| Product-quality judgment | `NOT_ACCEPTED — output text and presentation still need material improvement` |
| Frozen code baseline | branch `visual-report`, commit `2bce883` |
| Active design | `V1.2 — Visual Editorial Agent / Harness` |
| V1.1 task | `VR-V1.1-MODEL-UPGRADE-014 — CLOSED` |
| V1.1 status | `V1.1_FROZEN` |
| V1.2 | `REQUIREMENTS_AND_TECHNICAL_DESIGN_AUTHORIZED / IMPLEMENTATION_NOT_AUTHORIZED` |
| V1.3 | `DEFERRED / SCOPE_TO_BE_DECIDED_AFTER_V1.2` |
| Deployment / multi-tenant work | Deferred; not part of V1.2 design authority |

## Version naming

| Current name | Meaning | Historical compatibility |
|---|---|---|
| `V1.0` | Current runnable local Alpha baseline | Existing `V1-A`, `vr1a`, `semantic-v2`, Task 001–012 names remain unchanged in code, paths, schemas, tests, and evidence |
| `V1.1` | Frozen Transcript Foundation: ASR + subtitle track + burned-in subtitle OCR → Canonical Transcript | Accepted baseline at `2bce883` |
| `V1.2` | One end-to-end Visual Editorial Agent / Harness spanning semantic planning, presentation planning, deterministic rendering, browser observation, and bounded critic repair | Requirements and technical design only |
| `V1.3` | Post-Harness evolution selected from V1.2 evidence | Scope intentionally unassigned |

Do not mass-rename historical identifiers. `V1.0` is the product name going
forward, not a migration of frozen artifact identities.

## What V1.0 currently does

```text
Local MP4
  or public Bilibili BV URL
        ↓
FFmpeg audio extraction
        ↓
MLX Whisper ASR
        ↓
45–60 second VideoSegment[]
        ↓
Existing semantic-v2 Topic Mapper + Report Planner
        ↓
Existing deterministic renderer
        ↓
report.html
```

The Bilibili Web path is loopback-only and uses a single-process, single-active
worker with an in-memory FIFO queue. It is a local Alpha convenience surface,
not a durable or multi-user service.

## Current quality diagnosis

The product runs end to end, but pipeline completion is not the main problem.
The quality stack should be improved in this order:

1. **Transcript:** current ASR-only text can misrecognize proper nouns, numbers,
   and English abbreviations even when reliable subtitles are visible.
2. **Semantic:** the current Topic Mapper/Planner can only reason over the text
   it receives; transcript defects and planning-quality defects are currently
   mixed together.
3. **Render:** the deterministic renderer works, but its current visual result
   is not yet consistently attractive or information-dense enough.

V1.1 isolates the first problem and is now frozen at `2bce883`. V1.2 is no
longer split from a separately predesigned renderer phase: its authorized design
must define one end-to-end Harness contract while retaining semantic,
presentation, rendering, and observation as separately testable layers.

## Frozen V1.1 target

```text
Video
  ├─ ASR
  ├─ Subtitle Track
  └─ Burned-in Subtitle OCR
          ↓
   Temporal Alignment
          ↓
 High-confidence Local Fusion
          ↓
   Canonical Transcript
          ↓
 V1.0-compatible VideoSegment
          ↓
 Existing semantic-v2 + renderer
```

V1.1 must preserve every original text source and make every correction
traceable. It may correct only a reliable local span. Whole-sentence conflicts
or cases that need semantic rewriting keep ASR as provisional text and are
marked `UNRESOLVED`.

## V1.1 execution and authorization

The complete construction card is
[`VR-V1.1-TRANSCRIPT-FOUNDATION-013`](../tasks/VISUAL-REPORT-V1-1-TRANSCRIPT-FOUNDATION.md).

- A/B/C were the original implementation order and are already complete. The
  four changes in the task card's active final-rework section are the only
  remaining construction sequence and are not intermediate Owner gates.
- Explicit ROI OCR is the reliable primary path.
- Auto ROI is best-effort and cannot block V1.1 completion.
- Subtitle absence is normal degradation, not failure.
- No readiness validator, formal Eval framework, frozen measurement, or
  per-slice authorization is required.
- The Owner authorized the continuous construction Goal on 2026-09-01. A/B/C
  are implemented in this checkout; Owner acceptance, commit, push, deployment,
  and publication remain out of scope.
- The later full-video content review withdrew the review-ready state. The final
  bounded Fusion rework was then authorized and executed continuously on
  2026-09-01; the current stop is Owner freeze review.

## V1.1 implementation evidence

Delivery details are in [`V1.1-DELIVERY.md`](V1.1-DELIVERY.md). The completed
implementation provides:

- A: local RapidOCR explicit-ROI sampling, visual-change filtering,
  perceptual deduplication, timestamped OCR events, and traceable confidence/
  stability provenance.
- B: source-preserving `SourceTextEvent`, `TranscriptUnit`, and
  `TranscriptManifest` artifacts; deterministic local alignment/fusion;
  conservative `UNRESOLVED` handling; and transcript-unit provenance on the
  compatible 45–60 second `VideoSegment` projection.
- C: SRT/VTT/ASS subtitle parsing and local sidecar/container discovery,
  best-effort Auto ROI, MP4/URL CLI options, and minimal Web OCR/FUSING/
  degraded status exposure. Subtitle absence is recorded as `DEGRADED`, not a
  pipeline failure.

Real local checks produced deduplicated OCR on the Wu Yi and Bilibili game
videos, a conservative Auto ROI result for the game video, an honest unstable
result for Wu Yi and the presentation negative sample, a fused 302-unit /
30-segment game transcript, and a local 30-second MP4 ingest with 11 units and
one projected segment. The checked game sample contains one source-backed local
OCR correction (`礼店` → `里店`); a visually wrong multi-character OCR candidate
(`由于` → `由干` alongside another change) is retained as ASR provisional and
`UNRESOLVED`.

The unchanged semantic-v2 planning/renderer path was exercised with provider-free
replay for ASR-only and fused inputs; both produced `report.html`. No provider
arbitration was needed, and no video, frame, or OCR model call left the local
machine. Final checks and exact artifact paths are recorded in the delivery
document. That prior checkpoint stopped at `READY_FOR_OWNER_V1.1_REVIEW`; it was
not Owner acceptance.

The first Owner review requested changes because Fusion was too conservative.
The bounded refinement now accepts reliable Explicit ROI short spans (including
single-frame evidence at confidence `>= 0.90`) and internal insertions, while
Auto ROI remains multi-frame-only, OCR deletion remains rejected, and adjacent
mixed conflicts such as `于礼` → `干里` remain `UNRESOLVED`. Regenerated game
artifacts and provider-free ASR-only/Fused reports are recorded in the delivery
document; that checkpoint returned to `READY_FOR_OWNER_V1.1_REVIEW` without
Owner acceptance.

The subsequent full-video coverage review found that earlier real OCR evidence
covered only the first 30–70 seconds. Manifest coverage semantics and one real
full-video Explicit ROI OCR/Fusion run are now complete: the 1,566,677 ms game
video produced 504 OCR events with `processed_start_ms=0`,
`processed_end_ms=1566677`, `coverage_ratio=1.0`, and
`coverage_status=FULL`. The regenerated Canonical Transcript has 302 units and
projects to 30 segments. A fresh semantic-v2 call was first attempted without
replay in the sandbox and could not connect. After the Owner explicitly
authorized sending complete Fused and ASR-only transcript text to
`https://api.deepseek.com`, both fresh runs completed with exactly 2/2 model
calls and reached `RENDERED`. The Fused report has 5 sections / 8 blocks and
cites 26 unique segments; ASR-only has 5 / 9 and cites 13. This closes the
full-video execution gap. It did not establish transcript-quality acceptance.

The following Owner content review found that repeated correct OCR such as
`献祭` and `星象房` still failed to enter Canonical text reliably, while unstable
name candidates remained unsafe. This is a general Fusion defect, not a request
for video-specific word rules. At that historical pre-rework checkpoint, the
state was therefore `CHANGES_REQUESTED`, not Owner Review.

The only remaining V1.1 construction scope at that checkpoint was one finite
repair:

```text
frame-level OCR candidates
  → simple 2–5 frame consensus
  → ±1.5 s / current Unit ±1 local matching
  → high-evidence 1–8 character replace-only Fusion
  → full-video fresh OCR / Canonical / Semantic / Render rerun
```

No public candidate schema, consensus/alignment version-governance system,
complex alignment algorithm, terminology dictionary, or new Eval framework is
part of this repair. V1.2 remains unauthorized.

The final bounded rework is complete. Full local Explicit-ROI OCR for the same
game video retained `757` frame candidates and produced `504` OCR events over
`0–1,566,677 ms` with `coverage_ratio=1.0` and `coverage_status=FULL`. Fresh
Fused and ASR-only Canonical/segments each contain `302 / 30` records. Final
Fused accepts `20` multi-character replacement rows across `16` Units; every
row is OCR-backed, replace-only, supported by `2–5` candidates with support
`>=2`, and within the `1–8` span bound. `星象` and `献祭` now enter Fused
`canonical_text` values, while `由干`, `干里`, and `里店 END` remain absent
from those values and the accepted replacements.

The final fresh downstream runs used new, non-replayed inputs and the unchanged
semantic-v2/Renderer path. Fused
`fused-semantic-v2-20260901-final` reached `RENDERED` with `2/2` calls,
`5` sections, and `11` blocks. ASR-only
`asr-only-semantic-v2-20260901` reached `RENDERED` with `2/2` calls,
`4` sections, and `10` blocks. Focused Transcript Foundation tests reached
`30 passed`, the required combined focused suite `51 passed`, full pytest
`132 passed`, Ruff passed, and `git diff --check` passed. The current state is
`READY_FOR_OWNER_V1.1_FREEZE_REVIEW`; no V1.1 freeze or V1.2/V1.3
authorization is recorded.

## Final V1.1 model refresh

The construction commit/worktree was the completed `V1.1 Fusion`
submission described by Task 013; it is the required baseline for all following
work. Owner review did not freeze V1.1. The Owner judged the remaining upstream
ASR/OCR error rate too high to justify more Fusion tuning and selected one final
bounded source-model refresh:

```text
existing V1.1 Fusion baseline
  + mlx-community/whisper-large-v3-turbo
  + PP-OCRv6 Small detection/recognition on ONNX Runtime
  → unchanged consensus/alignment/Fusion
  → existing Zhipu GLM / glm-5.3-flash Semantic-v2
  → full-video fresh ASR-only and Fused Semantic/Render comparison
```

The construction-ready card is
[`VR-V1.1-MODEL-UPGRADE-014`](../tasks/VISUAL-REPORT-V1-1-MODEL-UPGRADE.md).
It does not authorize starting from the older V1.0 baseline, redoing Fusion,
running a model bake-off, adding terminology rules, changing semantic prompts,
switching the current GLM Semantic provider/model, or changing the renderer.
Historical DeepSeek run records remain historical evidence and are not the
provider contract for Task 014. The next construction run must stop at
`READY_FOR_OWNER_V1.1_MODEL_REVIEW` even if the measured quality gain is small.

Task 014 completed at that stop. The final fresh Small/Large run
`v11-model-upgrade-small-game-20260902-r3` used the same 1,566,677 ms video and
Explicit ROI, reached full OCR coverage (`545` OCR events, `coverage_ratio=1.0`),
and produced fresh Fused and ASR-only Canonical/segments, Semantic-v2, and
reports under new run identities. The unchanged Fusion path accepted `6`
OCR replacements versus `20` in the Task 013 bounded baseline; Large V3 Turbo
improved selected ASR terms but overall source-model quality was mixed rather
than a broad accuracy gain. Focused tests (`55`), full pytest (`137`), Ruff,
`uv lock --check`, and `git diff --check` all passed. That execution stopped at
`READY_FOR_OWNER_V1.1_MODEL_REVIEW`.

## Owner closure and V1.2 authority

On 2026-09-04, the Owner accepted commit `2bce883` as the V1.1 baseline and
ended V1.1. The accepted baseline retains the measured mixed ASR/OCR result and
known residual recognition errors; it does not claim perfect transcript
quality. Further Transcript Foundation or source-model tuning requires an
explicit scope reopen.

The same Owner decision authorizes V1.2 requirements and technical design for
one integrated Visual Editorial Agent / Harness. The design must cover
Semantic, Presentation, deterministic Renderer, Browser Observation, and
bounded Critic repair as one workflow. It does not authorize product code,
dependency changes, provider calls, browser execution, real V1.2 runs,
deployment, publication, or V1.3 implementation.

## Historical sources

- [`V1A-STATUS.md`](V1A-STATUS.md) is now a compressed historical compatibility
  index.
- `docs/requirements/visual-report-v1a/` remains the frozen semantic-v2 design
  and historical evidence package.
- Existing Task 001–012 documents remain the detailed audit trail for V1.0.
- V0 and P0-B inputs, results, and evaluation conclusions remain unchanged.
