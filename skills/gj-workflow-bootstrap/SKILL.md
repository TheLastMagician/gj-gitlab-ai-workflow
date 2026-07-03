---
name: gj-workflow-bootstrap
description: Install and verify the GitLab AI workflow skeleton in a repository. Use when setting up labels, issue/MR templates, .ai config, docs/context, CI policy checks, CODEOWNERS, orchestrator skeletons, or preflight checks before writing workflow objects to GitLab.
---

# GJ Workflow Bootstrap

## Workflow

1. Run preflight before any GitLab write:
   - Compare `git remote -v` with the GitLab API project path.
   - Confirm local API helpers or token files are ignored and not staged.
   - Confirm GitLab runner availability and prefer Docker executor for the
     example pipeline.
   - Record missing GitLab permissions as human confirmation points.
2. Install or update repository assets:
   - `.gitlab/issue_templates/`
   - `.gitlab/merge_request_templates/`
   - `.ai/project.yml`, `.ai/rule-map.yml`, `.ai/context-index.yml`
   - `docs/context/`, `docs/modules/`, `docs/standards/`
   - `.gitlab-ci.yml`, `scripts/policy_check.py`, `scripts/smoke_check.py`
   - `CODEOWNERS`
3. Create GitLab labels, milestone, and starter Issues idempotently.
4. Run local validation.
5. Write a bootstrap summary with created, skipped, failed, and manual-confirmation items.

## Output

```markdown
## Bootstrap Summary

GitLab project:

Created:

Skipped / already existed:

Failed:

Local files changed:

Validation:

Human confirmation needed:

Friction found:
```

## References

Read `references/demo-run.md` when you need a concrete first-run example.
