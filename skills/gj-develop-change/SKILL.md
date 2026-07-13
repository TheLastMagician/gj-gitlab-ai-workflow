---
name: gj-develop-change
description: Implement GitLab features, small changes, bugs, and hotfixes using focused project context and flow-aware safeguards. Use when code, tests, or scoped documentation edits are ready to be made after the flow label and required plan are confirmed.
---

# GJ Develop Change

## Workflow

1. Read the active Issue or MR, confirmed flow label, accepted plan when
   required, `.gj/context.yml`, `.gj/workflow.yml`, and only the relevant
   module docs, standards, ADRs, and recent summary. When present, use
   `docs/standards/12-context-governance.md` for document lifecycle decisions.
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
6. Re-evaluate the plan against the actual changed paths. Update module,
   requirement, design, solution, interface, or other current-fact docs in the
   same MR when behavior, contracts, permissions, data meaning, operations, or
   a lasting rule changes. Update existing semantic files in place. Otherwise
   state why no documentation update is needed.
7. Keep the Issue, MR, and feature documents linked to the confirmed Target
   release/Milestone. Ordinary feature, bug, and Fast MRs do not bump the
   repository version or create Tags; version fields in project manifests are
   changed only by explicit release-preparation work.
8. Run focused tests first, then the repository's broader required checks.
9. Output a documentation decision table using `create`, `update`, `no-change`,
   or `follow-up`, with path, reason, and status/confirmer. A follow-up is only
   valid with an Issue, owner, and due date.
10. Prepare a GitLab-ready implementation summary. Never approve, merge, or
   deploy from this skill.

## Output

```markdown
## Development Result

Flow and mode:
Target release / Milestone:
Context loaded:
Implemented:
Root cause (bug/hotfix):
Files changed:
Tests and results:
Documentation impact:
Documentation decisions (path / action / reason / status or confirmer):
Risks and rollback:
Follow-up Issues:
Ready for MR when:
```

## References

- Read `references/context-example.md` for focused context loading.
- Read `references/bug-example.md` for reproduction and regression structure.
- Read `references/hotfix-example.md` for emergency boundaries and follow-up.
