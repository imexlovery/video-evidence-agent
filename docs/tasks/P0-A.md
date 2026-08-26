# P0-A 施工任务单：中文视频证据检索 Smoke Test

| 字段 | 内容 |
|---|---|
| 任务编号 | `P0-A` |
| 发布状态 | `REOPENED-R1` |
| 发布日期 | 2026-08-26 |
| 当前修订 | `R1 / DEC-P0A-011 / 2026-08-26` |
| 项目目录 | `/Users/tristana/Develop/video-evidence-agent` |
| 项目等级 | G1 可行性 Smoke Test，不是生产系统 |
| 输入规模 | 1 个中文技术视频 |
| 问题规模 | 3～5 个手工问题 |
| 唯一目标 | 验证“问题 → 视频真实时间段 → 证据约束回答”能否从真实 MP4 重复跑通 |
| 停止点 | P0-A 验收并提交 Smoke Report；不得自动进入 P0-B、P1 或 P2-lite |

## 1. 任务结论

本任务只施工下面这条链路：

```text
中文 MP4
  ↓
FFmpeg 提取音频
  ↓
中文 ASR + segment timestamps
  ↓
VideoSegment（保留真实时间边界）
  ↓
本地文本检索
  ↓
Top-K VideoSegments
  ↓
基于证据回答 / 拒答
  ↓
Answer + timestamp citations
```

P0-A 成功不代表产品完成，也不证明 Agent、视觉检索或向量检索有价值。它只回答一个问题：

> 对一段真实中文技术视频，仅使用 transcript evidence，系统能否找到支持问题的时间段，并输出可人工复核的带时间戳答案？

## 2. 冻结边界

### 2.1 本阶段必须完成

- 处理 1 个本地中文技术 MP4。
- 使用 FFmpeg 提取单声道 16 kHz 音频。
- 生成带真实起止时间的中文 ASR 结果。
- 将 ASR 结果构造成稳定、可检索的 `VideoSegment`。
- 对 3～5 个问题返回 Top-K 证据片段。
- 仅依据 Top-K 证据生成答案。
- 输出 `segment_id`、`start_ms`、`end_ms` 和源 transcript quote。
- 对缺少充分证据的问题返回 `INSUFFICIENT_EVIDENCE`。
- 保留一次真实运行的中间产物和人工复核报告。

### 2.2 明确禁止进入本阶段

- Agent、Planner、Critic、LangGraph 或 Tool Calling。
- OCR、关键帧理解、VLM、Gemini Vision 或任何视觉补充解析。
- FastAPI、React、SSE 或其他 Web/UI 层。
- PostgreSQL、pgvector、Redis、MQ、Worker 或对象存储。
- Checkpoint、Retry 编排、幂等、故障恢复、背压或 Tool Trace。
- 多视频索引或跨视频查询。
- Hybrid Retrieval、Reranker 或远程向量数据库。
- 正式 3 视频/12 题 Benchmark。
- B0 Direct Multimodal 与 B1 Transcript Retrieval 对照实验。
- DOVideo-AI 的 Java → Python 逐模块翻译。

以上内容只能在 P0-A 报告完成、用户明确批准 P0-B 或后续阶段后再开工。

## 3. 技术决策

### 3.1 已冻结的契约

最小领域对象：

```python
class VideoSegment:
    video_id: str
    segment_id: str
    ordinal: int
    start_ms: int
    end_ms: int
    transcript_text: str
```

必须保持以下不变量：

- `0 <= start_ms < end_ms`。
- 同一视频内 `ordinal` 从 0 连续递增。
- segment 按时间单调排列，不允许重叠。
- `segment_id` 在相同输入和切分参数下稳定。
- `start_ms` 来自第一个被合并 ASR segment 的真实开始时间。
- `end_ms` 来自最后一个被合并 ASR segment 的真实结束时间。
- 检索、回答和引用始终传递完整 `VideoSegment`，不得退化成无时间边界的普通文本 chunk。

