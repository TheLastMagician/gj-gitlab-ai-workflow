# 项目文档生命周期与 AI 上下文治理

## 1. 信息职责和唯一事实源

项目文档只保存后续开发、测试和发布仍需依赖的结论。一次变更的提议、讨论、任务状态、
分工、审批和过程证据留在 GitLab，不复制到仓库形成第二份流水账。

| 信息 | 唯一事实源 | 生命周期 |
| --- | --- | --- |
| 本次变更的原因、范围、讨论、负责人和决策记录 | GitLab Requirement/Hotfix Issue、MR 和评论 | 工作中追加，关闭后保留 |
| 项目技术栈、架构边界、开发和测试工具链规范 | `01-development-standard.md`、`07-test-standard.md` | Dev Lead/QA 确认后原地维护 |
| 当前产品要求和交互 | `docs/product/` | 按能力原地更新，过时内容直接删除 |
| 当前技术、接口、数据和模块事实 | `docs/technical/`、`docs/modules/`、ADR | 按边界原地更新；ADR 确认后冻结 |
| 可复用的功能测试基线 | `docs/qa/test-plans/` | 按能力原地更新 |
| 某次发布的测试和发布证据 | `docs/qa/test-reports/<tag>.md`、`docs/releases/<tag>.md` | 按 Tag 新建，发布关闭后冻结 |
| 仓库与已部署环境的当前状态 | `docs/context/current-state.md` | 事实变化时覆盖更新 |
| AI 文档路由 | `.gj/context.yml` | 路径或模块边界变化时更新 |

Requirement 或 Hotfix Issue 是一次变更的主工作项。Solution、Task、Test Issue 只有在
存在独立负责人、排期、依赖或需要单独跟踪时才拆分；它们不能替代仓库中的长期文档。
缺陷使用 Bug Issue，发布协调可以使用 Release Issue，复盘使用 Retro Issue。

## 2. 文档决策公式

每次变更按以下顺序决定文档，不按模板数量机械产出：

1. **变更影响决定文档类型**：产品行为、交互、API、数据、模块规则、测试基线或发布
   事实改变，才命中对应文档。
2. **Flow 决定最低严谨程度**：Fast 允许省略计划文档；Standard 要求影响分析和确认；
   Hotfix 允许先止血，但欠账必须可跟踪并在收尾补齐。
3. **流程阶段决定写入时机**：计划阶段形成 draft，人的决策门确认，开发阶段随代码在
   同一 MR 更新，发布阶段生成版本证据，收尾回写实际状态。

没有改变后续人员需要依赖的事实时，明确写 `no-change`，不要创建空文档。

## 3. 阶段、产物和完成门

| 阶段 | 主要 Skill | GitLab 产物 | 仓库文档动作 | 完成门 / 确认人 |
| --- | --- | --- | --- | --- |
| 既有项目接入/重大重构 | `gj-codebase-map` | 接入 MR；技术债和缺陷按需建 Issue | 起草开发/测试规范、当前状态、模块地图、模块文档和 `.gj/context.yml` | Dev Lead/QA 确认规范草稿；不保存中间扫描报告 |
| 入口分流 | `gj-workflow-next` | Standard 创建 Requirement Issue；Hotfix 创建 Hotfix Issue；Fast 按需创建 SmallChange Issue | 不默认写仓库文档，只列预期文档影响 | flow、目标版本、主工作项由 PdM/PM 确认 |
| 需求确认 | `gj-plan-change` | 在主 Issue 记录范围、验收、反例和决策 | 产品行为变化时创建/更新 PRD；有交互时更新设计/原型记录 | PdM 将需求事实从 `draft` 确认为 `confirmed` |
| 方案与测试设计 | `gj-plan-change` | 评审结论留在主 Issue；仅按需拆 Solution/Task/Test Issue | 按影响更新技术方案、API、数据库、ADR 和测试计划 | Dev Lead 确认技术事实；QA 确认测试基线 |
| 开发 | `gj-develop-change` | MR 记录实现、自测、风险、回滚和文档决策 | 代码、测试、模块及受影响长期文档在同一 MR 更新 | 分支中的文档与分支代码一致 |
| MR 审阅 | `gj-mr-review` | Findings、讨论和合并结论 | 通常不创建；发现不一致就在原 MR 修正 | Reviewer 核对文档决策、diff 和确认记录 |
| QA/发布准备 | `gj-release-readiness` | Release Issue 按需协调发布 | 创建/更新 `<tag>` 测试报告和发布说明 | QA 给出结论；DevOps 准备发布证据 |
| 发布 | 人工 + GitLab CI/CD | Tag、Pipeline、Environment | 不在发布过程中临时补长期设计 | 人决定 Tag、构建和部署 |
| 收尾 | `gj-close-loop` | 遗留问题建 Issue；重要里程碑按需建 Retro Issue | 回写实际 Tag/SHA/环境、当前事实和索引；冻结版本证据 | 对应 Owner 确认事实，未解决项都有负责人和期限 |

