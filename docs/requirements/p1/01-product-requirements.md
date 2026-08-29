# P1 产品需求

## 1. 问题与用户

唯一 persona 是本地项目 Owner/演示者。当前 B1 固定检索已经很强，但仍可能在多证据
边界或 observation-driven query rewrite 上遗漏必要证据。P1 的价值不是展示一个 Agent
框架，而是用可复现比较回答：受限动态取证是否相对 B1 产生可审计净增量。

客户、tenant、account、付费与服务交付均不适用：这是 `GRADE-P1-001` 本地作品集原型，
无外部用户或服务承诺。

## 2. Goals

| ID | 目标 | 可测结果 |
| --- | --- | --- |
| GOAL-P1-001 | 先证明动态取证存在必要 Headroom | 至少 2 个预冻结、可回答、当前 B1 failure，且能新增缺失 Gold unit |
| GOAL-P1-002 | 在相同合同下验证 B2 净增量 | B2 净恢复至少 2 个 challenge，同时通过 H4 全部安全/回归/成本 Gate |
| GOAL-P1-003 | 给 Agent 复杂度一个证据化去留结论 | 每个有效实验只输出一个定义完备的终态与理由 |
| GOAL-P1-004 | 保持 P0 证据链可信 | 冻结历史不改写；引用只来自当前 run 的当前视频 observation |

## 3. Scope

首轮必须包含：Headroom 预注册、B1 先行、两个只读 Tool、Native Python bounded loop、
run-local Trace/Evidence Gate、同 revision B1/B2、自动评分、Owner 语义/Trace review、终态
报告。语言仅中文；每个 run 只绑定一个技术视频；Top-K 固定 5；最多 3 次 Tool Call。

明确非目标：B0/VLM/OCR/keyframe；Dense/Hybrid/Reranker/Embedding；LangGraph、Hypha、
其他 Agent 框架；claim-level schema；FastAPI/Web/UI；Redis/MQ/worker/database/object
storage；多用户、多视频联合推理、多语言、写操作、视频编辑、多 Agent、长期 memory、
生产/商用承诺。

## 4. Requirements

| ID | Requirement | 理由 | 优先级 | 证据 | 验收 |
| --- | --- | --- | --- | --- | --- |
| REQ-P1-001 | 系统必须在任何 B2 实现前完成 Headroom Gate | 防止为无增量空间造 Agent | P0 | DEC-P1-014/018 | TEST-P1-001/002 |
| REQ-P1-002 | B1 与 B2 必须共享 question、Gold、segments、首次 search、provider 配置、answer contract 与 rubric | 保持唯一变量为动态动作 | P0 | DEC-P1-002/014 | TEST-P1-012 |
| REQ-P1-003 | 运行时必须且只能暴露两个只读 Tool、Top-K=5、最多 3 calls | 限权、可解释、可比较 | P0 | DEC-P1-015 | TEST-P1-003..006 |
| REQ-P1-004 | B2 必须是 FRAMEWORKLESS Native Python bounded loop | 保持最小复杂度和可删除性 | P0 | DEC-P1-016 | TEST-P1-007 |
| REQ-P1-005 | 最终答案必须复用 P0 answer-level `AnswerProposal`/`AnswerResult` | 不混淆实验变量 | P0 | DEC-P1-017 | TEST-P1-008 |
| REQ-P1-006 | citation 必须来自当前 run、当前 video 的成功 observation，source 字段由程序回填 | 阻断伪造和跨视频泄漏 | P0 | DEC-P1-003/015 | TEST-P1-009 |
| REQ-P1-007 | 每个 run 必须产生结构化 Trace，且不得存储隐藏 chain-of-thought | 审计动作因果且控制敏感信息 | P0 | DEC-P1-022 | TEST-P1-010 |
| REQ-P1-008 | 候选、Gold、manifest、失败 revision 和正式结果必须 append-only/immutable | 防止选择性证据 | P0 | P0 governance + DEC-P1-018 | TEST-P1-011 |
| REQ-P1-009 | P1 报告必须把 B0 标为 `NOT_AVAILABLE/NOT_RUN`，且只声称 B1 vs B2 | 保持证据标签准确 | P0 | DEC-P1-020 | TEST-P1-013 |
| REQ-P1-010 | H4 必须产生且只产生一个适用终态，不得用笼统“实验失败”代替 | 将负结果变成工程决策 | P0 | DEC-P1-019 | TEST-P1-014 |
| REQ-P1-011 | 当前文档阶段不得调用 provider；后续正式调用必须有与 manifest/revision 绑定的 Owner 授权 | 控制成本与外部操作 | P0 | DEC-P1-021/029 | TEST-P1-015 |
| REQ-P1-012 | 所有越界、错误、超预算、timeout 和 malformed output 必须 fail closed 并留痕 | G1 安全底线 | P0 | DEC-P1-022 | TEST-P1-016 |
| REQ-P1-013 | 新 candidate 最多 4 个，必须源于已记录 failure taxonomy 且不得从 Gold transcript 反向造词 | 降低 challenge 选择偏差 | P0 | DEC-P1-022 | TEST-P1-017 |
| REQ-P1-014 | 首次 Tool action 必须是用原问题执行 `search_video`；仅剩余调用可 observation-driven | 保持 B1/B2 起点一致 | P0 | DEC-P1-015 | TEST-P1-018 |

## 5. 约束、依赖与未来路径

- 依赖：现有 Python 3.12/uv 项目、冻结 P0-B assets、FFmpeg/ASR 已生成的 segments、
  既有 OpenAI-compatible text provider adapter（仅后续授权运行）。
- 首轮不重跑 ASR、不下载新模型、不新增 provider、不改 P0 Gold/结果。
- 如果发现 mixed-support claim，记录为后续新 revision 的 schema 提案；P1 首轮不改变合同。
- 如果审计证明答案只存在于画面而 transcript 不存在，VLM 只能进入另一个 Owner
  checkpoint，不得在本阶段暗中恢复 B0。
- G2 promotion 需满足 `00-handoff.md` 的 named-user、access/consent、audit/recovery/support
  条件并通过新需求审查。

## 6. Glossary

- **B1**：固定一次 transcript retrieval + answer 的当前 baseline。
- **B2**：相同首次 search 后，允许最多两个 observation-driven 只读动作的实验组。
- **Headroom failure**：预冻结、可回答、当前 B1 的 `AllNecessaryEvidence@5=false`
  （即 `EvidenceUnitRecall@5<1.0`），且 scorer-only oracle 检查证明允许的 rewrite/邻接
  动作能新增至少一个缺失 Gold unit；历史已修复失败不算。该入口检查不调用 provider。
- **Dynamic recovery**：B1 failure 在 B2 中因后续 observation 新增必要 Gold evidence
  unit 并使 primary metric 通过；纯措辞变化不算。
- **H4**：决定是否保留 Agent 复杂度的强 Gate 集合。
- **正式 revision**：manifest 冻结后、每方法每题一次、失败保留且不得选择性补跑的运行。
