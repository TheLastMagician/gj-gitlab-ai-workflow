#!/usr/bin/env python3
"""Validate the distributable source package and write a report."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PACKAGE_PATHS = [
    "README.md",
    "CONTRIBUTING.md",
    "docs/gitlab-access.md",
    "docs/documentation-governance.md",
    "docs/versioning.md",
    "docs/workflow.md",
    "docs/quickstart.md",
    "docs/skills.md",
    "skills.sh.json",
    "scripts/install_skills.py",
    "templates/gj/workflow.yml",
    "templates/gj/context.yml",
    "templates/gitlab/.gitlab-ci.yml",
    "templates/gitlab/.gitlab/gj-workflow-ci.yml",
    "templates/gitlab/.gitlab/merge_request_templates/Default.md",
    "templates/CODEOWNERS",
    "templates/orchestrator/README.md",
    "templates/orchestrator/orchestrator.py",
    "skills/gj-workflow-bootstrap/SKILL.md",
    "skills/gj-workflow-bootstrap/scripts/bootstrap_from_github.py",
    "skills/gj-workflow-next/SKILL.md",
    "skills/gj-plan-change/SKILL.md",
    "skills/gj-develop-change/SKILL.md",
    "skills/gj-mr-review/SKILL.md",
    "skills/gj-release-readiness/SKILL.md",
    "skills/gj-close-loop/SKILL.md",
    "templates/docs/standards/10-environment-standard.md",
    "templates/docs/standards/11-notification-standard.md",
    "templates/docs/standards/12-context-governance.md",
    "templates/docs/standards/13-versioning-standard.md",
    "templates/gj/doc-templates/product-requirement.md",
    "templates/gj/doc-templates/product-design.md",
    "templates/gj/doc-templates/prototype-record.md",
    "templates/gj/doc-templates/technical-solution.md",
    "templates/gj/doc-templates/api-contract.md",
    "templates/gj/doc-templates/database-design.md",
    "templates/gj/doc-templates/adr.md",
    "templates/gj/doc-templates/module.md",
    "templates/gj/doc-templates/test-plan.md",
    "templates/gj/doc-templates/test-report.md",
    "templates/gj/doc-templates/release-note.md",
    "templates/scripts/release_dry_run.py",
    "templates/scripts/release_version_check.py",
    "templates/scripts/validate_role_map.py",
    "templates/scripts/gitlab_api.py",
    "examples/demo-run/00-run-log.md",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    package = ROOT / args.package
    output = ROOT / args.output
    if not package.exists():
        raise FileNotFoundError(package)

    with zipfile.ZipFile(package) as archive:
        names = set(archive.namelist())
    missing = [path for path in REQUIRED_PACKAGE_PATHS if path not in names]
    if missing:
        raise RuntimeError(f"package is missing required paths: {missing}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        """# Release Dry Run

## Result

Package validation passed.

## Required Manual Release Checks

- Remove or replace private GitLab URLs before public release if needed.
- Confirm license choice.
- Confirm GitLab Runner setup instructions against target environment.
- Confirm protected branch and merge gate settings in GitLab.
""",
        encoding="utf-8",
    )
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
