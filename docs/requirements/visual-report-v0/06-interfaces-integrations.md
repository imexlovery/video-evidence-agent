# Video Visual Report V0 — Interfaces and Integrations

## Surface inventory

| Surface | Consumer | Purpose | Contract ID |
|---|---|---|---|
| Local JSON files | Content/asset author and renderer | Declare semantic report content and selected assets | `IN-REPORT-PLAN`, `IN-ASSETS` |
| Python module CLI | Implementer | Validate and render one report | `CLI-VR0-RENDER` |
| Offline `report.html` | Owner/learner | Read, inspect, and decide save value | `OUT-REPORT-HTML` |
| Local browser screenshots | Owner | Review desktop/mobile visual quality | `OUT-VISUAL-CHECK` |

## Existing brand and creative assets

| Asset ID/status | Asset | Source/editable location and access | Formats/versions/variants | Rights/license/change limits | Localization/accessibility | Reuse/create/delivery decision | Approval owner |
|---|---|---|---|---|---|---|---|
| `REF-TUGEKUAI / REFERENCE_ONLY` | Example long visual summary | `/Users/tristana/Desktop/"图个快"效果图.png` | One 844×3753 PNG | Visual reference only; do not distribute or copy directly | Chinese reference; accessibility unknown | Extract principles only: hierarchy, density, sectional rhythm | Owner |
| `MEDIA-RLINF / LOCAL_ONLY` | Technical talk source | Fixed P0-B local MP4 | 16:9 video | No explicit open license; no publication/redistribution | Chinese; frame alt text required | Create 2–4 local frames and preserve attribution | Owner |
| `VISUAL-VR0 / TO_CREATE` | Original report design system | Renderer source | One theme, responsive CSS | Project-owned implementation; cannot broaden source-media rights | Chinese-first; semantic structure, alt text, contrast, responsive | Create original design | Owner visual gate |

## Canonical input/output to transport mapping

| IN/OUT ID | Surface/transport | Envelope/serialization | Auth | Limits | Delivery/error behavior |
|---|---|---|---|---|---|
| `IN-REPORT-PLAN` | Filesystem argument | UTF-8 JSON | Local filesystem | Supported V0 version; bounded component content | Full validation before rendering; non-zero error |
| `IN-ASSETS` | Filesystem argument | UTF-8 JSON + relative JPEG paths | Local filesystem | 2–4 used frames; contained local paths | Missing/unsafe ref fails |
| `OUT-REPORT-HTML` | Filesystem output | UTF-8 HTML/CSS/inline SVG with relative local image refs | Local filesystem | One natural-height page | Successful atomic replacement; concise stdout |
| `OUT-RENDER-ERROR` | Process stderr/exit | Stable category + context | Not applicable | No secret/media dump | Non-zero; no automatic retry |

## User interface contract

The report is an editorial document, not an application dashboard.

- **Page frame:** centered 1080 px desktop design canvas with about 96 px gutters;
  natural height; cool canvas around white editorial surfaces.
- **Hero:** source/category eyebrow, display title, one-sentence thesis, duration/
  speaker/source context. It must establish the argument rather than show generic
  KPIs.
- **Editorial density:** use a compact Chinese visual-article rhythm inspired by
  the reference's hierarchy and density, without copying its artwork. Remove
  reading instructions, decorative English labels, oversized poster spacing,
  and any side rail that competes with the summary itself.
- **Sections:** 3–5 numbered modules in a deliberate narrative order. Each
  section timestamp marks a verified semantic topic boundary, never a uniform
  interval or candidate-frame sampling time.
- **Components:** colored boxes are reserved for meaningful contrast, process,
  bullets, metrics, or takeaways; they use restrained small corner radii. Bullet
  groups use small round dots, not outlined squares.
- **Evidence frames:** 16:9 presentation content, useful alt text, one
  bottom-right timestamp chip from the asset timestamp, no visible caption/source
  trace below the image, no decorative blur, and no arbitrary crop.
- **Footer:** attribution, local prototype/use notice, and report/video metadata.
- **Responsive:** at about 390 px, one column; comparisons stack; process becomes
  vertical; metric groups wrap; no horizontal overflow.
- **Accessibility:** semantic headings in order, readable contrast, images have
  `alt`, decorative SVG is hidden from assistive technology, meaningful SVG has
  a label/title, focus styles exist for any link, and reduced-motion preferences
  are respected. Motion is unnecessary in V0.
- **Network:** page load performs zero external request. A displayed source URL
  must not auto-fetch previews, scripts, fonts, or media.

## API contract

Not applicable. V0 exposes no HTTP API, server, socket, or remote endpoint.

## CLI contract

```bash
uv run python -m video_evidence_agent.visual_report render \
  --plan artifacts/visual-report/v0-rlinf/report-plan.json \
  --assets artifacts/visual-report/v0-rlinf/assets.json \
  --output artifacts/visual-report/v0-rlinf/report.html
```

Required behavior:

- `render` is the only V0 subcommand.
- All three path arguments are required.
- Paths are resolved explicitly; the asset resolver still enforces its own
  contained relative-path contract.
- Exit `0` only after writing a complete HTML file.
- Success output includes report ID, section/block/used-asset counts, and output
  path; it does not dump report content.
- Contract or I/O failures exit non-zero with the stable error taxonomy.
- No provider, credential, environment secret, or network access is required.

## Background and event contract

Not applicable. There is no background work, webhook, queue, event schema,
notification, or callback.

## Canonical statuses and external mappings

There is no external mapping. Project status uses the vocabulary in
`03-functional-spec.md` and is owned by `docs/visual-report/V0-STATUS.md`.

## Agent tool or MCP contract

Not applicable. The product runtime is not an Agent and exposes no tools/MCP.
Codex/browser/FFmpeg usage during implementation is development tooling only.

## Library or SDK contract

The renderer may expose project-internal Python functions for tests, but V0 does
not promise a public library API or compatibility beyond the versioned JSON
fixtures and required CLI command.

## External integrations

| System | Owner | Purpose | Credentials/scopes | Limits | Outage behavior |
|---|---|---|---|---|---|
| FFmpeg/ffprobe on PATH | Local owner | Extract/inspect candidate frames during implementation | None | Development-time local media only | Stop and report missing binary; do not download a substitute |
| Local browser | Local owner | Render and capture review screenshots | None | No external requests | Use another installed local browser only if it preserves viewport evidence |
| Python/uv environment | Repository | Run renderer/tests | None | Existing Python 3.12 project | Repair only within established uv workflow |

Bilibili is provenance, not an integration. V0 does not fetch the URL.

## Errors, timeouts, retry, idempotency, and reconciliation

All errors use the functional-spec taxonomy. Rendering has no automatic retry.
The same valid inputs are safe to rerun and replace the same output. Ten seconds
on the fixed fixture triggers investigation rather than timeout machinery.
Reconciliation means validate current plan/assets and rerender; hand-edited HTML
is never merged back.

## Contract snapshots, drift detection, and compatibility

Tests hold minimal fixtures for every block and invalid path/reference cases.
`schema_version` rejects unsupported changes. The V0 schema is deliberately
provisional; breaking changes are permitted within this prototype only when the
real report demonstrates the need, tests/fixtures/docs update together, and the
status remains before owner acceptance.

## Contract examples

Canonical examples are in [Functional specification](03-functional-spec.md).
The real implementation fixture resides under
`artifacts/visual-report/v0-rlinf/` and must remain local.
