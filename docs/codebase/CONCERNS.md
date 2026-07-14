# 风险和关注点

## 安全

- `.gj/gitlab.local.json` 包含本地 GitLab Token，必须保持忽略状态。
- `policy_check.py` 扫描已跟踪文件，不扫描任意未跟踪的本地文件。
- Orchestrator 骨架尚不能用于生产，也没有 webhook 认证。

## 工作流

- GitLab API ProjectId 必须在写操作前与 `git remote` 匹配。
- 部分 GitLab 设置需要通过 UI 或管理员 API 确认。
- 必须检查 GitLab Runner 是否可用。首次 MR Pipeline 在注册 Runner 前一直处于 pending；
  Windows shell executor 还暴露过 PowerShell 工作目录问题。
- Skill 草案来自一次示例演练，还需要第二次演练验证。

## 工具

- 未传 `--name` 时，Skill 元数据生成器可能因 Windows 默认编码无法读取 UTF-8 中文
  `SKILL.md`。
