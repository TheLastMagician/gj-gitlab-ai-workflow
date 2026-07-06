---
name: gj-hotfix
description: Guide urgent GitLab hotfix flow without skipping accountability. Use for P0/P1 incidents, security risks, production blockers, data damage, or release blockers that need minimum safe analysis, quick fix scope, owner confirmation, release validation, and required post-fix retro/context updates.
---

# GJ Hotfix

## Workflow

1. Confirm the incident qualifies as hotfix.
2. Capture impact, severity, current mitigation, owner, and decision deadline.
3. Define the smallest safe fix and minimum review path.
4. Require explicit human owner confirmation for risk acceptance.
5. Define release validation and rollback.
6. Check documentation impact:
   - Release note and rollback record for the hotfix.
   - Test report for emergency validation.
   - Root-cause/context/module docs after the immediate fix.
7. Create post-fix requirements: root cause, tests, docs, context, and retro.

## Output

```markdown
## Hotfix Plan

Severity and impact:

Current mitigation:

Smallest safe fix:

Minimum review:

Release validation:

Rollback:

Documentation impact:

Owner confirmations:

Post-fix follow-up:

Upgrade to standard flow if:
```

## References

Read `references/demo-run.md` for hotfix boundaries derived from the first run.
