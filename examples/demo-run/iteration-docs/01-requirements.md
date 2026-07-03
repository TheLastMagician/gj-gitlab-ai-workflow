# Requirements

## Requirement

Orders must be submitted for approval before fulfillment. A non-applicant
approver can approve or reject the order.

## Acceptance Criteria

- Draft orders can be submitted and become pending.
- Pending orders can be approved by a non-applicant.
- Pending orders can be rejected by a non-applicant with a reason.
- Applicants cannot approve or reject their own orders.
- Approved or rejected orders cannot be approved again.

## Non-Goals

- Amount threshold approval chains.
- Notifications.
- Audit log persistence.
- Database and Web API.
