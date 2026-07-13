# 参与维护

本文只面向修改 `gj-gitlab-ai-workflow` 源码、Skills、模板或发布包的贡献者。
安装和使用工作流请从 `README.md` 和 `docs/quickstart.md` 开始。

## 修改原则

- 用户入口文档只写安装、配置、使用和排错；维护细节留在本文。
- `skills/` 是公开 Skill 源码，`templates/` 是安装到业务项目的工作流资产。
- 修改脚本或规则时同步检查对应模板，避免源码与安装结果不一致。
- 不提交 Token、本地 API helper、私有 GitLab 地址、生产日志或客户数据。
- 工作流策略、`.ai/`、CI、模板和标准文档属于高风险路径，使用
  `flow::standard` 或 `flow::hotfix`。

## 本地校验

提交 MR 前运行：

```powershell
python -m unittest discover -s tests
python scripts/policy_check.py --mr-description examples/demo-run/mr/merge-request.md --changed-files examples/demo-run/mr/changed-files.txt --labels flow::standard
python scripts/validate_role_map.py --role-map templates/ai/role-map.yml --allow-placeholders
python scripts/validate_skills.py
python scripts/install_skills.py --dry-run
python scripts/install_workflow.py --target C:\path\to\temporary-project --dry-run --only-missing
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

- `.ai/*.yml` 与 `templates/ai/*.yml`
- `.gitlab-ci.yml` 与 `templates/gitlab/.gitlab-ci.yml`
- `.gitlab/` 与 `templates/gitlab/.gitlab/`
- `scripts/` 与 `templates/scripts/`
- 长效文档和 `templates/docs/`

对已有项目默认使用 `--only-missing`；只有明确验证备份和覆盖行为时才使用
`--force --backup`。

## 构建发布包

```powershell
python scripts/package_open_source.py --output dist\gj-gitlab-ai-workflow.zip
python scripts/release_dry_run.py --package dist\gj-gitlab-ai-workflow.zip --output build\release-dry-run.md
```

发布干跑必须通过。发布前还要人工确认许可证、公开 URL、GitLab Runner 说明、保护
分支设置以及发布 ZIP 中不存在凭据或私有数据。

## 人工边界

测试、校验、打包可以自动执行；approve、merge、创建 Tag 和发布必须由有权限的人
明确决定并执行。
