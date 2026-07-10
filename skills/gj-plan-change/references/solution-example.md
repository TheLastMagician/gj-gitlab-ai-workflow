# Demo Run Reference

Solution Issue: #3 `[订单审批流 v1.0] 方案：最小订单状态机`

The accepted demo solution:

- Use an in-memory domain model.
- Model state as `draft -> pending -> approved/rejected`.
- Keep API, DB, audit log, and notifications out of scope.
- Treat self-approval as a permission risk.

The solution plan must explicitly list non-goals so implementation does not
grow beyond the accepted scope.
