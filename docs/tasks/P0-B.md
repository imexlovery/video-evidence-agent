# P0-B 施工任务单：中文技术视频 Retrieval Eval

> 历史状态：本文件是最初的 P0-B 设计草案，其中直接视频/B0 方案已被
> `DEC-P0B-016` 标记为 `SUPERSEDED`，不得再作为活动施工要求。已完成的正式
> r1 范围与结果以 `eval/p0b/eval-manifest.json`、
> `reports/p0b-retrieval-eval.md` 和 `docs/tasks/p0b/EVIDENCE.md` 为准；后续窄范围
> 修订任务见 `docs/tasks/P0-B-R2.md`。

| 字段 | 内容 |
|---|---|
| 任务编号 | `P0-B` |
| 发布状态 | `ISSUED` |
| 发布日期 | 2026-08-26 |
| 前置阶段 | `P0-A PASSED / OWNER_ACCEPTED` |
| 项目等级 | G1 离线评估，不是生产系统 |
| 评估规模 | 3 个中文技术视频、12 道冻结问题 |
| 对照基线 | `B0 Direct Multimodal` vs `B1 Transcript TF-IDF Retrieval` |
| 唯一目标 | 判断 transcript retrieval 是否能稳定定位时间戳证据，并相对直接多模态问答提供可证明的价值 |
| 停止点 | 发布 P0-B 锁定报告与阶段建议；不得自动进入 P1 Agent |

## 1. 发布依据

P0-A 已完成并封存，当前证据为：

- 真实中文 MP4 已跑通 FFmpeg、中文 ASR、时间戳 segment、TF-IDF Top-K、真实模型回答和 Evidence Gate。
- 4 道 Smoke 题中，3 道可回答题返回 `ANSWERED`，1 道不可回答题返回 `INSUFFICIENT_EVIDENCE`。
- 用户已确认 ASR 抽样、答案和 citation 语义支持，P0-A 报告状态为 `FINAL / PASSED`。
- 当前自动化基线：`uv run pytest` 为 18 passed；`uv run ruff check .` 通过。
- P0-A 的自然限制：视频仅 4 分 29 秒，只有 6 个 retrieval segments，不能代表长技术视频。
- P0-A 已暴露排序问题：`clm-q03-work-benefits` 的正确证据位于 03:32–03:39，而 TF-IDF Top-1 是 02:19–03:04，只在 Top-5 中覆盖正确片段。

P0-B 因此不能只统计“模型最后答对了几题”，必须独立评估：

1. 检索是否把真实证据排到前面；
2. 回答是否覆盖人工答案要点；
3. 引用是否真正支持结论；
4. 不可回答题是否正确拒答；
5. 相比直接多模态模型，retrieval 是否值得保留。

P0-A 封存文件 SHA-256：

| 文件 | SHA-256 |
|---|---|
| `reports/p0a-smoke-report.md` | `a57a15207c95f1c8217590a270cc30ce811001810f3fa6e25923953aed64ea9a` |
| `artifacts/chinese-lips-mini-val-kj-001/smoke-run.json` | `55563f08c99a709347e0715917e66028767f79b0066265ab5d5c866fbe11cf74` |
| `artifacts/chinese-lips-mini-val-kj-001/human-review.json` | `04d817974af0b73aeb39ce650ee980fe0ef6c904226c30ae147cc8dd20e23ed4` |
| `pyproject.toml` | `1b667d5de7cbc36a8c8cba0c8610c2d5acb0f36be98a7b248040b6fe4f6b6b7a` |
| `uv.lock` | `d62819c00268e64ff00d958b2cc5ebff587ed1f576c0e67e219999edb52d4851` |

以上哈希用于说明 P0-B 起点，不表示当前目录已经有 Git commit；发布时该目录仍不是 Git repository。

## 2. P0-B 要回答的问题

P0-B 只回答以下四个研究问题：

### RQ1：Retrieval 可行性

