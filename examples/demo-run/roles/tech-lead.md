# Tech Lead Role

## Input

- Requirement Issue #2
- AI clarification comment
- Current module context from `docs/modules/order.md`

## Output

Solution Issue #3:

- Use an in-memory domain model for the demo.
- Model state as `draft -> pending -> approved/rejected`.
- Keep API, DB, audit log, and notifications out of scope.
- Add tests for submit, approve, reject, self-approval, and repeated approval.

## Risk Notes

- `risk-permission` is valid because self-approval is a business permission rule.
- Real systems must not rely on plain usernames for authorization.

## Human Confirmation

Tech Lead confirms the solution is enough for a demo and does not set a precedent
for production authorization design.