外部回答契约：

```json
{
  "status": "ANSWERED",
  "answer": "讲者建议在召回阶段先使用混合检索。",
  "evidence": [
    {
      "segment_id": "smoke-001-seg-018",
      "start_ms": 312000,
      "end_ms": 347000,
      "quote": "该 segment 中的原始 transcript_text"
    }
  ]
}
```

拒答契约：

```json
{
  "status": "INSUFFICIENT_EVIDENCE",
  "answer": null,
  "evidence": []
}
```

### 3.2 P0-A 暂定实现

这些选择服务于快速验证，不视为长期架构结论：

- Python 3.12，由 `uv` 管理项目 `.venv` 和 `uv.lock`。
- Apple Silicon 上优先使用 `mlx-whisper` 做本地中文 ASR。
- ASR 模型先以准确率优先；若本机资源或耗时不合适，可降至较小模型，但必须在报告记录模型与原因。
- segment 采用 ASR 边界合并：目标约 45 秒、最大约 60 秒、无重叠；不得按固定字符数伪造时间边界。
- 首版检索采用 character n-gram TF-IDF（2～4 gram）+ cosine similarity。
- 默认 `Top-K = 5`，保存原始分数和排序，不设置未经校准的相似度阈值。
- 回答模型通过一个最小接口调用；具体供应商由施工时现有凭证决定，不允许静默退回 Mock。
- quote 由程序从被引用 `VideoSegment.transcript_text` 回填，不允许模型自由编造引用原文。

只有出现明确失败证据时才调整上述参数，并在 Smoke Report 记录“失败现象 → 调整 → 结果”。

## 4. 输入与前置条件

### 4.1 视频选择标准

选择 1 个满足以下条件的中文技术视频：

- 建议 20～60 分钟。
- 以中文口语为主，背景噪声不过重。
- 有足够技术密度和明确时间线。
- 问题能够主要依据口播内容回答。
- 本地使用和项目演示具有合法来源；不要提交受限原始视频。
- 不包含个人隐私、公司机密或求职敏感材料。

推荐内容类型：中文 AI/LLM 课程、开发者演讲、产品技术发布或公开技术会议录像。

### 4.2 本机前置状态

已知发布时状态：

- 机器架构：Apple Silicon `arm64`。
- `uv` 已安装。
- 系统 Python 版本不作为项目运行时；项目必须由 `uv` 固定 Python 3.12。
- FFmpeg 尚未安装，属于 P0-A 开工阻塞项。
- ASR 模型权重和 Python 依赖尚未下载。

安装 FFmpeg、下载依赖/模型和使用外部文本模型前，施工者应遵守当前环境的权限与密钥规则；不得在日志或仓库中写入凭证。

## 5. 目标目录与产物

施工后的最小结构：

```text
video-evidence-agent/
├── pyproject.toml
├── uv.lock
├── README.md
├── .gitignore
├── src/
│   └── video_evidence_agent/
│       ├── cli.py
│       ├── audio.py
│       ├── asr.py
│       ├── segments.py
│       ├── retrieval.py
│       ├── answering.py
│       ├── evidence.py
│       └── schemas.py
├── tests/
├── eval/
│   └── p0a/
│       └── questions.jsonl
├── artifacts/                 # 默认不提交大型运行产物
│   └── smoke-001/
│       ├── manifest.json
│       ├── audio.wav
│       ├── asr.json
│       ├── segments.jsonl
│       ├── retrieval/
│       └── answers/
├── reports/
│   └── p0a-smoke-report.md
└── docs/
    ├── requirements/p0a/decision-evidence.jsonl
    └── tasks/P0-A.md
```

原始 MP4、WAV、模型权重、密钥和大型运行产物必须进入 `.gitignore`；可提交脱敏、小体积的结构示例和报告。

## 6. 施工任务

### P0A-00：样本与问题集

**目标**

锁定一个适合 transcript evidence 验证的真实中文视频，并形成最小问题集。

