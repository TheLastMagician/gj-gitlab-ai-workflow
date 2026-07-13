# Notification And Handoff Standard

## Principles

- GitLab is the source of truth for workflow responsibility.
- Enterprise WeCom, email, or other company channels may deliver GitLab
  notifications, but they are not the workflow state store.
- AI may help a human inspect, summarize, assign, mention, and route work. AI
  must not treat notification delivery as approval, merge permission, or deploy
  permission.

## Complete Handoff

A handoff to a human is complete only when the GitLab item has:

- A responsible assignee, or a reviewer for MR review.
- A workflow label or status.
- A comment that mentions the next human with `@username` when notification is
  expected.
- A specific requested action.
- A milestone or due date when timing matters.

## Inbox Source

Use GitLab API data for personal workflow inboxes:

- GitLab Todos.
- Assigned Issues.
- Assigned MRs.
- Review-requested MRs.
- Mentions and unresolved discussions.
- Failed or blocked pipelines linked to the person's active work.

Do not build a separate email/Enterprise WeCom inbox reader unless the project
explicitly needs non-GitLab tasks. When notification delivery seems missing,
first check assignment, reviewer, mention, and GitLab notification settings.

## Bootstrap Responsibility

`gj-workflow-bootstrap` installs `.gj/workflow.yml`. Project maintainers must
replace placeholder users with real GitLab usernames before relying on workflow
handoffs.
