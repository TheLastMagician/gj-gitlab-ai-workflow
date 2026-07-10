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

- `python scripts/policy_check.py --mr-description examples/demo-run/mr/merge-request.md --changed-files examples/demo-run/mr/changed-files.txt --labels flow::standard`
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

## 文档影响

- 已更新：`docs/workflow.md`, `docs/quickstart.md`, `docs/context/current-state.md`, `docs/modules/order.md`, `examples/demo-run/`.
- 不需要更新，原因：首轮 demo 暂未引入正式 PRD/product-design 模板。
- 后续文档 Issue：后续由文档治理规范补充 PRD、设计、测试、发布模板。

## AI 使用范围

Codex generated the skeleton, demo artifacts, issue notes, and draft skills from
the supplied workflow document and the first end-to-end run.

## Reviewer 重点关注

- Ensure `gitlab-api.ps1` and tokens are not committed.
- Check `policy_check.py` secret scanning and minimum-flow behavior.
- Confirm skill drafts are not overclaiming maturity.
