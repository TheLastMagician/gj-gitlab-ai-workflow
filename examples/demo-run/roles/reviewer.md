# Reviewer Role

## Input

- MR description in `examples/demo-run/mr/merge-request.md`
- Changed files in `examples/demo-run/mr/changed-files.txt`
- Rule map in `.ai/rule-map.yml`

## AI Review Output

```markdown
## MR Review

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

## Human Confirmation

Reviewer accepts the MR only if CI passes and the token helper remains untracked.
