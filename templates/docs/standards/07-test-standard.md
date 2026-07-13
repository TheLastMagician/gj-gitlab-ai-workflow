# 测试文档规范

## 测试计划与测试报告不是一回事

- `docs/qa/test-plans/<capability>.md` 是可复用的当前测试基线，随需求和风险原地更新。
- `docs/qa/test-reports/<tag>.md` 是一次发布的实际执行证据，按 Tag 新建并在关闭后冻结。
- 临时探索和执行讨论留在 GitLab Test Issue 或 MR；只有需要独立负责人、排期或跟踪时
  才创建 Test Issue。

## 测试计划触发条件

验收、回归、权限、数据、兼容或发布验证不平凡时创建或更新测试计划。至少覆盖成功、
失败、权限和回归路径，并将 Requirement/风险 ID 映射到可执行用例、环境、数据和阻断
条件。简单局部改动可在 MR 写清自测并对测试计划写 `no-change`。

## 测试报告触发条件

执行正式 QA 或准备发布时，按计划 Tag 记录准确的 commit/build、Pipeline、环境、用例
结果、证据、缺陷、剩余风险和 QA 结论。失败项创建 Bug Issue，不得在报告中隐藏。

QA 负责确认测试基线和报告结论；Reviewer 检查代码测试与计划是否覆盖持久风险。
