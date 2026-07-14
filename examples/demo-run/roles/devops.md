# DevOps 角色

## 输入

- Release Issue #7
- `.gitlab-ci.yml`
- `scripts/policy_check.py`
- `scripts/smoke_check.py`

## 输出

发布清单：

- CI 包含 `policy` 和 `test` 阶段。
- `policy_check.py` 校验唯一 flow 标签、MR 证据、高风险变更文件和已提交秘密。
- `smoke_check.py` 运行示例单元测试。
- 回滚方式是回退 MR。

## 人工确认

需要 GitLab UI 或管理员 API 确认：

- 默认分支已保护。
- Pipeline 成功后才能合并。
- 合并前必须解决讨论。
