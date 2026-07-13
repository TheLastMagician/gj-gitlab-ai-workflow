# Current State

## 项目定位

`gj-workflow-demo` 当前用于验证 GitLab AI 项目交付工作流，并沉淀未来开源项目
`gj-gitlab-ai-workflow` 的模板、脚本、示例和 skill 草案。

## 当前事实

- 当前示例迭代是 `订单审批流 v1.0`。
- GitLab project 已通过只读 API 校验为 `zengqinglin/gj-workflow-demo`。
- 跨 Agent GitLab helper 位于 `scripts/gitlab_api.py`;本地凭据保存在被忽略的
  `.ai/gitlab.local.json`。
- 首轮目标是暴露摩擦点，不追求一次性写完全部 skills。
- 当前工作流使用唯一 `flow::*` 标签和 changed files 判断最低流程。
- 默认项目按低风险处理，不要求额外审批人数。
- GitLab CE 的硬门禁依赖成功 Pipeline、保护分支和受限合并权限。
- 对外 Skill 接口已收敛为 8 个，按 flow 标签控制计划和交付深度，
  Codex、Claude Code、OpenCode 共用同一份 `SKILL.md` 源码。
- demo 已用项目本地配置完成 GitLab helper 验证:读取 Issue、MR、Pipeline,
  写入并回读 Issue 评论,缺少写入确认和敏感端点访问均被拒绝。

## 人工确认点

- GitLab protected branch、merge checks、discussion resolved 规则需要在 UI 或管理员 API 中确认。
- GitLab 成员用户名和真实 owner 列表需要项目负责人确认。
- GitLab API 默认使用项目本地 `.ai/gitlab.local.json`;CI 可用环境变量覆盖。
  Token 类型、scope 和组织级密钥存储方式仍需项目负责人确认。