计划文档可以先在实现分支或 Draft MR 中形成并接受评审；进入默认分支时，应与该分支
实际代码一致。`confirmed` 表示人已确认该规范，不表示已经部署；生产事实以 Tag、SHA、
Environment 和 `current-state.md` 为准。

## 4. 三种 Flow 的最低文档要求

| Flow | 计划阶段 | 开发/MR | 发布和收尾 |
| --- | --- | --- | --- |
| `flow::fast` | 不强制 PRD、方案或独立 Issue；必须说明范围、自测和文档影响 | 只要持久事实变化，仍须更新对应长期文档；高风险路径不能走 Fast | 有用户或运维影响才进入发布文档；无变化明确 `no-change` |
| `flow::standard` | Requirement Issue 必须；按影响形成 PRD、设计、技术/API/数据库方案和测试计划 | 代码、测试与所有受影响长期文档同 MR；确认记录可追溯 | 正式 QA 形成版本测试报告；有发布影响形成发布说明 |
| `flow::hotfix` | Hotfix Issue 必须；先记录影响、最小修复、验证和回滚，不为凑模板延误止血 | 能同步的文档同 MR；不能同步的使用 `follow-up`，写明 Issue、负责人和期限 | 发布后必须补回归证据、受影响长期事实和根因/流程跟进 |

持久事实包括业务规则、权限、状态流、接口契约、数据含义、关键技术决策、测试基线、
发布/回滚方式和当前运行状态。改动行数不是判断依据。

## 5. 路径、命名和模板

| 文档类型 | 真实文档路径 | 命名 |
| --- | --- | --- |
| 项目开发规范 | `docs/standards/01-development-standard.md` | 单文件原地维护，包含技术基线和工程约定 |
| 项目测试规范 | `docs/standards/07-test-standard.md` | 单文件原地维护，包含测试工具链和执行规则 |
| PRD | `docs/product/requirements/<capability>.md` | 使用稳定能力名，不带版本或状态后缀 |
| 产品设计 | `docs/product/designs/<capability>.md` | 与 PRD 能力名一致 |
| 原型记录 | `docs/product/prototypes/<capability>.md` | 只记录可访问的原型和评审结论 |
| 技术方案 | `docs/technical/solutions/<capability>.md` | 按稳定技术/功能边界 |
| API 契约 | `docs/technical/apis/<domain>.md` | 按 API 或领域边界 |
| 数据库设计 | `docs/technical/database/<domain>.md` | 按数据领域边界 |
| ADR | `docs/technical/decisions/ADR-<number>-<decision>.md` | 编号加语义名，确认后冻结 |
| 模块文档 | `docs/modules/<module>.md` | 与代码模块边界一致 |
| 测试计划 | `docs/qa/test-plans/<capability>.md` | 与需求能力名一致 |
| 测试报告 | `docs/qa/test-reports/<tag>.md` | 如 `v1.3.0.md` |
| 发布说明 | `docs/releases/<tag>.md` | 与 Git Tag 完全一致 |

工作流模板位于 `.gj/doc-templates/`，它们不是项目事实。真实文档不能使用
`PRD.md`、`solution-design.md`、`test-report.md` 等模板式通用文件名，也不要创建
`v2`、`final`、`new` 副本。

开发和测试规范随工作流直接安装，不从功能模板创建。`gj-codebase-map` 可以根据现有
代码起草待确认内容，但不能保留 `docs/codebase/` 中间报告，也不能把已有代码习惯自动
认定为正确规范。

## 6. 通用文档契约

当前产品、技术、模块和测试计划文档至少包含：

```markdown
## 元数据

- 负责人：
- 状态：draft
- 来源 Issue：
- 目标版本：
- 生效范围：
- 实现 MR：
- 相关文档：
- 最后核验日期：
```

- `状态` 只使用 `draft` 或 `confirmed`。确认时记录确认人和日期。
- `生效范围` 表示从哪个 Tag 或仓库状态开始适用；未发布时允许写 `pending`。
- `实现 MR` 链接实际 MR；计划阶段允许留空，开发阶段补齐。
- `最后核验日期` 是最后一次对照代码或业务确认的日期，不等于普通编辑时间。
- 文档正文必须描述当前完整事实，不能只写“本次增加了什么”。
- 文档中不写 Token、密钥、生产数据和未脱敏日志。

版本证据使用自己的状态：测试报告为 `draft/passed/failed/blocked`；发布说明为
`draft/ready/released/rolled-back`。证据完成后只允许修正客观错误并留下说明，不覆盖成
下一版本内容。

