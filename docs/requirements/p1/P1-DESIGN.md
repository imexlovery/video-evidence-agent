# P1 Dynamic Evidence Seeking Owner 确认基线

- 文档状态：`OWNER_CHECKPOINT_CONFIRMED / CANONICALIZED_IN_HANDOFF_PACKAGE`
- 阶段：P1 设计；仅文档，不含实现授权
- 项目等级：`G1 PROTOTYPE`
- 设计结论：`CONDITIONAL_GO`
- 当前 checkout 基线：工作区 `main`，`HEAD=fc9b29c`；P0-B R3 closeout 与结果已提交
- R3 冻结 source baseline：`7cedce5`（来自 R3 manifest；与 closeout 提交是不同事实）
- P0 最终证据：`reports/p0b-r3-retrieval-eval.md`、`docs/tasks/p0b-r3/final-report.json`
- 设计边界：不修改 P0 冻结输入、历史 revision、源码、测试、依赖、模型配置或运行产物

这不是“给 P0 加一个 Agent”的施工单。它定义一个有退出机制的 G1 实验：先证明
当前 B1 仍存在至少两个可由观察后动作恢复的真实失败，再比较同一输入、同一证据源、
同一最终回答合同下的 `B1 Fixed Retrieval` 与 `B2 Dynamic Evidence Seeking`。若入口
Gate 不成立，P1 在实现 Agent 前直接结束；若 B2 不产生净增量，则删除 Agent 方案。

## 0. 结论摘要

### Go / Conditional Go / No-Go

结论是 **Conditional Go**。

原因：

1. P0 已证明固定 Retrieval 很强：R3 的 `QuestionHit@5=9/9`、可回答题
   `FullyCorrect=9/9`、`FullySupported=9/9`、非法 citation provenance `=0/10`。
2. 当前仍有一个真实 Evidence 缺口：`p0b-r1-rlinf-m` 的 Top-5 只覆盖 `2/3`
   Gold evidence units；以 `seg-010` 为锚点向前检查邻接 segment 可以获取漏掉的
   `seg-008/009`，因此 `inspect_segments` 有直接 P0 证据支持。
3. 但该题的 R3 最终答案已经被人工判定完整、正确且受支持，因此当前数据并不能证明
   Agent 会提升 Answer Correctness，只能证明它可能提升完整证据覆盖。
4. 唯一拒答失败 `p0b-r1-kling-u` 是输出合同失败，不是检索失败；应先用更严格的拒答
   规则或确定性后处理修复，不能拿它证明 Agent 价值。
5. P0 没有完成 B0 Direct Multimodal baseline；该方向已被 owner 明确 supersede。
   P1 不应声称有 `B0 vs B1 vs B2` 三方结果。

因此，P1 必须先执行“Headroom Gate”。若当前 B1 在预冻结候选集中找不到至少两个
动态可恢复失败，状态应为 `NO_GO_INSUFFICIENT_HEADROOM`，不实现 B2。

---

# A. P0 真实复盘

## A1. 当前完整 Pipeline

P0 的真实链路是：

```text
本地中文技术 MP4
  -> ffprobe 校验时长
  -> FFmpeg 提取 mono / 16 kHz WAV
  -> mlx-whisper 中文 ASR（保留原始时间边界与异常 segment provenance）
  -> 按 ASR 边界合并为 45 s 目标、60 s 上限的 VideoSegment
  -> 当前视频内 character 2-4 gram TF-IDF Top-5
  -> DeepSeek 文本模型只读取“问题 + 当前 Top-5”
  -> AnswerProposal
  -> Deterministic Evidence Gate 回填 source quote / timestamp
  -> AnswerResult 或 INSUFFICIENT_EVIDENCE
  -> 自动 Retrieval/Provenance 评分 + owner 语义审核
```

P0-A 使用原始 `retrieve()`；当前 P0-B R2/R3 正式路径使用
`retrieve_transcript_r2()`。每次问题处理仍只访问一个视频；P0-B 只是把同一单视频链路
分别在 3 个视频上评测。

