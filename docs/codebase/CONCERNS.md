# Concerns

## Security

- `.gj/gitlab.local.json` contains the local GitLab token and must stay ignored.
- `policy_check.py` scans tracked files, not arbitrary untracked local files.
- Orchestrator skeleton is not production-ready and has no webhook auth.

## Workflow

- GitLab API ProjectId must match `git remote` before writes.
- Some GitLab settings require UI or admin API confirmation.
- GitLab runner availability must be checked. The first MR pipeline stayed
  pending until a runner was registered, and Windows shell executor exposed a
  PowerShell working-directory issue.
- Skill drafts are based on one demo run and need a second run.

## Tooling

- Skill metadata generation can fail on Windows default encoding when reading
  UTF-8 Chinese SKILL.md files without `--name`.
