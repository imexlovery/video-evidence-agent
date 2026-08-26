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
