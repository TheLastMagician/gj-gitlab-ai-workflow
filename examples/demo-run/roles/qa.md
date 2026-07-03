# QA Role

## Input

- Requirement acceptance criteria.
- Demo service behavior.
- Unit tests.

## Failure Found

The first implementation allowed:

```text
Alice submits order -> Alice approves same order -> approved
```

## Expected

The service must reject self-approval.

## Action

QA creates Bug Issue #6 and requires a regression test.

## Regression

- `test_applicant_cannot_approve_own_order`
- Manual check that non-applicant approval still works.
