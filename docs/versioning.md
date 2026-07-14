# Git 项目版本治理

## 版本事实分四层

| 名称 | 示例 | 事实源 | 何时确定 |
| --- | --- | --- | --- |
| 目标版本 | `v1.3.0` | GitLab Milestone | 需求计划时由人确认，可调整 |
| 发布版本 | `v1.3.0` | Git Tag | 发布决定后由人创建，不再修改 |
| 构建身份 | `v1.3.0 + abc1234 + Pipeline 20080` | Tag Pipeline | 构建时自动产生 |
| 部署版本 | production=`v1.3.0/abc1234` | GitLab Deployment + current state | 部署和验证后记录 |

Git Tag 是“仓库已经发布哪个版本”的唯一事实源。Milestone 只是计划，不能写成已发布；
环境里实际运行什么版本必须同时记录 Tag 和 commit SHA。

## 默认策略

工作流默认使用 SemVer 和 `v{version}` Tag：

- Major：不兼容的接口、数据、配置或业务行为变化。
- Minor：向后兼容的新功能。
- Patch：Bug、Hotfix 或兼容性修复。
- typo、测试、内部重构不一定单独发布，通常进入下一个版本。

`flow::*` 表示交付风险和流程深度，不决定版本号。Fast 不等于 Patch，Standard 也不
等于 Minor。项目默认使用 main + tags，不要求长期 release 分支。

## 一个需求如何进入新版本

假设当前生产为 `v1.2.3`，新功能计划进入 `v1.3.0`：

1. `gj-workflow-next` 推荐 flow；人确认目标 Milestone `v1.3.0`。
2. Requirement Issue 设置 Milestone，并链接 PRD、方案和测试计划。
3. `gj-plan-change` 把 `目标版本：v1.3.0` 写入功能文档。
4. `gj-develop-change` 在 MR 关联同一 Issue/Milestone；普通功能 MR 不 bump 版本。
5. `gj-release-readiness` 汇总该 Milestone 的 Issues/MRs，锁定最终 SemVer，创建
   `docs/qa/test-reports/v1.3.0.md` 和 `docs/releases/v1.3.0.md`。
6. 人合并发布准备变更并创建 Tag `v1.3.0`。
7. Tag Pipeline 校验 Tag/发布说明，构建产物记录 Tag + SHA + Pipeline。
8. 人部署后，`gj-close-loop` 把实际发布和部署版本回写 current state 和发布说明。

多个需求可以进入同一 Milestone/版本。只有发布准备阶段才更新项目已有的 manifest
版本字段；不要让每个功能 MR 争抢 `package.json`、`pyproject.toml` 或 `pom.xml`。

## 文档关联

| 载体 | 必须关联 |
| --- | --- |
| Requirement Issue | flow、目标版本、GitLab Milestone、仓库文档链接 |
| PRD/设计/方案/测试计划 | 来源 Issue、目标版本、直接上下游文档 |
| MR | Issue、Milestone、文档决策；默认不修改版本 |
| 测试报告 | 版本、Tag、提交、Pipeline、环境、关联 Issue/MR、证据 |
| 发布说明 | 版本、里程碑、Tag、来源提交、Pipeline、测试报告、包含项、回滚 |
| current state | 最新仓库发布版本和各环境实际部署的 Tag/SHA |

功能文档按语义命名并原地更新，例如 `member-export.md`；不要为版本复制 PRD、
方案或模块文档。只有测试报告和发布说明按版本新增并在完成后冻结。

## 配置与检查

`.gj/workflow.yml` 声明通用策略：

```yaml
versioning:
  scheme: semver
  tag_pattern: "v{version}"
  release_note_pattern: "docs/releases/{tag}.md"
```

普通 MR 不运行版本硬门禁。Tag Pipeline 执行 `release_version_check.py`，只硬检查：

- Tag 符合配置的 SemVer 格式；
- 对应发布说明存在；
- 发布说明的“版本”和 `Tag` 与实际 Tag 一致，状态为 `ready` 或 `released`；
- 包含项、验证和回滚章节存在。

manifest 是否需要同步由项目技术栈决定，并在发布准备时由 Skill 和人确认；通用工作流
不强制所有仓库增加 `VERSION` 文件。Tag 创建、推送和部署始终是人的决定。
