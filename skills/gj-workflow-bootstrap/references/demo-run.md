# Demo Run Reference

Use this repository's first run as the bootstrap reference:

- Run log: `examples/demo-run/00-run-log.md`
- Labels: `examples/demo-run/gitlab/labels.md`
- Milestone and issues: `examples/demo-run/gitlab/milestone-and-issues.md`
- MR description: `examples/demo-run/mr/merge-request.md`

Key bootstrap lessons:

1. Compare GitLab API project path with `git remote` before writing.
2. Keep local token helpers ignored and unstaged.
3. Create labels, milestone, and Issues idempotently.
4. Record GitLab settings that need UI/admin confirmation.
5. Validate with `policy_check.py` and `smoke_check.py`.
