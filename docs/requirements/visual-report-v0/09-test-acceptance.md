# Video Visual Report V0 — Test and Acceptance

## Current-grade release and next-grade promotion evidence

V0 implementation evidence consists of passing targeted/full repository checks,
a successful offline render, final desktop/mobile screenshots, source/rights
review, and the owner visual decision. Automated checks may move the task only to
`READY_FOR_OWNER_VISUAL_REVIEW`. V1 requires a separate owner authorization even
after V0 acceptance.

## Test strategy and environments

| Level | Applicable | Command/environment | Evidence |
|---|---|---|---|
| Unit | Yes | `uv run pytest -q` with targeted renderer tests | Models/components/path/escaping tests |
| Contract | Yes | Pydantic valid/invalid fixtures | Closed union and cross-ref results |
| Integration | Yes | Required module render command | Real RLinf HTML exists and exit is 0 |
| Failure | Yes | Malformed plan, unknown block/asset, unsafe/missing path, invalid time | Stable non-zero errors |
| Recovery | Yes | Valid output followed by induced failed rerender | Prior HTML remains complete |
| Security | Yes | Hostile text, network URL, traversal fixtures | Inert text and rejected paths |
| Performance/load | Bounded | Time one real render; concurrency 1 | ≤5 s target; >10 s defect trigger |
| Replay | Yes | Render same input twice | Equivalent HTML |
| Regression | Yes | `uv run ruff check .`, `uv run pytest -q`, `git diff --check` | Existing P0 paths remain green |
| Visual | Yes | Local browser at 1080 px and about 390 px | Full-page screenshots and review notes |

## Acceptance cases

| ID | Given | When | Then | Linked requirements |
|---|---|---|---|---|
| `ACC-VR0-001` | Valid versioned plan/assets | Required CLI runs | Exit 0 writes a complete canonical HTML and prints counts/path | `REQ-VR0-001`, `005` |
| `ACC-VR0-002` | Minimal fixture for every content type | Components render | Each maps to its fixed semantic component; Hero/Section Header are structural | `REQ-VR0-002`, `004` |
| `ACC-VR0-003` | Unknown type or style/layout primitive | Input validates | It is rejected; no generic/free-layout fallback | `REQ-VR0-002`, `004`, `008` |
| `ACC-VR0-004` | Valid reused optional asset and required image asset | Render runs | Assets resolve by ID and can be reused; image block requires one | `REQ-VR0-003` |
| `ACC-VR0-005` | Unknown/duplicate asset or escaping/remote path | Render runs | Non-zero error names the problem and no false success occurs | `REQ-VR0-003`, `008`, `011` |
| `ACC-VR0-006` | Authored text contains script/HTML syntax | HTML renders | Syntax is visible inert text; no script executes | `REQ-VR0-008` |
| `ACC-VR0-007` | Factual blocks in the real plan | Plan validates/renders | 100% contain in-range timestamped source refs; text blocks show compact source times, while image blocks show only their asset timestamp and retain refs in data attributes | `REQ-VR0-007` |
| `ACC-VR0-008` | Final RLinf inputs | HTML renders | Hero, 3–5 modules, relationship/process, 2–4 useful frames, and takeaways are present | `REQ-VR0-006` |
| `ACC-VR0-009` | Final report at 1080 px | Owner/implementer inspects | Dense, readable Chinese editorial hierarchy; semantic numbered sections; compact small-radius components; self-explanatory evidence frames; no overflow/clipping | `REQ-VR0-009`, `010`, `013` |
| `ACC-VR0-010` | Same final report at about 390 px | Browser inspects | Single-column adaptation, stacked comparisons/vertical process, no horizontal overflow | `REQ-VR0-010`, `013` |
| `ACC-VR0-011` | Final page loads with browser network inspection | Page opens | Zero automatic external requests; local images load | `REQ-VR0-005`, `011` |
| `ACC-VR0-012` | RLinf source use basis | Final report inspected | Required attribution/local notice is visible; no publish/deploy path added | `REQ-VR0-011` |
| `ACC-VR0-013` | A valid prior HTML and invalid new input | Rerender is attempted | Command fails and prior valid HTML remains unchanged/complete | `REQ-VR0-008` |
| `ACC-VR0-014` | Same valid inputs and revision | Render runs twice | HTML is equivalent and contains no run-time/random drift | `REQ-VR0-004` |
| `ACC-VR0-015` | Final artifact and transcript/Markdown baseline | Owner reads for 60–90 seconds | Owner recovers thesis, progression, central relationship, takeaways and prefers report for review | `REQ-VR0-006`, `009`, `014` |
| `ACC-VR0-016` | Implementation checks pass | Session concludes | Task/status stop at owner visual review; no V1 work begins | `REQ-VR0-014` |
| `ACC-VR0-017` | Final code diff | Protected scope is reviewed | No frozen P0-B artifact/contract/retrieval/eval change | `REQ-VR0-012` |

