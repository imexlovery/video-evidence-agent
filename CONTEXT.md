# Video Evidence Agent

This glossary defines the product language used across the Video Evidence Agent and its Visual
Report workflow. It distinguishes source meaning, editorial decisions, presentation decisions,
and runtime evidence so that later specifications do not collapse them into one "report plan."

## Source and output

**Canonical Transcript**:
The V1.1 source-preserving transcript accepted as the authoritative textual input for downstream
report work, including explicit provenance and unresolved uncertainty.
_Avoid_: Clean transcript, corrected transcript

**Claim**:
A single atomic, reportable proposition that is either stated in the Canonical Transcript or is a
synthesis with explicit support from it; every Claim has a stable identifier and evidence bindings.
_Avoid_: Topic, external fact

**Claim Graph**:
The source-facing collection of Claims and their evidence links used as the semantic substrate for
editorial work; it is not a report outline or a general knowledge graph.
_Avoid_: Topic Map, report plan

**Candidate Report**:
A generated report that has reached a terminal run outcome but has not thereby received Owner
quality acceptance.
_Avoid_: Accepted report, final truth

**Canonical Report**:
The authoritative user-visible report artifact for one run; in V1.2 its formally supported visual
surface is the fixed-width desktop report, and canonical does not mean Owner-accepted.
_Avoid_: Screenshot, accepted report

**Report Shell**:
The stable outer structure shared by V1.2 reports: Hero and core overview, an ordered body, and
Sources and Limitations; it does not prescribe the body's chapter or component pattern.
_Avoid_: Report template, fixed outline

**Run Bundle**:
The retained source snapshot, intermediate decisions, observations, defects, revisions, terminal
state, and Candidate Report belonging to one execution identity.
_Avoid_: Output folder, final report

**Artifact Snapshot**:
The explicit, retained input seen by one model role or deterministic stage, independent of implicit
conversation memory.
_Avoid_: Chat context, working memory

**Visual Asset Set**:
An optional set of already supplied local images with source context that V1.2 may use but does not
discover or generate.
_Avoid_: Image search results, generated assets

**V1.2 Design Baseline**:
The Owner-confirmed requirements and technical design used to authorize a later implementation;
it fixes core boundaries but is not the Final V1.2 Spec.
_Avoid_: Frozen spec, implementation authorization

**Final V1.2 Spec**:
The Owner-frozen V1.2 contract produced only after implementation calibration and architecture
ablation have resolved the parameters explicitly reserved for runtime evidence.
_Avoid_: Design Baseline, implementation result

**Calibration Set**:
Historical or development samples used before Final V1.2 Spec freeze to tune evidence-reserved
parameters and test architecture ablations; their results are not final acceptance evidence.
_Avoid_: Locked evaluation set, acceptance set

**Locked Evaluation Set**:
Samples excluded from implementation calibration and used after Final V1.2 Spec freeze for formal
comparison across the declared report-generation conditions.
_Avoid_: Calibration set, selected showcase

## Visual editorial system

**Visual Editorial Agent**:
The bounded report-making capability that coordinates source-grounded editorial judgment,
presentation judgment, rendering observation, and finite repair.
_Avoid_: Report Planner, autonomous designer

**Harness**:
The product-owned control boundary that governs the Visual Editorial Agent's stages, authorities,
budgets, evidence, and terminal outcomes.
_Avoid_: Prompt, model wrapper

**Run Model Configuration**:
The single Provider and model configuration shared by every model-mediated role during one V1.2
run; roles differ by their contracts rather than by model identity.
_Avoid_: Role model, model router, fallback model

**Editorial Plan**:
The authoritative source for everything the Candidate Report says to the reader: final wording,
chapter order, content selection, and any semantic comparison, process, sequence, or grouping.
_Avoid_: Topic list, layout plan

**Editorial Content Unit**:
An individually identifiable piece of final semantic content in an Editorial Plan that can be
reviewed or revised without confusing it with a visual component.
_Avoid_: Presentation block, rendered section

**Editorial Objective**:
The fixed V1.2 goal of enabling a reader who has not watched the video to independently understand
its main conclusions, reasoning, key support, and important limitations.
_Avoid_: Editorial Brief, audience setting

**Presentation Plan**:
The decision about how an Editorial Plan is expressed using the controlled Presentation Vocabulary,
including whether and how supplied visual assets are used. It may not add reader-facing semantic
copy, conclusions, or relationships.
_Avoid_: Report copy, HTML specification

**Design System**:
The stable visual rules and reusable building blocks that define the report family's visual
identity.
_Avoid_: Template, generated style

**Presentation Vocabulary**:
The finite set of legal ways a report may express information through components, hierarchy,
density, emphasis, image weight, and spatial grouping inside the Design System.
_Avoid_: CSS vocabulary, free-form layout

**Renderer**:
The authority that faithfully realizes a valid Presentation Plan without making new editorial or
presentation judgments. It may deterministically generate non-semantic UI chrome such as numbering,
source labels, and step labels.
_Avoid_: Designer, critic

## Observation and repair

**Browser Observation**:
Structured evidence collected from the actual rendered report's browser DOM and screenshots during
the run, distinct from either source meaning or subjective Owner acceptance.
_Avoid_: Screenshot review, visual opinion

**Browser Observer**:
The narrow deterministic runtime sensor that produces Browser Observations from the actually
rendered Candidate Report.
_Avoid_: Visual Critic, browser reviewer

**Defect**:
A rule-defined problem that affects report credibility, readability, or legal delivery and is
classified only as blocking or non-blocking. Pure aesthetic opportunity is not a Defect.
_Avoid_: Preference, polish suggestion, open-ended improvement

**Semantic Revision**:
One budgeted, source-grounded replacement of semantic artifacts that may correct existing Claims or
Editorial Content Units or add omitted content with explicit Canonical Transcript evidence, while
leaving the Canonical Transcript unchanged.
_Avoid_: Semantic Patch, transcript correction, unrestricted rewrite

**Presentation Revision**:
One budgeted replacement of a Presentation Plan for a related set of presentation Defects without
changing its Editorial content.
_Avoid_: Presentation Patch, CSS edit, unrestricted redesign

**Revision Budget**:
The run-wide allowance of no more than two revision attempts, of which no more than one may be a
Semantic Revision; both attempts may instead be Presentation Revisions.
_Avoid_: Retry count, optimization loop
