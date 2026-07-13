# CI/CD Flow

The installed pipeline validates the target business project and its workflow
assets.

## Stages

| Stage | Job | Purpose |
| --- | --- | --- |
| policy | `policy_check` | Require exactly one `flow::*` MR label; check MR content, changed-file risk paths, and committed secrets. |
| workflow | `workflow_assets_check`, optional `validate_role_map` / `context_freshness_check` | Check installed assets; enable role validation explicitly and run context checks only for relevant changes. |
| test | `smoke_check` | Run the target project smoke test command. |
| deploy | `deploy_dev`, `deploy_test` | Optional project-specific deployment jobs. Dev may be automatic; shared test must be manual and locked. |
| release | optional `release_dry_run` | On tags or manual default-branch pipelines, emit a release checklist artifact. |

## Runner Requirement

The demo should run with a project runner using Docker executor and
`python:3.12-slim`. A shell runner on Windows exposed a GitLab Runner PowerShell
working-directory issue, so Docker executor is the recommended path for
repeatable target-project validation.

## GitLab CE Enforcement

- Protect the default branch and limit who can merge to it.
- Require a successful Pipeline before merge.
- Low-risk Fast MRs do not require an additional approval count.
- High-risk changed files cannot use `flow::fast`; Standard/Hotfix evidence and
  a human merge decision are required.
- CODEOWNERS and an optional Approve action may guide review, but the workflow
  uses GitLab permissions and merge records as the source of truth.

If Docker Hub access is restricted but `python:3.12-slim` is already available
locally, configure the runner with:

```toml
[runners.docker]
  image = "python:3.12-slim"
  pull_policy = "if-not-present"
```

## Expected Pipeline

```text
Fast MR: policy -> workflow -> test
Release: policy -> workflow -> test -> deploy(optional) -> release
```

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
