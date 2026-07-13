# Integrations

## Observed Facts

- GitLab REST API is used through a local helper during the first demo run.
- GitLab objects used: labels, milestones, issues, notes, merge requests, and pipelines.
- GitLab API helpers read URL, project ID, and token from environment variables;
  token storage and minimum scopes are defined in `docs/gitlab-access.md`.
- No external database, queue, or third-party service is used by the demo project.

## Needs Confirmation

- Webhook authentication method.
- AI gateway contract.
- Which organization secret manager should supply GitLab tokens outside CI.
