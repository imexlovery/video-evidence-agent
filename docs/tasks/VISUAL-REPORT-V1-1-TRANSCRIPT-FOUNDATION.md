# VR-V1.1-TRANSCRIPT-FOUNDATION-013 — Continuous Construction Task

Updated: 2026-09-01

## Task metadata

| Field | Value |
|---|---|
| Product version | `Visual Report V1.1` |
| Task ID | `VR-V1.1-TRANSCRIPT-FOUNDATION-013` |
| Target | Local Alpha Transcript Foundation |
| Task-card status | `READY_FOR_OWNER_V1.1_FREEZE_REVIEW` |
| Implementation status | `READY_FOR_OWNER_V1.1_FREEZE_REVIEW` |
| Execution style | One continuous final rework; no intermediate Owner gates |
| Required final stop | `READY_FOR_OWNER_V1.1_FREEZE_REVIEW` or one explicit hard blocker |
| Deployment | Excluded |

This card retains the completed A/B/C baseline and its evidence. The active
construction contract is the finite final rework below. The Owner explicitly
authorized that construction Goal on 2026-09-01; the implementation and final
downstream rerun are recorded in the evidence section below.

## Active construction contract — final bounded Fusion rework

### Current diagnosis and precedence

Full-video Explicit ROI coverage, Canonical regeneration, fresh semantic-v2,
and rendering have already been proven. Owner review then found that repeated,
correct OCR still fails to enter Canonical text reliably because frame evidence
is collapsed too early, time matching is too strict, and Fusion rejects useful
short multi-character replacements.

`献祭`, `星象房`, and `RLinf` are post-run probes only. They must not appear in a
dictionary, prompt, routing branch, fixture-only production rule, or
content-specific threshold.

This section is the only active construction scope and overrides conflicting
older text below:

- multi-frame consensus replaces Explicit ROI single-frame acceptance;
- final V1.1 Fusion is `replace`-only; prior OCR/subtitle insert/delete
  acceptance is not part of the final policy;
- the local match window is fixed to approximately ±1.5 seconds and the current
  ASR Unit plus at most one neighbor on each side;
- DeepSeek conflict arbitration is excluded; DeepSeek is used only by the
  unchanged fresh semantic-v2 downstream run;
- one complete fresh-video rerun replaces short-window or proposal-replay proof.

The original A/B/C sections and prior implementation evidence remain below as
history and baseline context. Do not repeat or redesign those completed slices.

### Change 1 — retain frame candidates and build simple consensus

Primary implementation surface:

- `src/video_evidence_agent/transcript_foundation.py`
- existing `_OcrSample`, `_merge_ocr_samples()`, and
  `extract_subtitle_ocr_events()` paths

Required behavior:

1. Keep each retained OCR sample after visual-change and duplicate filtering.
   Assign a deterministic candidate ID and retain timestamp, observed text,
   normalized text, confidence, ROI, and available frame/sample identity.
2. Write those rows to `subtitle-ocr-frame-candidates.jsonl` as a local debug and
   review artifact. This is not a new public Pydantic Schema or compatibility
   contract; do not retain cropped/full frame images as a product artifact.
3. For one temporally adjacent subtitle interval, compare 2–5 candidate texts
   with one simple similarity constant. A correction-eligible OCR consensus
   requires one uniquely supported winning cluster with at least two candidates.
4. Select the winning cluster's medoid or majority representative from an exact
   observed candidate string. Do not vote character by character, concatenate
   candidates, or invent text that no frame produced.
5. Put candidate IDs, representative candidate ID, support count, and observed
   variants into the existing free-form OCR event provenance. Do not add
   `consensus_version`, a public candidate model, or a new governance layer.
6. A tie, weak similarity, or one-frame result may remain inspectable evidence,
   but it is not eligible to correct ASR.

### Change 2 — bounded neighboring-Unit time matching

Primary implementation surface:

- existing `_assign_optional_events()` and its small alignment helpers in
  `transcript_foundation.py`

Required behavior:

1. Expand the OCR event interval by `1_500 ms` for matching.
2. Find the current temporal ASR anchor, then compare only that Unit and its
   immediate previous/next Unit when present.
3. Select at most one best ASR Unit using deterministic temporal proximity plus
   normalized local text/context agreement.
4. Never align to a more distant Unit merely because the text looks similar.
5. Do not add global alignment, DTW, dynamic programming, semantic/model-based
   matching, or a replacement spanning two ASR Units.

### Change 3 — high-evidence short multi-character replace

Primary implementation surface:

- existing `find_local_replacement()`, `_span_is_eligible()`, `_build_unit()`,
  and `build_canonical_transcript()` paths

Required behavior:

1. Accept only `replace`; both ASR and candidate spans must be non-empty. Final
   V1.1 does not accept insert, delete, whole-sentence rewrite, or cross-Unit
   replacement from any optional text source.
2. The ASR and candidate spans may differ in length, but each normalized span
   must be between 1 and 8 characters. This permits short names, numbers, Latin
   abbreviations, and compact lexical phrases.
3. An OCR replacement is eligible only when the selected event has the strong
   cross-frame consensus from Change 1, matches under Change 2, and has high
   unchanged local context around one localized difference. Keep the context
   requirement as one small code constant plus generic tests; do not create
   threshold/version governance or tune it to the known probes.
4. Every accepted character must be copied from the selected source event and
   keep existing event/candidate provenance.
5. Treat nearby mixed differences as one atomic conflict. If a candidate combines
   a plausible correction with an adjacent unsafe change, reject the whole
   replacement; do not accept only its attractive character or span.
