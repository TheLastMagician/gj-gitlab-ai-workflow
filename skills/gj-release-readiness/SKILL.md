---
name: gj-release-readiness
description: Assess and prepare GitLab dev, test, staging, and production release readiness. Use when a branch, MR, tag, or milestone needs environment policy checks, pipeline and test evidence, release notes, rollout, rollback, monitoring, or explicit human release decisions.
---

# GJ Release Readiness

## Boundaries

- AI prepares evidence and instructions; a human decides and triggers shared
  environment or production deployment.
- MR branches may deploy automatically only to isolated dev/review environments
  already permitted by project CI.
- Shared test/staging requires a lock such as GitLab `resource_group`, a known
  current occupant, a rollback target, and explicit human confirmation.
- MR pipelines must not create production release jobs.

## Workflow

1. Identify the target environment and source branch, MR, tag, commit SHA, and
   latest pipeline.
2. Read the release Issue or milestone, included MRs, test results, known risks,
   environment policy, CI rules, and deploy scripts.
3. Verify pipeline status, unresolved discussions, test evidence, config/data/
   permission changes, environment isolation or lock, and rollback target.
4. Prepare or update `docs/releases/<version>.md` and link the applicable test
   report. Record branch, SHA, pipeline, target, owner, time window, and rollback.
5. Produce rollout, monitoring, validation, and recovery steps.
6. Stop at the human gate. Do not approve, merge, tag, or deploy.

## Output

```markdown
## Release Readiness

Target and source:
Decision:
Pipeline and tests:
Included changes:
Config / data / permission impact:
Environment isolation or lock:
Release note and documentation impact:
Rollout and monitoring:
Rollback target and steps:
Post-release validation:
Human confirmation needed:
```

`Decision` is one of `not_ready`, `ready_for_isolated_dev`,
`ready_for_shared_environment_confirmation`, or
`ready_for_release_confirmation`.

## References

- Read `references/environment-policy.md` for GitLab environment locks and
  deployment record fields.
- Read `references/release-example.md` for a release dry-run example.
