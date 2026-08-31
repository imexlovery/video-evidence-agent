# Video Visual Report V1-A — Interfaces and Integrations

## Surface inventory

| Surface | Consumer | Purpose | Contract |
|---|---|---|---|
| Existing JSON/JSONL files | Planning pipeline | Manifest/transcript inputs | `IN-VR1A-MANIFEST`, `IN-VR1A-TRANSCRIPT` |
| Local Python module CLI | Implementer | Build one report from one transcript | `CLI-VR1A-BUILD` |
| Existing DeepSeek OpenAI-compatible endpoint | Mapper/Planner adapter | Two semantic JSON calls | `IF-VR1A-PROVIDER` |
| Local run directory | Owner/evaluator | Inspect plan, evidence, failure, and HTML | `OUT-VR1A-*` |
| Existing offline HTML | Owner | Read generated report | Current V0 renderer contract |

UI, HTTP API, SDK, MCP/tool server, background worker, webhook, queue, and
notification surfaces are not applicable — V1-A is one foreground local CLI.

## Input/output transport mapping

| Semantic contract | Channel/serialization | Authentication | Limits | Delivery/error |
|---|---|---|---|---|
| `IN-VR1A-TRANSCRIPT` | Local UTF-8 JSONL path | Filesystem | ≤80 segments/50,000 characters | Full validation before provider call |
| `IN-VR1A-MANIFEST` | Local UTF-8 JSON path | Filesystem | One matching manifest | Conflict/missing file fails |
| `IN-VR1A-MODEL-CONFIG` | Environment + versioned source defaults | Local process/provider credential | One explicit model; Thinking enabled; reasoning effort high; `max_tokens=32768`; timeout >0 | Missing/invalid config or a request/snapshot mismatch fails |
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
| `OPENAI_API_KEY` | Existing SDK-compatible DeepSeek credential; the legacy variable name does not imply an OpenAI account/key | Yes | Presence only may be logged; value never read/displayed by diagnostics |
| `OPENAI_BASE_URL` | DeepSeek compatible endpoint override | Required by the current v2 frozen tuple | Record normalized provider label, not credentials/query secrets |
| `VISUAL_REPORT_MODEL` | Explicit V1-A model | Yes | No implicit fallback to `VIDEO_EVIDENCE_MODEL` |
| `VISUAL_REPORT_TIMEOUT_SECONDS` | Per-call timeout | Optional default `120` | Positive; recorded in run config |

The separate names protect frozen P0-B answering configuration. Prompt versions,
`thinking.type=enabled`, `reasoning_effort=high`, `max_tokens=32768`, maximum
input size, and SDK `max_retries=0` are versioned product policy. Temperature may
remain present for SDK compatibility and trace completeness, but Thinking mode
ignores it and no stability claim may depend on it. The project-owned single
technical retry is a separate explicit run rule, not a hidden SDK/environment
knob.

## Provider integration: `IF-VR1A-PROVIDER`

| Field | Contract |
|---|---|
| Owner | Local Owner provisions credential/model; provider operates endpoint |
| Purpose | One Topic Mapper and one Report Planner semantic stage, with at most one eligible technical retry across the run |
| Payload | System instruction + JSON user payload containing authorized full transcript; Planner also receives canonical Topic Map and renderer grammar |
| Response | One valid JSON object containing the stage's shallow semantic v2 proposal; project normalization owns canonical validity |
| Model capability | Chinese long-context text; ≥50,000-character input envelope plus output; current `deepseek-v4-flash-vision-exp` model used with text-only DeepSeek Chat Completions JSON Output |
| Parameters | `response_format={"type":"json_object"}`; JSON instruction/example; `extra_body={"thinking":{"type":"enabled"}}`; `reasoning_effort="high"`; `max_tokens=32768`; explicit timeout; no tools/streaming/SDK retry; project retry repeats one identical failed stage at most once per run; temperature is not stability evidence |
| Quota/cost | Provider-defined; usage recorded; two base calls/three maximum per run and nine maximum for the product set; monetary cost is `unavailable` without authoritative pricing |
| Outage | Eligible technical failure may spend the one identical retry; exhaustion is technical-inconclusive; no alternate provider/model/cache/manual fallback |
| Reconciliation | Raw response is advisory; deterministic source resolution/non-semantic compiler/V0 validation owns canonical acceptance and writes an ordered governance ledger |

