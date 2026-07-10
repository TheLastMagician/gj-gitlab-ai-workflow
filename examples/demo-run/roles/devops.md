# DevOps Role

## Input

- Release Issue #7
- `.gitlab-ci.yml`
- `scripts/policy_check.py`
- `scripts/smoke_check.py`

## Output

Release checklist:

- CI has `policy` and `test` stages.
- `policy_check.py` verifies the unique flow label, MR evidence, high-risk
  changed files, and committed secrets.
- `smoke_check.py` runs demo unit tests.
- Rollback is reverting the MR.

## Manual Confirmation

Needs GitLab UI or admin API confirmation:

- Default branch is protected.
- Merge requires successful pipeline.
- Discussions must be resolved before merge.
