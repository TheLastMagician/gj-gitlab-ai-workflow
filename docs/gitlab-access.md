# GitLab 访问配置

## 什么时候需要认证

安装和加载 GJ Skills 不需要 GitLab Token。只有读取或写入真实 GitLab 状态时需要
认证，例如 Todo、Issue、MR、讨论、Pipeline、成员校验、标签、处理人和评论。

Skill 本身不保存凭据，也不绑定某一种 Agent。连接方式按优先级选择：

1. 使用 Codex、Claude Code 或 OpenCode 已配置的 GitLab MCP/连接器。
2. 使用团队批准的 GitLab CLI 或 API helper，并从环境变量读取凭据。
3. 没有 GitLab 连接时，Skill 只输出 Issue、MR 或评论草稿，由人手工提交。

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

Personal Access Token 通常在 GitLab 用户设置的 Access Tokens 页面创建。需要填写
名称、到期时间并选择 scope。Project Access Token 通常在目标项目 Settings 的
Access Tokens 页面创建，同时选择最低可用角色。不同 GitLab CE 版本的菜单名称可能
略有不同；如果项目页面没有 Project Access Token，就使用专用的低权限机器人用户。

Token 只在创建时显示一次。立即存入密码管理器或组织密钥管理系统，不要粘贴到聊天、
Issue、MR、源码或文档。

## 本地 PowerShell 会话

当前仓库约定以下环境变量：

```powershell
$env:GITLAB_URL = "https://gitlab.example.com"
$env:GITLAB_PROJECT_ID = "group/project"
$secureToken = Read-Host "GitLab Access Token" -AsSecureString
$env:GITLAB_TOKEN = [System.Net.NetworkCredential]::new("", $secureToken).Password
```

这些变量只对当前 PowerShell 进程及其子进程有效。应从同一个终端启动 Agent，确保
Agent 或 API helper 能继承变量。不要使用会把 Token 明文写入 shell 历史的赋值命令。

如果使用 GitLab MCP/连接器，它可能使用自己的凭据存储，不一定读取
`GITLAB_TOKEN`；以该连接器的认证文档为准。

## 验证配置

安装工作流资产并填写 `.ai/role-map.yml` 后，可以验证 Token、项目和成员映射：

```powershell
python scripts/validate_role_map.py --strict-gitlab
```

脚本读取 `GITLAB_URL`、`GITLAB_PROJECT_ID` 和 `GITLAB_TOKEN`，不会输出 Token。
在任何写操作前，还必须确认 GitLab API 返回的项目 path 与 `git remote get-url origin`
指向同一项目。

## CI/CD 变量

在 GitLab 项目 Settings -> CI/CD -> Variables 中配置需要的变量：

- `GITLAB_URL`
- `GITLAB_PROJECT_ID`
- `GITLAB_TOKEN`

Token 变量应启用 masked；只允许受保护分支或 Tag 使用时同时启用 protected。不要把
Token 直接写入 `.gitlab-ci.yml`。Fork 或不可信 MR Pipeline 默认不应获得写权限 Token。

## 写操作边界

即使配置了 `api` scope，AI 也不能自主 approve、merge、deploy 或扩大任务范围。
创建 Issue、修改标签和处理人、发表评论等写操作需要人在当前任务中明确确认。Token
只提供技术权限，不代表人的业务授权。