## A2. Segment 数据结构

权威结构是 `VideoSegment`：

| 字段 | 合同 |
| --- | --- |
| `video_id` | 非空；所有同次检索 segment 必须属于当前视频 |
| `segment_id` | 稳定、唯一；格式为 `<video_id>-seg-<ordinal>` |
| `ordinal` | 从 0 连续递增；用于安全邻接定位 |
| `start_ms` / `end_ms` | 真实、非负、单调、不重叠，`end_ms > start_ms` |
| `transcript_text` | 非空 ASR 文本；不被模型改写成 source quote |
| `source_asr_ordinals` | 组成该 segment 的原始 ASR segment provenance |

当前 3 个 P0-B 视频共 127 个 `VideoSegment`。`segment_id + ordinal` 已足够支持
按锚点检查邻接上下文，不需要让模型生成自由时间范围。

## A3. 当前 Retrieval

P0-B R3 的冻结 profile 是 `char_tfidf_2_4_query_views_v1`：

- 对问题与 transcript 做 Unicode NFKC、casefold、空白/标点归一化；
- 生成 `base`、`focus`、`aliases` 三个确定性 query view；
- 使用 character 2-4 gram TF-IDF，`sublinear_tf=true`；
- 固定权重：`base=0.10`、`focus=0.36`、`aliases=0.54`；
- cosine similarity 后稳定排序；同分以 `ordinal` 决定；
- 固定 Top-K=5，返回完整原始 `VideoSegment`。

这个 profile 没有 embedding、Dense、Hybrid、Reranker、LLM rewrite 或 VLM。其 alias
规则是在 R1 失败分析后形成，且 R2/R3 仍在同一 12 题固定回归集上评测，因此不能把
R3 分数当作未见问题泛化证据。

## A4. Answer / Evidence 输出合同

P0 模型输出 `AnswerProposal`：

```json
{
  "status": "ANSWERED | INSUFFICIENT_EVIDENCE",
  "answer": "string | null",
  "citation_segment_ids": ["segment-id"]
}
```

程序输出 `AnswerResult`：

```json
{
  "status": "ANSWERED | INSUFFICIENT_EVIDENCE",
  "answer": "string | null",
  "evidence": [
    {
      "segment_id": "segment-id",
      "start_ms": 0,
      "end_ms": 45000,
      "quote": "由程序从权威 VideoSegment 回填"
    }
  ]
}
```

`INSUFFICIENT_EVIDENCE` 必须是空 answer、空 evidence。Gate 只验证 provenance 和结构，
不把“存在 citation”解释成语义正确。

## A5. 当前 Eval case

P0-A：1 个 Chinese-LiPS 受控样本，3 个可回答题 + 1 个不可回答题，4/4 运行成功；
繁转简 CER `0.0489`，字形敏感 CER `0.3943`。

P0-B：3 个自然中文技术视频，每个视频固定 4 题，共 12 题：

| video | Single Lexical | Single Paraphrase | Multi Evidence | Unanswerable |
| --- | --- | --- | --- | --- |
| 可灵 2024 | 开放版本分辨率/时长 | 视频生成的创作优势 | 模型设计与数据处理 | 确切参数量 |
| RLinf 2026 | v0.1 首发日期 | RL 改善哪类泛化 | 仿真与真机关键约束 | GitHub 精确下载量 |
| 吴翼目标/对齐 | “不知道”的奖励分数 | 做饭/性别偏见 | 机器人保姆对齐问题 | CHAI 年度经费 |

类型分布固定为 3 `SINGLE_LEXICAL`、3 `SINGLE_PARAPHRASE`、3
`MULTI_EVIDENCE`、3 `UNANSWERABLE`。Gold 只进入评分/人工审核，不进入检索或回答。

## A6. 指标与 baseline

