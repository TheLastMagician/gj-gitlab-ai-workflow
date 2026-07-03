---
name: gj-test-design
description: Design QA and regression tests for GitLab workflow items. Use when requirements, solutions, MRs, bugs, or releases need acceptance tests, failure paths, permission checks, regression scope, QA reports, and conversion of failed checks into Bug Issues.
---

# GJ Test Design

## Workflow

1. Read requirement acceptance criteria, solution notes, MR changes, and bug history.
2. Cover happy path, failure path, permission path, regression path, and release validation.
3. Map every test to a requirement or risk.
4. State test data, steps, expected result, and automation/manual status.
5. If a test fails, create or draft a Bug Issue instead of hiding the failure in the report.

## Output

```markdown
## Test Design

Scope:

Test matrix:

Regression scope:

Permission and security checks:

Release validation:

Failed checks needing Bug Issues:

QA sign-off checklist:
```

## References

Read `references/demo-run.md` for the self-approval QA failure example.
