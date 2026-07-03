# 示例：订单审批流 v1.0

订单审批流 v1.0 是第一轮端到端模拟使用的小项目。它故意选择了一个小但足够真实的
业务：订单提交后需要由非申请人审批，审批通过才能进入后续履约。

## 业务目标

- 让业务人员能提交订单审批。
- 让审批人能通过或驳回订单。
- 防止申请人审批自己的订单。
- 为后续金额阈值、角色权限和审计日志留下扩展点。

## 第一轮发现的关键摩擦

1. GitLab API 配置可能和 `origin` 指向不同项目，写入前必须校验。
2. 本地 API helper 容易硬编码 token，必须加入 `.gitignore` 并避免复制到开源包。
3. skill 初始化元数据有长度约束，批量生成时需要校验。
4. “模拟角色”如果只写结论，很难反推 skill；必须保存每一步输入和输出。
5. QA 发现的问题要形成 Bug Issue，而不是直接在测试报告里吞掉。

## 产物位置

- 角色记录：`examples/demo-run/roles/`
- GitLab 对象记录：`examples/demo-run/gitlab/`
- MR 记录：`examples/demo-run/mr/`
- 迭代沉淀：`examples/demo-run/iteration-docs/`
