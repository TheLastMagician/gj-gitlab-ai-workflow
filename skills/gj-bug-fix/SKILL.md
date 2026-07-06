---
name: gj-bug-fix
description: Analyze GitLab Bug Issues or QA failures and produce reproduction, likely root cause, fix scope, regression tests, risk notes, and GitLab-ready comments. Use for bug reports, failed tests, failed acceptance checks, or pipeline failures tied to behavior.
---

# GJ Bug Fix

## Workflow

1. Read the Bug Issue, linked requirement, failing test, logs, and recent MR.
2. Separate observed facts from hypotheses.
3. Reproduce or describe exact reproduction steps.
4. Identify likely root cause and affected paths.
5. Propose the smallest safe fix.
6. Define regression tests and validation steps.
7. Check documentation impact:
   - Update `docs/qa/test-reports/<feature>.md` with failed checks and fix
     validation when QA execution exists.
   - Update PRD, product design, technical solution, module docs, or context docs
     when the bug changes durable behavior or exposes a wrong assumption.
8. If the bug reveals unclear requirements or architecture risk, recommend upgrading the workflow path.

## Output

```markdown
## AI Bug Analysis

Bug summary:

Reproduction steps:

Observed facts:

Likely root cause:

Fix scope:

Regression tests:

Documentation impact:

Risk and human confirmation:

Workflow upgrade needed:
```

## References

Read `references/demo-run.md` for the self-approval bug example.
