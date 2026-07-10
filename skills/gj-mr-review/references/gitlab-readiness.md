# GitLab MR Readiness Reference

Use read-only project-approved API or connector methods. Never print tokens.

Fetch or inspect:

- MR details: `GET /projects/:id/merge_requests/:iid`
- MR pipelines: `GET /projects/:id/merge_requests/:iid/pipelines`
- Pipeline jobs: `GET /projects/:id/pipelines/:pipeline_id/jobs`
- Discussions: `GET /projects/:id/merge_requests/:iid/discussions`
- Changes or diff stats: `GET /projects/:id/merge_requests/:iid/changes`

Check `state`, `sha`, `draft` or `work_in_progress`, `merge_status` or
`detailed_merge_status`, `blocking_discussions_resolved`, labels, linked Issues,
and the latest pipeline status for the current head SHA.

Return one decision:

- `ready_for_human_merge_decision`
- `not_ready`
- `blocked_by_policy`

This reference does not authorize approve or merge operations.