6. Anything that does not satisfy all conditions remains ASR provisional with
   `UNRESOLVED`. High OCR confidence by itself is never sufficient.

### Change 4 — artifacts, tests, and complete fresh rerun

Keep artifact changes local and small:

- emit `subtitle-ocr-frame-candidates.jsonl` when Explicit ROI OCR runs;
- emit `accepted-multi-character-replacements.jsonl` for Owner inspection, with
  Unit ID, timestamps, ASR span, accepted source span, source event ID, candidate
  IDs, and consensus support;
- reuse the current Canonical, Manifest, Segment, semantic-v2, and Renderer
  contracts; do not add consensus/alignment version fields.

Provider-free tests must cover six groups:

1. candidate retention, 2–5 frame consensus, observed-text medoid, and tie/one-
   frame rejection;
2. ±1.5 second current/previous/next Unit matching and distant-candidate
   rejection;
3. accepted 1–8 character Chinese/number/Latin replacements, including unequal
   ASR/OCR span lengths;
4. insert/delete, whole-sentence, adjacent mixed conflict, and unsafe OCR
   rejection;
5. Canonical → consensus event → frame candidate provenance;
6. ASR-only, subtitle, projection, CLI/URL/Web, and unchanged downstream
   regressions.

After focused tests pass, process the same complete real game video from `0` to
its measured end with Explicit ROI OCR. Do not reuse the previous OCR events,
Canonical Transcript, segments, Topic Map proposal, or Report Plan proposal.
Regenerate in this order:

```text
Full OCR
  → frame candidates
  → consensus OCR events
  → Fusion
  → canonical-transcript.jsonl
  → segments.jsonl
  → fresh Fused semantic-v2
  → report.html
```

Also generate a fresh ASR-only semantic-v2/report comparison from the same
source. The existing local `OPENAI_API_KEY` may be used with
`https://api.deepseek.com` for these unchanged semantic-v2 calls without another
Owner confirmation. Send only the transcript text and normal semantic-v2 text
context required by the existing path; never send video, frames, crops, or OCR
images. Do not change provider, model, prompt, call count policy, Planner, or
Renderer.

### Final completion and stop

The final rework is complete only when all five conditions hold:

1. the real-video OCR Manifest still records `coverage_ratio=1.0` and full
   processed start/end/duration;
2. correct cross-frame-supported multi-character OCR enters Canonical text
   materially more often than before;
3. the known probes are corrected by general rules, with no probe-specific
   production code or configuration;
4. obvious errors such as `由干`, unsafe deletion, one-frame guesses, and mixed
   conflicts do not appear in the newly accepted replacement export;
5. fresh Fused text completes Semantic → Renderer and at least part of the real
   improvement appears naturally in `report.html` compared with fresh ASR-only.

Inspect every row in `accepted-multi-character-replacements.jsonl` for obvious
pollution and record that bounded manual result in `V1.1-DELIVERY.md`. This is a
one-time Owner review aid, not a new Eval framework or permanent quality system.

Run focused tests, full pytest, Ruff, and `git diff --check`; update current
status and Delivery evidence; then stop at
`READY_FOR_OWNER_V1.1_FREEZE_REVIEW`. Do not record `V1.1_FROZEN`, start V1.2,
commit, push, open a PR, publish, or deploy.

## Mission

Implement V1.1 end to end so the product has one general, source-preserving
transcript truth layer:

```text
Video / Bilibili URL
        ↓
ASR
Subtitle Track
Burned-in Subtitle OCR
        ↓
Temporal Alignment
        ↓
High-confidence Local Fusion
        ↓
Canonical Transcript
        ↓
V1.0-compatible VideoSegment
        ↓
Existing semantic-v2
        ↓
Existing Renderer
        ↓
report.html
```

The product result must demonstrate that reliable subtitles can correct ASR
proper nouns, numbers, English abbreviations, and small formatting errors
without allowing OCR from slides, HUDs, logos, or unstable frames to pollute the
transcript.

## Mandatory read order

Read only the current package before editing:

1. `AGENTS.md`
2. `docs/visual-report/V1-STATUS.md`
3. `docs/visual-report/V1-ROADMAP.md`
4. this task card
5. the directly affected source files and tests

The old `docs/requirements/visual-report-v1a/` package is historical. Do not
reload or extend its readiness, coverage, decision-evidence, measurement, or
provider-conformance machinery for V1.1.

## Verified starting point

Documentation was prepared against branch `visual-report`, product-code commit
`065a592a8aa77829bdccc31828edadebc68a6d63`.

The current runtime already has:

- `src/video_evidence_agent/asr.py`: MLX Whisper ASR with timestamped
  `AsrSegment` output and retained raw result;
- `src/video_evidence_agent/segments.py`: ASR-specific 45–60 second
  `VideoSegment` construction;
- `src/video_evidence_agent/schemas.py`: `VideoSegment` with required
  `source_asr_ordinals` provenance;
- `src/video_evidence_agent/cli.py`: local MP4 ingest;
- `src/video_evidence_agent/visual_report/url_ingest.py`: public Bilibili BV URL
  download followed by existing ingest;
- `src/video_evidence_agent/visual_report/planning_runtime.py`: current
  semantic-v2 transcript-to-plan path;
- `src/video_evidence_agent/visual_report/renderer.py`: current deterministic
  renderer;
- `src/video_evidence_agent/visual_report/web.py`: loopback Web surface and
  single-process FIFO queue.

