# CI/CD Flow

The installed `.gitlab/gj-workflow-ci.yml` is included by the target business
project. GJ jobs own their Python image and use GitLab's built-in `.pre`/`.post`
stages, so existing project images, stages, and defaults are not replaced.

## Stages

| Stage | Job | Purpose |
| --- | --- | --- |
| `.pre` | `policy_check` | Block on one `flow::*` label, Standard/Hotfix Issue links, changed-file risk paths, and newly committed secrets; warn on MR template completeness. |
| `.pre` | advisory `workflow_assets_check`, optional `validate_role_map` | Report workflow setup issues without blocking normal MRs. Context audits are run manually when needed. |
| `.pre` | `smoke_check` | Run the target project smoke test command. |
| project-owned | `deploy_dev`, `deploy_test` | Optional project-specific deployment jobs. Dev may be automatic; shared test must be manual and locked. |
| `.post` | advisory `release_dry_run` | On tags or manual default-branch pipelines, emit a release checklist artifact for human confirmation. |

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
MR hard gates: policy -> test
Advisory jobs: workflow assets / release dry run
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
