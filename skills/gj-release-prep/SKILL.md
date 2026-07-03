---
name: gj-release-prep
description: Prepare GitLab release readiness artifacts. Use when a milestone or MR set is ready for release planning and needs release notes, included Issues/MRs, configuration or database changes, rollout checks, rollback steps, monitoring, and post-release validation.
---

# GJ Release Prep

## Workflow

1. Read release Issue, milestone, merged or ready MRs, test results, and known risks.
2. List included Issues/MRs and user-visible changes.
3. Check database, config, permission, and operations changes.
4. Draft release note, rollout plan, rollback plan, and validation checklist.
5. Mark manual confirmations for DevOps, Tech Lead, QA, security, or DBA.

## Output

```markdown
## Release Prep

Release scope:

Included Issues and MRs:

Testing result:

Config / database / permission changes:

Release note:

Rollout checklist:

Rollback plan:

Post-release validation:

Human confirmations:
```

## References

Read `references/demo-run.md` for the demo release dry-run example.
