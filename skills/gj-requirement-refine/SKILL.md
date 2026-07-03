---
name: gj-requirement-refine
description: Refine rough GitLab requirements into clear questions, acceptance criteria, non-goals, risks, and Definition of Ready checks. Use for product requirement Issues before planning, scheduling, or solution design.
---

# GJ Requirement Refine

## Workflow

1. Read the current requirement Issue and linked project or milestone.
2. Load minimal context:
   - `.ai/project.yml`
   - `.ai/context-index.yml`
   - `docs/context/current-state.md`
   - relevant `docs/modules/*.md`
3. Identify missing facts, ambiguity, hidden permission/data/API risks, and non-goals.
4. Draft acceptance criteria that can be tested.
5. Decide whether the requirement satisfies Definition of Ready.
6. Write a GitLab-ready comment. Do not mark the requirement approved unless a
   human product owner explicitly confirms or asks for assisted approval.

## Output

```markdown
## AI Requirement Refinement

Recommended path:

Requirement summary:

Missing questions:

Ambiguity and risks:

Acceptance criteria draft:

Suggested non-goals:

DoR conclusion:

Product confirmation needed:
```

## References

Read `references/demo-run.md` for the first-run requirement example.