| revision | Retrieval profile / execution | Hit@1 | Hit@5 | Evidence Recall@5 | Multi AllEvidence@5 | Fully Supported | Correct Refusal |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| R1 | 原始 char TF-IDF + 真实回答 | 2/9 | 7/9 | 0.6481 | 1/3 | 5/9 | 2/3 |
| R2 | 新 query views；provider 全失败 | 6/9 | 9/9 | 0.9630 | 2/3 | 不可比较 | 不可比较 |
| R3 | 与 R2 相同检索；12 次真实回答 | 6/9 | 9/9 | 0.9630 | 2/3 | 9/9 | 2/3 |

R3 另有：MRR `0.8056`、answer/refusal accuracy `11/12`、citation temporal hit
`9/9`、schema compliance `12/12`、非法 citation provenance `0/10`、平均检索
`34.6 ms`、平均回答 `4799.6 ms`、总 token `23858`。

**Direct Model baseline：不存在可比较结果。** B0 direct multimodal 方案已被 owner
supersede；当前正式 P0 只有 `TRANSCRIPT_RETRIEVAL`。P1 不恢复 B0，不上传视频。

## A7. 典型成功

- 所有 9 个可回答题在当前 B1 的 Top-5 中至少命中一个 Gold evidence unit。
- 9/9 可回答题最终答案被人工判定 fully correct、fully supported、semantic supported。
- 3 个 lexical、3 个 paraphrase、3 个 multi-evidence 最终答案均正确。
- 2/3 不可回答题正确拒答；所有回答 citation 都来自当前问题 Top-5。
- R3 12/12 schema 合法，没有跨视频或伪造 timestamp/quote。

## A8. 典型失败与当前瓶颈

| 失败 | 证据 | 性质 | P1 处理 |
| --- | --- | --- | --- |
| Query/证据词形不一致 | R1 的可灵 paraphrase、RLinf 日期等未进 Top-5 | Historical retrieval | 只作为新 blind paraphrase 的来源，不把 R1 当当前 B1 |
| 多证据被单一 Top-5 压缩 | R1 多题失败；R3 `RLinf-m=2/3` | 当前 residual | `inspect_segments` 是首要实验动作 |
| Top-1 仍不稳定 | R3 `6/9`，但 Top-5 `9/9` | Ranking diagnostic | 不足以单独证明 Agent；Answer 已稳定 |
| 未披露事实仍输出自然语言答案 | `kling-u` 返回 ANSWERED | Refusal contract | 先用规则/prompt；不得归功于 Agent |
| ASR 词形/单位错误 | `720P` 被识别为 `720MHz` | ASR | P1 不改；也不足以触发 VLM |
| Eval 无 holdout | R2/R3 复用 R1 修订后的 12 题 | Evidence limitation | P1 challenge slice 必须先冻结再调 B2 |

P1 最值得针对的真实失败是：**固定 Top-5 找到主题中心，但没有自动补齐相邻 segment
中的完整必要证据。** 次要候选是：**第一次 query 没有覆盖问题的某个语义子部分，
观察候选后需要重写 query。** 后者必须先通过 Headroom Gate 证明当前 B1 仍会失败。

---

# B. P1 是否值得做

## B1. 核心假设

```text
在完全相同的单视频 transcript、VideoSegment、初始 Top-5、最终回答合同和
Evidence Gate 下，允许模型在看到证据后最多再进行 2 次只读取证动作，能否恢复
当前 B1 未覆盖的必要证据，而不引入 citation、拒答、成本或无意义动作回归？
```

## B2. Headroom Gate（实现 Agent 前）

P1 必须先完成以下预注册步骤：

1. 保留现有 12 题作为 regression；不修改问题、Gold、segment 或 P0 历史结果。
2. 把现有 `p0b-r1-rlinf-m` 的 `2/3` evidence coverage 标为固定 hard case；再从
   P0 已观察失败建立最多 4 个新候选：R1 词形 mismatch、R1 多子句失衡、不可回答
   distractor；候选问题不得读取 Gold transcript 反向造词。
3. 在任何 B2 prompt/tool 策略调试前冻结候选与 Gold，再只运行当前 B1。
4. 所有候选及 B1 结果都保留；B1 已通过的题转为 regression，不删除、不换题。
5. 至少出现 2 个 answerable 的 B1 primary-metric failure，且必须有明确、可审计的
   动态恢复路径（新增 Gold evidence unit），才允许实现/运行 B2。

