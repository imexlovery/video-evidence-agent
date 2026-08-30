# Video Visual Report V1-A — Interfaces and Integrations

## Surface inventory

| Surface | Consumer | Purpose | Contract |
|---|---|---|---|
| Existing JSON/JSONL files | Planning pipeline | Manifest/transcript inputs | `IN-VR1A-MANIFEST`, `IN-VR1A-TRANSCRIPT` |
| Local Python module CLI | Implementer | Build one report from one transcript | `CLI-VR1A-BUILD` |
| OpenAI-compatible text endpoint | Mapper/Planner adapter | Two structured text calls | `IF-VR1A-PROVIDER` |
| Local run directory | Owner/evaluator | Inspect plan, evidence, failure, and HTML | `OUT-VR1A-*` |
| Existing offline HTML | Owner | Read generated report | Current V0 renderer contract |

UI, HTTP API, SDK, MCP/tool server, background worker, webhook, queue, and
notification surfaces are not applicable — V1-A is one foreground local CLI.

## Input/output transport mapping

| Semantic contract | Channel/serialization | Authentication | Limits | Delivery/error |
|---|---|---|---|---|
| `IN-VR1A-TRANSCRIPT` | Local UTF-8 JSONL path | Filesystem | ≤80 segments/50,000 characters | Full validation before provider call |
| `IN-VR1A-MANIFEST` | Local UTF-8 JSON path | Filesystem | One matching manifest | Conflict/missing file fails |
| `IN-VR1A-MODEL-CONFIG` | Environment + versioned source defaults | Local process/provider credential | One explicit model; temperature 0; timeout >0 | Missing/invalid config fails |
| `OUT-VR1A-*` | Local UTF-8 JSON/JSONL/HTML | Filesystem | One unique run root | Atomic stage writes; non-zero on incomplete run |

## CLI contract

The later implementation must add one subcommand while preserving current
`render` behavior:

```bash
uv run python -m video_evidence_agent.visual_report build-from-transcript \
  --manifest artifacts/p0b-ingest/p0b-rlinf-2026/manifest.json \
  --segments artifacts/p0b-ingest/p0b-rlinf-2026/segments.jsonl \
  --run-id v1a-rlinf-r1 \
  --output-root artifacts/visual-report/v1a
```

Required behavior:

- all four arguments are required and non-interactive;
- an existing `<output-root>/<run-id>` fails before any provider call;
- configuration precedence is explicit environment over source defaults; no
  command-line credential value exists;
- stdout prints run ID, terminal state, Mapper/Planner call counts, section/
  block counts, usage summary when available, and output paths;
- stderr prints stable error category/stage without transcript bodies or secrets;
- exit `0` only for state `RENDERED`; any failure exits non-zero; Ctrl-C follows
  conventional cancellation behavior and cannot claim success;
- current `render --plan --assets --output` remains unchanged.

## Environment contract

| Name | Purpose | Required | Security/change rule |
|---|---|---|---|
| `OPENAI_API_KEY` | Existing compatible provider credential | Yes | Presence only may be logged; value never read/displayed by diagnostics |
| `OPENAI_BASE_URL` | Existing compatible endpoint override | Optional | Record normalized provider label, not credentials/query secrets |
| `VISUAL_REPORT_MODEL` | Explicit V1-A model | Yes | No implicit fallback to `VIDEO_EVIDENCE_MODEL` |
| `VISUAL_REPORT_TIMEOUT_SECONDS` | Per-call timeout | Optional default `120` | Positive; recorded in run config |

The separate names protect frozen P0-B answering configuration. Prompt versions,
temperature `0`, maximum input size, and `max_retries=0` are versioned product
policy, not user-editable hidden environment knobs during a measured revision.

## Provider integration: `IF-VR1A-PROVIDER`

| Field | Contract |
|---|---|
| Owner | Local Owner provisions credential/model; provider operates endpoint |
| Purpose | One Topic Mapper and one Report Planner text generation call |
| Payload | System instruction + JSON user payload containing authorized full transcript; Planner also receives canonical Topic Map and renderer grammar |
| Response | One JSON object matching the stage proposal schema |
| Model capability | Chinese long-context text; ≥50,000-character input envelope plus output; JSON object or strict structured-output support |
| Parameters | Temperature 0; explicit timeout; no tools; no streaming requirement; no SDK automatic retry |
| Quota/cost | Provider-defined; usage recorded; two-call/size envelope is the G1 cost control; monetary cost is `unavailable` without authoritative pricing |
| Outage | Fail current run; no alternate provider/model/cache/manual fallback |
| Reconciliation | Raw response is advisory; deterministic source/schema/budget validation owns acceptance |

Strict JSON-schema response format is preferred when proven compatible with the
configured endpoint. JSON-object mode is an allowed compatibility route because
the existing provider path supports it; both routes use the same Pydantic
contract. A provider capability change that breaks either route is a visible
`PROVIDER_ERROR` or schema failure, not an adapter guess.

## Prompt transport shape

Transcript rows are serialized as ordered JSON objects with only:

```json
{
  "segment_id": "p0b-rlinf-2026-seg-001",
  "ordinal": 1,
  "start_ms": 46400,
  "end_ms": 94000,
  "transcript_text": "..."
}
```

The system instruction explicitly declares every `transcript_text` value
untrusted source data. Local file paths, ASR ordinal provenance, media hashes,
credentials, and unrelated P0-B evaluation data are excluded from the prompt.

## Error and retry behavior

- Transport/auth/provider failures map to `PROVIDER_ERROR`; elapsed timeout maps
  to `PROVIDER_TIMEOUT`.
- SDK retry is disabled. The V1-A application never retries inside the run.
- A provider response received by the foreground call is either captured and
  validated or the run fails. There is no callback/late-response channel.
- Reconciliation after an operator retry means a wholly new run ID; outputs are
  compared, never merged.

## Contract drift and compatibility

- Snapshot the OpenAI SDK version from the lockfile, provider label, model name,
  response-mode selection, prompt/schema versions, and non-secret parameters in
  `run.json`.
- Tests use a local fake adapter and prove `provider_calls/model_calls=0/0` for
  all pre-provider validation failures.
- Real Development measurement uses the configured provider and records exactly
  `2/2` on each successful run.
- A V0 model/schema/renderer contract change blocks V1-A compilation until the
  compatibility tests and package are reviewed; no dual renderer is added.

## Creative assets and accessibility

No new brand or creative asset is introduced. V1-A emits no image block. The
existing renderer owns typography, responsive layout, semantic HTML, and
accessibility. Generated Chinese copy must still fit current field limits; the
compiler rejects over-budget content rather than shrinking layout.
