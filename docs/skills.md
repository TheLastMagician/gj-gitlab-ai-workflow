# 工作流 Skills

使用同一个 GitHub 源把完整工作流 Skill 安装到 Codex、Claude Code 和 OpenCode：

```powershell
npx --yes skills@1.5.17 add https://github.com/TheLastMagician/gj-gitlab-ai-workflow --skill '*' -a codex -a claude-code -a opencode --copy -y
```

所有 Agent 使用同一份 `skills/*/SKILL.md`。Python 兜底命令是
`python scripts/install_skills.py --agent all --project-root <project> --force`。
所有 Skill 使用 `gj-` 命名空间；GJ 是“公交”的项目缩写。

日常工作从 `gj-workflow-next` 开始，用户不需要记住其他 Skill 名。

## 八个 Skill

| 阶段 | Skill | 作用 |
| --- | --- | --- |
| 初始化 | `gj-workflow-bootstrap` | 安装并校验标签、模板、AI 配置、文档、CI 和项目门禁。 |
| 现有项目建图 | `gj-codebase-map` | 根据代码起草工程规范、精简上下文、模块文档和风险 Issue。 |
| 分流 | `gj-workflow-next` | 读取待办/当前状态，推荐唯一 flow 标签并选择下一步。 |
| 计划 | `gj-plan-change` | 按 flow 深度准备需求、方案、任务边界、测试、文档、发布和回滚。 |
| 开发 | `gj-develop-change` | 使用聚焦上下文和测试实现功能、小改动、缺陷和紧急修复。 |
| 审阅 | `gj-mr-review` | 审阅策略、代码、测试、文档和合并就绪度，停在人工合并门。 |
| 发布准备 | `gj-release-readiness` | 准备环境和发布证据、发布、回滚与验证，停在人工发布门。 |
| 收尾 | `gj-close-loop` | 工作完成后沉淀经验并刷新长期项目上下文。 |

## Flow 深度

| Flow | 计划和交付深度 |
| --- | --- |
| `flow::fast` | 有边界的改动、自测、文档影响、MR 和审阅；默认不额外创建计划 Issue。 |
| `flow::standard` | 关联 Issue、验收标准、技术方案、风险、测试、发布、回滚和长期文档。 |
| `flow::hotfix` | 故障影响、最小安全修复、最低审阅、发布验证、回滚和强制跟进。 |

Issue 模板提出 flow，人编码前确认，MR 沿用同一个唯一 `flow::*` 标签，CI 根据变更路径
校验选择。Skill 推荐并执行已选深度，不代替人判断业务风险。

## 评论命令

可选 Orchestrator 只暴露以下命令：

```text
/ai-next
/ai-plan
/ai-develop
/ai-review
/ai-release
/ai-close
```

`gj-workflow-bootstrap` 和 `gj-codebase-map` 按需直接调用。

## 决策边界

AI 可以检查、起草、编辑、测试和准备决策证据。AI 不得自主批准、合并、创建 Tag、部署、
覆盖共享环境或绕过保护。人确认 flow 标签并作出合并和发布决定。

## 待办和通知

`gj-workflow-next` 使用 GitLab API 状态作为待办源：Todo、分配的 Issue/MR、审阅请求、
提及、未解决讨论和失败 Pipeline。邮件或企业微信可以投递通知，但不是流程状态源。

交接时应在 GitLab 指派负责人，并在评论中提及对方，让 GitLab 创建预期 Todo 和通知。

## 文档影响

每个交付 Skill 都输出文档决策表，包含目标路径、`create` / `update` / `no-change` /
`follow-up` 动作、触发事实、阶段/状态和人工确认人或跟进项。`follow-up` 只有包含 Issue、
负责人和期限时才有效。GitLab Issue 和 MR 评论保存过程，仓库文档保存长期结论。

用户不需要另行调用文档 Skill。长期事实确认后，`gj-plan-change`、`gj-develop-change`、
`gj-release-readiness` 和 `gj-close-loop` 在仓库可写时于当前变更中更新对应文档；
`gj-mr-review` 检查更新是否存在。事实未确认或仓库不可写时，Skill 返回准确草稿和人工
确认项。当前事实文档原地更新；测试/发布证据按 Tag 新建后冻结。过程历史留在 GitLab
和 Git。

| 长期变化 | 文档目标 |
| --- | --- |
| 技术栈、构建工具、架构/目录边界、前后端开发约定 | `docs/standards/01-development-standard.md`、模块地图/文档、ADR |
| 测试框架、目录、命令、覆盖和 CI 测试策略 | `docs/standards/07-test-standard.md` |
| 产品行为或验收标准 | `docs/product/requirements/<capability>.md` |
| UI、用户流程、页面状态、文案、原型 | `docs/product/designs/<capability>.md`、`docs/product/prototypes/<capability>.md` |
| 架构、权限、发布、回滚 | `docs/technical/solutions/<capability>.md`、ADR |
| API/事件契约 | 机器 schema + `docs/technical/apis/<domain>.md` |
| 数据库结构或含义 | schema/migration + `docs/technical/database/<domain>.md` |
| 验收、回归和权限基线 | `docs/qa/test-plans/<capability>.md` |
| 已执行发布验证 | `docs/qa/test-reports/<tag>.md` |
| 用户可见发布范围或回滚 | `docs/releases/<tag>.md` |
| 长期 AI 上下文 | `docs/context`、`docs/modules`、ADR、`.gj/context.yml` |

`gj-codebase-map` 不保存 `docs/codebase/` 中间扫描报告。扫描到的现有习惯先作为待确认
草稿路由到上述长期文档；Dev Lead/QA 确认后才成为后续计划、开发和 Review 的规范。

Requirement 或 Hotfix 是主工作项。Solution、Task 和 Test Issue 只为需要单独负责或跟踪
的工作创建，绝不替代仓库文档。新文档模板安装在 `.gj/doc-templates/`；项目事实目录只
包含 `member-export.md` 这类语义文件，不保留通用模板文件名。API 和数据库决策同时
写明可执行 contract/schema/migration 路径与解释性 Markdown 路径，便于一起审阅。

## 版本职责

- `gj-workflow-next` 独立于 flow 推荐目标版本/GitLab Milestone，由人分别确认。
- `gj-plan-change` 把 Issue 和功能文档关联到该目标。
- `gj-develop-change` 和普通 MR 不提升仓库版本。
- `gj-release-readiness` 锁定最终 SemVer，准备按 Tag 保存的测试/发布证据，并在人工决定
  Tag 前检查。
- `gj-close-loop` 记录实际 Tag、SHA、Pipeline、环境和部署验证。Milestone 不能描述为
  已发布。

详见 `docs/versioning.md` 和安装后的 `docs/standards/13-versioning-standard.md`。
