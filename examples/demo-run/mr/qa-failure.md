# QA Failure

## Failure

Applicant could approve their own submitted order.

## Why It Matters

The requirement explicitly says the applicant cannot approve their own order.
This is a permission rule, not a cosmetic defect.

## Bug Issue

Created: #6 `[订单审批流 v1.0] Bug：申请人可以审批自己的订单`

## Fix Requirement

- Block self-approval in `approve`.
- Block self-rejection in `reject`.
- Add regression tests.