**施工内容**

- 选择并登记 `video_id = smoke-001`。
- 记录视频来源、时长、文件哈希和使用说明。
- 手工设计 3～5 个问题，至少包括：
  - 2 个单片段可回答事实题；
  - 1 个同义改写题，问题措辞不直接复制 transcript；
  - 1 个确实不可回答的问题；
  - 可选 1 个相邻片段才能完整回答的问题。
- 为每题记录一个非正式的 `expected_interval` 和 `should_answer`，仅供 Smoke 人工判断，不称为正式 Gold Label。

**产物**

- `eval/p0a/questions.jsonl`
- `artifacts/smoke-001/manifest.json`

**验收**

- 问题均由人看过原视频后编写。
- 可回答题确实可从口播得到答案。
- 不可回答题不能仅凭常识补全。
- 原始媒体没有进入版本控制。

### P0A-01：Python/uv 最小工程

**目标**

建立独立于 DOVideo-AI 的 Python 工程和可复制运行入口。

**施工内容**

- 使用 `uv` 固定 Python 3.12，创建项目内 `.venv`。
- 只添加 P0-A 必需依赖。
- 生成并保留 `uv.lock`。
- 配置 `pytest` 和 `ruff`。
- 提供 `.env.example`，并允许本地 `.env` 由 CLI 自动加载；两者都不得包含或提交真实 key。

**允许的依赖类别**

- ASR：`mlx-whisper`。
- 数据契约：`pydantic`。
- 文本检索：`scikit-learn`。
- 文本模型：一个最小官方或 OpenAI-compatible SDK。
- 测试/检查：`pytest`、`ruff`。

**本阶段不引入**

- LangChain、LangGraph、sentence-transformers、FAISS、Qdrant。
- FastAPI、SQLAlchemy、Celery、Dramatiq、Redis client。

**验收**

- 在干净 shell 中可用 `uv sync --locked` 重建环境。
- `uv run pytest` 和 `uv run ruff check .` 有明确入口。
- `.venv` 未进入版本控制。

### P0A-02：FFmpeg 音频提取

**目标**

将真实 MP4 确定性地转换为 ASR 输入音频。

**施工内容**

- 验证 FFmpeg 可用后再运行。
- 输出 mono、16 kHz PCM WAV。
- 使用 subprocess 参数数组，不拼接不可信 shell 字符串。
- 记录命令参数、输入哈希、输出路径和运行状态到 manifest。
- 对文件不存在、无音轨、FFmpeg 非零退出和空输出显式失败。

**产物**

- `artifacts/smoke-001/audio.wav`
- 更新后的 `manifest.json`

**验收**

- WAV 可被 FFprobe/FFmpeg 识别为 mono 16 kHz。
- 输出非空且时长与视频音轨基本一致。
- 失败时返回非零状态，不生成“成功”记录。

### P0A-03：中文 ASR 与时间戳

**目标**

生成中文 transcript，并保留 ASR segment 的真实起止时间。

**施工内容**

- 显式设置中文识别，不在本阶段评估多语言。
- 先转写前约 5 分钟做质量/耗时检查，再运行完整视频。
- 保留 ASR 原始输出，不覆盖或人工润色源结果。
- 记录 ASR engine、模型、语言、参数和运行耗时。
- 人工抽查视频开始、中段、结尾各至少一处。
- 将明显错误、专有名词问题和时间漂移写入报告。

**产物**

- `artifacts/smoke-001/asr.json`

**验收**

- 每个 ASR segment 至少包含 `start`、`end`、`text`。
- 时间戳非负、递增且 `start < end`。
- 中文文本非空，抽样内容与音频大意一致。
- 报告明确区分“ASR 原文”和“人工观察”，不偷偷修 transcript。

### P0A-04：VideoSegment 构建

**目标**

把细粒度 ASR segment 合并成带真实时间边界的检索单元。

**施工内容**

