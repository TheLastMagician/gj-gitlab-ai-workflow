# Demo Run Reference

MR input:

- Description: `examples/demo-run/mr/merge-request.md`
- Changed files: `examples/demo-run/mr/changed-files.txt`
- AI review: `examples/demo-run/mr/ai-review.md`

Review lessons:

1. Check workflow sections before code details.
2. Match changed files against `.ai/rule-map.yml`.
3. Reject `flow::fast` when policy or orchestrator files change; require
   Standard/Hotfix evidence and a human merge decision.
4. Confirm local token helpers are not committed.
5. Keep draft skill maturity honest.
