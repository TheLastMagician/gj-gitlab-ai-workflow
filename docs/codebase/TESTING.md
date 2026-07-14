# 测试

## 已确认事实

- `python scripts/policy_check.py` 检查唯一 flow 标签、MR 证据、变更文件风险路径和已提交
  的秘密；高风险路径不能使用 `flow::fast`。
- `python scripts/smoke_check.py` 运行示例单元测试。
- 示例测试使用 `unittest`。
- 仓库校验检查八个 Skill 的目录清单和可移植 `SKILL.md` 元数据；Codex skill-creator 的
  `quick_validate.py` 可以提供额外兼容性检查。

## 待确认

- CI 是否增加 SAST 或依赖扫描。
- 后续 Orchestrator 是否需要 GitLab webhook payload 契约测试。
