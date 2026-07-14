# QA 角色

## 输入

- Requirement 验收标准。
- 示例服务行为。
- 单元测试。

## 发现的失败

首版允许：

```text
Alice 提交订单 -> Alice 审批同一订单 -> approved
```

## 预期

服务必须拒绝自审批。

## 动作

QA 创建 Bug Issue #6 并要求回归测试。

## 回归

- `test_applicant_cannot_approve_own_order`
- 手工检查非申请人审批仍然有效。
