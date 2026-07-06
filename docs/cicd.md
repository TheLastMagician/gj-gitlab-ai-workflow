# CI/CD Flow

The installed pipeline is meant for target business projects. It should validate
the project and the installed workflow assets; it should not package this
workflow project.

## Stages

| Stage | Job | Purpose |
| --- | --- | --- |
| policy | `policy_check` | Check MR description, documentation impact, owner ack from `.ai/rule-map.yml`, risk paths, and committed secrets. |
| workflow | `workflow_assets_check`, `validate_role_map` | Check that `.ai`, GitLab templates, context/docs templates, policy scripts, and role ownership are installed. |
| test | `smoke_check` | Run the target project smoke test command. |
| deploy | `deploy_dev`, `deploy_test` | Optional project-specific deployment jobs. Dev may be automatic; shared test must be manual and locked. |
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
policy -> workflow -> test -> deploy(optional) -> release
```

`skill_validate` belongs to this workflow project's own maintenance checks, not
to every installed target project. `package_open_source` also belongs only to a
future release process for this workflow project.

## Environment Deployment Policy

The template does not deploy by default because deploy scripts are project
specific. Add deployment jobs only after the project has a real deploy command.

Recommended defaults:

- MR branches may auto-deploy only to isolated dev/review environments.
- `develop` or `integration` may auto-deploy to dev.
- Shared `test` or `staging` must be `when: manual`.
- Shared environments must use `resource_group`, for example `resource_group: test-env`.
- Every shared test deploy must record branch, MR, commit SHA, pipeline URL,
  deployer, previous version, rollback target, and QA owner.

Example:

```yaml
deploy_dev:
  stage: deploy
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
    - if: '$CI_MERGE_REQUEST_IID'
  environment:
    name: dev/$CI_COMMIT_REF_SLUG
    auto_stop_in: 2 days
  script:
    - ./scripts/deploy_dev.sh

deploy_test:
  stage: deploy
  when: manual
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
    - if: '$CI_COMMIT_BRANCH =~ /^release\//'
  resource_group: test-env
  environment:
    name: test
  script:
    - ./scripts/deploy_test.sh
```

## Artifacts

- `build/release-dry-run.md`
