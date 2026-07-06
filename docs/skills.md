# Skills

The project ships a complete workflow skill set. Install them with:

```powershell
python scripts/install_skills.py --force
```

## Workflow Mapping

| Workflow stage | Skill | Purpose |
| --- | --- | --- |
| Bootstrap | `gj-workflow-bootstrap` | Install labels, templates, AI config, docs, CI, and preflight checks. |
| Inbox | `gj-workflow-inbox` | Inspect GitLab Todos, assignments, review requests, mentions, and route each item to the right skill. |
| Existing project map | `gj-codebase-map` | Map codebase facts into docs/codebase, docs/context, docs/modules, and context-index drafts. |
| Triage | `gj-workflow-triage` | Route work to standard, small change, bug fix, or hotfix flow. |
| Requirement | `gj-requirement-refine` | Clarify requirements, acceptance criteria, non-goals, risks, and DoR. |
| Solution | `gj-solution-plan` | Draft technical solution, impact, risks, tests, rollout, and rollback. |
| Split | `gj-issue-split` | Create traceable development, test, release, and follow-up Issues. |
| Development | `gj-dev-context` | Load focused implementation context before coding. |
| Review | `gj-mr-review` | Review MR policy, risk paths, code risks, tests, and context updates. |
| Merge | `gj-merge-assist` | Check merge readiness and execute GitLab merge only after explicit human authorization. |
| Test | `gj-test-design` | Design acceptance, regression, permission, and release validation tests. |
| Environment deploy | `gj-env-deploy-assist` | Plan dev/test deployment, environment locks, version records, and human confirmation. |
| Bug fix | `gj-bug-fix` | Analyze defects, root cause, fix scope, and regression tests. |
| Hotfix | `gj-hotfix` | Guide urgent fixes with minimum safe checks and post-fix follow-up. |
| Release | `gj-release-prep` | Prepare release notes, rollout, rollback, and validation. |
| Retro | `gj-retro-learnings` | Extract retrospective lessons and improvement actions. |
| Context update | `gj-context-extract` | Update durable AI context, module docs, ADRs, and context index. |
| Next action | `gj-workflow-next` | Inspect state and choose the next skill/action. |

## Decision Boundary

AI can assist every role, including review, approval preparation, merge
operation support, human-authorized merge execution, and release preparation. It must not autonomously approve,
merge, overwrite shared test/staging, deploy, or bypass human confirmation. The human role remains the decision
maker and accountable owner.

## Inbox And Notifications

`gj-workflow-inbox` uses GitLab API state as the inbox source: Todos, assigned
Issues, assigned MRs, review-requested MRs, mentions, unresolved discussions,
and failed pipelines. It does not read email or Enterprise WeCom directly.

Bootstrap owns role setup through `.ai/role-map.yml`. Handoffs should assign the
right person in GitLab and mention them in a comment so GitLab can create Todos
and send whatever company notification channel is configured.

## Documentation Impact

Core workflow skills include a documentation impact check. The expected rule is:
GitLab Issues and MR comments record discussion; repository docs record durable
conclusions.

Common routing:

| Durable change | Document target |
| --- | --- |
| Product behavior or acceptance criteria | `docs/product/requirements/<feature>.md` |
| UI, user flow, screen state, copy, prototype | `docs/product/designs/<feature>.md`, `docs/product/prototypes/<feature>.md` |
| Architecture, API, data, permission, rollout, rollback | `docs/technical/solutions/<feature>.md` |
| Acceptance, regression, permission, release validation | `docs/qa/test-plans/<feature>.md`, `docs/qa/test-reports/<feature>.md` |
| User-visible release scope or rollback | `docs/releases/<version>.md` |
| Long-term AI context | `docs/context`, `docs/modules`, `.ai/context-index.yml`, `docs/iterations/*/ai-context-summary.md` |