对自然连续的中文技术视频，当前 ASR + 45～60 秒 VideoSegment + character TF-IDF，能否把人工 Gold 时间段召回到 Top-1 / Top-5？

### RQ2：证据约束回答质量

当答案模型只能看到 Top-5 segments 时，能否覆盖人工答案要点、避免无证据扩写，并给出真正支持结论的引用？

### RQ3：拒答质量

当视频没有相关事实时，系统能否返回 `INSUFFICIENT_EVIDENCE`，而不是利用模型常识补全？

### RQ4：相对价值

与直接把视频交给多模态模型相比，B1 是否以可接受的答案质量提供更可靠的证据来源、更低或可解释的成本/延迟，以及可复核的检索轨迹？

## 3. 冻结范围

### 3.1 本阶段必须完成

- 选择 3 个自然连续的中文技术视频。
- 每个视频独立完成 P0-A ingest，不进行跨视频查询。
- 冻结 12 道题及人工 Gold 时间段、Gold Segment IDs、答案要点和拒答标签。
- 固定运行 B0 与 B1 两条基线。
- 独立计算 retrieval 指标和回答/引用/拒答指标。
- 保存两个基线未经修改的原始输出、延迟、token/用量和可获得的成本数据。
- 对 A/B 输出进行人工盲审或最小化基线身份影响的交叉审查。
- 形成 `reports/p0b-retrieval-eval.md`，给出阶段结论。

### 3.2 本阶段禁止施工

- Agent、Planner、Critic、LangGraph、Tool Calling 或动态 VLM 检查。
- 将 B0 直接多模态 baseline 包装成 P1 Agent 能力。
- OCR、关键帧索引、视觉摘要或画面级 enrichment。
- FastAPI、React、SSE、数据库、Redis、Worker、MQ、Checkpoint。
- 多视频联合检索或跨视频综合回答。
- 为了提高分数在锁定集上调 prompt、改问题、改 Gold 或反复挑最好结果。
- 在 P0-B R1 主结果中加入 Dense、Hybrid、Reranker、Query Rewrite。
- 将 P0-A 的短合成视频计入 P0-B 的 3 个视频或 12 道正式题。
- 自动进入 P1 或宣称 Agent 已被证明有价值。

## 4. 评估数据集契约

### 4.1 视频选择

3 个视频均须满足：

- 中文为主要口语，内容属于 AI、LLM、软件开发、系统设计或公开产品技术发布。
- 自然连续内容，不是由孤立语音片段拼接而成。
- 建议每个 20～60 分钟，总时长建议 60～150 分钟。
- 声音清晰，但允许存在真实演讲中的口头语、术语和轻微噪声。
- 主要问题能从口播回答；画面才有答案的问题不进入本阶段主评估集。
- 来源 URL、作者/发布者、许可或本地评估使用依据可记录。
- 原始媒体不得提交到仓库；仅保存哈希、元数据和可复现说明。
- 不含隐私、机密、付费受限课程或未经授权的内部视频。

三个视频应尽量覆盖不同说话风格或内容形态，例如：

- 单人技术课程；
- 开发者会议演讲；
- 产品/架构技术发布。

不能为了获得更好结果全部选择语速、术语和录音条件高度相似的视频。

### 4.2 12 道问题的固定分布

每个视频固定 4 道题：

| 类型 | 每视频 | 总数 | 目的 |
|---|---:|---:|---|
| `SINGLE_LEXICAL` | 1 | 3 | 单时间段事实题，问题和原话有一定词面重合 |
| `SINGLE_PARAPHRASE` | 1 | 3 | 单时间段事实题，使用同义改写测试 lexical retrieval |
| `MULTI_EVIDENCE` | 1 | 3 | 至少两个不相邻时间段共同支持完整答案 |
| `UNANSWERABLE` | 1 | 3 | 视频中没有所问事实，必须拒答 |

主评估人口因此为：

- 9 道可回答题；
- 3 道不可回答题；
- 6 道单证据题；
- 3 道多证据题。

