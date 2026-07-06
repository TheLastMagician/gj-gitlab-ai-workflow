#!/usr/bin/env python3
"""Minimal GitLab MR policy check for the GJ AI workflow."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable


REQUIRED_MR_SECTIONS = [
    "关联 Issue",
    "变更内容",
    "自测结果",
    "风险点",
    "回滚方案",
    "文档影响",
    "AI 使用范围",
]

DEFAULT_HIGH_RISK_RULES = [
    {
        "id": "database",
        "paths": ["db/migration/**", "**/migrations/**"],
        "require_owner_ack": ["dba", "tech-lead"],
    },
    {
        "id": "security",
        "paths": ["src/**/auth/**", "src/**/permission/**", "orchestrator/**"],
        "require_owner_ack": ["security"],
    },
    {
        "id": "workflow-policy",
        "paths": [".gitlab-ci.yml", "scripts/policy_check.py", "templates/**"],
        "require_owner_ack": ["tech-lead"],
    },
]

SECRET_PATTERNS = [
    re.compile(r"glpat-[A-Za-z0-9_.-]{16,}"),
    re.compile(r"(?i)(private[-_ ]?token|api[-_ ]?key|password|secret)\s*[:=]\s*['\"]?[^'\"\s]{8,}"),
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache"}
SKIP_FILES = {"gitlab-api.ps1"}


def run_git(args: list[str]) -> list[str]:
    try:
        result = subprocess.run(
            ["git", *args],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def load_text(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return os.environ.get("CI_MERGE_REQUEST_DESCRIPTION", "")


def load_changed_files(path: str | None) -> list[str]:
    if path:
        return [
            line.strip()
            for line in Path(path).read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    env_files = os.environ.get("GJ_CHANGED_FILES")
    if env_files:
        return [line.strip() for line in env_files.splitlines() if line.strip()]

    changed = run_git(["diff", "--name-only", "origin/main...HEAD"])
    if changed:
        return changed

    return run_git(["ls-files"])


def parse_simple_yaml_rule_map(path: Path) -> list[dict[str, object]]:
    """Parse the small .ai/rule-map.yml shape without external dependencies."""
    if not path.exists():
        return DEFAULT_HIGH_RISK_RULES

    rules: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    list_key: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        stripped = line.strip()

        if stripped == "rules:":
            continue
        if stripped.startswith("- id:"):
            current = {
                "id": stripped.split(":", 1)[1].strip().strip('"'),
                "paths": [],
                "require_owner_ack": [],
            }
            rules.append(current)
            list_key = None
            continue
        if current is None:
            continue
        if stripped in {"paths:", "require_owner_ack:"}:
            list_key = stripped[:-1]
            current.setdefault(list_key, [])
            continue
        if stripped == "standards:":
            list_key = None
            continue
        if stripped.startswith("- ") and list_key:
            value = stripped[2:].strip().strip('"').strip("'")
            current.setdefault(list_key, [])
            current[list_key].append(value)  # type: ignore[index]

    return rules or DEFAULT_HIGH_RISK_RULES


def glob_to_regex(pattern: str) -> re.Pattern[str]:
    escaped = re.escape(pattern.replace("\\", "/"))
    escaped = escaped.replace(r"\*\*/", r"(?:.*/)?")
    escaped = escaped.replace(r"\*\*", r".*")
    escaped = escaped.replace(r"\*", r"[^/]*")
    return re.compile(rf"^{escaped}$", re.IGNORECASE)


def matches_any_path(path: str, patterns: Iterable[str]) -> bool:
    normalized = path.replace("\\", "/")
    return any(glob_to_regex(pattern).match(normalized) for pattern in patterns)


def scan_candidate_files(changed_files: Iterable[str]) -> list[Path]:
    files = []
    for item in run_git(["ls-files"]):
        path = Path(item)
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        if path.exists() and path.is_file():
            files.append(path)

    for item in changed_files:
        path = Path(item)
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        if path.exists() and path.is_file():
            files.append(path)

    return files


def check_required_sections(description: str) -> list[str]:
    missing = []
    for section in REQUIRED_MR_SECTIONS:
        if section not in description:
            missing.append(f"MR 描述缺少章节：{section}")
    if "Closes #" not in description and "关联 Issue" in description:
        missing.append("MR 描述需要用 Closes #<issue> 或明确链接关联 Issue")
    return missing


def check_documentation_impact(description: str) -> list[str]:
    if "文档影响" not in description:
        return []
    section = description.split("文档影响", 1)[1].split("## ", 1)[0]
    has_updated = "已更新" in section and not re.search(r"已更新[：:]\s*(?:$|-?\s*$)", section, re.MULTILINE)
    has_not_needed = "不需要更新" in section and not re.search(r"不需要更新，?原因[：:]\s*(?:$|-?\s*$)", section, re.MULTILINE)
    has_follow_up = "后续文档 Issue" in section and not re.search(r"后续文档 Issue[：:]\s*(?:$|-?\s*$)", section, re.MULTILINE)
    if not (has_updated or has_not_needed or has_follow_up):
        return ["文档影响章节需要填写已更新、不需要更新原因，或后续文档 Issue"]
    return []


def check_high_risk_ack(
    description: str,
    changed_files: Iterable[str],
    rules: Iterable[dict[str, object]],
) -> list[str]:
    risky = []
    for changed in changed_files:
        for rule in rules:
            paths = [str(item) for item in rule.get("paths", [])]  # type: ignore[union-attr]
            owners = [str(item) for item in rule.get("require_owner_ack", [])]  # type: ignore[union-attr]
            if paths and owners and matches_any_path(changed, paths):
                risky.append(
                    f"{changed.replace('\\', '/')} "
                    f"(rule={rule.get('id', 'unknown')}, owners={','.join(owners)})"
                )

    if risky and "/owner-ack" not in description:
        return [
            "命中高风险路径但缺少 /owner-ack："
            + ", ".join(sorted(set(risky)))
        ]
    return []


def check_secrets(paths: Iterable[Path]) -> list[str]:
    findings = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(f"疑似 secret 出现在 {path}")
                break
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mr-description", help="Path to a markdown MR description.")
    parser.add_argument("--changed-files", help="Path to newline-separated changed files.")
    args = parser.parse_args()

    description = load_text(args.mr_description)
    changed_files = load_changed_files(args.changed_files)
    rules = parse_simple_yaml_rule_map(Path(".ai/rule-map.yml"))

    errors = []
    if description:
        errors.extend(check_required_sections(description))
        errors.extend(check_documentation_impact(description))
        errors.extend(check_high_risk_ack(description, changed_files, rules))
    elif os.environ.get("CI_MERGE_REQUEST_ID"):
        errors.append("CI_MERGE_REQUEST_DESCRIPTION 为空，无法检查 MR 模板。")

    errors.extend(check_secrets(scan_candidate_files(changed_files)))

    if errors:
        print("policy_check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("policy_check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
