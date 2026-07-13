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
   - MR description or Skill result includes a documentation decision table
     with path, action, reason, and status/confirmer;
   - each action is `create`, `update`, `no-change`, or `follow-up`, and every
     follow-up has an Issue, owner, and due date;
   - the table agrees with the actual diff and changed behavior;
   - PRD/design/prototype/solution/test/release docs are updated when durable
     facts changed.
   - `docs/context`, `docs/modules`, ADRs, or `ai-context-summary.md` are updated
     when long-term AI context changed.
6. Check version traceability: the Issue, MR, and feature docs use the same
   Target release/Milestone; a normal feature MR does not create a Tag or bump
   project manifests without explicit release scope. For release-preparation
   MRs, verify the final SemVer, release note path, included work, tests, and
   rollback evidence.
7. Review code for bugs, regressions, missing tests, and missing docs.
8. Check merge readiness: open non-draft MR, successful head pipeline, resolved
   discussions, valid flow evidence, linked Issue when required, test evidence,
   and rollback readiness.
9. Lead with findings ordered by severity. Keep summaries secondary.
10. Stop at the human gate. Never approve, merge, deploy, force, skip CI, or
   bypass unresolved discussions.

## Output

```markdown
## MR Review

Findings:

Workflow policy:

Risk paths:

Target release / version traceability:

Test gaps:

Documentation gaps:

Documentation decision verification:

Context updates needed:

Merge readiness:

Open questions:

Summary:
```

## References

- Read `references/demo-run.md` for the first MR review example.
- Read `references/gitlab-readiness.md` when live MR and pipeline evidence is
  needed.
