# GitLab MR 就绪检查参考

使用项目已批准的只读 API 或 connector，绝不输出 Token。

获取或检查：

- MR 详情：`GET /projects/:id/merge_requests/:iid`
- MR Pipeline：`GET /projects/:id/merge_requests/:iid/pipelines`
- Pipeline Job：`GET /projects/:id/pipelines/:pipeline_id/jobs`
- 讨论：`GET /projects/:id/merge_requests/:iid/discussions`
- 变更或 diff 统计：`GET /projects/:id/merge_requests/:iid/changes`

检查 `state`、`sha`、`draft` 或 `work_in_progress`、`merge_status` 或
`detailed_merge_status`、`blocking_discussions_resolved`、标签、关联 Issue，以及当前
head SHA 的最新 Pipeline 状态。

返回一个结论：

- `ready_for_human_merge_decision`
- `not_ready`
- `blocked_by_policy`

本参考资料不授权批准或合并操作。
