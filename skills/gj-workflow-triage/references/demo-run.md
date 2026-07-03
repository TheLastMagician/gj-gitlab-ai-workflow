# Demo Run Reference

Order approval was classified as a standard requirement because it involved:

- Approval flow.
- Permission boundary.
- Acceptance criteria that needed QA.
- Multiple workflow objects: requirement, solution, task, test, release, retro.

Example output:

```markdown
推荐路径：标准需求

判断理由：涉及审批规则和权限边界，不能走小改动。

可跳过的步骤：无。

必须保留的步骤：需求确认、方案、任务、MR、测试、发布、复盘。

风险提示：risk-permission。

需要人工确认：审批人来源、金额阈值是否进入 v1.0。
```
