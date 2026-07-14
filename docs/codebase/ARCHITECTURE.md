# 架构

## 已确认事实

- `templates/` 保存可复用的工作流资产。
- `.gitlab/` 和 `.gj/` 是安装到当前示例仓库的工作流资产。
- `scripts/policy_check.py` 是 CI 策略门禁。
- `scripts/smoke_check.py` 运行示例测试。
- `orchestrator/orchestrator.py` 是无第三方依赖的命令路由骨架。
- `examples/demo-project/` 是演练工作流的目标项目。
- `examples/demo-run/` 保存首次演练产物。

## 待确认

- 后续 Orchestrator 应实现为服务、CLI、GitLab CI Job 还是定时任务。
- GitLab 写操作如何认证和审计。