At construction start, recheck the current branch/dirty state and preserve all
user work. A later commit or expected documentation overlay is not a blocker and
must not be reset.

## Continuous execution contract

The four active changes above are one continuous implementation sequence. The
original A/B/C sections below are already completed baseline history, not work
to repeat and not Owner gates.

The execution session must:

1. recheck the current checkout and preserve user work;
2. implement frame-candidate retention and consensus;
3. implement the bounded neighboring-Unit match and replace-only Fusion rule;
4. run focused tests, repair ordinary failures, and continue automatically;
5. run the complete fresh-video OCR/Fusion/Semantic/Render comparison;
6. inspect the exported accepted multi-character replacements;
7. run final regression, update Delivery/status, and stop at the required final
   state.

Do not pause merely because OCR is imperfect, one optional subtitle is absent,
one sample is unresolved, Auto ROI is unstable, or a normal test needs repair.

Stop and ask the Owner only when:

- a required credential or source resource is missing and no in-scope path can
  continue;
- an irreversible external action is required;
- the core ASR + subtitle/OCR → Canonical Transcript route is technically
  infeasible after reasonable in-scope repair;
- the current repository has a major conflicting change that cannot be safely
  preserved or adapted around.

No commit, push, PR, public publication, or deployment is part of this card.

## Hard scope boundary

V1.1 may change transcript acquisition, normalization, alignment, fusion,
projection, CLI wiring, URL subtitle discovery, and minimal Web status display.

V1.1 must not change:

- semantic-v2 system/user prompts;
- Topic Mapper, Topic Resolver, Report Planner, planning budgets, or semantic
  compiler behavior;
- the renderer, visual tokens, block family, or page layout;
- RAG, retrieval, Agent, LangGraph, tool loops, memory, or fine-tuning;
- VLM, keyframes, frame captioning, or full-screen scene OCR;
- database, durable queue, multi-worker execution, accounts, tenancy,
  deployment, hosting, or public sharing;
- frozen P0-B/V0/V1-A inputs, runs, evaluation artifacts, or conclusions.

Auto ROI is best-effort only. Do not introduce a VLM, object detector, layout
model, or complex vision pipeline to improve it.

## Dependency policy

Use the existing Python 3.12 + uv workflow.

Expected new runtime capabilities are:

- RapidOCR with an ONNX Runtime backend for local OCR;
- a small subtitle parser such as `pysubs2` for SRT/VTT/ASS;
- the existing FFmpeg/ffprobe and OpenCC dependencies.

Choose currently compatible package versions during construction, add them with
`uv add`, and update `pyproject.toml` plus `uv.lock`. Do not add a second OCR
engine, cloud OCR, VLM SDK, or a general computer-vision framework unless
RapidOCR cannot run in the current environment and the task is otherwise
blocked. Provider-free tests must use a fake OCR adapter and must not require
model/network access.

## Canonical data contracts

Keep these contracts small and versioned. Internal file/class placement is
implementation-delegated; do not build a framework around them.

### `SourceTextEvent`

One timestamped event from `asr`, `subtitle_track`, or `ocr`:

```json
{
  "event_id": "ocr-000001",
  "source": "ocr",
  "start_ms": 12400,
  "end_ms": 15700,
  "text": "我们使用 RLinf 进行训练",
  "normalized_text": "我们使用 RLinf 进行训练",
  "confidence": 0.93,
  "stability": {
    "sample_count": 4,
    "distinct_frame_count": 3
  },
  "provenance": {
    "roi": [0.05, 0.72, 0.95, 0.98],
    "frame_timestamps_ms": [12400, 12900, 13400, 13900]
  }
}
```

Rules:

- `text` is source text and is never overwritten;
- `normalized_text` is deterministic comparison text;
- confidence is source-specific and may be absent;
- confidence values from different sources are never averaged;
- provenance carries only the source details that exist for that source.

### `TranscriptUnit`

One fine-grained canonical unit, anchored to ASR continuity:

```json
{
  "unit_id": "unit-000001",
  "start_ms": 12000,
  "end_ms": 15600,
  "canonical_text": "我们使用 RLinf 进行训练",
  "asr_text": "我们使用R英孚进行训练",
  "ocr_text": "我们使用 RLinf 进行训练",
  "subtitle_text": null,
  "resolution": "ocr_corrected_asr",
  "flags": [],
  "provenance": {
    "asr_event_ids": ["asr-000018"],
    "candidate_event_ids": ["ocr-000001"],
    "replacement": {
      "asr_span": "R英孚",
      "candidate_span": "RLinf"
    }
  }
}
```

Required resolution vocabulary may include:

- `asr_only`
- `sources_agree`
- `subtitle_corrected_asr`
- `ocr_corrected_asr`
- `subtitle_ocr_corrected_asr`
- `asr_preserved_ocr_rejected`
- `unresolved`

### `TranscriptManifest`

One lightweight JSON object recording:

- schema version, video ID, duration, and transcript mode;
- source status/count/path for ASR, subtitle track, and OCR;
- canonical-unit and projected-segment counts;
- deterministic normalizer/fusion versions;
- `READY`, `DEGRADED`, or `FAILED` plus concise warnings;
- artifact paths.

Do not add hashes, readiness coverage, frozen-revision governance, or a formal
evaluation protocol to this manifest.

## Deterministic normalization

Preserve raw text and derive comparison text with a closed deterministic pass:

