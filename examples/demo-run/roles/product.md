# Product Role

## Input

订单在进入履约前需要审批，审批人可以通过或驳回，申请人不能审批自己的订单。

## AI Output

```markdown
推荐路径：标准需求

判断理由：涉及审批规则和权限边界，不能走小改动。

缺失问题：
1. 审批人来源是否来自角色、组织架构或订单字段？
2. 是否有金额阈值？
3. 驳回后订单回到 draft 还是终止？
4. 是否需要审计日志？
```

## Human Confirmation

Product confirms:

- v1.0 only covers the minimal approval state machine.
- Amount threshold, audit log, notification, and external integration are non-goals.
- Self-approval prevention is required for v1.0.

## Output

Requirement Issue #2 with explicit acceptance criteria.
