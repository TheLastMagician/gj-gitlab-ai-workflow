# Bug Fix Record

## Root Cause

The first implementation only validated that an order was `pending`. It did not
compare `order.applicant` with the acting `approver`.

## Fix

Add:

```python
def _ensure_not_self_approval(order: Order, approver: str) -> None:
    if order.applicant == approver:
        raise OrderApprovalError("applicant cannot approve their own order")
```

Call it from both `approve` and `reject`.

## Regression

- `test_applicant_cannot_approve_own_order`
- Non-applicant approval still passes.