## 7. 各类文档最低正文

| 文档 | 必填内容 | 人工确认 |
| --- | --- | --- |
| 项目开发规范 | 语言/运行时、前后端栈、构建命令、架构和目录边界、命名、错误/日志、格式和静态检查 | Dev Lead |
| 项目测试规范 | 测试框架和版本、目录/命名、fixture/mock/数据、聚焦和完整命令、覆盖与 CI 门禁 | QA/Dev Lead |
| PRD | 背景、目标、非目标、用户场景、规则、可测试验收、反例、依赖、待确认问题 | PdM |
| 产品设计/原型 | 用户流、页面和状态、权限差异、异常/空态、关键文案、无障碍、原型链接 | PdM/设计负责人 |
| 技术方案 | 影响范围、方案、备选取舍、风险、测试、上线、监控和回滚 | Dev Lead |
| API 契约 | 权威 schema 位置、请求/响应、错误、权限、幂等、兼容和回归要求 | API 负责人/开发经理 |
| 数据库设计 | 权威 schema/migration、实体关系、字段语义、约束、索引、数据保留、迁移和回滚 | 数据负责人/开发经理 |
| ADR | 背景、决策、备选项、取舍和后果 | Dev Lead；确认后冻结 |
| 模块文档 | 职责边界、业务规则、状态/失败行为、接口和数据契约、依赖、测试入口 | 模块负责人 |
| 测试计划 | 需求/风险到用例映射、成功/失败/权限/回归、环境、数据和阻断条件 | QA |
| 测试报告 | Tag/SHA/Pipeline、环境、结果、证据、缺陷、剩余风险和 QA 结论 | QA |
| 发布说明 | 包含项、用户/运维影响、来源 SHA、测试、发布、监控、回滚和实际部署结果 | DevOps/发布负责人 |
| current state | 当前仓库版本、环境部署版本、已确认能力、限制和近期重点，不写变更流水账 | PM/DevOps |

API 有 OpenAPI/AsyncAPI 等机器可读定义时，以它为契约结构事实源，Markdown 只补业务
语义、权限、错误和兼容规则。数据库以 schema 和 migration 代码为执行事实源，Markdown
解释数据含义、不变量和运维策略，避免复制一份会漂移的完整 DDL。方案、实现结果和 MR
文档决策必须同时列出可执行路径和解释文档路径；路径未定时写 `TBD`、负责人和确认期限。

## 8. 创建、更新、冻结和删除

1. 没有持久事实变化：不建文档，文档决策写 `no-change`。
2. 技术栈、架构边界或工程约定变化：原地更新 `01-development-standard.md`；测试工具链
   或执行规则变化：原地更新 `07-test-standard.md`。
3. 已有同一能力、模块或契约边界：原地更新为当前完整事实。
4. 新的稳定能力、模块或独立评审边界：从 `.gj/doc-templates/` 复制合适模板并使用
   语义文件名创建。
5. ADR：新的不可逆或跨团队技术取舍才新增；确认后不改写，后续用新 ADR 取代。
6. 测试报告和发布说明：按 Tag 新建，关闭后冻结。
7. 当前事实失效：直接修改或删除；历史由 Git、Issue/MR 和冻结证据追溯。
8. 文档路径或模块边界变化：同步更新 `.gj/context.yml` 和直接上下游链接。

## 9. Skill 的文档决策输出

每个执行 Skill 必须在回复、Issue 评论或 MR 描述中输出下表；它不是新文件：

```markdown
## 文档决策

| 文档 | 动作 | 触发事实 | 阶段/状态 | 确认人或跟进 |
| --- | --- | --- | --- | --- |
| docs/modules/<module>.md | update | 模块业务规则变化 | develop / confirmed | @module-owner |
| docs/technical/apis/<domain>.md | no-change | API 契约未变化 | develop / - | - |
```

动作只能是 `create`、`update`、`no-change` 或 `follow-up`。每一种受影响的持久事实都要
有一行；`follow-up` 必须包含 GitLab Issue、负责人和期限。Reviewer 逐项对照实际 diff、
行为变化、确认记录和目标版本。

## 10. AI 渐进加载与结构审计

1. 当前 Issue/MR。
2. `.gj/context.yml` 的 `global.always_load`。
3. changed paths 命中的模块文档和有效 ADR。
4. 工作项或模块明确链接的 PRD、设计、方案、API、数据库和测试文档。
5. 仅为明确追溯问题读取指定 Git 历史、Issue/MR 或版本证据。

`context_freshness_check.py` 默认只告警无效路径、上下文预算、通用模板文件误入事实目录、
语义命名和必要元数据问题，不进入默认 CI 门禁。专项治理时使用 `--strict`。脚本不能判断
事实是否正确，内容仍由对应负责人和决策门确认。
