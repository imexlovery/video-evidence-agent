# P0-B R1 pre-freeze owner review

**状态：历史审核记录 / 已由 owner 确认 / 不作为运行结果。**

2026-08-26：项目所有者已确认来源使用范围、12 题/Gold 的视频语义和时间边界，以及可灵题的 `720P / 5 秒`。正式输入已另存为 `corpus.jsonl`、`questions.jsonl` 与 `gold.jsonl`；本审核记录保留用于审计，不再修改。

`questions.draft.jsonl` 和 `gold.draft.jsonl` 是根据三段真实视频的本地 ASR 生成的审核候选，不是人类 Gold。正式输入已由所有者明确确认，冻结命令只读取 `questions.jsonl` 和 `gold.jsonl`。

| question_id | 类型 | 审核问题 | 应回放的视频时间 | 草案预期 |
| --- | --- | --- | --- | --- |
| `p0b-r1-kling-l` | SINGLE_LEXICAL | 线上开放版本的分辨率和时长？ | 10:57–11:42 | 720P、5 秒；特别核对 ASR 将 P 误写为 MHz 的问题。 |
| `p0b-r1-kling-p` | SINGLE_PARAPHRASE | 视频生成相对摄影和渲染的核心创作优势？ | 05:29–06:14 | 内容自由度高，并降低普通创作者门槛。 |
| `p0b-r1-kling-m` | MULTI_EVIDENCE | 低成本且保质的模型与数据做法？ | 20:37–22:58 | 3D VAE/时空建模 + 数据平台、标签过滤、caption。 |
| `p0b-r1-kling-u` | UNANSWERABLE | 是否披露确切参数量？ | 29:12–30:01 | 拒绝；只说明不便透露。 |
| `p0b-r1-rlinf-l` | SINGLE_LEXICAL | v0.1 首发日期？ | 10:04–10:49 | 2025-09-01。 |
| `p0b-r1-rlinf-p` | SINGLE_PARAPHRASE | RL 相比 SFT 改善/未明显改善的泛化？ | 03:09–04:41 | 语义、执行明显提升；视觉不明显。 |
| `p0b-r1-rlinf-m` | MULTI_EVIDENCE | 仿真与真机训练的不同系统约束？ | 06:16–09:18 | 仿真器/GPU；端云通信与同步；人在环。 |
| `p0b-r1-rlinf-u` | UNANSWERABLE | 是否给出精确累计下载量？ | 全片核对 | 拒绝；无此数字。 |
| `p0b-r1-wuyi-l` | SINGLE_LEXICAL | “不知道”的奖励是多少？ | 19:29–20:59 | 0.5 分。 |
| `p0b-r1-wuyi-p` | SINGLE_PARAPHRASE | 做饭数据分布为何会导致偏见？ | 13:16–14:02 | 学到相关性的捷径而非因果。 |
| `p0b-r1-wuyi-m` | MULTI_EVIDENCE | 机器人保姆故事说明什么对齐问题？ | 23:17–25:35 | 简单目标无法穷尽复杂的人类价值。 |
| `p0b-r1-wuyi-u` | UNANSWERABLE | 是否公布研究机构年度经费？ | 全片核对 | 拒绝；无此信息。 |

## 必须由所有者完成的最小审核

1. 确认三条来源链接、归属、使用权依据与 `corpus.jsonl` 中的限制描述；若任一视频不能用于本地评测，先替换视频并重新 ingest。
2. 对表中每个时间段回放原视频，纠正 ASR 误字、问题措辞、时间边界和答案要点。至少将每条 Gold 的 `annotator_status` 改为能反映真实人工审核的状态。
3. 对三条拒答题确认“没有确切答案”而不是“问题表述模糊”或“视频给了部分数值”。
4. 确认后，将审定版本写入 `questions.jsonl` 与 `gold.jsonl`；不要覆盖本草案。之后才可执行 `video-evidence p0b-freeze`。

四项审核已完成。仍须先通过代码、输入、媒体哈希/时长和 ingest 快照校验，才能冻结并运行唯一的 `TRANSCRIPT_RETRIEVAL` 方法；自动评分后仍须由 owner 完成语义审核，才能讨论 P0-B 结论。
