# 合并请求

## 关联 Issue

Closes #4

关联：#1 #2 #3 #5 #6 #7 #8

## 变更内容

- 添加开源工作流骨架文档。
- 添加 GitLab Issue 和 MR 模板。
- 添加 `.gj` 配置和可复用模板。
- 添加 CI 策略和冒烟检查脚本。
- 添加 Orchestrator 路由骨架。
- 添加订单审批示例项目。
- 添加首次示例演练产物。
- 添加首批草稿 Skill。

## 自测结果

- `python scripts/policy_check.py --mr-description examples/demo-run/mr/merge-request.md --changed-files examples/demo-run/mr/changed-files.txt --labels flow::standard`
- `python scripts/smoke_check.py`

## 风险点

- 工作流策略文件会影响后续合并门禁。
- Orchestrator 骨架尚不能用于生产。
- 本地 GitLab API helper 可能包含凭据，必须保持未跟踪。

## 回滚方案

回退本 MR。本次不包含数据库、外部 API 或生产配置变化。

## 数据库 / 配置变更

无数据库变化。首次演练已在示例项目中创建 GitLab 标签、Milestone、Issue 和评论。

## 文档影响

- 已更新：`docs/workflow.md`, `docs/quickstart.md`, `docs/context/current-state.md`, `examples/order-demo/docs/modules/order.md`, `examples/demo-run/`.
- 不需要更新，原因：首轮 demo 暂未引入正式 PRD/product-design 模板。
- 后续文档 Issue：后续由文档治理规范补充 PRD、设计、测试、发布模板。

## AI 使用范围

Codex 根据提供的工作流文档和首次端到端演练生成骨架、示例产物、Issue 评论和草稿 Skill。

## 代码审阅重点

- 确认 `gitlab-api.ps1` 和 Token 未提交。
- 检查 `policy_check.py` 秘密扫描和最低 flow 行为。
- 确认 Skill 草稿没有夸大成熟度。
