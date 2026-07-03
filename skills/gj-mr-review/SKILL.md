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
5. Review code for bugs, regressions, missing tests, and missing docs.
6. Lead with findings ordered by severity. Keep summaries secondary.

## Output

```markdown
## MR Review

Findings:

Workflow policy:

Risk paths:

Test gaps:

Context updates needed:

Open questions:

Summary:
```

## References

Read `references/demo-run.md` for the first MR review example.
