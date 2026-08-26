# P0-B Transcript Retrieval Evaluation Report

- eval_revision: `p0b-r3`
- evaluation_method: `TRANSCRIPT_RETRIEVAL`
- evaluation_status: `OWNER_REVIEW_COMPLETE`
- human_review_status: `COMPLETED`
- recommendation: `READY_FOR_OWNER_P0B_DECISION`
- owner_final_decision: `P0B_PASSED_OWNER_ACCEPTED`
- final_status: `P0B_PASSED_OWNER_ACCEPTED`

## Scope and evidence boundary

The formal chain is three local Chinese technical videos, local FFmpeg and MLX Whisper Chinese ASR, 127 timestamped VideoSegments, character 2–4 gram TF-IDF Top-5, and one DeepSeek text answer call per question. No video is uploaded to an answer provider.
The answer model receives only the question and its current Top-5 segments. Gold, full transcripts, and answer points are excluded from that call.
Retrieval, deterministic citation provenance, timestamp overlap, schema compliance, model status, and owner semantic review are reported separately.

## Overall metrics

| method | results | QuestionHit@1 | QuestionHit@5 | Gold evidence-unit recall@5 | AllEvidence@5 (multi) | MRR | answer/refusal accuracy | correct refusal | provenance invalid | schema failures | mean latency ms |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TRANSCRIPT_RETRIEVAL | 12 | 6/9 | 9/9 | 0.963 | 2/3 | 0.8056 | 11/12 | 2/3 | 0/10 | 0/12 | 4799.5833 |

Token usage (provider-reported, if available): {"available": true, "rows_with_usage": 12, "totals": {"completion_tokens": 6041, "prompt_tokens": 17817, "total_tokens": 23858, "prompt_cache_hit_tokens": 5120, "prompt_cache_miss_tokens": 12697}}

## Deterministic checks

| check | result |
| --- | --- |
| question_hit_at_1_at_least_6_of_9 | PASS |
| question_hit_at_5_at_least_8_of_9 | PASS |
| multi_all_evidence_at_5_at_least_2_of_3 | PASS |
| fully_supported_answer_at_least_7_of_9 | PASS |
| correct_refusal_at_least_2_of_3 | PASS |
| invalid_citation_provenance_is_zero | PASS |

Additional deterministic metrics: temporal citation hit `9/9`, schema compliance `12/12`, mean retrieval latency `34.5833 ms`. 

## Per-video and question-type slices

| slice | QuestionHit@5 | AllEvidence@5 | answer/refusal accuracy | correct refusal | fully supported (owner) | schema failures |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| video `p0b-kling-2024` | 3/3 | 1/1 | 3/4 | 0/1 | 3/3 | 0/4 |
| video `p0b-rlinf-2026` | 3/3 | 0/1 | 4/4 | 1/1 | 3/3 | 0/4 |
| video `p0b-wuyi-goals` | 3/3 | 1/1 | 4/4 | 1/1 | 3/3 | 0/4 |
| type `SINGLE_LEXICAL` | 3/3 | N/A | 3/3 | N/A | 3/3 | 0/3 |
| type `SINGLE_PARAPHRASE` | 3/3 | N/A | 3/3 | N/A | 3/3 | 0/3 |
| type `MULTI_EVIDENCE` | 3/3 | 2/3 | 3/3 | N/A | 3/3 | 0/3 |
| type `UNANSWERABLE` | N/A | N/A | 2/3 | 2/3 | N/A | 0/3 |

## Per-question audit trail

| video | question | type | call | answer status | answer/refusal | hit@1 | hit@5 | temporal citation | provenance | schema | owner review | failure |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| p0b-kling-2024 | p0b-r1-kling-l | SINGLE_LEXICAL | SUCCEEDED | ANSWERED | True | True | True | True | True | True | True |  |
| p0b-kling-2024 | p0b-r1-kling-p | SINGLE_PARAPHRASE | SUCCEEDED | ANSWERED | True | True | True | True | True | True | True |  |
| p0b-kling-2024 | p0b-r1-kling-m | MULTI_EVIDENCE | SUCCEEDED | ANSWERED | True | True | True | True | True | True | True |  |
| p0b-kling-2024 | p0b-r1-kling-u | UNANSWERABLE | SUCCEEDED | ANSWERED | False | None | None | None | True | True | False |  |
| p0b-rlinf-2026 | p0b-r1-rlinf-l | SINGLE_LEXICAL | SUCCEEDED | ANSWERED | True | True | True | True | True | True | True |  |
| p0b-rlinf-2026 | p0b-r1-rlinf-p | SINGLE_PARAPHRASE | SUCCEEDED | ANSWERED | True | False | True | True | True | True | True |  |
| p0b-rlinf-2026 | p0b-r1-rlinf-m | MULTI_EVIDENCE | SUCCEEDED | ANSWERED | True | True | True | True | True | True | True |  |
| p0b-rlinf-2026 | p0b-r1-rlinf-u | UNANSWERABLE | SUCCEEDED | INSUFFICIENT_EVIDENCE | True | None | None | None | True | True | False |  |
| p0b-wuyi-goals | p0b-r1-wuyi-l | SINGLE_LEXICAL | SUCCEEDED | ANSWERED | True | False | True | True | True | True | True |  |
| p0b-wuyi-goals | p0b-r1-wuyi-p | SINGLE_PARAPHRASE | SUCCEEDED | ANSWERED | True | True | True | True | True | True | True |  |
| p0b-wuyi-goals | p0b-r1-wuyi-m | MULTI_EVIDENCE | SUCCEEDED | ANSWERED | True | False | True | True | True | True | True |  |
| p0b-wuyi-goals | p0b-r1-wuyi-u | UNANSWERABLE | SUCCEEDED | INSUFFICIENT_EVIDENCE | True | None | None | None | True | True | False |  |

## Human review boundary

`human-review.json` and `human-review.jsonl` contain one completed row per question with the model answer, program-restored evidence, Gold answer points, Gold evidence units, and owner-authorized semantic labels. The owner reviewed the presented R3 material and explicitly delegated final per-row labeling to Codex before those fields were written.
`citation_provenance_verified` only means that the cited ID, quote, and timestamps came from this question's Top-5. It is not semantic correctness or evidence support.

## Limitations

- R2 and R3 use the same fixed 12-question regression set revised after R1 failures; this is not a fresh independent evaluation set.
- There is no unseen-video holdout, so cross-video generalization has not been established.
- The owner superseded the B0 direct-multimodal baseline; this run is not a B0-versus-B1 architecture comparison.
- The evaluated capability is limited to Chinese transcript evidence retrieval.
- OCR, VLM, Agent, LangGraph, Web/API, concurrency, and production reliability were not evaluated.
- Valid citation provenance does not automatically establish semantic support; those judgments remain separately human-reviewed.
- Passing this small G1 gate is not a production, commercial, or statistical-significance conclusion.

## Decision boundary

Current recommendation: `READY_FOR_OWNER_P0B_DECISION`.
Owner final decision: `P0B_PASSED_OWNER_ACCEPTED`.
P0-B is accepted by the owner for this scoped evaluation. No Dense, Hybrid, Reranker, OCR, VLM, Agent, Web/API, database, or P1 work is authorized by this report.
