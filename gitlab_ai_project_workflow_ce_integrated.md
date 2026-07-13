---
title: "GitLab AI 项目交付工作流实施方案"
subtitle: "精简版：用 GitLab、AI Skills、CI 门禁和项目上下文沉淀支撑持续迭代"
author: "AI 项目工作流方案"
date: "2026-07-03"
lang: zh-CN
version: "v2.0"
---

# 1. 目标

本方案用于在 GitLab 项目中建立一套 AI 辅助的软件交付工作流。

核心目标：

1. GitLab 作为项目事实源：需求、方案、任务、MR、测试、发布、复盘都能追溯。
2. AI 作为流程助手：读取 GitLab 和仓库上下文，辅助澄清、拆解、Review、测试、发布和复盘。
3. 人负责最终决策：AI 不自主审批、不自主合并、不替代产品、Tech Lead、Reviewer、QA、DevOps；但各角色可以在明确授权下使用 AI 辅助审批判断、合并操作、发布准备和记录沉淀。
4. 每个迭代沉淀上下文：项目越做越有记忆，后续 AI 能读取当前事实、模块背景和历史摘要。
5. 工作流可封装为 skills：每个流程节点都可以成为团队复用的 AI skill。

本方案只依赖 GitLab 常见能力：

```text
Project Issue / Milestone / Board / Merge Request / Pipeline
Project Webhook / REST API / Protected Branch / Repository Files
```

# 2. 总体原则

1. 没有 Issue 不开发。
2. 没有验收标准不排期。
3. 复杂需求没有方案评审不进入开发。
4. 代码必须通过 MR 合并。
5. 默认分支必须受保护。
6. Pipeline 必须成功才能合并。
7. 高风险变更必须有人确认。
8. AI 输出必须写回 GitLab 或仓库文档。
9. 重要里程碑结束后在 GitLab 复盘，并更新仍需长期依赖的项目事实。
10. 历史资料用于追溯，当前事实以 `docs/context/`、`docs/modules/` 和有效 ADR 为准。

# 3. 工作流总览

```text
需求进入
  ↓
AI 需求澄清：缺失信息、歧义、验收标准草案
  ↓
产品 / 业务确认需求
  ↓
AI 方案草案：影响范围、接口、数据、权限、风险
  ↓
Tech Lead / 架构师评审方案
  ↓
AI 拆分开发 / 测试 / 文档 / 发布任务
  ↓
开发创建分支和 MR
  ↓
CI：lint / test / policy_check / security scan / AI Review
  ↓
人工 Review / 风险证据 / 线程解决
  ↓
合并
  ↓
测试 / 验收
  ↓
发布 / 回滚准备 / 上线验证
  ↓
复盘
  ↓
更新当前上下文、模块文档和 ADR
```

# 4. GitLab 对象模型

| 对象 | 用途 |
|---|---|
| 项目总控 Issue | 一个项目、版本或大功能的主索引。 |
| Milestone | 一次迭代、版本或交付阶段。 |
| 需求 / Hotfix Issue | 一次变更的主工作项，保存范围、验收、讨论、负责人和决策过程。 |
| 方案 Issue | 仅在独立负责人、排期或跟踪需要时拆分；不替代仓库技术方案。 |
| 开发任务 Issue | 仅在独立负责人、依赖或排期需要时拆分的执行任务。 |
| 测试 Issue | 仅在独立测试协作需要时使用；不替代测试计划和版本报告。 |
| 发布 Issue | 发布清单、配置、DB 变更、回滚、验证。 |
| 复盘 Issue | 项目复盘、改进项、上下文沉淀清单。 |
| MR | 代码变更、Review、CI 结果、AI Review。 |
| Pipeline | 自动化检查、测试、门禁、扫描、报告。 |
| Webhook | 触发 AI Orchestrator。 |

推荐关系：

```text
项目总控 Issue
  ├── Milestone
  ├── 需求 / Hotfix 主 Issue
  ├── 按需：方案 / 开发任务 / 测试 Issue
  ├── 开发 MR
  │     └── Pipeline
  ├── 发布 Issue
  └── 复盘 Issue
```

# 5. GSD 风格阶段协议

本工作流借鉴 GSD 的核心思想：模糊想法先澄清，再形成可执行工件，执行后验证和沉淀。

