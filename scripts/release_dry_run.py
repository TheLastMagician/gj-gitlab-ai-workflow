#!/usr/bin/env python3
"""Validate release package and write a release dry-run artifact."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PACKAGE_PATHS = [
    "README.md",
    "docs/workflow.md",
    "docs/quickstart.md",
    "docs/skills.md",
    "templates/ai/project.yml",
    "templates/gitlab/.gitlab/merge_request_templates/Default.md",
    "skills/gj-workflow-bootstrap/SKILL.md",
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