1. Unicode NFKC;
2. trim and collapse whitespace;
3. conservative punctuation-width/spacing normalization;
4. OpenCC traditional-to-simplified normalization for Chinese comparison;
5. retain the selected source's meaningful Latin casing and numeric spelling in
   canonical output.

Normalization may change presentation-equivalent characters, but it may not
invent lexical content or silently rewrite a sentence.

## Completed baseline — Slice A: Explicit-ROI Subtitle OCR Value Prototype

### Objective

Prove that local burned-in subtitle OCR produces useful timestamped correction
candidates before building the fusion layer.

### Required CLI

Add a provider-free command equivalent to:

```bash
video-evidence transcript-ocr VIDEO \
  --video-id VIDEO_ID \
  --roi X1,Y1,X2,Y2 \
  --sample-fps 2 \
  --output PATH
```

The ROI uses normalized coordinates in `[0,1]` and must satisfy
`0 ≤ x1 < x2 ≤ 1` and `0 ≤ y1 < y2 ≤ 1`.

### Required behavior

Implement:

1. sparse timestamped sampling, not per-frame OCR;
2. cropping to the explicit subtitle ROI before text analysis;
3. lightweight visual-change filtering before OCR;
4. perceptual duplicate suppression so unchanged captions are not repeatedly
   recognized;
5. RapidOCR only on retained changed samples;
6. conservative text normalization;
7. merge temporally adjacent, highly similar OCR samples into one event with a
   start/end range;
8. retain sample timestamps, ROI, OCR confidence, and cross-frame stability.

Output `SubtitleOcrEvent[]` as JSONL. A repeated subtitle must become one event,
not frame-level fragments. Event IDs and ordering must be deterministic for the
same video, ROI, sample rate, and OCR output.

Temporary sampled frames may be deleted after successful event creation; the
event provenance must retain enough timestamps to reproduce or inspect the
choice. Do not retain a large frame dump as a product artifact.

### A self-check

The execution session selects short ranges from existing local media:

- positive caption sample: the Wu Yi video under `eval/p0b/media/`;
- subtitle-plus-noise stress sample: the Bilibili game video currently retained
  under `artifacts/visual-report/url-ingest/`;
- negative/static-text sample: the retained Codex presentation video under the
  same URL-ingest root.

The game sample is only a general HUD/noise stress case. Do not add game
dictionaries, game-specific terms, or content-specific routing.

Inspect whether OCR:

- captures real subtitles and useful names/numbers/Latin tokens;
- avoids obvious slide, HUD, logo, and static UI pollution;
- produces reasonable event times;
- merges repeated frames into one event.

Repair ordinary failures and continue automatically to B. Auto ROI is not part
of A and is not an A completion condition.

## Completed baseline — Slice B: Canonical Transcript and V1.0 Compatibility

### Objective

Create the actual transcript truth layer:

```text
ASR Events + Subtitle Track Events + Subtitle OCR Events
        ↓
Temporal Alignment
        ↓
High-confidence Local Fusion
        ↓
TranscriptUnit[] + TranscriptManifest
```

### Source conversion and alignment

- Convert current normalized `AsrSegment` rows into `SourceTextEvent` rows and
  retain raw ASR provenance. Preserve word timestamps when the ASR backend
  supplies them, but do not make word timestamps a V1.1 dependency.
- Convert subtitle cues and A output to the same event contract.
- Align by interval overlap with only a small documented timestamp-jitter
  allowance. Do not align distant text because it looks semantically similar.
- ASR provides continuity anchors. An unaligned OCR/PPT/HUD candidate remains in
  `source-text-events.jsonl` but cannot create free-standing canonical body text
  in V1.1.

### Fusion rule

Fusion is not general text rewriting. It is one conservative operation:

> Replace one localized ASR span with a span copied from a temporally aligned,
> stable subtitle source when the surrounding text clearly identifies the same
> utterance.

A replacement is eligible only when all of the following hold:

1. the source events overlap in time within the documented alignment tolerance;
2. after deterministic normalization, the texts share enough unchanged local
   context to identify one utterance;
3. the difference is one localized span, not a sentence-level rewrite;
4. a subtitle-track cue is structurally valid, or an OCR event is stable across
   multiple samples;
5. the changed span is suitable for a local correction, such as a proper name,
   number, English abbreviation, short lexical token, punctuation, spacing, or
   casing;
6. every inserted character comes from an aligned source event and is recorded
   in provenance.

Subtitle track, OCR, and ASR do not have a universal priority order:

- subtitle + OCR agreement strengthens a local candidate;
- a stable single subtitle source may correct ASR when local context is clear;
- unstable or one-frame OCR cannot correct ASR;
- if ASR agrees with a reliable source and OCR is an outlier, keep ASR and mark
  the OCR candidate rejected;
- if sources disagree across a whole sentence, timestamps are weak, or choosing
  requires semantic interpretation, keep normalized ASR as provisional
  `canonical_text`, set `resolution="unresolved"`, add `UNRESOLVED`, and retain
  all candidates.

Do not add a large hierarchy of heuristics. If the one-local-span rule is not
clearly satisfied, use `UNRESOLVED`.

### Required provider-free CLI

Add a command equivalent to:

```bash
video-evidence fuse-transcript \
  --manifest MANIFEST_JSON \
  --asr ASR_JSON \
  --ocr OCR_EVENTS_JSONL \
  --subtitle SUBTITLE_EVENTS_JSONL \
  --output-root OUTPUT_DIR
```

`--ocr` and `--subtitle` are optional. ASR-only input must still produce a valid
Canonical Transcript and compatible segments.

