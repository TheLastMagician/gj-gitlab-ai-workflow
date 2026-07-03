---
name: gj-context-extract
description: Extract durable AI context from completed GitLab workflow artifacts. Use after releases, retrospectives, bug fixes, hotfixes, or major MRs to update docs/context, docs/modules, ADRs, .ai/context-index.yml, and iteration ai-context-summary without treating stale history as current truth.
---

# GJ Context Extract

## Workflow

1. Read milestone artifacts, release notes, retro, merged MRs, tests, bugs, and current docs.
2. Separate current durable facts from historical narrative and unconfirmed inferences.
3. Decide update targets:
   - `docs/context/current-state.md`
   - `docs/context/module-map.md`
   - `docs/context/glossary.md`
   - `docs/modules/*.md`
   - `docs/architecture/adr/*.md`
   - `.ai/context-index.yml`
   - iteration `ai-context-summary.md`
4. Preserve conflicts and request human confirmation when facts disagree.
5. Produce a patch plan or make scoped edits when requested.

## Output

```markdown
## Context Extraction

Source artifacts:

Durable facts:

Historical-only notes:

Conflicts:

Files to update:

Proposed changes:

Human confirmation needed:
```

## References

Read `references/demo-run.md` for the first ai-context-summary example.
