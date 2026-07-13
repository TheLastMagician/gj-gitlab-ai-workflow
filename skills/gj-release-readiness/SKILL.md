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
3. Read `.gj/workflow.yml` versioning policy and determine the final SemVer from
   compatibility impact and the latest released Tag. Confirm the GitLab
   Milestone matches. This is the point where the version is locked.
4. Verify pipeline status, unresolved discussions, test evidence, config/data/
   permission changes, environment isolation or lock, and rollback target.
5. Create or update `docs/qa/test-reports/<tag>.md` with Version, planned Tag,
   exact commit/build, Pipeline, environment, included Issues/MRs, results,
   evidence, defects, and QA decision.
6. Create or update the configured `docs/releases/<tag>.md` and link the test
   report. Record Version, Milestone, planned Tag, branch, SHA,
   pipeline, target, owner, time window, rollout, monitoring, validation, and
   rollback. Freeze version evidence after the release completes.
7. Update an existing project manifest version only when the technology stack
   requires it. Do not introduce a generic VERSION file. Run
   `python scripts/release_version_check.py --tag <tag>` before asking a human
   to create the Tag.
8. Output a documentation decision table using `create`, `update`, `no-change`,
   or `follow-up`, with path, reason, and status/confirmer.
9. Stop at the human gate. Do not approve, merge, tag, or deploy.

## Output

```markdown
## Release Readiness

Target and source:
Final version / Milestone / planned Tag:
Decision:
Pipeline and tests:
Included changes:
Config / data / permission impact:
Environment isolation or lock:
Release note and documentation impact:
Documentation decisions (path / action / reason / status or confirmer):
Rollout and monitoring:
Rollback target and steps:
Post-release validation:
Tag command for human execution:
Human confirmation needed:
```

`Decision` is one of `not_ready`, `ready_for_isolated_dev`,
`ready_for_shared_environment_confirmation`, or
`ready_for_release_confirmation`.

## References

- Read `references/environment-policy.md` for GitLab environment locks and
  deployment record fields.
- Read `references/release-example.md` for a release dry-run example.
