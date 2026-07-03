# CI/CD Flow

The installed pipeline is meant for target business projects. It should validate
the project and the installed workflow assets; it should not package this
workflow project.

## Stages

| Stage | Job | Purpose |
| --- | --- | --- |
| policy | `policy_check` | Check MR description, owner ack, risk paths, and committed secrets. |
| workflow | `workflow_assets_check` | Check that `.ai`, GitLab templates, context docs, and policy scripts are installed. |
| test | `smoke_check` | Run the target project smoke test command. |
| release | `release_dry_run` | Emit a business release checklist artifact. |

## Runner Requirement

The demo should run with a project runner using Docker executor and
`python:3.12-slim`. A shell runner on Windows exposed a GitLab Runner PowerShell
working-directory issue, so Docker executor is the recommended path for
repeatable target-project validation.

If Docker Hub access is restricted but `python:3.12-slim` is already available
locally, configure the runner with:

```toml
[runners.docker]
  image = "python:3.12-slim"
  pull_policy = "if-not-present"
```

## Expected Pipeline

```text
policy -> workflow -> test -> release
```

`skill_validate` belongs to this workflow project's own maintenance checks, not
to every installed target project. `package_open_source` also belongs only to a
future release process for this workflow project.

## Artifacts

- `build/release-dry-run.md`
