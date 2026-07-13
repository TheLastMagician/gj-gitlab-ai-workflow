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

Ask the newly installed bootstrap Skill to initialize the current repository:

```text
Use gj-workflow-bootstrap to initialize this project.
```

The Skill-local GitHub bootstrap script fetches this repository's source archive
and runs the same non-destructive asset installer. In a source checkout, the
equivalent command is:

```powershell
python scripts/install_workflow.py --target C:\path\to\your-project
```

The installer fills missing files recursively and never deletes target
directories. `--force` replaces only known conflicting files and automatically
backs them up. An existing complex GitLab CI include is left unchanged and
reported as a required manual action.

Minimum setup after installation:

- `.gj/workflow.yml`
- `.gj/context.yml`
- `.gitlab/gj-workflow-ci.yml` included by `.gitlab-ci.yml`
- `GJ_TEST_COMMAND` configured for the real project test command

Update `.gj/workflow.yml`, `.gj/context.yml`, `CODEOWNERS`, and the
provided documentation templates when those capabilities are actually used.

Keep AI context selective: `always_load` is limited to three small current-fact
files, module docs load only when paths match, and each module keeps only its
latest iteration summary. Do not add `docs/iterations/` to permanent context.
See `docs/documentation-governance.md` for the split and loading model.

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

The hidden prompt writes the token to ignored `.gj/gitlab.local.json`. Use
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

When role routing is needed, replace placeholders in `.gj/workflow.yml` with real GitLab usernames. For every
human handoff, assign the Issue/MR owner or reviewer and add an `@username`
comment. `gj-workflow-next` reads GitLab API state directly; company channels
such as Enterprise WeCom or email should be configured in GitLab notification
settings, not as a separate workflow inbox.

Validate role ownership after editing `.gj/workflow.yml`:

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

After installation, run the project test that remains a hard CI gate:

```powershell
python scripts/smoke_check.py
```

Run workflow, role, context, and release audits when those capabilities are in use:

```powershell
python scripts/workflow_assets_check.py
python scripts/validate_role_map.py
python scripts/context_freshness_check.py
python scripts/release_dry_run.py --output build/release-dry-run.md
```

## 6. Run CI/CD In A Target Project

The installer adds `.gitlab/gj-workflow-ci.yml` and includes it from the root
pipeline. Each GJ hard-gate job explicitly enters merge-request pipelines and
uses its own Python image, so it does not replace the business project's image,
stages, or `before_script`. Existing complex `include` blocks require the exact
manual include action printed by the installer.

Configure a GitLab Runner with Docker executor. Policy and project tests are the
only default hard gates; advisory Jobs may still appear in other stages:

```text
MR hard gates: policy -> test
Advisory: workflow assets / release dry run
```

See `docs/cicd.md` for job details and artifacts.

The template defaults to `python:3.12-slim` for its helper scripts. Non-Python
projects can set the GitLab CI variable `GJ_CI_IMAGE` to a project image that
contains Python and the real test toolchain, then set `GJ_TEST_COMMAND`.
