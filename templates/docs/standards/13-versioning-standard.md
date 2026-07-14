# Git 项目版本规范

## 四类版本事实

| 名称 | 事实源 | 生命周期 |
| --- | --- | --- |
| 目标版本 | GitLab Milestone | 需求计划时确认，可在发布前调整 |
| Released version | Git Tag | 人确认发布后创建，不再修改 |
| Build identity | Tag + commit SHA + Pipeline | Tag Pipeline 构建时产生 |
| Deployed version | Environment + Tag + SHA | 部署和验证后记录 |

Git Tag 是仓库已发布版本的唯一事实源。Milestone 只是计划，环境实际版本必须记录 Tag
和 SHA。默认使用 SemVer、`v{version}` Tag、main + tags，不要求长期 release 分支。

## SemVer 选择

- Major：不兼容的接口、数据、配置或业务行为变化。
- Minor：向后兼容的新功能。
- Patch：Bug、Hotfix 或兼容性修复。
- typo、测试和内部重构通常进入下个版本，不必单独发布。

flow 表示风险和流程深度，不决定版本号。Fast 不等于 Patch，Standard 不等于 Minor。

## 阶段规则

| 阶段 | 版本动作 | 文档动作 |
| --- | --- | --- |
| 入口 | 人确认目标版本/Milestone | Requirement Issue 记录目标版本和文档链接 |
| 计划 | 版本仍是计划，可调整 | PRD、设计、方案、测试计划记录来源 Issue 和目标版本 |
| 开发/MR | 不创建 Tag，不逐 MR bump | MR 关联同一 Issue/Milestone并输出文档决策 |
| 发布准备 | 汇总 Milestone，锁定最终 SemVer | 创建版本测试报告和发布说明；按技术栈更新 manifest |
| 发布 | 人创建并推送 Tag | Tag Pipeline 校验并记录构建身份 |
| 收尾 | 记录实际部署版本 | current state 和发布说明记录 Tag/SHA/Pipeline/环境/验证 |

多个需求可以进入同一版本。版本只在发布准备时集中收口，避免多个功能 MR 修改同一个
manifest 产生冲突。

## 文档关联字段

| 文档 | 最低版本字段 |
| --- | --- |
| PRD/设计/方案/测试计划 | 来源 Issue、目标版本、直接上下游链接 |
| 测试报告 | 版本、Tag、提交、Pipeline、环境、关联 Issue/MR |
| 发布说明 | 版本、里程碑、Tag、来源提交、Pipeline、测试报告、状态 |
| 当前状态 | 最新发布 Tag、各环境已部署 Tag/SHA、最近验证时间 |

功能文档原地更新，不在文件名增加 v2/final。测试报告和发布说明使用
`docs/qa/test-reports/<tag>.md`、`docs/releases/<tag>.md`，完成后冻结。

## 配置

```yaml
versioning:
  scheme: semver
  tag_pattern: "v{version}"
  release_note_pattern: "docs/releases/{tag}.md"
```

项目已有 manifest 时，在发布准备阶段同步版本；通用工作流不强制增加 `VERSION` 文件。

## 检查与人工边界

- 普通 MR 不因版本字段被硬阻断。
- `release_dry_run.py` 在发布准备时提供提醒。
- Tag Pipeline 的 `release_version_check.py` 硬检查 Tag 格式、发布说明存在性、版本、
  Tag、状态和必要章节，避免错误版本进入构建/部署。
- 文档内容、SemVer 选择、Tag 创建、合并和部署仍由人确认。
