---
name: gj-workflow-next
description: Accept a new requirement or inspect a GitLab inbox or active work item, recommend the flow label, and choose the next workflow action. Use when a user brings new work, asks what is assigned to them, what to do next, which flow to use, why work is blocked, or how an Issue, MR, discussion, or pipeline should be routed.
---

# GJ Workflow Next

## Workflow

1. Identify whether the input is a new requirement or existing GitLab work.
   For a new requirement, capture the goal and known constraints, then route to
   `gj-plan-change` before creating an Issue. Create or label the Issue only
   after a human confirms the requirement and flow; without GitLab write access,
   return a complete Issue draft instead.
2. Identify the actor and project. When the request is about personal work,
   use `scripts/gitlab_api.py` when present to fetch GitLab Todos, assigned
   Issues/MRs, review requests, mentions, discussions, and related failed or
   pending pipelines. A configured GitLab connector is an optional alternative.
3. Inspect repository status, the selected work item, current labels, changed or
   expected paths, pipeline state, and workflow docs.
4. Resolve the flow:
   - Fast for low-risk, local work with bounded validation.
   - Standard for business rules, permissions, money, APIs, databases,
     cross-module work, or unclear validation.
   - Hotfix for urgent production, security, or data risk.
   Recommend exactly one `flow::*` label; a human confirms it before coding.
5. Resolve version planning separately from flow. Read `.gj/workflow.yml`
   `versioning` when present. For new releasable work, recommend a Target
   release and matching GitLab Milestone from compatibility impact and the
   latest released Tag. A human confirms it; do not bump a manifest, create a
   Tag, or describe a Milestone as already released.
6. Identify the current stage and route to one of the small set of downstream
   skills: `gj-plan-change`, `gj-develop-change`, `gj-mr-review`,
   `gj-release-readiness`, or `gj-close-loop`.
7. Check blockers:
   - missing or conflicting `flow::*` label.
   - missing Issue or acceptance criteria.
   - missing solution review.
   - failing or pending pipeline.
   - unresolved review comments.
   - a high-risk path incorrectly using `flow::fast`.
   - missing context update.
   - missing documentation impact answer or required repo docs.
8. Identify assignment, reviewer, mention, due-date, target-release/Milestone,
   and documentation gaps. Treat Requirement/Hotfix as the main work item;
   recommend Solution, Task, or Test Issues only for independently owned or
   tracked work, never as substitutes for repository documentation.
9. Keep the answer action-oriented and include evidence links or file paths.
   Read-only inspection is the default; only set labels or hand off work after
   the human confirms the action.

## Output

```markdown
## Workflow Next

Current stage:

Flow recommendation:

Target release / Milestone recommendation:

Evidence:

Blockers:

Recommended next skill:

Next action:

Issue action (create after confirmation or return draft):

Documentation impact:

Human confirmation needed:

Done when:
```

## References

- Read `references/gitlab-inbox.md` when querying GitLab API state.
- Read `references/demo-run.md` for the first-run stage trace.
