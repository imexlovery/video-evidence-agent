# Video Visual Report V0 — Decisions and Risks

## Implementation-grade and promotion decision

| Field | Decision |
|---|---|
| Current grade | `G1 PROTOTYPE` |
| Allowed/prohibited use | One local renderer proof; no public fixture sharing, deployment, production reliance, runtime AI, or V1 automation |
| Safety floor | Escaping, contained assets, visible validation, offline output, source refs, attribution, protected P0-B history |
| Deferred risks | Automated coverage/compression/asset quality and broader video/template fit remain unproven |
| Next grade/horizon | `V1 — Automated Video Report`, only after accepted V0 |
| Promotion evidence/approvers | Owner visual acceptance plus separate scope authorization |

## Decision log

| ID/status | Decision | Source | Drivers | Alternatives | Tradeoffs | Reversal | Verification |
|---|---|---|---|---|---|---|---|
| `DEC-VR0-001 / confirmed` | Grade is G1 Visual Prototype | Owner message | Validate product hypothesis cheaply | Build V1 immediately | Does not prove automation | Owner-only | Readiness evidence |
| `DEC-VR0-002 / confirmed` | Renderer-first is the active objective | Owner message | Visual output is highest uncertainty | Pipeline-first | Manual authoring accepted | Owner-only | Final artifact/rubric |
| `DEC-VR0-003 / confirmed` | Existing transcript and hand-authored plan are valid V0 input | Owner message | Isolate rendering | Automatic mapping | More manual effort | Owner-only | Real plan renders |
| `DEC-VR0-004 / confirmed` | Topic Mapper and Report Planner remain separate later | Owner message | Coverage and compression optimize different objectives | One prompt/call | Extra future stage | Owner-only | V1 design review |
| `DEC-VR0-005 / confirmed` | Assets are separate; blocks reference `asset_id` | Owner message | Reuse and clean responsibility | Keyframe request block | Cross-file validation | Owner-only | Contract tests |
| `DEC-VR0-006 / confirmed` | No free Layout Planner | Owner message | Stable visual system | LLM HTML/layout | Less per-report freedom | Owner-only | Plan has no style fields |
| `DEC-VR0-007 / confirmed` | Seven content types plus Hero/Section Header structure | Owner message | Small high-quality component set | 20 generic blocks | Narrower content grammar | Owner can add only after observed need | Component tests |
| `DEC-VR0-008 / confirmed` | HTML is canonical; other formats derive from it | Owner message | One rendering source | Separate PNG/PDF renderer | Browser remains required | Owner-only | Output scope |
| `DEC-VR0-009 / confirmed` | Desktop width 1080 px, natural height | Owner message | Preserve readability/density | Fixed 1080×1920 | Long page can be tall | Owner-only | Browser screenshot |
| `DEC-VR0-010 / confirmed` | Final keyframes may be selected manually | Owner message | Separate asset and visual hypotheses | Automatic ranking now | Does not prove Asset Resolver | Owner-only | 2–4 inspected assets |
| `DEC-VR0-011 / delegated` | RLinf is the single V0 fixture | Owner delegated one existing technical video | Diverse PPT/process/system content | Kling/Wu Yi fixtures | About 34:53 exceeds future range | Replace only before implementation with owner direction | Fixture inspection |
| `DEC-VR0-012 / fixed` | RLinf artifacts remain local/non-public | P0-B corpus | No explicit open license | Public demo | Public share value cannot be tested on this fixture | Use licensed future fixture | Rights review |
| `DEC-VR0-013 / delegated` | Visual identity is research notebook × systems blueprint with argument spine | Owner delegated concrete design | Subject-specific, non-generic output | Copy reference aesthetic; generic cards | One fixed theme | Iterate tokens within identity | Screenshots/owner review |
| `DEC-VR0-014 / delegated` | Existing Python/Pydantic; no new framework/service | Current repo + lean scope | Smallest implementation | New frontend toolchain | Less ecosystem tooling | Only after observed blocker | Dependency diff |
| `DEC-VR0-015 / confirmed` | Report claims retain lightweight timestamps/source refs | Owner product target | Return to source and correct errors | Evidence Gate reuse; no traceability | Some authoring overhead | Owner-only | 100% factual blocks |
| `DEC-VR0-016 / confirmed` | Screenshot iteration precedes schema stabilization | Owner phase order | Schema must serve visuals | Finalize schema first | Early fixture may change | Owner-only | Delivery evidence |
| `DEC-VR0-017 / confirmed` | Implementation is one bounded session with durable docs/status | Owner continuity request | Prevent context drift | Implicit chat memory/many tasks | Larger handoff package | Owner-only | AGENTS/status/task updates |
| `DEC-VR0-018 / confirmed` | Implementation stops for owner visual review; V1 is not authorized | Owner message | Human product-quality judgment | Auto-promote on green tests | Requires owner turn | Owner-only | Status state |

## Business, integration, and platform gap decisions

| Gap | Baseline evidence | Classification | Why adapter/overlay is insufficient | Reuse evidence | Owner | Acceptance |
|---|---|---|---|---|---|---|
| No visual-report renderer | Current source has ingest/retrieval/eval but no report components | Project-owned V0 module | This is the product hypothesis, not an adapter gap | Existing Python/Pydantic/FFmpeg retained | Implementer | Real HTML + tests + owner review |
| No automatic mapping/planning | Explicit V0 exclusion | Grade-deferred | Automation would confound renderer validation | Existing transcript enables manual plan | Owner | Separate V1 authorization |
| No publishable fixture rights | Corpus states local-only | Current-grade prohibition | Hosting wrapper cannot broaden rights | Local research use retained | Owner | Future licensed/user-owned fixture |

