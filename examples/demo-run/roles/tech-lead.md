# 开发经理角色

## 输入

- Requirement Issue #2
- AI 澄清评论
- `docs/modules/order.md` 中的当前模块上下文

## 输出

Solution Issue #3：

- 示例使用内存领域模型。
- 状态建模为 `draft -> pending -> approved/rejected`。
- API、数据库、审计日志和通知保持范围外。
- 为提交、通过、驳回、自审批和重复审批添加测试。

## 风险说明

- `risk-permission` 有效，因为自审批是业务权限规则。
- 真实系统不能依赖纯用户名进行授权。

## 人工确认

开发经理确认方案足以用于示例，但不作为生产授权设计的先例。