| 阶段 | GitLab 载体 | AI skill | 产物 | 准出标准 |
|---|---|---|---|---|
| Explore | 主 Issue 评论 | `gj-plan-change` | 澄清问题、业务目标、边界 | 需求能被业务确认 |
| Spec | 主 Issue + PRD | `gj-plan-change` | 验收、反例和当前产品要求 | PdM 确认 |
| Plan | 主 Issue + 仓库技术文档 | `gj-plan-change` | 方案、API、数据、风险和测试基线 | Dev Lead/QA 确认 |
| Split | 按需拆分 Issue | `gj-plan-change` | 独立负责人、依赖和优先级 | 拆分确有协作价值 |
| Execute | 分支 + MR | `gj-develop-change` | 实现、测试和长期文档更新 | MR 创建 |
| Review | MR | `gj-mr-review` | 变更摘要、风险、测试建议 | Pipeline 通过、线程解决 |
| Verify | 测试计划/报告 + 按需 Test Issue | `gj-release-readiness` | 测试基线和版本执行证据 | QA 给出结论 |
| Release | 发布 Issue / tag | `gj-release-readiness` | Release Note、回滚、验证 | 发布完成 |
| Retro | 复盘 Issue | `gj-close-loop` | 复盘报告、改进项 | 改进项明确 |
| Context Update | 仓库文档 | `gj-close-loop` | 当前状态、模块文档、ADR | 长期上下文已更新 |

# 6. 流程分流规则

本工作流约束的是交付节点、输入输出、流转条件和沉淀要求，不约束个人在节点内使用的具体工具和方法。产品、开发、测试、运维可以使用任意工具或 AI，只要完成当前节点产物，并满足进入下一节点的条件。

不是所有事项都需要走完整重流程。先由人或 `gj-workflow-next` 判断事项类型，再选择对应路径。

| 类型 | 适用场景 | 可跳过 | 必须保留 |
|---|---|---|---|
| 标准需求 | 新功能、复杂改造、跨模块、影响业务规则 | 不相关的文档和无协作价值的拆分 Issue | 主 Issue、按影响更新的长期文档、MR、测试和发布证据 |
| 小改动 | 文案、样式、小字段、低风险局部逻辑 | 方案评审、任务拆分、额外过程文档 | 轻量 Issue、MR、CI、Review、自测 |
| Bug 修复 | 测试失败、线上缺陷、明确复现路径 | 需求确认、方案评审、完整任务拆分 | Bug Issue、根因、修复 MR、回归验证 |
| Hotfix | P0/P1 线上故障、安全风险、发布阻塞 | 事前完整方案和复盘 | Hotfix Issue、最小 Review、发布验证、事后补复盘 |

## 6.1 标准需求流程

```text
需求 Issue
  ↓
需求确认
  ↓
主 Issue 中的方案评审 + 仓库技术文档
  ↓
任务拆分
  ↓
开发 MR
  ↓
Review / CI / 测试
  ↓
发布
  ↓
复盘和上下文更新
```

适用条件：

1. 新业务能力。
2. 跨模块或跨系统。
3. 改变业务规则、权限、数据模型、接口契约。
4. 涉及金额、审批、安全、生产配置。
5. 需要多人协作或超过 1 天开发。

## 6.2 小改动流程

```text
轻量 Issue
  ↓
开发
  ↓
MR
  ↓
CI / Review
  ↓
合并
```

适用条件：

1. 不改变核心业务规则。
2. 不改变权限。
3. 不改变数据库结构。
4. 不影响外部接口兼容。
5. 不涉及金额、审批、安全、生产配置。
6. 可快速验证，通常半天内完成。

小改动 Issue 至少包含：

1. 改动说明。
2. 影响范围。
3. 自测方式。
4. 风险判断。

## 6.3 Bug 修复流程

```text
Bug Issue
  ↓
定位原因
  ↓
修复 MR
  ↓
回归验证
  ↓
CI / Review
  ↓
合并
```

Bug Issue 至少包含：

1. 缺陷现象。
2. 复现步骤。
3. 预期结果。
4. 实际结果。
5. 影响范围。
6. 根因分析。
7. 修复说明。
8. 回归验证。

如果 Bug 修复过程中发现需求理解、业务规则或架构设计存在问题，应升级为标准需求，
更新对应长期文档；只有独立跟踪有价值时才补充方案 Issue。

## 6.4 Hotfix 流程

```text
Hotfix Issue
  ↓
快速修复 MR
  ↓
最小必要 Review
  ↓
发布和验证
  ↓
事后补根因、测试、复盘和上下文更新
```

