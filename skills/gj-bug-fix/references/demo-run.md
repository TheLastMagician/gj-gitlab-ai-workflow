# Demo Run Reference

Bug Issue: #6 `[订单审批流 v1.0] Bug：申请人可以审批自己的订单`

Facts:

- Alice submitted an order.
- Alice approved the same order.
- The first implementation allowed it.

Root cause:

- The service checked only `pending` status.
- It did not compare `order.applicant` with `approver`.

Fix:

- Add `_ensure_not_self_approval`.
- Call it from both `approve` and `reject`.
- Add regression test `test_applicant_cannot_approve_own_order`.
