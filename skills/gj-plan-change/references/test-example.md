# 示例演练参考

QA 发现以下失败检查：

```text
Alice 提交订单 -> Alice 审批同一订单 -> approved
```

预期：

```text
自审批被拒绝。
```

该失败转为 Bug Issue #6 和回归测试，没有只留在测试报告中。
