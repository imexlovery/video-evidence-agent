# P1 用户场景

## Actors

- `ACTOR-P1-OWNER`：本地项目 Owner；批准 Gold、provider 调用与最终语义判决。
- `ACTOR-P1-ENGINEER`：后续实施者；只在确认合同与任务依赖内施工。
- `ACTOR-P1-RUNTIME`：单进程本地 B1/B2 runner；没有账户、tenant 或外部写权限。

## SCN-P1-001：Headroom 先行

**前置**：P0 R3 baseline 与 12 题 regression 可核验。**触发**：Owner 单独授权进入实施。

1. Engineer 冻结 source/segment/question/Gold/hash baseline。
2. 最多创建 4 个候选；每个关联已记录 failure taxonomy，Gold 由 Owner 在 B2 设计前确认。
3. Runtime 只运行当前 B1，所有候选结果落盘。
4. 评分器识别 answerable B1 primary failures；review 只判断是否存在可审计的动态恢复路径。
5. 若数量至少 2，进入 `HEADROOM_PASSED`；否则发布 `OUT-P1-003`，终止为
   `NO_GO_INSUFFICIENT_HEADROOM`。

后者是有效 No-Go 结论；不得继续 `TASK-P1-030` 及后续 B2 源码施工。

## SCN-P1-002：可回答题动态补证

给定当前视频、原始中文问题和冻结 segments，首次 action 固定 `search_video(question)`。
若 Top-5 已充分，模型直接产生 answer proposal。若 observation 显示邻接边界缺口，模型
可对已观察 anchor 调 `inspect_segments(radius=1|2)`；若 query 方向错，可执行一次不同的
observation-driven search。最多 3 calls 后必须 answer 或 refuse。

Evidence Gate 只接受本 run 成功 observation 的当前视频 segment ID，并回填原始 quote/
timestamp。完整输出交给 Owner 查看 answer、evidence 与 Trace；文件保留到本地 Owner
主动清理该实验 revision。

## SCN-P1-003：不可回答、malformed 与越界

- 无充分证据：输出 `INSUFFICIENT_EVIDENCE`，answer/evidence 均为空。
- 重复 query/inspect、未知 anchor、非法 radius、跨视频、预算耗尽：记录稳定错误码，
  不重试并 fail closed。
- provider malformed/unsafe/timeout：拒绝 late output，保存失败 Trace，当前 revision
  进入 `EVALUATION_BLOCKED_PROVIDER_FAILURE`；不得选择性补跑。
- cancellation：在下一个确定性边界停止，不再执行 Tool/provider，已落盘记录保留。

## SCN-P1-004：正式 B1/B2 比较与终态

**前置**：Headroom、离线测试和 manifest freeze 均通过，Owner 对准确 revision 授权
provider。Runtime 对每题/方法只执行一次。评分完成后 Owner review 语义支持与 Trace。

终态优先级：

1. 工件不完整或 provider failure：`EVALUATION_BLOCKED_PROVIDER_FAILURE`，不执行 H4 判决。
2. provenance/runtime safety 回归：`DELETE_AGENT`。
3. 多数 challenge 无法通过两 Tool 新增必要证据：`REPAIR_RETRIEVAL_FIRST`。
4. 动态收益可由固定序列复现或同一序列比例 `>=80%`：`CONVERT_TO_WORKFLOW`。
5. 仅当净恢复 `>=2` 且 H4 全过、Trace 证明动态性：`KEEP_AGENT_EXPERIMENTAL`。
6. 其他无足够净增量：`DELETE_AGENT`。

报告必须说明是 answer、evidence completeness 或 refusal 的哪一种变化，不能泛化为
“更智能”。B0 固定显示 `NOT_AVAILABLE/NOT_RUN`。

## SCN-P1-005：离线 replay 与恢复

成功 replay 使用 synthetic/approved fixture 重放 `search -> inspect -> answer`，不得调用
provider；输出必须与原 fixture 的 tool observations、eligible evidence、Gate status 一致。
失败/recovery replay 注入跨视频 citation、budget exhaustion 或 malformed action；系统
必须重现相同错误码、fail-closed 输出和 terminal state。正式 provider revision 本身不
resume；恢复只能复制冻结输入创建新 revision，并再次获得 Owner 授权。

## 生命周期覆盖

- Provision/onboarding：本地 checkout、uv `.venv`、冻结 assets；无账户创建。
- Configuration：admin 等同本地 Owner；manifest 是一次 revision 的权威配置。
- Normal use：以上五个场景。
- Support/recovery：Owner 读取 Trace/manifest；无第三方 support access。
- Release/change：新 source/prompt/tool/schema 必须新 revision；旧 revision 不改写。
- Suspension/offboarding/export/deletion：停止本地运行即 suspension；工件可按 revision
  导出；删除只能由 Owner 明示且不能删除已指定为冻结验收历史的 revision。

## Misuse

将 P1 用于敏感数据、跨视频事实拼接、外部写操作、生产服务、三方 baseline 宣称、
Gold 泄漏、选择性补跑或把合法 citation 等同语义正确，均为 prohibited use；验收必须
拒绝或在报告中阻断该声明。

