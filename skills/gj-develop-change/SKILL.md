---
name: gj-develop-change
description: Implement GitLab features, small changes, bugs, and hotfixes using focused project context and flow-aware safeguards. Use when code, tests, or scoped documentation edits are ready to be made after the flow label and required plan are confirmed.
---

# GJ Develop Change

## Workflow

1. Read the active Issue or MR, confirmed flow label, accepted plan when
   required, `.ai/context-index.yml`, `.ai/rule-map.yml`, and only the relevant
   module docs, standards, ADRs, and recent summary.
2. Confirm readiness:
   - Fast needs a bounded change, self-test, and documentation-impact answer.
   - Standard needs an Issue, testable acceptance criteria, and an accepted
     approach for risky behavior.
   - Hotfix needs incident impact, owner-confirmed urgency, minimum review,
     release validation, and rollback.
3. Choose the implementation mode:
   - Feature/change: implement the smallest coherent scope.
   - Bug: separate facts from hypotheses, reproduce, identify root cause, and
     add a regression test.
   - Hotfix: apply the smallest safe fix and defer non-critical cleanup to a
     tracked follow-up.
4. Inspect the codebase before editing and stay within the confirmed scope.
5. Add or update tests for acceptance criteria, failure paths, permissions, and
   the reported regression as applicable.
6. Update module or durable docs in the same MR when behavior or a lasting rule
   changes. Otherwise state why no documentation update is needed.
7. Run focused tests first, then the repository's broader required checks.
8. Prepare a GitLab-ready implementation summary. Never approve, merge, or
   deploy from this skill.

## Output

```markdown
## Development Result

Flow and mode:
Context loaded:
Implemented:
Root cause (bug/hotfix):
Files changed:
Tests and results:
Documentation impact:
Risks and rollback:
Follow-up Issues:
Ready for MR when:
```

## References

- Read `references/context-example.md` for focused context loading.
- Read `references/bug-example.md` for reproduction and regression structure.
- Read `references/hotfix-example.md` for emergency boundaries and follow-up.
