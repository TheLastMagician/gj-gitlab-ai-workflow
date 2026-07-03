#!/usr/bin/env python3
"""Validate that core workflow assets exist in an installed project."""

from __future__ import annotations

import sys
from pathlib import Path


REQUIRED = [
    ".ai/project.yml",
    ".ai/rule-map.yml",
    ".ai/context-index.yml",
    ".ai/role-map.yml",
    ".gitlab/issue_templates/Requirement.md",
    ".gitlab/merge_request_templates/Default.md",
    "docs/context/current-state.md",
    "docs/modules/order.md",
    "docs/standards/00-index.md",
    "docs/standards/10-environment-standard.md",
    "docs/standards/11-notification-standard.md",
    "scripts/policy_check.py",
    "scripts/smoke_check.py",
    "scripts/release_dry_run.py",
]


def main() -> int:
    missing = [path for path in REQUIRED if not Path(path).exists()]
    if missing:
        print("missing workflow assets:")
        for path in missing:
            print(f"- {path}")
        return 1
    print("workflow assets check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