Hotfix 只适用于：

1. P0 / P1 线上故障。
2. 安全风险。
3. 生产发布阻塞。
4. 数据损坏或核心流程不可用。

Hotfix 可以先推进，但事后必须补齐：

1. 根因分析。
2. 影响范围。
3. 回归结果。
4. 是否需要补测试。
5. 是否需要更新 `docs/context/`、`docs/modules/`、ADR 或 `.gj/context.yml`。
6. 是否需要调整流程或门禁。

## 6.5 分流判断规则

`gj-workflow-next` 应读取 Issue 标题、描述、标签、影响模块和风险关键词，输出建议路径：

```text
标准需求 / 小改动 / Bug 修复 / Hotfix
```

建议输出：

```markdown
## 流程分流建议

推荐路径：

判断理由：

可跳过的步骤：

必须保留的步骤：

风险提示：

需要人工确认：
```

命中以下任一条件时，不得走小改动流程：

1. 涉及权限、金额、审批、安全、生产配置。
2. 涉及数据库结构或数据迁移。
3. 涉及外部 API 契约。
4. 涉及多个模块或多个团队。
5. 无法明确验证影响范围。

# 7. 阶段准入准出

## 7.1 Definition of Ready

需求进入开发前至少满足：

1. 背景和业务目标清楚。
2. 用户场景清楚。
3. 功能范围和非目标范围清楚。
4. 验收标准明确。
5. 权限、数据、外部依赖已说明。
6. 风险已记录。
7. 复杂需求已有技术方案并完成评审；方案 Issue 只在独立跟踪需要时创建。

## 7.2 Definition of Done

任务关闭前至少满足：

1. MR 已合并。
2. Pipeline 通过。
3. AI Review 已执行，人工已处理或确认建议。
4. 测试完成。
5. 文档、配置、接口说明已更新。
6. 发布和回滚注意事项已说明。
7. 影响当前事实或模块知识的变更已沉淀到仓库文档。

# 8. 标签与看板

标签保持简单，优先用于流程流转和筛选。

## 8.1 类型标签

```text
type-project
type-requirement
type-small-change
type-solution
type-task
type-bug
type-hotfix
type-test
type-release
type-retro
```

## 8.2 状态标签

```text
status-需求池
status-需求待分析
status-需求待确认
status-需求已确认
status-方案设计中
status-方案待评审
status-方案已确认
status-待开发
status-开发中
status-待CodeReview
status-测试中
status-待发布
status-已发布
status-已关闭
status-阻塞
```

状态标签同一时间只保留一个，由人或 Bot 清理。

## 8.3 风险与 AI 标签

```text
priority-P0 / priority-P1 / priority-P2 / priority-P3
risk-high / risk-security / risk-database / risk-devops / risk-permission
ai-待分析 / ai-已分析 / ai-需人工确认 / ai-阻塞
```

推荐看板：

1. 项目总览 Board：按 `status-` 流转。
2. 研发执行 Board：待开发、开发中、待 Review、测试中。
3. 风险 Board：按 `risk-*` 聚合高风险事项。

# 9. Issue 与 MR 模板

模板不要堆过多制度说明，只收集当前阶段必要事实。

## 9.1 需求 Issue 必填

1. 需求背景。
2. 业务目标。
3. 用户场景。
4. 功能范围。
5. 非目标范围。
6. 权限与数据范围。
7. 外部依赖。
8. 验收标准。
9. 优先级和期望上线时间。
10. 关联项目总控 Issue。

## 9.2 按需拆分的方案 Issue

只有方案存在独立负责人、排期、依赖或需要单独跟踪时才创建。下列字段记录过程，
确认后的长期结论仍写入 `docs/technical/`：

1. 关联需求。
2. 方案摘要。
3. 影响范围。
4. 接口、数据库、权限变化。
5. 测试范围。
6. 发布和回滚方案。
7. 风险清单。
8. 人工评审结论。

## 9.3 开发任务 Issue 必填

1. 任务目标。
2. 关联需求和方案。
3. 实现范围和非实现范围。
4. 涉及模块 / 文件。
5. 验收标准。
6. 测试要求。
7. 风险点。
8. AI 使用记录。

## 9.4 MR 必填

1. 关联 Issue。
2. 变更内容。
3. 自测结果。
4. 风险点。
5. 回滚方案。
6. 数据库 / 配置变更。
7. AI 使用范围。
8. 需要 Reviewer 重点关注的问题。
9. 高风险确认记录。

