---
name: gj-workflow-inbox
description: Inspect and triage a person's GitLab workflow inbox through GitLab API data. Use when a user asks what work is assigned to them, what review requests or mentions need action, what GitLab Todos are pending, which workflow skill should handle each item, or whether handoff/notification ownership is missing.
---

# GJ Workflow Inbox

## Overview

Use GitLab as the source of truth for actionable work. Do not read email or
Enterprise WeCom directly; those channels are notification/audit delivery
mechanisms that should point back to GitLab Issues, MRs, Todos, and comments.

## Safety Boundary

- Do not approve, merge, deploy, or close work unless the human explicitly asks
  for that action and the matched downstream skill permits it.
- Treat assignee, reviewer, and mention data as routing signals, not automatic
  authorization.
- If a notification appears missing, report the GitLab assignment or mention
  gap instead of creating a separate notification workflow.
- Do not expose tokens, private helper files, or personal contact addresses in
  summaries.

## Inputs

Gather as much as is available:

- Current GitLab username or user id.
- Project id/path and GitLab base URL.
- Local helper command, MCP tool, or direct API method approved for the project.
- `.ai/project.yml`, `.ai/role-map.yml`, and `.ai/rule-map.yml` when present.
- Optional focus: today, milestone, MR review, QA, failed pipeline, release, or
  a specific role.

Read `references/gitlab-inbox.md` when using GitLab API endpoints.

## Workflow

1. Resolve the actor:
   - Prefer the explicit username in the request.
   - Otherwise read `.ai/role-map.yml` and infer from the role.
   - If still unknown, ask for the GitLab username before writing anything.
2. Fetch GitLab work:
   - Todos for the actor.
   - Open Issues assigned to the actor.
   - Open MRs assigned to or requiring review from the actor.
   - Recent mentions and unresolved MR discussions when the API/tool supports
     them.
   - Failed, blocked, or pending pipelines related to the actor's open MRs.
3. Normalize each item:
   - Type: todo, issue, MR, review request, discussion, pipeline, release, bug,
     hotfix, or context task.
   - URL, iid, title, labels, state, assignee/reviewer, updated time, and
     blocking condition.
   - Required human decision, if any.
4. Route items to the smallest useful workflow skill:
   - Triage or unclear path: `gj-workflow-triage`
   - Requirement clarification: `gj-requirement-refine`
   - Solution/architecture: `gj-solution-plan`
   - Issue/task split: `gj-issue-split`
   - Development context: `gj-dev-context`
   - MR review: `gj-mr-review`
   - Merge readiness or human-authorized merge: `gj-merge-assist`
   - QA/test design or failed acceptance: `gj-test-design`
   - Dev/test deployment: `gj-env-deploy-assist`
   - Bug: `gj-bug-fix`
   - Hotfix: `gj-hotfix`
   - Release: `gj-release-prep`
   - Retro/context update: `gj-retro-learnings` or `gj-context-extract`
5. Identify notification and handoff gaps:
   - Missing assignee on a human-owned step.
   - Missing reviewer on an MR review step.
   - Missing `@username` mention on a handoff comment.
   - Missing due date or milestone when the task is time-bound.
   - Todo exists but the linked item has no clear next action.
6. Present the inbox and wait for the human to choose actions unless the request
   already names a safe read-only action.

## Output

```markdown
## GitLab Workflow Inbox

Actor:
Project:
Fetched:

### Actionable Items
| Priority | Item | Why it needs attention | Suggested skill | Human decision |
| --- | --- | --- | --- | --- |

### Waiting / Blocked
| Item | Blocker | Owner | Suggested next step |
| --- | --- | --- | --- |

### Handoff Gaps
- ...

### Recommended Next Action
...
```

## Priority Heuristics

- P0: production incident, hotfix, security issue, blocked release, failed
  shared environment deployment.
- P1: MR waiting on the actor, failed pipeline on an active MR, QA blocker,
  explicit due date today.
- P2: requirement/solution/task work needed for the current milestone.
- P3: retro, context extraction, backlog cleanup, non-blocking suggestions.

## Handoff Rule

A GitLab handoff is complete only when the item has:

- A responsible assignee or reviewer.
- A visible workflow label/status.
- A comment that names the next human with `@username` when a notification is
  expected.
- A specific requested action.
- A due date or milestone when timing matters.

## References

Read `references/gitlab-inbox.md` for endpoint patterns and local helper usage.
