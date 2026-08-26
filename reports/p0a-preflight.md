# P0-A 施工预检记录

- 状态：COMPLETE_STOPPED_P0A — DeepSeek Smoke、答案/citation 复核和最终报告均已封存
- 范围：仅 P0-A 中文视频 transcript evidence smoke test
- 停止点：不得进入 P0-B、P1 或 P2-lite

本记录区分已退役的历史运行、自动化验证与仍需人类完成的 Gate。它不是
`p0a-smoke-report.md`，不构成完整 P0-A 验收结论。

## 已退役的历史运行证据

| 字段 | 结果 |
| --- | --- |
| 证据 ID | `E-P0A-INGEST-20260826-001`（RETIRED，不再满足当前样本 Gate） |
| 输入样本 | `/private/tmp/wikidata-cross-domain-forum-5.mp4`（27 MB，本地未提交） |
| 来源 | `https://commons.wikimedia.org/wiki/File:Wikidata_Cross-Domain_Forum_5.webm` |
| 授权 / 署名 | CC BY-SA 4.0 / Wikidata Taiwan / Allenwang6212a |
| 输入 SHA-256 | `6b6f9e381b34ccf537674adaff50f9b6ab042dd94babea64d6228663ad5420bd` |
| 视频时长 | 2,728,693 ms（45:28） |
| 音频产物 | `artifacts/smoke-001/audio.wav`；1 channel、16,000 Hz、2,728,689 ms |
| ASR | `mlx-whisper` / `mlx-community/whisper-small-mlx` / `zh`；1,802 个可检索 ASR segments |
| VideoSegment | `artifacts/smoke-001/segments.jsonl`；60 个，连续 ordinal、无重叠、最长 49,000 ms |
| ingest 结果 | 成功；完整运行耗时约 80 秒（含 5 分钟 ASR preview 和完整 ASR） |

原始 MP4 已按用户要求从 `/private/tmp/wikidata-cross-domain-forum-5.mp4` 删除；删除不可在本机恢复，但公开来源可重新取得。派生的 WAV、ASR、segments 和 manifest 暂留在被忽略的 `artifacts/smoke-001/` 下，仅用于解释历史运行，不得作为新样本的 Gate 证据。

## 已完成的工程与自动化证据

| 检查 | 结果 | 说明 |
| --- | --- | --- |
| Python 项目与锁文件 | 通过 | Python 3.12；`pyproject.toml` 与 `uv.lock` 已包含 Hugging Face range read 和 OpenCC CER normalization 依赖。 |
| 静态检查 | 通过 | `uv run ruff check .`：All checks passed。 |
| 自动化契约测试 | 通过 | `uv run pytest -q`：18 passed。覆盖确定性数据选择、ZIP entry 预算、CER normalization、浮点边界噪声、真实重叠 fail-closed、segment 稳定 ID、TF-IDF 排序、citation provenance 和失败 manifest。 |
| FFmpeg/FFprobe | 通过 | Homebrew FFmpeg 9.0.1 可用。 |
| P0A-02 历史音频提取 | RETIRED | 旧样本曾通过 FFprobe；新 Chinese-LiPS-mini 样本必须重跑。 |
| P0A-03 历史中文 ASR | RETIRED | 旧样本 ASR 不再属于当前样本路线。 |
| P0A-04 历史 VideoSegment 构建 | RETIRED | 旧样本 60 个 segments 仅保留为历史工程证据。 |

## Chinese-LiPS-mini R1 自动化证据

| 字段 | 当前结果 |
| --- | --- |
| 数据集版本 | `BAAI/Chinese-LiPS@db96948538811029011eee44602438a26710ecd9` |
| 元数据 | validation `meta_valid.csv`；SHA-256 `29b5ed52e4ec3a44de3284a81362165c4088e18973fe301d286282a471edcec9` |
| 确定性选择 | `KJ` / `127_21_M_KJ` / clip `_001`～`_030`，共 30 个，不按 transcript 内容挑选 |
| 小流量读取 | `processed_val.zip` 中 60 个所需 WAV/MP4 entries；压缩后 7,637,689 bytes，未下载完整 546 MB archive |
| 合成视频 | 269,492 ms；SHA-256 `1599fed5b62fdc2b973ce4daf0f441d159124692775404935d6888191906c704`；H.264 96×96 + AAC mono 16 kHz |
| 音画边界 | 视频轨 269,480 ms，音频轨 269,492 ms，差 12 ms；已移除会累计 AAC padding 的旧逐段中间合成物 |
| 真实 ASR | `mlx-whisper` / `mlx-community/whisper-small-mlx` / `zh`；95 个原始时间片，6 个 VideoSegments；完整 ASR 7,326 ms |
| ASR 末端 | 最后 ASR `end_ms=269500`，与容器时长差 8 ms；无空、非正或亚毫秒丢弃项 |
| CER | OpenCC `t2s` 归一化整体 4.89%（62/1,268）；字形敏感整体 39.43%（500/1,268）；两者均保存在 `cer.json` |
| 候选题 | 4 题：3 个可回答（含 1 个同义改写）+ 1 个不可回答；用户已确认，正式 `questions.jsonl` 已冻结 |
| 正式问题集 | `questions.jsonl` SHA-256 `03d5256397c9af3dc7ec5311c3e9526f84942577f75eb2b9ec1125279db317d4`；3 answerable + 1 unanswerable |
| 短片复核量 | 3 个本地 MP4，分别 8.46、11.05、6.25 秒，总计约 25.75 秒 |