- 按时间排序 ASR segments。
- 使用可配置的目标时长 45 秒、最大时长 60 秒进行无重叠合并。
- 只在 ASR segment 边界处切分；若单个 ASR segment 超过上限，保留其真实范围。
- 标准化空白，但不改写语义、不做 LLM 摘要。
- 生成稳定 ID，例如 `smoke-001-seg-018`。
- 将切分参数记录到输出元数据或 manifest。

**产物**

- `artifacts/smoke-001/segments.jsonl`

**验收**

- 每行符合 `VideoSegment` 契约。
- 时间单调、不重叠、文本非空、ID 唯一。
- 任意 segment 可映射回原始 ASR segment 和视频区间。
- 用相同输入和参数重复运行，ID 与边界一致。

### P0A-05：本地文本检索

**目标**

在不引入向量数据库的情况下，验证问题能否召回正确时间段。

**施工内容**

- 对 `transcript_text` 建立 character n-gram TF-IDF 索引。
- 使用 cosine similarity 排序。
- 默认返回 Top-5；segment 少于 5 个时返回全部。
- 返回完整 segment 元数据和未经隐藏的检索分数。
- 在回答模型运行前先持久化每题原始 Top-K，防止答案阶段掩盖检索失败。

**产物**

- `artifacts/smoke-001/retrieval/<question_id>.json`

**验收**

- 3～5 个问题均能产生可复核的排序结果。
- 结果中的文本、ID 和时间边界与 `segments.jsonl` 完全一致。
- 不对失败题手工插入正确 segment。
- 不把模型最终答案当作 retrieval 命中证明。

### P0A-06：证据约束回答与 Evidence Gate

**目标**

只使用当前问题的 Top-K segments 回答，并使引用可由程序验证来源。

**施工内容**

- 给回答模型的上下文只包含问题和 Top-K segments。
- 要求模型返回：`status`、`answer`、`citation_segment_ids`。
- 模型只能引用当前 `video_id`、当前问题 Top-K 中存在的 ID。
- 由确定性代码根据 ID 回填 `start_ms`、`end_ms` 和完整源 transcript quote。
- 下列情况统一降级为 `INSUFFICIENT_EVIDENCE`：
  - 模型声明证据不足；
  - `ANSWERED` 但没有 citation；
  - citation ID 不存在或不属于当前 Top-K；
  - 引用无法映射回原始 segment。
- P0-A 的 Gate 只验证引用来源和结构，不声称自动完成语义蕴含判断；语义支持由 Smoke 人工审查。

**产物**

- `artifacts/smoke-001/answers/<question_id>.json`

**验收**

- 可回答题至少有一个来自 Top-K 的合法引用。
- quote 由程序从源 segment 取得，不采用模型生成的“引文”。
- 非法 citation 测试会被拒绝。
- 不可回答题不依赖模型常识强行回答。
- 未配置真实模型时显式失败，不静默改成 Mock 并宣称 E2E 成功。

### P0A-07：CLI 串联真实链路

**目标**

提供无需 Web 服务的可重复端到端入口。

**命令契约**

```bash
uv run video-evidence ingest <video-path> --video-id smoke-001
uv run video-evidence ask smoke-001 --question "..." --top-k 5
```

可以增加 `smoke` 命令批量运行问题集，但不得因此引入任务队列或服务层。

**验收**

- `ingest` 串联音频、ASR、segment 和索引。
- `ask` 先保存 retrieval，再保存 answer。
- 终端结果包含可读时间戳，例如 `05:12–05:47`，同时 JSON 保留毫秒整数。
- 同一个 artifact 目录可被再次查询，不要求重新转写视频。
- 任一步失败时 CLI 返回非零退出码并指出失败阶段。

### P0A-08：最小自动化测试

**目标**

保护时间边界、检索和 citation provenance 三个核心契约。

**至少覆盖**

