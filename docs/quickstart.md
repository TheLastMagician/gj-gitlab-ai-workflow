# Quickstart

## 1. Install Skills

From the target project root, install the same skill source for Codex, Claude
Code, and OpenCode:

```powershell
npx --yes skills@1.5.15 add https://github.com/TheLastMagician/gj-gitlab-ai-workflow --skill '*' -a codex -a claude-code -a opencode --copy -y
```

The installer writes project-local discovery entries to `.agents/skills` for Codex
and OpenCode and `.claude/skills` for Claude Code. Start a new agent session
after installation.

Pasting a GitHub URL must not silently execute code. Run the command explicitly
or ask the current agent to install it. If Node.js is unavailable, clone this
repository and use the Python fallback:

```powershell
python scripts/install_skills.py --agent all --project-root C:\path\to\your-project --force
```

Use `--dest` only for a custom single skills directory.

The full skill list and workflow mapping are in `docs/skills.md`.

## 2. Bootstrap Repository Assets

Install the reusable assets into a target GitLab repository:

```powershell
python scripts/install_workflow.py --target C:\path\to\your-project
```

Install once. Fast / Standard / Hotfix are runtime workflow routes, not
different installation editions.

For an existing project, prefer a non-destructive install:

```powershell
python scripts/install_workflow.py --target C:\path\to\your-project --only-missing
```

When you intentionally replace existing workflow assets, create a backup:

```powershell
python scripts/install_workflow.py --target C:\path\to\your-project --force --backup
```

Minimum setup after installation:

- `.ai/project.yml`
- `.ai/rule-map.yml`
- `.gitlab-ci.yml` or `GJ_TEST_COMMAND` for the real project test command

Update `.ai/context-index.yml`, `.ai/role-map.yml`, `CODEOWNERS`, and the
provided documentation templates when those capabilities are actually used.

Decide early whether MR branches deploy only to isolated dev/review
environments or whether a human may manually deploy them to shared test. Do not
let every MR branch automatically overwrite a single shared test environment.

Keep GitLab Issues/MRs as the discussion trail and repository docs as the
durable source. For each requirement or MR, require a documentation impact
answer: update PRD/design/prototype/solution/test/release/context docs, or
explain why no doc update is needed.

## 3. Configure GitLab

Skill installation and offline planning do not need a token. For live GitLab
access, configure the installed cross-Agent helper once from the target project:

```powershell
python scripts/gitlab_api.py configure --url https://gitlab.example.com --project-id group/project
python scripts/gitlab_api.py doctor
```

The hidden prompt writes the token to ignored `.ai/gitlab.local.json`. Use
`read_api` for read-only access and grant `api` only when confirmed writes are
needed. CI may override the local file with `GITLAB_URL`, `GITLAB_PROJECT_ID`,
and `GITLAB_TOKEN`. See `docs/gitlab-access.md` for commands and security rules.

Create the workflow labels from `examples/demo-run/gitlab/labels.md`, then add a
milestone for the first iteration. Protect the default branch and require a
passing pipeline before merge.

For GitLab CE, also limit who may merge to the default branch. Low-risk Fast
MRs do not require an extra approval count. CODEOWNERS and an optional Approve
action can guide review, but the workflow does not depend on paid approval
rules.

Before implementation, confirm exactly one route label on the Issue or work
item. When creating the MR, select the same `flow::fast`, `flow::standard`, or
`flow::hotfix` label in GitLab. The policy job rejects missing or conflicting
flow labels.

When role routing is needed, replace placeholders in `.ai/role-map.yml` with real GitLab usernames. For every
human handoff, assign the Issue/MR owner or reviewer and add an `@username`
comment. `gj-workflow-next` reads GitLab API state directly; company channels
such as Enterprise WeCom or email should be configured in GitLab notification
settings, not as a separate workflow inbox.

Validate role ownership after editing `.ai/role-map.yml`:

```powershell
python scripts/validate_role_map.py
```

For live GitLab membership checks, reuse the local config:

```powershell
python scripts/validate_role_map.py --strict-gitlab
```

## 4. Run The Demo Flow

Use a small target project such as `gj-workflow-demo` to run the workflow once:

```text
产品经理 -> Tech Lead -> 开发 -> Reviewer -> QA -> DevOps -> PM
```

The recorded inputs, outputs, failures, and human confirmations are in
`examples/demo-run/00-run-log.md`.

## 5. Validate An Installed Target Project

After installation, run the checks used by every project:

```powershell
python scripts/workflow_assets_check.py
python scripts/smoke_check.py
```

Run role, context, and release checks when those capabilities are in use:

```powershell
python scripts/validate_role_map.py
python scripts/context_freshness_check.py
python scripts/release_dry_run.py --output build/release-dry-run.md
```

## 6. Run CI/CD In A Target Project

Configure a GitLab Runner with Docker executor. Fast MRs use the first three
stages; release runs only for tags or a manual default-branch pipeline:

```text
Fast / Standard MR: policy -> workflow -> test
Tag / manual release: policy -> workflow -> test -> release
```

See `docs/cicd.md` for job details and artifacts.
