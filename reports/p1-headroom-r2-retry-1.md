# P1 TASK-P1-020 B1 Headroom Report

- Status: `NO_GO_INSUFFICIENT_HEADROOM`
- Source attempt: `p1-headroom-r2`
- Reporting revision: `p1-headroom-r2-retry-1`
- CandidateManifest: `eval/p1/revisions/p1-candidate-freeze-r2/candidate-manifest.json`
- CandidateManifest SHA-256: `d523c22fdfbfb8d1ff55a2d5620d94bd6cdfac5368472995f1317b857f495cf2`
- Workload: `3` cases; one current B1 retrieval per case
- Retrieval profile: `char_tfidf_2_4_query_views_v1`; Top-K `5`
- Provider calls: `0`; video upload: `false`; B2 design/execution: `false`
- Gold is scorer-only oracle context; it was not passed as runtime retrieval context.
- This retry assembles preserved outputs only; B1 was not rerun.

## Case summary

| case | answerable | B1 result | Gold hit / total | recall@5 | missing units | dynamic recoverable | qualifying |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| `p0b-r1-rlinf-m` | `True` | `PRIMARY_FAILURE` | 2/3 | `0.6666666666666666` | p0b-r1-rlinf-m-u1 | `True` | `True` |
| `p1-c02-kling-signal-quality-001` | `True` | `COMPLETE_AT_TOP_K` | 2/2 | `1.0` | — | `False` | `False` |
| `p1-c03-rlinf-simulation-001` | `True` | `COMPLETE_AT_TOP_K` | 1/1 | `1.0` | — | `False` | `False` |

## Per-case current B1 evidence

### `p0b-r1-rlinf-m`

- Question: 面向具身智能的强化学习系统为何需要同时处理仿真训练和真机训练的不同资源、通信或人工参与问题？请概括两类场景的关键约束。
- Answerable: `True`; fixed hard case: `True`
- B1 profile: `char_tfidf_2_4_query_views_v1`; retrieval calls for this case: `1`
- B1 Top-5: p0b-rlinf-2026-seg-010 (rank 1, score 0.085506746064625), p0b-rlinf-2026-seg-011 (rank 2, score 0.083591137274035), p0b-rlinf-2026-seg-032 (rank 3, score 0.034175141222227), p0b-rlinf-2026-seg-026 (rank 4, score 0.027861932640743), p0b-rlinf-2026-seg-022 (rank 5, score 0.026258567546346)
- B1 Gold units hit: `p0b-r1-rlinf-m-u2, p0b-r1-rlinf-m-u3`
- Missing Gold units: `p0b-r1-rlinf-m-u1`
- Evidence-unit recall@5: `0.6666666666666666`; `AllNecessaryEvidence@5`: `False`
- Answerable: `True`; dynamic recoverable: `True`; qualifying: `True`
- Deterministic oracle: inspect_segments，anchor=p0b-rlinf-2026-seg-010，radius=2，新增 Gold=p0b-r1-rlinf-m-u1，新增 segments=p0b-rlinf-2026-seg-008,p0b-rlinf-2026-seg-009,p0b-rlinf-2026-seg-012；scorer-only、runtime_reads_gold=false、cross_video=false。
- Case artifact: `eval/p1/revisions/p1-headroom-r2/cases/p0b-r1-rlinf-m.json`; SHA-256 `df68b88f649bef3aa69bd55a7f6729595c941587bb3cec75ea434c498c8825c1`

### `p1-c02-kling-signal-quality-001`

- Question: 可灵处理视频信号时，怎样在降低计算负担的同时保持生成画质？
- Answerable: `True`; fixed hard case: `False`
- B1 profile: `char_tfidf_2_4_query_views_v1`; retrieval calls for this case: `1`
- B1 Top-5: p0b-kling-2024-seg-027 (rank 1, score 0.059964951823976), p0b-kling-2024-seg-026 (rank 2, score 0.055442905259324), p0b-kling-2024-seg-004 (rank 3, score 0.037694072780716), p0b-kling-2024-seg-031 (rank 4, score 0.032682425647221), p0b-kling-2024-seg-002 (rank 5, score 0.032129529383787)
- B1 Gold units hit: `p1-c02-kling-signal-quality-001-u1, p1-c02-kling-signal-quality-001-u2`
- Missing Gold units: `none`
- Evidence-unit recall@5: `1.0`; `AllNecessaryEvidence@5`: `True`
- Answerable: `True`; dynamic recoverable: `False`; qualifying: `False`
- Deterministic oracle: 无可恢复缺失 Gold unit；未生成 oracle action。
- Case artifact: `eval/p1/revisions/p1-headroom-r2/cases/p1-c02-kling-signal-quality-001.json`; SHA-256 `d2b5889b91a161b46911bfcb46a197520cba1e8af39072d9433e60a17c6ba486`

### `p1-c03-rlinf-simulation-001`

- Question: 在具身智能的仿真强化学习中，仿真器需要满足哪些视觉和计算方面的要求？
- Answerable: `True`; fixed hard case: `False`
- B1 profile: `char_tfidf_2_4_query_views_v1`; retrieval calls for this case: `1`
- B1 Top-5: p0b-rlinf-2026-seg-009 (rank 1, score 0.201728356314010), p0b-rlinf-2026-seg-022 (rank 2, score 0.090591244588154), p0b-rlinf-2026-seg-000 (rank 3, score 0.048793505040347), p0b-rlinf-2026-seg-024 (rank 4, score 0.046266253265265), p0b-rlinf-2026-seg-003 (rank 5, score 0.043024676479501)
- B1 Gold units hit: `p1-c03-rlinf-simulation-001-u1`
- Missing Gold units: `none`
- Evidence-unit recall@5: `1.0`; `AllNecessaryEvidence@5`: `True`
- Answerable: `True`; dynamic recoverable: `False`; qualifying: `False`
- Deterministic oracle: 无可恢复缺失 Gold unit；未生成 oracle action。
- Case artifact: `eval/p1/revisions/p1-headroom-r2/cases/p1-c03-rlinf-simulation-001.json`; SHA-256 `3aad2e276c407abdbba99e2fd416d86ac41cc51c731da70e46541601f310f910`

## Gate decision

- Qualifying Headroom cases: `1/3`; minimum required: `2`.
- Gate result: `NO_GO_INSUFFICIENT_HEADROOM`.
- Reason: Fewer than two qualifying pre-frozen answerable current B1 primary failures have an auditable allowed-action recovery path.
- Rejected c01 and c04 remain history only and are absent from the workload and all Headroom counts.
- `TASK-P1-030` was not started. B2 was not designed, implemented, or run.
- P0 historical evidence remains unchanged. The task stops at this terminal No-Go boundary.
