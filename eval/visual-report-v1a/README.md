# V1-A measurement package

This directory contains the versioned review cards and immutable measurement
declarations for `VR-V1A-PLANNING-001`. The current declaration is
`measurement-manifest-v2.json`; it predeclares two retained run identities for
each of the three fixed transcripts and twelve planned model calls.

Freeze and evaluate from the repository root:

```bash
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run python -m video_evidence_agent.visual_report freeze-measurement \
  --repository-root . \
  --artifact-root artifacts/visual-report/v1a \
  --card-root eval/visual-report-v1a/review-cards \
  --output eval/visual-report-v1a/measurement-manifest-next.json

UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run python -m video_evidence_agent.visual_report evaluate \
  --measurement-manifest eval/visual-report-v1a/measurement-manifest-v2.json \
  --output-root artifacts/visual-report/v1a/evaluation
```

The output path must be new for each revision; the command refuses to overwrite
an existing frozen manifest. The checked-in current revision is
`measurement-manifest-v2.json`.

The current provider admission is `BLOCKED_CONFIGURATION`: a credential is
present but `VISUAL_REPORT_MODEL` is not configured. The six declared attempts
were still executed as foreground CLI attempts and retained as failed
`CONFIGURATION_ERROR` runs with `provider_calls/model_calls=0/0`. No fallback
model was used and no quality score was fabricated. The aggregate therefore
reports `measurement_valid=false` and
`conclusion=BLOCKED_PROVIDER_CONFIGURATION`; the Owner must supply an explicit
model and authorize a new complete measurement revision before any external
model call is admissible.

Human rubric files are generated under each evaluation revision's `rubrics/`
directory. They remain `PENDING_OWNER_REVIEW` until the Owner or designated
reviewer records source-linked scores. `RENDERED` is execution success only;
it is never `OWNER_ACCEPTED`.
