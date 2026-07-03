# Environment Standard

- Dev/review environments may be automatic when isolated per branch or MR.
- Shared test/staging environments must not be overwritten automatically by MR branches.
- Shared test/staging deployment requires human confirmation.
- Shared environments must use an environment lock such as GitLab `resource_group`.
- Record branch, MR, commit SHA, pipeline, deployer, previous version, rollback target, and QA owner for every shared environment deployment.
- Use `develop`, `integration`, `release/*`, or tag-based rules for shared test deployment.
- AI may assist with checks, deployment notes, and project-approved commands, but must not autonomously overwrite shared test/staging or production.
