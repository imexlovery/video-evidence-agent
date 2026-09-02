# Visual Report V1 — Roadmap

Updated: 2026-09-02

The roadmap is intentionally sequential. Each version isolates one quality
layer so later work is not used to conceal an earlier defect.

## V1.0 — Runnable Alpha baseline

Status: `IMPLEMENTED / QUALITY_NOT_ACCEPTED`

V1.0 is the current local MP4 and Bilibili URL product path. It includes ASR,
45–60 second `VideoSegment` projection, semantic-v2 planning, the deterministic
renderer, loopback Web use, and the single-process FIFO queue.

The historical implementation name `V1-A` remains in schemas, commands, task
IDs, tests, paths, and retained evidence. No compatibility rename is planned.

## V1.1 — Transcript Foundation

Status: `READY_FOR_OWNER_V1.1_MODEL_REVIEW`

Objective: build one general, traceable transcript layer from ASR, text subtitle
tracks, and burned-in subtitle OCR, then project it back into the current V1.0
`VideoSegment` contract.

Key boundaries:

- reliable explicit-ROI subtitle OCR first;
- Auto ROI best-effort only;
- sparse sampling, visual-change filtering, perceptual deduplication, and
  temporal subtitle merging;
- high-confidence, local, source-backed fusion only;
- ambiguous or sentence-level conflict keeps provisional ASR and is marked
  `UNRESOLVED`;
- original ASR/OCR/subtitle content is never overwritten;
- current semantic-v2 prompts/planning and renderer remain unchanged;
- no VLM, keyframes, full-scene OCR, RAG, Agent, database, multi-tenancy, or
  deployment.

Execution card:
[`docs/tasks/VISUAL-REPORT-V1-1-TRANSCRIPT-FOUNDATION.md`](../tasks/VISUAL-REPORT-V1-1-TRANSCRIPT-FOUNDATION.md).

The Owner authorized the continuous construction Goal on 2026-09-01. A/B/C are
implemented and locally validated; Owner acceptance is pending and no automatic
promotion to V1.2 is implied.

The full-video coverage correction completed local OCR and Fusion for one
1,566,677 ms real video at `coverage_ratio=1.0`. The regenerated Canonical
Transcript then passed through fresh, non-replay Fused and ASR-only semantic-v2
calls plus the deterministic renderer. Both reached `RENDERED`, returning V1.1
to Owner Review without implying acceptance or promotion to V1.2.

That content review found a remaining general Fusion gap: reliable repeated OCR
was still discarded by strict single-span handling or attached to the wrong
neighboring ASR Unit. V1.1 is therefore back in `CHANGES_REQUESTED`. Its final
bounded repair is limited to frame-candidate consensus, ±1 neighboring Unit
matching, conservative 1–8 character replace-only Fusion, and one complete
fresh-video rerun. Passing that repair makes V1.1 eligible for Owner freeze
review; it does not authorize V1.2.

That bounded repair is now the completed `V1.1 Fusion` construction baseline.
The next task must build directly on that existing commit/worktree and must not
reimplement or loosen Fusion. Owner review chose not to freeze V1.1 yet because
upstream ASR and OCR errors remain visible. One last bounded model refresh was
construction-ready: Large V3 Turbo ASR plus PP-OCRv6 Small detection and
recognition, followed by a complete fresh-video ASR-only/Fused comparison.
Fresh Semantic-v2 uses the already configured Zhipu GLM endpoint and
`glm-5.3-flash`; it does not return to the historical DeepSeek provider.
Limited or mixed quality gain is a valid measured result and ends the task
rather than triggering another transcript subsystem redesign.

Model-refresh execution card:
[`docs/tasks/VISUAL-REPORT-V1-1-MODEL-UPGRADE.md`](../tasks/VISUAL-REPORT-V1-1-MODEL-UPGRADE.md).

The authorized model-refresh execution is complete. The final Small/Large
fresh run reached full-video OCR coverage and generated new ASR-only/Fused
Semantic-v2 reports with the unchanged Zhipu GLM path. The measured result is
mixed: selected Large V3 Turbo ASR terms improve, while unchanged Fusion
accepts fewer OCR replacements than Task 013. The roadmap therefore stops at
`READY_FOR_OWNER_V1.1_MODEL_REVIEW`; it does not imply V1.1 freeze or authorize
V1.2.

## V1.2 — Semantic Quality

Status: `BRIEF_ONLY / NOT_AUTHORIZED`

After V1.1 makes transcript truth inspectable, V1.2 will revisit how the full
canonical transcript is understood, mapped into topics, compressed, and turned
into a report plan. The future design should compare semantic behavior against
the V1.1 transcript rather than compensate for ASR mistakes inside prompts.

No prompt, Topic Mapper, Report Planner, RAG, Agent, or model-routing redesign
belongs to V1.1.

## V1.3 — Renderer Quality

Status: `BRIEF_ONLY / NOT_AUTHORIZED`

After transcript and semantic quality are stable, V1.3 will improve visual
hierarchy, typography, component selection, information density, and
cross-video presentation quality while preserving deterministic rendering.

No renderer redesign, new template system, VLM-selected keyframes, or visual
export expansion belongs to V1.1.

## Promotion order

```text
V1.0 runnable baseline
  → V1.1 trustworthy transcript foundation
  → V1.2 semantic/report-planning quality
  → V1.3 renderer and visual quality
  → later deployment/multi-user work only when product quality warrants it
```

There is no date or automatic promotion. Completion of one version only makes
the next version discussable; it does not authorize it.
