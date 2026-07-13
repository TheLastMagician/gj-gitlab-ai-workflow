# Demo Run Log: 订单审批流 v1.0

Run date: 2026-07-03

GitLab project: `zengqinglin/gj-workflow-demo`

Milestone: [订单审批流 v1.0](https://gitlab.example.com/acme/gj-workflow-demo/-/milestones/1)

Merge request: [!1 feat(workflow): 初始化 GitLab AI 工作流骨架](https://gitlab.example.com/acme/gj-workflow-demo/-/merge_requests/1)

## End-to-End Trace

| Step | Role | Input | Output | Failure / Friction | Human Confirmation |
| --- | --- | --- | --- | --- | --- |
| 1 | DevOps / Codex | Local repo and workflow doc | Labels, templates, `.ai`, CI files | API helper originally pointed at a different project before user fixed it | Confirm API ProjectId matches `origin` before writes |
| 2 | Product | Rough need: order approval | Requirement Issue #2 and AI clarification comment | Approval owner source and amount threshold unclear | Product confirms v1.0 excludes amount threshold |
| 3 | Tech Lead | Requirement Issue #2 | Solution Issue #3 | Permission risk needs owner attention | Tech Lead accepts minimal state machine for demo |
| 4 | Tech Lead | Requirement + solution | Task Issue #4, Test Issue #5, Release Issue #7 | Task split is easy to overdo for a tiny demo | Keep Web API, DB, notification out of scope |
| 5 | Developer | Task Issue #4 | Demo service and tests | Initial implementation missed self-approval rule | Developer adds regression test and fix |
| 6 | Reviewer | MR description and changed files | AI review notes | Policy checks the minimum flow for changed paths | Reviewer checks risk, test, rollback, and merge readiness |
| 7 | QA | Acceptance criteria | QA failure and Bug Issue #6 | Failure must not be hidden in test report | QA upgrades failure to Bug Issue |
| 8 | Developer | Bug Issue #6 | `_ensure_not_self_approval` and regression test | Need same rule in approve and reject | Reviewer confirms both paths |
| 9 | DevOps | Release Issue #7 | Release and rollback checklist | Protected branch settings require GitLab UI/admin confirmation | DevOps confirms before merge |
| 10 | PM | All Issues and MR notes | Retro Issue #8 and AI context summary | Skill drafts should not be written before examples exist | PM approves first-batch draft extraction only |

## Exposed Friction

1. GitLab API helper configuration can drift from `git remote`.
2. Local token helper files need explicit ignore rules before opening source.
3. GitLab label and Issue creation needs idempotency to avoid duplicate demo runs.
4. Skill initialization metadata has strict length constraints.
5. QA failures must become Bug Issues, not prose hidden in test reports.
6. CI policy checks cannot see untracked local secret files; commit hygiene still matters.
7. On Windows, the skill metadata generator can fail on UTF-8 Chinese SKILL.md
   files unless `--name` is passed or the script reads with UTF-8 explicitly.
8. Python dataclasses fail under dynamic import unless the imported module is
   registered in `sys.modules` before `exec_module`.
9. GitLab pipeline can remain pending when no project/shared runner is active.
   A temporary shell runner picked up the job but failed under Windows
   PowerShell working-directory handling. The stable path for this demo is a
   Docker executor runner with `python:3.12-slim`.

## CI/CD Pipeline

The demo pipeline was expanded to show the whole delivery flow:

```text
policy -> workflow -> test -> package -> release
```

Expected jobs:

- `policy_check`
- `workflow_contract`
- `smoke_check`
- `package_open_source`
- `release_dry_run`

Skill validation runs inside `package_open_source`, because skills are part of
the reusable open-source package rather than a standalone business workflow
stage.

Validation result:

- Pipeline: https://gitlab.example.com/acme/gj-workflow-demo/-/pipelines/19841
- Status: success
- Note: initial `policy_check` job failed because Docker Runner tried to pull
  `python:3.12-slim` from Docker Hub with `pull_policy=always`. After setting
  the temporary runner to `pull_policy=if-not-present`, the retried job and all
  downstream jobs succeeded.

## Stable Actions Worth Extracting

- Validate GitLab project identity before any write.
- Bootstrap labels, templates, `.ai`, docs, CI, and CODEOWNERS.
- Use triage to recommend one `flow::fast`, `flow::standard`, or
  `flow::hotfix` label for human confirmation.
- Convert rough requirements into missing questions and acceptance criteria.
- Review MR descriptions against workflow policy.
- Convert QA failures into Bug Issues with root cause and regression scope.
- Close every iteration with `ai-context-summary.md`.