## Contract and permission tests

- Parse one valid top-level plan and asset manifest.
- Exercise all seven discriminants and structural Hero/section data.
- Reject missing required fields, extra layout/style fields, unsupported versions,
  duplicate section/block/asset IDs, and empty required collections.
- Permit optional asset absence on non-image blocks; require it on `image_caption`.
- Reject publication/network asset behavior by contract and scope review.

## Input validation, limits, duplicates, order, authorization, and invalid-input tests

Test malformed UTF-8/JSON, negative or reversed timestamps, end beyond
`duration_ms`, blank strings, over-budget lists/copy once calibrated, unknown
segment/asset IDs where cross-checkable, absolute/URL/escaping asset paths, and
missing files. Confirm plan array order exactly determines rendered narrative
order. Filesystem denial produces an I/O error, not a success.

## Output schema, completeness, partial/degraded, evidence, uncertainty, lifecycle, and side-effect tests

Parse generated HTML enough to verify title/language/meta viewport, ordered
sections, expected component markers, escaped content, visible source times,
attribution, local stylesheet/assets, and absence of remote `src`/`href` loads.
There is no successful partial output. Optional image absence on a compatible
text block is a normal complete render; required image absence is failure.

## Migration, retention, deletion, backup, and restore tests

No migration or service backup tests. Confirm the V0 artifact root is self-bounded
for owner deletion and that rendering does not write into frozen P0-B paths.
Recovery is deterministic regeneration from retained inputs.

## Source rights, authority, schema, coverage/quality, lineage, conflict, poisoning, freshness, outage, and correction tests

- Check report attribution against `eval/p0b/corpus.jsonl`.
- Check all source ranges against the fixed video duration.
- Manually review each used frame and factual/numeric claim.
- Treat plan text as untrusted and confirm escaping/path controls.
- After a correction, rerender and replace both screenshots before review.
- If source/manifest is unavailable or conflicts, stop rather than fetch/guess.

## State, stale approval, late result, partial/degraded, and recovery tests

Artifact existence does not update status. A changed plan/renderer makes earlier
screenshots and any earlier owner acceptance stale until the owner reviews the
new output. No background result exists. Failed or cancelled render cannot
advance state or overwrite a good artifact with a partial file.

## Consent withdrawal and protected-record tests

No user-consent system. Scope review confirms a documented response to source-use
withdrawal and no mutation of frozen P0-B evidence.

## Accessibility, compatibility, performance, load, and fault tests

- Inspect semantic heading order, landmarks, alt text, contrast, focus state, and
  reduced-motion CSS.
- Capture full-page screenshots at 1080 px and about 390 px.
- Include long Chinese copy and long Latin identifiers in an overflow fixture.
- Record fixed-fixture render time; no concurrency/spike/soak infrastructure.
- Induce missing file and output write failure.

## Security and abuse tests

