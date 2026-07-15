---
name: gj-release-readiness
description: Assess and prepare GitLab dev, test, staging, and production release readiness. Use when a branch, MR, tag, or milestone needs environment policy checks, pipeline and test evidence, release notes, rollout, rollback, monitoring, or explicit human release decisions.
---

# GJ 发布就绪检查

## 边界

- AI 准备证据和说明；人决定并触发共享环境或生产部署。
- MR 分支只能自动部署到项目 CI 已允许的隔离开发/评审环境。
- 共享测试/预发布环境需要 GitLab `resource_group` 等锁、已知当前版本、回滚目标和明确
  人工确认。
- MR Pipeline 不得创建生产发布 Job。

## 工作流程

1. 确认目标环境以及来源分支、MR、Tag、commit SHA 和最新 Pipeline。
2. 读取发布 Issue 或 Milestone、包含的 MR、测试结果、已知风险、CI 规则、部署脚本，
   以及 `docs/standards/06-release-standard.md`、
   `docs/standards/10-environment-standard.md`、
   `docs/standards/11-notification-standard.md` 和
   `docs/standards/13-versioning-standard.md`。
3. 读取 `.gj/workflow.yml` 版本策略，根据兼容影响和最新已发布 Tag 确定最终 SemVer，
   并确认 GitLab Milestone 匹配。此时锁定版本。
4. 核验 Pipeline 状态、未解决讨论、测试证据、配置/数据/权限变化、环境隔离或锁以及
   回滚目标。
5. 从 `.gj/doc-templates/test-report.md` 创建或更新
   `docs/qa/test-reports/<tag>.md`，填写版本、计划 Tag、准确提交/构建、Pipeline、环境、
   包含的 Issue/MR、结果、证据、缺陷和 QA 结论。
6. 从 `.gj/doc-templates/release-note.md` 创建或更新配置的
   `docs/releases/<tag>.md` 并关联测试报告。记录版本、里程碑、计划 Tag、分支、SHA、
   Pipeline、目标、负责人、时间窗口、发布、监控、验证和回滚。发布完成后冻结版本证据。
7. 只有技术栈要求时才更新现有项目 manifest 版本，不引入通用 `VERSION` 文件。请求人
   创建 Tag 前运行 `python scripts/release_version_check.py --tag <tag>`。
8. 使用 `create`、`update`、`no-change` 或 `follow-up` 输出文档决策表，包含路径、触发
   事实、阶段/状态和确认人/跟进项。
9. 停在人工决策门，不得批准、合并、创建 Tag 或部署。

## 输出格式

```markdown
## 发布就绪检查

目标和来源：
最终版本/Milestone/计划 Tag：
结论：
Pipeline 和测试：
包含的变更：
配置/数据/权限影响：
环境隔离或锁：
发布说明和文档影响：
文档决策（路径/动作/触发事实/阶段和状态/确认人或跟进项）：
发布和监控：
回滚目标和步骤：
发布后验证：
供人执行的 Tag 命令：
需要人工确认：
```

“结论”只能是 `not_ready`、`ready_for_isolated_dev`、
`ready_for_shared_environment_confirmation` 或 `ready_for_release_confirmation`。

## 参考资料

- 需要 GitLab 环境锁和部署记录字段时读取 `references/environment-policy.md`。
- 需要发布预演示例时读取 `references/release-example.md`。
