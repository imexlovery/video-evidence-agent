# P1 Dynamic Evidence Seeking 施工 Handoff

## 1. 权威状态与边界

- 项目：`video-evidence-agent`
- 目标等级：`GRADE-P1-001 — G1 PROTOTYPE`
- 产品决策：`CONDITIONAL_GO_HEADROOM_FIRST`
- 独立 readiness：只以 `requirements-readiness.json` 为准；本文不自授予状态
- 当前阶段：文档正式化，禁止源码实现、依赖变更、数据迁移、基础设施操作和 provider 调用
- 施工启动条件：独立 validator 通过，并由 Owner 另行发出实施授权
- 发现覆盖：以 validator 报告的 `confidence` 为准；本包所有 critical discovery gate
  已由 `USER_CONFIRMED`、`USER_DELEGATED` 或有理由的 `NOT_APPLICABLE` evidence 闭合

P1 是一个单用户、本地、中文、单技术视频、只读的 G1 实验。它比较相同输入、相同
transcript source、相同初始 Top-K=5 与相同 answer-level 输出合同下的 `B1 Fixed
Retrieval` 和 `B2 Dynamic Evidence Seeking`。B2 只能通过两个只读 Tool，在 Native
Python bounded loop 中最多调用 3 次。P1 不恢复 B0 Direct Multimodal，也不得发布
B0/B1/B2 三方比较声明。

## 2. 首要施工目标

先冻结并运行 Headroom Gate，而不是先造 Agent。至少 2 个 pre-frozen、answerable、
当前 B1 primary-metric failure 必须能通过可审计的后续检索或邻接检查新增必要 Gold
evidence unit。否则直接产生 `NO_GO_INSUFFICIENT_HEADROOM`，停止所有 B2 源码任务。

若 Gate 通过，才依次实现只读 Tools、run-local Trace/Evidence Gate、无框架 bounded
loop、离线验证、同 revision B1/B2 正式比较和 H4 终态判决。

## 3. 等级、允许使用与安全底线

| 项目 | GRADE-P1-001 合同 |
| --- | --- |
| 选择 | Owner 已确认 `G1 PROTOTYPE`；批准者为本地项目 Owner |
| 允许 | 单一 Owner、本地开发机、公开/获准的技术视频评测资产、只读分析、作品集演示 |
| 禁止 | 生产用户、敏感/受监管数据、外部写操作、跨用户/跨视频推理、服务承诺、自动发布 |
| 规模 | 单进程、单问题 run；正式集为现有 12 题加最多 4 个 pre-frozen candidate |
| 外部依赖 | 后续正式 B1/B2 可使用既有 OpenAI-compatible 文本 provider；必须先获单独 Owner 授权 |
| 安全底线 | 当前视频隔离、Gold 隔离、引用 provenance、预算上限、失败留痕、禁止选择性重跑 |
| 下一等级 | `G2 CONTROLLED_PILOT`；无预定日期，仅在 P1 终态证据与单独 Owner 批准后进入 |

G2 提升必须新增命名用户与访问控制、有限真实数据的用途/同意、可恢复任务状态、审计、
支持 Owner、受控 workload、发布/回滚和 pilot exit criteria。P1 文件合同必须保持版本化，
以便升级而不改写冻结的 G1 历史。

## 4. 输入、输出、来源与资产摘要

- 主输入：`IN-P1-001 QuestionRunRequest`、`IN-P1-002 HeadroomCandidateSet`、
  `IN-P1-003 OwnerProviderAuthorization`，完整合同见 `03-functional-spec.md`。
- 主输出：`OUT-P1-001 AnswerResult`、`OUT-P1-002 RunTrace`、
  `OUT-P1-003 HeadroomReport`、`OUT-P1-004 TerminalDecisionReport`。
- 权威来源：当前视频冻结 `segments.jsonl`（`SRC-P1-001`）、预冻结问题/Gold
  （`SRC-P1-002`）、同 revision provider output（`SRC-P1-003`）。
- 现有资产：P0-B 的 12 题、3 个视频、127 个 `VideoSegment`、R3 基线报告与 manifest；
  只读复用且不覆盖。P1 candidate/Gold 是 `TASK-P1-010` 的预期产物，不是隐藏输入。
