---
name: gj-mr-review
description: Review GitLab merge requests for workflow compliance, code risks, test and documentation gaps, and merge readiness. Use when an MR is opened, marked ready, has review feedback, or needs a decision-ready report before a human chooses whether to merge.
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
3. Match changed paths against `.gj/workflow.yml`.
4. Load relevant module context from `.gj/context.yml`.
5. Check documentation impact:
   - MR description lists docs changed or explains why none are needed.
   - PRD/design/prototype/solution/test/release docs are updated when durable
     facts changed.
   - `docs/context`, `docs/modules`, ADRs, or `ai-context-summary.md` are updated
     when long-term AI context changed.
6. Review code for bugs, regressions, missing tests, and missing docs.
7. Check merge readiness: open non-draft MR, successful head pipeline, resolved
   discussions, valid flow evidence, linked Issue when required, test evidence,
   and rollback readiness.
8. Lead with findings ordered by severity. Keep summaries secondary.
9. Stop at the human gate. Never approve, merge, deploy, force, skip CI, or
   bypass unresolved discussions.

## Output

```markdown
## MR Review

Findings:

Workflow policy:

Risk paths:

Test gaps:

Documentation gaps:

Context updates needed:

Merge readiness:

Open questions:

Summary:
```

## References

- Read `references/demo-run.md` for the first MR review example.
- Read `references/gitlab-readiness.md` when live MR and pipeline evidence is
  needed.
