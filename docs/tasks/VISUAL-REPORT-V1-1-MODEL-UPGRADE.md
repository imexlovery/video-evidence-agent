# VR-V1.1-MODEL-UPGRADE-014 — Local ASR/OCR Model Refresh

Updated: 2026-09-04

## Task metadata

| Field | Value |
|---|---|
| Product version | `Visual Report V1.1` |
| Task ID | `VR-V1.1-MODEL-UPGRADE-014` |
| Target | Local Alpha / controlled real-video validation |
| Task-card status | `CLOSED — V1.1_FROZEN` |
| Starting point | Existing construction commit/worktree: completed `V1.1 Fusion` (Task 013) |
| Existing Semantic provider | Zhipu GLM OpenAI-compatible endpoint / `glm-5.3-flash` |
| Required construction stop | `READY_FOR_OWNER_V1.1_MODEL_REVIEW` or one explicit hard blocker |
| Execution style | One bounded model refresh and one complete fresh rerun |
| Deployment / publication | Excluded |

This card is the complete construction contract for the model refresh. The
current construction baseline is the existing `V1.1 Fusion` implementation and
its completed full-video evidence, including all Task 013 frame consensus,
neighboring-Unit alignment, replace-only Fusion, Canonical projection, and
fresh Semantic/Render work. The model upgrade is an incremental change on top
of that baseline; it does not reopen or reimplement the Fusion design. Product
code, dependency changes, model downloads, and real runs start only from a new
explicit Owner Goal that names this task.

## Owner decision and objective

The Owner selected these local models:

- ASR: `mlx-community/whisper-large-v3-turbo`;
- OCR detection: Chinese `PP-OCRv6 Small` on ONNX Runtime;
- OCR recognition: Chinese `PP-OCRv6 Small` on ONNX Runtime.

The objective is to measure the practical gain from stronger source models on
the existing full-video V1.1 path. This is not another attempt to perfect game
subtitle recognition. ASR and OCR may both remain wrong; the run must report
that result honestly rather than compensate with vocabulary rules or looser
Fusion.

## Mandatory read order

1. `AGENTS.md`
2. `docs/visual-report/V1-STATUS.md`
3. `docs/visual-report/V1-ROADMAP.md`
4. `docs/tasks/VISUAL-REPORT-V1-1-TRANSCRIPT-FOUNDATION.md`
5. this card
6. the directly affected source and tests

Treat the current checkout as the Owner's existing `V1.1 Fusion` construction
submission, whether its changes are already committed or still present in the
working tree. Preserve all Task 013 implementation and evidence. Do not reset,
rewrite, delete, or relabel prior source changes or artifacts, and do not start
from the older V1.0/ASR-only baseline.

## Construction scope

### Change 1 — make Large V3 Turbo the effective ASR model

1. Keep the existing `mlx-whisper` adapter and Chinese timestamped ASR
   contract unchanged.
2. Make `mlx-community/whisper-large-v3-turbo` the consistent default in the
   CLI, `.env.example`, README examples, and any committed runtime default.
3. A developer's uncommitted `.env` may be updated locally when required, but
   never print, copy, or commit its other values.
4. Keep `--asr-model` as an explicit override. Do not add model routing,
   fallback, ensemble, decoding experiments, or a model registry.
5. Allow `mlx-whisper` / Hugging Face Hub to resume or download the model into
   the normal user cache. Do not copy model weights into the repository or run
   artifacts.
6. Preserve the exact ASR engine and model identifier in the existing run
   manifest/snapshot and verify that the fresh run did not silently use Small.

Expected local cache class:

```text
/Users/tristana/.cache/huggingface/hub/
```

The absolute cache path is execution evidence, not a public product contract.

### Change 2 — migrate the OCR adapter to PP-OCRv6 Small

1. Replace the legacy `rapidocr-onnxruntime` dependency with the unified
   `rapidocr>=3.9.0` package and keep ONNX Runtime as an explicit project
   dependency. Use the existing `uv` workflow and update `uv.lock`.
