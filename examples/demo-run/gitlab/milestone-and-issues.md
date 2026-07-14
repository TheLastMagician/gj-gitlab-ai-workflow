# GitLab Milestone 和 Issue

Milestone：[订单审批流 v1.0](https://gitlab.example.com/acme/gj-workflow-demo/-/milestones/1)

| 类型 | IID | 标题 | URL |
| --- | --- | --- | --- |
| project | #1 | `[订单审批流 v1.0] 项目总控` | https://gitlab.example.com/acme/gj-workflow-demo/-/work_items/1 |
| requirement | #2 | `[订单审批流 v1.0] 需求：订单提交后需要审批` | https://gitlab.example.com/acme/gj-workflow-demo/-/work_items/2 |
| solution | #3 | `[订单审批流 v1.0] 方案：最小订单状态机` | https://gitlab.example.com/acme/gj-workflow-demo/-/work_items/3 |
| task | #4 | `[订单审批流 v1.0] 任务：实现订单审批服务和测试` | https://gitlab.example.com/acme/gj-workflow-demo/-/work_items/4 |
| test | #5 | `[订单审批流 v1.0] 测试：审批流验收和回归` | https://gitlab.example.com/acme/gj-workflow-demo/-/work_items/5 |
| bug | #6 | `[订单审批流 v1.0] Bug：申请人可以审批自己的订单` | https://gitlab.example.com/acme/gj-workflow-demo/-/work_items/6 |
| release | #7 | `[订单审批流 v1.0] 发布：demo 工作流资产和示例` | https://gitlab.example.com/acme/gj-workflow-demo/-/work_items/7 |
| retro | #8 | `[订单审批流 v1.0] 复盘：首轮真实模拟` | https://gitlab.example.com/acme/gj-workflow-demo/-/work_items/8 |

## 已回写评论

- #2 AI 需求澄清。
- #3 开发经理评审结论。
- #4 开发上下文。
- #5 QA 失败记录。
- #6 AI 缺陷分析。
- #7 DevOps 发布就绪结论。
- #8 PM 复盘摘要。

## 合并请求

- !1 `feat(workflow): 初始化 GitLab AI 工作流骨架`
- URL：https://gitlab.example.com/acme/gj-workflow-demo/-/merge_requests/1

## 流水线

- Pipeline #19841：https://gitlab.example.com/acme/gj-workflow-demo/-/pipelines/19841
- 状态：success
- 成功 Job：
  - `policy_check` retry #48329
  - `workflow_contract` #48325
  - `smoke_check` #48326
  - `package_open_source` #48327
  - `release_dry_run` #48328
