# Requirement Standard

字段的权威定义是 `.gitlab/issue_templates/Requirement.md`,本标准不重复
字段清单,只规定模板管不了的原则:

- Requirement Issue 记录本次需求变化、讨论和状态；
  `docs/product/requirements/<capability>.md` 记录确认后的当前完整产品要求。
  两者必须互相链接，不能复制后各自演进。

- 验收标准必须可测试:每一条都能回答"怎么验证它通过了"。
- 验收标准必须包含反例:明确什么情况应该被拒绝或报错
  (示例:v1.0 的"申请人不能自审批"、v1.1 的"非主管不能批高金额单")。
- 非目标范围必须真实填写,"无"也是一个需要想过才能给出的答案。

## 执行点

- 字段完整性:需求助理 agent 检查(补齐草稿时标出缺失字段)。
- 可测试性与反例:决策门 1(PM 确认需求)人工确认。
- 产品事实确认后:更新语义化 PRD 的 Owner、Status、Source Issue、Target release、
  Effective from、Implemented by、Related documents 和 Last verified。
