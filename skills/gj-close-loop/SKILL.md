---
name: gj-close-loop
description: Close completed GitLab work by capturing lessons and refreshing durable project context. Use after an MR, bug fix, hotfix, release, or milestone when current-state, module docs, ADRs, context indexes, iteration summaries, or process follow-ups may need updates.
---

# GJ Close Loop

## Workflow

1. Read the completed work item, MR, pipeline and test evidence, release notes,
   bugs, follow-ups, `.gj/context.yml`, relevant module docs, and only the
   current iteration directory. Do not load older iteration archives unless a
   specific decision conflict requires traceability.
2. Scale closure to the flow:
   - Fast: record the result and update durable docs only if behavior changed.
   - Standard: summarize delivery, decisions, tests, friction, and context
     updates; write the iteration summary when the project uses iterations.
   - Hotfix: require root cause, regression coverage, documentation repair,
     risk follow-ups, and a short retro after the immediate fix.
3. Separate current durable facts from history, hypotheses, and superseded
   decisions.
4. Update the smallest applicable set of `docs/context`, `docs/modules`, product
   docs, solution docs, test reports, release notes, ADRs, and
   `.gj/context.yml`. Only update `current-state.md` for cross-project current
   facts, and only create an iteration summary for an important milestone or
   when project policy explicitly requires it. Normal Fast and most single-Issue
   changes do not need an iteration directory.
5. After a release or deployment, distinguish planned from actual state. Update
   the release note and `docs/context/current-state.md` with the released Tag,
   commit SHA, Pipeline, environment, deployment time, post-release validation,
   and rollback result. Never claim a Milestone or untagged commit is released.
6. Keep `recent_iteration_summaries` within its configured limit and ensure the
   latest summary is first.
7. Preserve conflicts and ask for human confirmation instead of inventing a
   single truth.
8. Remove superseded current facts instead of retaining deprecation sections;
   Git and frozen evidence provide history.
9. Output a documentation decision table using `create`, `update`, `no-change`,
   or `follow-up`. Every follow-up includes an Issue, owner, and due date.
10. Create tracked improvement items for unresolved defects or process changes.

## Output

```markdown
## Close Loop

Completed scope:
Evidence:
Released Tag / SHA / Pipeline / deployed environments:
What worked or failed:
Durable facts:
Historical-only notes:
Files updated:
Documentation impact:
Documentation decisions (path / action / reason / status or confirmer):
Follow-up Issues:
Human confirmation needed:
Closure status:
```

## References

- Read `references/retro-example.md` for milestone learning extraction.
- Read `references/context-example.md` for durable-versus-historical context.
