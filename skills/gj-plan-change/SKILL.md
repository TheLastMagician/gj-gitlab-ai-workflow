---
name: gj-plan-change
description: Plan GitLab work at the depth required by its flow label. Use when a requirement, feature, small change, bug, or hotfix needs acceptance criteria, technical approach, task boundaries, test coverage, documentation impact, rollout, or rollback before implementation.
---

# GJ 变更计划

## 工作流程

1. 读取工作项、当前标签、`.gj/context.yml` 和已知约束。涉及代码时读取
   `docs/standards/01-development-standard.md` 和 `07-test-standard.md`，再按预计路径
   加载相关 API、数据库、安全或环境标准；其余上下文只加载 `always_load`、路径匹配的
   模块和工作项直接关联的功能文档。规划需求或产品变化时读取
   `docs/standards/02-requirement-standard.md`；以 `docs/standards/12-context-governance.md`
   作为文档生命周期和内容规范。
2. 所有澄清问题和开发阻断项必须能指向工作项、已加载文档、代码或配置中的具体依据。
   不把其他业务、历史演练或通用风险清单中的角色、字段、规则和状态迁移到当前需求。
   对接口、数据、权限、迁移、外部集成等通用影响维度，先判断是否适用；没有命中依据时
   记录为“不涉及”或 `no-change`，不能列为待确认或开发阻断项。只有未知答案会实质改变
   验收、方案、安全边界或测试方法时，才列入“需要人工确认”或“满足以下条件可开发”。
3. 确定且仅确定一个 flow 标签。缺失时提出建议，但在人工确认前不视为已选择。
4. 按已选 flow 调整计划深度：
   - `flow::fast`：说明改动、非目标、受影响文件、自测和文档影响；默认不创建额外
     计划 Issue。
   - `flow::standard`：澄清验收和非目标；记录技术方案、接口/数据/权限影响、风险、
     测试、发布、回滚和可独立审阅的任务。
   - `flow::hotfix`：记录等级、影响、止血、最小安全修复、最低审阅、发布验证、回滚和
     强制跟进。
5. 根据 `.gj/workflow.yml` 匹配已变更或预计路径。最低 flow 要求更高时，把 Fast 升级为
   Standard 或 Hotfix。
6. 对将发布的工作，读取 `docs/standards/13-versioning-standard.md`，独立于 flow 规划
   目标版本。根据 SemVer 策略和兼容影响推荐 Major、Minor 或 Patch，并关联 Requirement
   Issue 和 GitLab Milestone。这是目标版本，不是已发布版本；功能计划阶段不提升项目
   manifest 或创建 Tag。
7. 只有单独负责人、依赖或审阅边界让额外 Issue 有价值时才拆分。Requirement 或 Hotfix
   是主工作项；Solution、Task 或 Test Issue 只记录需单独跟踪的工作，不能替代仓库方案、
   测试计划或其他长期文档。
8. 按风险覆盖成功、失败、权限、回归和发布验证路径。失败检查要创建 Bug Issue，不能
   藏在备注里。
9. 先按影响决定文档，再应用已选 flow 深度：
   - 语言、框架、运行时、依赖、构建命令、架构/目录边界或前后端开发约定变化时，
     更新 `01-development-standard.md`、模块地图、模块文档或 ADR；
   - 测试框架、目录、命令、覆盖或 CI 测试策略变化时更新 `07-test-standard.md`；
   - 产品行为、规则、权限或验收标准变化时创建或更新 PRD；
   - 只有交互或 UI 状态变化时才创建或更新产品设计/原型记录；
   - 架构、兼容、发布、监控或回滚需要决策时创建或更新技术方案；
   - API/事件结构或语义变化时更新机器契约和 `docs/technical/apis/<domain>.md`；
   - 持久数据结构、含义、迁移或恢复变化时更新 schema/migration 和
     `docs/technical/database/<domain>.md`；
   - 只有长期、跨边界且有取舍的技术决策才创建 ADR，确认后冻结；
   - 验收或回归覆盖不平凡时创建或更新测试计划。
   在适用功能文档中填写来源 Issue、目标版本/Milestone 和直接文档链接。新文件从
   `.gj/doc-templates/` 创建并使用语义文件名，事实目录不能保留模板名。已有能力或领域
   文档原地更新，不创建版本副本。长期事实未确认时保持 `draft`；经过对应人工门后记录
   确认人并改为 `confirmed`，该状态不代表已部署。每个 API 或数据库决策都要在计划和
   文档决策中同时写出可执行路径及说明 Markdown 路径；未知路径要写具体 `TBD` 和负责
   人。没有定位两种事实时，“更新 schema”不是完整文档动作。
10. 起草或发布 Issue、MR、评论、讨论或交接消息前读取
    `docs/standards/11-notification-standard.md`。以文档决策表结尾，包含路径、动作、触发
    事实、阶段/状态和确认人/跟进项。动作只能是
    `create`、`update`、`no-change` 或 `follow-up`；`follow-up` 需要 Issue、负责人和
    期限。默认不另建文档任务。

## 输出格式

```markdown
## 变更计划

Flow 和原因：
目标版本/Milestone 及 SemVer 原因：
目标和非目标：
验收标准：
技术方案：
影响和风险：
任务和依赖：
测试覆盖：
文档影响：
文档决策（路径/动作/触发事实/阶段和状态/确认人或跟进项）：
发布和回滚：
需要人工确认：
满足以下条件可开发：
```
