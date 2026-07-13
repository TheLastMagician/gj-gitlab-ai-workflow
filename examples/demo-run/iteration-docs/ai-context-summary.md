# AI Context Summary

## 迭代目标

用订单审批流 v1.0 真实跑通 GitLab AI 项目交付工作流，暴露摩擦点后再提炼 skill。

## 已上线能力

- GitLab 标签、Milestone、Issue 和评论样例已创建。
- 仓库包含 `.gitlab` 模板、`.gj` 配置、docs/context、docs/modules、CI 脚本和 Orchestrator 骨架。
- Demo 项目实现订单提交、审批、驳回、自审批禁止和重复审批禁止。

## 关键业务规则变化

- 订单申请人不能审批或驳回自己提交的订单。
- `pending` 订单才允许审批或驳回。

## 关键技术决策

- 第一轮 demo 使用 Python 内存领域模型，不引入 Web API、数据库、通知或审计日志。
- `policy_check.py` 只扫描已提交文件，不替代本地 secret 管理。

## 涉及模块和路径

- `examples/demo-project/src/order_approval.py`
- `examples/demo-project/tests/test_order_approval.py`
- `.gj/context.yml`
- `docs/modules/order.md`
- `scripts/policy_check.py`

## 接口 / 数据库 / 权限变化

- 无外部接口。
- 无数据库变化。
- 权限规则以 `applicant != approver` 模拟。

## 后续开发必须知道的注意事项

- 真实系统必须接入可信身份和角色模型。
- GitLab API 写操作前必须校验 project path 和 remote path 一致。
- `gitlab-api.ps1` 等本地 token helper 不能提交。
- 首批 skills 仍是草案，需要第二轮验证。

## 相关 GitLab 链接

- Milestone: https://gitlab.example.com/acme/gj-workflow-demo/-/milestones/1
- Issues: #1-#8
- MR: https://gitlab.example.com/acme/gj-workflow-demo/-/merge_requests/1
