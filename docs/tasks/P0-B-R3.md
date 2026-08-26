# P0-B R3 任务 Prompt：Execution-Only 最终补测

| 字段 | 内容 |
|---|---|
| 任务编号 | `P0-B-R3` |
| 发布状态 | `ISSUED_DOCUMENT_ONLY` |
| 当前授权 | 仅发布施工 Prompt；不包含外部 API 调用或正式运行授权 |
| 项目等级 | `G1 PROTOTYPE / L0 EXPLORATION` |
| 前置结果 | `p0b-r2 CLOSED / BLOCKED_EXECUTION_FAILURE` |
| 唯一目标 | 不改代码、不改检索、不改评测集，只在网络可用环境完成新的 12 题真实回答运行、评分和人工复核 |
| 停止点 | 生成 R3 报告并等待 owner 决定；不得进入 P1 |

## 1. 可直接交给施工 Session 的主指令

在 `/Users/tristana/Develop/video-evidence-agent` 中执行本文件定义的
`P0-B-R3 Execution-Only` 任务。

这是一次外部执行环境补测，不是新一轮算法开发。必须保留 `p0b-r1` 和
`p0b-r2` 的 manifest、retrieval、result、metrics、human-review、报告和失败状态。
不得重跑、覆盖或修饰 R2 的 12 个 `APIConnectionError`。

R3 必须创建新的 `p0b-r3` revision，完全复用 R2 的应用源码、TF-IDF retrieval
profile、R2 answer prompt、三个视频、127 个 VideoSegments、12 道问题和 Gold。
在执行正式 12 题之前，先在网络可用环境用 P0-A 开发样本完成一次可丢弃的真实
Chat Completion 预检，证明精确 endpoint、模型和结构化输出链路可用。

本任务发布本身不授权任何付费或外部模型调用。施工 Session 必须先展示预检方案、
调用上限和预计影响，并获得 owner 对“最多 1 次开发预检 + 12 次正式回答调用”的
明确授权。未获授权不得调用 provider。

所有正式调用完成后运行自动评分，生成 12 题人工语义审核材料并暂停。只有 owner
亲自填写语义标签，或在查看材料后明确授权施工 Session 代为记录标签，才能生成最终
Gate 报告。无论通过、未达线或再次阻塞，到报告和 owner 决策点立即停止。

## 2. 当前已验证事实

### 2.1 R1 历史结果

`p0b-r1` 已真实完成 12 次 DeepSeek 回答和 owner review，但冻结门槛未达到：

| 指标 | R1 |
|---|---:|
| QuestionHit@1 | 2/9 |
| QuestionHit@5 | 7/9 |
| AllEvidence@5 | 1/3 |
| MRR | 0.435185 |
| FullySupportedAnswer | 5/9 |
| CorrectRefusal | 2/3 |
| Invalid citation provenance | 0/9 |

R1 保持 `P0B_RETRIEVAL_THRESHOLDS_NOT_MET`，不得改写。

### 2.2 R2 已完成的改进

R2 只增加了通用、确定性的 lexical query views 和 score aggregation，并使用更明确的
拒答 prompt；未加入 Dense、Hybrid、Reranker、Embedding、VLM 或 Agent。

R2 冻结 retrieval 结果达到：

| 指标 | R2 retrieval | 门槛 |
|---|---:|---:|
| QuestionHit@1 | 6/9 | ≥ 6/9 |
| QuestionHit@5 | 9/9 | ≥ 8/9 |
| AllEvidence@5 | 2/3 | ≥ 2/3 |
| Gold evidence-unit recall@5 | 0.962963 | 记录项 |
| MRR | 0.805556 | 记录项 |

但 R2 的 12 次 DeepSeek 调用全部以 `APIConnectionError` 结束，因此答案、拒答、
schema、citation 和语义支持不可评估。R2 正式状态是：

```text
P0B_BLOCKED_EXECUTION_FAILURE
```

不能标记为 `P0B_R2_PASSED`。

### 2.3 已知连接诊断

