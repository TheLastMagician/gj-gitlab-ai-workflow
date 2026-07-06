---
name: gj-mr-review
description: Review GitLab merge requests for workflow compliance, risk paths, code issues, test coverage, rollback readiness, and AI context updates. Use when an MR is opened, marked ready, or explicitly requested for AI review.
---

# GJ MR Review

## Workflow

1. Read MR title, description, linked Issues, diff, pipeline result, and comments.
2. Check required MR sections:
   - linked Issue.
   - change summary.
   - self-test.
   - risks.
   - rollback.
   - database/config changes.
   - AI usage.
3. Match changed paths against `.ai/rule-map.yml`.
4. Load relevant module context from `.ai/context-index.yml`.
5. Check documentation impact:
   - MR description lists docs changed or explains why none are needed.
   - PRD/design/prototype/solution/test/release docs are updated when durable
     facts changed.
   - `docs/context`, `docs/modules`, ADRs, or `ai-context-summary.md` are updated
     when long-term AI context changed.
6. Review code for bugs, regressions, missing tests, and missing docs.
7. Lead with findings ordered by severity. Keep summaries secondary.

## Output

```markdown
## MR Review

Findings:

Workflow policy:

Risk paths:

Test gaps:

Documentation gaps:

Context updates needed:

Open questions:

Summary:
```

## References

Read `references/demo-run.md` for the first MR review example.