The command emits:

- `source-text-events.jsonl`
- `canonical-transcript.jsonl`
- `transcript-manifest.json`
- V1.0-compatible `segments.jsonl`

### V1.0 `VideoSegment` projection

The Canonical Transcript is the fine-grained truth. The existing 45–60 second
`VideoSegment` remains a batching and compatibility layer.

Extend `VideoSegment` with an optional:

```json
"source_transcript_unit_ids": ["unit-000001", "unit-000002"]
```

Compatibility requirements:

- historical JSONL containing only `source_asr_ordinals` still validates;
- a new segment must retain at least one of `source_asr_ordinals` or
  `source_transcript_unit_ids`;
- fused ASR-backed segments should retain both when available;
- current segment IDs, ordering, non-overlap, duration behavior, and semantic-v2
  input fields remain compatible;
- no semantic-v2 loader, prompt, planner, or renderer change is permitted merely
  to consume the optional provenance field.

### B self-check and downstream proof

Run provider-free unit/integration checks, then inspect real aligned conflicts.
Repair ordinary issues and continue automatically.

Before entering C, run the current V1.0 report pipeline with one real fused
transcript and confirm:

```text
Canonical Transcript
  → compatible segments.jsonl
  → existing semantic-v2
  → existing renderer
  → report.html
```

For final comparison, produce one ASR-only and one fused report from the same
source/config. Do not modify the semantic prompt to force a word into the
report. Select a naturally report-relevant known ASR error and verify at least
one corrected term can propagate when that content is selected.

## Completed baseline — Slice C: Generalization and Product Integration

### C1. Subtitle-track support

Support the smallest useful text-subtitle paths:

1. explicit sidecar supplied by the operator;
2. text subtitle track inside a local container;
3. text subtitle file made available by the existing Bilibili/yt-dlp download.

Support SRT, VTT, and ASS text cues through one parser. Prefer a Chinese track
when several discoverable tracks exist and record the selected track. Keep
discovery rules deterministic and documented; do not attempt to support every
subtitle format.

Source behavior:

- no subtitle: `ABSENT`, continue;
- image subtitle such as PGS: `UNSUPPORTED`, continue;
- malformed optional subtitle: `FAILED` for that source and overall
  `DEGRADED` when ASR is still usable;
- valid cues become `SourceTextEvent` rows and enter the same B fusion logic.

### C2. Best-effort Auto ROI

Only after explicit ROI is reliable, add a simple optional Auto mode:

1. OCR a small number of sparse full-frame samples;
2. cluster text boxes into coarse horizontal bands by position;
3. favor recurring, centered, sentence-like bands whose text changes over time;
4. reject obvious tiny-corner logos, always-static bands, oversized slide/code
   regions, and unstable candidates;
5. choose at most one subtitle ROI only when the best candidate is clearly
   usable;
6. hand the resulting ROI to the already-tested explicit-ROI path.

If no stable ROI is found, record `AUTO_ROI_UNSTABLE`, continue without OCR,
and mark the run `DEGRADED` when appropriate. Do not add VLM, object detection,
layout analysis, or a second OCR system. Auto ROI quality is not part of the
V1.1 completion gate.

### C3. DeepSeek conflict arbitration (not implemented)

Default: do not implement it. The active final rework above excludes this
arbitrator even if additional local conflicts are observed.

The following retained text describes the earlier optional boundary only; it is
not current construction authority. If a future separately authorized version
adds an arbitrator, it must:

- receive only the aligned candidate strings and a small neighboring text
  window;
- receive no frame, full transcript, or unrelated context;
- select only source-provided character spans and return their source event IDs;
- never rewrite a sentence or generate a new character;
- use the existing configured provider with one explicit identical technical
  retry at most;
- leave unresolved cases `UNRESOLVED`.

If deterministic fusion handles the observed cases, record “not needed” in the
delivery report and add no arbitration code.

### C4. CLI and existing product paths

Extend the existing ingest surface with the smallest compatible options:

```text
--transcript-mode asr-only|fused
--ocr-mode off|roi|auto
--ocr-roi X1,Y1,X2,Y2
--subtitle-file PATH
```

Use `fused` as the new transcript mode default. With no usable subtitle/OCR
source, fused mode must deterministically reduce to ASR-only text and remain
compatible.

For local MP4:

- explicit ROI is the reliable product path;
- `off` preserves a fast ASR-only run;
- `auto` is optional and degradable.

For Bilibili URL:

- keep the current validated URL and yt-dlp boundary;
- request available text subtitles without making their presence mandatory;
- run the same transcript foundation after download;
- allow the server/operator to provide an explicit ROI; otherwise Auto mode may
  be attempted and may degrade to ASR-only;
- preserve the current single-process FIFO behavior.

### C5. Minimal Web status integration

Do not build a new state machine. Extend the current display mapping with the
minimum transcript stages:

- `TRANSCRIBING`
- `OCR`
- `FUSING`
- `READY`
- `DEGRADED`
- `FAILED`

Existing download/planning/render states may remain internal or map to the
nearest display step. `READY` maps to a completed current report. `DEGRADED`
means the report can continue from usable ASR while an optional subtitle/OCR
source is absent, unsupported, unstable, or failed. `FAILED` is reserved for no
usable text source or an invalid core artifact.

Do not add durable queue persistence, accounts, database, tenancy, or remote
hosting.

## Artifact contract

For a fused run, retain under its transcript/output root:

