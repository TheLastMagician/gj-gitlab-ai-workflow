# 示例演练记录：订单审批流 v1.0

演练日期：2026-07-03

GitLab 项目：`zengqinglin/gj-workflow-demo`

Milestone：[订单审批流 v1.0](https://gitlab.example.com/acme/gj-workflow-demo/-/milestones/1)

合并请求：[!1 feat(workflow): 初始化 GitLab AI 工作流骨架](https://gitlab.example.com/acme/gj-workflow-demo/-/merge_requests/1)

## 端到端轨迹

| 步骤 | 角色 | 输入 | 输出 | 失败/阻碍 | 人工确认 |
| --- | --- | --- | --- | --- | --- |
| 1 | DevOps / Codex | 本地仓库和工作流文档 | 标签、模板、`.gj`、CI 文件 | API helper 最初指向错误项目，用户随后修正 | 写操作前确认 API ProjectId 与 `origin` 匹配 |
| 2 | 产品 | 粗略需求：订单审批 | Requirement Issue #2 和 AI 澄清评论 | 审批人来源和金额阈值不清晰 | 产品确认 v1.0 不包含金额阈值 |
| 3 | 开发经理 | Requirement Issue #2 | Solution Issue #3 | 权限风险需要负责人关注 | 开发经理接受示例的最小状态机 |
| 4 | 开发经理 | 需求和方案 | Task Issue #4、Test Issue #5、Release Issue #7 | 小型示例容易过度拆分任务 | Web API、数据库、通知保持范围外 |
| 5 | 开发 | Task Issue #4 | 示例服务和测试 | 首版遗漏自审批规则 | 开发添加回归测试和修复 |
| 6 | Reviewer | MR 描述和变更文件 | AI 审阅意见 | policy 根据变更路径检查最低 flow | Reviewer 检查风险、测试、回滚和合并就绪度 |
| 7 | QA | 验收标准 | QA 失败和 Bug Issue #6 | 失败不能隐藏在测试报告中 | QA 把失败升级为 Bug Issue |
| 8 | 开发 | Bug Issue #6 | `_ensure_not_self_approval` 和回归测试 | approve 和 reject 都需要相同规则 | Reviewer 确认两条路径 |
| 9 | DevOps | Release Issue #7 | 发布和回滚清单 | 保护分支设置需要 GitLab UI/管理员确认 | DevOps 在合并前确认 |
| 10 | PM | 所有 Issue 和 MR 评论 | Retro Issue #8 和长期上下文更新 | 示例存在前不应编写 Skill 草稿 | PM 只批准提取首批草稿 |

## 暴露的问题

1. GitLab API helper 配置可能与 `git remote` 漂移。
2. 开源前，本地 Token helper 文件需要明确忽略规则。
3. GitLab 标签和 Issue 创建需要幂等，避免重复演练。
4. Skill 初始化元数据有严格长度限制。
5. QA 失败必须转为 Bug Issue，不能藏在测试报告文字里。
6. CI policy 检查看不到未跟踪的本地秘密文件，提交卫生仍然重要。
7. Windows 上，Skill 元数据生成器可能无法读取 UTF-8 中文 `SKILL.md`，除非传入
   `--name` 或脚本明确使用 UTF-8。
8. Python dataclass 动态导入时，必须在 `exec_module` 前把模块注册到 `sys.modules`。
9. 没有活跃项目/共享 Runner 时，GitLab Pipeline 会保持 pending。临时 shell Runner
   接收了 Job，但受 Windows PowerShell 工作目录处理影响而失败。本示例稳定方案是使用
   `python:3.12-slim` 的 Docker executor Runner。

## CI/CD 流水线

示例 Pipeline 扩展为完整交付流程：

```text
policy -> workflow -> test -> package -> release
```

预期 Job：

- `policy_check`
- `workflow_contract`
- `smoke_check`
- `package_open_source`
- `release_dry_run`

Skill 校验在 `package_open_source` 中运行，因为 Skill 属于可复用开源包，不是独立业务
流程阶段。

校验结果：

- Pipeline：https://gitlab.example.com/acme/gj-workflow-demo/-/pipelines/19841
- 状态：success
- 说明：首次 `policy_check` Job 失败，是因为 Docker Runner 使用
  `pull_policy=always` 从 Docker Hub 拉取 `python:3.12-slim`。把临时 Runner 改为
  `pull_policy=if-not-present` 后，重试 Job 和所有下游 Job 成功。

## 值得固化的稳定动作

- 任何写操作前校验 GitLab 项目标识。
- 初始化标签、模板、`.gj`、文档、CI 和 CODEOWNERS。
- 使用分流推荐一个 `flow::fast`、`flow::standard` 或 `flow::hotfix` 标签供人确认。
- 把粗略需求转为待确认问题和验收标准。
- 根据工作流策略审阅 MR 描述。
- 把 QA 失败转为包含根因和回归范围的 Bug Issue。
- 工作完成后按需更新长期当前事实文档并闭环。
