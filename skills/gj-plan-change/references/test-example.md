# Demo Run Reference

QA found this failed check:

```text
Alice submits an order -> Alice approves the same order -> approved
```

Expected:

```text
Self-approval is rejected.
```

The failure became Bug Issue #6 and a regression test instead of being left only
inside a test report.
