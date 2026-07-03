# Testing

## Observed Facts

- `python scripts/policy_check.py` checks MR template sections, owner ack for
  risky paths, and committed secrets.
- `python scripts/smoke_check.py` runs demo unit tests.
- Demo tests use `unittest`.
- Skill validation uses Codex skill-creator `quick_validate.py`.

## Needs Confirmation

- Whether CI should add SAST or dependency scanning.
- Whether future Orchestrator needs contract tests for GitLab webhook payloads.
