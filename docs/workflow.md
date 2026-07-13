# GitLab AI 项目交付工作流

本项目把 `gitlab_ai_project_workflow_ce_integrated.md` 中的方案整理成可复用
开源骨架。当前版本的核心原则是：先在真实 GitLab 项目里跑通一次，再把稳定动作
封装成 skills。

## 流程总览

```text
工作进入 -> gj-workflow-next 推荐 flow -> 人确认标签
  -> gj-plan-change（Fast 可极简）
  -> gj-develop-change
  -> MR + CI + gj-mr-review
  -> 人决定合并
  -> gj-release-readiness
  -> 人决定 Tag / 发布
  -> gj-close-loop 回写实际 Tag / SHA / 环境版本
```

## 必守原则

1. Standard / Hotfix 必须关联 Issue；Fast 低风险 MR 可以不建 Issue。
2. 没有验收标准不排期。
3. 复杂需求没有方案评审不进入开发。
4. 代码必须通过 MR 合并。
5. Pipeline 必须成功才能合并。
6. 高风险变更必须有人确认。
7. AI 输出必须写回 GitLab 或仓库文档。
8. MR 分支默认不自动覆盖共享测试环境。
9. 共享测试环境必须有人确认、环境锁、版本记录和回滚目标。
10. 需要人处理的节点必须有 GitLab assignee / reviewer / @mention 交接。
11. Issue 记录讨论过程，仓库 docs 记录稳定结论。
12. Milestone 是目标版本，Git Tag 才是已发布版本；普通功能 MR 不 bump 版本。

## 分流

| 类型 | 适用场景 | 必须保留 |
| --- | --- | --- |
| Fast | 低风险局部改动，通常一天内完成 | MR、风险说明、自测证据、文档影响；需要协作时再建 SmallChange Issue |
| Standard | 新功能、复杂改造、跨模块、审批、权限、金额、生产配置 | Issue 和 MR 必须;PRD、方案、测试、发布、摘要按实际影响更新 |
| Hotfix | P0/P1、生产阻塞、安全或数据风险 | Hotfix Issue、最小 Review、发布验证、事后复盘 |

低风险局部工作选择 Fast；Requirement 模板预填 Standard；生产事故选择
Hotfix。命中 `.gj/workflow.yml` 高风险路径时，CI 要求从 Fast 改为
Standard 或 Hotfix。Bug 可以按风险进入 Fast 或 Standard，不单独增加流程重量。

## 通道确认与标签

通道在开始实现前由人确认，并记录为 GitLab 标签：

- Requirement Issue 模板预填 `flow::standard`。
- SmallChange Issue 模板预填 `flow::fast`。
- Hotfix Issue 模板预填 `flow::hotfix`。
- Bug 由 `gj-workflow-next` 根据影响范围推荐 Fast 或 Standard。
- 创建 MR 时选择与当前工作一致的唯一 `flow::*` 标签。

CI 从 `CI_MERGE_REQUEST_LABELS` 读取状态。没有 flow 标签、同时选择多个
flow 标签，或者 `flow::fast` 命中高风险路径，都会阻止 policy job。
CI 只负责复核和兜底，不替人决定业务紧急程度或风险是否可接受。

## GitLab CE 合并门禁

- 默认项目按低风险处理，Fast MR 不要求额外审批人数。
- `.gj/workflow.yml` 只定义最低流程；高风险 changed files 不能走 Fast。
- Standard / Hotfix 必须有关联 Issue、风险、自测和回滚证据。
- 默认分支必须保护，限制可合并角色，并要求 Pipeline 成功后才能合并。
- `CODEOWNERS` 和可选 Approve 操作用于辅助 Review，不作为硬门禁。

## 上下文读取顺序

```text
当前 Issue / MR
  -> 关联总控 Issue / Milestone
  -> .gj/workflow.yml
  -> .gj/context.yml
  -> context.yml 的 global.always_load
  -> 命中模块的 docs/modules/*.md 和明确链接的产品/技术/API/数据库/测试文档
  -> 工作项明确链接的 PRD / 设计 / 技术方案
  -> 有效 ADR
```

## 环境策略

工作流不假设项目一定有多套环境。项目提供部署能力，工作流规定什么时候能部署到哪个环境。

| 环境 | 推荐用途 | 默认策略 |
| --- | --- | --- |
| dev / review | 开发自测、联调、MR 快速验证 | 可自动部署，优先使用 `dev/$CI_COMMIT_REF_SLUG` 这类隔离环境 |
| shared test / staging | QA、产品验收、集成回归 | 不允许 MR 分支自动覆盖；需要人工确认、环境锁和版本记录 |
| production | 生产发布 | 不由环境辅助流程自动发布，必须走发布治理 |

推荐分支规则：

