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
  -> 人工 Review
  -> 测试 / 验收
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
自主审批、自主合并或自主发布。

完整方案见仓库根目录的 `gitlab_ai_project_workflow_ce_integrated.md`。
