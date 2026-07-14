# 示例演练参考

示例项目刻意保持精简：

- 代码：`examples/demo-project/src/order_approval.py`
- 测试：`examples/demo-project/tests/test_order_approval.py`
- 模块文档：`docs/modules/order.md`
- 上下文索引：`.gj/context.yml`

真实代码库建图时，扫描结果直接更新后续 Skill 会读取的文档：

- 技术栈、架构和开发约定：`docs/standards/01-development-standard.md`
- 测试工具链和执行规则：`docs/standards/07-test-standard.md`
- 当前状态、模块地图和术语：`docs/context/*.md`
- 模块边界、规则和集成：`docs/modules/*.md`
- AI 路由：`.gj/context.yml`
- 可执行风险和技术债：带负责人和期限的 GitLab Issue 草稿

示例级假设写入标准或 `docs/context/current-state.md` 前，必须标记为需要人工确认；现有
代码习惯不能自动升级为团队规范。
