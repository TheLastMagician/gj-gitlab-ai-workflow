# 可持续项目文档与 AI 上下文治理

## 核心模型

GJ 的文档决策使用同一个公式：**变更影响决定文档类型，Flow 决定最低严谨程度，流程
阶段决定写入时机和确认人**。不是每个需求复制一整套模板，也不是发布后集中补文档。

GitLab 与仓库各自只有一种职责：

| 信息 | 唯一事实源 |
| --- | --- |
| 本次变更、讨论、状态、分工、审批和过程证据 | GitLab Issue、MR、评论、Pipeline |
| 当前产品、交互、技术、API、数据和模块事实 | `docs/product/`、`docs/technical/`、`docs/modules/` |
| 可复用测试基线 | `docs/qa/test-plans/` |
| 按版本冻结的交付证据 | `docs/qa/test-reports/<tag>.md`、`docs/releases/<tag>.md` |
| 仓库与环境当前状态 | `docs/context/current-state.md` |
| AI 文档路由 | `.gj/context.yml` |

Requirement 或 Hotfix Issue 是一次变更的主工作项。Solution、Task、Test Issue 只在独立
负责人、排期、依赖或单独跟踪有价值时创建；它们不能替代仓库里的方案和测试文档。

## 一个需求的文档流转

| 阶段 | Skill | 仓库文档动作 | 完成标志 |
| --- | --- | --- | --- |
| 入口 | `gj-workflow-next` | 只列预期文档影响 | 人确认 flow、Target release 和主工作项 |
| 需求确认 | `gj-plan-change` | 产品变化更新 PRD；交互变化更新设计/原型 | PdM 确认需求事实 |
| 方案/测试设计 | `gj-plan-change` | 按影响更新方案、API、数据库、ADR 和测试计划 | Dev Lead/QA 确认可实施、可验证 |
| 开发 | `gj-develop-change` | 代码、测试和受影响长期文档在同一 MR 更新 | 分支文档与分支代码一致 |
| MR 审阅 | `gj-mr-review` | 通常不新建；发现差异在原 MR 修正 | Reviewer 核对决策表和实际 diff |
| QA/发布 | `gj-release-readiness` | 按 Tag 生成测试报告和发布说明 | 发布证据足以让人决策 |
| 收尾 | `gj-close-loop` | 回写实际 Tag/SHA/环境和当前事实，冻结证据 | 未解决项都有 Issue、Owner 和期限 |

`confirmed` 只表示相应责任人确认了规范，不等于已经部署。生产事实必须由 Git Tag、
commit SHA、Pipeline、Environment 和 `current-state.md` 共同证明。

## Flow 深度

| Flow | 最低要求 |
| --- | --- |
| Fast | 不强制计划文档；持久事实变化仍更新对应长期文档 |
| Standard | Requirement Issue 必须；按实际影响更新需求、设计、技术、API、数据库和测试文档 |
| Hotfix | 先记录影响、最小修复、验证和回滚；不能同步完成的文档必须跟踪并在收尾补齐 |

高风险路径不能用 Fast。文档类型由实际影响决定，不能用“改动很小”豁免业务规则、API、
数据库、权限或数据含义的更新。

## 路径和模板

真实项目文档使用稳定语义名：

```text
docs/product/requirements/<capability>.md
docs/product/designs/<capability>.md
docs/product/prototypes/<capability>.md
docs/technical/solutions/<capability>.md
docs/technical/apis/<domain>.md
docs/technical/database/<domain>.md
docs/technical/decisions/ADR-<number>-<decision>.md
docs/modules/<module>.md
docs/qa/test-plans/<capability>.md
docs/qa/test-reports/<tag>.md
docs/releases/<tag>.md
```

安装后模板位于 `.gj/doc-templates/`，不属于项目事实。禁止把 `PRD.md`、
`solution-design.md`、`test-report.md` 等通用模板名留在事实目录，也不要创建
`v2/final/new` 副本。

## 通用文档契约

当前产品、技术、模块和测试计划文档至少包含：

```markdown
- Owner:
- Status: draft | confirmed
- Source Issue:
- Target release:
- Effective from:
- Implemented by:
- Related documents:
- Last verified:
```

正文描述当前完整事实，不写“本次新增了什么”的变更流水账。API 结构优先以 OpenAPI、
AsyncAPI、protobuf 等机器契约为事实源；数据库结构以 schema/model/migration 为执行事实
源，Markdown 解释业务语义、权限、不变量、兼容、迁移和恢复。计划、实现摘要和 MR
文档决策必须同时写出可执行路径与 Markdown 路径；未知路径要写 `TBD + Owner`。

测试报告状态使用 `draft/passed/failed/blocked`，发布说明使用
`draft/ready/released/rolled-back`。版本证据关闭后冻结；当前事实过时时直接修改或删除，
历史由 Git 和 GitLab 追溯。

## Skill 文档决策

每个执行 Skill 输出：

```markdown
## 文档决策

| 文档 | 动作 | 触发事实 | 阶段/状态 | 确认人或跟进 |
| --- | --- | --- | --- | --- |
| docs/modules/order.md | update | 审批规则变化 | develop / confirmed | @owner |
```

动作只能是 `create/update/no-change/follow-up`。`follow-up` 必须包含 GitLab Issue、
负责人和期限。Reviewer 对照实际行为、diff、文档元数据和人的确认记录。

安装到业务项目后的完整内容契约、各类文档必填正文、责任人和结构审计规则位于
`docs/standards/12-context-governance.md`。`context_freshness_check.py` 默认只告警，
专项治理时使用 `--strict`；内容正确性仍由对应 Owner 确认。
