# Integrations

## Observed Facts

- GitLab REST API is used through the installed `scripts/gitlab_api.py` helper.
- GitLab objects used: labels, milestones, issues, notes, merge requests, and pipelines.
- Local URL, project ID, and token are stored in ignored
  `.gj/gitlab.local.json`; CI environment variables may override them.
- No external database, queue, or third-party service is used by the demo project.

## Needs Confirmation

- Webhook authentication method.
- AI gateway contract.
- Which organization secret manager should supply GitLab tokens outside CI.
