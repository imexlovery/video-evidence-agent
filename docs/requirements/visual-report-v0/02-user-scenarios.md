# Video Visual Report V0 — User Scenarios

## Actors

- **Owner/learner:** supplies the product direction, reads the local report, and
  alone decides whether it has save value.
- **Implementer:** turns fixed source content into the bounded plan, components,
  HTML, tests, and visual-review evidence.

## Primary end-to-end scenario

| Field | Detail |
|---|---|
| Scenario ID | `SCN-VR0-001` |
| Actor | Owner/learner, after implementer completion |
| Trigger | The owner wants to review the RLinf talk without watching all 34:53 or reading 46 transcript segments |
| Preconditions | Fixed local media/transcript exist; plan/assets pass validation; no external network is required |
| Producers and inputs | Implementer authors `report-plan.json`, extracts/selects 2–4 frames, and records `assets.json` |
| Decision-relevant sources | RLinf timestamped transcript, inspected source frames, manifest attribution and rights |
| Steps | Validate inputs → render deterministic components → open at 1080 px → inspect at 390 px → compare against transcript/Markdown → owner decides |
| Outputs/side effects and consumers | Local HTML and screenshots; no remote side effect; owner consumes the report |
| Feedback, storage, and deletion | Owner can request content/design iteration; all outputs remain under the local artifact root and may be deleted as one directory |
| Success evidence | Owner can explain the thesis, progression, central system relationship, and takeaways in 60–90 seconds and prefers the report for review |
| Postconditions | Status is either owner accepted or returned for bounded visual iteration; V1 remains separate |
| Linked goals | `GOAL-VR0-001` through `GOAL-VR0-005` |

## Alternate and role-specific scenarios

### `SCN-VR0-002` — Implementer renders after content editing

The implementer changes only structured copy/order/source refs, re-runs the same
command, and inspects the resulting HTML. No CSS or component layout is emitted
from the plan. The canonical output is replaced only after full validation.

### `SCN-VR0-003` — Owner returns visual feedback

The owner identifies a concrete content, hierarchy, density, image, or responsive
problem. The implementer changes the smallest relevant plan or renderer rule,
re-renders, refreshes screenshots, re-runs targeted tests, and preserves earlier
task evidence. The loop stays inside V0.

### `SCN-VR0-004` — Reader returns to source video

The reader uses the visible timestamp attached to a claim or frame to locate the
corresponding source moment. V0 need not implement a hosted deep link; a clear
`mm:ss`/`hh:mm:ss` label and retained source ref are sufficient.

## Failure and recovery scenarios

| ID | Situation | Expected behavior | Recovery | User-visible evidence |
|---|---|---|---|---|
| `FAIL-VR0-001` | Plan JSON is malformed or schema version unsupported | Exit non-zero before output success | Fix the plan; rerun | Field/path-specific error |
| `FAIL-VR0-002` | Unknown block type or duplicate block/section ID | Reject the plan; do not silently fallback | Correct discriminant/ID | Named invalid item |
| `FAIL-VR0-003` | Asset ID is missing, duplicated, unknown, or path escapes the artifact root | Reject render before referencing file | Correct manifest/path | Named asset and reason |
| `FAIL-VR0-004` | Source ref timestamp is outside video bounds or has reversed boundaries | Reject the factual block | Correct source ref | Block ID and invalid boundary |
| `FAIL-VR0-005` | Optional visual asset cannot be read | Fail the block/render rather than leave a broken image | Restore or remove the deliberate asset reference | Local path error |
| `FAIL-VR0-006` | Browser screenshot shows clipping, overflow, weak hierarchy, or illegible process labels | Implementation remains in visual iteration | Change deterministic component/design token and recheck both viewports | New screenshots and task note |
| `FAIL-VR0-007` | A numeric claim cannot be verified clearly | Omit or rewrite without the number | Return to transcript/frame | No unsupported metric in final HTML |
| `FAIL-VR0-008` | A command fails after a prior report existed | Preserve failure evidence; do not call the old file a new success | Fix and rerun full acceptance command | Task log distinguishes old artifact from new run |

## Empty, loading, validation, and permission states

- Empty sections, empty blocks, or no usable assets are invalid for the first
  report; the renderer gives a concise validation error.
- Rendering is synchronous and local, so there is no loading UI.
- There is no permission UI. Filesystem read/write failure is surfaced as a
  command error.

## Duplicate, cancellation, timeout, and partial-completion behavior

- IDs must be unique within their collection.
- Concurrent render coordination is outside V0; the task runs one render at a time.
- Ctrl-C cancellation may leave a temporary file, but must not replace a valid
  output with a partial HTML file; write then atomically replace where practical.
- A render that does not finish within ten seconds on the fixed local fixture is
  treated as an observed prototype defect and investigated; no automatic retry.

## Onboarding, administration, support, release/change, and offboarding

Onboarding is the required context read plus the one documented render command.
There is no administration or support system. Release is owner visual acceptance.
Offboarding/deletion is removal of `artifacts/visual-report/v0-rlinf/`; protected
P0-B source data remains untouched.

## Misuse and abuse scenarios

- A plan containing HTML/script must render as inert text, not executable markup.
- An asset path attempting `..`, an absolute path outside the bounded local
  fixture area, or a network URL is rejected.
- The implementation must not upload media, load CDN resources, track the reader,
  or publish the report.
