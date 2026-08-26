# P0-B R2 任务 Prompt：最小 TF-IDF 质量修订

| 字段 | 内容 |
| --- | --- |
| 任务编号 | `P0-B-R2` |
| 发布状态 | `IMPLEMENTATION_IN_PROGRESS`（原始发布记录为 `ISSUED_DOCUMENT_ONLY`） |
| 施工授权 | `OWNER_AUTHORIZED`；owner 已明确“开始施工” |
| 项目等级 | `G1 PROTOTYPE`，本地离线评测 |
| 前置结果 | `p0b-r1 FROZEN / OWNER_REVIEW_COMPLETE / P0B_RETRIEVAL_THRESHOLDS_NOT_MET` |
| 唯一目标 | 在不扩展技术栈的前提下，提高现有 TF-IDF Top-5 检索与拒答质量，并以新的 `p0b-r2` 完整评测判断是否通过 P0-B |
| 停止点 | 发布 r2 报告并等待 owner 决策；不得进入 P1 或自动开启 r3 |

## 1. 给实施代理的主指令

在 `/Users/tristana/Develop/video-evidence-agent` 中实施 `P0-B-R2`。

这是一次窄范围质量修订，不是重做项目。必须保留 `p0b-r1` 的冻结输入、
原始结果、人工标签、报告和失败结论。先建立可恢复的 r1 Git 基线，再只改进
现有 character 2–4 gram TF-IDF Top-5 的通用问题处理/排序，以及
`INSUFFICIENT_EVIDENCE` 拒答规则。不得新增 Dense、Hybrid、Reranker、
Embedding、VLM、Agent 或服务化组件。

冻结 `p0b-r2` 前完成测试、静态检查、严格 JSONL、媒体/segment/Gold 映射和
r1 完整性校验。冻结后对原 12 题进行一次全量正式运行：每题先持久化自己的
Top-5，再执行一次 DeepSeek 文本回答。不得选择性重跑或覆盖失败结果。

自动评分后生成逐题人工审核材料，并在 owner 必须确认语义标签时暂停。只有六项
冻结门槛全部通过且人工语义审核完成，才能报告 `P0B_R2_PASSED`。否则如实关闭为
`P0B_R2_THRESHOLDS_NOT_MET`。无论结果如何，到报告为止立即停止。

## 2. r1 基线与差距

当前正式证据来自：

- `eval/p0b/eval-manifest.json`：`p0b-r1` 冻结 manifest；
- `reports/p0b-retrieval-eval.json`：自动与人工合并评分；
- `artifacts/p0b/p0b-r1/human-review.json`：12 题人工语义标签；
- `docs/requirements/p0b/decision-evidence.jsonl`：append-only 决策历史。

| 冻结门槛 | r1 | 通过线 | r2 所需净提升 |
| --- | ---: | ---: | ---: |
| QuestionHit@1 | 2/9 | ≥ 6/9 | +4 题 |
| QuestionHit@5 | 7/9 | ≥ 8/9 | +1 题 |
| Multi AllEvidence@5 | 1/3 | ≥ 2/3 | +1 题 |
| FullySupportedAnswer | 5/9 | ≥ 7/9 | +2 题 |
| CorrectRefusal | 2/3 | ≥ 2/3 | 已达到，必须保持 |
| Invalid citation provenance | 0/9 | 0/9 | 已达到，必须保持 |

r1 已证明媒体、ASR、segment、DeepSeek 文本调用、引用回填和评分链路可运行。
r2 不再重复验证这些工程事实，只处理检索排序、多证据召回和拒答契约。

## 3. 固定输入与保护边界

以下内容属于 `fixed constraint`，r2 不得修改：

- 三个现有中文技术视频及其媒体哈希、时长和使用依据；
- `artifacts/p0b-ingest/` 中 127 个真实 `VideoSegment`；
- `eval/p0b/corpus.jsonl`、`questions.jsonl`、`gold.jsonl`；
- 12 道问题的文字、题型、Gold answer points、时间边界和 Gold segment IDs；
- ASR 模型、ASR 输出和 45/60 秒 segment 合并结果；
- character 2–4 gram TF-IDF 算法族与 `Top-K=5`；
- DeepSeek 只读取“当前问题 + 当前视频 Top-5”的上下文边界；
- citation ID 必须属于当前题 Top-5，quote 与时间戳必须由程序从源 segment 回填；
- P0-A 所有冻结证据；
- `p0b-r1` manifest、result、raw response、retrieval、human review 和报告。

`docs/requirements/p0b/decision-evidence.jsonl` 只能追加，不能改写或删除历史记录。

