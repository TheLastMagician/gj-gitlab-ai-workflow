---
name: gj-close-loop
description: Close completed GitLab work by capturing lessons and refreshing durable project context. Use after an MR, bug fix, hotfix, release, or milestone when current-state, module docs, ADRs, context indexes, release evidence, or process follow-ups may need updates.
---

# GJ Close Loop

## Workflow

1. Read the completed work item, MR, pipeline and test evidence, release notes,
   bugs, follow-ups, `.gj/context.yml`, and relevant current project documents.
2. Scale closure to the flow:
   - Fast: record the result and update durable docs only if behavior changed.
   - Standard: summarize delivery, decisions, tests, friction, and durable
     context updates.
   - Hotfix: require root cause, regression coverage, documentation repair,
     risk follow-ups, and a short retro after the immediate fix.
3. Separate current durable facts from history, hypotheses, and superseded
   decisions.
4. Re-run the durable-impact classification across product, interaction,
   API/event, database, architecture/ADR, module rule, test baseline, release,
   and runtime state. Update the smallest applicable set of current documents
   and `.gj/context.yml`. Only update `current-state.md` for cross-project or
   deployed-environment facts. Keep process history in GitLab and change
   history in Git instead of copying either into repository archives.
5. After a release or deployment, distinguish planned from actual state. Update
   the release note and `docs/context/current-state.md` with the released Tag,
   commit SHA, Pipeline, environment, deployment time, post-release validation,
   and rollback result. Never claim a Milestone or untagged commit is released.
6. Preserve conflicts and ask for human confirmation instead of inventing a
   single truth.
7. Remove superseded current facts instead of retaining deprecation sections;
   Git and frozen evidence provide history.
8. Output a documentation decision table with path, action, triggering fact,
   stage/status, and confirmer/follow-up. Every follow-up includes an Issue,
   owner, and due date.
9. Create tracked improvement items for unresolved defects or process changes.

## Output

```markdown
## Close Loop

Completed scope:
Evidence:
Released Tag / SHA / Pipeline / deployed environments:
What worked or failed:
Durable facts:
Historical-only notes:
Files updated:
Documentation impact:
Documentation decisions (path / action / triggering fact / stage and status / confirmer or follow-up):
Follow-up Issues:
Human confirmation needed:
Closure status:
```

## References

- Read `references/retro-example.md` for milestone learning extraction.
- Read `references/context-example.md` for durable-versus-historical context.
