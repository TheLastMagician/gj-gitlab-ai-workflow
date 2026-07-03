# Developer Role

## Input

- Task Issue #4
- Solution Issue #3
- `docs/modules/order.md`

## Output

- `examples/demo-project/src/order_approval.py`
- `examples/demo-project/tests/test_order_approval.py`

## First-Pass Bug

Initial implementation checked only the order state and missed:

```text
applicant != approver
```

QA found the bug and it was recorded as Bug Issue #6.

## Fix

Add `_ensure_not_self_approval` and call it in both `approve` and `reject`.

## Verification

Run:

```powershell
python scripts/smoke_check.py
```