## 9.5 轻量 Issue 必填

用于小改动，不要求完整需求澄清和方案评审。

1. 改动说明。
2. 影响范围。
3. 不涉及高风险项的确认。
4. 自测方式。
5. 回滚或撤销方式。

## 9.6 Bug Issue 必填

1. 缺陷现象。
2. 复现步骤。
3. 预期结果。
4. 实际结果。
5. 影响范围。
6. 根因分析。
7. 修复说明。
8. 回归验证。

## 9.7 Hotfix Issue 必填

1. 故障等级和影响范围。
2. 当前止血方案。
3. 修复方案。
4. 最小必要 Review 负责人。
5. 发布和验证结果。
6. 事后根因分析。
7. 需要补的测试、文档、上下文或流程改进。

# 10. 仓库目录规范

推荐目录：

```text
.gitlab/
  issue_templates/
  merge_request_templates/

.gj/
  workflow.yml
  context.yml
  gitlab.local.json  # 本机忽略，不提交
    gj-release-readiness/
    gj-close-loop/
  scripts/

docs/
  ai-workflow.md
  context/
    current-state.md
    module-map.md
    glossary.md
  codebase/
    STACK.md
    INTEGRATIONS.md
    ARCHITECTURE.md
    STRUCTURE.md
    CONVENTIONS.md
    TESTING.md
    CONCERNS.md
  modules/
    order.md
    auth.md
  standards/
    00-index.md
    01-development-standard.md
    02-requirement-standard.md
    03-api-standard.md
    04-database-standard.md
    05-review-standard.md
    06-release-standard.md
    07-test-standard.md
    08-security-standard.md
    09-ai-development-boundary.md
  architecture/
    adr/

scripts/
  policy_check.py
  collect_project_context.py

CODEOWNERS
.gitlab-ci.yml
```

# 11. AI 上下文规则

AI 不应每次读取全部文档。必须按优先级装载最小必要上下文。

读取顺序：

```text
当前 Issue / MR
  ↓
关联项目总控 Issue / Milestone
  ↓
.gj/workflow.yml
  ↓
.gj/workflow.yml
  ↓
.gj/context.yml
  ↓
docs/context/current-state.md
  ↓
命中模块的 docs/modules/*.md
  ↓
命中模块的有效 ADR
```

上下文分层：

| 层级 | 文件 | 说明 |
|---|---|---|
| 当前事实 | `docs/context/current-state.md` | 当前系统真实状态。 |
| 模块知识 | `docs/modules/*.md` | 模块长期背景和业务规则。 |
| 技术决策 | `docs/technical/decisions/ADR-*.md` | 人确认且冻结的长期技术取舍。 |

关键规则：

1. 当前事实文档必须与代码一起更新。
2. 旧方案不能直接当作当前事实。
3. 如果当前事实和 Git、Issue 或 MR 历史冲突，AI 必须提示人工确认。
4. 发布或复盘后，长期有效变化必须同步到当前上下文或模块文档。

# 12. 持续知识沉淀

仓库只维护当前有效的需求、设计、模块、上下文和 ADR；测试报告与发布说明按版本冻结。
工作过程和复盘保留在 GitLab Issue/MR，历史变化由 Git 追溯，不在仓库重复保存。

需要进入长期上下文的变化：

| 变化类型 | 更新位置 |
|---|---|
| 当前产品或业务规则变化 | `docs/product/requirements/*.md`、相关 `docs/modules/*.md` |
| 模块边界变化 | `docs/context/module-map.md`、`.gj/context.yml` |
| 新术语 | `docs/context/glossary.md` |
| 架构或长期技术决策 | `docs/technical/solutions/*.md`、`docs/technical/decisions/ADR-*.md` |
| 风险路径或负责人变化 | `.gj/workflow.yml` |

# 13. 既有项目接入：Codebase Map

如果是已有项目，不要直接让 AI 根据零散代码开始开发。应先做一次 codebase map，把现有项目梳理成可审查、可追溯、可被后续 AI 读取的基础上下文。

这个过程借鉴 GSD 的 codebase mapper 思路：按不同关注面扫描代码库，分别产出结构化文档，最后再汇总成当前项目上下文。

推荐输出：