`VR-V1A-PROVIDER-CONFORMANCE-004` historically required provider-side schema
conformance and closed at no-go. Its rules below are frozen evidence, not
current execution authority. The unexecuted official-OpenAI isolation proposal
is cancelled. Current task `VR-V1A-CONTRACT-SIMPLIFICATION-006` instead uses
DeepSeek JSON Output only as a valid-JSON envelope and applies the versioned v2
compiler contract locally. Empty or malformed JSON may use the single identical
technical retry and remains attempt-recorded; it is not semantic repair.

### Completed provider-conformance strategy contract

At most two materially distinct strategies may be declared. Each strategy
freezes provider, exact model/version, API surface, native schema mechanism,
submitted Mapper/Planner schema hashes, prompt-bundle hashes, reasoning/token/
timeout settings, SDK version, and adapter code snapshot before the first real
transcript call. Two prompt variants over the same model/API mechanism are not
two strategies.

Capability admission uses current official provider documentation or an
official capability/metadata response for the exact model/API. It sends no real
transcript and performs no uncounted generation. A schema projection may omit
only cross-field/semantic constraints that the provider mechanism cannot
express; it must preserve supported required fields, types, enums/
discriminators, `additionalProperties=false`, and list bounds. Existing-ID
membership, chronology, grounding, source entailment, and aggregate budgets
remain deterministic gates.

Historically, the strategy boundary was outside an individual run and was not provider
fallback: Strategy B may execute only after the complete predeclared Strategy A
three-video set fails, and only because both were frozen before Strategy A's
first transcript call. No strategy changes within a run or canary set.

### Current DeepSeek semantic-v2 product contract

Freeze `deepseek-v4-flash-vision-exp`, the Chat Completions JSON-object API
surface, `thinking.type=enabled`, `reasoning_effort=high`, `max_tokens=32768`,
one Mapper/Planner prompt bundle, v2 raw/canonical schema versions,
normalizer/compiler versions, source hashes, timeout settings, SDK version, and
all three product-run identities before the first call. GLM, Qwen, official
OpenAI, or a second DeepSeek model are not eligible fallbacks or comparison
arms. The trace must distinguish input, reasoning, visible-output, and total
tokens when supplied by the provider. The official DeepSeek JSON Output warning
about incomplete content maps to an eligible retained technical retry; retry
exhaustion remains technical-inconclusive rather than product-route No-Go.

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
- SDK retry is disabled. The V1-A application owns exactly one retry budget per
  run for connection/timeout/HTTP `429`/provider `5xx`, empty content,
  provider-declared incomplete output, or malformed non-decodable JSON.
- The retry repeats the identical current-stage request/configuration, records
  both attempt identities/raw outputs/usage/latency and may not add corrective
  instructions. No run retries both stages or exceeds three calls.
- Valid JSON with weak semantics, grounding errors, insufficient usable
  sections/units, unsupported claims, or V0 incompatibility is non-retryable.
- A provider response received by the foreground call is captured, parsed,
  normalized with evidence, and compiled, or the run fails. There is no
  callback/late-response channel.
- After the one technical retry, further execution requires a separately
  authorized new product-set revision; attempts and outputs are never merged.

## Contract drift and compatibility

- Snapshot the OpenAI SDK version from the lockfile, provider label, model name,
  response-mode selection, prompt/schema versions, and non-secret parameters in
  `run.json`.
- Tests use a local fake adapter and prove `provider_calls/model_calls=0/0` for
  all pre-provider validation failures.
- The product set uses the configured provider and records `2` base calls or
  `3` calls when the one eligible technical retry is spent.
- A V0 model/schema/renderer contract change blocks V1-A compilation until the
  compatibility tests and package are reviewed; no dual renderer is added.

## Creative assets and accessibility

No new brand or creative asset is introduced. V1-A emits no image block. The
existing renderer owns typography, responsive layout, semantic HTML, and
accessibility. Generated Chinese copy must already fit current field limits.
The v2 compiler may omit a whole unusable unit with evidence but may not clip,
rewrite, merge, or split semantic copy to force layout compliance.
