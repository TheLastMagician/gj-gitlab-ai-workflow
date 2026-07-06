# gj-gitlab-ai-workflow

GitLab CE friendly AI delivery workflow for teams that want requirements,
planning, review, testing, release, and retrospective artifacts to stay
traceable in GitLab while AI assistants work from a stable project context.

This repository packages the reusable workflow assets and Codex skills. The
included demo artifacts show how the workflow was exercised on a small order
approval project before the stable actions were extracted into skills.

## What Is Included

- GitLab issue and merge request templates.
- AI context templates under `templates/ai` and `templates/docs`.
- Product, technical, QA, release, and documentation standards/templates.
- Role-map and handoff standards for GitLab assignee/reviewer/@mention ownership.
- A target-project CI/CD template: policy, workflow asset check, test, and
  release dry run.
- An orchestrator skeleton for GitLab webhook command routing.
- A small demo project plus a recorded end-to-end demo run.
- A complete workflow skill set derived from the demo artifacts.
- A GitLab API inbox skill that reads Todos, assignments, review requests, and mentions.
- Human-authorized merge assistance that checks readiness before executing a merge.
- Dev/test environment deployment policy with shared test locks and human confirmation.

## Current Run

The first run is recorded in `examples/demo-run/`.

The intentional order is:

1. Bootstrap the GitLab workflow assets.
2. Run the order approval demo through product, tech lead, developer, reviewer,
   QA, DevOps, and PM roles.
3. Record inputs, outputs, failure points, and human confirmations.
4. Extract stable actions into workflow skills.
5. Re-run with those skills before expanding automation.

## Quickstart

See `docs/quickstart.md` for the local bootstrap flow and `docs/workflow.md` for
the workflow contract. See `docs/cicd.md` for the pipeline stages and runner
requirements. See `docs/skills.md` for the complete skill-to-workflow mapping.

Install the skills into Codex:

```powershell
python scripts/install_skills.py --force
```

Install the GitLab workflow assets into another repository:

```powershell
python scripts/install_workflow.py --target C:\path\to\your-project
```

## Target Project CI/CD

The GitLab CI template installed into target projects is a business-project
pipeline:

```text
policy -> workflow -> test -> release
```

It does not contain `skill_validate` or `package_open_source`. Skills are used by
people through Codex to help with requirement refinement, review, QA, release
prep, and retrospectives; they are not pipeline stages in every business
project.

Personal workflow inboxes are read from GitLab API state. Enterprise WeCom,
email, or similar company channels can deliver GitLab notifications, but this
project does not require a separate email inbox reader.

GitLab comments are the discussion trail. Repository docs are the durable source
for PRDs, product designs, prototypes, technical solutions, test plans, release
notes, and long-term AI context.

Use a GitLab Runner with Docker executor and `python:3.12-slim` for the most
repeatable result.

## Safety Note

Do not commit project-local API helper files, tokens, private GitLab settings,
or production data. The workflow assumes AI outputs are written back as GitLab
comments or repository docs, but secrets must stay outside prompts and commits.
