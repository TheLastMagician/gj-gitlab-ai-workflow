---
name: gj-retro-learnings
description: Extract iteration retrospectives, process learnings, improvement actions, and ai-context-summary content from GitLab Issues, MRs, tests, releases, and demo-run artifacts. Use when closing a milestone or preparing durable AI context.
---

# GJ Retro Learnings

## Workflow

1. Read the project control Issue, milestone, requirement, solution, tasks, test, release, retro, and merged MRs.
2. Summarize what shipped and what changed.
3. Separate process friction from product or code defects.
4. Identify which changes belong in long-term context:
   - `docs/context/current-state.md`
   - `docs/modules/*.md`
   - `.ai/context-index.yml`
   - ADRs
5. Identify document quality issues:
   - missing PRD/design/prototype/solution/test/release docs.
   - stale docs that misled implementation, review, or QA.
   - templates or standards that need improvement.
6. Generate `docs/iterations/<iteration>/06-retro.md`.
7. Generate `docs/iterations/<iteration>/ai-context-summary.md`.

## Output

```markdown
## Retro Summary

Shipped:

What worked:

What failed or slowed down:

Defects and root causes:

AI suggestions adopted:

AI misses:

Process improvements:

Documentation improvements:

Long-term context updates:

ai-context-summary draft:
```

## References

Read `references/demo-run.md` for the first-run retro example.
