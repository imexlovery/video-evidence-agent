# P0-B Transcript Retrieval Evaluation Report

- eval_revision: `p0b-r2`
- evaluation_method: `TRANSCRIPT_RETRIEVAL`
- evaluation_status: `BLOCKED_EXECUTION_FAILURE`
- human_review_status: `PENDING_OWNER_SEMANTIC_REVIEW`
- recommendation: `P0B_BLOCKED_EXECUTION_FAILURE`

## Scope and evidence boundary

The formal chain is three local Chinese technical videos, local FFmpeg and MLX Whisper Chinese ASR, 127 timestamped VideoSegments, character 2–4 gram TF-IDF Top-5, and one DeepSeek text answer call per question. No video is uploaded to an answer provider.
The answer model receives only the question and its current Top-5 segments. Gold, full transcripts, and answer points are excluded from that call.
Retrieval, deterministic citation provenance, timestamp overlap, schema compliance, model status, and owner semantic review are reported separately.

## Execution outcome

The single owner-authorized r2 run created 12/12 retrieval files before the
answer attempts and 12/12 result slots. All 12 DeepSeek attempts failed with
`provider / APIConnectionError`; no raw provider response or token usage was
available. The failure artifacts were preserved without retry or overwrite.
Consequently, answer/refusal quality, schema compliance, citation validity,
latency, and semantic support are not evaluable in this revision. The report is
closed as `P0B_BLOCKED_EXECUTION_FAILURE`, not `P0B_R2_PASSED`.

## Overall metrics

| method | results | QuestionHit@1 | QuestionHit@5 | Gold evidence-unit recall@5 | AllEvidence@5 (multi) | MRR | answer/refusal accuracy | correct refusal | provenance invalid | schema failures | mean latency ms |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TRANSCRIPT_RETRIEVAL | 12 | 6/9 | 9/9 | 0.963 | 2/3 | 0.8056 | 0/12 | 0/3 | N/A | 12/12 | 0.0 |

Token usage (provider-reported, if available): {"available": false, "rows_with_usage": 0, "totals": {}}

## Deterministic checks

| check | result |
| --- | --- |
| question_hit_at_1_at_least_6_of_9 | PASS |
| question_hit_at_5_at_least_8_of_9 | PASS |
| multi_all_evidence_at_5_at_least_2_of_3 | PASS |
| fully_supported_answer_at_least_7_of_9 | FAIL |
| correct_refusal_at_least_2_of_3 | FAIL |
| invalid_citation_provenance_is_zero | PASS |

Additional deterministic metrics: temporal citation hit `0/9`, schema compliance `0/12`, mean retrieval latency `0.0 ms`.

## Per-video and question-type slices

| slice | QuestionHit@5 | AllEvidence@5 | answer/refusal accuracy | correct refusal | fully supported (owner) | schema failures |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| video `p0b-kling-2024` | 3/3 | 1/1 | 0/4 | 0/1 | 0/3 | 4/4 |
| video `p0b-rlinf-2026` | 3/3 | 0/1 | 0/4 | 0/1 | 0/3 | 4/4 |
| video `p0b-wuyi-goals` | 3/3 | 1/1 | 0/4 | 0/1 | 0/3 | 4/4 |
| type `SINGLE_LEXICAL` | 3/3 | N/A | 0/3 | N/A | 0/3 | 3/3 |
| type `SINGLE_PARAPHRASE` | 3/3 | N/A | 0/3 | N/A | 0/3 | 3/3 |
| type `MULTI_EVIDENCE` | 3/3 | 2/3 | 0/3 | N/A | 0/3 | 3/3 |
| type `UNANSWERABLE` | N/A | N/A | 0/3 | 0/3 | N/A | 3/3 |

## Per-question audit trail

| video | question | type | call | answer status | answer/refusal | hit@1 | hit@5 | temporal citation | provenance | schema | owner review | failure |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| p0b-kling-2024 | p0b-r1-kling-l | SINGLE_LEXICAL | FAILED | None | False | True | True | False | False | False | None | provider |
| p0b-kling-2024 | p0b-r1-kling-p | SINGLE_PARAPHRASE | FAILED | None | False | True | True | False | False | False | None | provider |
| p0b-kling-2024 | p0b-r1-kling-m | MULTI_EVIDENCE | FAILED | None | False | True | True | False | False | False | None | provider |
| p0b-kling-2024 | p0b-r1-kling-u | UNANSWERABLE | FAILED | None | False | None | None | None | False | False | None | provider |
| p0b-rlinf-2026 | p0b-r1-rlinf-l | SINGLE_LEXICAL | FAILED | None | False | True | True | False | False | False | None | provider |
| p0b-rlinf-2026 | p0b-r1-rlinf-p | SINGLE_PARAPHRASE | FAILED | None | False | False | True | False | False | False | None | provider |
| p0b-rlinf-2026 | p0b-r1-rlinf-m | MULTI_EVIDENCE | FAILED | None | False | True | True | False | False | False | None | provider |
| p0b-rlinf-2026 | p0b-r1-rlinf-u | UNANSWERABLE | FAILED | None | False | None | None | None | False | False | None | provider |
| p0b-wuyi-goals | p0b-r1-wuyi-l | SINGLE_LEXICAL | FAILED | None | False | False | True | False | False | False | None | provider |
| p0b-wuyi-goals | p0b-r1-wuyi-p | SINGLE_PARAPHRASE | FAILED | None | False | True | True | False | False | False | None | provider |
| p0b-wuyi-goals | p0b-r1-wuyi-m | MULTI_EVIDENCE | FAILED | None | False | False | True | False | False | False | None | provider |
| p0b-wuyi-goals | p0b-r1-wuyi-u | UNANSWERABLE | FAILED | None | False | None | None | None | False | False | None | provider |

## Human review boundary

`human-review.json` and `human-review.jsonl` contain one row per question with the model answer, program-restored evidence, Gold answer points, and Gold evidence units. The owner must fill `review` fields.
`citation_provenance_verified` only means that the cited ID, quote, and timestamps came from this question's Top-5. It is not semantic correctness or evidence support.

## Decision boundary

Current recommendation: `P0B_BLOCKED_EXECUTION_FAILURE`.
P0-B is not declared PASSED before owner semantic review. No Dense, Hybrid, Reranker, OCR, VLM, Agent, Web/API, database, or P1 work is authorized by this report.
