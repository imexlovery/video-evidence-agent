# Decisions, Alternatives, Risks, and Architecture Ablation

## Decision authority

`decision-evidence.jsonl` is the append-only record of Owner-confirmed V1.2 decisions. Later records
clarify earlier ones. In particular:

- `DEC-VR12-024` removes the bounded Presentation Profile mentioned in `DEC-VR12-005`;
- `DEC-VR12-029` narrows Defect severity to `BLOCKING`/`NON_BLOCKING` and fixes terminal semantics;
- `DEC-VR12-030` fixes one run-level model configuration;
- `DEC-VR12-031` defines this package as Design Baseline rather than Final Spec;
- `DEC-VR12-032` narrows technical retry and fixes Revision consumption timing;
- `DEC-VR12-033` freezes capabilities rather than independent call topology;
- `DEC-VR12-037` replaces the target-list/diff detail in the Semantic portion of
  `DEC-VR12-028` with the simpler source-grounded Revision and full downstream-regeneration rule.

## Confirmed decision summary

| Decision IDs | Confirmed outcome |
|---|---|
| 001–002 | V1.1 baseline `2bce883` is closed; V1.2 design only; G2 named-owner local pilot |
| 003–004 | Chinese long-form report scope; existing entry points; stability is quality floor/variance rather than byte identity |
| 005–007 | one Design System, controlled vocabulary, deterministic Renderer, runtime Observer, two total Revisions/one Semantic |
| 008–012 | minimal grounded Claims, Editorial/Presentation split, three terminal outcomes, pre-freeze Architecture Ablation |
| 013–015 | fixed Harness and Artifact snapshots; optional supplied assets; narrow deterministic Observer; no free browser/tool loop |
| 016–018 | only 1080px desktop is a hard visual surface; fixed Editorial Objective; no Brief/customization |
| 019–021 | reuse V1.1 uncertainty, fail unsafe core, complete-context 50k envelope, stable shell plus adaptive body |
| 022–024 | model may read supplied assets/screenshots; local product; Python/Pydantic; no framework or named profile |
| 025–027 | Controller-only Semantic escalation; parallel V1.2 path; legacy ReportPlan/seven blocks are not contracts |
| 028–029 | typed Artifact regeneration without Patch DSL; same-layer related Defect set; minimal Defect/terminal vocabulary |
| 030–032 | single-model architecture; Design Baseline/calibration/ablation/freeze sequence; exact retry and budget timing |
| 033–034 | capabilities do not fix call topology; honest repeated calibration/locked-evaluation structure without fixed 27-run matrix |
| 035–037 | one-way semantic ownership; minimal Claim fields/provenance; simple source-grounded Semantic Revision and full cascade |

## Rejected alternatives

### Prompt-only report generation

Rejected because it cannot deterministically enforce source lineage, semantic/presentation authority,
real-render observation, finite repair, or retention of all runs. Prompt quality remains useful
inside the Harness but is not the product boundary.

### Unrestricted coding agent

Rejected for V1.2 because free file/browser/tool control and unconstrained continuation undermine
repeatability and authority. The Harness reproduces the valuable observe-and-repair behavior through
typed, narrow stages.

### Fixed semantic output filled into legacy blocks

Rejected because Editorial cannot adapt narrative structure and the old seven-block vocabulary
becomes a hidden content constraint. Legacy primitives may be reused only behind a new Presentation
contract.

### Critic rewrites the report

Rejected because it creates semantic drift and open-ended optimization. Critics report Defects;
Controller authorizes one-layer typed Artifact regeneration under a two-unit budget.

### Free ReAct, multi-agent, LangGraph, Hypha, or MCP workflow

Rejected for V1.2 because the required graph is fixed and shallow. Project-owned Python/Pydantic is
the smallest sufficient choice. Typed seams keep later migration possible.

### Patch DSL and generic invalidation engine

Rejected because whole typed Artifact regeneration plus direct Controller version links satisfy the
bounded use case. Exact stable-ID and scope-check mechanics are calibrated for minimum complexity.

### Hidden long-context fallback

Rejected because truncation/chunking changes source coverage invisibly. Input above 50,000 Unicode
characters fails explicitly.

### Multiple styles, Profiles, and mobile gates

Rejected for the V1.2 baseline. One Design System still allows controlled composition. Profiles may
emerge only from repeated evidence; mobile remains best-effort.

## Core contract versus calibration parameters

### Fixed by this Design Baseline

- target user/grade and local product boundary;
- full V1.1 Canonical Transcript as sole factual authority;
- Claim → Editorial → Presentation ownership and full provenance;
- fixed Editorial Objective and adaptive body;
- single run-level model and no fallback;
- controlled visual expression with no executable model page language;
- deterministic Renderer and required 1080px Browser Observation;
- two total Revisions, one Semantic maximum, and exact retry semantics;
- downstream regeneration after Semantic Revision;
- `COMPLETE`/`DEGRADED`/`FAILED` meaning;
- parallel versioned V1.2 path and separate Owner gates.

