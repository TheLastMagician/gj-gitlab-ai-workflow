#!/usr/bin/env python3
"""Validate installed workflow assets and GJ MR pipeline jobs."""

from __future__ import annotations

import re
import sys
from pathlib import Path


CORE_REQUIRED = [
    ".gitlab-ci.yml",
    ".gitlab/gj-workflow-ci.yml",
    ".gj/workflow.yml",
    ".gj/context.yml",
    ".gitlab/merge_request_templates/Default.md",
    "docs/context/current-state.md",
    "docs/context/module-map.md",
    "scripts/policy_check.py",
    "scripts/smoke_check.py",
    "scripts/workflow_assets_check.py",
    "scripts/release_version_check.py",
]

OPTIONAL_ASSETS = [
    ".gitlab/issue_templates/Requirement.md",
    ".gitlab/issue_templates/SmallChange.md",
    "docs/standards/00-index.md",
    "docs/standards/10-environment-standard.md",
    "docs/standards/11-notification-standard.md",
    "docs/standards/12-context-governance.md",
    "docs/standards/13-versioning-standard.md",
    "scripts/context_freshness_check.py",
    "scripts/validate_role_map.py",
    "scripts/gitlab_api.py",
    "scripts/release_dry_run.py",
    ".gj/doc-templates/product-requirement.md",
    ".gj/doc-templates/product-design.md",
    ".gj/doc-templates/prototype-record.md",
    ".gj/doc-templates/technical-solution.md",
    ".gj/doc-templates/api-contract.md",
    ".gj/doc-templates/database-design.md",
    ".gj/doc-templates/adr.md",
    ".gj/doc-templates/module.md",
    ".gj/doc-templates/test-plan.md",
    ".gj/doc-templates/test-report.md",
    ".gj/doc-templates/release-note.md",
]

OPTIONAL_DIRS = ["docs/modules"]
MANDATORY_MR_JOBS = ["policy_check", "smoke_check"]
MANDATORY_TAG_JOBS = ["release_version_check"]
GJ_CI_INCLUDE = ".gitlab/gj-workflow-ci.yml"


def top_level_block(text: str, key: str) -> str:
    match = re.search(
        rf"(?ms)^{re.escape(key)}:\s*\n(.*?)(?=^[A-Za-z0-9_.-]+:\s*(?:#.*)?$|\Z)",
        text,
    )
    return match.group(1) if match else ""


def root_ci_errors(text: str) -> list[str]:
    if GJ_CI_INCLUDE not in text:
        return [f".gitlab-ci.yml 未 include {GJ_CI_INCLUDE}"]
    return []


def gj_ci_errors(text: str) -> list[str]:
    errors: list[str] = []
    for job in MANDATORY_MR_JOBS:
        block = top_level_block(text, job)
        if not block:
            errors.append(f"{GJ_CI_INCLUDE} 缺少必跑 Job：{job}")
        elif 'CI_PIPELINE_SOURCE == "merge_request_event"' not in block:
            errors.append(f"{GJ_CI_INCLUDE} 的 {job} 未加入 MR Pipeline")
    for job in MANDATORY_TAG_JOBS:
        block = top_level_block(text, job)
        if not block:
            errors.append(f"{GJ_CI_INCLUDE} 缺少 Tag 发布 Job：{job}")
        elif "CI_COMMIT_TAG" not in block:
            errors.append(f"{GJ_CI_INCLUDE} 的 {job} 未加入 Tag Pipeline")
    return errors


def gj_ci_warnings(text: str) -> list[str]:
    warnings: list[str] = []
    for job in MANDATORY_MR_JOBS:
        block = top_level_block(text, job)
        if block and ("CI_OPEN_MERGE_REQUESTS" not in block or "when: never" not in block):
            warnings.append(f"{GJ_CI_INCLUDE} 的 {job} 未抑制重复 branch Job")
    return warnings


def declared_module_docs() -> list[str]:
    config = Path(".gj/context.yml")
    if not config.exists():
        return []
    docs: list[str] = []
    in_docs = False
    for raw_line in config.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if re.match(r"docs:\s*$", stripped):
            in_docs = True
            continue
        if in_docs:
            if stripped.startswith("- "):
                docs.append(stripped[2:].strip().strip('"').strip("'"))
                continue
            in_docs = False
    return docs


def main() -> int:
    missing_core = [path for path in CORE_REQUIRED if not Path(path).exists()]
    missing_optional = [path for path in OPTIONAL_ASSETS if not Path(path).exists()]
    missing_optional.extend(path for path in OPTIONAL_DIRS if not Path(path).is_dir())
    missing_optional.extend(path for path in declared_module_docs() if not Path(path).exists())
    errors = [f"缺少核心工作流资产：{path}" for path in missing_core]
    warnings = [f"可选工作流资产未启用：{path}" for path in missing_optional]

    root_ci = Path(".gitlab-ci.yml")
    gj_ci = Path(GJ_CI_INCLUDE)
    if root_ci.exists():
        errors.extend(root_ci_errors(root_ci.read_text(encoding="utf-8")))
    if gj_ci.exists():
        gj_text = gj_ci.read_text(encoding="utf-8")
        errors.extend(gj_ci_errors(gj_text))
        warnings.extend(gj_ci_warnings(gj_text))

    if warnings:
        print("workflow assets warnings:")
        for warning in warnings:
            print(f"- {warning}")
    if errors:
        print("workflow assets check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("workflow assets check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
