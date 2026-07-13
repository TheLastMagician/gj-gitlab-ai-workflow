# gj-gitlab-ai-workflow

这是一个面向 GitLab CE 项目的 AI 协作工作流骨架。它提供 GitLab 模板、项目
上下文目录、CI 门禁脚本、角色交接规则，以及一组遵循 Agent Skills 开放格式、
可同时用于 Codex、Claude Code 和 OpenCode 的 workflow skills。

核心目标不是让 AI 自主审批、合并或发布，而是让团队里的产品经理（PdM）、项目经理
（PM）、开发经理（Dev Lead）、开发（Dev）、代码审阅（Reviewer）、测试（QA）、运维
（DevOps）、合并（Maintainer）都可以用 AI 辅助完成自己负责的动作。最终责任和确认权
仍然在人手里。

## 快速安装 Skills

在需要使用工作流的业务项目根目录运行一条命令，即可同时安装到 Codex、
Claude Code 和 OpenCode：

```powershell
npx --yes skills@1.5.15 add https://github.com/TheLastMagician/gj-gitlab-ai-workflow --skill '*' -a codex -a claude-code -a opencode --copy -y
```

安装结果：Codex 和 OpenCode 使用项目内 `.agents/skills`，Claude Code 使用
`.claude/skills`。安装后重新打开 Agent 会话。只使用一个 Agent 时，可以只保留对应的
`-a codex`、`-a claude-code` 或 `-a opencode` 参数。

GitHub 链接不会自动执行代码；用户需要运行上述命令，或明确要求当前 Agent 执行安装。
没有 Node.js 时，先 clone 本仓库，再运行 Python 兜底安装器：

```powershell
python scripts/install_skills.py --agent all --project-root C:\path\to\your-project --force
```

这一步安装 8 个 `gj-*` Skills。业务仓库所需的 GitLab 模板、CI 门禁、`.ai/` 和
`docs/` 资产需要再执行一次“新项目怎么初始化”中的 `install_workflow.py`。

## GitLab Access Token 怎么配置

只安装 Skill、生成计划或处理本地代码不需要 Token。以下操作需要连接真实 GitLab：

- `gj-workflow-next` 读取个人 Todo、Issue、MR、讨论和 Pipeline；
- 校验项目成员与角色映射；
- 经人确认后创建 Issue、设置标签或处理人、发布交接评论。

优先使用 Codex、Claude Code 或 OpenCode 已配置的 GitLab MCP/连接器，并按该工具的
方式授权。没有连接器时，可让项目认可的 API helper 从以下环境变量读取配置：

```powershell
$env:GITLAB_URL = "https://gitlab.example.com"
$env:GITLAB_PROJECT_ID = "group/project"
$secureToken = Read-Host "GitLab Access Token" -AsSecureString
$env:GITLAB_TOKEN = [System.Net.NetworkCredential]::new("", $secureToken).Password
```

读取自己的 Todo 时使用当前用户的 Personal Access Token：只读场景选择 `read_api`；
确实需要写 Issue、标签、处理人或评论时才选择 `api`。自动化服务可改用独立的 Project
Access Token，但它代表机器人账号，不能代替当前用户的个人 Todo。Token 应设置较短
有效期并只给最低项目角色；不要选择 `sudo`、`write_repository` 或管理员权限。

不要把 Token 写进代码、README、`.ai/project.yml`、Git remote、Issue/MR 或仓库内
的 `.env`，即使该文件已被 Git 忽略。CI 中应使用 GitLab Settings -> CI/CD ->
Variables 的 masked/protected 变量。本地配置、连接方式和验证命令见
[GitLab 访问配置](docs/gitlab-access.md)。

## 这个项目提供什么

- GitLab Issue / MR 模板，以及 `flow::fast`、`flow::standard`、
  `flow::hotfix` 三个流程标签。
- `.ai/project.yml`、`.ai/rule-map.yml`、`.ai/context-index.yml`、`.ai/role-map.yml`
  等 AI 工作流配置。