```text
MR / feature branch:
  CI 必跑；可自动部署隔离 dev/review；默认不部署共享 test

develop / integration:
  可自动部署 dev；人工确认后部署 shared test

release/* / tag:
  人工确认后部署 shared test/staging；生产发布另走 release gate
```

如果只有一个测试环境，必须使用 GitLab `resource_group` 或等价环境锁，确保同一时间只有一个部署占用测试环境。每次部署要记录 branch、MR、commit SHA、pipeline、部署人、当前占用、回滚目标和 QA 窗口。

## 角色分配与通知

角色分配属于初始化能力，由 `gj-workflow-bootstrap` 安装并提示维护
`.gj/workflow.yml`。不要单独拆一个角色分配 skill。

工作流的责任来源是 GitLab：

- Issue 的 `assignee` 表示当前处理人。
- MR 的 `reviewer` 表示当前 Review 责任人。
- 交接评论里必须 `@username`，用于触发 GitLab Todo/通知。
- 企业微信或邮件只是 GitLab 通知的投递渠道，不作为工作流状态源。

每个需要人处理的节点，只有在 GitLab 上完成“处理人 + 状态/标签 + 明确动作 +
必要时限 + @mention”后，才算真正交接。个人待办由 `gj-workflow-next` 通过
GitLab API 读取 Todos、assigned issues、review requests、mentions、失败
pipeline 和未解决讨论，再路由到对应 workflow skill。

## 个人基于 AI 的工作方式

个人每天不需要从所有 Issue、MR、Pipeline 和评论里手动找工作入口。标准做法是：

```text
gj-workflow-next 获取我的 GitLab 待办并推荐 flow/下一步
  -> 选择一个待办
  -> AI 判断待办类型并推荐 workflow skill
  -> 人确认处理方式
  -> AI 辅助分析 / 起草 / 编码 / 审阅 / 测试 / 发布检查
  -> 人审阅并确认结果
  -> 写回 GitLab 评论、Issue、MR 或仓库 docs / 代码
  -> 设置 assignee / reviewer，并用 @username 交接给下一个人
```

常见待办路由：

| 待办类型 | 常用 skill | 人保留的决定权 |
| --- | --- | --- |
| 新工作、Bug 或阻塞 | `gj-workflow-next` | flow 标签、优先级和下一步。 |
| 需求、方案、拆分或测试设计 | `gj-plan-change` | 验收标准、技术方案、任务边界和风险。 |
| 开发、Bug 修复或 Hotfix | `gj-develop-change` | 实现范围、测试、文档和回滚。 |
| MR 审阅或合并就绪检查 | `gj-mr-review` | 阻塞问题和是否进入人工合并决策。 |
| 环境或发布准备 | `gj-release-readiness` | 环境锁、版本、验证、回滚和发布窗口。 |
| 复盘或上下文沉淀 | `gj-close-loop` | 长期事实、文档更新和后续事项。 |

AI 可以辅助人完成当前节点，但不能替代人做审批、合并、覆盖共享测试环境或发布决定。

## 文档治理

正式结论进入按模块/功能拆分的仓库文档，讨论过程留在 GitLab。AI 通过
`.gj/context.yml` 渐进加载，不扫描整个 `docs/`，也不默认读取 Git 历史。
各 Skill 在当前改动内完成对应文档回写，`gj-close-loop` 清理过时事实并修剪上下文。
完整分层、预算、文件边界和读写算法见 `docs/documentation-governance.md`；安装到
业务项目后的团队标准见 `docs/standards/12-context-governance.md`。

## 当前 MVP 范围

- 标签、模板、目录和轻量 CI 检查。
- `.gj/workflow.yml` 角色映射和 GitLab handoff 规则。
- 文档生命周期、阶段产物和内容规范由 `docs/standards/12-context-governance.md` 定义;
  `06-release-standard.md` 只定义发布与收尾。
- `policy_check.py` 检查 MR 描述、风险路径和疑似 secret。
- `gj-codebase-map` 生成既有项目上下文草案。
- `gj-workflow-next` 读取 GitLab API 待办、推荐 flow 和下一步 skill。
- `gj-plan-change`、`gj-develop-change` 按 flow 调整交付深度。
- `gj-mr-review`、`gj-release-readiness`、`gj-close-loop` 完成审阅、发布准备和上下文闭环。

## Skill Layer

八个 Skill 覆盖完整工作流，见 `docs/skills.md`。它们按 flow 深度辅助规划、
开发、Review、发布准备和上下文闭环。AI 可以准备判断依据，但不能自主审批、
合并、覆盖共享测试环境或发布。

早期详细设计背景见仓库根目录的
`gitlab_ai_project_workflow_ce_integrated.md`；当前可执行流程以本文、
`README.md` 和 `docs/skills.md` 为准。