- 数据库、共享 cache、品牌素材、新视觉素材：不适用；理由见 `05-data-memory.md` 与
  `06-interfaces-integrations.md`。

## 5. 产品成熟度与发布证据

| 轴 | 当前目标 | 测量与阈值 | Owner / 后果 |
| --- | --- | --- | --- |
| 智能行为 | A2 只读取证 | H4：至少净恢复 2 个 challenge；证据与回归 Gate 全过 | AI-quality Owner；否则选择非保留终态 |
| 系统完整性 | 可复现本地实验闭环 | manifest、Trace、answer、评分、终态文件齐全且 hash 可核验 | Engineering Owner；缺件则不得判决 |
| 生产韧性 | G1 fail-closed | 无未捕获 tool/schema/budget error；失败 revision 保留 | Engineering Owner；新 revision 才可重试 |
| 商业运行 | 不适用 | 无客户、租户、计费、SLA 或 on-call 声明 | Product Owner；越界必须晋级 |

## 6. 固定决策

- `DEC-P1-014`：Conditional Go；Headroom `<2` 即 No-Go。
- `DEC-P1-015`：只有 `search_video`、`inspect_segments`；Top-K=5；max calls=3。
- `DEC-P1-016`：`FRAMEWORKLESS`；Native Python；P1 禁止 LangGraph、Hypha、VLM。
- `DEC-P1-017`：复用 P0 answer-level schema；首轮无 claim-level schema。
- `DEC-P1-019`：`KEEP_AGENT_EXPERIMENTAL` 的强 Gate 为至少净恢复 2 个 challenge。
- `DEC-P1-020`：B0 无正式结果、不恢复、不得用于三方比较。
- `DEC-P1-029`：当前阶段禁止 provider；后续正式调用需要 Owner 明示授权。

所有实现面对的选择分类与允许范围见 `12-engineering-context.md`。当前不存在
`blocking unknown`；provider 授权是已定义的运行时人审 Gate，不是未决设计问题。
施工期 GATE-P1-1..H4 尚未执行，不能与 discovery gate 的闭合混为完成实现或评测。

## 7. 关键风险

1. **没有真实 Headroom**：通过先行 Gate 消除；终态为 `NO_GO_INSUFFICIENT_HEADROOM`。
2. **Agent 只是固定 workflow**：序列集中度达到 80% 或离线固定策略复现收益时转为
   `CONVERT_TO_WORKFLOW`。
3. **证据/回答/成本回归**：H4 fail-closed；不得以“实验成功”覆盖负面结果。
4. **评测选择偏差**：candidate/Gold 先冻结，B1 全结果保留，B2 后置。
5. **provider 不稳定**：一次正式 revision 不补跑；失败工件保留，新 revision 需新授权。

## 8. 目标表面与运行责任

目标表面是现有本地 CLI/库与文件工件；没有 Web、API、worker 或服务部署。本地项目
Owner 同时承担产品、数据、AI-quality、工程和运行验收。源码施工的目标仓库是
`/Users/tristana/Develop/video-evidence-agent`；P0 冻结输入和历史 revision 为保护区。

下游框架状态：`NOT_APPLICABLE`。产品策略：`FRAMEWORKLESS`。所有适用模块均为
`PROJECT_OWNED`；不适用模块不得预留框架脚手架。Hypha 的 P1 disposition 为
`REJECTED_FOR_P1`，原因是其运行时能力超出当前有界实验需求并会改变实验变量。

## 9. 阅读顺序与索引

1. `01-product-requirements.md`：目标、范围与 REQ。
2. `02-user-scenarios.md`：端到端行为与失败恢复。
3. `03-functional-spec.md`：输入/输出、TASK、STATE、错误与规则。
4. `04-system-design.md` 至 `08-quality-security-operations.md`：设计与运行边界。
5. `09-test-acceptance.md`：Gate 和验收矩阵。
6. `10-delivery-plan.md`：依赖顺序与施工停点。
7. `11-decisions-risks.md`、`12-engineering-context.md`：决策权限和改动范围。
8. `decision-evidence.jsonl`、`coverage.json`、`requirements-readiness.json`：证据与独立校验。

Canonical 文件共 13 份 Markdown；`P1-DESIGN.md` 仅为已确认设计背景，不覆盖本包合同。
