# 示例演练参考

主工作项：Requirement Issue #2

长期方案：`docs/technical/solutions/order-approval.md`

历史示例还创建了 Solution Issue #3 单独跟踪评审。只有独立负责人、排期或跟踪确实有
价值时才重复这种拆分。

已接受的示例方案：

- 使用内存领域模型。
- 状态建模为 `draft -> pending -> approved/rejected`。
- API、数据库、审计日志和通知不在范围内。
- 把自审批视为权限风险。

方案文档必须明确列出非目标，避免实现超出已接受范围。评审讨论保留在主 Issue。
