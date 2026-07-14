# 代码审阅角色

## 输入

- `examples/demo-run/mr/merge-request.md` 中的 MR 描述
- `examples/demo-run/mr/changed-files.txt` 中的变更文件
- `.gj/workflow.yml` 中的规则地图

## AI 审阅输出

```markdown
## MR 审阅

变更摘要：新增 GitLab AI 工作流骨架、demo 项目、demo-run 产物和首批 skill 草案。

主要风险：
- `scripts/policy_check.py` 属于 workflow-policy，高风险规则需要 tech-lead ack。
- `orchestrator/` 涉及未来 webhook 和 AI 调用，需 security/devops 后续确认。
- 本地 `gitlab-api.ps1` 不应进入提交。

测试建议：
- 运行 `policy_check.py`。
- 运行 `smoke_check.py`。
- 验证 skill metadata。
```

## 人工确认

只有 CI 通过且 Token helper 保持未跟踪时，Reviewer 才接受 MR。