实施前已建立可恢复的 r1 Git baseline：`982f5ea5d8036a65ce9779ec1d24a5d1f495511d`。
baseline 只保存代码、配置和可提交文档，不提交媒体、密钥或被忽略的 provider
原始响应。r1 冻结 manifest、结果、人工标签、报告和媒体/ingest 快照继续保持不变。

## 4. r2 允许改动

实施代理可以在以下范围内选择最简单的通用实现：

1. 对问题文本做确定性的通用规范化，例如中英文大小写、空白、标点和术语别名
   规范化；规则不得包含 question ID 或某道 Gold 的专用答案词。
2. 在仍使用 character 2–4 gram TF-IDF 的前提下，调整通用查询构造、分句组合
   和分数聚合，使多子问题与多证据问题更容易进入 Top-5。
3. 调整 TF-IDF 内部排序策略，但最终仍只输出 5 个有稳定 ID 的原始
   `VideoSegment`；不得增加第二阶段模型排序器。
4. 新建 r2 DeepSeek answer prompt，明确：证据只说明“未披露、不方便透露、
   不知道确切值”时，对所求确切事实必须返回 `INSUFFICIENT_EVIDENCE`；答案必须
   仅覆盖 Top-5 真正支持的要点。
5. 增加 r2 专属 manifest、artifact 和 report 路径支持，确保任何命令都无法覆盖
   r1。
6. 增加必要的单元测试、回归测试、CLI 参数和文档。

所有通用检索规则必须先用合成测试或 P0-A 开发样本证明，不得用逐题硬编码制造
r2 分数。

## 5. 明确禁止

- 不使用 Dense、Hybrid、Reranker、Embedding、LLM Query Rewrite。
- 不新增或更换视频，不重跑 ASR，不重新切 segment。
- 不修改问题、Gold、answer points、时间边界或 Gold segment IDs。
- 不把 Gold、完整 transcript、r1 人工答案或 Codex 草案提供给 DeepSeek。
- 不为具体 question ID、视频 ID 或 Gold 答案写专用检索分支。
- 不上传视频，不恢复 Gemini/B0/direct-video 路径。
- 不改变 `Top-K=5`，不把邻接全文作为隐藏上下文交给回答模型。
- 不在冻结集上反复调 prompt 后挑最好输出。
- 不选择性重跑失败题，不覆盖 provider、schema、timeout 或 retrieval failure。
- 不进入 OCR/VLM、Agent、FastAPI、数据库、Dense/Hybrid/Reranker 或 P1。
- 不将同一 12 题上的 r2 结果描述为独立 holdout 或普遍泛化证明；它只能证明
  固定回归集上的改进和 G1 门槛结果。

## 6. 施工顺序

### P0B-R2-00：保护 r1

- 复算并确认 r1 manifest、正式输入、媒体、ingest、结果和报告均存在且未被覆盖。
- 建立包含当前 r1 实现和文档的可恢复 Git baseline，记录 commit ID。
- 保存 r1 关键 artifact 哈希清单；不得把密钥、媒体或 ignored 原始响应加入 Git。
- 若无法建立可恢复基线，停止并报告，不得继续修改源码。

### P0B-R2-01：形成失败分析

- 从 r1 report、retrieval 和 human review 归类排序、多证据、回答完整性和拒答失败。
- 产出 `docs/tasks/p0b-r2/failure-analysis.md`。
- 每个拟议修改必须说明它是通用规则、对应哪个失败类别、如何用非 Gold 硬编码测试。

### P0B-R2-02：实现最小检索修订

- 只在第 4 节范围内修改 TF-IDF 问题处理和排序。
- 保持 Top-5 输出 schema、稳定 segment ID、分数和持久化顺序。
- 加入正常、同义改写、多子句、多证据和空查询回归测试。

### P0B-R2-03：修订拒答契约

- 新建 r2 prompt，不修改 r1 prompt。
- 对“没有给出确切事实”和“证据不足”增加结构化拒答测试。
- Evidence Gate、provenance 和 quote 回填继续由确定性程序执行。

### P0B-R2-04：建立 revision 隔离

- r2 manifest 必须写入新的 revision 专属路径；当前
  `eval/p0b/eval-manifest.json` 不得被覆盖。
- r2 结果只写入 `artifacts/p0b/p0b-r2/`。
- r2 报告只写入 `reports/p0b-r2-retrieval-eval.json` 和 `.md`。
- 增加“目标目录已有正式结果时拒绝覆盖”的测试。

### P0B-R2-05：冻结前验证

必须运行并保存结果：