- `docs/context`、`docs/modules`、`docs/iterations` 等长期上下文目录。
- PRD、产品设计、原型记录、技术方案、测试计划、测试报告、发布说明等文档模板。
- 目标业务项目 CI：MR 运行 `policy -> workflow -> test`，tag 或手工发布再运行 `release`。
- `policy_check.py`、`workflow_assets_check.py`、`validate_role_map.py` 等检查脚本。
- GitLab webhook Orchestrator 骨架。
- 八个跨 Agent workflow skills。
- 所有 Skill 固定使用 `gj-` 前缀；GJ 是“公交”工作流的简称。
- `examples/demo-project` 和 `examples/demo-run`，用于查看一次端到端模拟留下的样例产物。

## Fast、Standard、Hotfix 怎么选

| 标签 | 适用场景 | Issue | 计划和证据 | 合并与发布要求 |
| --- | --- | --- | --- | --- |
| `flow::fast` | typo、文案、低风险小修复、范围明确且验证简单的局部改动 | 可选；需要排期、协作或追踪时再建 SmallChange Issue | 极简计划；MR 写清动机、范围、自测、风险和文档影响 | 正常 MR 和 Pipeline；默认不增加审批人数 |
| `flow::standard` | 新功能、业务规则、权限、金额、API、数据库、跨模块改造，或风险与验证方式不清楚 | 必须关联 Issue | 完整验收标准、技术方案、任务、测试、文档影响、发布和回滚计划 | 人确认方案；MR Pipeline 全绿后由有权限的人决定合并 |
| `flow::hotfix` | 生产阻塞、P0/P1、安全事件、数据风险，需要立即止血或修复 | 必须关联 Hotfix Issue | 影响范围、止血方案、最小安全修复、验证和明确回滚；事后补测试、文档和复盘 | 最小必要 Review；人决定紧急发布并验证，随后完成闭环 |

`gj-workflow-next` 根据需求和预计改动路径推荐一个标签，人必须在编码前确认。
有 Issue 时把标签加在 Issue 上，创建 MR 时继续使用同一个且唯一的 `flow::*` 标签。
命中 `.ai/rule-map.yml` 高风险路径时不能使用 Fast；CI 会拒绝缺失标签、多个 flow
标签以及高风险改动误用 Fast。

## 角色怎么理解

| 统一称呼 | 主要责任 |
| --- | --- |
| 产品经理（PdM） | 负责需求来源、业务目标、验收标准、非目标、产品规则、原型/交互说明。 |
| 项目经理（PM） | 负责推进节奏、排期、风险、跨角色协调、复盘和待办闭环。 |
| 开发经理（Dev Lead） | 负责技术方案、架构判断、任务拆分、技术风险、技术评审口径。 |
| 开发（Dev） | 负责编码、单测、自测、提交 MR、修复审阅或测试发现的问题。 |
| 代码审阅（Reviewer） | 负责审 MR，检查代码质量、风险路径、测试覆盖和文档影响。 |
| 合并（Maintainer） | 负责最终合并判断和合并操作，通常需要 GitLab 维护者权限。 |
| 测试（QA） | 负责测试计划、验收测试、回归测试、测试报告、缺陷跟踪。 |
| 运维（DevOps） | 负责 CI/CD、环境部署、共享测试环境锁、发布准备、回滚方案。 |
| 任意成员（Member） | 通过 `gj-workflow-next` 查看待办、确认 flow 和下一步。 |

这些是责任帽子，不代表必须有对应人数；同一个人可以承担多个角色。高风险改动仍建议由第二个人确认。

## 新项目怎么初始化

这里的“新项目”指你自己的业务项目，不是把业务项目打包成这个开源项目。

1. 按“快速安装 Skills”执行一次跨 Agent 安装。

2. 在目标业务项目里一次性安装工作流资产：

```powershell
python scripts/install_workflow.py --target C:\path\to\your-project
```

安装只做一次。日常流程由工作项和 MR 的 `flow::*` 标签决定，
不需要重新安装或升级工作流。

已有项目建议先只补缺失文件：

