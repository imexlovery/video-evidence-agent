# P0-B implementation report

- 状态：`CLOSED_OWNER_REVIEWED_RETRIEVAL_THRESHOLDS_NOT_MET`
- 评估 revision：计划冻结为 `p0b-r1`
- 正式方法：`TRANSCRIPT_RETRIEVAL`
- 风险等级：G1 离线评估
- 结论边界：`p0b-r1` 已冻结、完成 12 次 DeepSeek 调用，并由 owner 确认
  审核 12 条材料；检索门槛未达标，因此本报告不构成 P0-B 质量通过结论。

## 本次范围迁移

原直接视频路径已由 owner 确认废止并标记为 `SUPERSEDED`。当前有效范围
只有本地媒体、FFmpeg/中文 `mlx-whisper`、127 个带时间戳
`VideoSegment`、character 2–4 gram TF-IDF Top-5、DeepSeek 文本回答、
本地 Evidence Gate 和人工确认 Gold。项目不上传视频，也没有单独的视频
provider、模型或密钥配置。

历史 `docs/requirements/p0b/decision-evidence.jsonl` 未被改写；范围修订
以追加的 owner 决策记录保存。

## 已完成施工

- Schema 只保留 `EvaluationMethod.TRANSCRIPT_RETRIEVAL`，并移除直接视频
  输出结构。
- `p0b-freeze` 只冻结一份 DeepSeek answer prompt，并在冻结前校验三条
  媒体的哈希/时长、三份 ingest 快照、127 个 segment 以及 Gold segment
  ID/时间映射。
- `p0b-run` 只建立一个 `transcript-retrieval/<question_id>` 结果槽；每题
  在唯一回答调用前持久化自己的 `retrieval.json`。
- 结果保留回答/拒答状态、schema、引用来源回填、时间重叠、失败类型、
  延迟和可获得的 token usage；不会把程序化引用合法性当作语义正确性。
- `p0b-grade` 生成自动指标和逐题审核材料；owner 查看 12 条材料后，明确
  授权 Codex 按冻结 rubric 写入逐题语义布尔值。
- 未进入 Dense/Hybrid/Reranker、OCR/VLM、Agent、FastAPI、数据库或 P1。

## 已知正式输入证据

| 输入 | 结果 |
| --- | --- |
| `eval/p0b/corpus.jsonl` | 3 条 owner-confirmed 视频记录 |
| `eval/p0b/questions.jsonl` | 12 条 owner-confirmed 问题 |
| `eval/p0b/gold.jsonl` | 12 条 owner-confirmed Gold |
| `artifacts/p0b-ingest/` | 43 + 46 + 38 = 127 个真实 timestamped segments |

冻结前检查通过：22 个 pytest、Ruff、JSONL 严格校验、`git diff --check`、三条
媒体哈希/时长、三份 ingest 快照、127 个 segment 和全部 Gold segment ID/时间
映射均通过。随后 `p0b-r1` 已冻结，manifest 记录 corpus/questions/Gold、
prompt、源码和媒体哈希。

正式运行完成 12/12 次 DeepSeek 文本调用；12/12 有 retrieval artifact 且
12/12 schema 合规。自动评分见 [`reports/p0b-retrieval-eval.md`](p0b-retrieval-eval.md)，
逐题审核材料见 `artifacts/p0b/p0b-r1/human-review.json` 和 `.jsonl`。owner
已审核 Answer/Evidence/Quote/Points，并明确授权 Codex 依据冻结 rubric 判断后
写入全部逐题字段。派生语义结果为：answer-point coverage 均值 `0.685185`，
可回答题 `fully_correct` 为 `5/9`、`fully_supported` 为 `5/9`、
`semantic_support` 为 `8/9`；正确拒答为 `2/3`。程序化 provenance 仍只表示
引用来自当前 Top-5，没有被冒充为语义支持。

主要语义缺口是：一题漏掉“内容自由度”，一题对可回答问题拒答，一题发布日期
只答到月份，一题漏掉真机训练的人在环约束；另有一题虽正确说明“未披露”，但
没有按冻结的不可回答题契约输出 `INSUFFICIENT_EVIDENCE`。

## 停止点

自动评分、owner 材料审核和逐题语义标注均已完成。六项冻结门槛中仅正确拒答
与 citation provenance 两项通过；QuestionHit@1、QuestionHit@5、
AllEvidence@5 和 fully-supported-answer 四项未通过。因此 P0-B 以
`CLOSED_OWNER_REVIEWED_RETRIEVAL_THRESHOLDS_NOT_MET` 收口，不标记为
`PASSED`，也不开始后续阶段。
