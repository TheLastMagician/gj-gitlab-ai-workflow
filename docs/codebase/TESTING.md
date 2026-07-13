# Testing

## Observed Facts

- `python scripts/policy_check.py` checks the unique flow label, MR evidence,
  changed-file risk paths, and committed secrets. High-risk paths cannot use
  `flow::fast`.
- `python scripts/smoke_check.py` runs demo unit tests.
- Demo tests use `unittest`.
- Repository validation enforces the eight-skill catalog and portable
  `SKILL.md` metadata; Codex skill-creator `quick_validate.py` can provide an
  additional compatibility check.

## Needs Confirmation

- Whether CI should add SAST or dependency scanning.
- Whether future Orchestrator needs contract tests for GitLab webhook payloads.