- 沙箱内 outbound network 被 `PermissionError: [Errno 1] Operation not permitted` 拒绝。
- 网络可用环境中，无认证 endpoint 请求得到预期 HTTP 401。
- 使用项目 `.env` 的 authenticated `models.list()` 成功并返回 3 个模型。
- 以上只证明 endpoint 与 credential 可达；尚未证明当前精确模型的 Chat Completion、
  `AnswerProposal` schema 和 R2 prompt 在网络可用环境中可以成功执行。

### 2.4 当前代码基线

发布 R3 任务时已复核：

- 当前 HEAD：`7cedce5475b928ded3d7c071f09132963cd0f9fa`；
- R2 冻结 source commit：`3e280afc5d11a7976575ca0c8c660d6c79d70aaa`；
- 从 R2 source commit 到当前 HEAD，`src/`、`tests/`、`pyproject.toml`、`uv.lock`
  无差异；后续提交只是 R2 closeout/diagnosis 文档；
- 当前复核为 `28 passed`、Ruff clean、`git diff --check` clean；
- `p0b-r3` manifest、artifact root 和 report 路径均尚不存在；
- 工作树存在用户文件：`.DS_Store` 以及两个未跟踪 draft JSONL。不得擅自删除、提交
  或把它们纳入正式 R3 输入。

## 3. R3 固定输入与不变量

以下内容全部冻结，施工 Session 不得修改：

- `src/video_evidence_agent/`；
- `tests/`；
- `pyproject.toml` 和 `uv.lock`；
- `eval/p0b/corpus.jsonl`；
- `eval/p0b/questions.jsonl`；
- `eval/p0b/gold.jsonl`；
- `eval/p0b/prompts/transcript-retrieval-r2.md`；
- 三个现有中文技术视频的媒体哈希与时长；
- `artifacts/p0b-ingest/` 中 127 个 timestamped VideoSegments；
- ASR 模型、ASR 输出和 45/60 秒 segment 边界；
- R2 retrieval profile：`char_tfidf_2_4_query_views_v1`；
- R2 query-view weights、`sublinear_tf`、character 2～4 gram 和 `Top-K=5`；
- `gold_revision = p0b-r1`；
- DeepSeek 只读取“当前问题 + 当前 Top-5”的上下文边界；
- citation 必须来自当前 Top-5，quote 与时间戳由程序从源 segment 回填；
- P0-A、P0-B R1、P0-B R2 的所有历史工件和状态。

R3 不允许重新 ingest、重跑 ASR、重新切 segment、修改问题/Gold、改 prompt、改模型
参数、改 retrieval、改 schema 或修应用代码。

如果现有代码无法完成 R3，必须停止并报告新的明确代码缺口；不得在 execution-only
任务中顺手修复后继续跑正式集。

## 4. 允许写入的路径

只有施工正式开始后，才允许新增或追加：

- `eval/p0b/revisions/p0b-r3/eval-manifest.json`；
- `artifacts/p0b/p0b-r3/`；
- `reports/p0b-r3-retrieval-eval.md`；
- `reports/p0b-r3-retrieval-eval.json`；
- `docs/tasks/p0b-r3/` 下的执行证据；
- `docs/requirements/p0b/decision-evidence.jsonl` 的 append-only 记录；
- `docs/tasks/p0b/TASK.json`、`INTENT.json`、`CONTEXT.json`、`EVIDENCE.md` 中与 R3
  状态直接相关的最小追加/更新。

不得初始化新的治理体系或创建与现有 task/evidence 文件平行的事实源。当前没有
`.project-to-act` 配置；R3 继续使用仓库已有 `docs/tasks/p0b/` 和 decision ledger。

## 5. 明确禁止

- 不重跑或覆盖 `p0b-r2`。
- 不复制 R2 成功 retrieval 指标后直接手工填入 R3。
- 不修改 application source、tests、依赖或 lockfile。
- 不修改 R2 prompt、问题、Gold、答案要点、时间段或 Gold Segment IDs。
- 不加入 Dense、Hybrid、Reranker、Embedding、Query Rewrite 或邻接扩展。
- 不加入 OCR、VLM、Agent、LangGraph、FastAPI、数据库、Worker 或 UI。
- 不恢复 B0/Gemini/direct-video 路径；该路径已由 owner 明确 supersede。
- 不上传视频；provider 只能收到问题和当前 Top-5 transcript segments。
- 不把完整 transcript、Gold、answer points、R1/R2 回答或人工标签交给模型。
- 不使用 Mock、缓存答案或手工答案满足正式调用。
- 不选择性重跑失败题、不覆盖 provider/schema failure、不从多次输出中挑最好答案。
- 不因 R3 通过就宣称 Agent、视觉取证或跨数据集泛化已经得到证明。
- 不自动开启 P1、R4 或新 holdout 施工。