## DeepSeek Smoke 与报告证据

| 字段 | 当前结果 |
| --- | --- |
| API 配置 | `.env` 自动加载；DeepSeek `https://api.deepseek.com` / `deepseek-v4-flash`；Key 存在性已布尔核验，不写入报告 |
| Smoke | `smoke-run.json`：4/4 无运行失败；3 `ANSWERED` + 1 `INSUFFICIENT_EVIDENCE` |
| 检索 | 4 个问题均保存原始 Top-5 与分数；所有命中属于 `chinese-lips-mini-val-kj-001` |
| Citation Gate | 3 个回答的 citation 均在各自 Top-5，quote 由程序从 `VideoSegment` 回填；不可回答题走真实拒答路径 |
| 报告 | `reports/p0a-smoke-report.md` 已封存为 `FINAL`；三个问题短片和四题答案/citation 均标记 `CONFIRMED` |

中途保留了一次 `asr_full` fail-closed 事实：相邻 Whisper 时间边界因二进制浮点产生 `1.42e-14` 秒伪重叠。修复只容忍绝对值不超过 `1e-9` 秒的边界噪声；100 ms 真实重叠仍由测试确认会拒绝。

## Gate 状态

| Gate | 状态 | 事实与解除条件 |
| --- | --- | --- |
| A：样本与问题冻结 | HUMAN_CONFIRMED | 用户确认四题和三个短片；dataset revision、30 个 clip ID、ground-truth 边界与 `questions.jsonl` 均已固定。 |
| B：真实音频提取 | AUTOMATED_PASS | 真实 composite 已提取 16 kHz mono WAV；source hash、命令、时长和轨道探测已保存。 |
| C：中文 ASR 与质量核对 | HUMAN_CONFIRMED | 用户确认三个短片；真实 ASR 与两种 CER 已保存，不要求观看完整 composite。 |
| D：VideoSegment 边界 | AUTOMATED_PASS | 6 个连续 ordinal、无重叠 VideoSegments；时间来自 95 个真实 ASR 时间片。 |
| E：所有问题原始 Top-K | AUTOMATED_PASS | 4/4 问题的 Top-5 已持久化，含分数和时间边界。 |
| F：真实回答与 Evidence Gate | AUTOMATED_PASS | DeepSeek 真实调用完成；3 个合法回答 + 1 个真实拒答，citation provenance 全部通过。 |
| G：真实 Smoke Report | PASSED_USER_CONFIRMED | `reports/p0a-smoke-report.md` 已封存为最终证据；用户批准停止在 P0-A。 |

## Chinese-LiPS-mini R1 路线（已确认）

- 官方仓库约 93.1 GB；不下载全量。
- P0-A 不训练模型，因此不需要同时取得 train、validation 和 test 媒体。
- 建议只从 `validation` 的 `KJ`（Science & Technology）主题、一个说话人中确定性抽取约 30 个按原序排列的 clips，平均约 5 分钟。
- 先取得 555 kB 的 `meta_valid.csv`，冻结 clip ID、人工 transcript、split、speaker 和 topic；再尝试从 546 MB 的 `processed_val.zip` 按条目选择性读取。若远程 ZIP 范围读取不可用，则在真正下载 546 MB 前停止并报告。
- 将这些 clips 合成为一个 P0-A MP4，同时保存每个原始 clip 到合成视频绝对起止时间的 manifest。
- 使用官方人工 transcript 计算 ASR CER，并从 transcript 自动生成带支持 clip ID 的候选问题；人类只需复核 3–5 个问题和少量随机 clip，而不需观看完整视频。
- train/test 媒体留给后续正式 benchmark；P0-A 只保留其官方 split 名称，不宣称完成跨 split 泛化评测。

Chinese-LiPS 标注为 CC BY-NC-SA 4.0，并附加仅限学术/教育、禁止商业使用、禁止重新分发原始或派生数据等访问条款。用户必须亲自在数据集页面接受条款；项目不得把 clips、transcript 子集或派生媒体提交到公开仓库。

## 仍需人工提供或完成的输入

1. API Key 已填入本地 `.env`，其余 DeepSeek 配置已经写好；不要把值写入仓库、报告或对话。
2. 用户已确认 `review-clips/` 下 3 个短片和 4 个问题；无需再观看 4.5 分钟 composite。
3. 真实回答、Top-K、citation 语义与最终报告均已确认；不进入 P0-B。

下一步严格停止在 P0-A；如需进入 P0-B，必须由用户另行授权并创建新的阶段/修订。

## 治理说明

本机没有安装 Project-to-Act，因此未创建伪造的 managed 生命周期账本。当前 `docs/tasks/P0-A.md` 是范围与 Gate 的规范来源；本记录保存本轮可复核运行证据和阻塞条件。
