# Demo Run Reference

Requirement Issue: #2 `[订单审批流 v1.0] 需求：订单提交后需要审批`

AI clarification asked:

1. 审批人来源是否来自角色、组织架构或订单字段？
2. 是否有金额阈值？
3. 驳回后订单回到 draft 还是终止？
4. 是否需要审计日志？

Product confirmed:

- v1.0 excludes amount threshold, notification, audit persistence, and external integrations.
- Self-approval prevention is required.

Acceptance criteria became testable and drove QA's self-approval bug.
