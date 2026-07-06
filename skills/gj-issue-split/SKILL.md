---
name: gj-issue-split
description: Split confirmed requirements and solution plans into traceable GitLab work items. Use when creating development, test, documentation, release, bug, hotfix, or follow-up Issues with dependencies, labels, acceptance criteria, owners, and workflow states.
---

# GJ Issue Split

## Workflow

1. Read the requirement, solution, milestone, and project control issue.
2. Decide the smallest useful set of Issues:
   - development tasks.
   - test tasks.
   - release tasks.
   - documentation/context tasks.
   - follow-up risks or bugs.
3. Keep each task independently reviewable and linked back to source Issues.
4. Add labels, dependencies, expected files/modules, acceptance criteria, test requirements, and AI usage notes.
5. Add explicit documentation Issues when PRD, product design, prototype record,
   technical solution, test plan, release note, module docs, or context updates
   are needed but should not be bundled into the development task.
6. Mark any split that needs human owner assignment.

## Output

```markdown
## Issue Split

Source requirement:

Source solution:

Milestone:

Issues to create:

Dependencies:

Suggested labels:

Documentation tasks:

Human owner assignment needed:

Out of scope:
```

## References

Read `references/demo-run.md` for the order approval task map example.
