---
name: gj-codebase-map
description: Map an existing repository into AI-readable project context. Use when onboarding a GitLab project, refreshing docs/codebase, deriving docs/context and docs/modules, generating .ai/context-index.yml drafts, or scanning changed paths after major refactors.
---

# GJ Codebase Map

## Workflow

1. Discover the repository structure with `rg --files`.
2. Scan from four views:
   - tech: stack, runtime, dependencies, integrations.
   - arch: entry points, layers, data flow, module boundaries.
   - quality: conventions, tests, CI, error handling.
   - concerns: security, brittle areas, performance, unknowns.
3. Write or update:
   - `docs/codebase/STACK.md`
   - `docs/codebase/INTEGRATIONS.md`
   - `docs/codebase/ARCHITECTURE.md`
   - `docs/codebase/STRUCTURE.md`
   - `docs/codebase/CONVENTIONS.md`
   - `docs/codebase/TESTING.md`
   - `docs/codebase/CONCERNS.md`
4. Derive draft current context:
   - `docs/context/current-state.md`
   - `docs/context/module-map.md`
   - `docs/context/glossary.md`
   - `docs/modules/*.md`
   - `.ai/context-index.yml`
5. Mark every inference that needs human confirmation.
6. Scan generated output for secrets before staging or sharing.

## Rules

- Treat `docs/codebase/*` as observed facts, not approved business truth.
- Do not convert observed behavior into current-state rules without confirmation.
- Stop and ask for human action if a token, private key, password, or connection string appears.

## Output

```markdown
## Codebase Map Summary

Scanned paths:

Generated / updated docs:

Observed facts:

Inferences needing confirmation:

Risks and concerns:

Secret scan:
```

## References

Read `references/demo-run.md` for the demo-sized mapping example.