```text
source-text-events.jsonl
subtitle-ocr-events.jsonl        # when OCR was attempted
canonical-transcript.jsonl
transcript-manifest.json
segments.jsonl
manifest.json                    # existing ingest manifest, extended minimally
```

The downstream Visual Report run continues to own its current Topic Map, plan,
assets, `run.json`, and `report.html` artifacts.

All canonical changes must trace to ASR, subtitle track, or OCR events. No
source-less lexical text may appear. Deterministic punctuation/Unicode
normalization must be named separately from source-backed correction.

## Expected change surface

Use the smallest useful module split. Expected allowed paths are:

- a small new transcript-foundation module/package under
  `src/video_evidence_agent/`;
- `src/video_evidence_agent/asr.py` for optional word-timestamp preservation;
- `src/video_evidence_agent/schemas.py` and
  `src/video_evidence_agent/segments.py` for compatible projection;
- `src/video_evidence_agent/cli.py` for OCR/fusion/ingest commands;
- `src/video_evidence_agent/visual_report/url_ingest.py` and
  `src/video_evidence_agent/visual_report/web.py` for subtitle discovery and
  minimal product-state wiring;
- focused tests/fixtures;
- `pyproject.toml` and `uv.lock` for the bounded OCR/subtitle dependencies;
- this task, `V1-STATUS.md`, and the final delivery report.

Protected unless a reproduced compatibility defect makes a tiny plumbing fix
unavoidable:

- `visual_report/planning.py`
- `visual_report/planning_runtime.py`
- `visual_report/evaluation.py`
- `visual_report/models.py`
- `visual_report/renderer.py`
- frozen `eval/p0b/**`, `artifacts/p0b-*/**`, and historical V0/V1-A evidence.

Any unavoidable protected-file change must leave semantic and visual behavior
identical and be covered by a regression test. Do not use V1.1 to clean up
unrelated historical code.

## Completed baseline test and sample plan

### Provider-free tests

Add focused fixtures/tests for:

- explicit normalized ROI validation and crop boundaries;
- sparse sampling and pre-OCR visual-change filtering;
- perceptual duplicate removal;
- stable OCR sample merge and event timing;
- source event schemas and raw-text preservation;
- SRT/VTT/ASS parsing and container/URL discovery outcomes;
- NFKC, whitespace, punctuation, and OpenCC normalization;
- temporal alignment and jitter boundaries;
- accepted local proper-name/number/Latin/format correction;
- bad/unstable OCR leaving correct ASR unchanged;
- whole-sentence conflict producing ASR provisional + `UNRESOLVED`;
- rejection of any canonical character without source/normalization provenance;
- ASR-only canonical output;
- `VideoSegment` historical JSON compatibility and new unit provenance;
- fused projection into the unchanged semantic-v2 loader;
- optional subtitle/OCR absence mapping to `DEGRADED`, not `FAILED`;
- URL/local CLI and Web/FIFO regressions.

Use a fake OCR adapter for unit/integration tests. Real OCR is a sample check,
not a CI dependency.

### Real sample checks

Use a few short, fixed time ranges rather than building a new Eval framework.
For each selected range, retain only enough manual transcription to compare:

- ASR-only text;
- available OCR/subtitle text;
- final canonical text;
- optional short-range CER;
- proper-name, number, English abbreviation, and newly introduced error counts.

The final delivery needs only a small Before/After set:

1. ASR error corrected by reliable OCR or subtitle;
2. incorrect/unstable OCR rejected so correct ASR is not polluted;
3. ambiguous conflict retained as provisional ASR + `UNRESOLVED`;
4. one known correction visible in the downstream report path.

Do not create an Eval framework, readiness validator, coverage map, formal gate,
or fixed pass threshold from these examples.

### Required final commands

Adapt test filenames to the final small module split, then run at least:

```bash
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run ruff check .
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q \
  tests/test_transcript_foundation.py \
  tests/test_asr.py \
  tests/test_segments.py \
  tests/test_visual_report_url_ingest.py \
  tests/test_visual_report_web.py
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q
git diff --check
```

Also run the real explicit-ROI OCR command, real fusion command, one local or
URL fused ingest, and one ASR-only versus fused downstream report comparison.

## Original baseline deliverables (completed)

The completed task must deliver:

- working ASR, subtitle-track, and burned-in subtitle OCR source paths;
- reliable explicit ROI OCR CLI;
- best-effort Auto ROI with honest limitations;
- deterministic local fusion with `UNRESOLVED` behavior;
- `source-text-events.jsonl`;
- `canonical-transcript.jsonl`;
- `transcript-manifest.json`;
- compatible `segments.jsonl` with transcript-unit provenance;
- local MP4 and Bilibili URL integration;
- minimal Web OCR/FUSING/degraded status behavior;
- provider-free tests and full regression results;
- one ASR-only versus fused real downstream comparison;
- a few Before/After examples;
- `docs/visual-report/V1.1-DELIVERY.md` containing changed files, commands,
  results, examples, limitations, whether arbitration was needed, and the final
  state;
- updated `docs/visual-report/V1-STATUS.md` and this task's implementation
  evidence.

## Definition of done

The original A/B/C baseline criteria above are already satisfied. The active
final rework is done only when its five completion conditions pass, every newly
accepted multi-character replacement has been manually inspected for obvious
pollution, tests pass, and the fresh Fused/ASR-only reports are recorded in
`V1.1-DELIVERY.md`.

