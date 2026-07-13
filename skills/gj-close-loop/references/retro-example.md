# Demo Run Reference

Retro inputs:

- Run log: `examples/demo-run/00-run-log.md`
- Role notes: `examples/demo-run/roles/`

Key learnings:

1. API project identity mismatch is a preflight blocker.
2. Local token helpers must be ignored and never included in open-source packages.
3. Skill metadata validation should run immediately after generation.
4. QA failure must become a Bug Issue with regression scope.
5. First-batch skills remain draft until a second run validates them.
6. On Windows, pass `--name` to metadata generation if UTF-8 Chinese SKILL.md
   files fail under the default locale.

Long-term context output:

- `docs/context/current-state.md`
- `docs/modules/order.md`
- `.gj/context.yml`