- ASR segment 合并后的时间单调与不重叠。
- stable segment ID 与真实首尾时间继承。
- 使用合成中文 segments 的检索 Top-K 测试。
- citation 只允许来自当前 Top-K。
- citation quote 从原 segment 确定性回填。
- 空 citation、越界 ID、跨视频 ID 均降级为 `INSUFFICIENT_EVIDENCE`。
- FFmpeg/ASR 子进程失败不会生成伪成功 manifest。

**验收**

- `uv run pytest` 通过。
- `uv run ruff check .` 通过。
- 测试不依赖真实 API key 或重复下载 ASR 模型。
- 自动化测试通过不替代真实 MP4 Smoke Run。

### P0A-09：真实 Smoke Run 与报告

**目标**

用同一个真实视频和冻结问题集给出 P0-A 是否成立的证据。

**报告逐题记录**

| 字段 | 说明 |
|---|---|
| question_id | 问题编号 |
| question | 原问题 |
| should_answer | 人工预期是否可回答 |
| expected_interval | 非正式人工参考区间 |
| top_1 | Top-1 segment 与分数 |
| top_5_hit | Top-5 是否覆盖预期区间 |
| final_status | `ANSWERED` / `INSUFFICIENT_EVIDENCE` |
| citation_valid | 引用来源是否合法 |
| human_supported | 引用是否真正支持答案 |
| notes | ASR、切分、检索或回答问题 |

**报告还必须包含**

- 视频、音频、ASR 模型和切分参数。
- 每阶段实际耗时。
- 开始/中段/结尾的 ASR 人工抽查结论。
- 至少一个成功案例的完整 `question → Top-K → answer → evidence`。
- 不可回答题的真实结果。
- 已知失败和 transcript-only 边界。
- 是否建议进入 P0-B，以及该建议的证据。

**产物**

- `reports/p0a-smoke-report.md`
- README 中的复现命令与 P0-A 范围声明。

## 7. 执行顺序与关卡

严格按以下顺序施工，不并行堆叠未验证层：

```text
Gate A：样本/问题冻结
  ↓
Gate B：FFmpeg 真实音频成功
  ↓
Gate C：中文 ASR + timestamps 人工抽查可用
  ↓
Gate D：VideoSegment 边界测试通过
  ↓
Gate E：所有问题的原始 Top-K 已保存
  ↓
Gate F：证据约束回答和拒答路径通过
  ↓
Gate G：真实 Smoke Report 完成
  ↓
STOP，等待用户决定是否进入 P0-B
```

上一关失败时，先修复或记录该层，不允许用后续模型能力遮盖问题。

## 8. P0-A Definition of Done

只有以下条件全部满足，P0-A 才可标记完成：

- [ ] 独立 Python/uv 项目可从锁文件重建。
- [ ] FFmpeg 对真实中文 MP4 成功提取可验证音频。
- [ ] 完整视频生成中文 ASR 和真实 segment timestamps。
- [ ] `segments.jsonl` 满足时间、ID、顺序和非空契约。
- [ ] 3～5 个冻结问题均保存原始 Top-K 结果和分数。
- [ ] 至少一个可回答题从真实 MP4 跑到合法带时间戳答案。
- [ ] 所有输出 citation 都来自该问题的 Top-K。
- [ ] 所有 quote 都由程序从原始 segment 回填。
- [ ] 至少一个不可回答题实际走过拒答路径，或报告如实记录其失败。
- [ ] 自动化测试和静态检查通过。
- [ ] 人工检查 ASR、Top-K 和 citation 是否真正支持回答。
- [ ] `p0a-smoke-report.md` 完成并给出是否进入 P0-B 的证据化建议。
- [ ] 没有将 Mock、合成测试或 README 描述包装为真实 E2E 证据。
- [ ] 没有施工任何 P0-A 排除项。

## 9. 不予验收的情况

出现任一项即不能宣称 P0-A 完成：

