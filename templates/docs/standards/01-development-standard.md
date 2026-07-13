# Development Standard

- Standard and Hotfix changes must link a GitLab Issue. A Fast low-risk MR may
  omit the Issue when its motivation and scope are clear in the MR description.
- Confirm one route label before implementation and use the same label on the
  MR: `flow::fast`, `flow::standard`, or `flow::hotfix`.
- Keep changes scoped to the accepted requirement and solution.
- Add or update tests when behavior changes.
- Record AI assistance in the MR description.
- When a change touches a business rule, update the matching
  `docs/modules/*.md` in the same MR. This applies to SmallChange MRs too:
  skipping the iteration folder is allowed, skipping the module doc is not.

## 执行点

- 唯一 flow、Standard/Hotfix Issue 关联、高风险路径和新增 secret:CI
  `policy_check` 硬检查。
- MR 章节完整性:`policy_check` 只告警，由评审员判断是否足够。
- 模块文档和迭代上下文回写:对应 Skill 提醒，评审员或发布责任人人工确认。
  `context_freshness_check` 仅供按需审计，不进入默认 CI。
