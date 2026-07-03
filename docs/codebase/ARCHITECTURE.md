# Architecture

## Observed Facts

- `templates/` stores reusable workflow assets.
- `.gitlab/` and `.ai/` install the workflow into the current demo repository.
- `scripts/policy_check.py` is the CI policy gate.
- `scripts/smoke_check.py` runs demo tests.
- `orchestrator/orchestrator.py` is a dependency-free command router skeleton.
- `examples/demo-project/` is the target used to exercise the workflow.
- `examples/demo-run/` records first-run artifacts.

## Needs Confirmation

- Whether future Orchestrator should be a service, CLI, GitLab CI job, or scheduled worker.
- How GitLab writes should be authenticated and audited.
