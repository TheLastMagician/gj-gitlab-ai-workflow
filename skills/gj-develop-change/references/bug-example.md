# 示例演练参考

缺陷 Issue：#6 `[订单审批流 v1.0] Bug：申请人可以审批自己的订单`

事实：

- Alice 提交了订单。
- Alice 审批了同一订单。
- 首版实现允许该操作。

根因：

- 服务只检查了 `pending` 状态。
- 没有比较 `order.applicant` 和 `approver`。

修复：

- 新增 `_ensure_not_self_approval`。
- 在 `approve` 和 `reject` 中调用。
- 新增回归测试 `test_applicant_cannot_approve_own_order`。
