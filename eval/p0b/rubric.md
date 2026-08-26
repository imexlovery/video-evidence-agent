# P0-B human review rubric

Review the one-method materials in Chinese. Each row contains one
`TRANSCRIPT_RETRIEVAL` answer, its program-restored citations, and the matching
Gold reference.

For each answerable question, mark `review.answer_point_coverage` with one
boolean per Gold answer point, then mark:

- `review.fully_correct`: every required point is covered and there is no material false
  statement;
- `review.fully_supported`: the answer is fully correct and every material conclusion
  is supported by the displayed evidence interval(s);
- `review.semantic_support`: the displayed interval(s) semantically support the answer.

For each unanswerable question, `review.fully_correct=true` only when the output is a
refusal (`INSUFFICIENT_EVIDENCE`) and does not invent the requested fact.
`citation_provenance_verified` and timestamp overlap are computed by the
program; they are not substitutes for this semantic review.

The reviewer may add a concise failure note using one primary category:
`ASR`, `SEGMENTATION`, `RETRIEVAL`, `ANSWERING`, `REFUSAL`, `PROVIDER`, or
`GOLD`. Do not edit raw model outputs or remove failed rows.
