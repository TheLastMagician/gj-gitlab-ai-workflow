# GitLab 待办 API 参考

`gj-workflow-next` 需要真实 GitLab 状态时使用本参考资料。优先使用已安装的
`scripts/gitlab_api.py` helper，让 Codex、Claude Code 和 OpenCode 使用同一套受保护
API 行为。绝不输出 Token。

## 认证

安装 Skill 不需要 Token。需要真实访问时配置一次：

```powershell
python scripts/gitlab_api.py configure --url https://gitlab.example.com --project-id group/project
python scripts/gitlab_api.py doctor
```

helper 读取被忽略的 `.gj/gitlab.local.json`；CI 环境变量可以覆盖。不要打开、输出、
暂存本地配置或把它发送给 Agent。

读取个人 Todo 时使用当前用户且带 `read_api` 的 Personal Access Token。只有创建 Issue、
设置标签/负责人、发布评论等经人确认的写操作才使用 `api`。Project Access Token 代表
机器人账号，不能代替人的 Todo 待办。设置和存储规则见公开
[GitLab 访问指南](https://github.com/TheLastMagician/gj-gitlab-ai-workflow/blob/main/docs/gitlab-access.md)。

## 核心数据源

- 当前用户：`GET /user`
- 用户查询：`GET /users?username=<username>`
- Todo：`GET /todos`
- 分配给用户的项目 Issue：
  `GET /projects/:project/issues?state=opened&assignee_username=<username>`
- 分配给用户的项目 MR：
  `GET /projects/:project/merge_requests?state=opened&assignee_username=<username>`
- 需要用户审阅的项目 MR：
  `GET /projects/:project/merge_requests?state=opened&reviewer_username=<username>`
- MR 讨论：
  `GET /projects/:project/merge_requests/:iid/discussions`
- MR Pipeline：
  `GET /projects/:project/merge_requests/:iid/pipelines`
- 项目失败 Pipeline：
  `GET /projects/:project/pipelines?status=failed`
- Issue 评论：
  `GET /projects/:project/issues/:iid/notes`
- MR 评论：
  `GET /projects/:project/merge_requests/:iid/notes`

## 可选写操作

只有人要求指派、设置 Reviewer 或发布交接评论时才使用写操作。这些动作建立责任和通知
事件，不代表批准或完成工作。

- 指派 Issue：
  `PUT /projects/:project/issues/:iid` with `assignee_ids`
- 指派 MR：
  `PUT /projects/:project/merge_requests/:iid` with `assignee_ids`
- 设置 MR Reviewer：
  `PUT /projects/:project/merge_requests/:iid` with `reviewer_ids`
- 添加 Issue 评论：
  `POST /projects/:project/issues/:iid/notes`
- 添加 MR 评论：
  `POST /projects/:project/merge_requests/:iid/notes`

## Helper 命令

```powershell
python scripts/gitlab_api.py request --path "todos"
python scripts/gitlab_api.py request --path "projects/:project/issues?state=opened&assignee_username=zengqinglin"
python scripts/gitlab_api.py request --path "projects/:project/merge_requests?state=opened&reviewer_username=zengqinglin"
python scripts/gitlab_api.py request --method PUT --path "projects/:project/issues/12" --body-json '{"assignee_ids":[55]}' --confirm-write
python scripts/gitlab_api.py request --method POST --path "projects/:project/issues/12/notes" --body-json '{"body":"@zengqinglin please handle QA verification."}' --confirm-write
```

只有带 `--confirm-write`、路径使用 `:project` 且配置的 GitLab 项目与
`git remote origin` 匹配时，写操作才会成功。helper 拒绝凭据、Runner、webhook 和 CI
变量端点。

## 通知模型

GitLab 是事实源。企业微信、邮件或其他公司消息系统可以投递 GitLab 通知，但本 Skill
不读取这些渠道。某人未收到通知时，先确认 GitLab 工作项有 assignee/reviewer 和
`@username` 交接评论，再让人检查 GitLab 通知设置。
