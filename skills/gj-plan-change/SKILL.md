---
name: gj-plan-change
description: Plan GitLab work at the depth required by its flow label. Use when a requirement, feature, small change, bug, or hotfix needs acceptance criteria, technical approach, task boundaries, test coverage, documentation impact, rollout, or rollback before implementation.
---

# GJ Plan Change

## Workflow

1. Read the work item, current labels, `.gj/context.yml`, and known
   constraints. Load only `always_load`, modules matched by expected paths, and
   feature docs linked by the work item. When present, use
   `docs/standards/12-context-governance.md` as the
   document lifecycle and content standard.
2. Resolve exactly one flow label. Recommend a label when missing, but wait for
   human confirmation before treating it as selected.
3. Scale the plan to the selected flow:
   - `flow::fast`: state the change, non-goals, affected files, self-test, and
     documentation impact. Do not create extra planning Issues by default.
   - `flow::standard`: clarify acceptance criteria and non-goals; document the
     technical approach, interface/data/permission impact, risks, tests,
     rollout, rollback, and independently reviewable tasks.
   - `flow::hotfix`: capture severity, impact, mitigation, smallest safe fix,
     minimum review, release validation, rollback, and mandatory follow-up.
4. Match changed or expected paths against `.gj/workflow.yml`. Upgrade Fast to
   Standard or Hotfix when the minimum flow requires it.
5. Plan the target version independently from flow when the work will be
   released. Use the configured SemVer policy and compatibility impact to
   recommend Major, Minor, or Patch, then link the Requirement Issue and GitLab
   Milestone. Treat this as `Target release`, not a released version. Do not
   bump project manifests or create a Tag during feature planning.
6. Split work only when separate ownership, dependencies, or review boundaries
   make additional Issues useful. Keep Requirement or Hotfix as the main work
   item. A Solution, Task, or Test Issue records separately tracked work; it
   never replaces the repository solution, test plan, or other durable docs.
7. Cover happy, failure, permission, regression, and release-validation paths
   according to risk. Failed checks become Bug Issues rather than hidden notes.
8. Decide documentation by impact first, then apply the selected flow depth:
   - create or update a PRD when product behavior, rules, permissions, or
     acceptance criteria change;
   - create or update product design/prototype records only when interaction or
     UI states matter;
   - create or update a technical solution when architecture, compatibility,
     rollout, monitoring, or rollback decisions are needed;
   - update the machine-readable contract and
     `docs/technical/apis/<domain>.md` when API/event structure or semantics
     change;
   - update schema/migrations and `docs/technical/database/<domain>.md` when
     persistent data structure, meaning, migration, or recovery changes;
   - create an ADR only for a lasting cross-boundary technical trade-off, then
     freeze it after confirmation;
   - create or update a test plan when acceptance or regression coverage is not
     trivial.
   Add Source Issue, Target release/Milestone, and direct document links to the
   applicable feature documents. Use semantic filenames and start new files
   from `.gj/doc-templates/`; never leave a template-named file in the project
   fact directories. Update an existing capability or domain document in place
   instead of creating versioned copies. When lasting facts are unresolved,
   leave them as `draft`; after the relevant human gate, record the confirmer
   and use `confirmed`. This status does not claim production deployment.
   For every API or database decision, name the executable source path (or a
   concrete `TBD` path with an owner) beside the explanatory Markdown path in
   the plan and documentation decision. Do not accept "update the schema" as a
   complete document action without locating both facts.
9. End with a documentation decision table containing path, action, triggering
   fact, stage/status, and confirmer/follow-up. Use only `create`, `update`,
   `no-change`, or `follow-up`; a follow-up requires an Issue, owner, and due
   date. Do not create a separate documentation task by default.

## Output

```markdown
## Change Plan

Flow and reason:
Target release / Milestone and SemVer reason:
Goal and non-goals:
Acceptance criteria:
Technical approach:
Impact and risk:
Tasks and dependencies:
Test coverage:
Documentation impact:
Documentation decisions (path / action / triggering fact / stage and status / confirmer or follow-up):
Rollout and rollback:
Human confirmation needed:
Ready to implement when:
```

## References

- Read `references/requirement-example.md` when requirements are ambiguous.
- Read `references/solution-example.md` for a Standard technical plan.
- Read `references/split-example.md` before creating multiple Issues.
- Read `references/test-example.md` when acceptance or regression risk matters.
