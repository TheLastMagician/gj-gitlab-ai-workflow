# 已创建的 GitLab 标签

## 类型

- `type-project`
- `type-requirement`
- `type-solution`
- `type-task`
- `type-bug`
- `type-hotfix`
- `type-test`
- `type-release`
- `type-retro`

## 状态

- `status-需求池`
- `status-需求待分析`
- `status-需求待确认`
- `status-需求已确认`
- `status-方案设计中`
- `status-方案待评审`
- `status-方案已确认`
- `status-待开发`
- `status-开发中`
- `status-待CodeReview`
- `status-测试中`
- `status-待发布`
- `status-已发布`
- `status-已关闭`
- `status-阻塞`

## 工作流通道

- `flow::fast`
- `flow::standard`
- `flow::hotfix`

## 优先级/风险/AI

- `priority-P1`
- `priority-P2`
- `priority-P3`
- `risk-permission`
- `risk-devops`
- `ai-待分析`
- `ai-已分析`
- `ai-需人工确认`

## 阻碍

The first API helper configuration pointed at a project that did not match
`git remote -v`. The safe bootstrap action is to call `GET /projects/:project`
and compare `path_with_namespace` to the remote URL before creating labels.
