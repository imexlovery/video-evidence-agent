# VR-V1.1-MODEL-UPGRADE-014 — Local ASR/OCR Model Refresh

Updated: 2026-09-02

## Task metadata

| Field | Value |
|---|---|
| Product version | `Visual Report V1.1` |
| Task ID | `VR-V1.1-MODEL-UPGRADE-014` |
| Target | Local Alpha / controlled real-video validation |
| Task-card status | `READY_FOR_CONSTRUCTION` |
| Starting point | Existing construction commit/worktree: completed `V1.1 Fusion` (Task 013) |
| Required final stop | `READY_FOR_OWNER_V1.1_MODEL_REVIEW` or one explicit hard blocker |
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
- OCR detection: Chinese `PP-OCRv6 Medium` on ONNX Runtime;
- OCR recognition: Chinese `PP-OCRv6 Medium` on ONNX Runtime.

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

### Change 2 — migrate the OCR adapter to PP-OCRv6 Medium

1. Replace the legacy `rapidocr-onnxruntime` dependency with the unified
   `rapidocr>=3.9.0` package and keep ONNX Runtime as an explicit project
   dependency. Use the existing `uv` workflow and update `uv.lock`.
2. Update only the existing lazy `RapidOcrAdapter`. Configure both detection
   and recognition as Chinese `PPOCRV6 + MEDIUM + ONNXRUNTIME`; keep the
   package's ordinary text-direction classifier unless the API requires an
   explicit equivalent.
3. Adapt the unified RapidOCR result object (`boxes`, `txts`, and `scores`, or
   the installed public equivalent) back into the existing `OcrDetection`
   boundary. Downstream frame filtering, consensus, alignment, Fusion,
   Canonical, and coverage behavior must remain unchanged.
4. Update the retained OCR engine/version provenance to identify PP-OCRv6
   Medium. The fresh manifest or OCR provenance must make the detection and
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
Medium models, use its supported path parameters and document the resolved
local paths without inventing a new public configuration system.

### Change 3 — focused compatibility tests

Provider-free tests must prove:

1. the committed ASR default is Large V3 Turbo while an explicit CLI override
   still works;
2. the RapidOCR adapter requests PP-OCRv6 Medium detection and recognition on
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
  → PP-OCRv6 Medium Explicit-ROI OCR
  → existing frame consensus
ASR + OCR
  → unchanged alignment and Fusion
  → canonical-transcript.jsonl
  → segments.jsonl
  → fresh Fused semantic-v2
  → report.html
```

Also regenerate a fresh ASR-only Canonical/segments/Semantic/report comparison
from the same new Large V3 Turbo ASR output. DeepSeek may be called through the
existing semantic-v2 path without another authorization prompt. Send only the
normal transcript text and semantic-v2 context; never send video, audio,
frames, crops, or OCR images. Do not replay proposals or change provider,
model, prompt, call-count policy, Planner, or Renderer.

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

1. the fresh run proves the exact Large V3 Turbo and PP-OCRv6 Medium model
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
