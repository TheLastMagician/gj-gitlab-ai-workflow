# 示例演练参考

使用本仓库首次演练作为初始化参考：

- 演练记录：`examples/demo-run/00-run-log.md`
- 标签：`examples/demo-run/gitlab/labels.md`
- Milestone 和 Issue：`examples/demo-run/gitlab/milestone-and-issues.md`
- MR 描述：`examples/demo-run/mr/merge-request.md`

关键初始化经验：

1. 写操作前比较 GitLab API 项目路径和 `git remote`。
2. 保持本地 Token helper 被忽略且未暂存。
3. 幂等创建标签、Milestone 和 Issue。
4. 记录需要 UI/管理员确认的 GitLab 设置。
5. 使用 `policy_check.py` 和 `smoke_check.py` 校验。
