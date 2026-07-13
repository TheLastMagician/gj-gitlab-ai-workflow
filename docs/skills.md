# Skills

Install the complete workflow skill set from one GitHub source into Codex,
Claude Code, and OpenCode with:

```powershell
npx --yes skills@1.5.15 add https://github.com/TheLastMagician/gj-gitlab-ai-workflow --skill '*' -a codex -a claude-code -a opencode --copy -y
```

All agents consume the same `skills/*/SKILL.md` source. The Python fallback is
`python scripts/install_skills.py --agent all --project-root <project> --force`.
Every Skill uses the `gj-` namespace; GJ is the project abbreviation for
Chinese `公交`.

Daily work starts from `gj-workflow-next`; users do not need to memorize the
other names.

## The Eight Skills

| Stage | Skill | Purpose |
| --- | --- | --- |
| Bootstrap | `gj-workflow-bootstrap` | Install and verify labels, templates, AI config, docs, CI, and project gates. |
| Existing project map | `gj-codebase-map` | Map codebase facts into focused context and module documentation. |
| Route | `gj-workflow-next` | Read inbox/current state, recommend one flow label, and choose the next action. |
| Plan | `gj-plan-change` | Scale requirements, solution, task boundaries, tests, docs, rollout, and rollback to the flow. |
| Develop | `gj-develop-change` | Implement features, small changes, bugs, and hotfixes with focused context and tests. |
| Review | `gj-mr-review` | Review policy, code, tests, documentation, and merge readiness; stop at the human merge gate. |
| Release | `gj-release-readiness` | Prepare environment and release evidence, rollout, rollback, and validation; stop at the human deploy gate. |
| Close | `gj-close-loop` | Capture lessons and refresh durable project context after completed work. |

## Flow Depth

| Flow | Plan and delivery depth |
| --- | --- |
| `flow::fast` | Bounded change, self-test, documentation impact, MR, and review. No extra planning Issues by default. |
| `flow::standard` | Linked Issue, acceptance criteria, technical approach, risks, tests, rollout, rollback, and durable docs. |
| `flow::hotfix` | Incident impact, smallest safe fix, minimum review, release validation, rollback, and mandatory follow-up. |

The Issue template proposes a flow, a human confirms it before coding, the MR
uses the same single `flow::*` label, and CI validates the choice against
changed paths. Skills recommend and enforce the selected depth; they do not
decide business risk for the human.

## Comment Commands

The optional orchestrator exposes only these commands:

```text
/ai-next
/ai-plan
/ai-develop
/ai-review
/ai-release
/ai-close
```

`gj-workflow-bootstrap` and `gj-codebase-map` are invoked directly when needed.

## Decision Boundary

AI may inspect, draft, edit, test, and prepare decision evidence. It must not
autonomously approve, merge, tag, deploy, overwrite a shared environment, or
bypass protections. Humans confirm the flow label and make merge and release
decisions.

## Inbox And Notifications

`gj-workflow-next` uses GitLab API state as the inbox source: Todos, assigned
Issues/MRs, review requests, mentions, unresolved discussions, and failed
pipelines. Email or Enterprise WeCom may deliver notifications but is not a
workflow state source.

Handoffs should assign the responsible person in GitLab and mention them in a
comment so GitLab creates the expected Todo and notification.

## Documentation Impact

Every delivery Skill reports a documentation decision table with the target
path, one of `create` / `update` / `no-change` / `follow-up`, the triggering
fact, stage/status, and human confirmer or follow-up. A follow-up is valid only
with an Issue, owner, and due date. GitLab Issues and MR comments hold process;
repository docs hold durable conclusions.

Users do not need to invoke a separate documentation Skill. After durable facts
are confirmed, `gj-plan-change`, `gj-develop-change`,
`gj-release-readiness`, and `gj-close-loop` update their applicable documents
within the current change when repository writes are available. `gj-mr-review`
checks that those updates are present. If facts are unresolved or writes are
unavailable, the Skill returns an exact draft and a human confirmation item.
Current-fact documents are updated in place; versioned test/release evidence is
created per Tag and then frozen. Process history remains in GitLab and Git.

| Durable change | Document target |
| --- | --- |
| Product behavior or acceptance criteria | `docs/product/requirements/<capability>.md` |
| UI, user flow, screen state, copy, prototype | `docs/product/designs/<capability>.md`, `docs/product/prototypes/<capability>.md` |
| Architecture, permission, rollout, rollback | `docs/technical/solutions/<capability>.md`, ADR |
| API/event contract | machine schema + `docs/technical/apis/<domain>.md` |
| Database structure or meaning | schema/migration + `docs/technical/database/<domain>.md` |
| Acceptance, regression, permission baseline | `docs/qa/test-plans/<capability>.md` |
| Executed release validation | `docs/qa/test-reports/<tag>.md` |
| User-visible release scope or rollback | `docs/releases/<tag>.md` |
| Long-term AI context | `docs/context`, `docs/modules`, ADRs, `.gj/context.yml` |

Requirement or Hotfix is the main work item. Solution, Task, and Test Issues are
created only for separately owned or tracked work and never replace repository
documents. New document templates are installed under `.gj/doc-templates/`;
project fact directories contain only semantic files such as
`order-approval.md`, never generic template filenames.
API and database decisions name both the executable contract/schema/migration
path and its explanatory Markdown path so the two facts can be reviewed
together.

## Version Responsibilities

- `gj-workflow-next` recommends a Target release/GitLab Milestone separately
  from flow; a human confirms both.
- `gj-plan-change` links the Issue and feature documents to that target.
- `gj-develop-change` and normal MRs do not bump the repository version.
- `gj-release-readiness` locks the final SemVer, prepares per-Tag test/release
  evidence, and checks it before the human Tag decision.
- `gj-close-loop` records the actual Tag, SHA, Pipeline, environment, and
  deployment validation. A Milestone is never reported as released.

See `docs/versioning.md` and the installed
`docs/standards/13-versioning-standard.md`.