```powershell
python scripts/install_workflow.py --target C:\path\to\your-project --only-missing
```

确实要覆盖模板时再使用备份模式：

```powershell
python scripts/install_workflow.py --target C:\path\to\your-project --force --backup
```

3. 使用 `gj-workflow-bootstrap` 辅助初始化目标项目：

- 确认 GitLab labels、Issue/MR 模板、CI、目录结构是否完整。
- 创建 `flow::fast`、`flow::standard`、`flow::hotfix` 标签。
- 填写 `.ai/project.yml` 的项目基本信息。
- 按需填写 `.ai/role-map.yml`，把产品经理（PdM）、项目经理（PM）、开发经理（Dev Lead）、
  开发（Dev）、代码审阅（Reviewer）、合并（Maintainer）、测试（QA）、运维（DevOps）
  映射到真实 GitLab 用户。
- 确认 `.ai/rule-map.yml` 的 MR 门禁规则。
- 确认保护分支、可合并角色、必须通过 Pipeline 后才能 merge。
- `CODEOWNERS` 仅用于推荐 Reviewer，不作为 GitLab CE 强制审批证据。

4. 如果是已有代码项目，继续使用 `gj-codebase-map`：

- 扫描现有模块、入口、关键流程、测试和风险点。
- 生成或更新 `docs/context/current-state.md`。
- 生成或更新 `docs/context/module-map.md`。
- 生成或更新 `docs/modules/*.md`。
- 更新 `.ai/context-index.yml`，让后续 AI 能稳定读取项目背景。

5. 配置 GitLab 通知和待办来源：

- GitLab Issue 的 `assignee` 是当前处理人。
- GitLab MR 的 `reviewer` 是当前代码审阅。
- 交接评论必须 `@username`。
- 企业微信、邮箱等只是 GitLab 通知投递渠道。
- 个人待办统一由 `gj-workflow-next` 通过 GitLab API 读取，不绕到邮件里解析。

## 一个新需求怎么流转

新需求可以直接用自然语言交给 `gj-workflow-next`。它识别这是新工作，推荐 flow，
并路由到 `gj-plan-change` 补齐验收和方案。人确认需求与唯一 flow 标签后，有 GitLab
能力的 Agent 才创建 Issue；没有连接时输出完整 Issue 草稿，由人提交。已有待办也从
`gj-workflow-next` 开始。

最短操作路径：

```text
描述新需求或选择现有工作项
  -> gj-workflow-next 推荐 flow 并路由计划
  -> 人在编码前确认唯一 flow 标签
  -> 创建 GitLab Issue（Fast 可按规则省略）
  -> plan-change（Fast 可极简）
  -> develop-change 开发和自测
  -> 创建 MR，并选择同一个 flow 标签
  -> CI + mr-review
  -> 人决定合并和发布
  -> close-loop 更新长期上下文
```

```mermaid
flowchart TD
  A["描述新需求或选择 GitLab 待办"] --> B["gj-workflow-next<br/>识别状态并推荐 flow"]
  B --> C{"人确认唯一 flow 标签"}
  C -- "flow::standard" --> D["gj-plan-change<br/>需求、方案、任务和测试"]
  C -- "flow::fast" --> E["gj-develop-change<br/>边界明确后直接实现"]
  C -- "flow::hotfix" --> E
  D --> E
  E --> F["创建 MR<br/>选择相同 flow 标签"]
  F --> G["CI policy / workflow / test"]
  G --> H["gj-mr-review<br/>问题审阅与合并就绪检查"]
  H --> I{"存在阻塞问题？"}
  I -- "是" --> E
  I -- "否" --> J["人决定并执行合并"]
  J --> K["gj-release-readiness<br/>发布、验证和回滚证据"]
  K --> L["人决定并执行发布"]
  L --> M["gj-close-loop<br/>复盘并更新长期上下文"]
```

