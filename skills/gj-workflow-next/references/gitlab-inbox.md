# GitLab Inbox API Reference

Use this reference when `gj-workflow-next` needs live GitLab state. Prefer the
installed `scripts/gitlab_api.py` helper so Codex, Claude Code, and OpenCode use
the same guarded API behavior. Never print tokens.

## Authentication

Installing the Skill does not require a token. For live access, configure once:

```powershell
python scripts/gitlab_api.py configure --url https://gitlab.example.com --project-id group/project
python scripts/gitlab_api.py doctor
```

The helper reads ignored `.gj/gitlab.local.json`; CI environment variables may
override it. Do not open, print, stage, or send the local config to an Agent.

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
  `GET /projects/:project/issues?state=opened&assignee_username=<username>`
- Project MRs assigned to a user:
  `GET /projects/:project/merge_requests?state=opened&assignee_username=<username>`
- Project MRs requiring review from a user:
  `GET /projects/:project/merge_requests?state=opened&reviewer_username=<username>`
- MR discussions:
  `GET /projects/:project/merge_requests/:iid/discussions`
- MR pipelines:
  `GET /projects/:project/merge_requests/:iid/pipelines`
- Project failed pipelines:
  `GET /projects/:project/pipelines?status=failed`
- Notes for an Issue:
  `GET /projects/:project/issues/:iid/notes`
- Notes for an MR:
  `GET /projects/:project/merge_requests/:iid/notes`

## Optional write actions

Use write actions only when the human asks for assignment, reviewer setup, or a
handoff comment. These actions create accountability and notification events;
they do not approve or complete work.

- Assign Issue:
  `PUT /projects/:project/issues/:iid` with `assignee_ids`
- Assign MR:
  `PUT /projects/:project/merge_requests/:iid` with `assignee_ids`
- Set MR reviewer:
  `PUT /projects/:project/merge_requests/:iid` with `reviewer_ids`
- Add Issue note:
  `POST /projects/:project/issues/:iid/notes`
- Add MR note:
  `POST /projects/:project/merge_requests/:iid/notes`

## Helper commands

```powershell
python scripts/gitlab_api.py request --path "todos"
python scripts/gitlab_api.py request --path "projects/:project/issues?state=opened&assignee_username=zengqinglin"
python scripts/gitlab_api.py request --path "projects/:project/merge_requests?state=opened&reviewer_username=zengqinglin"
python scripts/gitlab_api.py request --method PUT --path "projects/:project/issues/12" --body-json '{"assignee_ids":[55]}' --confirm-write
python scripts/gitlab_api.py request --method POST --path "projects/:project/issues/12/notes" --body-json '{"body":"@zengqinglin please handle QA verification."}' --confirm-write
```

Writes fail unless `--confirm-write` is present, the path uses `:project`, and
the configured GitLab project matches `git remote origin`. The helper rejects
credential, runner, webhook, and CI-variable endpoints.

## Notification model

GitLab is the source of truth. Enterprise WeCom, email, or other company
messaging systems may deliver GitLab notifications, but this skill should not
read those channels. If a person did not receive a notification, verify the
GitLab item has an assignee/reviewer and an `@username` handoff comment, then
ask the human to check GitLab notification settings.
