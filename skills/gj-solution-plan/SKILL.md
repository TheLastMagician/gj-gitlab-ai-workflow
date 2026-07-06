---
name: gj-solution-plan
description: Draft technical solution plans from confirmed GitLab requirements. Use when a requirement needs impact analysis, architecture options, interface/data/permission changes, risk assessment, test scope, release notes, rollback notes, and Tech Lead review output.
---

# GJ Solution Plan

## Workflow

1. Read the confirmed requirement, acceptance criteria, linked project issue, and milestone.
2. Load minimal context from `.ai/context-index.yml`, `docs/context`, relevant `docs/modules`, and active ADRs.
3. Identify impacted modules, files, interfaces, data, permissions, operations, and rollout paths.
4. Present the recommended solution and rejected alternatives.
5. Check documentation impact:
   - Create or update `docs/technical/solutions/<feature>.md` when architecture,
     interface, data, permission, compatibility, rollout, or rollback decisions
     become durable.
   - Update `docs/modules/*.md` when module behavior or boundaries change.
   - Propose ADR updates when the decision is cross-module or long-lived.
6. List risks, owner ack needs, test scope, rollout, and rollback.
7. Write a GitLab-ready solution Issue or comment for Tech Lead review.

## Output

```markdown
## Solution Plan

Requirement:

Recommended solution:

Alternatives considered:

Impact scope:

Interface / data / permission changes:

Documentation impact:

Implementation notes:

Test scope:

Release and rollback:

Risks and owner ack:

Tech Lead review checklist:
```

## References

Read `references/demo-run.md` for the order approval solution example.