```text
uv run pytest -q
uv run ruff check .
严格 JSON/JSONL 校验
git diff --check
r1 保护文件哈希校验
3 个媒体哈希和时长校验
127 个 segment 与全部 Gold segment/time 映射校验
```

验证失败时停止，不得制造形式上的 r2 Freeze。

### P0B-R2-06：冻结 r2

- 新建 `p0b-r2` manifest，冻结复用输入的哈希、r2 prompt、r2 源码、参数、媒体和
  ingest 哈希。
- 冻结后不得改源码、调 prompt、调 Gold、调问题、选择性重跑或覆盖失败结果。

### P0B-R2-07：正式 12 题运行

- 运行前必须再次获得 owner 对 12 次真实 DeepSeek 文本 API 调用的明确授权；
  当前任务发布不包含该费用/调用授权。
- 每题调用前先持久化该题 `retrieval.json`。
- 每题只有一个 `TRANSCRIPT_RETRIEVAL` 正式结果槽和一次应用级回答调用。
- DeepSeek 不得读取完整 transcript、Gold、answer points、r1 回答或人工标签。
- provider、schema、timeout、retrieval 等失败原样保留，不补跑、不覆盖。

### P0B-R2-08：评分、人工审核与报告

- 计算与 r1 完全同口径的 retrieval、回答/拒答、citation、schema、延迟和 token
  指标。
- 生成 12 题逐题人工语义审核材料。
- 在 `answer_point_coverage`、`fully_correct`、`fully_supported`、
  `semantic_support` 需要 owner 判断或授权时暂停。
- 人工审核完成后生成 r1→r2 对照，只比较同口径指标，不删除失败题。
- 发布最终 r2 报告并立即停止。

## 6.1 当前施工进度

- `P0B-R2-00`：已完成；r1 baseline commit 与保护哈希已记录在
  `docs/tasks/p0b-r2/r1-baseline.json`。
- `P0B-R2-01`：已完成；失败分析见 `docs/tasks/p0b-r2/failure-analysis.md`。
- `P0B-R2-02` 至 `P0B-R2-04`：已完成，当前改动为通用字符 2–4 gram TF-IDF
  查询视图/固定分数聚合、r2 拒答 prompt 和 revision-safe 路径隔离。
- `P0B-R2-05` 至 `P0B-R2-06`：已完成；`p0b-r2` manifest 已冻结并通过冻结复核。
- `P0B-R2-07`：已按 owner 授权执行一次；12/12 retrieval 先落盘，12/12 DeepSeek
  调用均原样记录为 `provider / APIConnectionError`，没有 raw response。
- `P0B-R2-08`：已完成自动评分和最终报告；由于没有成功回答，语义审核字段保持
  空值，不将本次运行判为通过。
- 当前状态为 `CLOSED / BLOCKED_EXECUTION_FAILURE`；不在本 revision 重试或覆盖结果。

## 7. 验收与状态

只有以下六项全部满足，且 owner 语义审核完成，才可记录
`P0B_R2_PASSED`：

- `QuestionHit@1 >= 6/9`；
- `QuestionHit@5 >= 8/9`；
- `AllEvidence@5 >= 2/3`；
- `FullySupportedAnswer >= 7/9`；
- `CorrectRefusal >= 2/3`；
- invalid citation provenance `= 0`。

若任何一项未通过，状态必须是 `P0B_R2_THRESHOLDS_NOT_MET`。不得用平均分、
主观“效果不错”或程序化 citation 合法性替代语义正确性，也不得自动开启 r3。

## 8. 必交付产物

- r1 可恢复 baseline commit 与保护哈希记录；
- `docs/tasks/p0b-r2/failure-analysis.md`；
- r2 prompt；
- revision-safe freeze/run/grade/report 实现与测试；
- r2 manifest；
- `artifacts/p0b/p0b-r2/` 下 12 份 retrieval、result、raw response 和人工审核材料；
- `reports/p0b-r2-retrieval-eval.json`；
- `reports/p0b-r2-retrieval-eval.md`；
- append-only 的 r2 决策与证据记录。

## 9. 本任务当前状态

当前为 `CLOSED / BLOCKED_EXECUTION_FAILURE`。r2 manifest 位于
`eval/p0b/revisions/p0b-r2/eval-manifest.json`，结果根目录为
`artifacts/p0b/p0b-r2/`，最终报告为 `reports/p0b-r2-retrieval-eval.md` 及其 JSON
文件。12 次真实调用已按授权执行且失败结果已锁定；不得在本 revision 重试、覆盖
或把检索开发指标冒充为 P0B 通过。未形成 `P0B_R2_PASSED`。
