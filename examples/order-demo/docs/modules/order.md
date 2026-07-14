# 订单模块

## 当前规则

- 订单提交后进入 `pending` 状态。
- 审批人可以通过或驳回 `pending` 订单。
- 申请人不能审批自己提交的订单。
- 已审批或已驳回的订单不能重复审批。

## 示例代码

- `examples/order-demo/src/order_approval.py`
- `examples/order-demo/tests/test_order_approval.py`

## 后续扩展

- 金额阈值影响审批层级。
- 审批操作写入审计日志。
- 审批结果通知申请人。
- 与外部 ERP 或库存系统联动。