```text
docs/codebase/
  STACK.md          技术栈、语言、框架、依赖、运行时
  INTEGRATIONS.md   外部系统、数据库、消息队列、第三方 API、Webhook
  ARCHITECTURE.md   架构模式、分层、数据流、入口点、核心抽象
  STRUCTURE.md      目录结构、关键路径、模块边界、命名约定
  CONVENTIONS.md    代码风格、错误处理、日志、配置、常见模式
  TESTING.md        测试框架、测试目录、mock、覆盖策略、CI 测试方式
  CONCERNS.md       技术债、脆弱点、安全风险、性能风险、待确认问题
```

推荐流程：

```text
扫描项目文件结构
  ↓
按 tech / arch / quality / concerns 四个视角分析
  ↓
生成 docs/codebase/*.md
  ↓
扫描输出中是否误带 secret / token / password
  ↓
人工快速审查 codebase map
  ↓
提炼 docs/context/current-state.md
  ↓
提炼 docs/context/module-map.md
  ↓
提炼 docs/context/glossary.md
  ↓
生成 docs/modules/*.md 草案
  ↓
生成 .gj/context.yml 草案
  ↓
创建“既有项目接入”MR
```

全量扫描适合首次接入；后续大改或重构后可以增量刷新：

```text
gj-codebase-map --paths src/order,db/migration
```

增量刷新只更新命中路径相关的 codebase 文档、模块文档和 `.gj/context.yml`，避免每次重新扫描整个项目。

Codebase map 的定位：

| 文档 | 定位 |
|---|---|
| `docs/codebase/*.md` | 从代码中观察到的现状，偏工程事实。 |
| `docs/context/*.md` | 当前项目对外稳定事实，偏 AI 默认上下文。 |
| `docs/modules/*.md` | 模块级长期知识，偏后续开发参考。 |
| ADR | 人工确认过的长期技术决策。 |

重要规则：

1. `docs/codebase/*.md` 是 AI 观察结果，必须经过人工确认后才能沉淀为当前事实。
2. 不要把扫描出的历史代码行为直接等同于正确业务规则。
3. 发现疑似密钥、账号、连接串时必须停止提交并要求人工确认。
4. 既有项目第一次接入时，`docs/context/` 和 `.gj/context.yml` 应从 codebase map 派生，而不是凭空编写。
5. 每次重大重构后，应刷新相关 codebase map，并同步更新模块文档和上下文索引。

## 13.1 `gj-codebase-map` skill 设计

用途：接入既有项目、刷新项目地图、重构前理解现状、重大变更后更新 AI 上下文。

触发示例：

```text
使用 gj-codebase-map 梳理这个已有项目，并生成 docs/codebase、docs/context、docs/modules 和 `.gj/context.yml` 草案。

使用 gj-codebase-map --paths src/order,db/migration 增量刷新订单模块上下文。
```

输入：

1. 当前仓库文件。
2. 可选路径范围：`--paths <path1,path2>`。
3. 已有 `docs/codebase/`、`docs/context/`、`docs/modules/`、ADR 和 `.gj/context.yml`。
4. GitLab 最近 Milestone、Issue、MR 信息，如 API 可用。

输出：

1. `docs/codebase/STACK.md`
2. `docs/codebase/INTEGRATIONS.md`
3. `docs/codebase/ARCHITECTURE.md`
4. `docs/codebase/STRUCTURE.md`
5. `docs/codebase/CONVENTIONS.md`
6. `docs/codebase/TESTING.md`
7. `docs/codebase/CONCERNS.md`
8. `docs/context/current-state.md` 草案或更新建议
9. `docs/context/module-map.md` 草案或更新建议
10. `docs/modules/*.md` 草案或更新建议
11. `.gj/context.yml` 草案或更新建议

推荐执行策略：

| 分析视角 | 产物 |
|---|---|
| tech | `STACK.md`、`INTEGRATIONS.md` |
| arch | `ARCHITECTURE.md`、`STRUCTURE.md` |
| quality | `CONVENTIONS.md`、`TESTING.md` |
| concerns | `CONCERNS.md` |

如果运行环境支持子任务，可以并行分析四个视角；如果不支持，就在当前会话中按四个 pass 顺序执行。无论哪种方式，最终都必须扫描输出中是否包含疑似密钥。

验收标准：

1. `docs/codebase/` 下 7 个文档存在且非空。
2. 文档包含真实文件路径，例如 `src/order/service/OrderService.java`。
3. 不提交任何 secret、token、password、连接串。
4. 已明确标记“观察到的事实”和“需要人工确认的推断”。
5. 已给出 `docs/context/`、`docs/modules/` 和 `.gj/context.yml` 的更新建议。
6. 既有项目接入 MR 中说明哪些内容需要人工确认后才能作为当前事实。

