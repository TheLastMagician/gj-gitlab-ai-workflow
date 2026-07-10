# Retro

## What Worked

- The workflow produced traceable GitLab objects and local docs.
- The small demo was enough to expose real friction.
- QA failure became a Bug Issue and regression test.

## What Did Not Work Smoothly

- API project identity was wrong until manually corrected.
- Local token helper needed explicit ignore handling.
- Skill initialization failed for overlong short descriptions.
- Skill metadata generation hit a Windows default-encoding issue on Chinese
  SKILL.md files; passing `--name` avoided reading frontmatter.
- Some GitLab settings still need UI/admin confirmation.
- The MR pipeline initially stayed pending because no runner was active. A
  Windows shell runner picked up the job but failed before running scripts. A
  Docker executor runner is the recommended setup.

## Process Improvements

- Add a bootstrap preflight that compares API project path with `git remote`.
- Add a template warning about local token helpers.
- Keep skill metadata short and validate after generation.
- Make skill tooling read UTF-8 explicitly or document the `--name` workaround.
- Require QA failure -> Bug Issue conversion in `gj-plan-change` or QA guidance.
- Add runner availability and executor type checks to `gj-workflow-bootstrap`
  preflight.

## Next Step

Use the draft skills to run a second demo pass and update them based on the
actual friction.