否则停止为：

```text
NO_GO_INSUFFICIENT_HEADROOM
```

这不是 P1 失败，而是实验说明当前固定 RAG 已足够，没必要引入 Agent。

---

# C. 最小 P1 架构

## C1. P0 保留

- 本地 MP4 -> FFmpeg -> mlx-whisper -> `VideoSegment` ingest 全部保留；P1 不重跑 ASR。
- 127 个当前 P0-B segment、现有 12 题、Gold、R3 结果作为历史基线保留。
- 当前 R2/R3 character TF-IDF profile 作为 B1 和 B2 的共同搜索实现。
- Top-K=5、单视频边界、`AnswerProposal`、`AnswerResult`、Evidence Gate 原则保留。
- P0 的 revision isolation、manifest/hash、单次正式运行、不覆盖失败结果规则保留。

## C2. P1 新增

仅新增以下逻辑能力：

1. `search_video`：把现有 B1 retrieval 包装为只读工具；初次调用固定使用原问题。
2. `inspect_segments`：按已观察的一个 `segment_id` 加载有限邻接 segment。
3. 原生 Python bounded loop：观察后选择 final / rewrite search / inspect / refuse。
4. 结构化 Trace：记录 action、validated args、observation IDs、evidence delta、预算、
   final proposal、Gate 与 token/latency；不保存隐藏 chain-of-thought。
5. P1 Eval：同一 manifest 下比较 B1/B2，新增 Agent 行为与成本指标。

不新增数据库、API、UI、队列、checkpoint service、长期 memory 或多 Agent。

---

# D. Tool Contract

## D1. `search_video`

设计修改：**不把 `top_k` 交给模型。** Top-K 固定为 5，保证 B1/B2 初始证据预算可比。

输入：

```json
{
  "query": "非空中文或中英混合检索意图"
}
```

隐式运行上下文：`run_id`、当前 `video_id`、冻结 retrieval profile、`top_k=5`。

输出：

```json
{
  "status": "OK",
  "video_id": "current-video",
  "query": "validated query",
  "retrieval_profile": "char_tfidf_2_4_query_views_v1",
  "top_k": 5,
  "hits": [
    {
      "rank": 1,
      "score": 0.1,
      "segment": {
        "video_id": "current-video",
        "segment_id": "current-video-seg-010",
        "ordinal": 10,
        "start_ms": 466600,
        "end_ms": 512800,
        "transcript_text": "source transcript",
        "source_asr_ordinals": [100, 101]
      }
    }
  ]
}
```

边界：

- 只能查询当前视频的冻结 `segments.jsonl`；不能读取其他视频、Gold、完整 transcript
  拼接、历史答案或外部资源。
- 初次 search 固定为原始 question；第二/第三次 search 才允许 observation-driven rewrite。
- 规范化后与历史 query 完全相同的重复 search 被拒绝。
- 每次结果仍是 5 个完整 source `VideoSegment`，不返回模型生成的摘要。

错误：`INVALID_QUERY`、`DUPLICATE_QUERY`、`VIDEO_SCOPE_VIOLATION`、
`RETRIEVAL_UNAVAILABLE`、`TOOL_BUDGET_EXHAUSTED`。错误也进入 Trace，不自动重试。

Evidence 来源：当前视频冻结 `segments.jsonl`，由现有 R2/R3 retrieval profile 排序。

## D2. `inspect_segments`

设计修改：输入只接受**一个已观察锚点**，不是任意 ID 列表；这已足够覆盖当前
RLinf residual，并能限制上下文膨胀。

输入：

```json
{
  "anchor_segment_id": "current-video-seg-010",
  "radius": 1
}
```

`radius` 只允许 `1` 或 `2`；一次最多返回 5 个 segment。

输出：

