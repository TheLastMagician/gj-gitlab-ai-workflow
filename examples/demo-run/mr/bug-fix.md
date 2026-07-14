# 缺陷修复记录

## 根因

首版只校验订单为 `pending`，没有比较 `order.applicant` 与当前 `approver`。

## 修复

新增：

```python
def _ensure_not_self_approval(order: Order, approver: str) -> None:
    if order.applicant == approver:
        raise OrderApprovalError("applicant cannot approve their own order")
```

在 `approve` 和 `reject` 中调用。

## 回归

- `test_applicant_cannot_approve_own_order`
- 非申请人审批仍然通过。