Use payloads containing `<script>`, event-handler-like text, ampersands, quotes,
`javascript:`/`https:` asset paths, absolute paths, and `../` traversal. Confirm
the output has no executable injection and invalid asset paths are rejected.

## Agent evaluation and regression policy

Not applicable because V0 runtime has no Agent/model. Do not reuse P0-B Agent,
retrieval, or Evidence Gate evaluation as visual-quality evidence.

## AI baseline, grounding, uncertainty/abstention, drift, promotion, rollback, and slice tests

The non-AI baseline is transcript/Markdown. Grounding is reviewed via source refs.
Ambiguous metrics are omitted. There is no model drift test. Promotion is the
owner's visual decision followed by separate V1 authorization.

## Deterministic-gate, safety-interrupt, and multi-agent failure tests

Schema/path/escaping gates are covered above. Ctrl-C and failed output replacement
are checked proportionally. Multi-agent product behavior is not applicable.

## Offline successful and failure/recovery replay fixtures

Keep compact test fixtures in `tests/` for every component and invalid category.
The real report plan/assets under `artifacts/` are the local integration fixture
and must not be published or assumed available in CI.

## Spike, soak, degradation, restore, incident/support, customer lifecycle, compatibility, and deprecation evidence

Not applicable beyond the bounded single-render timing and recovery tests. V0 is
not a service and creates no commercial/production claim.

## Test data and privacy

Unit fixtures use synthetic Chinese technical content and tiny local placeholder
images. Only the local integration/report uses the RLinf media-derived frames.
Never commit or upload rights-restricted media just to make CI self-contained.

## Traceability

| Goal | Scenario | Requirement/NFR | Component/interface | Test | Operational signal |
|---|---|---|---|---|---|
| `GOAL-VR0-001` | `SCN-VR0-001` | `REQ-VR0-006`, `009`, `013` | HTML/browser | `ACC-VR0-008`, `009`, `015` | Owner visual decision |
| `GOAL-VR0-002` | `SCN-VR0-001`, `004` | `REQ-VR0-006`, `007` | Plan/source refs | `ACC-VR0-007`, `008`, `015` | Content review |
| `GOAL-VR0-003` | `SCN-VR0-002` | `REQ-VR0-001`–`005`, `008` | Models/components/CLI | `ACC-VR0-001`–`006`, `013`, `014` | Tests/render exit |
| `GOAL-VR0-004` | `SCN-VR0-003` | `REQ-VR0-009`, `010`, `013` | CSS/SVG/browser | `ACC-VR0-009`, `010`, `011` | Screenshots/network check |
| `GOAL-VR0-005` | `SCN-VR0-004` | `REQ-VR0-007`, `011`, `012` | Source/asset metadata | `ACC-VR0-007`, `012`, `017` | Attribution/diff review |

## Release acceptance owner and evidence

The repository owner is the only V0 visual acceptance authority. The
implementation session supplies:

1. required command output and elapsed time;
2. Ruff/pytest/diff-check results;
3. desktop/mobile screenshots from the final HTML;
4. content/source/rights review notes;
5. changed-file list and residual issues;
6. status set to `READY_FOR_OWNER_VISUAL_REVIEW`.

The owner then accepts or requests iteration. Passing automated checks alone is
not a product-quality conclusion.

## Commercial go-live sign-off

| Area | Owner | Required evidence | Status |
|---|---|---|---|
| Product prototype | Owner | Final HTML, screenshots, comparison rubric | Pending owner review after implementation |
| Data/source | Owner/implementer | Attribution, local-only compliance, source refs | Required for V0 review |
| AI quality | None | Runtime AI absent | Not applicable |
| Security/privacy | Implementer | Escaping/path/offline tests | Required for V0 review |
| Performance/reliability | Implementer | One-run timing and recovery tests | Required for V0 review |
| Operations/support/legal/business | Owner | No service/public release claim | Not applicable to G1 |
