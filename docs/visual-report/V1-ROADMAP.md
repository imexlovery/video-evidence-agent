# Visual Report V1 — Roadmap

Updated: 2026-09-04

The roadmap preserves separately testable quality layers, but V1.2 now designs
their Agent coordination and shared contracts end to end. Internal construction
slices are sequencing boundaries, not separate architecture designs.

## V1.0 — Runnable Alpha baseline

Status: `IMPLEMENTED / QUALITY_NOT_ACCEPTED`

V1.0 is the current local MP4 and Bilibili URL product path. It includes ASR,
45–60 second `VideoSegment` projection, semantic-v2 planning, the deterministic
renderer, loopback Web use, and the single-process FIFO queue.

The historical implementation name `V1-A` remains in schemas, commands, task
IDs, tests, paths, and retained evidence. No compatibility rename is planned.

## V1.1 — Transcript Foundation

Status: `V1.1_FROZEN`

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

The Owner authorized the continuous construction Goal on 2026-09-01. A/B/C were
implemented and locally validated. Their completion did not automatically
promote the project to V1.2.

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

The authorized model-refresh execution completed. The final Small/Large
fresh run reached full-video OCR coverage and generated new ASR-only/Fused
Semantic-v2 reports with the unchanged Zhipu GLM path. The measured result is
mixed: selected Large V3 Turbo ASR terms improve, while unchanged Fusion
accepts fewer OCR replacements than Task 013. That construction run stopped at
`READY_FOR_OWNER_V1.1_MODEL_REVIEW`.

On 2026-09-04, the Owner accepted HEAD `2bce883` as the V1.1 baseline and ended
V1.1. The mixed source-model outcome and residual recognition errors remain
documented limitations rather than triggers for more V1.1 tuning. This decision
freezes the V1.1 input contract and separately authorizes V1.2 requirements and
technical design; it does not authorize V1.2 product implementation.

## V1.2 — Visual Editorial Agent / Harness

Status: `REQUIREMENTS_AND_TECHNICAL_DESIGN_AUTHORIZED / IMPLEMENTATION_NOT_AUTHORIZED`

V1.2 will design one source-grounded, end-to-end Harness that transforms the
frozen V1.1 Canonical Transcript into a visually reviewed report while keeping
each quality layer independently observable. The shared workflow comprises:

1. Canonical Transcript to Claim Graph;
2. Claim Graph to Editorial Plan;
3. one bounded Semantic Critic and local semantic revision;
4. Editorial Plan to Presentation Plan;
5. deterministic rendering;
6. DOM and screenshot observation;
7. one bounded Visual Critic and local presentation revision; and
8. final validation plus complete run-artifact retention.

The design must define the common state model, artifact schemas, issue routing,
patch authority, revision budgets, failure behavior, evidence lineage, and stop
conditions before any internal slice is implemented. Tentative construction
slices are:

- **A — Editorial intelligence:** Claim Graph, Editorial Plan, grounding,
  Semantic Critic, and semantic patching;
- **B — Presentation intelligence:** Presentation Plan, visual grammar, and the
  deterministic Renderer contract;
- **C — Closed-loop quality:** Browser Observation, Visual Critic, global issue
  routing, bounded revision, comparison evaluation, and run freezing.

These slices share one design and one Controller. They may be implemented and
evaluated incrementally, but must not introduce throwaway cross-version
contracts. V1.2 should compare semantic behavior against the V1.1 transcript
rather than compensate for ASR mistakes inside prompts.

The current authority permits documentation and read-only inspection only. No
prompt, Topic Mapper, Report Planner, Agent runtime, Renderer, browser tool,
dependency, model call, or generated runtime artifact may be changed or
executed under this design authorization.

## V1.3 — Post-Harness evolution

Status: `DEFERRED / SCOPE_TO_BE_DECIDED_AFTER_V1.2`

V1.3 is intentionally not preassigned to a renderer-only redesign because
Presentation, Renderer, Browser Observation, and visual repair now belong to
the integrated V1.2 Harness. Evidence from V1.2 will determine whether V1.3
should focus on multi-style templates, Skill/plugin packaging, broader content
domains, quality hardening, or another explicitly approved direction.

## Promotion order

```text
V1.0 runnable baseline
  → V1.1 frozen transcript foundation
  → V1.2 integrated Visual Editorial Agent / Harness
  → V1.3 evidence-selected post-Harness evolution
  → later deployment/multi-user work only when product quality warrants it
```

There is no date or automatic promotion. Requirements/design authority,
implementation authority, validation, Owner acceptance, deployment, and
publication remain separate decisions.