2. Update only the existing lazy `RapidOcrAdapter`. Configure both detection
   and recognition as Chinese `PPOCRV6 + SMALL + ONNXRUNTIME`; keep the
   package's ordinary text-direction classifier unless the API requires an
   explicit equivalent.
3. Adapt the unified RapidOCR result object (`boxes`, `txts`, and `scores`, or
   the installed public equivalent) back into the existing `OcrDetection`
   boundary. Downstream frame filtering, consensus, alignment, Fusion,
   Canonical, and coverage behavior must remain unchanged.
4. Update the retained OCR engine/version provenance to identify PP-OCRv6
   Small. The fresh manifest or OCR provenance must make the detection and
   recognition model selections inspectable.
5. Let RapidOCR download its selected models through its supported mechanism.
   For this bounded local task, its installed-environment model directory is
   acceptable. Do not add a cache manager, copy the ONNX files into Git, or put
   model weights under `artifacts/`.

Expected default model location for this project environment:

```text
/Users/tristana/Develop/video-evidence-agent/.venv/lib/python3.12/site-packages/rapidocr/models/
```

The implementation must use the installed package's public API rather than
depending on this absolute path. If the package requires explicit paths for
Small models, use its supported path parameters and document the resolved
local paths without inventing a new public configuration system.

### Change 3 — focused compatibility tests

Provider-free tests must prove:

1. the committed ASR default is Large V3 Turbo while an explicit CLI override
   still works;
2. the RapidOCR adapter requests PP-OCRv6 Small detection and recognition on
   ONNX Runtime;
3. the unified RapidOCR output object maps boxes, text, and confidence into the
   existing `OcrDetection` values, including empty output;
4. OCR frame candidates and consensus still consume the adapter output without
   contract changes;
5. the Task 013 neighboring-Unit and replace-only Fusion regression cases stay
   unchanged;
6. CLI/URL/Web and ASR-only paths do not require OCR and retain their current
   behavior.

Do not make tests depend on downloading models or calling a provider. Use a
small fake public-result shape at the adapter boundary.

### Change 4 — one complete fresh real-video comparison

After focused tests pass, use the same complete game video, existing Explicit
ROI `[0.12, 0.74, 0.88, 0.96]`, and current sampling settings. Create a new run
identity and regenerate everything; do not reuse old ASR, OCR events,
Canonical Transcript, segments, Topic Map proposal, or Report Plan proposal.

```text
Full-video audio
  → Large V3 Turbo ASR
Full-video frames
  → PP-OCRv6 Small Explicit-ROI OCR
  → existing frame consensus
ASR + OCR
  → unchanged alignment and Fusion
  → canonical-transcript.jsonl
  → segments.jsonl
  → fresh Fused semantic-v2
  → report.html
```

Also regenerate a fresh ASR-only Canonical/segments/Semantic/report comparison
from the same new Large V3 Turbo ASR output. Use the project's current Semantic
configuration unchanged:

```text
OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4
VIDEO_EVIDENCE_MODEL=glm-5.3-flash
```

The existing Zhipu GLM Semantic-v2 path may be called without another
authorization prompt. Send only the normal transcript text and semantic-v2
context; never send video, audio, frames, crops, or OCR images. Do not switch
back to DeepSeek, replay proposals, or change provider, model, prompt,
call-count policy, Planner, or Renderer. Read credentials from the existing
environment and never print or record secret values.

Compare the new outputs with the completed Task 013 baseline. Inspect, at
minimum:

- whether obvious ASR errors and game-specific terms decrease, stay similar,
  or move to different errors;
- whether correct PP-OCRv6 candidates enter Canonical under the unchanged
  Fusion policy;
- whether accepted OCR replacements contain obvious new pollution;
- whether `献祭`, `星象`, `星象房`, and unstable proper-name examples improve as
  post-run probes only, with no production special cases;
- whether the final Fused report shows any natural improvement over the fresh
  ASR-only report.

Record counts and representative examples in `docs/visual-report/V1.1-DELIVERY.md`.
This is one bounded manual comparison, not a new Eval framework.

## Acceptance and stop rule

Construction is complete when all of the following hold:

1. the fresh run proves the exact Large V3 Turbo and PP-OCRv6 Small model
   selections were used;
