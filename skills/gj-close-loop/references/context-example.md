# 示例演练参考

首次演练的上下文产物：

- `docs/context/current-state.md`
- `examples/order-demo/docs/modules/order.md`
- `.gj/context.yml`

提取的长期事实：

- 禁止自审批。
- Docker executor 是本示例稳定的 CI Runner 方案。
- 本地 Token helper 必须被忽略且不能进入分发包。

仅属历史的事实：

- 首次失败的 policy Job 是 Runner 拉取策略问题，不是工作流策略失败。
