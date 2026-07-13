---
name: gj-workflow-bootstrap
description: Install and verify the GitLab AI workflow skeleton in a repository. Use when setting up labels, issue/MR templates, .gj workflow and context config, role ownership, docs/context, CI policy checks, CODEOWNERS, orchestrator skeletons, or preflight checks before writing workflow objects to GitLab.
---

# GJ Workflow Bootstrap

## Workflow

1. Run preflight before any GitLab write:
   - When `.gj/gitlab.local.json` is missing, run
     `python scripts/gitlab_api.py configure --url <url> --project-id <id>`.
   - Run `python scripts/gitlab_api.py doctor` to compare `git remote origin`
     with the GitLab API project path without printing the token.
   - Confirm `.gj/gitlab.local.json` is ignored and not staged.
   - Confirm GitLab runner availability and prefer Docker executor for the
     example pipeline.
   - Record missing GitLab permissions as human confirmation points.
2. Install all reusable assets once:
   - In a source checkout, run `scripts/install_workflow.py --target <repo>`.
   - When only this Skill is installed, resolve this Skill's own directory and
     run `scripts/bootstrap_from_github.py --target <repo>`. It fetches the
     trusted source archive and invokes the same non-destructive installer.
   - If the installer reports exit code `2`, stop and show the exact manual CI
     include action. Fast, Standard, and Hotfix are runtime routes, not
     installation editions.
3. Ask the maintainer to replace placeholder roles in `.gj/workflow.yml` when
   role routing is needed and review `docs/standards/06-release-standard.md`.
   Confirm `.gj/workflow.yml` versioning policy, the Tag pattern, release-note
   path, and `docs/standards/13-versioning-standard.md` without adding a generic
   VERSION file.
   Confirm `.gj/doc-templates/` was installed as workflow scaffolding and that
   no generic template files were placed in the project's fact directories.
4. Create GitLab labels, milestone, and starter Issues idempotently through the
   configured helper or an approved GitLab connector.
5. Assign human-owned starter Issues/MRs from `.gj/workflow.yml` when requested
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

Documentation templates installed under .gj/doc-templates:

Friction found:
```

## References

Read `references/demo-run.md` when you need a concrete first-run example.
