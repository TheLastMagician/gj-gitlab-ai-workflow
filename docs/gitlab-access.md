# GitLab 访问配置

## 什么时候需要认证

安装和加载 GJ Skills 不需要 GitLab Token。读取或写入真实 GitLab 状态时才需要认证，
例如 Todo、Issue、MR、讨论、Pipeline、成员校验、标签、处理人和评论。

工作流默认安装 `scripts/gitlab_api.py`。Codex、Claude Code 和 OpenCode 都通过这个
脚本使用相同的项目配置、端点白名单和写入保护。已有 GitLab MCP/连接器可以作为可选
替代；没有任何连接能力时，Skill 只输出草稿，由人手工提交。

## Token 类型和最小权限

| 使用场景 | 推荐 Token | Scope | 说明 |
| --- | --- | --- | --- |
| 读取自己的 Todo 和待办 | 当前用户 Personal Access Token | `read_api` | Todo 属于当前用户，项目机器人不能替代 |
| 读取项目 Issue、MR、Pipeline 和成员 | Personal 或 Project Access Token | `read_api` | Project Token 适合共享的只读自动化 |
| 创建 Issue、设置标签/处理人、发表评论 | Personal 或独立 Project Access Token | `api` | 仅在人明确确认写操作后使用 |
| CI 或长期服务 | 独立 Project Access Token | `read_api` 或必要时 `api` | 设置短有效期、最低角色并定期轮换 |

GitLab 的 `api` 是宽权限 scope。只读流程不要为了方便直接授予 `api`。不要授予
`sudo`、管理员权限或不需要的 `write_repository`。

## 创建 Token

Personal Access Token 通常在 GitLab 用户设置的 Access Tokens 页面创建。填写名称、
到期时间并选择 scope。Project Access Token 通常在项目 Settings 的 Access Tokens
页面创建，同时选择最低可用角色。不同 GitLab CE 版本的菜单名称可能略有不同；如果
项目没有 Project Access Token，就使用专用的低权限机器人用户。

Token 只在创建时显示一次。存入密码管理器或组织密钥管理系统，不要粘贴到聊天、
Issue、MR、源码或文档。

## 项目本地配置

在业务项目根目录运行：

```powershell
python scripts/gitlab_api.py configure --url https://gitlab.example.com --project-id group/project
```

命令通过隐藏输入读取 Token，并写入 `.gj/gitlab.local.json`：

- 配置一次后，项目中的 Codex、Claude Code 和 OpenCode 可以共同使用。
- `scripts/install_workflow.py` 和 `configure` 都会把该文件加入 `.gitignore`。
- 文件权限会尽量限制为当前用户读写。
- 配置文件仍含明文 Token，只适合受控开发机；不要打开给 Agent、提交、复制或同步。
- 更换 URL、项目或 Token 时重新执行并增加 `--force`。

项目 ID 可以使用数字 ID，也可以使用 `group/project` 路径。环境变量
`GITLAB_URL`、`GITLAB_PROJECT_ID`、`GITLAB_TOKEN` 会覆盖本地文件，主要供 CI、
容器或临时运行使用，本地日常操作不需要反复配置环境变量。

## 验证连接

```powershell
python scripts/gitlab_api.py doctor
python scripts/validate_role_map.py --strict-gitlab
```

`doctor` 验证 Token、当前用户和项目，并比较 GitLab API 返回的项目地址与
`git remote get-url origin`。输出不会包含 Token。远端不一致时，所有 helper 写操作
都会失败。

常用只读命令：

```powershell
python scripts/gitlab_api.py request --path "user"
python scripts/gitlab_api.py request --path "todos"
python scripts/gitlab_api.py request --path "projects/:project/issues?state=opened"
python scripts/gitlab_api.py request --path "projects/:project/merge_requests?state=opened"
python scripts/gitlab_api.py request --path "projects/:project/pipelines?status=failed"
```

`:project` 会替换成配置中的项目 ID，并进行 URL 编码。

## 受控写操作

写操作必须同时满足：

1. 人在当前任务中明确确认具体写入内容。
2. 命令包含 `--confirm-write`。
3. API path 使用 `:project` 或 `{project}`，不能手写另一个项目 ID。
4. 配置项目与 `git remote origin` 一致。
5. 端点属于 Issue、MR、评论、标签或 Milestone 白名单。

示例：

```powershell
python scripts/gitlab_api.py request --method POST --path "projects/:project/issues/16/notes" --body-json '{"body":"Workflow API verification passed."}' --confirm-write
```

helper 拒绝 Access Token、CI/CD Variables、Runner、Webhook 等敏感管理端点，也不提供
approve、merge、repository file 或 deploy 操作。

## CI/CD 变量

在 GitLab 项目 Settings -> CI/CD -> Variables 中配置：

- `GITLAB_URL`
- `GITLAB_PROJECT_ID`
- `GITLAB_TOKEN`

Token 变量启用 masked；只允许受保护分支或 Tag 使用时同时启用 protected。不要把
Token 写入 `.gitlab-ci.yml`。Fork 或不可信 MR Pipeline 默认不应获得写权限 Token。

## 写操作边界

即使配置了 `api` scope，AI 也不能自主 approve、merge、deploy 或扩大任务范围。
Token 只提供技术权限，不代表人的业务授权。
