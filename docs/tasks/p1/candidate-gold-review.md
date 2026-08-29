# P1 TASK-P1-010 Candidate / Gold Owner Review

- Task: `TASK-P1-010`
- Review state: `PENDING_OWNER_CONFIRMATION`
- Draft: `eval/p1/revisions/p1-candidate-draft-r1/candidate-draft.json`
- Draft SHA-256: `e7dc08dc78881e0c35262635460e297c8f0347facaebaca7f919b355e8346567`
- Failure-taxonomy source: `docs/tasks/p0b-r2/failure-analysis.md`
- Failure-taxonomy SHA-256: `c3fd2982c1118c659015e52a595b7040f9c640fe129c895dd83ffb73d5fff750`
- Frozen P0 question set SHA-256: `c82990972d75776a2758373fd78afdd5ccb8651cfcb780041b5925e07dc485a0`
- Provider calls: `0`; B1 Headroom run: `false`; B2 design: `false`.

## Owner action required

Before `ART-P1-002 CandidateManifest` can be frozen, Owner must explicitly accept or
reject each candidate, confirm the exact Gold evidence units/answer points, and confirm
that accepted questions are not duplicates of the existing 12-question regression set.
The existing `p0b-r1-rlinf-m` remains one fixed hard case and must not be copied or
double-counted. No B1 Headroom run or B2 prompt/tool design is allowed before this review.

## Candidate inventory

| candidate | video | type | historical failure basis | distinctness risk | proposed decision |
| --- | --- | --- | --- | --- | --- |
| `p1-c01-kling-creative-001` | `p0b-kling-2024` | `SINGLE_PARAPHRASE` | `p0b-r1-kling-p` retrieval/answering mismatch | medium: same evidence area, narrower target | PENDING |
| `p1-c02-kling-signal-quality-001` | `p0b-kling-2024` | `SINGLE_PARAPHRASE` | `p0b-r1-kling-m` multi-clause retrieval imbalance | medium: related technical section | PENDING |
| `p1-c03-rlinf-simulation-001` | `p0b-rlinf-2026` | `SINGLE_PARAPHRASE` | `p0b-r1-rlinf-m` multi-evidence imbalance | low: simulation-only scope | PENDING |
| `p1-c04-rlinf-real-system-001` | `p0b-rlinf-2026` | `MULTI_EVIDENCE` | `p0b-r1-rlinf-m` multi-evidence omission | high: correlated with fixed hard case | PENDING |

All four drafts are `answerable=true`, use one video, have new IDs, and do not embed
transcript text. The draft contains no unanswerable candidate: the canonical P1 input
contract requires `answerable=true`; historical unanswerable refusal failures remain
failure taxonomy evidence, not a new candidate population.

## Proposed candidate and Gold mapping

### `p1-c01-kling-creative-001`

Question: 如果不受现实拍摄条件限制，视频生成可以为内容创作带来怎样的空间？

Proposed answer point: 视频生成的内容自由度高，可以呈现现实世界中不存在的概念组合或想象场景。

| Gold unit | interval | source segment(s) |
| --- | --- | --- |
| `p1-c01-kling-creative-001-u1` | `328500..373500` | `p0b-kling-2024-seg-007` |

Source snapshot: `artifacts/p0b-ingest/p0b-kling-2024/segments.jsonl`, SHA-256
`c350e1c6a69ca13ae0349061dfa1436782704ef737a9a28092504b18eb75010b`.

### `p1-c02-kling-signal-quality-001`

Question: 可灵处理视频信号时，怎样在降低计算负担的同时保持生成画质？

Proposed answer points:

1. 在原始像素空间处理视频的计算代价很高，因此采用 3D VAE 在隐空间高效压缩视频信号。
2. 压缩结构既要减少信息和计算损耗，又要保持足够的信息、生成能力与画质。

| Gold unit | interval | source segment(s) |
| --- | --- | --- |
| `p1-c02-kling-signal-quality-001-u1` | `1237400..1330200` | `p0b-kling-2024-seg-026`, `p0b-kling-2024-seg-027` |

Source snapshot: `artifacts/p0b-ingest/p0b-kling-2024/segments.jsonl`, SHA-256
`c350e1c6a69ca13ae0349061dfa1436782704ef737a9a28092504b18eb75010b`.

### `p1-c03-rlinf-simulation-001`

Question: 在具身智能的仿真强化学习中，仿真器需要满足哪些视觉和计算方面的要求？

Proposed answer points:

1. 仿真器需要高保真的图像渲染能力，以保证视觉层面的仿真质量。
2. 仿真器需要较高速的科学计算能力来模拟碰撞等过程，并通常使用 GPU 并行计算。

| Gold unit | interval | source segment(s) |
| --- | --- | --- |
| `p1-c03-rlinf-simulation-001-u1` | `420800..466500` | `p0b-rlinf-2026-seg-009` |

Source snapshot: `artifacts/p0b-ingest/p0b-rlinf-2026/segments.jsonl`, SHA-256
`d284cb127b4cdd2c56d556cdf80c8c77754b6e2bdec7a51bb6565976de1ae9c0`.

### `p1-c04-rlinf-real-system-001`

Question: 真机强化学习中的端云系统和人在环分别要解决什么问题？

Proposed answer points:

1. 端侧负责推理、云侧负责训练，需要解决端云通信、权重同步和资源协调。
2. 真实机器昂贵且探索有风险，因此需要人在环来保护机器并提高探索效率。

| Gold unit | interval | source segment(s) |
| --- | --- | --- |
| `p1-c04-rlinf-real-system-001-u1` | `466600..512800` | `p0b-rlinf-2026-seg-010` |
| `p1-c04-rlinf-real-system-001-u2` | `512800..558200` | `p0b-rlinf-2026-seg-011` |

Source snapshot: `artifacts/p0b-ingest/p0b-rlinf-2026/segments.jsonl`, SHA-256
`d284cb127b4cdd2c56d556cdf80c8c77754b6e2bdec7a51bb6565976de1ae9c0`.

## Hashes and validation

| candidate | draft content SHA-256 |
| --- | --- |
| `p1-c01-kling-creative-001` | `2989fff6b3d567f86a1527e9744ee177f7ec873b4e43dc3836084376f4d93c38` |
| `p1-c02-kling-signal-quality-001` | `c6c60350781693fd7d894097c72516bf0f7da37afc291835238740712ded035f` |
| `p1-c03-rlinf-simulation-001` | `fe1aa02097609c7d8b6236b6400588fef2528881aa8d05ec6a00c2a3f31ea482` |
| `p1-c04-rlinf-real-system-001` | `3074b79fd1f1f5f51ee5a2d00eb9293d19349f6accb388f40ff9b173de8c256a` |

The draft validator confirmed: candidate count `4/4` within the `1..4` limit; unique
new IDs; one video per candidate; `answerable=true`; source segment IDs and Gold
intervals resolve against the frozen P0 segment snapshots; no embedded transcript text;
and no provider call. This is validation of a draft, not Owner semantic approval or
Headroom evidence.

## Mandatory pause

State: `WAITING_CANDIDATE_GOLD_OWNER_FREEZE`.

Do not freeze `ART-P1-002`, run current B1, calculate Headroom, create B2 tools/prompts,
or enter any later task until Owner responds with the accepted candidate IDs and confirmed
Gold mappings. If Owner changes any question or Gold mapping, retain this draft and issue
a new draft revision; do not overwrite this evidence.
