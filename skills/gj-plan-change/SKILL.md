---
name: gj-plan-change
description: Plan GitLab work at the depth required by its flow label. Use when a requirement, feature, small change, bug, or hotfix needs acceptance criteria, technical approach, task boundaries, test coverage, documentation impact, rollout, or rollback before implementation.
---

# GJ Plan Change

## Workflow

1. Read the work item, current labels, `.gj/context.yml`, and known
   constraints. Load only `always_load`, modules matched by expected paths, and
   feature docs linked by the work item. Never scan `docs/iterations/` by
   default.
2. Resolve exactly one flow label. Recommend a label when missing, but wait for
   human confirmation before treating it as selected.
3. Scale the plan to the selected flow:
   - `flow::fast`: state the change, non-goals, affected files, self-test, and
     documentation impact. Do not create extra planning Issues by default.
   - `flow::standard`: clarify acceptance criteria and non-goals; document the
     technical approach, interface/data/permission impact, risks, tests,
     rollout, rollback, and independently reviewable tasks.
   - `flow::hotfix`: capture severity, impact, mitigation, smallest safe fix,
     minimum review, release validation, rollback, and mandatory follow-up.
4. Match changed or expected paths against `.gj/workflow.yml`. Upgrade Fast to
   Standard or Hotfix when the minimum flow requires it.
5. Split work only when separate ownership, dependencies, or review boundaries
   make additional Issues useful.
6. Cover happy, failure, permission, regression, and release-validation paths
   according to risk. Failed checks become Bug Issues rather than hidden notes.
7. Record documentation impact. When confirmed lasting facts exist and the
   repository is writable, directly update the applicable requirement, design,
   solution, test, module, or release docs as part of the current change. Do not
   create a separate documentation task by default. When facts are unresolved
   or write access is unavailable, return an exact draft and confirmation item.

## Output

```markdown
## Change Plan

Flow and reason:
Goal and non-goals:
Acceptance criteria:
Technical approach:
Impact and risk:
Tasks and dependencies:
Test coverage:
Documentation impact:
Rollout and rollback:
Human confirmation needed:
Ready to implement when:
```

## References

- Read `references/requirement-example.md` when requirements are ambiguous.
- Read `references/solution-example.md` for a Standard technical plan.
- Read `references/split-example.md` before creating multiple Issues.
- Read `references/test-example.md` when acceptance or regression risk matters.
