# 快速开始

## 1. 安装 Skills

在目标项目根目录运行以下命令，为 Codex、Claude Code 和 OpenCode 安装同一份 Skill：

```powershell
npx --yes skills@1.5.17 add https://github.com/TheLastMagician/gj-gitlab-ai-workflow --skill '*' -a codex -a claude-code -a opencode --copy -y
```

安装器为 Codex 和 OpenCode 写入项目内 `.agents/skills`，为 Claude Code 写入
`.claude/skills`。安装后重新打开 Agent 会话。

粘贴 GitHub URL 不会自动执行代码。请明确运行命令，或要求当前 Agent 执行安装。没有
Node.js 时，先克隆本仓库，再使用 Python 兜底安装器：

```powershell
python scripts/install_skills.py --agent all --project-root C:\path\to\your-project --force
```

只有需要自定义单一 Skill 目录时才使用 `--dest`。

完整 Skill 清单和流程映射见 `docs/skills.md`。

## 2. 初始化仓库资产

让新安装的 bootstrap Skill 初始化当前仓库：

```text
使用 gj-workflow-bootstrap 初始化当前项目。
```

Skill 自带的 GitHub 引导脚本会获取本仓库源码包，并运行同一个非破坏式资产安装器。在
本仓库源码目录中，等价命令是：

```powershell
python scripts/install_workflow.py --target C:\path\to\your-project
```

安装器递归补齐缺失文件，绝不会删除目标目录。`--force` 只替换已知冲突文件并自动备份。
已有复杂 GitLab CI include 时保持原样，并输出需要人工执行的准确操作。

安装后的最低配置包括：

- `.gj/workflow.yml`
- `.gj/context.yml`
- `.gitlab/gj-workflow-ci.yml` included by `.gitlab-ci.yml`
- `GJ_TEST_COMMAND` configured for the real project test command

更新 `.gj/workflow.yml`、`.gj/context.yml` 和 `CODEOWNERS`。只有对应能力或领域存在时，
才从 `.gj/doc-templates/` 创建长期文档，并写入使用语义名的项目路径。

已有代码项目随后运行：

```text
使用 gj-codebase-map 扫描当前项目并起草工程规范和模块上下文。
```

它直接更新 `docs/standards/01-development-standard.md`、`07-test-standard.md`、
`docs/context/`、`docs/modules/` 和 `.gj/context.yml` 草稿，并把可执行风险整理成 GitLab
Issue 草稿；不会创建中间扫描报告。Dev Lead、QA 和模块负责人确认后这些内容才生效。

保持 AI 上下文精简：`always_load` 最多包含三个小型当前事实文件，模块文档只在路径匹配
时加载。职责拆分和加载模型见 `docs/documentation-governance.md`。

尽早决定 MR 分支只部署到隔离的开发/评审环境，还是允许人手工部署到共享测试环境。不要
让每个 MR 分支自动覆盖同一个共享测试环境。

GitLab Issue/MR 保存讨论轨迹，仓库文档保存长期事实。每个需求或 MR 都要回答文档影响：
更新产品、设计、方案、API、数据库、ADR、模块、测试、发布或上下文文档，或者说明相关
类别为什么不需要更新。

## 3. 配置 GitLab

安装 Skill 和离线规划不需要 Token。需要访问真实 GitLab 时，在目标项目中配置一次跨
Agent helper：

```powershell
python scripts/gitlab_api.py configure --url https://gitlab.example.com --project-id group/project
python scripts/gitlab_api.py doctor
```

隐藏输入会把 Token 写入被忽略的 `.gj/gitlab.local.json`。只读访问使用 `read_api`；只有
确认需要写操作时才授予 `api`。CI 可以用 `GITLAB_URL`、`GITLAB_PROJECT_ID` 和
`GITLAB_TOKEN` 覆盖本地配置。命令和安全规则见 `docs/gitlab-access.md`。

按照 `examples/demo-run/gitlab/labels.md` 创建流程标签，再为第一轮迭代创建 Milestone。
保护默认分支，并要求 Pipeline 成功后才能合并。

GitLab CE 还要限制谁可以合并到默认分支。低风险 Fast MR 不要求额外审批人数。
CODEOWNERS 和可选 Approve 动作可以辅助审阅，但工作流不依赖付费版审批规则。

实现前，在 Issue 或工作项上确认唯一流程标签。创建 MR 时，在 GitLab 中选择同一个
`flow::fast`、`flow::standard` 或 `flow::hotfix` 标签。policy Job 会拒绝标签缺失或冲突。

需要角色路由时，把 `.gj/workflow.yml` 中的占位符替换为真实 GitLab 用户名。每次人工
交接都要设置 Issue/MR 负责人或 Reviewer，并添加 `@username` 评论。
`gj-workflow-next` 直接读取 GitLab API 状态；企业微信或邮件应配置为 GitLab 通知渠道，
不要另建流程待办源。

编辑 `.gj/workflow.yml` 后校验角色归属：

```powershell
python scripts/validate_role_map.py
```

需要检查真实 GitLab 成员时，复用本地配置：

```powershell
python scripts/validate_role_map.py --strict-gitlab
```

## 4. 演练示例流程

使用 `gj-workflow-demo` 这类小型目标项目完整运行一次工作流：

```text
产品经理 -> Tech Lead -> 开发 -> Reviewer -> QA -> DevOps -> PM
```

记录的输入、输出、失败和人工确认见 `examples/demo-run/00-run-log.md`。

## 5. 校验已安装的目标项目

安装后运行作为 CI 硬门禁的项目测试：

```powershell
python scripts/smoke_check.py
```

使用对应能力时，再运行工作流、角色、上下文和发布审计：

```powershell
python scripts/workflow_assets_check.py
python scripts/validate_role_map.py
python scripts/context_freshness_check.py
python scripts/release_dry_run.py --output build/release-dry-run.md
# docs/releases/v1.3.0.md 准备完成后：
python scripts/release_version_check.py --tag v1.3.0
```

## 6. 在目标项目运行 CI/CD

安装器会添加 `.gitlab/gj-workflow-ci.yml`，并从根 Pipeline 引用它。每个 GJ 硬门禁 Job
明确进入 MR Pipeline，并使用自己的 Python 镜像，因此不会替换业务项目的镜像、stage
或 `before_script`。已有复杂 `include` 块时，按安装器输出的准确操作手工加入。

使用 Docker executor 配置 GitLab Runner。策略和项目测试是 MR 硬门禁；发布版本一致性
只在 Tag Pipeline 中硬检查。其他阶段仍可能出现提醒 Job：

```text
MR 硬门禁：policy -> test
Tag 硬门禁：release version -> test
提醒：workflow assets / release dry run
```

Job 细节和产物见 `docs/cicd.md`。

模板 helper 脚本默认使用 `python:3.12-slim`。非 Python 项目可以把 GitLab CI 变量
`GJ_CI_IMAGE` 设置为同时包含 Python 和真实测试工具链的项目镜像，再设置
`GJ_TEST_COMMAND`。
