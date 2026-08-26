# P0-A frozen questions

Create questions.jsonl only after a human has watched the selected real Chinese
technical video. Each JSON line must contain question_id, question,
should_answer, and expected_interval. The interval is a non-formal human review
reference expressed as [start_ms, end_ms].

Do not replace this file with synthetic questions or questions inferred solely
from a transcript; that would not satisfy Gate A.
