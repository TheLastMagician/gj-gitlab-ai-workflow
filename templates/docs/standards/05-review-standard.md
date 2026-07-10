# Review Standard

- Confirm linked Issue and acceptance criteria.
- Check risk paths from `.ai/rule-map.yml`.
- Verify self-test and rollback notes.
- Treat the MR label and actual changed files as the final risk facts; the Issue
  records the initial plan.
- On GitLab CE, use protected branches, restricted merge permissions, and a
  successful Pipeline for hard enforcement. CODEOWNERS or an optional Approve
  action may guide review but are not mandatory approval evidence.
- Keep AI review advisory by default. Humans may use AI to assist approval and
  merge operations after they explicitly decide to proceed.
