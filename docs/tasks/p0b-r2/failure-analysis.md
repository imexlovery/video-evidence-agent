# P0-B R2 r1 失败分析

状态：`DEVELOPMENT_ANALYSIS_ONLY`。本文只解释 `p0b-r1` 的失败，不改变 r1
的任何输入、结果、人工标签或报告，也不作为新的评测结果。

## 1. r1 结论

正式链路本身已运行完成：3 个视频、127 个 `VideoSegment`、12 个 DeepSeek
文本调用、12 个 retrieval artifact、引用回填和自动评分均存在。质量门槛未达标：

- `QuestionHit@1 = 2/9`，目标 `6/9`；
- `QuestionHit@5 = 7/9`，目标 `8/9`；
- `AllEvidence@5 = 1/3`，目标 `2/3`；
- `FullySupportedAnswer = 5/9`，目标 `7/9`；
- `CorrectRefusal = 2/3`、invalid citation provenance `= 0/9`，已达标。

## 2. 逐题证据分析

| 题目 | r1 观察 | 主要类别 | r2 允许的通用处理 |
| --- | --- | --- | --- |
| `p0b-r1-kling-l` | Top-1 命中；答案正确。ASR 将 `720P` 识别成 `720MHz`，属于已人工识别的 ASR 词形问题。 | ASR（非检索阻塞） | 不改 ASR；答案 prompt 不得把明显 ASR 单位误识别扩写成新事实。 |
| `p0b-r1-kling-p` | Gold 在 `seg-007`，Top-5 未召回；答案只覆盖降低门槛，漏掉内容自由度。 | RETRIEVAL + ANSWERING | 用通用问题规范化/词面分数聚合改善“创作优势/自由度/想象场景”类改写；回答只输出 Top-5 支持内容。 |
| `p0b-r1-kling-m` | Top-5 只覆盖多证据 Gold 的一部分（`seg-028`），模型直接拒答。 | RETRIEVAL + REFUSAL | 多子句问题的确定性分数聚合；证据不足时拒答，不能把部分召回伪装成完整回答。 |
| `p0b-r1-kling-u` | 引用内容支持“未披露”，但返回 `ANSWERED`，不是规定的 `INSUFFICIENT_EVIDENCE`。 | REFUSAL | 在 r2 prompt 明确“确切值未披露/不方便透露”必须使用拒答结构。 |
| `p0b-r1-rlinf-l` | Top-1 只落在“2025 年 9 月”的后文，未把包含“9 月 1 日”的 `seg-013` 排入 Top-5；答案缺少日期。 | RETRIEVAL + ANSWERING | 通用日期/版本号词形保留与查询分数聚合；不得为该 question ID 写特例。 |
| `p0b-r1-rlinf-p` | Gold 证据跨 `seg-004/005`；首段因 50% 覆盖规则略低于命中线，后段在 Top-5。答案语义完整。 | SEGMENTATION/BOUNDARY | 保持 Gold 与 segment 不变；测试边界行为，不降低命中规则，不用人工调区间。 |
| `p0b-r1-rlinf-m` | Top-5 集中在仿真/云边端部分，遗漏“人在环” Gold unit；答案也漏该要点。 | RETRIEVAL + ANSWERING | 对多子句问题保留不同语义子部分的候选；回答必须覆盖所有实际召回且有依据的要点，不能补全缺失部分。 |
| `p0b-r1-rlinf-u` | 正确返回 `INSUFFICIENT_EVIDENCE`。 | — | 作为拒答回归样例，必须保持。 |
| `p0b-r1-wuyi-l` | Gold 在 Top-5，但邻近前一段排名第一；答案正确。 | RANKING/BOUNDARY | 通用排序处理可改善相邻 segment 的证据优先级；不可改变 Top-5 或 Gold。 |
| `p0b-r1-wuyi-p` | Top-1 命中，答案完整且有支持。 | — | 作为正向回归样例，必须保持。 |
| `p0b-r1-wuyi-m` | 多证据 Gold 全部进入 Top-5，答案完整且有支持。 | — | 作为多证据正向回归样例，必须保持。 |
| `p0b-r1-wuyi-u` | 正确返回 `INSUFFICIENT_EVIDENCE`。 | — | 作为拒答回归样例，必须保持。 |

## 3. 允许的最小改进假设

### H1：问题词形与证据词形不一致

中文改写、英文术语、大小写、标点和 ASR 口语词会让 character n-gram 重合度
下降。可以验证通用规范化、同题内部的多子句分数聚合是否改善 Top-1/Top-5，
但规则不得读取 Gold，也不得维护 question-specific 词表。

### H2：单一总分会把多个子问题压成一个主题

`MULTI_EVIDENCE` 问题需要多个语义子部分。允许把一个问题确定性拆成有限子句，
对同一段的分数做通用聚合，再选择 5 个原始 segment；不可借此增加上下文数量或
引入第二阶段模型排序器。

### H3：回答契约没有把“事实未披露”视为拒答

当前引用可能证明“没有披露”，但模型仍生成自然语言 `ANSWERED`。r2 prompt
必须把“不方便说/没有确切数字/证据没有给出所问事实”映射为
`INSUFFICIENT_EVIDENCE`，并保留空答案、空 citation 的 schema。

## 4. 不允许的修复方式

- 不把 Gold segment、answer point、r1 人工标签或完整 transcript 放进运行时检索或 prompt。
- 不为失败 question ID 加关键词、分数、排名或强制 segment。
- 不改变 ASR、segment 边界、Gold 时间、题目或阈值。
- 不加入 embedding、Dense、Hybrid、Reranker、LLM Query Rewrite 或 VLM。
- 不因为某一题失败而重复调用 DeepSeek或挑选最好结果。

## 5. 验证要求

每个改进必须先由非 Gold 硬编码的单元/回归测试证明，再进入 r2 freeze。正式
r2 必须对 12 题全量运行一次，并同时保留 r1→r2 的指标对照。若 r2 仍未满足
六项门槛，关闭 r2，不自动开启下一轮。