## 6. 施工顺序

### P0B-R3-00：只读接管与保护历史

施工 Session 首先读取：

- `docs/tasks/P0-B-R3.md`；
- `docs/tasks/p0b/TASK.json`；
- `docs/tasks/p0b/INTENT.json`；
- `docs/tasks/p0b/CONTEXT.json`；
- `docs/tasks/p0b/EVIDENCE.md`；
- `docs/requirements/p0b/decision-evidence.jsonl`；
- `eval/p0b/revisions/p0b-r2/eval-manifest.json`；
- `reports/p0b-r2-retrieval-eval.md` 和 `.json`；
- `artifacts/p0b/p0b-r2/run-manifest.json` 与 `metrics.json`。

随后：

- 复算 R2 manifest、run-manifest、metrics、报告和 12 个 retrieval/result 的哈希；
- 新建 `docs/tasks/p0b-r3/r2-baseline.json` 记录保护哈希；
- 确认 R3 三个目标路径尚不存在；
- 记录现有 dirty/untracked 文件，但不得删除或修改用户文件；
- 将现有 task 文件中的 R2 状态保留为 closed，并将 R3 标记为新的
  `ISSUED`/`IN_PROGRESS` follow-up；不能改写 R2 历史。

历史保护失败时立即停止。

### P0B-R3-01：离线验证

使用任务专用 uv cache，运行：

```bash
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run pytest -q
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run ruff check .
git diff --check
git diff --exit-code 3e280afc5d11a7976575ca0c8c660d6c79d70aaa..HEAD -- \
  src tests pyproject.toml uv.lock
jq -c . eval/p0b/corpus.jsonl
jq -c . eval/p0b/questions.jsonl
jq -c . eval/p0b/gold.jsonl
jq -c . docs/requirements/p0b/decision-evidence.jsonl
```

还必须只读验证：

- 3 个媒体哈希和时长；
- 3 个 ingest manifest 与 segments 哈希；
- 127 个非空、时间合法的 VideoSegments；
- 12 个问题与 12 个 Gold rows；
- 全部 Gold segment/time mappings；
- P0-A anchor hashes；
- R2 manifest pin 的 source file hashes。

任一项失败时停止；不得创建 R3 manifest。

### P0B-R3-02：外部调用授权 checkpoint

向 owner 明确报告：

- provider endpoint 和精确模型名；
- 将执行最多 1 次 P0-A 开发预检；
- 预检成功后将执行 12 次正式 R3 回答调用；
- 本任务新增外部回答调用总上限为 13 次；
- 视频不会上传；
- 正式调用每题一次，失败不重跑；
- 可能产生的 provider token/费用；
- 不会打印或提交 API key。

必须获得明确授权。`P0-B-R3.md` 的发布不等于调用授权。

### P0B-R3-03：网络可用环境中的一次开发预检

预检必须满足：

- 使用 P0-A 开发样本，不使用 P0-B 12 题作为连通性试探；
- 在 `/private/tmp` 创建可丢弃 artifact 副本；
- 不写入或覆盖 P0-A/R1/R2 项目工件；
- 使用项目当前 `.env` 的 endpoint、model 和 credential，但不打印敏感值；
- 真实执行一次 Chat Completion；
- 验证响应能解析为 `AnswerProposal`，并经过现有 Evidence Gate；
- 记录模型、状态、latency、usage 和错误类别，不保存密钥；
- 预检失败即停止，不冻结 R3，不尝试正式 12 题。

可以使用下面的隔离方式，具体临时目录名允许变化：

