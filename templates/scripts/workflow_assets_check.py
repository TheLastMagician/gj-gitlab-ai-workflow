#!/usr/bin/env python3
"""Validate that reusable workflow assets are installed."""

from __future__ import annotations

import sys
from pathlib import Path


REQUIRED = [
    ".ai/project.yml",
    ".ai/rule-map.yml",
    ".ai/context-index.yml",
    ".ai/role-map.yml",
    ".gitlab/issue_templates/Requirement.md",
    ".gitlab/issue_templates/SmallChange.md",
    ".gitlab/merge_request_templates/Default.md",
    "docs/context/current-state.md",
    "docs/context/module-map.md",
    "scripts/policy_check.py",
    "scripts/smoke_check.py",
    "docs/standards/00-index.md",
    "docs/standards/10-environment-standard.md",
    "docs/standards/11-notification-standard.md",
    "scripts/context_freshness_check.py",
    "scripts/validate_role_map.py",
    "scripts/release_dry_run.py",
    "docs/product/requirements/PRD.md",
    "docs/product/designs/product-design.md",
    "docs/product/prototypes/prototype-record.md",
    "docs/technical/solutions/solution-design.md",
    "docs/qa/test-plans/test-plan.md",
    "docs/qa/test-reports/test-report.md",
    "docs/releases/release-note.md",
]

REQUIRED_DIRS = [
    "docs/modules",
]


def main() -> int:
    missing = [path for path in REQUIRED if not Path(path).exists()]
    missing.extend(path for path in REQUIRED_DIRS if not Path(path).is_dir())
    if missing:
        print("missing workflow assets:")
        for path in missing:
            print(f"- {path}")
        return 1

    print("workflow assets check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
