# Current State

## 项目定位

本项目使用 GitLab Issue、Merge Request、Pipeline 和仓库文档承载 AI 辅助交付流程。

## 当前事实

- GitLab 是需求、方案、任务、MR、测试、发布和复盘的事实源。
- AI 输出必须写回 GitLab 评论或仓库文档。
- 高风险 changed files 不能使用 `flow::fast`;最终合并由成功 Pipeline、
  受保护分支和受限合并权限控制。

## 版本状态

| 项目 | Tag / SHA | 状态 | 最近验证 |
| --- | --- | --- | --- |
| 目标版本 / Milestone | 待确认 | planned | |
| 最新仓库发布版本 | 尚未发布 | no-tag | |
| production 部署版本 | 待确认 | unknown | |

目标版本是计划，Git Tag 才是仓库已发布版本；环境版本必须同时记录 Tag 和 commit SHA。

## 待人工确认

- 真实 GitLab 项目 ID、默认分支和 owner 列表。
- 受保护分支、合并规则和 Pipeline 必须成功策略是否已开启。
