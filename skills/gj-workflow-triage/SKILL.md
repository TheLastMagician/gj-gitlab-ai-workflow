---
name: gj-workflow-triage
description: Classify GitLab work into standard requirement, small change, bug fix, or hotfix flow. Use when an Issue, MR, incident, QA failure, or pipeline failure needs workflow routing, required steps, risk labels, and human confirmation points.
---

# GJ Workflow Triage

## Workflow

1. Read the Issue or MR title, description, labels, changed paths, and comments.
2. Look for hard blockers against small-change flow:
   - permission, approval, money, security, production config.
   - database schema or migration.
   - external API contract.
   - multiple modules or teams.
   - unclear validation scope.
3. Classify the path:
   - standard requirement.
   - small change.
   - bug fix.
   - hotfix.
   - Hotfix
4. List required workflow objects and which steps can be skipped.
5. Add explicit human confirmation points.

## Output

```markdown
## Workflow Triage

Recommended path:

Reasoning:

Skippable steps:

Required steps:

Suggested labels:

Risk notes:

Human confirmation needed:
```

## References

Read `references/demo-run.md` for the order approval triage example.