### Fixed by calibration and Owner Final Spec freeze

- concrete Presentation Vocabulary membership;
- deterministic content/component/density/asset ceilings;
- model-call combination or separation;
- Observer detail beyond the minimum;
- simplest stable-ID retention and Semantic authority check;
- human quality rubric and unacceptable-run definition;
- formal evaluation sample/repeat counts and thresholds.

These parameters are intentionally evidence-owned; they cannot be used to reopen the fixed list.

## Risk register

| Risk | Control in Design Baseline | Required evidence |
|---|---|---|
| Model variability still creates weak runs | typed schemas, hard gates, repeated evaluation, no best-of-N | worst-case, unacceptable-rate, and variance comparison |
| Claim/Editorial omissions make report incomplete | explicit semantic review and fixed reader objective | source-to-report coverage review on calibration and locked samples |
| Fluent synthesis exceeds evidence | `STATED`/`SYNTHESIS`, evidence binding, semantic review | adversarial unsupported-synthesis tests and human source audit |
| Presentation smuggles in meaning | no semantic fields, Editorial trace for every substantive string/relation | authority-negative tests and deterministic diff of rendered text to Editorial |
| Visual repair drifts correct content | Presentation default, no Semantic write authority, bounded Semantic escalation | revision lineage and before/after semantic checks |
| Critic pursues taste indefinitely | rule-defined Defects only and two-unit budget | zero Revision for aesthetic-only fixtures |
| Vocabulary is too narrow and feels templated | content-adaptive plan and calibration-owned vocabulary | varied historical samples and human ratings |
| Vocabulary is too broad and unstable | allowlist and deterministic ceilings | invalid-plan rate and cross-run presentation variance |
| Browser sensor misses visible defects | real screenshot plus geometry/overflow/clipping minimum | injected-layout-fixture detection and human cross-check |
| Browser/runtime differences reduce reproducibility | fixed viewport and recorded runtime versions | model-free re-observation comparison |
| Semantic Revision becomes a hidden rewrite | evidence required for additions, semantic revalidation, full cascade | before/after provenance and authority tests |
| Call topology adds cost without quality | all roles share model; topology is ablatable | same-source ablation of quality, cost, and latency |
| External Provider receives sensitive content | explicit disclosure, Owner configuration, no secret persistence | UI/config disclosure and secret-leak tests |
| V1.2 corrupts legacy evidence or behavior | parallel versioned path, no fallback, isolated runs | affected legacy tests and filesystem-write assertions |
| Calibration overfits historical samples | historical-only calibration and untuned locked set | sample registry and frozen evaluation manifest |
| Formal results are cherry-picked | repeats, all results in denominator, no selective rerun | immutable run manifest and denominator reconciliation |
| Local pilot assumptions leak into public release | explicit G2 limits and V1.3 productization gate | new requirements package before hosting/public use |

The named Owner owns all current risks because V1.2 has one local operator and no service team.

## Required Architecture Ablation

The ablation pass is mandatory after real-run calibration and before Final Spec freeze. For each
candidate, compare the current mechanism with the simplest viable removal/combination under the same
source and declared configuration.

| Candidate | Simpler comparison | Keep only if |
|---|---|---|
| independent Semantic Critic call | validation plus review in semantic construction call | material grounding/coverage gain exceeds cost/variance impact |
| split Critic and Reviser calls | one bounded review-and-replacement call | separation improves legal repair or reduces drift |
| broad Presentation Vocabulary | remove each low-use primitive/dimension | primitive improves varied-report quality without raising invalidity |
| complex safety ceilings | one small deterministic ceiling set | added rule prevents observed failure |
| Observer fields beyond minimum | screenshot + geometry + overflow/clipping only | field detects a real material Defect reliably |
| stable-ID/diff machinery | direct snapshot/version and provenance checks | added machinery prevents an observed authority violation |
| legacy compatibility layer | reuse primitives directly behind V1.2 | layer reduces implementation risk without constraining V1.2 |
| second Revision opportunity | zero/one/two Revision comparison | second opportunity reduces unacceptable runs without drift/cost failure |

The ablation outcome is removal by default when evidence is neutral. It cannot remove mandatory
source grounding, explicit Semantic review, real Render/Observe, visual review, post-Revision
revalidation, Controller termination, or the terminal semantics.

## No open core-architecture question

The Q1–Q30 grilling sequence closed every question that would alter V1.2 product behavior or core
architecture. Remaining implementation/calibration choices are explicitly bounded above. Discovery
does not need another governance object, state taxonomy, Claim relationship model, Profile, or
workflow framework before construction can be separately authorized.
