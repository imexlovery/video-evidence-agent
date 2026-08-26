# P0-A Smoke Report

- 文档状态：FINAL — 用户已确认 ASR 短片、问题、答案与 citation 语义支持。
- video_id：chinese-lips-mini-val-kj-001
- 生成时间：2026-08-26T03:41:33.612719+00:00

## 视频与运行配置

- 来源：https://huggingface.co/datasets/BAAI/Chinese-LiPS
- 授权：CC BY-NC-SA 4.0 plus dataset access terms
- 署名：Chinese-LiPS authors / BAAI
- 本地使用说明：local non-commercial P0-A R1; restricted data not versioned
- 输入 SHA-256：1599fed5b62fdc2b973ce4daf0f441d159124692775404935d6888191906c704
- 视频时长：04:29
- 音频：1 channel, 16000 Hz, 04:29
- ASR：mlx-whisper / mlx-community/whisper-small-mlx / zh
- 不参与检索的原始空文本 ASR segments：[]
- 不参与检索的原始零/负时长 ASR segments：[]
- 不参与检索的原始亚毫秒 ASR segments：[]
- 切分：目标 45000 ms，最大 60000 ms，6 个 VideoSegments
- 阶段耗时（ms）：{"source_probe": 18, "audio_extraction": 77, "asr_preview": 2597, "asr_full": 7326, "segment_build": 0}

## ASR 人工抽查

| 位置 | 时间段 | ASR 原文 | 人工结论 |
| --- | --- | --- | --- |
| 问题 clm-q01-ai-processes | 01:31–01:41 | 人工智能的概念 人工智能是研究使用計算機來模擬人的某些思維過程和智能行為 如學習、推理、思考、規劃等學科 | USER_CONFIRMED |
| 问题 clm-q02-learning-performance | 02:40–02:54 | 他們將互相促進更快的發展 人工智能的特色 1 系統化處理 首先 人工智能系統具有學習能力 可以通過分析和處理大量數據來提高自身性能 | USER_CONFIRMED |
| 问题 clm-q03-work-benefits | 03:31–03:39 | 減少人力資源需求 它可以代替人類重固性、繁瑣或威脅的工作 提高工作效率和安全性 | USER_CONFIRMED |

R1 的三个问题短片与答案 citation 语义均已由用户确认；不要修改 ASR 原文。

## 逐题 Smoke 结果

| question_id | question | should_answer | expected_interval | top_1 | top_5 | final_status | citation_valid | human_supported | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clm-q01-ai-processes | 人工智能使用计算机模拟了人的哪些思维过程或智能行为？ | true | 01:33–01:41 | chinese-lips-mini-val-kj-001-seg-002 01:33–02:19 score=0.1739 | chinese-lips-mini-val-kj-001-seg-002 01:33–02:19 score=0.1739; chinese-lips-mini-val-kj-001-seg-003 02:19–03:04 score=0.1067; chinese-lips-mini-val-kj-001-seg-001 00:48–01:33 score=0.0981; chinese-lips-mini-val-kj-001-seg-004 03:04–03:52 score=0.0396; chinese-lips-mini-val-kj-001-seg-000 00:00–00:48 score=0.0361 | ANSWERED | yes | CONFIRMED | citation_provenance_verified |
| clm-q02-learning-performance | 人工智能系统可以通过什么方式提高自身性能？ | true | 02:43–02:54 | chinese-lips-mini-val-kj-001-seg-003 02:19–03:04 score=0.2081 | chinese-lips-mini-val-kj-001-seg-003 02:19–03:04 score=0.2081; chinese-lips-mini-val-kj-001-seg-004 03:04–03:52 score=0.0826; chinese-lips-mini-val-kj-001-seg-002 01:33–02:19 score=0.0571; chinese-lips-mini-val-kj-001-seg-001 00:48–01:33 score=0.0512; chinese-lips-mini-val-kj-001-seg-005 03:52–04:29 score=0.0366 | ANSWERED | yes | CONFIRMED | citation_provenance_verified |
| clm-q03-work-benefits | 按照视频的说法，哪些工作适合交给人工智能处理，这样做有什么好处？ | true | 03:32–03:39 | chinese-lips-mini-val-kj-001-seg-003 02:19–03:04 score=0.1536 | chinese-lips-mini-val-kj-001-seg-003 02:19–03:04 score=0.1536; chinese-lips-mini-val-kj-001-seg-002 01:33–02:19 score=0.1525; chinese-lips-mini-val-kj-001-seg-001 00:48–01:33 score=0.1445; chinese-lips-mini-val-kj-001-seg-004 03:04–03:52 score=0.1324; chinese-lips-mini-val-kj-001-seg-000 00:00–00:48 score=0.0532 | ANSWERED | yes | CONFIRMED | citation_provenance_verified |
| clm-q04-training-count | 视频中的人工智能系统使用了多少条训练数据？ | false | N/A | chinese-lips-mini-val-kj-001-seg-003 02:19–03:04 score=0.1788 | chinese-lips-mini-val-kj-001-seg-003 02:19–03:04 score=0.1788; chinese-lips-mini-val-kj-001-seg-002 01:33–02:19 score=0.1267; chinese-lips-mini-val-kj-001-seg-001 00:48–01:33 score=0.1085; chinese-lips-mini-val-kj-001-seg-004 03:04–03:52 score=0.0812; chinese-lips-mini-val-kj-001-seg-000 00:00–00:48 score=0.0399 | INSUFFICIENT_EVIDENCE | no | CONFIRMED | model_declared_insufficient_evidence |

human_supported 已由用户核对并确认；citation_valid 记录程序化来源校验。

## 一个完整真实案例

问题：人工智能使用计算机模拟了人的哪些思维过程或智能行为？
Top-1：chinese-lips-mini-val-kj-001-seg-002 01:33–02:19 score=0.1739
Top-K：chinese-lips-mini-val-kj-001-seg-002 01:33–02:19 score=0.1739; chinese-lips-mini-val-kj-001-seg-003 02:19–03:04 score=0.1067; chinese-lips-mini-val-kj-001-seg-001 00:48–01:33 score=0.0981; chinese-lips-mini-val-kj-001-seg-004 03:04–03:52 score=0.0396; chinese-lips-mini-val-kj-001-seg-000 00:00–00:48 score=0.0361
答案：人工智能使用计算机模拟人的思维过程和智能行为，如学习、推理、思考、规划等。
程序回填的 evidence：
- chinese-lips-mini-val-kj-001-seg-002 01:33–02:19: 人工智能是研究使用計算機來模擬人的某些思維過程和智能行為 如學習、推理、思考、規劃等學科 主要包括計算機實現智能層次原理 製造類似於人腦的計算機 使計算機實現更高層次應用 人工智能將涉及到計算機科學、心理學、哲學、語言學等學科 可以說 幾乎是自然科學和社會科學的所有學科 其範圍已遠遠超過了計算機科學範疇 人工智能與思維科學的關係是實踐和理論的關係 人工智能是處於思維科學的技術應用層次 是它的一個應用分支 從思維觀點看 人工智能不僅局限於思維邏輯

## 结论与下一步

- P0-A 验收决定：PASSED — Gate A-G 已完成，按范围停止。
- 已知失败与 transcript-only 边界：已记录；原始 ASR 保留繁体，CER 同时保存繁转简与字形敏感指标；未使用 OCR/VLM。
- P0-B 建议：STOP — 等待用户另行授权，不自动进入下一阶段。

用户已完成 owner acceptance；本报告是 P0-A 最终证据。
