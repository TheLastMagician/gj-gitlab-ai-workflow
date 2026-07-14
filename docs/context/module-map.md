# 模块地图

| 模块 | 路径 | 说明 | 负责人 |
| --- | --- | --- | --- |
| workflow-assets | `templates/`, `.gitlab/`, `.gj/` | 可安装到 GitLab 项目的工作流资产 | @tech-lead |
| workflow-policy | `scripts/policy_check.py`, `.gitlab-ci.yml` | CI 门禁和自动化策略检查 | @devops-owner |
| workflow-tools | `scripts/` | 安装、校验、GitLab helper、打包和发布工具 | @devops-owner |
| orchestrator | `orchestrator/` | 可选 Webhook 命令路由骨架，当前不可直接用于生产 | @ai-platform-owner |
| documentation | `README.md`, `docs/`, `templates/docs/` | 开源说明和安装到业务项目的长期规范模板 | @tech-lead |
| examples | `examples/` | 与通用安装资产隔离的业务样例和端到端演练记录 | @qa-owner |
| skills | `skills/` | 从真实 run 反推的首批 skill 草案 | @ai-platform-owner |
