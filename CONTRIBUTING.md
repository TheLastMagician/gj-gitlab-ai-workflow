# Contributing

This project should evolve from real workflow runs, not speculative process
documents.

## Contribution Rules

- Add or update examples before generalizing a skill.
- Keep each skill focused on one workflow node.
- Keep secrets, private GitLab tokens, and production data out of examples.
- Run the local validation commands before opening a merge request.

## Local Validation

```powershell
python scripts/policy_check.py --mr-description examples/demo-run/mr/merge-request.md --changed-files examples/demo-run/mr/changed-files.txt
python scripts/validate_skills.py
python scripts/smoke_check.py
python scripts/package_open_source.py --output dist/gj-gitlab-ai-workflow.zip
python scripts/release_dry_run.py --package dist/gj-gitlab-ai-workflow.zip --output build/release-dry-run.md
```