V1.1 still does not require perfect OCR, universal subtitle-region discovery,
every subtitle format, a DeepSeek Fusion arbitrator, VLM, keyframes, a formal
Eval system, deployment, or automatic Owner acceptance. Success means reliable
OCR is materially more useful without obvious new contamination; it is not a
perfect subtitle-engine claim.

## Copy-ready Goal prompt

Use the following as the separate construction Goal. Sending it is the explicit
authorization that this documentation turn intentionally does not provide.

```text
请在 /Users/tristana/Develop/video-evidence-agent 中连续执行
VR-V1.1-TRANSCRIPT-FOUNDATION-013 的最后一轮有限 Fusion 返工。

先依次阅读 AGENTS.md、docs/visual-report/V1-STATUS.md、
docs/visual-report/V1-ROADMAP.md 和
docs/tasks/VISUAL-REPORT-V1-1-TRANSCRIPT-FOUNDATION.md。以其中置顶的
“Active construction contract — final bounded Fusion rework”为本轮完整施工合同；原 A/B/C
已经完成，只是保留的历史基线，不要重新施工。

本 Goal 授权你连续完成：帧级 OCR 候选保留与 2–5 帧简单共识、±1.5 秒且当前 Unit ±1 的
局部时间匹配、高证据 1–8 字符 replace-only Fusion，以及同一完整真实视频从 Full OCR 到
fresh Semantic-v2 与 Renderer 的全链路重跑。自行修改现有实现和测试、修复普通失败并继续，
不要在内部步骤等待 Owner 确认。

必须撤销 Explicit ROI 单帧高置信修正和 insert/delete 放行。无法同时满足跨帧共识、局部
时间匹配和高上下文一致性的候选，继续保留 ASR provisional + UNRESOLVED。不得为献祭、
星象房、RLinf 或其他样本词加入词典、专名规则、Prompt 或阈值特判。

完整重跑不得复用旧 OCR events、Canonical Transcript、segments、Topic Map proposal 或
Report Plan proposal。Fresh Fused 与 fresh ASR-only semantic-v2 可以直接使用本地
OPENAI_API_KEY 调用 https://api.deepseek.com，无需再次询问授权；只发送现有 semantic-v2
正常需要的转录文本与文本上下文，不发送视频、帧、裁剪图或 OCR 图片，不做
Provider/模型/Prompt 实验。

完成后导出并逐条检查 accepted-multi-character-replacements.jsonl，运行 focused tests、
full pytest、Ruff、git diff --check，更新 V1.1-DELIVERY.md、V1-STATUS.md 和任务证据。不要新增
公共候选 Schema、consensus/alignment 版本治理、复杂 Alignment、Eval Framework、VLM、
Semantic/Renderer 改造；不要 commit、push、PR、发布、部署或开始 V1.2/V1.3。最终停在
READY_FOR_OWNER_V1.1_FREEZE_REVIEW。
```

## Implementation evidence

Status: `READY_FOR_OWNER_V1.1_FREEZE_REVIEW` (the historical pre-rework
paragraphs below are retained for audit context).

The Owner authorized `VR-V1.1-TRANSCRIPT-FOUNDATION-013` on 2026-09-01. A/B/C
were implemented continuously in this checkout without intermediate Owner
gates. RapidOCR/ONNX Runtime and `pysubs2` are locked through the existing uv
workflow. The implementation is local-only for video, frames, subtitle parsing,
OCR, alignment, and fusion; no provider arbitration was needed.

Implementation evidence:

- Explicit ROI OCR produced deduplicated timestamped events on the local Wu Yi
  and Bilibili game samples. The game sample produced 16 events in the first
  30 seconds; the Wu Yi sample produced 8 events. The presentation negative
  sample produced one static/noisy event and was not used as a positive fusion
  example.
- Canonical transcript artifacts preserve source events and project into
  compatible `VideoSegment` records with `source_transcript_unit_ids`. A real
  game fusion produced 302 units and 30 segments with subtitle absence recorded
  as `DEGRADED`; a real local 30-second MP4 ingest produced 11 units and one
  segment with the same honest degradation.
- A frame-checked game example corrected `免得吞掉我们礼店宝贵的商店` to
  `免得吞掉我们里店宝贵的商店` from stable two-frame explicit-ROI OCR. The
  same sample's visually wrong OCR `并且由干里店...` is now preserved as ASR
  provisional and marked `UNRESOLVED`; deletion-like `刀刃` → `刀` is also not
  accepted. Whole-sentence conflict behavior is covered by provider-free tests.
- SRT/VTT/ASS parsing, sidecar/container discovery, best-effort Auto ROI,
  local MP4 ingest, Bilibili subtitle-request wiring, CLI options, and minimal
  Web status/options are implemented. Auto ROI was `READY` for the game sample
  and `UNSTABLE` for Wu Yi and the static presentation sample; Auto ROI is not a
  completion gate.
- Provider-free semantic-v2 replay produced ASR-only and fused `report.html`
  outputs through the unchanged semantic/renderer path. The fused report
  carries the source-backed `礼店` → `里店` correction. No new Eval framework,
  validator, formal gate, VLM, keyframe path, RAG, Agent, database,
  multi-tenancy, deployment, commit, push, or PR was added.

Validation completed after the bounded Fusion refinement: focused Transcript
Foundation tests `23 passed`; existing
non-Web regression `109 passed, 8 deselected`; URL/Web regression `12 passed`;
full pytest `125 passed`; Ruff and `git diff --check` passed. Full commands,
artifact paths, and Before/After evidence are in
[`docs/visual-report/V1.1-DELIVERY.md`](../visual-report/V1.1-DELIVERY.md).