```json
{
  "status": "OK",
  "video_id": "current-video",
  "anchor_segment_id": "current-video-seg-010",
  "radius": 2,
  "segments": [
    {
      "relation": -2,
      "segment": {
        "segment_id": "current-video-seg-008",
        "ordinal": 8,
        "start_ms": 375500,
        "end_ms": 420800,
        "transcript_text": "source transcript"
      }
    }
  ]
}
```

边界：

- anchor 必须来自本次 run 已成功返回的 search/inspect observation。
- 系统按权威 segment ordinal 解析邻接，不接受模型提供 `start_ms/end_ms`。
- 只能读取当前视频，保持源顺序，不跨越首尾，不执行 OCR/VLM。
- 重复 inspect 相同 anchor/radius 被拒绝；不会静默扩大 radius。

错误：`UNKNOWN_SEGMENT_ID`、`ANCHOR_NOT_OBSERVED`、`VIDEO_SCOPE_VIOLATION`、
`INVALID_RADIUS`、`SEGMENT_SOURCE_UNAVAILABLE`、`TOOL_BUDGET_EXHAUSTED`。

Evidence 来源：当前视频冻结 `segments.jsonl`；时间、quote、ordinal 全部由程序回填。

## D3. 为什么仍需要两个 Tool

- `search_video` 解决“方向/词形不对”，可用新 query 找到不相邻的候选。
- `inspect_segments` 解决“主题找对但上下文被 segment 边界截断”，无需重新排序。
- 当前 RLinf residual 直接支持第二个工具；历史 R1 query mismatch 支持第一个工具的
  rewrite 候选。
- 合并成一个万能 retrieve 工具会模糊动作因果，降低 Eval 对增量来源的解释力。

---

# E. Agent State

最小 run state：

```json
{
  "run_id": "p1-run-id",
  "eval_revision": "p1-r1",
  "video_id": "one-video-id",
  "question_id": "question-id",
  "question": "question text",
  "tool_call_count": 1,
  "max_tool_calls": 3,
  "search_queries": ["original question"],
  "seen_segments": {
    "segment-id": {
      "first_seen_step": 1,
      "sources": ["search_video"]
    }
  },
  "last_observation_segment_ids": ["segment-id"],
  "trace_steps": [],
  "terminal_status": null
}
```

不单独存储可从 Trace 推导的 `candidate_segments`、`inspected_segments`、
`search_history` 副本，避免多个权威来源。没有 session memory、长期 memory、跨问题
共享 evidence 或 checkpoint。进程失败后该 run 记为失败，不在同一 revision 恢复/重跑。

---

# F. Agent Loop

建议最大 **3 次 Tool Call**，不是 4 次。初次固定 search 占 1 次；剩余 2 次足够覆盖：

- search(original) -> answer/refuse；
- search(original) -> inspect -> answer/refuse；
- search(original) -> search(rewrite) -> answer/refuse；
- search(original) -> search(rewrite) -> inspect -> answer/refuse。

伪代码：

```text
validate current video + frozen segment source
state = new_run(max_tool_calls=3)

observation = search_video(question)       # deterministic first action
record(observation)

while true:
    decision = model(question, bounded_trace, eligible_segments, remaining_budget)

    if decision.action == FINAL_ANSWER:
        return evidence_gate(decision.proposal, state)

    if decision.action == REFUSE:
        return INSUFFICIENT_EVIDENCE

    if remaining_tool_budget == 0:
        return INSUFFICIENT_EVIDENCE(reason="tool_budget_exhausted")

    validated_action = validate_action(decision, state)
    if invalid:
        record_error_and_refuse()           # no model-selected retry loop

    observation = execute_read_only(validated_action)
    record(observation, newly_seen_segment_ids)
```

动态性证明不是“代码里有 while”，而是 Trace 显示：

- 简单题在第一次 observation 后直接回答；
- 无证据题在有界搜索后拒答；
- 邻接缺口题选择 inspect；
- query 方向错时选择不同 query 的 search；
- 后续动作确实新增证据或改变终止判断。

若 `>=80%` 题目都出现同一固定 `search -> inspect -> answer` 序列，B2 应改写为
deterministic workflow，并停止使用 Agent 标签。

---

# G. Evidence Gate

