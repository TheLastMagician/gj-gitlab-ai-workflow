# GitLab AI 项目交付工作流

本项目把 `gitlab_ai_project_workflow_ce_integrated.md` 中的方案整理成可复用
开源骨架。当前版本的核心原则是：先在真实 GitLab 项目里跑通一次，再把稳定动作
封装成 skills。

## 流程总览

```text
需求进入
  -> AI 需求澄清
  -> 产品确认
  -> AI 方案草案
  -> Tech Lead 评审
  -> AI 拆分开发 / 测试 / 发布任务
  -> 开发创建分支和 MR
  -> CI / policy_check / AI Review
  -> 开发环境验证（可自动）
  -> 人工 Review
  -> 测试环境申请 / 验收（需人工确认）
  -> 发布 / 回滚准备
  -> 复盘
  -> 更新 AI 上下文
```

## 必守原则

1. 没有 Issue 不开发。
2. 没有验收标准不排期。
3. 复杂需求没有方案评审不进入开发。
4. 代码必须通过 MR 合并。
5. Pipeline 必须成功才能合并。
6. 高风险变更必须有人确认。
7. AI 输出必须写回 GitLab 或仓库文档。
8. 迭代结束必须生成 `ai-context-summary.md`。
9. MR 分支默认不自动覆盖共享测试环境。
10. 共享测试环境必须有人确认、环境锁、版本记录和回滚目标。

## 分流

| 类型 | 适用场景 | 必须保留 |
| --- | --- | --- |
| 标准需求 | 新功能、复杂改造、跨模块、审批、权限、金额、生产配置 | 需求、方案、任务、MR、测试、发布、复盘 |
| 小改动 | 低风险局部改动，通常半天内完成 | 轻量 Issue、MR、CI、Review、自测 |
| Bug 修复 | 有复现路径的缺陷 | Bug Issue、根因、修复 MR、回归验证 |
| Hotfix | P0/P1、生产阻塞、安全风险 | Hotfix Issue、最小 Review、发布验证、事后复盘 |

## 上下文读取顺序

```text
当前 Issue / MR
  -> 关联总控 Issue / Milestone
  -> .ai/project.yml
  -> .ai/rule-map.yml
  -> .ai/context-index.yml
  -> docs/context/current-state.md
  -> 命中模块的 docs/modules/*.md
  -> 有效 ADR
  -> 最近相关 ai-context-summary.md
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

## 当前 MVP 范围

- 标签、模板、目录和 CI 门禁。
- `policy_check.py` 检查 MR 描述、风险路径和疑似 secret。
- `gj-codebase-map` 生成既有项目上下文草案。
- `gj-workflow-triage` 判断流程路径。
- 需求分析、Bug 修复、MR Review、复盘上下文提取。

## Skill Layer

每个工作流节点都有对应 skill，见 `docs/skills.md`。这些 skill 让团队成员可以
用 AI 辅助完成需求澄清、方案、拆分、开发上下文、Review、测试、发布、复盘和
上下文沉淀。AI 可以辅助审批判断、合并操作和发布准备，但不能脱离人的明确授权
自主审批、自主合并、自主覆盖共享测试环境或自主发布。

完整方案见仓库根目录的 `gitlab_ai_project_workflow_ce_integrated.md`。