# 14. GJ 工作流配置

## 14.1 `.gj/workflow.yml`

```yaml
project:
  name: example-service
  default_branch: main
  gitlab_url: https://gitlab.example.com

roles:
  product:
    gitlab_users: ["@product-owner"]
  tech_lead:
    gitlab_users: ["@tech-lead"]

handoff_policy:
  source_of_truth: gitlab
  require_assignee_for_human_steps: true
  require_reviewer_for_mr_review: true

rules:
  - id: database
    paths:
      - "db/migration/**"
      - "**/migrations/**"
    standards:
      - "docs/standards/04-database-standard.md"
      - "docs/standards/06-release-standard.md"
    minimum_flow: "standard"

  - id: security
    paths:
      - "src/**/auth/**"
      - "src/**/permission/**"
    standards:
      - "docs/standards/08-security-standard.md"
    minimum_flow: "standard"
```

## 14.2 `.gj/context.yml`

用于把变更路径映射到模块背景、当前事实文档和 ADR。

```yaml
version: 1

global:
  always_load:
    - "docs/context/current-state.md"
    - "docs/context/module-map.md"
    - "docs/context/glossary.md"

modules:
  order:
    name: 订单模块
    paths:
      - "src/**/order/**"
      - "db/migration/*order*"
    docs:
      - "docs/modules/order.md"
    active_decisions:
      - "docs/technical/decisions/ADR-0001-order-state-machine.md"
    ai_focus:
      - "订单状态机是否兼容历史状态"
      - "审批流是否影响查询、导出和权限"
```

# 15. Skills 设计

当前工作流固定为八个 skills。每个 skill 只负责一个清晰场景，详细规则放入 references，重复 API 操作放入 scripts。所有名称使用 `gj-` 前缀，GJ 是公交工作流的简称。

推荐 skill：

| Skill | 用途 |
|---|---|
| `gj-workflow-bootstrap` | 给项目安装整套工作流。 |
| `gj-codebase-map` | 梳理既有项目，生成 codebase map、当前上下文、模块文档和 `.gj/context.yml` 草案。 |
| `gj-workflow-next` | 读取待办和当前状态，推荐 flow，并判断下一步。 |
| `gj-plan-change` | 按 flow 完成需求、方案、任务边界、测试和回滚计划。 |
| `gj-develop-change` | 实现功能、Fast 改动、Bug 修复和 Hotfix。 |
| `gj-mr-review` | 审查 MR 风险、测试、文档和合并就绪状态。 |
| `gj-release-readiness` | 准备环境、发布、验证和回滚证据。 |
| `gj-close-loop` | 复盘并更新长期上下文。 |

Skill 推荐结构：

```text
gj-plan-change/
  SKILL.md
  references/
    workflow.md
    output-format.md
  scripts/
    fetch_gitlab_context.py
```

原则：

1. `SKILL.md` 写触发条件和核心步骤。
2. 长说明放 `references/`。
3. 可重复、易出错的 API 操作放 `scripts/`。
4. 输出格式固定，便于写回 GitLab。

# 16. AI Orchestrator

AI Orchestrator 是常驻服务，负责接收 GitLab Webhook、读取上下文、调用 AI、写回评论。

核心职责：

1. 接收 Issue、MR、Note、Pipeline、Job 事件。
2. 读取 GitLab Issue/MR/diff/comments/pipeline。
3. 根据事件、标签和评论命令选择 skill。
4. 根据 `.gj/workflow.yml` 和 `.gj/context.yml` 装载规范和背景。
5. 调用 AI Gateway 或模型服务。
6. 把结果写回 GitLab 评论。
7. 维护状态标签互斥。
8. 识别高风险路径并阻止 `flow::fast`。
9. 生成文档决策和复盘改进项。
10. 记录审计日志。

支持命令：

```text
/ai-next
/ai-plan
/ai-develop
/ai-review
/ai-release
/ai-close
```

自动触发建议：

| 事件 | 条件 | 动作 |
|---|---|---|
| Issue opened | `type-requirement` | 需求完整性分析 |
| Issue opened | `type-bug` | 缺陷定位建议 |
| Issue opened | `type-hotfix` | Hotfix 风险和事后补齐清单 |
| MR opened | 非 Draft | MR 摘要和风险提示 |
| Pipeline failed | MR pipeline | 失败分析 |
| Release / 发布完成 | 有发布 Issue | 生成发布摘要 |
| Milestone closed | 有复盘 Issue | 生成复盘并核对长期文档是否仍为真 |