Gate 使用当前 P0 的 fail-closed 原则，并增加 run-local provenance：

1. 工具调用前验证当前 `video_id`、步骤预算、query/radius/anchor 合同。
2. 只有本次 run 中成功的 search/inspect observation 返回的 segment 才进入
   `eligible_evidence_ids`。
3. final proposal 的每个 citation ID 必须存在、属于当前视频、来自 eligible set。
4. quote、start/end、ordinal 由权威 `VideoSegment` 回填；模型值不被信任。
5. `ANSWERED` 必须有非空答案和至少一个唯一 citation。
6. `INSUFFICIENT_EVIDENCE` 必须是空答案、空 evidence。
7. 超预算、非法 action、跨视频、未知 ID、伪造 timestamp、完全无 citation 的回答均
   降级为 `INSUFFICIENT_EVIDENCE`，并记录确定性 reason code。
8. Gate 可以维持或降级模型状态，绝不升级。
9. Gate 不判断 citation 是否语义支持 claim，也不因为 citation 合法而判定答案正确。

P1 首轮**不新增 claim-level 输出合同**。原因是 P0 当前输出与人工 rubric 都是 answer
level，R3 没有暴露“一个回答混合多个独立 claim 但部分无引用”的结构性失败。现在引入
`claim/evidence_ids/proposed_status` 会同时改变 B1/B2 输出合同，混淆 Agent 实验。
若 P1 人工审核观察到 mixed-support claim，再在新 revision 中单独提案。

---

# H. Eval

## H1. 比较组

- `B0 Direct Model`：`NOT_AVAILABLE / NOT_RUN`，不进入 P1 结论。
- `B1 Fixed Retrieval`：当前 R2/R3 retrieval profile + 一次 answer。
- `B2 Dynamic Evidence Seeking`：相同首次 B1 search + 最多 2 次 observation-driven tool。

B1/B2 必须使用同一 P1 manifest、同一视频/segment snapshot、问题、Gold、provider model、
温度、最终 answer contract、Gate 和人工 rubric。正式运行前单独获得真实模型调用授权；
每个方法每题只运行一次，不选择性重跑。

## H2. 数据集升级

1. 现有 12 题全部保留为 regression，不以当前 9/9 结果替代新 B1/B2 同 revision 比较。
2. 把现有 `p0b-r1-rlinf-m` 标为固定 hard case；它不是新题，也不重复计入总题数。
3. 新增最多 4 个 pre-frozen candidate，不为 Agent 造大量容易题。
4. 新候选只能来自 P0 已记录失败类型；问题在 B2 设计前冻结，B1 通过题也保留。
5. 只有 Headroom Gate 通过，才把 B1 primary-metric failure 标为 challenge slice。
6. 不把 Gold、answer point、historical answer 或完整 transcript 交给 B1/B2。

## H3. 指标

Retrieval / Evidence：

- Question Hit@1 / Hit@5（首次 search 与最终 seen evidence 分开报告）；
- Evidence Unit Recall；All Necessary Evidence；跨 segment evidence coverage；
- 新增 Gold evidence unit 数；invalid/fabricated citation、timestamp、cross-video。

Answer / Refusal：

- Fully Correct、Fully Supported、Answer Point Recall、Semantic Support；
- Unsupported Claim（人工 rubric）；
- Correct Refusal、False Refusal、未披露事实却输出 `ANSWERED`。

Agent 行为：

- Tool Calls mean/max；step-limit rate；action sequence 分布；
- rewrite 后新增 segment / Gold unit 的比例；
- inspect 后新增 segment / Gold unit 的比例；
- 重复 query、重复 inspect、无新增 evidence 的 action；
- dynamic recovery：B1 failure 且 B2 因后续 observation 转为通过的题数。

成本：

- model calls、prompt/completion/total token、provider-reported cache token；
- search/inspect latency、model latency、end-to-end latency；
- 无冻结价格快照时不伪造货币成本；VLM calls 固定为 0。

## H4. Owner 确认的保留 Gate

