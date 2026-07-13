# Release Standard

本文只定义发布准备和迭代关闭。需求到收尾每个阶段的文档产物、文件规范和更新方式见
`12-context-governance.md`;目标版本、Tag、构建和部署版本见
`13-versioning-standard.md`。

## 发布准备

- 列出包含的 Issues、MRs、commit SHA 和 Pipeline。
- 确认最终 SemVer、GitLab Milestone、计划 Tag 和对应发布说明路径。
- 确认测试结果、配置/数据库/权限变化、发布步骤、监控、回滚和发布后验证。
- 说明目标是隔离的 dev/review 环境，还是共享 test/staging/production 环境。
- 共享环境必须确认人工部署决定、环境锁、当前版本、目标版本和回滚目标。
- `gj-release-readiness` 准备证据，人决定并执行发布；AI 不自主 tag 或 deploy。
- 普通功能 MR 不 bump 版本;版本和项目 manifest 在发布准备阶段集中收口。

## 发布文档

- 执行正式 QA 时创建或更新 `docs/qa/test-reports/<tag>.md`。
- 有用户可见、运维、配置、数据库、权限、灰度或回滚影响时，创建或更新
  `docs/releases/<tag>.md`。
- 测试报告记录实际 build/commit、环境、结果和证据；发布说明记录计划和最终结果。
- 一次发布完成后冻结该版本证据；后续发布新建版本文件，不覆盖旧证据。

## 收尾回写清单

`gj-close-loop` 按下列清单判断并输出文档决策，由发布责任人确认；这些不是默认 CI
硬门禁：

- [ ] 有跨项目当前事实变化时，已覆盖更新 `docs/context/current-state.md`。
- [ ] 有业务规则、接口或模块行为变化时，相关 `docs/modules/*.md` 已在变更 MR 更新。
- [ ] 有重要里程碑时，已写短小的 `ai-context-summary.md`；普通 Fast/单 Issue 可不写。
- [ ] 文档路径或模块边界变化时，`.gj/context.yml` 已更新。
- [ ] `recent_iteration_summaries` 只保留每模块最新一轮入口。
- [ ] 过时的当前事实已直接删除，没有继续保留“已废弃”段落。
- [ ] 未解决问题已进入 GitLab Issue，含负责人和期限。

`context_freshness_check.py` 可按需报告结构和预算问题，但不进入默认 CI。文档事实是否
正确，仍由对应责任人确认。