问题由人根据原视频编写，不能由 B0/B1 模型根据 ASR 自动出题。`SINGLE_PARAPHRASE` 不得只是替换一个标点或复制 transcript 原句。

### 4.3 Gold Schema

Gold 与运行时输入必须物理分离；模型和 retriever 均不得读取 Gold 文件。

```json
{
  "eval_revision": "p0b-r1",
  "question_id": "p0b-v01-q02",
  "video_id": "p0b-v01",
  "question_type": "SINGLE_PARAPHRASE",
  "question": "讲者认为这种检索策略为什么更适合当前场景？",
  "should_answer": true,
  "gold_evidence_units": [
    {
      "unit_id": "e01",
      "start_ms": 632000,
      "end_ms": 659000,
      "gold_segment_ids": ["p0b-v01-seg-014"]
    }
  ],
  "answer_points": [
    "答案必须覆盖的语义要点一",
    "答案必须覆盖的语义要点二"
  ],
  "unanswerable_rationale": null,
  "annotator_status": "USER_CONFIRMED"
}
```

不可回答题必须满足：

- `should_answer = false`；
- `gold_evidence_units = []`；
- `answer_points = []`；
- `unanswerable_rationale` 说明为什么确认视频没有该事实；
- 经完整 transcript 搜索和人工视频复核，而不是凭印象标注。

### 4.4 Gold 时间与 Segment ID 的关系

- 人工先依据原视频标注 Gold 时间段。
- 在 VideoSegment 切分参数冻结后，程序按时间覆盖生成候选 Gold Segment IDs。
- 人工确认候选 segment 的 transcript 是否真正包含支持内容。
- 如果改变 ASR 模型、segment 合并参数或源视频，必须生成新的 `eval_revision`；不得沿用旧 Gold Segment IDs。
- Gold 时间段是语义证据边界；Gold Segment IDs 是当前切分实现的可接受检索单元，两者都必须保存。

## 5. 评估版本与防泄漏

### 5.1 三类数据严格分开

- **开发集**：只使用已封存的 P0-A 样本调通 B0/B1 adapter、schema、grader 和报告生成。
- **锁定集**：P0-B 的 3 视频/12 题，只用于一次冻结评估。
- **后续修订集**：只有 R1 报告完成后才能创建 `p0b-r2`；不得覆盖 R1。

### 5.2 锁定清单

在运行任一 P0-B baseline 前，生成 `eval/p0b/eval-manifest.json`，至少冻结：

- `eval_revision`；
- 3 个视频的来源、媒体 SHA-256、时长与本地路径别名；
- ASR engine、模型、语言和参数；
- segment 目标/最大时长与生成文件 SHA-256；
- 12 道 questions 文件 SHA-256；
- Gold 文件 SHA-256；
- B0/B1 prompt 版本与 SHA-256；
- B0/B1 精确模型/服务版本；
- temperature、max output、Top-K 和其他运行参数；
- Python/依赖锁文件 SHA-256；
- 当前源码 Git commit；若仍没有 Git，则记录全部参与运行源码文件 SHA-256；
- 锁定人和锁定时间。

锁定之后如需改变任何以上项目，必须关闭当前 revision 并创建新 revision。

### 5.3 禁止泄漏

- B0 只能看到当前视频和问题，不能看到 ASR、Gold、答案要点或 B1 结果。
- B1 retriever 只能看到当前视频的 `segments.jsonl` 和问题。
- B1 answerer 只能看到问题和当前 Top-K，不得读取全文、Gold 或 B0 结果。
- Grader 在两条 baseline 完成后才读取 Gold。
- 人工审查前，将两条输出以稳定随机种子映射成 A/B，审查表不显示 baseline 身份。

## 6. 基线定义

### 6.1 B0：Direct Multimodal Model

**输入**

- 单个完整 MP4；
- 当前问题；
- 与 B1 对齐的中文回答、拒答和时间戳要求。