| Gate | 建议阈值 |
| --- | --- |
| Headroom | 至少 2 个 pre-frozen answerable B1 failure 有明确动态恢复路径 |
| Dynamic recovery | B2 至少净恢复 2 个 challenge case |
| Regression | 现有 12 题 FullyCorrect/FullySupported 不低于同 revision B1 |
| Refusal | B2 CorrectRefusal 不低于 B1；FalseRefusal 不高于 B1 |
| Evidence safety | invalid citation / timestamp / cross-video = 0 |
| Runtime safety | schema failure、预算越界、未捕获 tool error = 0 |
| Dynamicity | 至少存在直接终止路径和 observation-driven 恢复路径 |
| Efficiency | 平均 Tool Calls <= 2.0；任何达 limit 的 run 必须 fail closed |
| Cost | B2 平均 total token <= B1 的 3 倍；超出则默认不保留 Agent |

这是小样本 G1 count gate，不宣称统计显著性。若 B2 只改善 Evidence Recall、没有改善
Answer/Refusal，最终报告必须明确写成“证据完整性增量”，不能泛化为“答案更智能”。

## H5. 终止决策

- `KEEP_AGENT_EXPERIMENTAL`：Headroom 与所有保留 Gate 通过，且 Trace 证明非固定序列。
- `CONVERT_TO_WORKFLOW`：收益成立但绝大多数动作序列固定。
- `DELETE_AGENT`：B2 没有净恢复、回归、或成本超过建议上限。
- `REPAIR_RETRIEVAL_FIRST`：rewrite/inspect 在多数 hard case 中无法新增必要 evidence。
- `NO_GO_INSUFFICIENT_HEADROOM`：在构建 B2 前就没有足够当前 B1 失败。

---

# I. LangGraph 决策

选择：**Native Python bounded loop**。

理由：

- 当前只有一个 run、两个只读工具、一个预算计数器和三个终止动作；
- 无持久 checkpoint、并发分支、人工中断恢复、多 Agent、长任务或跨进程 replay；
- 原生循环更容易保持 B1/B2 实验变量单一，也更容易删除；
- JSON Trace 已满足 G1 的可审计需求，不需要 graph runtime 才能保存 Trace。

LangGraph 在 P1 明确禁止。只有后续出现持久 checkpoint、复杂并行/恢复状态或图运行时
本身成为被验证需求时，才在新阶段重新评估。

框架策略为 `FRAMEWORKLESS / PROJECT_OWNED`。按 requirements skill 要求，已评估
Hypha：项目方将其定位为 CodeSoul × 电子科技大学联合研发、覆盖多等级 Agent Native
交付的框架；但 P1 不需要共享 runtime、memory、MCP、审批、恢复或多 Agent 能力，引入
它会改变实验变量。因此 P1 标记 `Hypha: REJECTED_FOR_P1`；只在后续新阶段出现持久
恢复、并发图、共享 memory 或多 Agent 等已验证需求时重新评估。

---

# J. P1 范围

## Must Have

- Headroom Gate 先于 Agent 实现；
- 同一 revision 的 B1 vs B2；
- 固定第一次 B1 search、最多 3 次 tool call；
- 两个只读 tool 的严格 schema、当前视频边界与稳定错误码；
- Native Python bounded loop；
- run-local eligible evidence set 与确定性 Gate；
- 完整结构化 Trace、token/model/tool/latency 指标；
- 现有 12 题 regression + 最多 4 个 pre-frozen candidate；
- 一次正式运行、失败保留、不可选择性重跑；
- 最终输出五选一终态并允许删除 Agent。

## Conditional

- Query rewrite：只有 Headroom Gate 证明当前 B1 有 query-mismatch failure 才保留；
- `inspect_segments(radius=2)`：当前 RLinf residual 已给出保留依据，但仍要验证新增 Gold；
- 新 challenge case：只允许来自 P0 已观察失败，且必须先冻结、再跑 B1；
- claim-level schema：只有出现 mixed-support claim 证据后另开 revision；
- VLM/keyframe：只有 transcript 中不存在答案而画面存在答案的审计证据后另开 revision。

