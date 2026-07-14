# Orchestrator 骨架

本目录包含一个无第三方依赖的最小路由骨架，用于 GitLab webhook 事件和斜杠命令。它
目前有意保持为不可用于生产的状态。

用于生产前仍需完成：

- 认证 webhook 请求。
- 通过 GitLab API 获取 Issue、MR、diff、Pipeline 和评论。
- 加载 `.gj/workflow.yml` 和 `.gj/context.yml`。
- 调用具备脱敏、超时、重试和审计日志的 AI 网关。
- 把评论写回 GitLab。
- 保持工作流状态标签互斥。