**禁止输入**

- 本地 ASR transcript；
- VideoSegments 或 retrieval results；
- Gold 时间、答案要点和人工备注。

**输出**

```json
{
  "baseline_id": "B0_DIRECT_MULTIMODAL",
  "status": "ANSWERED",
  "answer": "……",
  "evidence": [
    {
      "start_ms": 632000,
      "end_ms": 659000,
      "quote": null,
      "source_kind": "MODEL_PROPOSED_VIDEO_INTERVAL"
    }
  ]
}
```

B0 的时间段是模型提出的候选证据，不能标记成程序化 provenance verified；必须用 Gold 和人工审查验证。

### 6.2 B1：Transcript TF-IDF Retrieval

沿用 P0-A 主路径，不改变算法：

```text
MP4 → FFmpeg → mlx-whisper zh → VideoSegment
→ character 2–4 gram TF-IDF → Top-5
→ evidence-constrained answerer → deterministic Evidence Gate
```

**冻结项**

- `Top-K = 5`；
- character n-gram 范围为 2～4；
- 当前 45 秒目标/60 秒最大 segment 合并策略；
- answerer 只看 Top-5；
- citation ID 必须属于当前 Top-5；
- quote 从源 VideoSegment 程序回填。

B1 的原始 Top-K 必须在 answerer 调用前保存。回答正确不能覆盖 retrieval miss。

### 6.3 模型选择规则

- P0-B 任务单不预先声称某个具体多模态模型可用。
- 施工时先依据官方文档确认直接视频输入、时长限制、时间戳能力、地区和费用。
- 优先让 B0 与 B1 answerer 使用同一提供方、同一模型系列和相同生成参数；如果能力接口不允许，报告必须将结果标为“系统级方案比较”，不得声称是纯 retrieval ablation。
- 只允许一个冻结的 B0 模型和一个冻结的 B1 answerer 版本进入 R1。
- 模型调用失败时保存失败结果；只允许针对明确的传输错误按固定策略重试，不能为了换答案重复抽样。
- 未配置真实 B0 或 B1 provider 时显式停止，不得用 Mock 填补正式结果。
- 新增外部付费调用前记录预计调用量；若产生尚未授权的新费用，先获得用户批准。

## 7. 指标与判定规则

### 7.1 时间覆盖规则

对候选区间 `c` 和 Gold evidence unit `g`：

```text
gold_coverage(c, g) = duration(intersection(c, g)) / duration(g)
```

当 `gold_coverage >= 0.50` 时，候选区间命中该 Gold evidence unit。

采用 0.50 是为了容忍 45～60 秒粗粒度 segment 包含较短 Gold，同时排除仅在边界轻微相交的伪命中。该确定性命中还必须与人工“语义支持”分开报告。

### 7.2 B1 Retrieval 指标

只在 9 道可回答题上计算，并按视频、问题类型及 overall 分层：

- `QuestionHit@1`：Top-1 是否命中至少一个 Gold evidence unit。
- `QuestionHit@5`：Top-5 是否命中至少一个 Gold evidence unit。
- `EvidenceUnitRecall@5`：Top-5 覆盖的 Gold evidence units / 全部 Gold evidence units。
- `AllEvidence@5`：一道题的全部 Gold evidence units 是否均被 Top-5 覆盖。
- `MRR`：第一个命中 Gold evidence unit 的结果排名倒数。
- `RetrievalLatencyMs`：只记录检索耗时，不含 ASR 和 answerer。

不得用回答指标替代 retrieval 指标，也不得只报告平均分而隐藏视频或题型切片。

### 7.3 B0/B1 共同回答指标