2. Explicit-ROI OCR covers `0` through the measured video end with
   `coverage_ratio=1.0` and `coverage_status=FULL`;
3. fresh Large V3 Turbo ASR-only and fresh Fused transcripts, segments,
   semantic-v2 outputs, and reports all exist under new run identities;
4. the unchanged Fusion safety regressions pass and the newly accepted OCR
   replacements have been manually checked for obvious pollution;
5. Task 013 baseline versus new-model results are recorded honestly, including
   the case where quality improvement is small, mixed, or absent;
6. focused tests, full pytest, Ruff, and `git diff --check` pass.

Meaningful accuracy improvement is desired but is not fabricated as a hard
pass threshold. If the stronger models show limited gain, retain that result
and stop at Owner review. Do not respond by tuning Fusion, adding dictionaries,
trying more OCR/ASR models, or expanding the task.

Final status:

```text
READY_FOR_OWNER_V1.1_MODEL_REVIEW
```

Only the Owner may then freeze V1.1, request a separate experiment, or move to
V1.2.

## Hard exclusions

- no Fusion, consensus, time-alignment, or replacement-policy changes;
- no terminology dictionary, prompt vocabulary, probe-specific branch, or
  manual transcript correction;
- no alternate ASR/OCR model bake-off, ensemble, fallback, or auto-selection;
- no VLM, full-scene OCR, keyframe work, fine-tuning, RAG, or Agent system;
- no semantic-v2 prompt, Topic Mapper, Report Planner, or Renderer changes;
- no Semantic provider/model change: keep the existing Zhipu GLM endpoint and
  `glm-5.3-flash`; DeepSeek is not part of Task 014;
- no new public schema, model registry, cache service, Eval framework, or
  quality-governance subsystem;
- no database, deployment, publication, commit, push, or PR.

## Final delivery evidence

Append, without rewriting Task 013 history:

- changed files and dependency versions;
- resolved model identifiers and local cache locations, excluding secrets;
- targeted and full validation commands/results;
- fresh run identities and artifact paths;
- full-video OCR processed range and coverage;
- ASR-only versus Fused comparison and Task 013 baseline comparison;
- bounded accepted-replacement inspection;
- final status or explicit blocker.

## Implementation evidence — 2026-09-02

The Owner changed the OCR selection to Small during execution. The final
completed downstream run is `v11-model-upgrade-small-game-20260902-r3`; an
earlier overlapping Small transcript run also completed, but lacked the source
metadata needed by the semantic command and was not reused for downstream
comparison. The earlier Medium attempt
(`v11-model-upgrade-game-20260902`) is also retained only as an execution note;
it is not part of the final comparison or a model bake-off.

### Source, dependencies, and provenance

- Source: the same local Bilibili game video used by Task 013,
  `artifacts/visual-report/url-ingest/url-bilibili-BV1aTtb6uE7d-534f521ef87b/download/source.mp4`;
  duration `1,566,677 ms` (26:06.677), source SHA-256
  `1a2bdf87f6c8a729159bfef9335082bda062c0ac006ac24601c34c52eed3f63a`.
- Locked runtime versions: `mlx-whisper==0.4.3`, `rapidocr==3.9.2`,
  `onnxruntime==1.29.0`; `pyproject.toml` and `uv.lock` now use unified
  `rapidocr>=3.9.0` plus explicit `onnxruntime>=1.29.0`.
- ASR provenance in the fresh manifest is
  `mlx-whisper` / `mlx-community/whisper-large-v3-turbo` / `zh`.
- OCR provenance in every merged OCR event is
  `rapidocr-ppocrv6-small-onnxruntime.v1`, engine `onnxruntime`, detection
  `PP-OCRv6-small`, recognition `PP-OCRv6-small`. The resolved local model
  files are under the installed environment's
  `.venv/lib/python3.12/site-packages/rapidocr/models/` directory; no weights
  were copied into Git or the run artifacts.

### Fresh full-video outputs

