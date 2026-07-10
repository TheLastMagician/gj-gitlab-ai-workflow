---
name: gj-close-loop
description: Close completed GitLab work by capturing lessons and refreshing durable project context. Use after an MR, bug fix, hotfix, release, or milestone when current-state, module docs, ADRs, context indexes, iteration summaries, or process follow-ups may need updates.
---

# GJ Close Loop

## Workflow

1. Read the completed work item, MR, pipeline and test evidence, release notes,
   bugs, follow-ups, and current durable docs.
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
   `.ai/context-index.yml`.
5. Keep `recent_iteration_summaries` within its configured limit and ensure the
   latest summary is first.
6. Preserve conflicts and ask for human confirmation instead of inventing a
   single truth.
7. Create tracked improvement items for unresolved defects or process changes.

## Output

```markdown
## Close Loop

Completed scope:
Evidence:
What worked or failed:
Durable facts:
Historical-only notes:
Files updated:
Documentation impact:
Follow-up Issues:
Human confirmation needed:
Closure status:
```

## References

- Read `references/retro-example.md` for milestone learning extraction.
- Read `references/context-example.md` for durable-versus-historical context.
