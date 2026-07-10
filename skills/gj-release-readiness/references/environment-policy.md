# Environment Deployment Policy

Use this reference when deciding whether to deploy a branch or MR to a non-production environment.

## Default Model

- Dev is fast and may be automatic.
- Shared test is stable and requires human confirmation.
- Production is outside this skill and belongs to release governance.

## Required Record For Shared Test

Before deploying to shared test, record:

- target environment
- source branch or MR
- commit SHA
- pipeline URL and status
- deploy requester
- deploy approver when different
- previous deployed version
- rollback command or rollback target
- expected QA owner and test window

After deploying, record:

- deployment time
- deployed version
- deployment job URL
- smoke result
- QA status
- whether the environment should be restored to baseline

## GitLab CI Pattern

```yaml
stages:
  - policy
  - workflow
  - test
  - build
  - deploy
  - release

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
    - if: '$CI_COMMIT_BRANCH =~ /^release\\//'
  resource_group: test-env
  environment:
    name: test
  script:
    - ./scripts/deploy_test.sh
```

If the project has only one test environment, do not deploy every MR branch there automatically.
