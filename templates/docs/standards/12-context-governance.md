# Context Governance Standard

## Loading Order

AI loads context progressively, never by scanning all of `docs/`:

1. Current Issue or MR.
2. `.gj/context.yml` and its `global.always_load` files.
3. Only the module whose `paths` match the requested or changed files.
4. Only feature, decision, test, or release docs linked by the work item or module.
5. At most the latest listed `ai-context-summary.md` for that module.

`docs/iterations/` is frozen history and is not loaded by default. A specific
historical file may be read only to answer an explicit traceability question.

## Context Budget

The default `.gj/context.yml` budget is mandatory:

- at most 3 `always_load` files and 24,000 total characters;
- no iteration archive in `always_load`;
- at most 5 docs and 40,000 total characters for one module context;
- at most 1 recent iteration summary per module.

`context_freshness_check.py` reports these machine-checkable limits as advisory
warnings by default. Use `--strict` only for an explicit governance audit; normal
MRs must not be blocked solely by documentation size or archive hygiene.

## File Boundaries

- `docs/context/current-state.md`: current cross-project facts only; overwrite,
  never append a changelog.
- `docs/context/module-map.md`: module routing and ownership, not detailed rules.
- `docs/modules/<module>.md`: current complete rules for one bounded module.
- `docs/product`, `docs/technical`, `docs/qa`: one feature or decision scope per
  file; split by stable ownership or review boundary, not by iteration date.
- `docs/releases` and `docs/iterations`: immutable release/iteration evidence.
- GitLab Issues/MRs: discussion and confirmation history, not durable truth.

When a file mixes unrelated modules, owners, or review lifecycles, split it and
update `.gj/context.yml`. Do not create a single project encyclopedia.

## Writeback

The active Skill updates its applicable durable docs in the same change when
facts are confirmed. `gj-close-loop` rewrites current state, prunes the context
index, and records the latest iteration summary. Humans review factual decisions;
they do not need to remember every documentation path.