## Assumption register

| ID | Assumption | Evidence state | Impact if wrong | Validation |
|---|---|---|---|---|
| `ASM-VR0-001` | Fixed MP4/transcript/manifest remain readable locally | Confirmed at design inspection | Implementation cannot build real fixture | Phase S0/S1 read checks; stop without downloading |
| `ASM-VR0-002` | Four sampled timestamps yield at least 2 useful frames | Confirmed by preliminary visual inspection | Extract adjacent frames manually within same source | Contact-sheet review |
| `ASM-VR0-003` | Existing dependencies suffice for HTML composition/validation | Strong repository evidence | A minimal dependency exception may be needed | Implement simplest path before dependency change |
| `ASM-VR0-004` | Installed local browser can capture full-page desktop/mobile evidence | Expected local capability | Visual gate cannot be evidenced | Use another installed local browser; record limitation if none |
| `ASM-VR0-005` | Owner can judge save value from a private report even though public share is prohibited | Product-test assumption | Shareability remains untested | Rubric separates save value from public distribution |

## Risk register

| ID | Risk | Probability | Impact | Trigger | Prevention/mitigation | Owner | Verification |
|---|---|---|---|---|---|---|---|
| `RISK-VR0-001` | Output resembles generic AI cards | Medium | Critical | Uniform rounded grid, weak thesis/rhythm | Subject-specific identity, argument spine, varied section rhythm, screenshot critique | Implementer/owner | Desktop visual review |
| `RISK-VR0-002` | Technically complete pipeline crowds out design | Low after scope freeze | High | Automation/dependency work appears | Protected exclusions and task stop | Implementer | Diff/task review |
| `RISK-VR0-003` | Schema over-abstracts before visuals settle | Medium | High | Plugin/layout options or unused fields | Provisional closed union; stabilize after real report; delete unused abstraction | Implementer | Schema/diff review |
| `RISK-VR0-004` | Report is dense but not scannable | Medium | High | Owner cannot recover story in 60–90 s | 3–5 modules, thesis-led Hero, content budgets, whitespace/rhythm iteration | Implementer/owner | Comprehension rubric |
| `RISK-VR0-005` | Report is attractive but misses key content | Medium | High | Core RLinf progression/caveat absent | Read full transcript structure manually, then intentionally compress; owner content review | Implementer/owner | Source map/review |
| `RISK-VR0-006` | ASR errors become polished false metrics | Medium | High | Number/name supported only by noisy text | Verify clear source frame/cross-segment evidence or omit | Implementer | Metric review |
| `RISK-VR0-007` | Frames are decorative or illegible | Medium | Medium | Tiny slide text, redundant image | Select for information increment, preserve 16:9, caption/time, use 2–4 only | Implementer | Screenshot review |
| `RISK-VR0-008` | Rights-restricted material is published | Low | Critical | Deployment/public URL/committed media | Local-only root, no hosting, explicit AGENTS/task restriction | Everyone | Scope/diff review |
| `RISK-VR0-009` | Mobile adaptation becomes an afterthought | Medium | Medium | Overflow/miniature process | Required 390 px iteration in same session | Implementer | Mobile screenshot |
| `RISK-VR0-010` | V0 changes stable P0-B history/contracts | Low | High | Diff touches frozen eval/retrieval artifacts | Protected paths and full regression/diff review | Implementer | `git diff`, tests |
| `RISK-VR0-011` | Context compaction changes objective/state | Low after docs | High | Agent starts V1 or broadens scope | Root AGENTS read order, status resume, single task/evidence | Owner/implementer | Status consistency |
| `RISK-VR0-012` | One fixture overfits design | High | Medium | Second video needs new structure | Accept for V0; do not generalize until later reports | Owner | V1/multi-fixture evaluation |

## Intelligence, source-data, stability, customer-operation, vendor, compliance, and support risks

Runtime intelligence/vendor/customer-operation/support risks are not applicable
because V0 is A0 and local. Applicable residual risks are manual editorial bias,
ASR/source quality, single-fixture overfit, media rights, and local environment
availability. The risk register defines their bounded mitigations.

## Resolved contradictions

| Tension | Resolution |
|---|---|
| Original full video pipeline versus current priority | V0 starts from existing transcript/hand plan; automation moves to V1 |
| 1080×1920 concept versus content density | Canonical report is 1080 px wide with natural height; condensed poster is future |
| Keyframe as content block versus reusable material | Keyframe is an asset; blocks use optional `asset_id` |
| LLM layout flexibility versus reliable product output | Plan chooses semantics/order; deterministic renderer chooses all layout/style |
| Future 10–30 minute target versus 34:53 RLinf fixture | Explicit renderer stress-fixture exception; future boundary unchanged |
| “Worth sharing” hypothesis versus source rights | V0 measures private save value and perceived finish; actual public sharing waits for licensed/user-owned media |

## Residual non-blocking questions

There are no implementation-blocking product decisions. Fine-grained copy length,
exact type sizes inside the fixed hierarchy, and whether the final RLinf report
uses every optional content type are delegated to screenshot-driven iteration
within the documented component and visual envelope.
