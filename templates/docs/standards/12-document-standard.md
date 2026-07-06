# Documentation Standard

## Principles

- GitLab Issues and MR comments record discussion, questions, decisions, and
  handoffs.
- Repository docs record stable conclusions that future humans and AI agents
  should treat as durable project context.
- Do not let important product, design, technical, test, release, or context
  decisions live only in comments.
- AI may draft documents, but accountable humans must confirm product intent,
  technical decisions, QA sign-off, release decisions, and high-risk changes.

## Required Documents

Create or update these documents when the workflow step changes durable facts:

| Document | Default path | Required when |
| --- | --- | --- |
| PRD | `docs/product/requirements/<feature>.md` | A new feature, behavior change, permission rule, amount rule, workflow rule, or acceptance criteria is introduced. |
| Product design | `docs/product/designs/<feature>.md` | UX, UI behavior, user flow, page state, copy, permission visibility, or error handling matters. |
| Prototype record | `docs/product/prototypes/<feature>.md` | There is a Figma/Axure/Sketch/image/html prototype, screenshot, or clickable demo. |
| Technical solution | `docs/technical/solutions/<feature>.md` | Architecture, interface, data, permission, compatibility, rollout, or rollback decisions are needed. |
| Test plan | `docs/qa/test-plans/<feature>.md` | QA needs acceptance, regression, permission, failure-path, or release validation coverage. |
| Test report | `docs/qa/test-reports/<feature>.md` | QA has executed validation or found failures. |
| Release note | `docs/releases/<version>.md` | User-visible behavior, operations, rollout, or rollback information changes. |
| Iteration summary | `docs/iterations/<iteration>/ai-context-summary.md` | A milestone or significant workflow run ends. |

## Definition Of Ready

A standard feature should not enter solution design until:

- PRD exists or the requirement Issue explicitly states why a PRD is not needed.
- Acceptance criteria are testable.
- Non-goals are stated.
- Product owner confirmation is recorded.
- UX/design/prototype needs are either linked or explicitly marked not needed.

## Definition Of Done

A change should not be considered done until:

- Durable conclusions are in repo docs, not only GitLab comments.
- MR description lists documentation changes or explains why none are needed.
- Related docs are updated in the same MR or linked follow-up Issue.
- `docs/context`, `docs/modules`, or `ai-context-summary.md` are updated when
  long-term AI context changes.

## Documentation Impact Check

Every workflow skill should answer:

```text
Documentation impact:
- Create/update:
- Not needed because:
- Human confirmation needed:
- Follow-up Issue needed:
```

If the answer affects development, testing, release, support, or future AI
context, prefer updating repo docs through MR instead of leaving it as a
comment.

## Staleness And Conflicts

- Mark obsolete documents as superseded instead of deleting history silently.
- Link the replacing document.
- If Issue comments and repo docs disagree, treat repo docs as the current
  durable source only after human confirmation.
- `gj-context-extract` should resolve or record conflicts before updating
  long-term AI context.
