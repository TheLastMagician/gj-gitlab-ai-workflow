# Current State

## 项目定位

`gj-workflow-demo` 当前用于验证 GitLab AI 项目交付工作流，并沉淀未来开源项目
`gj-gitlab-ai-workflow` 的模板、脚本、示例和 skill 草案。

## 当前事实

- 当前示例迭代是 `订单审批流 v1.0`。
- GitLab project 已通过只读 API 校验为 `zengqinglin/gj-workflow-demo`。
- 本地 API helper 被视为私密文件，不进入提交。
- 首轮目标是暴露摩擦点，不追求一次性写完全部 skills。

## 人工确认点

- GitLab protected branch、merge checks、discussion resolved 规则需要在 UI 或管理员 API 中确认。
- GitLab 成员用户名和真实 owner 列表需要项目负责人确认。
- API token 管理方式需要迁移到环境变量或密钥管理。