```bash
R3_PREFLIGHT_DIR=$(mktemp -d /private/tmp/video-evidence-r3-preflight.XXXXXX)
mkdir -p "$R3_PREFLIGHT_DIR/artifacts/chinese-lips-mini-val-kj-001"
cp artifacts/chinese-lips-mini-val-kj-001/manifest.json \
  artifacts/chinese-lips-mini-val-kj-001/segments.jsonl \
  "$R3_PREFLIGHT_DIR/artifacts/chinese-lips-mini-val-kj-001/"
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run video-evidence ask \
  chinese-lips-mini-val-kj-001 \
  --question "人工智能系统可以通过什么方式提高自身性能？" \
  --question-id p0b-r3-connectivity-preflight \
  --artifacts-dir "$R3_PREFLIGHT_DIR/artifacts"
```

该命令必须在获准的 network-enabled execution context 运行。预检成功只能证明外部回答
链可执行，不能计入正式 P0-B 分数。

### P0B-R3-04：冻结新的 R3 Revision

预检成功后，重新确认正式 R3 artifact root 和 manifest 不存在，再运行：

```bash
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run video-evidence p0b-freeze \
  --project-root . \
  --eval-revision p0b-r3 \
  --gold-revision p0b-r1 \
  --manifest-out eval/p0b/revisions/p0b-r3/eval-manifest.json \
  --answer-prompt eval/p0b/prompts/transcript-retrieval-r2.md
```

冻结后必须核对 manifest：

- `eval_revision = p0b-r3`；
- `gold_revision = p0b-r1`；
- `artifact_root = artifacts/p0b/p0b-r3`；
- `evaluation_method = TRANSCRIPT_RETRIEVAL`；
- `retrieval_profile = char_tfidf_2_4_query_views_v1`；
- prompt SHA-256 与 R2 一致；
- corpus/questions/Gold/media/ingest/source file hashes 与固定输入一致；
- 模型、temperature、timeout 和 response schema 与任务契约一致；
- P0-A anchor hashes 全部 verified；
- manifest 中没有 secret。

冻结后禁止修改任何 pin 项。若发现错误，关闭 R3 manifest 并报告；不得编辑 manifest
后继续。

### P0B-R3-05：正式 12 题运行

在与预检相同的 network-enabled context 中运行一次：

```bash
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run video-evidence p0b-run \
  --project-root . \
  --manifest eval/p0b/revisions/p0b-r3/eval-manifest.json
```

运行不变量：

- 每题先持久化 `retrieval.json`，再调用 answer provider；
- 每题只有一个正式 result slot 和一次应用级回答调用；
- 12 个问题必须全部留下 result；
- 任何 provider、schema、timeout、retrieval 或 ingest failure 原样保留；
- 不重跑、不覆盖、不补写答案；
- 记录真实 latency、usage 和模型信息；
- `mock_used = false`、`video_upload = false`。

若任何正式调用失败，仍完成 result ledger 和自动 grade，但 R3 必须关闭为
`P0B_BLOCKED_EXECUTION_FAILURE`；不能只补跑失败题。

### P0B-R3-06：自动评分

```bash
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run video-evidence p0b-grade \
  --project-root . \
  --manifest eval/p0b/revisions/p0b-r3/eval-manifest.json
```

自动评分后必须检查：

- 12/12 retrieval artifacts；
- 12/12 result artifacts；
- call status 与 failure 类型；
- retrieval 指标是否与冻结 R2 一致；
- schema compliance；
- answer/refusal status accuracy；
- citation provenance 与 temporal hit；
- latency 与 token usage；
- `human-review.json` 与 `.jsonl` 是否包含 12 行待审材料。

如果所有调用成功，预期状态应是 `AUTO_SCORED_PENDING_OWNER_REVIEW`，不能提前报告
P0-B 通过。

### P0B-R3-07：owner 语义审核 checkpoint

向 owner 展示每题：

- Question；
- Answer / `INSUFFICIENT_EVIDENCE`；
- Top-K Evidence；
- 程序回填 quote 和时间戳；
- Gold answer points；
- Gold evidence units；
- 自动 provenance/temporal 判定。

owner 需要判断：

- `answer_point_coverage`；
- `fully_correct`；
- `fully_supported`；
- `semantic_support`；
- 不可回答题是否确实正确拒答。