- 只有架构图、README、伪代码或 Mock 输出。
- 只处理现成字幕，没有从真实 MP4 执行音频提取和 ASR。
- ASR 有文本但没有可追溯的真实时间边界。
- 检索结果没有保存，直接让大模型看全文后回答。
- 时间戳由模型猜测或由固定字符比例推算。
- citation 不属于当前 Top-K，或 quote 是模型生成文本。
- 没有人工复核 retrieval 命中和 evidence support。
- 为修复一个 Smoke 失败提前加入 Agent、VLM、向量数据库或异步基础设施。
- 未配置真实模型时静默使用 Mock，却报告端到端成功。

## 10. 失败分支与允许调整

| 失败现象 | P0-A 内允许动作 | 当前禁止动作 |
|---|---|---|
| ASR 明显不可读 | 换更清晰视频、调整/更换 ASR 模型并记录 | 加 VLM/OCR 掩盖 ASR |
| 时间戳漂移 | 检查音频、ASR 参数和时间换算 | 手工伪造时间戳 |
| segment 过碎/过宽 | 调整 45/60 秒合并参数并重跑 | 引入复杂语义切分 Agent |
| 同义问题 Top-K 未命中 | 记录 lexical retrieval 失败，保留为 P0-B 决策证据 | 立即扩成 Hybrid/Reranker 大工程 |
| 模型忽略证据 | 收紧输出 schema、prompt 和确定性 Gate | 增加 Planner/Critic 多 Agent |
| 问题需要画面才能回答 | 标记为 transcript-only 边界或换题 | 在 P0-A 加 VLM |
| 运行缓慢 | 记录阶段耗时、缩短开发期样本 | 加 Worker/MQ/SSE |
| 不可回答题被强答 | 收紧拒答 prompt，保留失败证据 | 隐藏或删除失败题 |

## 11. P0-A 完成后的唯一决策

任务完成后只提交下面三选一建议，不直接开工：

1. `PROCEED_TO_P0_B`：链路可行，值得扩为 3 个中文视频/12 题正式 Retrieval Eval。
2. `REVISE_P0_A`：链路基本可行，但 ASR、切分、检索或拒答有明确可修问题。
3. `STOP_PROJECT`：核心证据检索价值不足，或成本/质量不值得继续。

只有用户明确选择进入 P0-B 后，才能讨论 embedding、hybrid、reranker 和 B0/B1 对照；只有 P0-B 证明 transcript retrieval 的边界后，才讨论 P1 Agent/VLM。

## 12. R1 Scope Reopen：Chinese-LiPS-mini

本节由 `DEC-P0A-011` 授权，自 2026-08-26 起成为 P0-A 当前范围；与本节冲突的原始样本选择、问题编写、人工观看和产物路径条款保留为 R0 历史，但不再控制当前施工。P0-A 的唯一目标、transcript-only 边界、Evidence Gate、禁止项和停止点不变。

### 12.1 变更原因

R0 要求人类先完整观看一段 20～60 分钟视频再编写问题，人工成本与 G1 Smoke 不成比例。Chinese-LiPS 提供短片、人工 transcript、说话人/主题和官方 split，可将人工工作缩减为抽查少量 clips 与审核问题候选，同时继续验证真实 MP4、ASR、检索、回答和时间戳证据链路。

### 12.2 冻结样本契约

- 数据源：`BAAI/Chinese-LiPS`；CC BY-NC-SA 4.0 及数据集附加访问条款。
- 用户已于 2026-08-26 声明本人接受访问条款；施工不得代替用户作身份、机构或授权声明。
- 下载前必须记录数据集不可变 revision；验收证据不得只引用浮动的 `main`。
- split：只使用 `validation`；P0-A 不训练模型，不下载 train/test 媒体。
- topic：`KJ`（Science & Technology）。
- speaker：从 validation/KJ 中按确定性规则选择一个拥有足够连续 clips 的说话人。
- clip 数：30；按 clip ID 数字后缀升序排列，不按 transcript 内容挑选容易样本。
- 新 `video_id`：`chinese-lips-mini-val-kj-001`；不得复用旧 `smoke-001` 工件。
- 将 30 个 clips 合成为一个约 5 分钟 MP4；不使用其视觉内容回答问题，PPT/OCR/VLM 仍在 P0-A 范围外。