| 阶段 | 角色 | 使用 skill | 产物 |
| --- | --- | --- | --- |
| 入口和分流 | 任意成员（Member） | `gj-workflow-next` | 待办、flow 建议、阻塞项和下一步；人确认标签 |
| 变更计划 | 产品经理（PdM）/开发经理（Dev Lead） | `gj-plan-change` | 与 flow 匹配的验收、方案、任务、测试和回滚计划 |
| 开发和修复 | 开发（Dev） | `gj-develop-change` | 功能、Fast 改动、Bug 或 Hotfix 的实现、测试和文档 |
| MR 审阅 | 代码审阅（Reviewer） | `gj-mr-review` | 按严重级别排列的问题和合并就绪结论 |
| 合并 | 合并（Maintainer） | GitLab | 人检查证据并决定、执行合并 |
| 发布准备 | 运维（DevOps）/测试（QA） | `gj-release-readiness` | 环境锁、发布说明、验证、回滚和人工确认项 |
| 发布 | 运维（DevOps）/Maintainer | GitLab CI/CD | 人决定、执行发布 |
| 收尾 | 项目经理（PM）/开发经理（Dev Lead） | `gj-close-loop` | 复盘、模块文档、ADR、context index 和摘要更新 |

每个节点完成后，都要在 GitLab 上设置下一个处理人的 assignee/reviewer，并用
`@username` 评论交接。被指派的人可以用 `gj-workflow-next` 查看自己的待办，再进入
对应节点的 skill。

关键规则：

- Standard / Hotfix 必须关联 Issue；Fast 低风险 MR 可以不建 Issue。
- 工作开始前由人确认唯一通道标签：`flow::fast`、`flow::standard` 或 `flow::hotfix`。
- 创建 MR 时选择同一个 flow 标签；CI 校验缺失、冲突和高风险误用。
- 没有验收标准不排期。
- 复杂需求没有方案评审不进入开发。
- 代码必须通过 MR 合并。
- Pipeline 必须成功才能合并。
- 低风险 Fast MR 不要求额外审批人数；高风险 changed files 不能走 Fast。
- GitLab CE 的硬门禁是成功 Pipeline、保护分支和受限合并权限。
- AI 可以辅助审批判断、审阅、合并检查、发布准备，但不能脱离人的明确授权自主审批、自主合并、自主发布。
- 每个需要人处理的节点都要设置 assignee/reviewer，并用 `@username` 评论交接。
- Issue/MR 记录讨论过程，仓库 `docs/` 记录稳定结论。

## 个人如何用 AI 处理待办

对个人来说，日常入口只有 `gj-workflow-next`。它读取 GitLab Todo、Issue、MR、
审阅请求、失败 Pipeline 和未解决讨论，推荐 flow 和下一步 Skill；人确认后再执行。

```mermaid
flowchart TD
  A["gj-workflow-next<br/>读取 GitLab 待办和项目状态"] --> B["选择一个待办"]
  B --> C["AI 推荐 flow 和下一步 Skill"]
  C --> D{"人确认标签和处理方式？"}
  D -- "确认" --> E["plan / develop / review / release / close"]
  D -- "暂不处理" --> I["处理下一项或结束"]
  E --> F["人审阅 AI 结果"]
  F --> G["写回 GitLab 或仓库"]
  G --> H["设置 assignee/reviewer + @username 交接"]
  H --> I
```

| 待办类型 | 常用 skill | 人需要确认什么 |
| --- | --- | --- |
| 新工作、Bug 或流程阻塞 | `gj-workflow-next` | flow 标签、优先级和下一步。 |
| 需求、方案、任务和测试设计 | `gj-plan-change` | 验收、方案、风险、任务边界和测试覆盖。 |
| 开发、Bug 修复或 Hotfix | `gj-develop-change` | 实现范围、测试、文档和回滚。 |
| MR 审阅或合并前检查 | `gj-mr-review` | 阻塞问题和是否进入人的合并决定。 |
| 环境或发布准备 | `gj-release-readiness` | 环境锁、部署版本、验证、回滚和发布窗口。 |
| 复盘或上下文沉淀 | `gj-close-loop` | 长期事实、文档更新和后续事项。 |

