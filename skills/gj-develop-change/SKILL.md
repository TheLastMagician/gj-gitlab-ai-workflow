---
name: gj-develop-change
description: Implement GitLab features, small changes, bugs, and hotfixes using focused project context and flow-aware safeguards. Use when code, tests, or scoped documentation edits are ready to be made after the flow label and required plan are confirmed.
---

# GJ 开发变更

## 工作流程

1. 读取当前 Issue 或 MR、已确认 flow、必要时已接受的计划、`.gj/context.yml`、
   `.gj/workflow.yml`、`docs/standards/01-development-standard.md`、
   `docs/standards/07-test-standard.md`、`docs/standards/09-ai-development-boundary.md`、
   `docs/standards/11-notification-standard.md`，以及 changed paths 命中的模块文档、
   专项规范和 ADR。存在时，以 `docs/standards/12-context-governance.md` 作为文档生命周期
   依据。
2. 确认开发就绪：
   - Fast 需要边界明确的改动、自测和文档影响结论。
   - Standard 需要 Issue、可测试验收标准和已接受的风险行为方案。
   - Hotfix 需要故障影响、负责人确认的紧急性、最低审阅、发布验证和回滚。
3. 选择实现模式：
   - 功能/变更：实现最小且完整的范围。
   - 缺陷：区分事实和假设，复现问题，确认根因并添加回归测试。
   - Hotfix：应用最小安全修复，把非关键清理放入可跟踪的后续项。
4. 编辑前检查代码库，保持在已确认范围内。
5. 按需为验收标准、失败路径、权限和已报告回归新增或更新测试。
6. 根据实际变更路径重新判断技术栈、构建工具、架构/目录边界、前后端工程约定、测试
   工具链、产品行为、交互、API/事件契约、数据库含义、架构/ADR、模块规则、测试基线和
   运维影响。在同一 MR 更新所有受影响的当前事实文档。机器 API
   schema 和数据库 migration 必须与说明文档一致；实现结果同时列出可执行和说明路径。
   新边界从 `.gj/doc-templates/` 创建并使用语义文件名，已有边界原地更新；否则说明每个
   可能相关文档类型为何是 `no-change`。项目工程基线和测试工具链分别原地更新
   `01-development-standard.md` 和 `07-test-standard.md`，不创建扫描报告。
7. Issue、MR 和功能文档关联同一已确认目标版本/Milestone。普通功能、缺陷和 Fast MR
   不提升仓库版本或创建 Tag；项目 manifest 版本只在明确的发布准备工作中修改。
8. 先运行聚焦测试，再运行仓库要求的更广检查。
9. 使用 `create`、`update`、`no-change` 或 `follow-up` 输出文档决策表，包含路径、触发
   事实、阶段/状态和确认人/跟进项。`follow-up` 必须有 Issue、负责人和期限。
10. 准备可直接写入 GitLab 的实现摘要。本 Skill 不得批准、合并或部署。

## 输出格式

```markdown
## 开发结果

Flow 和模式：
目标版本/Milestone：
已加载上下文：
实现内容：
根因（缺陷/Hotfix）：
变更文件：
测试和结果：
文档影响：
文档决策（路径/动作/触发事实/阶段和状态/确认人或跟进项）：
风险和回滚：
后续 Issue：
满足以下条件可创建 MR：
```

## 参考资料

- 聚焦加载上下文时读取 `references/context-example.md`。
- 组织缺陷复现和回归时读取 `references/bug-example.md`。
- 处理紧急边界和跟进时读取 `references/hotfix-example.md`。
