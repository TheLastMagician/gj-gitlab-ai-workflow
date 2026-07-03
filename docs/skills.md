# Skills

The project ships a complete workflow skill set. Install them with:

```powershell
python scripts/install_skills.py --force
```

## Workflow Mapping

| Workflow stage | Skill | Purpose |
| --- | --- | --- |
| Bootstrap | `gj-workflow-bootstrap` | Install labels, templates, AI config, docs, CI, and preflight checks. |
| Existing project map | `gj-codebase-map` | Map codebase facts into docs/codebase, docs/context, docs/modules, and context-index drafts. |
| Triage | `gj-workflow-triage` | Route work to standard, small change, bug fix, or hotfix flow. |
| Requirement | `gj-requirement-refine` | Clarify requirements, acceptance criteria, non-goals, risks, and DoR. |
| Solution | `gj-solution-plan` | Draft technical solution, impact, risks, tests, rollout, and rollback. |
| Split | `gj-issue-split` | Create traceable development, test, release, and follow-up Issues. |
| Development | `gj-dev-context` | Load focused implementation context before coding. |
| Review | `gj-mr-review` | Review MR policy, risk paths, code risks, tests, and context updates. |
| Merge | `gj-merge-assist` | Check merge readiness and execute GitLab merge only after explicit human authorization. |
| Test | `gj-test-design` | Design acceptance, regression, permission, and release validation tests. |
| Bug fix | `gj-bug-fix` | Analyze defects, root cause, fix scope, and regression tests. |
| Hotfix | `gj-hotfix` | Guide urgent fixes with minimum safe checks and post-fix follow-up. |
| Release | `gj-release-prep` | Prepare release notes, rollout, rollback, and validation. |
| Retro | `gj-retro-learnings` | Extract retrospective lessons and improvement actions. |
| Context update | `gj-context-extract` | Update durable AI context, module docs, ADRs, and context index. |
| Next action | `gj-workflow-next` | Inspect state and choose the next skill/action. |

## Decision Boundary

AI can assist every role, including review, approval preparation, merge
operation support, human-authorized merge execution, and release preparation. It must not autonomously approve,
merge, deploy, or bypass human confirmation. The human role remains the decision
maker and accountable owner.
