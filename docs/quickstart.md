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

Then customize:

- `.ai/project.yml`
- `.ai/rule-map.yml`
- `.ai/context-index.yml`
- `CODEOWNERS`
- `.gitlab-ci.yml`

## 3. Configure GitLab

Create the workflow labels from `examples/demo-run/gitlab/labels.md`, then add a
milestone for the first iteration. Protect the default branch and require a
passing pipeline before merge.

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
python scripts/validate_skills.py
python scripts/install_skills.py --dry-run
python scripts/install_workflow.py --target C:\path\to\your-project --dry-run
```

These commands are for maintaining this standalone workflow and skills project.

## 6. Validate An Installed Target Project

After installing into a business project, run the target project checks there:

```powershell
python scripts/workflow_assets_check.py
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
- `gj-requirement-refine`
- `gj-mr-review`
- `gj-bug-fix`
- `gj-retro-learnings`

Treat these as draft skills until a second run proves they work with less manual
intervention.
