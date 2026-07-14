# 开发角色

## 输入

- Task Issue #4
- Solution Issue #3
- `examples/order-demo/docs/modules/order.md`

## 输出

- `examples/order-demo/src/order_approval.py`
- `examples/order-demo/tests/test_order_approval.py`

## 首轮缺陷

首版只检查订单状态，遗漏：

```text
applicant != approver
```

QA 发现该缺陷并记录为 Bug Issue #6。

## 修复

添加 `_ensure_not_self_approval`，并在 `approve` 和 `reject` 中调用。

## 验证

运行：

```powershell
python scripts/smoke_check.py
```
