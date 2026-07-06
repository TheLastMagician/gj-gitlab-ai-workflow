---
name: gj-env-deploy-assist
description: Plan, verify, and guide GitLab dev/test environment deployments with branch rules, environment locks, version records, rollback notes, and human confirmation. Use when a human asks whether a branch or MR can deploy to dev, shared test, staging, or another non-production environment, especially when only one shared test environment exists.
---

# GJ Env Deploy Assist

## Overview

Guide environment deployment decisions without assuming every project has multiple test environments. Keep dev fast, keep shared test stable, and require human confirmation before overwriting shared environments.

## Environment Policy

- Dev environments may be automatic if the project supports them.
- MR branches may deploy to isolated dev/review environments, not to shared test by default.
- Shared test/staging environments must be manual or queued.
- Shared environments must use an environment lock such as GitLab `resource_group`.
- Every shared environment deployment must record branch, commit SHA, MR, pipeline, deployer, time, and rollback target.
- AI may prepare or execute deployment commands only after explicit human authorization and project policy checks.
- Do not deploy to production from this skill. Route production release work to `gj-release-prep`.

## Branch Rules

Use these defaults unless the repository documents a stricter policy:

| Source | Dev deploy | Shared test deploy |
| --- | --- | --- |
| MR / feature branch | automatic only to isolated `dev/<ref>` or review app | no automatic deploy |
| `develop` / `integration` | automatic or manual dev deploy | manual deploy with lock |
| `release/*` | optional dev deploy | manual deploy with lock |
| tag / protected release | not required | manual deploy, release-gated |

## Workflow

1. Identify environment target: dev, review, test, staging, or production.
2. Identify source: branch, MR, tag, commit SHA, and latest pipeline.
3. Load project environment docs if present: `docs/standards/*environment*`, `docs/cicd.md`, `.gitlab-ci.yml`, deploy scripts, and release Issue.
4. For dev/review:
   - Confirm whether isolated environment naming exists.
   - Check latest pipeline/build status.
   - Allow automatic deployment only if CI rules already permit it.
5. For shared test/staging:
   - Check current occupant or last deployed version when available.
   - Check whether `resource_group` or another lock protects the environment.
   - Require explicit human confirmation before deploy.
   - Record rollback target before deploy.
6. If authorization is missing, output readiness and required confirmation.
7. Check documentation impact:
   - Update release note or deployment record when shared test/staging is
     overwritten.
   - Link test report or QA window for shared environment validation.
   - Update environment standard if the project discovers a new deploy rule.
8. If authorization is present and checks pass, execute only the project-approved deploy command or GitLab manual job trigger.
9. After deploy, report deployed version and follow-up QA/recovery actions.

## Readiness Output

```markdown
## Environment Deploy Readiness

Target environment:
Source:
Decision:

Checks:
- Pipeline/build:
- Environment type:
- Isolation:
- Lock/resource group:
- Current deployed version:
- Rollback target:
- Documentation impact:
- Human confirmation:
- Risk:

Recommended action:
Required confirmation:
```

`Decision` must be one of:

- `auto_dev_allowed`
- `manual_test_confirmation_required`
- `ready_after_human_confirmation`
- `deployed_after_explicit_human_authorization`
- `blocked_by_environment_policy`

## Explicit Confirmation

For shared test/staging, require wording that names target and source:

```text
Confirm deploy MR !12 commit <sha> to test.
Confirm deploy branch develop to test.
```

Ambiguous wording such as `deploy it if ready` is not enough.

## GitLab CI Guidance

Use `resource_group` for shared environments:

```yaml
deploy_test:
  stage: deploy
  when: manual
  resource_group: test-env
  environment:
    name: test
```

Use isolated environment names for MR/review dev deploys:

```yaml
deploy_dev:
  stage: deploy
  environment:
    name: dev/$CI_COMMIT_REF_SLUG
```

## References

Read `references/environment-policy.md` for the recommended GitLab CI pattern and deployment records.
