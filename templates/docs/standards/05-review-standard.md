# Review Standard

- Confirm linked Issue and acceptance criteria.
- Check risk paths from `.gj/workflow.yml`.
- Verify self-test and rollback notes.
- Verify the documentation decision table includes path, action, triggering
  fact, stage/status, and confirmer/follow-up, then compare it with the actual
  diff and durable behavior. Blank rows are not evidence; every follow-up needs
  an Issue, owner, and due date.
- Check product, interaction, API/event, database, architecture/ADR, module
  rule, test baseline, release, and runtime-state impact. GitLab child Issues do
  not replace durable repository docs.
- Treat the MR label and actual changed files as the final risk facts; the Issue
  records the initial plan.
- On GitLab CE, use protected branches, restricted merge permissions, and a
  successful Pipeline for hard enforcement. CODEOWNERS or an optional Approve
  action may guide review but are not mandatory approval evidence.
- Keep AI review advisory by default. Humans may use AI to assist approval and
  merge operations after they explicitly decide to proceed.