- `AnswerPointRecall`：命中的人工答案要点 / 全部答案要点。
- `FullyCorrectAnswer`：所有必要要点均覆盖，且无实质错误陈述。
- `FullySupportedAnswer`：答案正确，且每个实质结论都被引用区间支持。
- `CitationTemporalHit`：引用区间是否命中 Gold evidence unit。
- `CorrectRefusal`：不可回答题返回 `INSUFFICIENT_EVIDENCE`。
- `FalseRefusal`：可回答题错误拒答。
- `UnsupportedAnswer`：输出答案但引用不足以支持实质结论。
- `SchemaFailure`：输出不能解析成冻结 schema。
- `EndToEndLatencyMs`、input/output token 或 provider usage、可获得的外部成本。

不使用 BLEU、ROUGE 或模型自评作为主质量指标。语义正确性与支持度由中文人工审查决定，程序只负责 schema、provenance 和时间重叠等确定性检查。

### 7.4 R1 建议决策阈值

由于样本只有 12 题，报告使用“题数/总数”，不以小样本百分比包装统计显著性。

将 B1 判断为 `RETRIEVAL_VIABLE` 的建议门槛：

- `QuestionHit@1 >= 6/9`；
- `QuestionHit@5 >= 8/9`；
- 三道 `MULTI_EVIDENCE` 中至少 `2/3` 达到 `AllEvidence@5`；
- 可回答题至少 `7/9` 达到 `FullySupportedAnswer`；
- 不可回答题至少 `2/3` 达到 `CorrectRefusal`；
- B1 citation provenance 非法数为 `0`。

将 B1 判断为相对 B0 `VALUE_SUPPORTED` 的建议门槛：

- B1 的 `FullySupportedAnswer` 数量不能比 B0 少 2 题或以上；
- B1 必须保留可读 Top-K、分数、稳定 segment ID 和程序回填 quote；
- 延迟、外部成本和失败率必须实测报告，不能只用架构推测宣称更优。

这些是 G1 小样本阶段决策线，不是生产 SLA，也不构成统计显著性结论。

## 8. 施工任务

### P0B-00：封存 P0-A 与建立 Eval Revision

**施工内容**

- 验证本任务单列出的 P0-A 核心文件哈希。
- 再次运行 P0-A 测试和静态检查，保存输出。
- 创建 `eval_revision = p0b-r1`。
- 固定源码版本：优先建立 Git baseline commit；若当前阶段暂不初始化 Git，则生成完整源码 hash manifest。

**验收**

- P0-A 原始报告和 artifacts 不被覆盖。
- P0-B 的任何代码/数据变化可与封存起点区分。

### P0B-01：选择 3 个视频并登记 Corpus

**产物**

- `eval/p0b/corpus.jsonl`
- 三个被忽略的本地媒体文件或明确的本地路径映射。

**验收**

- 三个视频均满足 4.1。
- 每个视频有来源、使用依据、时长、SHA-256、语言、内容类型和敏感性记录。
- 媒体没有进入版本控制。

### P0B-02：逐视频 Ingest 与质量检查

**施工内容**

- 对每个视频运行 FFmpeg、完整中文 ASR 和 VideoSegment 构建。
- 开始/中间/结尾各抽查至少一处 ASR。
- 记录每视频 ASR 模型、耗时、segment 数量和明显识别问题。
- 在出题前冻结 ASR 与切分产物。

**验收**

- 三个视频分别拥有合法 `manifest.json`、`asr.json`、`segments.jsonl`。
- 时间单调、segment ID 稳定且可追溯到 ASR。
- 如果某视频 ASR 差到无法可靠标 Gold，则在锁定前更换视频，不带病进入评估。

### P0B-03：编写 12 题与人工 Gold

**施工内容**

- 按 4.2 的固定分布逐视频出题。
- 人工从原视频标时间段并写答案要点。
- 生成/复核 Gold Segment IDs。
- 对不可回答题完成 transcript 搜索和整视频复核。
- 使用 Pydantic 或等价确定性校验保证 schema、数量和题型分布正确。

**产物**

- `eval/p0b/questions.jsonl`：只含可给 baseline 的字段。
- `eval/p0b/gold.jsonl`：只给 grader 和人工审查流程。
- `eval/p0b/rubric.md`：人工判定标准和例子。