## Explicitly Deferred

- OCR、VLM、keyframe extraction、Dense/Hybrid/Reranker/Embedding；
- LangGraph、Hypha、其他 Agent framework；
- Planner/Executor/Critic/Judge、多 Agent；
- FastAPI、Web/UI、Redis、Dramatiq、MQ、Worker、数据库、对象存储；
- 多用户、多视频联合推理、多语言、写操作、视频编辑；
- 生产 SLO、商用 SLA、计费、租户、部署与运维承诺；
- 长期 memory、跨问题学习、自动调 prompt、自动吸收用户反馈。

---

# K. 最小实施顺序（仅计划，不执行）

1. **P1-00 Baseline audit**：冻结当前 working-tree 基线、P0 R3 hashes、测试命令、
   现有 12 题与 127 segments；记录 README 仍停留在 R2 的文档漂移，但不改 P0 历史。
2. **P1-01 Headroom candidates**：从真实失败生成最多 4 个候选并人工确认 Gold；先冻结。
3. **P1-02 B1 headroom run**：只跑 B1；保留全部结果；不足 2 个动态可恢复失败就停止。
4. **P1-03 Tool contracts**：实现并单测 `search_video`、`inspect_segments` 的范围、预算、
   ID、radius、错误、provenance；此步不得调用模型。
5. **P1-04 Trace + Gate**：实现 run-local evidence eligibility、结构化 Trace 和 fail-closed
   Gate；先用 deterministic fixtures 覆盖成功/失败/replay。
6. **P1-05 Native loop**：实现最小 action schema 和 3-tool-call bounded loop；不引入框架。
7. **P1-06 Freeze**：冻结 B1/B2 manifest、prompts、tool schema、source、dataset、provider
   配置布尔状态与调用预算；另行取得 owner 的真实调用授权。
8. **P1-07 One formal comparison**：B1/B2 每题一次，先落盘 action/retrieval，再调用模型；
   provider/tool/schema/timeout 失败不补跑。
9. **P1-08 Review and decision**：自动评分 + owner 语义/Trace 审核，输出
   `KEEP_AGENT_EXPERIMENTAL` / `CONVERT_TO_WORKFLOW` / `DELETE_AGENT` /
   `REPAIR_RETRIEVAL_FIRST` / `NO_GO_INSUFFICIENT_HEADROOM`，然后停止。

---

# L. Owner checkpoint 结果

Owner 已确认以下一组相互依赖的决策，并授权整理为正式可施工 handoff：

1. P1 为 `Conditional Go`，先过“至少 2 个动态可恢复 B1 failure”的 Headroom Gate；
2. 采用两个只读 tool、固定 Top-K=5、最多 3 次 tool call；
3. 采用 Native Python / FRAMEWORKLESS；P1 不采用 LangGraph、Hypha 或 VLM；
4. 最终回答继续复用 P0 answer-level contract，不在首轮引入 claim-level schema；
5. 使用本文件 H4 的建议保留 Gate；若 Agent 无净增量则删除或改 workflow。

本文件现在是背景基线，不再是权威施工入口。权威施工合同从 `00-handoff.md` 开始；
最终 readiness 只读取 validator 生成的 `requirements-readiness.json`。本次仍不授权
任何 provider 调用或源码实现。

## 证据索引

- `src/video_evidence_agent/schemas.py`
- `src/video_evidence_agent/segments.py`
- `src/video_evidence_agent/retrieval.py`
- `src/video_evidence_agent/answering.py`
- `src/video_evidence_agent/evidence.py`
- `src/video_evidence_agent/p0b_eval.py`
- `eval/p0b/questions.jsonl`
- `eval/p0b/gold.jsonl`
- `reports/p0a-smoke-report.md`
- `reports/p0b-retrieval-eval.md`
- `reports/p0b-r2-retrieval-eval.md`
- `reports/p0b-r3-retrieval-eval.md`
- `docs/tasks/p0b-r2/failure-analysis.md`
- `docs/tasks/p0b-r3/final-report.json`
