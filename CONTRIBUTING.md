# 参与维护

本文只面向修改 `gj-gitlab-ai-workflow` 源码、Skills、模板或发布包的贡献者。
安装和使用工作流请从 `README.md` 和 `docs/quickstart.md` 开始。

## 修改原则

- 用户入口文档只写安装、配置、使用和排错；维护细节留在本文。
- `skills/` 是公开 Skill 源码，`templates/` 是安装到业务项目的工作流资产。
- 源码仓库不保留安装后的 `.gj/`、`.gitlab/`、`.gitlab-ci.yml` 或
  `docs/context/` 实例；需要验证安装结果时使用临时 Git 仓库。
- 修改脚本或规则时同步检查对应模板，避免源码与安装结果不一致。
- 不提交 Token、`.gj/gitlab.local.json`、私有 GitLab 地址、生产日志或客户数据。
- 工作流策略、安装 CI、模板和标准文档属于高风险路径，使用
  `flow::standard` 或 `flow::hotfix`。

## 本仓库工程约定

- 面向人的工作流文档使用中文；路径、Skill 名和机器枚举可保留英文。
- 代码和配置路径优先使用小写连字符，Skill 目录固定使用小写连字符。
- Python 脚本优先使用标准库，保持安装器、检查脚本和示例的可移植性。
- 本地命令示例优先提供 PowerShell；安装资产使用 GitLab CI，业务项目测试由项目自己提供。
- 提交信息使用中文并遵循 Angular 规范：`<type>(<scope>): <subject>`。
- 新增依赖、改变安装资产、CI 门禁或跨 Agent 契约时，必须同步源码、模板和测试。

## 本地校验

提交 MR 前运行：

```powershell
python -m unittest discover -s tests
python templates/scripts/policy_check.py --mr-description examples/demo-run/mr/merge-request.md --changed-files examples/demo-run/mr/changed-files.txt --labels flow::standard
python templates/scripts/validate_role_map.py --workflow-config templates/gj/workflow.yml --allow-placeholders
python scripts/verify_order_demo.py
python scripts/validate_skills.py
python scripts/install_skills.py --dry-run
python scripts/install_workflow.py --target C:\path\to\temporary-project --dry-run
```

涉及安装行为时，还应在临时项目中实际安装一次，确认 Codex/OpenCode 的
`.agents/skills` 和 Claude Code 的 `.claude/skills` 都能发现 8 个 Skill。

## 修改 Skills

当前公开接口固定为：

- `gj-workflow-bootstrap`
- `gj-codebase-map`
- `gj-workflow-next`
- `gj-plan-change`
- `gj-develop-change`
- `gj-mr-review`
- `gj-release-readiness`
- `gj-close-loop`

优先向现有 Skill 的 `references/` 增加细节。只有新能力具有独立触发条件、工作流和
输出，且不能作为现有 Skill 的一种模式时，才考虑新增 Skill。

修改 `SKILL.md` 时同步检查 `agents/openai.yaml` 的展示名称、简介和默认提示，并运行
`python scripts/validate_skills.py`。面向 Agent 的详细 API、策略和示例放入
`references/`，避免让 `SKILL.md` 膨胀。

## 修改安装资产

`scripts/install_workflow.py` 从 `templates/` 安装业务项目资产。修改以下任一内容时，
检查源码、模板和测试是否需要同步：

- `templates/gj/*.yml`
- `templates/gitlab/.gitlab-ci.yml` 与 `templates/gitlab/.gitlab/`
- `templates/scripts/`、`templates/orchestrator/` 与 `templates/CODEOWNERS`
- 面向使用者的 `docs/*.md` 与安装到目标项目的 `templates/docs/`

`templates/` 是安装资产的唯一源。不要为了演示或测试，把安装结果复制回源码根目录；
安装器行为由 `tests/` 创建临时 Git 仓库验证。

安装器必须逐文件处理，禁止删除目标目录。`--force` 只能替换已知冲突文件并自动备份。

## 构建发布包

```powershell
python scripts/package_open_source.py --output dist\gj-gitlab-ai-workflow.zip
python scripts/validate_release_package.py --package dist\gj-gitlab-ai-workflow.zip --output build\release-package-validation.md
```

发布干跑必须通过。发布前还要人工确认许可证、公开 URL、GitLab Runner 说明、保护
分支设置以及发布 ZIP 中不存在凭据或私有数据。

## 人工边界

测试、校验、打包可以自动执行；approve、merge、创建 Tag 和发布必须由有权限的人
明确决定并执行。
