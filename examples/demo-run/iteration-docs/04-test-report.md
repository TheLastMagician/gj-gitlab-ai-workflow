# Test Report

## Scope

- Submit draft order.
- Approve pending order.
- Reject pending order with required reason.
- Block applicant self-approval.
- Block repeated approval.

## Failure

QA found that the applicant could approve their own order in the first pass.

## Resolution

Bug Issue #6 was created. The final implementation adds
`_ensure_not_self_approval` and a regression test.

## Regression Result

Expected local command:

```powershell
python scripts/smoke_check.py
```
