---
name: gj-workflow-next
description: Accept a new requirement or inspect a GitLab inbox or active work item, recommend the flow label, and choose the next workflow action. Use when a user brings new work, asks what is assigned to them, what to do next, which flow to use, why work is blocked, or how an Issue, MR, discussion, or pipeline should be routed.
---

# GJ 下一步

## 工作流程

1. 判断输入是新需求还是已有 GitLab 工作。新需求先记录目标和已知约束，在创建 Issue 前
   读取 `docs/standards/02-requirement-standard.md` 并路由到 `gj-plan-change`。只有人确认
   需求和 flow 后才创建或设置 Issue 标签；没有 GitLab 写权限时返回完整 Issue 草稿。
2. 确认参与人和项目。用户询问个人工作时，优先使用项目中的
   `scripts/gitlab_api.py` 获取 GitLab Todo、已分配 Issue/MR、审阅请求、提及、讨论和
   相关失败或 pending Pipeline；已配置 GitLab connector 可作为替代。
3. 检查仓库状态、所选工作项、当前标签、已变更或预计路径、Pipeline 状态和工作流文档。
4. 判断 flow：
   - 低风险、局部且验证有界的工作使用 Fast。
   - 业务规则、权限、金额、API、数据库、跨模块或验证不清晰的工作使用 Standard。
   - 紧急生产、安全或数据风险使用 Hotfix。
   只推荐一个 `flow::*` 标签，由人在编码前确认。
5. 独立于 flow 处理版本规划。存在时读取 `.gj/workflow.yml` 的 `versioning` 和
   `docs/standards/13-versioning-standard.md`。对将发布的新工作，根据兼容影响和最新
   已发布 Tag 推荐目标版本及匹配的 GitLab Milestone，由人确认。不要提升 manifest、
   创建 Tag 或把 Milestone 描述为已发布。
6. 判断当前阶段。已有代码但 `01-development-standard.md`、`07-test-standard.md`、模块地图
   或模块上下文仍是占位内容，或者刚完成重大重构时，先路由到 `gj-codebase-map`；其他
   工作路由到 `gj-plan-change`、`gj-develop-change`、`gj-mr-review`、
   `gj-release-readiness` 或 `gj-close-loop`。
7. 检查阻塞项：缺失/冲突的 `flow::*` 标签、缺少 Issue 或验收标准、缺少方案评审、
   失败或 pending Pipeline、未解决审阅评论、高风险路径错误使用 `flow::fast`、缺少
   工程规范仍未确认、上下文更新、缺少文档影响结论或必需仓库文档。
8. 检查 assignee、reviewer、提及、截止日期、目标版本/Milestone 和文档缺口。
   Requirement/Hotfix 是主工作项；只有工作需要独立负责或跟踪时才推荐 Solution、Task
   或 Test Issue，不能替代仓库文档。
9. 答案保持可执行，并包含证据链接或文件路径。起草或发布 Issue、MR、评论、讨论或交接
   消息前读取 `docs/standards/11-notification-standard.md`。默认只读检查；只有人确认动作
   后才设置标签或交接工作。

## 输出格式

```markdown
## 工作流下一步

当前阶段：

Flow 建议：

目标版本/Milestone 建议：

证据：

阻塞项：

建议的下一个 Skill：

下一步动作：

Issue 动作（确认后创建或返回草稿）：

文档影响：

需要人工确认：

完成条件：
```

## 参考资料

- 查询 GitLab API 状态时读取 `references/gitlab-inbox.md`。
- 需要首次运行阶段轨迹时读取 `references/demo-run.md`。
