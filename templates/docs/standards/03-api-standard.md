# API 契约规范

## 事实源与文档位置

- API 结构优先以仓库中的 OpenAPI、AsyncAPI、protobuf 或同类 schema 为可执行事实源。
- `docs/technical/apis/<domain>.md` 记录业务语义、权限、错误、幂等、兼容和回归要求，
  不手工复制一份容易漂移的完整 schema。
- 新 API 边界从 `.gj/doc-templates/api-contract.md` 创建；已有边界原地更新。

## 触发条件

新增或改变端点、事件、请求/响应字段、错误语义、权限、幂等、速率限制、弃用策略或
兼容行为时，必须更新机器契约和对应 API 文档。仅内部实现变化且契约不变时写
`no-change`。

## 最低内容

- 权威 schema 路径、Owner、适用版本和相关需求/方案。
- 请求、响应或事件语义，以及成功、失败和权限行为。
- 身份认证、授权、敏感数据分类、幂等和重试规则。
- 向后兼容判断、弃用窗口和调用方迁移要求。
- 契约测试与回归入口。

Breaking change 必须得到明确批准，不能通过修改文档把不兼容变化包装成兼容变化。
API Owner 或 Dev Lead 在方案门确认；Reviewer 在 MR 中核对 schema、实现、测试和文档。
