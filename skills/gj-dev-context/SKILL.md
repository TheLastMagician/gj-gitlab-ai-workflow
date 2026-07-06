---
name: gj-dev-context
description: Load focused implementation context before coding in a GitLab workflow. Use when a developer starts a task or MR and needs linked Issues, accepted solution, module docs, standards, ADRs, risk rules, expected files, tests, and implementation cautions.
---

# GJ Dev Context

## Workflow

1. Read the development Issue, linked requirement, linked solution, and existing MR if present.
2. Load `.ai/project.yml`, `.ai/rule-map.yml`, `.ai/context-index.yml`.
3. Load only relevant context docs, module docs, standards, ADRs, and recent iteration summaries.
4. Summarize implementation goal, non-goals, risk paths, expected files, tests, and open questions.
5. Check whether required docs exist before coding:
   - PRD for durable product behavior.
   - Product design/prototype when UI or interaction matters.
   - Technical solution for risky architecture, interface, data, permission, or
     rollout changes.
   - Test plan when acceptance or regression coverage is non-trivial.
6. Warn when current context conflicts with historical iteration notes.
7. Produce a concise developer handoff before code changes.

## Output

```markdown
## Development Context

Task:

Linked requirement and solution:

Context loaded:

Implementation goal:

Non-goals:

Expected files/modules:

Risk rules and owner ack:

Documentation readiness:

Tests to run or add:

Open questions:
```

## References

Read `references/demo-run.md` for the order approval developer context.
