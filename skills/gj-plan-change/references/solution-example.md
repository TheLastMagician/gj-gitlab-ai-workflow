# Demo Run Reference

Main work item: Requirement Issue #2

Durable solution: `docs/technical/solutions/order-approval.md`

The historical demo also created Solution Issue #3 for a separately tracked
review. Do not repeat that split unless independent ownership, scheduling, or
tracking makes it useful.

The accepted demo solution:

- Use an in-memory domain model.
- Model state as `draft -> pending -> approved/rejected`.
- Keep API, DB, audit log, and notifications out of scope.
- Treat self-approval as a permission risk.

The solution document must explicitly list non-goals so implementation does
not grow beyond the accepted scope. Review discussion remains on the main Issue.
