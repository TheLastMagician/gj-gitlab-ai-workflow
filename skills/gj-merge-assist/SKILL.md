---
name: gj-merge-assist
description: Prepare, verify, and execute GitLab merge request merges only after explicit human authorization. Use when a human asks Codex to check whether an MR can be merged, summarize merge risks, verify pipeline/discussions/Issue linkage/MR template compliance, or perform a GitLab merge after the human clearly says to merge a specific MR.
---

# GJ Merge Assist

## Overview

Assist a human with GitLab MR merge decisions and merge execution. Never approve, merge, deploy, or bypass protections autonomously.

## Hard Boundary

- Treat merge as a human decision.
- Without explicit human authorization, only inspect, summarize, and recommend next actions.
- Explicit authorization must name the MR and use an unambiguous command such as `confirm merge MR !2`, `merge MR !2`, or `please merge MR !2`.
- Do not infer authorization from phrases like `looks good`, `can this be merged?`, `LGTM`, or `please check this`.
- Do not approve the MR unless the human explicitly asks to approve and the current environment has a safe, audited approval command.
- Do not merge when checks are failed, running, missing, or unknown unless the human explicitly acknowledges the exact failing condition and the repository policy allows it.
- Do not use admin override, force merge, skip CI, or bypass unresolved discussions.

## Workflow

1. Identify the GitLab project and MR number from the user's request or repository remote.
2. Read MR details: title, source/target branch, author, state, merge status, labels, description, linked Issues, assignees/reviewers, discussions, commits, diff summary, and latest pipeline.
3. Check merge readiness:
   - MR state is opened.
   - `detailed_merge_status` is mergeable or equivalent.
   - Latest pipeline for the MR/head SHA is success.
   - Discussions are resolved.
   - MR description includes linked Issue, change summary, test result, risks, rollback, config/database changes, and AI usage.
   - Required owner acknowledgements are present for high-risk paths.
   - Release and rollback notes are clear.
4. If authorization is absent, output a readiness report and the exact human confirmation sentence needed to merge.
5. If authorization is present and all checks pass, execute the merge with the normal GitLab merge API or project-approved tool.
6. After merge, report final state, merge commit SHA when available, closed Issues, and any follow-up actions.

## Merge Readiness Output

Use this shape before any merge:

```markdown
## Merge Readiness

MR:
Decision:

Blocking items:

Checks:

- Merge status:
- Pipeline:
- Discussions:
- Linked Issues:
- MR template:
- Risk / owner ack:
- Tests:
- Rollback:
- AI usage boundary:

Recommendation:

Required human confirmation:
```

`Decision` must be one of:

- `ready_to_merge_after_human_confirmation`
- `not_ready`
- `merged_after_explicit_human_authorization`
- `blocked_by_policy`

## Execution Rules

When executing a merge:

1. Echo the authorization phrase you are acting on.
2. Re-fetch MR details immediately before merge.
3. Refuse if the MR SHA changed after the readiness check; re-run readiness instead.
4. Use normal merge, not force merge or skip CI.
5. Prefer removing the source branch only if the MR or human requested it.
6. Post a short MR note when useful: checked by AI, merged by human authorization, pipeline/result, and follow-ups.

## Examples

Check only:

```text
Check whether MR !2 can be merged.
```

Authorized execution:

```text
Confirm merge MR !2.
```

Blocked wording:

```text
MR !2 looks fine, merge it if you think so.
```

This is not explicit enough. Ask for a clear confirmation sentence.

## References

Read `references/gitlab-merge.md` when using GitLab API or local helper scripts to perform merge operations.
