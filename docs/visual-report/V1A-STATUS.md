# Visual Report V1-A — Historical Compatibility Index

Updated: 2026-09-01

`V1-A` is no longer the active product-roadmap name. The runnable baseline it
produced is now called **Visual Report V1.0**. This file is intentionally a
short historical index; detailed task cards, frozen requirements, run artifacts,
and Git history retain the old execution record.

For current work, start with:

1. [`V1-STATUS.md`](V1-STATUS.md)
2. [`V1-ROADMAP.md`](V1-ROADMAP.md)
3. [`VR-V1.1-TRANSCRIPT-FOUNDATION-013`](../tasks/VISUAL-REPORT-V1-1-TRANSCRIPT-FOUNDATION.md)

## Current interpretation

| Historical label | Current meaning |
|---|---|
| `V1-A`, `vr1a`, `semantic-v2` | Preserved implementation/evidence identifiers inside the V1.0 baseline |
| V1-A Topic Mapper + Report Planner | Existing V1.0 semantic planning stage; unchanged by V1.1 |
| V1-B keyframes | Superseded roadmap concept; not the current V1.1 |
| V1-C MP4/ASR | Superseded roadmap concept; local MP4/ASR and URL ingest already exist in V1.0 |
| Active next version | `V1.1 — Transcript Foundation` |

Do not rename historical schemas, commands, task IDs, run IDs, fixture paths,
or evidence directories. Their original names are compatibility contracts and
audit history, not current roadmap terminology.

## V1-A outcome retained as V1.0

The current checked code baseline before the V1.1 documentation update is
branch `visual-report` at
`065a592a8aa77829bdccc31828edadebc68a6d63`.

It supplies:

- existing manifest + `VideoSegment` transcript input;
- two sequential semantic-v2 stages: Topic Mapper and Report Planner;
- deterministic source binding, plan compilation, and V0 renderer reuse;
- local `report.html` output;
- a loopback Web surface;
- public Bilibili BV URL download → existing ingest → existing report flow;
- one in-memory FIFO queue with one active local worker.

This is a runnable Alpha baseline. It is not a statement that transcript,
semantic, or visual quality has been accepted.

## Condensed history

| Work | Retained result |
|---|---|
| V0 renderer | Deterministic report renderer and local HTML prototype implemented; historical visual-review record remains in V0 documents |
| V1-A strict planning | Built the first two-stage transcript-to-plan path and preserved failed provider/schema measurements |
| Recovery/provider experiments | Retained bounded failures and the provider-conformance no-go without rewriting their identities |
| semantic-v2 simplification | Replaced strict model-facing contracts with shallow semantic proposals plus deterministic non-semantic compilation |
| Adaptive budget closure | Allowed content-dependent report capacity while preserving current V0 contracts |
| Network-recovered text/Web closure | Produced the three-video local semantic-v2/Web evidence package; Owner content/visual acceptance remained separate |
| URL local MVP | Added public Bilibili BV URL → download → ingest → semantic-v2 → report flow |
| URL FIFO queue | Replaced active-run rejection with visible in-memory sequential queuing; no durable queue or multi-worker service |

## Detailed historical sources

Use these only when changing or auditing the corresponding historical contract:

- `docs/requirements/visual-report-v1a/` — frozen V1-A requirements, decisions,
  readiness output, semantic-v2 amendments, and test contracts;
- `docs/tasks/VISUAL-REPORT-V1A-PLANNING.md` — initial implementation;
- `docs/tasks/VISUAL-REPORT-V1A-MEASUREMENT.md` — strict measurement attempt;
- `docs/tasks/VISUAL-REPORT-V1A-GOAL-RECOVERY.md` — bounded recovery history;
- `docs/tasks/VISUAL-REPORT-V1A-PROVIDER-CONFORMANCE.md` — provider-conformance
  experiment;
- `docs/tasks/VISUAL-REPORT-V1A-CONTRACT-SIMPLIFICATION.md` — semantic-v2 design;
- `docs/tasks/VISUAL-REPORT-V1-TEXT-WEB-CLOSURE.md` and
  `docs/tasks/VISUAL-REPORT-V1A-ADAPTIVE-BUDGET-WEB-CLOSURE.md` — text/Web
  closure work;
- `docs/tasks/VISUAL-REPORT-V1A-NETWORK-RECOVERY-CANARY.md` and
  `docs/tasks/VISUAL-REPORT-V1A-NETWORK-RECOVERED-TEXT-WEB-CLOSURE.md` —
  network recovery and completed local Web evidence;
- `docs/tasks/VISUAL-REPORT-V1-URL-INGEST-LOCAL-MVP.md` — URL ingest;
- retained artifacts under `artifacts/visual-report/` and manifests under
  `eval/visual-report-v1a/` — detailed run evidence.

## Historical boundary

Frozen V1-A results remain immutable evidence. V1.1 may consume the current
V1.0 interfaces and add transcript-source artifacts, but it must not:

- rewrite old runs, measurements, rubrics, or conclusions;
- change semantic-v2 prompts, Topic Mapper/Planner behavior, or the renderer;
- reinterpret an old provider result as V1.1 evidence;
- publish rights-restricted local media or artifacts.

The active V1.1 task deliberately uses a lightweight design → implementation →
test → real-sample inspection loop. The old readiness/coverage/decision package
is historical and is not extended for V1.1.
