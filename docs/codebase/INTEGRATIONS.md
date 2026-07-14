# 外部集成

## 已确认事实

- 通过安装的 `scripts/gitlab_api.py` helper 使用 GitLab REST API。
- 使用的 GitLab 对象包括标签、里程碑、Issue、评论、MR 和 Pipeline。
- 本地 URL、项目 ID 和 Token 保存在被忽略的 `.gj/gitlab.local.json`；CI 环境变量
  可以覆盖这些值。
- 示例项目不使用外部数据库、队列或第三方服务。

## 待确认

- Webhook 认证方式。
- AI 网关契约。
- CI 之外由哪个组织级秘密管理器提供 GitLab Token。