Previous Owner review history: the first review recorded
`CHANGES_REQUESTED — FUSION_POLICY_TOO_CONSERVATIVE`. The authorized refinement
now supports independently separated short spans, Explicit ROI single-frame
evidence at the policy threshold `0.90`, and OCR insertions, while retaining
Auto ROI multi-frame stability, rejecting OCR deletions, and keeping adjacent
`于礼` → `干里` plus sentence-level conflicts unresolved. The real game
Canonical Transcript, segments, and ASR-only/Fused reports were regenerated.
Those single-frame and insertion behaviors are superseded by the active final
rework contract; this paragraph remains historical evidence only.

The Owner later identified that the retained real OCR evidence covered only
30–70 second windows, so the prior review-ready state was withdrawn. A new
single-call Explicit ROI run now covers the complete 1,566,677 ms game video:
504 events, `processed_start_ms=0`, `processed_end_ms=1566677`,
`coverage_ratio=1.0`, and `coverage_status=FULL`. Fresh Fusion regenerated 302
Canonical Units and 30 segments; 42 units differ from ASR-only text, with the
last changed unit at 1,480,000 ms.

The new Manifest contract preserves compatible source `status` while adding
explicit coverage fields. `PARTIAL` and `UNKNOWN` OCR inputs degrade the fused
manifest with named warnings, preventing a short sample from being read as a
full-video fused transcript. Focused regression is `44 passed`, full pytest is
`125 passed`, and Ruff plus `git diff --check` pass.

The first mandatory non-replay semantic-v2 attempt on regenerated Fused
segments failed in the sandbox with `PROVIDER_ERROR`; that failed identity is
retained. After the Owner explicitly authorized the complete Fused and ASR-only
transcript text transfer to `https://api.deepseek.com`, both new runs completed
with exactly 2/2 model calls and reached `RENDERED`. The Fused output contains
8 Topics, 5 sections, 8 blocks, and 26 uniquely cited segments; ASR-only
contains 7 Topics, 5 sections, 9 blocks, and 13 uniquely cited segments.

The full-video execution gap is closed, but the following Owner content review
found the transcript quality insufficient: repeated correct OCR such as `献祭`
and `星象房` still failed to enter Canonical text reliably, and unstable names
must not be forced into the output. The former review-ready state is withdrawn.

The preceding paragraph records the pre-rework state. The final bounded rework
is now complete and the current stop is
`READY_FOR_OWNER_V1.1_FREEZE_REVIEW`. No V1.1 freeze or V1.2/V1.3
authorization is recorded.

### Final bounded Fusion rework evidence — 2026-09-01

The final rework retained frame-level OCR candidates and applied the bounded
consensus, neighboring-Unit time match, and replace-only Fusion contract. It
also added generic repeated corroboration for ambiguous multi-character CJK
replacements; no sample-specific words, dictionaries, prompts, providers,
models, or thresholds were added. Explicit-ROI single-frame acceptance and
insert/delete acceptance are absent from the final policy.

The complete local Bilibili game video was freshly processed with Explicit ROI
from `0` to measured end (`1,566,677 ms`) at the existing ROI
`[0.12, 0.74, 0.88, 0.96]` and `sample_fps=2`:

- `504` fresh deduplicated OCR events;
- `757` retained frame candidates;
- `coverage_ratio=1.0`, `coverage_status=FULL`;
- fresh Fused and ASR-only Canonical/segments: `302 / 30` each;
- Fused status `DEGRADED` only for absent subtitle track and
  `UNALIGNED_OPTIONAL_EVENTS:107`.

The final Fused accepted export contains `20` rows across `16` Units. Every
row is OCR-backed, has `2–5` candidate IDs with consensus support `>=2`, is a
non-empty replace-only operation, and keeps both normalized spans within
`1–8` characters. Manual inspection found no `由干`, `干里`, `里店 END`,
insertion, deletion, or one-frame row in the accepted export. `星象` enters
Canonical in `unit-000016` and `unit-000137`; `献祭` enters Canonical in
`unit-000191`; the rejected `由干` candidate remains ASR provisional with
`UNRESOLVED`.

Fresh downstream runs used new transcript inputs and did not reuse old OCR
events, Canonical/segments, Topic Map proposals, or Report Plan proposals:

- Fused `fused-semantic-v2-20260901-final`: `RENDERED`, `2/2` provider/model
  calls, `5` sections, `11` blocks, report at
  `artifacts/visual-report/v1.1/final-bounded-rework-20260901/game/semantic-v2/fused-semantic-v2-20260901-final/report.html`;
- ASR-only `asr-only-semantic-v2-20260901`: `RENDERED`, `2/2` provider/model
  calls, `4` sections, `10` blocks, report at
  `artifacts/visual-report/v1.1/final-bounded-rework-20260901/game/semantic-v2/asr-only-semantic-v2-20260901/report.html`.

Only the normal transcript/text context was sent to the authorized
`https://api.deepseek.com` semantic-v2 path; no video, frame, crop, or OCR
image was sent. An initial sandbox connection failure and a later unusable
model-plan failure remain preserved as separate failed run identities; neither
was overwritten or deleted.

Final validation: focused Transcript Foundation `30 passed`; required combined
focused suite `51 passed`; full pytest `132 passed`; `uv run ruff check .`
passed; `git diff --check` passed. The final state is
`READY_FOR_OWNER_V1.1_FREEZE_REVIEW`.