施工 Session 不得把 citation provenance 自动合法等同于语义支持。owner 如果希望
委托施工 Session 填写，必须在看到材料后明确授权，且委托记录要追加到 decision
ledger。审核未完成时停止在 `PENDING_OWNER_SEMANTIC_REVIEW`。

### P0B-R3-08：最终报告与 Gate

人工审核完成后运行：

```bash
UV_CACHE_DIR=/private/tmp/video-evidence-agent-uv-cache uv run video-evidence p0b-report \
  --project-root . \
  --manifest eval/p0b/revisions/p0b-r3/eval-manifest.json \
  --report reports/p0b-r3-retrieval-eval.md
```

确认同时生成：

- `reports/p0b-r3-retrieval-eval.md`；
- `reports/p0b-r3-retrieval-eval.json`；
- `artifacts/p0b/p0b-r3/metrics.json`；
- 完整 owner review artifacts。

最终六项 Gate：

| Gate | 通过线 |
|---|---:|
| QuestionHit@1 | ≥ 6/9 |
| QuestionHit@5 | ≥ 8/9 |
| Multi AllEvidence@5 | ≥ 2/3 |
| FullySupportedAnswer | ≥ 7/9 |
| CorrectRefusal | ≥ 2/3 |
| Invalid citation provenance | 0 |

状态规则：

- 任一正式 provider call 失败：`P0B_BLOCKED_EXECUTION_FAILURE`；
- 调用完成但 owner review 未完成：`PENDING_OWNER_SEMANTIC_REVIEW`；
- owner review 完成但任一门槛未达到：`P0B_RETRIEVAL_THRESHOLDS_NOT_MET`；
- 六项全部通过：`READY_FOR_OWNER_P0B_DECISION`。

`READY_FOR_OWNER_P0B_DECISION` 仍不是自动 P0-B passed。必须向 owner 报告全部指标、
失败案例、成本和限制，等待 owner 明确选择：

```text
P0B_PASSED_OWNER_ACCEPTED
P0B_THRESHOLDS_NOT_MET
P0B_BLOCKED
```

只有 `P0B_PASSED_OWNER_ACCEPTED` 才允许把 P0 标记为完成，并开始讨论 P1；它仍不
授权 P1 施工。

## 7. 必交付产物

- `docs/tasks/p0b-r3/r2-baseline.json`；
- preflight 证据记录，不含 secret；
- `eval/p0b/revisions/p0b-r3/eval-manifest.json`；
- `artifacts/p0b/p0b-r3/` 下 12 份 retrieval 与 result；
- `artifacts/p0b/p0b-r3/run-manifest.json`；
- `artifacts/p0b/p0b-r3/metrics.json`；
- `artifacts/p0b/p0b-r3/human-review.json` 和 `.jsonl`；
- `reports/p0b-r3-retrieval-eval.md` 和 `.json`；
- append-only decision/evidence 记录；
- `docs/tasks/p0b/` 中准确的 R3 task、status、evidence 和 handoff 状态。

## 8. 结论表述限制

即使 R3 六项 Gate 全部通过，报告仍必须明确：

- R2/R3 使用的是根据 R1 失败修订后的同一批 12 题，属于固定 regression set；
- 没有新的 unseen-video holdout，因此不能声称跨视频泛化已得到证明；
- B0/direct multimodal baseline 已被 owner supersede，本轮没有架构级 B0 vs B1 比较；
- 当前只验证 Chinese transcript evidence retrieval；
- 没有验证 OCR、VLM、Agent、LangGraph、Web/API、并发或生产可靠性；
- citation provenance 合法不自动代表 citation 语义支持；
- G1 小样本通过不是生产、商业或统计显著性结论。

## 9. 施工 Session 最终汇报格式

最终汇报必须先给 Gate 结论，再列：

1. 当前 revision、source commit 和 manifest hash；
2. 实际执行命令与退出码；
3. 预检结果和正式调用数；
4. 六项 Gate 的原始计数；
5. latency、token usage 和可获得成本；
6. provider/schema/retrieval/语义失败逐题清单；
7. owner review 状态；
8. 新增/修改文件；
9. dirty/untracked 用户文件是否保持未动；
10. 最终建议和下一阶段所需的 owner 明确决定。

不得只汇报“测试通过”“效果不错”或“可以进入 Agent”。
