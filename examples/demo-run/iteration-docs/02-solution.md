# Solution

## Summary

Use a minimal Python domain service for the demo. The state model is:

```text
draft -> pending -> approved
                 -> rejected
```

## Files

- `examples/demo-project/src/order_approval.py`
- `examples/demo-project/tests/test_order_approval.py`

## Risks

- Self-approval is a permission rule and must be explicitly checked.
- A real system must replace plain string users with trusted identity and role
  checks.
