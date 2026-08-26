# P0-B locked evaluation inputs

This directory holds the owner-confirmed versioned metadata for `p0b-r1` and
the single formal `TRANSCRIPT_RETRIEVAL` evaluation method. It uses three
natural continuous Chinese technical videos, local FFmpeg plus Chinese MLX
Whisper ASR, 127 timestamped segments, character 2–4 gram TF-IDF Top-5
retrieval, and a DeepSeek text answer call constrained to the current question
and Top-5.

The media files belong under the ignored `eval/p0b/media/` directory. They are
read locally for FFmpeg/ASR and hash/duration validation; they are never
uploaded by the P0-B answer workflow and must never be committed.
`local_path_alias` in `corpus.jsonl` is an alias relative to that media root,
not a secret or a replacement for the public source URL.

Required files:

- `corpus.jsonl`: exactly three `CorpusRecord` rows, including source URL,
  license, attribution, local-use basis, media hash, and duration.
- `questions.jsonl`: exactly twelve `P0BQuestion` rows, four per video.
- `gold.jsonl`: exactly twelve human-reviewed `P0BGoldRecord` rows.
- `prompts/transcript-retrieval-v1.md`: the frozen DeepSeek answer prompt.

The safe order is:

```text
1. validate the owner-confirmed corpus/questions/Gold and existing ingest artifacts
2. `video-evidence p0b-freeze`
3. `video-evidence p0b-run` (one DeepSeek text call per question)
4. `video-evidence p0b-grade` (automatic score plus review material)
5. owner reviews the materials and records the semantic labels, or explicitly
   delegates that labeling under `eval/p0b/rubric.md`
6. `video-evidence p0b-report`
```

`p0b-run` does not load `gold.jsonl`, full transcript, or answer points. Before
each answer call it persists that question's `retrieval.json`; the local gate
then restores quote and timestamps from the source segment. Provider, schema,
timeout, retrieval, and ingest failures are preserved as per-question result
artifacts. No video-provider or Mock path exists.

For the frozen `p0b-r1` run, the owner reviewed all 12 materials and explicitly
authorized Codex to record the rubric booleans. The final recommendation is
`P0B_RETRIEVAL_THRESHOLDS_NOT_MET`; this is a closed evaluation, not a P0-B
quality pass.

## P0-B R2 follow-up

`p0b-r2` is a new revision of the same single method, not a second baseline.
It reuses the three owner-confirmed videos, the 127 existing ingest segments,
the 12 questions, and the 12 Gold rows. The only implementation changes are a
deterministic character 2–4 gram TF-IDF query-view/score-aggregation profile,
an evidence-insufficiency answer prompt, and revision-safe output paths. No
video is uploaded and no Gemini, Dense, Hybrid, Reranker, Embedding, VLM, Agent,
FastAPI, or database path is active.

The r2 prompt is `prompts/transcript-retrieval-r2.md`. Its frozen manifest is at
`revisions/p0b-r2/eval-manifest.json`, with formal results under
`artifacts/p0b/p0b-r2/` and the report under
`reports/p0b-r2-retrieval-eval.md` plus its JSON companion. The r1 manifest at
`eval-manifest.json` and all r1 artifacts remain immutable.

The r2 safe order is:

```text
1. run the offline tests, strict JSONL checks, r1 protection checks, and media/
   ingest/Gold validation
2. `video-evidence p0b-freeze --eval-revision p0b-r2 --gold-revision p0b-r1 \
   --manifest-out eval/p0b/revisions/p0b-r2/eval-manifest.json`
3. obtain explicit owner authorization for 12 new real DeepSeek text calls
4. `video-evidence p0b-run --manifest eval/p0b/revisions/p0b-r2/eval-manifest.json`
5. `video-evidence p0b-grade --manifest eval/p0b/revisions/p0b-r2/eval-manifest.json`
6. pause for owner semantic review of the generated 12-question materials
7. after the required review, generate `reports/p0b-r2-retrieval-eval.md`
```

The r2 manifest is frozen and no new DeepSeek calls have been made. Each future question will persist its own
Top-5 retrieval before its single answer call; failures remain visible and are
not selectively rerun or overwritten. The fixed-set development retrieval
check is not a formal P0-B result and cannot by itself establish a pass.