**验收**

- 恰好 3 视频、每视频 4 题、总计 12 题。
- question IDs 唯一，Gold intervals 合法。
- 每道可回答题至少一个 Gold evidence unit 和一个 answer point。
- Gold 已由用户或明确指定人工 reviewer 确认。

### P0B-04：实现并验证 B0 Adapter

**施工内容**

- 根据选定 provider 的官方能力实现单视频直接多模态请求。
- 结构化输出 `status`、`answer` 和视频时间区间。
- 记录精确模型版本、prompt、参数、usage、latency 和原始响应。
- 错误和重试作为独立事件保存。

**验收**

- 先在 P0-A 开发样本跑通，不接触 P0-B Gold。
- B0 不读取本地 transcript 或 B1 artifacts。
- 真实 provider 不可用时明确阻塞正式 eval。

### P0B-05：冻结 B1 与增加 Retrieval Grader

**施工内容**

- 保持 P0-A TF-IDF、Top-5、segment 和 Evidence Gate 契约不变。
- 增加 Gold interval → segment hit 的确定性 grader。
- 计算 7.2 的所有 retrieval 指标及切片。
- 保留 raw Top-K，不允许 answerer 结果反向改写排序。

**验收**

- 人造边界测试覆盖：完全包含、半覆盖、边界轻触、无重叠、多 Gold units。
- P0-A q03 的错误 Top-1 / 正确 Top-5 现象可被 grader 正确表达。

### P0B-06：回答 Grader 与盲审材料

**施工内容**

- 确定性计算 schema、refusal、citation provenance 和 temporal hit。
- 为人工 reviewer 生成不显示 B0/B1 身份的 A/B 输出。
- 人工标注 answer point coverage、正确性和语义支持。
- 解盲映射单独保存，审查完成前不展示。

**验收**

- 同一 rubric 同时用于 B0 和 B1。
- 人工判断与程序判断分字段保存，不互相冒充。
- 原始模型输出保持只读，不因人工审查被改写。

### P0B-07：冻结 Eval Manifest

**施工内容**

- 完成 5.2 的全部 hash、模型、prompt、参数和版本记录。
- 使用 P0-A 开发样本完成最后一次 adapter/grader dry run。
- 验证 P0-B baselines 尚未读取 Gold。

**验收**

- manifest 字段完整且 hash 可复算。
- questions、Gold、prompt 或参数从此不可原地修改。
- 外部 provider、凭证和费用权限已就绪。

### P0B-08：执行一次锁定 B0/B1 Run

**施工内容**

- 对 12 道题分别执行 B0 与 B1。
- 使用固定顺序或记录的稳定随机顺序。
- 每题每 baseline 保留一个主结果。
- 传输错误按冻结策略重试并保留所有 attempt；模型质量不好不是重试理由。
- 保存 raw response、normalized result、usage、latency、Top-K 和 Gate 结果。

**验收**

- 应有 24 个主 baseline 结果，任何缺失都必须有显式 failure artifact。
- 无静默 fallback、无人工补答案、无挑选最好样本。

### P0B-09：评分、人工盲审与报告

**施工内容**

- 运行 retrieval 和 answer graders。
- 完成人工 A/B 审查后解盲。
- 按 overall、video、question type 报告结果。
- 列出每个失败是 ASR、segmentation、retrieval、answering、refusal、provider 还是 Gold 问题。
- 给出 P0-B 唯一阶段建议，不开始修复性 R2。

**产物**

- `reports/p0b-retrieval-eval.md`
- `artifacts/p0b/p0b-r1/metrics.json`
- `artifacts/p0b/p0b-r1/human-review.json`
- `artifacts/p0b/p0b-r1/run-manifest.json`

## 9. 建议目录