### 12.3 小流量与失败关闭

- 先只下载 `meta_valid.csv`，冻结 split、topic、speaker、clip ID 和路径。
- 优先从 `processed_val.zip` 远程读取 ZIP central directory，再只提取选中 entries。
- 选择 entry 的压缩后总量上限为 64 MiB；超过预算、服务端不支持范围读取、鉴权失败或工具将退化为下载完整包时立即停止。
- 下载完整约 546 MB 的 `processed_val.zip` 需要新的用户确认；不得静默下载 train、test、原始高分辨率包或完整仓库。
- 所有数据集媒体、transcript、metadata 子集、问题和派生物只能保存在已忽略的 `artifacts/`；公开文件只保存 schema、聚合指标、哈希、clip ID 和不含受限原文的证据摘要。

### 12.4 新增本地工件契约

以下路径均位于 `artifacts/chinese-lips-mini-val-kj-001/`，不进入版本控制：

```text
source/
  meta_valid.csv
  selected-clips.json
  extracted/                # 仅 30 个选中 clips 所需媒体/标注
composite.mp4
ground-truth.jsonl          # clip_id、start_ms、end_ms、gt_text、源路径与哈希
cer.json                   # 聚合与逐 clip 指标，不复制 transcript 原文
review-clips/              # 仅供本地人工抽查的 3 个短 MP4
questions.candidates.jsonl  # 自动生成、尚未人工确认
questions.jsonl             # 人工确认后的 3～5 题
manifest.json
```

`ground-truth.jsonl` 必须满足：clip 时间单调、无重叠、ID 唯一、首段从 0 开始、末段与 composite 时长基本一致；任意问题的 `expected_interval` 必须来自支持 clip 的真实合成边界。

### 12.5 ASR 与问题 Gate 修订

- 仍必须从真实 composite MP4 提取 mono 16 kHz WAV 并运行中文 ASR；不得直接把官方 transcript 当作检索结果。
- 官方 transcript 只作为本地受限 ground truth，用固定 normalization 计算整体与逐 clip CER；不得人工润色 ASR 原文。固定 normalization 为 Unicode NFKC、casefold、OpenCC `t2s` 繁转简、只保留 Unicode 字母与数字；同时保留不做繁转简的字形敏感 CER，不能用 normalization 覆盖原始输出差异。
- 逐 clip CER 将每个 ASR segment 唯一分配给时间重叠最大的 clip；整体 CER 直接比较完整顺序文本，不依赖该分配。
- 人工 ASR 审核改为固定随机种子抽取至少 3 个 clips，对照短片与 transcript；不要求完整观看 composite。
- 可回答问题可以从 ground-truth transcript 自动生成候选，但必须绑定支持 clip ID 与 expected interval，并由人类逐题确认后才能进入 `questions.jsonl`。
- 问题集仍为 3～5 题：至少 2 个单 clip 可回答题、1 个同义改写题、1 个不可回答题；不可回答题不得仅凭常识补全。
- 人工复核仍必须检查所有问题的 Top-K、答案和 citation 语义支持；自动 CER、引用来源验证或问题生成都不能替代该复核。

### 12.6 R1 Gate 状态

- Scope Reopen：`CONFIRMED`，证据 `DEC-P0A-011`。
- Gate A：`HUMAN_CONFIRMED`；dataset revision、30 个 clip ID、ground-truth 边界、3 个短片抽查和 4 题问题集均已确认。
- Gate B～D：`AUTOMATED_PASS|HUMAN_CONFIRMED`；Gate E/F/G 已完成真实 Top-K、DeepSeek 回答、Evidence Gate 和最终报告，用户已批准封存并停止在 P0-A；R0 的任何通过结果均保持 `RETIRED`。
- P0-A 风险等级仍为 G1/L0；完成后仍必须 STOP，等待用户三选一决定。
