# P1 Interfaces and Integrations

## 1. Surface applicability

- CLI/library: applicable, local only. Exact command names may follow existing CLI conventions,
  but their observable contracts below are fixed.
- Agent Tools: applicable as project-owned in-process JSON contracts; not MCP/network services.
- UI/API/background worker/events/webhooks: Not applicable — excluded by G1 scope.
- New brand/creative assets: Not applicable — no visual surface; existing MP4 files remain
  `ASSET-P1-001` source data and cannot be edited.

## 2. CLI/library envelope

Later implementation must expose equivalent operations for: baseline freeze, headroom freeze/run,
offline verification, formal manifest freeze, B1/B2 run, grade/review/report. It may extend the
existing `video-evidence` CLI or a public Python module; it must not create a server.

- Input mapping: CLI JSONL/arguments must resolve to IN-P1-001/002/003 without redefining them.
- stdout: machine-readable success summary or artifact path; stderr: diagnostics without secrets.
- Stable exit classes: `0 success/gate terminal produced`, `2 invalid contract/config`,
  `3 no-go gate`, `4 authorization required`, `5 external/runtime failure`.
- Non-interactive: all formal values come from manifest; no hidden prompt during batch run.
- Config precedence and duplicate behavior follow `04-system-design.md`.

## 3. IF-P1-001 — `search_video`

Classification: read-only, deterministic executor, current video only, idempotent for same frozen
source/query but duplicate query in one run is rejected.

Input JSON schema:

```json
{"type":"object","additionalProperties":false,"required":["query"],"properties":{"query":{"type":"string","minLength":1,"maxLength":500}}}
```

Hidden trusted context: `run_id`, `video_id`, source hash, retrieval profile
`char_tfidf_2_4_query_views_v1`, `top_k=5`, remaining budget. Output fields: `status`, current
`video_id`, validated query, profile, `top_k=5`, and exactly up to five ordered hits containing score
and full authoritative `VideoSegment`. Empty hits are valid and lead to further bounded decision or
refusal. Errors: `INVALID_QUERY`, `DUPLICATE_QUERY`, `VIDEO_SCOPE_VIOLATION`,
`RETRIEVAL_UNAVAILABLE`, `TOOL_BUDGET_EXHAUSTED`.

The first invocation must use the exact original question after canonical normalization. No caller
or model may select Top-K, video, profile or source path.

## 4. IF-P1-002 — `inspect_segments`

Classification: read-only, deterministic executor, current video only.

Input JSON schema:

```json
{"type":"object","additionalProperties":false,"required":["anchor_segment_id","radius"],"properties":{"anchor_segment_id":{"type":"string","minLength":1},"radius":{"type":"integer","enum":[1,2]}}}
```

Anchor must already appear in a successful current-run observation. Runtime resolves its authority
by stable ID/ordinal; the model cannot send timestamps. Output fields: `status`, current `video_id`,
anchor, radius and ordered `segments` with relation `-2..2` and authoritative VideoSegment. At video
boundaries fewer than five is valid. Errors: `UNKNOWN_SEGMENT_ID`, `ANCHOR_NOT_OBSERVED`,
`VIDEO_SCOPE_VIOLATION`, `INVALID_RADIUS`, `SEGMENT_SOURCE_UNAVAILABLE`,
`TOOL_BUDGET_EXHAUSTED`. Same anchor/radius duplicate is rejected and radius never expands silently.

## 5. IF-P1-003 — text provider adapter

- Owner/purpose: Owner controls credential and authorizes answer/action generation for one formal
  revision; existing `openai` compatible adapter is the only allowed external integration.
- Credentials/scopes: `OPENAI_API_KEY` secret; `OPENAI_BASE_URL` and `VIDEO_EVIDENCE_MODEL`
  identifiers. Logs/manifests record credential presence boolean only.
- Contract: structured AgentAction or P0 AnswerProposal; exact schema/prompt/model/base URL snapshot
  frozen in ART-P1-003. No video upload, VLM, web search or provider tool execution.
- Quota/cost: call count is derived from frozen population and loop contract; explicit authorization
  sets ceilings. Runtime stops before exceeding them.
- Timeout/retry: one provider attempt per planned decision; no automatic formal retry. Timeout,
  malformed or outage preserves failure and blocks H4 for that revision.
- Drift: preflight compares provider/model/schema identifiers with manifest. Changed tool/schema/
  model capability requires a new manifest/revision; runtime never adapts silently.
- Reconciliation: local manifest/Trace is authoritative; provider usage metadata is observational.

## 6. Compatibility and versioning

IN/OUT/IF v1 contracts are frozen for the first P1 revision. Additive optional Trace fields may be
accepted only if old readers ignore them and hashes identify the version. Any change to Tool args,
Top-K, call budget, AnswerResult, terminal vocabulary or Gold rubric is breaking and requires Owner
checkpoint plus a new evaluation revision. P0 public contracts and commands must remain green.