The final manifest is
`artifacts/visual-report/v1.1/model-upgrade-small-20260902/game/v11-model-upgrade-small-game-20260902-r3/manifest.json`.
It reached `SUCCEEDED` with Large V3 Turbo ASR producing `324` units and the
unchanged Explicit ROI `[0.12, 0.74, 0.88, 0.96]` producing `545` OCR events
and `790` frame candidates. OCR processed `0..1,566,677 ms`,
`coverage_ratio=1.0`, `coverage_status=FULL`; Canonical and projected
segments contain `324` and `32` rows respectively. The measured transcript
foundation phase was `901,063 ms` (15:01.063); the full ASR phase was
`104,877 ms` (1:44.877).

Fresh ASR-only projection was generated from the same new `asr.json` into the
run's `asr-only/` directory. Both fresh transcript modes use the unchanged
`local-span-fusion.v1` projection contract; ASR-only has `324` Canonical units
and `32` segments, with OCR explicitly off.

### Semantic-v2 and report outputs

Both fresh runs used only normal transcript/semantic text context with the
current configuration `OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4`
and `VIDEO_EVIDENCE_MODEL=glm-5.3-flash`; no video, audio, frame, crop, or OCR
image was sent. Each run completed the unchanged two-call Topic Mapper →
Report Planner path and deterministic renderer:

- Fused: `semantic-v2/fused-semantic-v2-small-20260902-r1/`,
  `RENDERED`, `5` sections, `10` blocks, report `report.html`.
- ASR-only: `semantic-v2/asr-only-semantic-v2-small-20260902-r1/`,
  `RENDERED`, `5` sections, `15` blocks, report `report.html`.

The Fused report naturally contains `星象房` where the same-run ASR-only
report retains the ASR-derived `新巷房` wording. This is a bounded observed
downstream difference, not a semantic prompt or renderer change.

### Task 013 comparison and quality conclusion

| Measure | Task 013 final bounded Fusion | Task 014 final Small/Large run |
|---|---:|---:|
| ASR units / projected segments | `302 / 30` | `324 / 32` |
| OCR events / frame candidates | `504 / 757` | `545 / 790` |
| accepted OCR replacement rows / Units | `20 / 16` | `6 / 5` |
| Fused report sections / blocks | `5 / 11` | `5 / 10` |
| ASR-only report sections / blocks | `4 / 10` | `5 / 15` |

The report-count comparison is descriptive, not a controlled semantic-quality
score: Task 013's retained historical reports used its then-configured
DeepSeek run, while Task 014 is required to use the current Zhipu GLM path.
The source-model result is mixed. Large V3 Turbo improves several ASR probes:
`献祭` appears in `10` Small-run Canonical units versus `1` in the Task 013
Fused Canonical output, and `星象房` is accepted from OCR for the ASR span
`新相防`; `以之 → 已知` is also accepted twice. However, unchanged Fusion
accepts fewer OCR replacements overall (`6` versus `20`) despite the larger
OCR event count. Case variation such as `boss/BOSS` and unstable names such as
`李店/礼店/里店` remain unresolved; no terminology rule or manual correction
was added. All six accepted rows were inspected and have support `2–3` with no
obvious out-of-span pollution (the two `已知` rows are separate OCR events for
one Unit). There is therefore no claim of broad accuracy improvement.

### Validation and stop

- Focused compatibility and regression suite: `55 passed`.
- Full pytest: `137 passed`.
- Ruff: passed; `uv lock --check`: passed; `git diff --check`: passed.
- Protected Consensus, Alignment, Fusion Policy, Canonical, Semantic-v2
  provider/model/prompt/call-count, and Renderer behavior was not changed.

The bounded execution is complete and stops at
`READY_FOR_OWNER_V1.1_MODEL_REVIEW`. No commit, push, PR, deployment,
publication, V1.2, model bake-off, or further experiment was performed after
the final Small rerun.

## Owner closure

On 2026-09-04, the Owner accepted repository HEAD `2bce883` as the V1.1
baseline and ended V1.1. This closes the task as `V1.1_FROZEN` with the measured
mixed model-refresh result and known residual recognition errors retained. No
additional model run or implementation change was requested as part of the
closure.

The Owner separately authorized V1.2 requirements and technical design for an
integrated Visual Editorial Agent / Harness. Product implementation remains
unauthorized.
