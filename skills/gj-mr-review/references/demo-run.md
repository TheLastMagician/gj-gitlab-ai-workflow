# 示例演练参考

MR 输入：

- 描述：`examples/demo-run/mr/merge-request.md`
- 变更文件：`examples/demo-run/mr/changed-files.txt`
- AI 审阅：`examples/demo-run/mr/ai-review.md`

审阅经验：

1. 先检查工作流章节，再看代码细节。
2. 根据 `.gj/workflow.yml` 匹配变更文件。
3. 策略或 Orchestrator 文件变化时拒绝 `flow::fast`；要求 Standard/Hotfix 证据和人工
   合并决定。
4. 确认本地 Token helper 未提交。
5. 如实标注草稿 Skill 的成熟度。
