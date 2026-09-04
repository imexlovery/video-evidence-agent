# Agent and Intelligent Behavior

## Intelligence target

V1.2 must improve the report-making behavior that a generic coding agent demonstrates informally:
understand source meaning, select and organize useful content, choose a coherent visual expression,
look at the actual page, and repair material defects. Its product differentiation is not “another
Prompt”; it is a typed, evidence-retaining, browser-observed, finite Harness with explicit semantic
authority.

Model count, agent count, and framework adoption are not quality metrics. The target is a better
worst-run quality floor and lower cross-run variance while preserving source truth.

## Autonomy level

The product is `A1 assistive`: it drafts a local report for the Owner to inspect. Internal bounded
Revision is automatic, but the system performs no external, destructive, privileged, financial, or
public action. The Owner remains responsible for accepting, exporting, publishing, or deleting any
result. A run status is never Owner approval.

## Harness behavior

The Harness fixes capability order and explicit inputs. The same configured model may act through
different roles, but no role receives general control of the workflow.

| Capability | Authorized judgment | Required output boundary |
|---|---|---|
| Claim construction | atomic source-backed propositions and evidence selection | Claim Graph |
| Editorial construction | final wording, focus, chapter order, semantic relationships | Editorial Plan |
| Semantic review | grounding, omissions, uncertainty, authority Defects | review evidence/Defects |
| Presentation construction | legal visual expression of existing semantics | Presentation Plan |
| Visual review | defects visible in real render and recommended layer | review evidence/Defects |
| Revision | regenerate one authorized layer's typed Artifact | replacement Artifact |

These capabilities may be combined into fewer calls when calibration shows equal or better quality.
They do not become independent agents, permanent services, or autonomous product states by default.

## Prompt and context contract

Every model call MUST:

- identify one capability and its authority;
- include only explicit, versioned authorized Artifacts;
- state that transcript, asset metadata, and report content are data rather than instructions;
- request one typed response Schema;
- prohibit unsupported knowledge, transcript correction, tool use, workflow continuation, and
  output outside the role's authority;
- record Prompt version and input snapshot identity;
- use the one run-level Provider and model configuration.

The model has no implicit chat memory between roles. If a fact or decision is not in the authorized
Artifact snapshot, the model cannot rely on it.

## Grounding rules

1. A Claim is legal only as `STATED` or source-supported `SYNTHESIS`.
2. Every Claim references one or more actual Canonical Transcript units.
3. Every substantive Editorial Content Unit references one or more Claims.
4. The model may compress and synthesize but may not add outside facts, “correct” source wording, or
   conceal uncertainty.
5. `UNRESOLVED` evidence cannot independently support a key conclusion.
6. When the core meaning cannot be stated safely, abstention is run failure rather than invention.

Deterministic validation proves reference closure; semantic review assesses entailment and omission.
Neither alone substitutes for the other.

## Editorial behavior

Editorial optimizes for the fixed Objective. It chooses what matters, not a fixed number of sections
or blocks. It may express a comparison, process, sequence, or grouping only when that meaning is
supported by Claims; it then owns that relationship explicitly. It produces final wording rather
than notes that Presentation must rewrite.

Editorial SHOULD omit weak, repetitive, or nonessential material. It MUST retain important
limitations and enough reasoning/evidence for an unseen reader to understand the conclusion.

## Presentation behavior

Presentation composes a report from one Design System and the active controlled Vocabulary. It may
choose hierarchy, density, emphasis, spatial grouping, component, and image weight. It cannot repair
content by silently rewriting, inventing labels with semantic force, or creating a visual relation
that implies a comparison or causal sequence absent from Editorial.

When the source provides no useful asset, Presentation creates a complete text-only report. When
assets exist, relevance and readability outrank using every image.

## Review and Defect behavior

Review is bounded by explicit rules. A reported Defect must include observed evidence and explain
its impact on credibility, readability, or legal delivery. It is only `BLOCKING` or `NON_BLOCKING`.
Preference, novelty, beauty, and “could be improved” are not Defects.

Semantic review occurs before Presentation. Visual review consumes the actual screenshot and DOM
Observation after rendering. Visual review may recommend Semantic escalation but has no permission
to edit Editorial content.

## Revision policy

The Controller, not the model, applies this algorithm:

```text
if no material Defect:
    finish according to hard gates
elif no legal Revision budget remains:
    finish DEGRADED or FAILED according to blocking status
elif Defect is presentation-layer:
    authorize one Presentation Revision
elif Defect is editorial root cause and Presentation cannot reasonably solve it
     and the Semantic allowance remains:
    authorize one Semantic Revision
else:
    finish DEGRADED or FAILED according to blocking status
```

Authorization immediately consumes one of two run-wide Revision units. Semantic use is capped at
one. A Revision handles one related same-layer Defect set and returns a complete replacement typed
Artifact; no Patch DSL is exposed.

After Semantic Revision, downstream Presentation, Render, Observation, and visual review always run
again. After Presentation Revision, Render, Observation, and visual review always run again.

## Retry and invalid-output behavior

The run has one shared identical model retry, usable only when an eligible transient failure prevents
any complete response for the failed logical call. After it is spent, later calls cannot retry. A
complete response is retained even when parsing or validation fails. The Harness never silently
asks for another sample, switches model/provider, repairs JSON semantically, or substitutes a
manually authored Artifact inside the run.

A Reviser response that is invalid or exceeds authority consumes its already-authorized budget.
The Controller then uses current blocking status and remaining budget; the model does not negotiate
an exception.

## Tool and browser permissions

The model has no general tool interface. It cannot execute shell commands, inspect arbitrary files,
navigate the browser, click, follow links, mutate the DOM, invoke the Renderer, or write output
directly. Deterministic stages expose only typed Artifacts. The screenshot and Observation are model
inputs for visual review, not browser-control permission.

## Multi-agent and partial failure

V1.2 has one model configuration and one Controller. Role labels are scoped calls, not cooperating
agents. There is no delegation, message bus, consensus, shared agent memory, or partial-agent result
merging. A failed mandatory capability follows the single run's failure and Revision rules.

## Fallback and escalation

- No legacy runtime fallback.
- No alternate Provider or model fallback.
- No transcript truncation/chunk fallback.
- No manual hidden Artifact substitution.
- Source-critical uncertainty escalates to `FAILED`.
- A non-blocking local omission may yield `DEGRADED`.
- Product acceptance and default promotion escalate to the Owner after evidence; they are outside
  runtime autonomy.

## Unacceptable intelligent behavior

- unsupported Claim or reader-facing content;
- Presentation-authored semantics;
- key conclusion based only on `UNRESOLVED` evidence;
- transcript correction or external-knowledge completion;
- model-authored HTML/CSS/color/coordinates/executable content;
- aesthetic-only Revision;
- hidden resampling, selective rerun, or best-of-N selection;
- use of stale Presentation/Observation after Semantic Revision;
- continuation past budget;
- reporting `COMPLETE` without real 1080px Observation;
- implying Owner acceptance or publication readiness.