# 17. CI 门禁

## 17.1 `.gitlab-ci.yml`

最小 CI：

```yaml
stages:
  - policy
  - test

policy_check:
  stage: policy
  script:
    - python scripts/policy_check.py

smoke_check:
  stage: test
  script:
    - python scripts/smoke_check.py
```

已有 CI 时，只追加必要 job，不覆盖原有流水线。

## 17.2 `policy_check.py`

MVP 检查项：

1. MR 是否关联 Issue。
2. MR 描述是否填写变更内容。
3. MR 是否填写自测结果。
4. MR 是否填写风险点。
5. MR 是否填写回滚方案。
6. 是否声明 AI 使用情况。
7. MR 是否恰好有一个 `flow::*` 标签。
8. 命中高风险路径时，是否错误使用 `flow::fast`。
9. 是否存在明显 secret、token、password。

`policy_check` 只检查可自动化规则，不替代人工判断。

# 18. 发布与复盘

## 18.1 发布 Issue

发布前必须确认：

1. 本次发布包含哪些 Issue 和 MR。
2. 测试结论已通过。
3. Release Note 已确认。
4. 配置变更和数据库变更已说明。
5. 回滚方案已确认。
6. 监控和发布后验证已准备。

## 18.2 复盘 Issue

复盘输入：

1. 项目总控 Issue。
2. Milestone 完成情况。
3. Issue / MR / Pipeline 数据。
4. 测试和缺陷情况。
5. 发布问题和线上反馈。
6. AI 建议采纳情况。

复盘输出：

1. 项目周期和完成情况。
2. 延期原因。
3. 缺陷分布。
4. AI 提前识别的问题。
5. AI 未识别的问题。
6. 流程改进建议。
7. 需要进入长期上下文的变化。
8. 需要更新的模块文档、ADR、`.gj/context.yml`。

# 19. 安全与合规

禁止输入 AI：

1. 生产密钥、Token、证书、私钥。
2. 客户隐私数据。
3. 未脱敏生产日志。
4. 合同、财务、敏感商业数据。
5. 账号密码、数据库连接串。

AI Gateway 至少要做：

1. 脱敏。
2. 限流。
3. 超时和重试。
4. 模型路由。
5. Prompt 和响应版本记录。
6. 成本和调用审计。

默认不保存完整 prompt 原文和完整 diff，除非公司安全合规允许。

# 20. 指标

## 20.1 交付指标

| 指标 | 含义 |
|---|---|
| 需求创建到确认时长 | 需求澄清效率 |
| 方案评审通过时长 | 方案成熟度 |
| Issue 平均交付时长 | 开发效率 |
| MR 平均 Review 时长 | Review 效率 |
| Pipeline 首次通过率 | 代码质量和 CI 稳定性 |
| Milestone 准时率 | 项目交付能力 |

## 20.2 AI 指标

| 指标 | 含义 |
|---|---|
| AI 需求问题采纳率 | 产品采纳 AI 澄清问题的比例 |
| AI 方案风险命中率 | AI 风险被确认有效的比例 |
| AI Code Review 采纳率 | 开发采纳 AI 建议的比例 |
| AI 测试用例采纳率 | QA 使用 AI 建议的比例 |
| AI 误报率 | 被明确判定无效的建议比例 |

## 20.3 知识沉淀指标

| 指标 | 含义 |
|---|---|
| 当前上下文更新率 | 长期有效变化是否同步到当前事实 / 模块文档 |
| `.gj/context.yml` 命中率 | AI 是否能按路径找到相关背景 |
| ADR 更新及时率 | 架构决策是否及时沉淀 |

# 21. 落地步骤

## 21.1 第一阶段：工作流基础

1. 创建标签体系。
2. 配置 Project Board。
3. 配置 Issue / MR 模板。
4. 配置 Protected Branch。
5. 开启 Pipeline 必须成功、讨论必须解决。
6. 添加 `policy_check.py` 和 CI job。

## 21.2 第二阶段：项目上下文

1. 既有项目先运行 `gj-codebase-map`，生成 `docs/codebase/`。
2. 建立或更新 `docs/context/`。
3. 建立或更新 `docs/modules/`。
4. 按需建立 `docs/technical/decisions/`。
5. 配置 `.gj/workflow.yml`。
6. 配置 `.gj/workflow.yml`。
7. 配置 `.gj/context.yml`。

