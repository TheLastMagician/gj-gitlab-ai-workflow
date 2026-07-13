# GitLab Inbox API Reference

Use this reference when `gj-workflow-next` needs live GitLab state. Prefer the
project-approved helper or MCP/API client. Never print tokens.

## Authentication

Installing the Skill does not require a token. For live access, prefer the
Agent's configured GitLab MCP/connector. Otherwise use a project-approved API
helper that reads `GITLAB_URL`, `GITLAB_PROJECT_ID`, and `GITLAB_TOKEN` from the
environment. Do not read credentials from repository files or print them.

Use a current-user Personal Access Token with `read_api` when personal Todos are
required. Use `api` only for human-confirmed writes such as creating an Issue,
setting labels or assignees, and posting notes. A Project Access Token represents
a bot account and therefore cannot stand in for a person's Todo inbox. See
the public [GitLab access guide](https://github.com/TheLastMagician/gj-gitlab-ai-workflow/blob/main/docs/gitlab-access.md)
for setup and storage rules.

## Core sources

- Current user: `GET /user`
- User lookup: `GET /users?username=<username>`
- Todos: `GET /todos`
- Project Issues assigned to a user:
  `GET /projects/:id/issues?state=opened&assignee_username=<username>`
- Project MRs assigned to a user:
  `GET /projects/:id/merge_requests?state=opened&assignee_username=<username>`
- Project MRs requiring review from a user:
  `GET /projects/:id/merge_requests?state=opened&reviewer_username=<username>`
- MR discussions:
  `GET /projects/:id/merge_requests/:iid/discussions`
- MR pipelines:
  `GET /projects/:id/merge_requests/:iid/pipelines`
- Project failed pipelines:
  `GET /projects/:id/pipelines?status=failed`
- Notes for an Issue:
  `GET /projects/:id/issues/:iid/notes`
- Notes for an MR:
  `GET /projects/:id/merge_requests/:iid/notes`

## Optional write actions

Use write actions only when the human asks for assignment, reviewer setup, or a
handoff comment. These actions create accountability and notification events;
they do not approve or complete work.

- Assign Issue:
  `PUT /projects/:id/issues/:iid` with `assignee_ids`
- Assign MR:
  `PUT /projects/:id/merge_requests/:iid` with `assignee_ids`
- Set MR reviewer:
  `PUT /projects/:id/merge_requests/:iid` with `reviewer_ids`
- Add Issue note:
  `POST /projects/:id/issues/:iid/notes`
- Add MR note:
  `POST /projects/:id/merge_requests/:iid/notes`
- Mark todo done only after the human confirms the underlying work was handled:
  `POST /todos/:id/mark_as_done`

## Local PowerShell helper pattern

Some projects keep a local ignored helper such as `gitlab-api.ps1`.

```powershell
.\gitlab-api.ps1 -Method GET -ApiPath "todos"
.\gitlab-api.ps1 -Method GET -ApiPath "projects/:project/issues?state=opened&assignee_username=zengqinglin"
.\gitlab-api.ps1 -Method GET -ApiPath "projects/:project/merge_requests?state=opened&reviewer_username=zengqinglin"
.\gitlab-api.ps1 -Method PUT -ApiPath "projects/:project/issues/12" -Body @{
  assignee_ids = @(55)
}
.\gitlab-api.ps1 -Method POST -ApiPath "projects/:project/issues/12/notes" -Body @{
  body = "@zengqinglin please handle the QA verification step."
}
```

## Notification model

GitLab is the source of truth. Enterprise WeCom, email, or other company
messaging systems may deliver GitLab notifications, but this skill should not
read those channels. If a person did not receive a notification, verify the
GitLab item has an assignee/reviewer and an `@username` handoff comment, then
ask the human to check GitLab notification settings.
