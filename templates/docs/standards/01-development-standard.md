# 开发规范

- Standard 和 Hotfix 变更必须关联 GitLab Issue。低风险 Fast MR 在描述中写清动机和
  范围后可以不建 Issue。
- 实现前确认唯一流程标签，并在 MR 中沿用：`flow::fast`、`flow::standard` 或
  `flow::hotfix`。
- 变更范围不得超出已确认的需求和方案。
- 行为变化时新增或更新测试。
- 在 MR 描述中记录 AI 使用范围。
- 变更业务规则时，在同一 MR 更新对应的 `docs/modules/*.md`。SmallChange MR 也适用：
  Fast 可以省略计划文档，但不能省略已变化的长期事实。

## 执行点

- 唯一 flow、Standard/Hotfix Issue 关联、高风险路径和新增 secret:CI
  `policy_check` 硬检查。
- MR 章节完整性:`policy_check` 只告警，由评审员判断是否足够。
- 文档决策和持久事实回写:对应 Skill 执行，评审员或发布责任人人工确认。
  `context_freshness_check` 仅供按需审计，不进入默认 CI。