这不是“AI 自动把所有事情做完”。正确边界是：AI 帮人读取上下文、生成草稿、做检查、
执行范围明确的分析、代码、文档和测试；人负责 flow、审批、合并、发布和交接。

## 常用 skill 使用场景

| Skill | 什么时候用 |
| --- | --- |
| `gj-workflow-bootstrap` | 新项目接入，安装并检查标签、模板、上下文和 CI 门禁 |
| `gj-codebase-map` | 旧项目第一次接入或大型重构后刷新代码库上下文 |
| `gj-workflow-next` | 每天开始工作、检查待办、推荐 flow 或判断下一步 |
| `gj-plan-change` | 需求、方案、任务、测试或回滚需要按 flow 规划 |
| `gj-develop-change` | 实现功能、Fast 改动、Bug 修复或 Hotfix |
| `gj-mr-review` | 审 MR、检查风险和测试，并给出合并就绪结论 |
| `gj-release-readiness` | 准备环境、发布说明、验证、监控和回滚证据 |
| `gj-close-loop` | 完成后复盘并更新长期文档和 AI 上下文 |

## 文档怎么维护

每个核心 skill 都应该输出 `Documentation impact`，说明本次是否需要创建或更新正式文档。

默认规则：

- GitLab Issue/MR：记录讨论、澄清、人工确认、交接和审阅过程。
- 仓库 `docs/`：记录长期有效的产品、技术、测试、发布和 AI 上下文结论。

常见文档位置：

| 内容 | 推荐路径 |
| --- | --- |
| 产品需求、验收标准、业务规则 | `docs/product/requirements/<feature>.md` |
| 页面、交互、用户流、错误文案 | `docs/product/designs/<feature>.md` |
| 原型链接、截图、HTML demo、可点击原型记录 | `docs/product/prototypes/<feature>.md` |
| 架构、接口、数据、权限、兼容、发布和回滚 | `docs/technical/solutions/<feature>.md` |
| 验收、回归、权限、失败路径、发布验证 | `docs/qa/test-plans/<feature>.md` |
| 测试执行结果、失败项、阻塞项 | `docs/qa/test-reports/<feature>.md` |
| 用户可见变更、部署步骤、回滚步骤 | `docs/releases/<version>.md` |
| 长期 AI 上下文 | `docs/context`、`docs/modules`、`docs/iterations/*/ai-context-summary.md`、`.ai/context-index.yml` |

## 目标项目 CI/CD

安装到业务项目里的 GitLab CI 是业务项目流水线：

```text
Fast / Standard MR: policy -> workflow -> test
Tag / 手工主分支发布: policy -> workflow -> test -> release
```

各阶段含义：

- `policy`：要求唯一 `flow::*` 标签，并检查 MR 内容、文档影响、changed-file 风险和疑似 secret。
- `workflow`：检查工作流资产；角色映射校验按需开启。
- `test`：运行目标项目自己的测试或 smoke check。
- `release`：生成 release dry run，用于发布前人工确认。

Fast MR 默认只跑 policy、workflow assets 和 test。上下文新鲜度只在相关
文档变化时运行；release dry run 只在 tag 或手工主分支流水线运行。

环境建议：

- `dev/review` 环境可以跟随分支或 MR 自动部署，最好是隔离环境。
- 共享 `test/staging` 环境不建议被每个 MR 自动覆盖，需要人工确认、环境锁、版本记录和回滚目标。
- 生产发布必须走发布治理，不能由 AI 或普通分支 pipeline 自动发布。

## 安全边界

- 不要提交本地 API helper、token、私有 GitLab 配置或生产数据。
- 不要把密码、密钥、客户隐私、生产日志直接放进 prompt 或仓库。
- AI 输出必须落到 GitLab 评论或仓库文档，方便追溯。
- AI 可以辅助人做决定，但不能替代责任人做决定。

更多细节见：

- `docs/quickstart.md`
- `docs/workflow.md`
- `docs/skills.md`
- `docs/cicd.md`

## 参与维护

贡献代码、Skill、模板或发布包时，请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。
