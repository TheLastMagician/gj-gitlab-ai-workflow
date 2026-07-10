---
name: gj-workflow-bootstrap
description: Install and verify the GitLab AI workflow skeleton in a repository. Use when setting up labels, issue/MR templates, .ai config, role-map ownership, docs/context, CI policy checks, CODEOWNERS, orchestrator skeletons, or preflight checks before writing workflow objects to GitLab.
---

# GJ Workflow Bootstrap

## Workflow

1. Run preflight before any GitLab write:
   - Compare `git remote -v` with the GitLab API project path.
   - Confirm local API helpers or token files are ignored and not staged.
   - Confirm GitLab runner availability and prefer Docker executor for the
     example pipeline.
   - Record missing GitLab permissions as human confirmation points.
2. Install or update all reusable assets once with
   `scripts/install_workflow.py`. Fast, Standard, and Hotfix are runtime routes,
   not installation editions.
3. Ask the maintainer to replace placeholder roles in `.ai/role-map.yml` when
   role routing is needed and review `docs/standards/06-release-standard.md`.
4. Create GitLab labels, milestone, and starter Issues idempotently.
5. Assign human-owned starter Issues/MRs from `.ai/role-map.yml` when requested
   and add `@username` handoff comments when notification is expected.
6. Run local validation.
7. Write a bootstrap summary with created, skipped, failed, and manual-confirmation items.

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

Documentation templates installed:

Friction found:
```

## References

Read `references/demo-run.md` when you need a concrete first-run example.
