---
name: gj-codebase-map
description: Map an existing repository into confirmed engineering standards and focused AI context. Use when onboarding a GitLab project, refreshing development or test standards, deriving docs/context and docs/modules, generating .gj/context.yml drafts, or scanning changed paths after major refactors.
---

# GJ 代码库建图

## 工作流程

1. 使用 `rg --files` 了解仓库结构。
2. 从四个视角扫描：
   - 技术：技术栈、运行时、依赖、外部集成。
   - 架构：入口、分层、数据流、模块边界。
   - 质量：约定、测试、CI、错误处理。
   - 风险：安全、脆弱区域、性能、未知项。
3. 把扫描结果直接路由到后续流程会读取的长期文档，不创建中间扫描目录：
   - 技术栈、构建命令、架构边界、目录和前后端约定：
     `docs/standards/01-development-standard.md`；
   - 测试框架、目录、命令、覆盖和 CI 规则：`docs/standards/07-test-standard.md`；
   - API、数据库、安全或环境专项事实：对应 `03`、`04`、`08`、`10` 标准，以及按需的
     API、数据库或技术方案文档；
   - 模块结构、集成和依赖：`docs/context/module-map.md`、`docs/modules/*.md` 以及按需的
     API/技术方案；
   - 项目级长期限制：`docs/context/current-state.md`；可执行技术债和缺陷输出为
     GitLab Issue 草稿，不写入仓库待办清单。起草前读取
     `docs/standards/09-ai-development-boundary.md` 和
     `docs/standards/11-notification-standard.md`。
4. 创建或更新当前上下文草稿：
   - `docs/context/current-state.md`
   - `docs/context/module-map.md`
   - `docs/context/glossary.md`
   - `docs/modules/*.md`
   - `.gj/context.yml`
   从 `.gj/doc-templates/module.md` 创建模块文档，使用语义化模块名，包含通用元数据契约，
   并明确区分已观察事实和推断。
5. 根据模块路径更新 `.gj/context.yml`，让开发、计划和审阅 Skill 能加载模块文档、
   功能文档和有效 ADR；`01`/`07` 由代码相关 Skill 固定读取，不要把所有规范加入
   `always_load`。
6. 标记所有需要人工确认的推断，并列出 Dev Lead、QA、安全或模块负责人分别需要确认
   的标准草稿。扫描到的现有习惯不自动等于正确规范。
7. 暂存或分享前扫描生成内容中的秘密信息。

## 规则

- 不创建 `docs/codebase/` 或其他扫描报告目录；扫描只是生成长期规范和上下文草稿的过程。
- 未经确认，不要把观察到的行为转为当前状态规则。
- `01-development-standard.md` 和 `07-test-standard.md` 中新增的项目规则先标记为待确认，
  分别由 Dev Lead 和 QA/Dev Lead 确认后生效。
- 已有长期文档原地更新，不创建 `v2`、`final` 或 `new` 副本。
- 外部集成写入负责该集成的模块或技术/API 文档；没有长期解释价值时不额外建文档。
- 风险有明确修复动作时创建 Issue 草稿；只有后续任务都会依赖的当前限制才写
  `current-state.md`。
- 发现 Token、私钥、密码或连接字符串时停止，并要求人处理。

## 输出格式

```markdown
## 代码库建图摘要

扫描路径：

创建/更新的开发与测试规范：

创建/更新的上下文和模块文档：

已观察事实：

待确认推断：

需要人工确认的规范：

风险、缺陷和建议的 GitLab Issue：

秘密扫描：
```

## 参考资料

需要查看小型示例建图时，读取 `references/demo-run.md`。
