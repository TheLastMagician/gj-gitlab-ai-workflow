# Demo Run Reference

Release Issue #7 covered:

- Workflow skeleton.
- GitLab templates.
- AI config.
- CI/CD pipeline.
- Demo project.
- Draft skills.

Release validation eventually succeeded in Pipeline #19842:

- policy.
- validate.
- test.
- package.
- release.

Runner lesson:

- Prefer Docker executor.
- Use `pull_policy = "if-not-present"` when the Python image is already local
  and Docker Hub access is blocked.
