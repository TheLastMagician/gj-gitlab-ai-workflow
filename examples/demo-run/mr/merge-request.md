# Merge Request

## 关联 Issue

Closes #4

Related: #1 #2 #3 #5 #6 #7 #8

## 变更内容

- Add open-source workflow skeleton docs.
- Add GitLab issue and MR templates.
- Add `.ai` config and reusable templates.
- Add CI policy and smoke check scripts.
- Add Orchestrator routing skeleton.
- Add order approval demo project.
- Add first demo-run artifacts.
- Add first-batch draft skills.

## 自测结果

- `python scripts/policy_check.py --mr-description examples/demo-run/mr/merge-request.md --changed-files examples/demo-run/mr/changed-files.txt`
- `python scripts/smoke_check.py`

## 风险点

- Workflow policy files affect future merge gates.
- Orchestrator skeleton is not production-ready.
- Local GitLab API helper must stay untracked because it can contain credentials.

## 回滚方案

Revert this MR. No database, external API, or production configuration changes
are included.

## 数据库 / 配置变更

No database changes. GitLab labels, milestone, issues, and notes were created in
the demo project as part of the first run.

## AI 使用范围

Codex generated the skeleton, demo artifacts, issue notes, and draft skills from
the supplied workflow document and the first end-to-end run.

## Reviewer 重点关注

- Ensure `gitlab-api.ps1` and tokens are not committed.
- Check `policy_check.py` secret scanning and owner ack behavior.
- Confirm skill drafts are not overclaiming maturity.

## 高风险确认记录

/owner-ack tech-lead "同意本 MR 修改 workflow policy 和模板，作为 demo 验证。"

/owner-ack security "Orchestrator 当前仅为骨架，不接收真实 webhook，不处理生产数据。"

/owner-ack devops "CI 门禁可作为 MVP，protected branch 规则需在 GitLab UI 另行确认。"
