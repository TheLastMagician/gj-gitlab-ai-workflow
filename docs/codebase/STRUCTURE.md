# Structure

```text
.gj/                         Current project AI config
.gj/doc-templates/           Installed document scaffolding, not project facts
.gitlab/                     Current project GitLab templates
docs/context/                Stable AI context
docs/codebase/               Observed codebase map
docs/product/                Current product requirements and interaction facts
docs/technical/              Current solution, API, database, and ADR facts
docs/modules/                Module knowledge
docs/qa/                     Reusable test plans and per-Tag test evidence
docs/releases/               Per-Tag release evidence
examples/demo-project/       Tiny order approval project
examples/demo-run/           First end-to-end run artifacts
orchestrator/                Webhook routing skeleton
scripts/                     CI and utility scripts
skills/                      Eight cross-agent workflow skills
templates/                   Reusable assets for target projects
```

Document templates are installed under `.gj/doc-templates/`; project fact
directories contain only semantic documents created when their boundary exists.
