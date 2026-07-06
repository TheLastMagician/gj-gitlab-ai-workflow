# Quickstart

## 1. Install Skills

Install the bundled skills into Codex:

```powershell
python scripts/install_skills.py --force
```

Use `--dest` when you want to install into a custom skills directory.

The full skill list and workflow mapping are in `docs/skills.md`.

## 2. Bootstrap Repository Assets

Install the reusable assets into a target GitLab repository:

```powershell
python scripts/install_workflow.py --target C:\path\to\your-project
```

For an existing project, prefer a non-destructive install:

```powershell
python scripts/install_workflow.py --target C:\path\to\your-project --only-missing
```

When you intentionally replace existing workflow assets, create a backup:

```powershell
python scripts/install_workflow.py --target C:\path\to\your-project --force --backup
```

Then customize:

- `.ai/project.yml`
- `.ai/rule-map.yml`
- `.ai/context-index.yml`
- `.ai/role-map.yml`
- `CODEOWNERS`
- `.gitlab-ci.yml`
- `docs/standards/10-environment-standard.md`
- `docs/standards/11-notification-standard.md`
- `docs/standards/12-document-standard.md`
- `docs/product/requirements/PRD.md`
- `docs/product/designs/product-design.md`
- `docs/product/prototypes/prototype-record.md`
- `docs/technical/solutions/solution-design.md`
- `docs/qa/test-plans/test-plan.md`
- `docs/qa/test-reports/test-report.md`
- `docs/releases/release-note.md`

Decide early whether MR branches deploy only to isolated dev/review
environments or whether a human may manually deploy them to shared test. Do not
let every MR branch automatically overwrite a single shared test environment.

Keep GitLab Issues/MRs as the discussion trail and repository docs as the
durable source. For each requirement or MR, require a documentation impact
answer: update PRD/design/prototype/solution/test/release/context docs, or
explain why no doc update is needed.

## 3. Configure GitLab

Create the workflow labels from `examples/demo-run/gitlab/labels.md`, then add a
milestone for the first iteration. Protect the default branch and require a
passing pipeline before merge.

Replace placeholders in `.ai/role-map.yml` with real GitLab usernames. For every
human handoff, assign the Issue/MR owner or reviewer and add an `@username`
comment. `gj-workflow-inbox` reads GitLab API state directly; company channels
such as Enterprise WeCom or email should be configured in GitLab notification
settings, not as a separate workflow inbox.

Validate role ownership after editing `.ai/role-map.yml`:

```powershell
python scripts/validate_role_map.py
```

For live GitLab membership checks, provide a token through `GITLAB_TOKEN` and
pass `--gitlab-url` plus `--project-id`.

## 4. Run The Demo Flow

Use a small target project such as `gj-workflow-demo` to run the workflow once:

```text
产品经理 -> Tech Lead -> 开发 -> Reviewer -> QA -> DevOps -> PM
```

The recorded inputs, outputs, failures, and human confirmations are in
`examples/demo-run/00-run-log.md`.

## 5. Validate This Workflow Project

```powershell
python scripts/policy_check.py --mr-description examples/demo-run/mr/merge-request.md --changed-files examples/demo-run/mr/changed-files.txt
python scripts/validate_role_map.py --role-map templates/ai/role-map.yml --allow-placeholders
python scripts/validate_skills.py
python scripts/install_skills.py --dry-run
python scripts/install_workflow.py --target C:\path\to\your-project --dry-run
```

These commands are for maintaining this standalone workflow and skills project.

## 6. Validate An Installed Target Project

After installing into a business project, run the target project checks there:

```powershell
python scripts/workflow_assets_check.py
python scripts/validate_role_map.py
python scripts/smoke_check.py
python scripts/release_dry_run.py --output build/release-dry-run.md
```

## 7. Run CI/CD In A Target Project

Configure a GitLab Runner with Docker executor. The demo pipeline uses:

```text
policy -> workflow -> test -> release
```

See `docs/cicd.md` for job details and artifacts. The installed target-project
pipeline does not run `skill_validate` or `package_open_source`.

## 8. Extract Skills

After the first run, update only the first-batch skills:

- `gj-workflow-bootstrap`
- `gj-codebase-map`
- `gj-workflow-triage`
- `gj-workflow-inbox`
- `gj-requirement-refine`
- `gj-mr-review`
- `gj-bug-fix`
- `gj-retro-learnings`

Treat these as draft skills until a second run proves they work with less manual
intervention.
