---
name: gj-workflow-next
description: Decide the next best action in an installed GitLab AI workflow. Use when a user asks what to do next, a workflow is stuck, a milestone needs routing, or the current Issue/MR/pipeline state must be inspected to choose the next skill, GitLab action, human confirmation, or validation step.
---

# GJ Workflow Next

## Workflow

1. Inspect current repository status, GitLab MR/Issue/pipeline state, and workflow docs.
2. Identify the active workflow stage: triage, requirement, solution, split, development, review, test, release, retro, or context update.
3. Check blockers:
   - missing Issue or acceptance criteria.
   - missing solution review.
   - failing or pending pipeline.
   - unresolved review comments.
   - missing owner ack.
   - missing context update.
4. Recommend the next skill and concrete action.
5. Keep the answer action-oriented and include evidence links or file paths.

## Output

```markdown
## Workflow Next

Current stage:

Evidence:

Blockers:

Recommended next skill:

Next action:

Human confirmation needed:

Done when:
```

## References

Read `references/demo-run.md` for the full first-run stage trace.