## 21.3 第三阶段：AI 接入

1. 建立 AI Gateway。
2. 建立 AI Orchestrator。
3. 配置 GitLab Project Webhook。
4. 支持 `/ai-next`、`/ai-plan`、`/ai-develop`、`/ai-review`、`/ai-release`、`/ai-close` 命令。
5. 把 AI 输出写回 GitLab 评论。
6. 加入审计日志和脱敏。

## 21.4 第四阶段：Skills 化

1. 固定八个 `gj-` Skill 作为唯一接口。
2. 每个 Skill 固定输入、输出和 GitLab 写回格式。
3. 新场景优先作为现有 Skill 的 flow 模式或 reference。
4. 把重复 API 操作沉淀成 scripts。
5. 只有出现独立触发条件、流程和输出时才新增 Skill。

# 22. 项目初始化清单

| 步骤 | 产物 | 负责人 |
|---|---|---|
| 1 | 项目仓库 | DevOps / Tech Lead |
| 2 | 标签和 Board | PM / DevOps |
| 3 | Issue / MR 模板 | PM / Tech Lead |
| 4 | `docs/standards/` | Tech Lead / QA / DevOps |
| 5 | `docs/codebase/`，既有项目由 `gj-codebase-map` 生成 | Tech Lead / AI 平台 |
| 6 | `docs/context/` | 产品 / Tech Lead |
| 7 | `docs/modules/` | 模块负责人 |
| 8 | `.gj/workflow.yml` | Tech Lead / AI 平台负责人 |
| 9 | `.gj/workflow.yml` | Tech Lead / 安全 / DevOps |
| 10 | `.gj/context.yml` | Tech Lead / 架构师 |
| 11 | `.gitlab-ci.yml` 和 `policy_check.py` | DevOps |
| 12 | 项目总控 Issue | PM / Tech Lead |
| 13 | Milestone | PM |
| 15 | AI Orchestrator / Webhook | AI 平台 / DevOps |
| 16 | 首批 skills | AI 平台 / 各角色负责人 |

# 23. 团队使用方式

既有项目接入：

```text
使用 gj-codebase-map 梳理当前项目，生成 docs/codebase、docs/context、docs/modules 和 .gj/context.yml 草案。
```

流程分流：

```text
使用 gj-workflow-next 判断 #128 应该走标准需求、小改动、Bug 修复还是 Hotfix。
```

产品经理：

```text
使用 gj-plan-change 分析 #123，准备和业务讨论的问题。
```

Tech Lead：

```text
使用 gj-plan-change 基于 #123 生成方案草案和风险清单。
```

开发：

```text
使用 gj-develop-change 读取 #145、关联方案和项目上下文，告诉我实现时要注意什么。
```

Bug 修复：

```text
使用 gj-develop-change 分析 #156 的复现步骤和日志，给出根因、修复建议和回归范围。
```

紧急修复：

```text
使用 gj-develop-change 处理 #159，输出最小修复路径、发布验证和事后补齐清单。
```

Reviewer：

```text
使用 gj-mr-review 审查 !56，重点看权限、数据库和回滚风险。
```

QA：

```text
使用 gj-plan-change 根据需求、方案和 MR 生成测试用例。
```

项目负责人：

```text
使用 gj-close-loop 总结本 Milestone，并更新仍然有效的项目文档。
```

# 24. 最小可行版本

第一版不要做全量自动化，先跑通：

1. 标签、模板、Board。
2. Protected Branch 和 CI 门禁。
3. `policy_check.py`。
4. 既有项目用 `gj-codebase-map` 生成 `docs/codebase/` 和上下文草案。
5. `gj-workflow-next` 能判断标准需求、小改动、Bug 修复、Hotfix。
6. 需求分析 AI 评论。
7. Bug 修复 AI 建议。
8. MR Review AI 评论。
9. 复盘更新仍然有效的当前事实、模块文档和 ADR。
10. `.gj/context.yml` 能让 AI 读到相关模块背景。

跑通后再扩展：

1. 技术方案草案。
2. 任务拆分。
3. 测试用例。
4. 发布说明。
5. Pipeline 失败分析。
6. 高风险 minimum flow 自动检查。
7. Hotfix 事后复盘自动提醒。
8. 跨项目报表。
9. 完整 skills 包。