```text
eval/p0b/
├── corpus.jsonl
├── questions.jsonl
├── gold.jsonl
├── rubric.md
└── eval-manifest.json

artifacts/p0b/p0b-r1/
├── videos/<video_id>/...
├── b0/<question_id>/...
├── b1/<question_id>/...
├── blind-review.jsonl
├── blind-map.json
├── metrics.json
├── human-review.json
└── run-manifest.json

reports/
└── p0b-retrieval-eval.md
```

## 10. P0-B Definition of Done

P0-B 完成表示评估可信地执行完，不表示结果一定支持继续项目。

- [ ] P0-A 封存证据未被覆盖，起点 hash 可验证。
- [ ] 3 个自然连续中文技术视频均有来源、使用依据、hash 和 ingest artifacts。
- [ ] 12 题严格满足固定题型分布。
- [ ] 每道题都有用户确认的 Gold、答案要点或拒答依据。
- [ ] questions、Gold、prompts、模型、参数和源码 revision 在运行前冻结。
- [ ] B0 对 12 题均实际调用冻结的真实直接视频 provider；逐题成功或 failure 均保留，provider 从未可用则属于阻塞而非完成。
- [ ] B1 当前 TF-IDF Top-5 baseline 完成，未混入 Dense/Hybrid/Reranker。
- [ ] 24 个主结果均有 raw/normalized artifact 或显式失败原因。
- [ ] B1 原始 Top-K 和分数全部在 answerer 前持久化。
- [ ] retrieval 指标按 overall、video 和 question type 输出。
- [ ] 回答正确性、证据支持、拒答和 citation 时间命中均有结果。
- [ ] 人工审查与确定性 grader 结果分开保存。
- [ ] latency、usage、外部成本和 provider failure 如实报告。
- [ ] 测试和 ruff 通过，真实锁定 run 不由 Mock 代替。
- [ ] 报告保留所有失败题，不删除离群或低分结果。
- [ ] 报告只提出下一步建议，并停在用户审批点。

## 11. 不予验收的情况

- 只增加 3 个视频，但没有冻结 12 题和 Gold。
- 用模型自动生成 Gold，并让同一模型给自己评分。
- 只报告最终回答准确率，不报告 B1 retrieval 排名。
- B0 偷看 transcript，或 B1 偷看全文/Gold。
- 评估过程中修改问题、prompt、Top-K、segment 或答案要点。
- 一道题反复运行并挑最好输出。
- B0 使用真实模型而 B1 使用 Mock，或反之。
- B0 时间戳未经 Gold/人工验证，却标记为可信 citation。
- 将 P0-A 的 4 分 29 秒合成样本算入 3 个正式视频。
- 因 TF-IDF 失败直接加入 embedding，然后把改后结果冒充 R1。
- 没有人类复核中文答案要点与 evidence support。
- 未达到建议门槛却用主观描述宣称 retrieval 已被证明。

## 12. P0-B 完成后的阶段决策

报告只能建议以下一种状态：

### `PROCEED_TO_P1_DISCUSSION`

适用条件：B1 达到 `RETRIEVAL_VIABLE`，且相对 B0 达到 `VALUE_SUPPORTED`。该状态只允许讨论 P1 假设，不授权 Agent、VLM 或 LangGraph 施工。

### `OPEN_P0B_R2_RETRIEVAL_REVISION`

适用条件：ASR、Gold 与 pipeline 有效，但 TF-IDF 的主要失败集中在 `SINGLE_PARAPHRASE` 或 `MULTI_EVIDENCE`。R1 报告封存后，可另行申请只比较 Dense/Hybrid 等 retrieval 方案。

### `REVISE_P0B_DATA_OR_GOLD`

适用条件：视频不代表目标场景、ASR 质量不足、题目不可审查、Gold 冲突或 baseline 不公平。必须建立新 revision，不修改 R1 历史。

### `STOP_PROJECT`

适用条件：B1 无法可靠召回证据，或 B0 在质量、时间戳和成本上明显占优，而 B1 没有提供足够的可复核性价值。

任何状态都必须由用户确认。P0-B 报告完成后立即停止，不自动实现下一阶段。
