# P0-B Transcript Retrieval Evaluation Report

- eval_revision: `p0b-r1`
- evaluation_method: `TRANSCRIPT_RETRIEVAL`
- evaluation_status: `OWNER_REVIEW_COMPLETE`
- human_review_status: `COMPLETED`
- recommendation: `P0B_RETRIEVAL_THRESHOLDS_NOT_MET`

## Scope and evidence boundary

The formal chain is three local Chinese technical videos, local FFmpeg and MLX Whisper Chinese ASR, 127 timestamped VideoSegments, character 2–4 gram TF-IDF Top-5, and one DeepSeek text answer call per question. No video is uploaded to an answer provider.
The answer model receives only the question and its current Top-5 segments. Gold, full transcripts, and answer points are excluded from that call.
Retrieval, deterministic citation provenance, timestamp overlap, schema compliance, model status, and owner semantic review are reported separately.

## Overall metrics

| method | results | QuestionHit@1 | QuestionHit@5 | Gold evidence-unit recall@5 | AllEvidence@5 (multi) | MRR | answer/refusal accuracy | correct refusal | provenance invalid | schema failures | mean latency ms |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TRANSCRIPT_RETRIEVAL | 12 | 2/9 | 7/9 | 0.6481 | 1/3 | 0.4352 | 10/12 | 2/3 | 0/9 | 0/12 | 3645.0833 |

Token usage (provider-reported, if available): {"available": true, "rows_with_usage": 12, "totals": {"completion_tokens": 4578, "prompt_tokens": 16754, "total_tokens": 21332, "prompt_cache_hit_tokens": 3840, "prompt_cache_miss_tokens": 12914}}

## Deterministic checks

| check | result |
| --- | --- |
| question_hit_at_1_at_least_6_of_9 | FAIL |
| question_hit_at_5_at_least_8_of_9 | FAIL |
| multi_all_evidence_at_5_at_least_2_of_3 | FAIL |
| fully_supported_answer_at_least_7_of_9 | FAIL |
| correct_refusal_at_least_2_of_3 | PASS |
| invalid_citation_provenance_is_zero | PASS |

Additional deterministic metrics: temporal citation hit `6/9`, schema compliance `12/12`, mean retrieval latency `32.0833 ms`.

## Per-video and question-type slices

| slice | QuestionHit@5 | AllEvidence@5 | answer/refusal accuracy | correct refusal | fully supported (owner) | schema failures |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| video `p0b-kling-2024` | 2/3 | 0/1 | 2/4 | 0/1 | 1/3 | 0/4 |
| video `p0b-rlinf-2026` | 2/3 | 0/1 | 4/4 | 1/1 | 1/3 | 0/4 |
| video `p0b-wuyi-goals` | 3/3 | 1/1 | 4/4 | 1/1 | 3/3 | 0/4 |
| type `SINGLE_LEXICAL` | 2/3 | N/A | 3/3 | N/A | 2/3 | 0/3 |
| type `SINGLE_PARAPHRASE` | 2/3 | N/A | 3/3 | N/A | 2/3 | 0/3 |
| type `MULTI_EVIDENCE` | 3/3 | 1/3 | 2/3 | N/A | 1/3 | 0/3 |
| type `UNANSWERABLE` | N/A | N/A | 2/3 | 2/3 | N/A | 0/3 |

## Per-question audit trail

| video | question | type | call | answer status | answer/refusal | hit@1 | hit@5 | temporal citation | provenance | schema | owner review | failure |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| p0b-kling-2024 | p0b-r1-kling-l | SINGLE_LEXICAL | SUCCEEDED | ANSWERED | True | True | True | True | True | True | True |  |
| p0b-kling-2024 | p0b-r1-kling-p | SINGLE_PARAPHRASE | SUCCEEDED | ANSWERED | True | False | False | False | True | True | False |  |
| p0b-kling-2024 | p0b-r1-kling-m | MULTI_EVIDENCE | SUCCEEDED | INSUFFICIENT_EVIDENCE | False | False | True | False | True | True | False |  |
| p0b-kling-2024 | p0b-r1-kling-u | UNANSWERABLE | SUCCEEDED | ANSWERED | False | None | None | None | True | True | False |  |
| p0b-rlinf-2026 | p0b-r1-rlinf-l | SINGLE_LEXICAL | SUCCEEDED | ANSWERED | True | False | False | False | True | True | False |  |
| p0b-rlinf-2026 | p0b-r1-rlinf-p | SINGLE_PARAPHRASE | SUCCEEDED | ANSWERED | True | False | True | True | True | True | True |  |
| p0b-rlinf-2026 | p0b-r1-rlinf-m | MULTI_EVIDENCE | SUCCEEDED | ANSWERED | True | False | True | True | True | True | False |  |
| p0b-rlinf-2026 | p0b-r1-rlinf-u | UNANSWERABLE | SUCCEEDED | INSUFFICIENT_EVIDENCE | True | None | None | None | True | True | False |  |
| p0b-wuyi-goals | p0b-r1-wuyi-l | SINGLE_LEXICAL | SUCCEEDED | ANSWERED | True | False | True | True | True | True | True |  |
| p0b-wuyi-goals | p0b-r1-wuyi-p | SINGLE_PARAPHRASE | SUCCEEDED | ANSWERED | True | True | True | True | True | True | True |  |
| p0b-wuyi-goals | p0b-r1-wuyi-m | MULTI_EVIDENCE | SUCCEEDED | ANSWERED | True | False | True | True | True | True | True |  |
| p0b-wuyi-goals | p0b-r1-wuyi-u | UNANSWERABLE | SUCCEEDED | INSUFFICIENT_EVIDENCE | True | None | None | None | True | True | False |  |

## Human review boundary

The owner reviewed all 12 rows across Answer, Evidence, Quote, and Points, then
explicitly authorized Codex to record the per-row semantic booleans. The labels
are preserved in `human-review.json` and `human-review.jsonl`; raw model outputs
and frozen inputs were not changed.

| human semantic metric | result |
| --- | ---: |
| answer-point coverage mean | 0.6852 |
| fully correct (answerable) | 5/9 |
| fully supported (answerable) | 5/9 |
| semantic support (answerable) | 8/9 |

Correct refusals are scored separately (`2/3`). Evidence-support fields for a
correct refusal with no emitted answer or citation are treated as not applicable
and do not enter the nine-answerable-question semantic denominator.
`citation_provenance_verified` only means that the cited ID, quote, and timestamps came from this question's Top-5. It is not semantic correctness or evidence support.

## Decision boundary

Current recommendation: `P0B_RETRIEVAL_THRESHOLDS_NOT_MET`.
Human semantic review is complete, but P0-B is not declared `PASSED`: four of
the six frozen threshold checks failed. No Dense, Hybrid, Reranker, OCR, VLM,
Agent, Web/API, database, or P1 work is authorized by this report.
