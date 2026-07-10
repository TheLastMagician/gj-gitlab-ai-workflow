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

- Issue 关联、MR 章节完整性:CI `policy_check`。
- 模块文档回写:评审员在决策门 3(合并)人工确认;
  迭代级兜底由 CI `context_freshness_check` 在发布阶段拦截。
