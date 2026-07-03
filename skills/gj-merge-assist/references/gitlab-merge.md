# GitLab Merge Reference

Use this reference only when the human has explicitly authorized a merge.

Clear authorization examples can be English or Chinese, for example
`Confirm merge MR !2` or `确认合并 MR !2`. Ambiguous wording is not enough.

## Readiness API Data

Fetch or inspect:

- MR details: `GET /projects/:id/merge_requests/:iid`
- MR pipelines: `GET /projects/:id/merge_requests/:iid/pipelines`
- Pipeline jobs: `GET /projects/:id/pipelines/:pipeline_id/jobs`
- Discussions: `GET /projects/:id/merge_requests/:iid/discussions`
- Changes or diff stats when needed: `GET /projects/:id/merge_requests/:iid/changes`

Check these fields when available:

- `state`
- `sha`
- `merge_status` or `detailed_merge_status`
- `blocking_discussions_resolved`
- `draft` or `work_in_progress`
- latest pipeline `status`

## Merge API

Use normal merge:

```text
PUT /projects/:id/merge_requests/:iid/merge
```

Common body fields:

```json
{
  "should_remove_source_branch": true,
  "merge_when_pipeline_succeeds": false,
  "sha": "<last-read-mr-sha>"
}
```

Do not set options that skip CI or bypass normal policy.

## Local Helper Pattern

If a repository has a project-local API helper, prefer its established pattern. Example shape:

```powershell
.\gitlab-api.ps1 -Method GET -ApiPath "projects/:project/merge_requests/2"
.\gitlab-api.ps1 -Method PUT -ApiPath "projects/:project/merge_requests/2/merge" -Body @{
  should_remove_source_branch = $true
  merge_when_pipeline_succeeds = $false
  sha = "<last-read-mr-sha>"
}
```

Never commit local helper files containing tokens.
