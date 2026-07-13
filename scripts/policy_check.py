#!/usr/bin/env python3
"""Minimal GitLab MR policy check for the GJ AI workflow.

High-risk rules are read from .gj/workflow.yml when present, so installed
projects control their own risk paths without editing this script.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable


STANDARD_REQUIRED_MR_SECTIONS = [
    "关联 Issue",
    "变更内容",
    "自测结果",
    "风险点",
    "回滚方案",
    "文档影响",
]

FAST_REQUIRED_MR_SECTIONS = [
    "变更内容",
    "自测结果",
    "风险点",
    "文档影响",
]

VALID_FLOWS = {"fast", "standard", "hotfix"}
FLOW_LABELS = {f"flow::{flow}": flow for flow in VALID_FLOWS}

DEFAULT_HIGH_RISK_RULES = [
    {
        "id": "database",
        "paths": ["db/migration/**", "**/migrations/**"],
        "minimum_flow": "standard",
    },
    {
        "id": "security",
        "paths": ["src/**/auth/**", "src/**/permission/**", "orchestrator/**"],
        "minimum_flow": "standard",
    },
    {
        "id": "workflow-policy",
        # Only files that can weaken CI or risk classification force Standard.
        "paths": [
            ".gitlab-ci.yml",
            ".gitlab/gj-workflow-ci.yml",
            "scripts/policy_check.py",
            ".gj/workflow.yml",
        ],
        "minimum_flow": "standard",
    },
]

SECRET_PATTERNS = [
    re.compile(r"glpat-[A-Za-z0-9_.-]{16,}"),
    re.compile(r"(?i)(private[-_ ]?token|api[-_ ]?key|password|secret)\s*[:=]\s*['\"]?[^'\"\s]{8,}"),
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache"}
SKIP_FILES: set[str] = set()
FORBIDDEN_SECRET_PATHS = {".gj/gitlab.local.json"}


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

    diff_base = os.environ.get("CI_MERGE_REQUEST_DIFF_BASE_SHA", "").strip()
    if diff_base and set(diff_base) != {"0"}:
        changed = run_git(["diff", "--name-only", f"{diff_base}...HEAD"])
        if changed:
            return changed

    target = os.environ.get("CI_MERGE_REQUEST_TARGET_BRANCH_NAME", "").strip()
    candidates = [f"origin/{target}" if target else "", "origin/main", "HEAD~1"]
    for base in candidates:
        if not base:
            continue
        changed = run_git(["diff", "--name-only", f"{base}...HEAD"])
        if changed:
            return changed
    return []


def parse_workflow_rules(path: Path) -> list[dict[str, object]]:
    """Parse the small .gj/workflow.yml shape without external dependencies."""
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
                "minimum_flow": "standard",
            }
            rules.append(current)
            list_key = None
            continue
        if current is None:
            continue
        if stripped == "paths:":
            list_key = stripped[:-1]
            current.setdefault(list_key, [])
            continue
        if stripped.startswith("minimum_flow:"):
            current["minimum_flow"] = stripped.split(":", 1)[1].strip().strip('"').strip("'")
            list_key = None
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
    # Scan only this change. Existing repository debt must not block an
    # unrelated MR; a separate security scanner can audit the full repository.
    seen: set[Path] = set()
    files: list[Path] = []
    for item in changed_files:
        path = Path(item)
        if path in seen:
            continue
        seen.add(path)
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        if path.exists() and path.is_file():
            files.append(path)

    return files


def split_sections(description: str) -> dict[str, str]:
    """Map each markdown heading to the body text before the next heading."""
    sections: dict[str, str] = {}
    current: str | None = None
    body: list[str] = []
    for line in description.splitlines():
        heading = re.match(r"#{1,6}\s+(.*)", line)
        if heading:
            if current is not None:
                sections[current] = "\n".join(body)
            current = heading.group(1).strip()
            body = []
        elif current is not None:
            body.append(line)
    if current is not None:
        sections[current] = "\n".join(body)
    return sections


def section_has_content(body: str) -> bool:
    text = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    for line in text.splitlines():
        stripped = line.strip()
        # An unchecked empty checkbox, a bare "Closes #", or a template label
        # with nothing after the colon is template residue, not content.
        if stripped in {"", "- [ ]", "Closes #"}:
            continue
        if re.fullmatch(r"-?\s*(已更新|不需要更新，?原因|后续文档 Issue)[：:]\s*", stripped):
            continue
        compact = stripped.replace(" ", "")
        if compact in {
            "|文档|动作|原因|状态/确认人|",
            "|---|---|---|---|",
            "|||||",
        }:
            continue
        return True
    return False


def resolve_flow(description: str, labels_text: str) -> tuple[str, list[str]]:
    configured = os.environ.get("GJ_WORKFLOW_FLOW", "").strip().lower()
    if configured in VALID_FLOWS:
        return configured, []

    labels = {label.strip().lower() for label in labels_text.split(",") if label.strip()}
    selected = sorted(FLOW_LABELS[label] for label in labels if label in FLOW_LABELS)
    if len(selected) == 1:
        return selected[0], []
    if len(selected) > 1:
        return "standard", [
            "MR 只能选择一个工作流标签：flow::fast、flow::standard、flow::hotfix"
        ]

    return "standard", [
        "MR 缺少工作流标签，请在 Labels 中选择 flow::fast、"
        "flow::standard 或 flow::hotfix"
    ]


def check_required_sections(description: str, flow: str) -> list[str]:
    missing = []
    sections = split_sections(description)
    required = (
        FAST_REQUIRED_MR_SECTIONS
        if flow == "fast"
        else STANDARD_REQUIRED_MR_SECTIONS
    )
    for section in required:
        matched = next((title for title in sections if section in title), None)
        if matched is None:
            missing.append(f"MR 描述缺少章节：{section}")
        elif not section_has_content(sections[matched]):
            missing.append(f"MR 章节内容为空：{section}")
    return missing


def check_issue_link(description: str, flow: str) -> list[str]:
    if flow == "fast":
        return []
    sections = split_sections(description)
    issue_title = next((title for title in sections if "关联 Issue" in title), None)
    issue_body = sections.get(issue_title, "") if issue_title else ""
    if not re.search(r"#\d+", issue_body):
        return ["Standard / Hotfix 的关联 Issue 章节需要填写 #<数字>"]
    return []


def check_risk_flow(
    changed_files: Iterable[str],
    rules: Iterable[dict[str, object]],
    flow: str,
) -> list[str]:
    risky = []
    for changed in changed_files:
        for rule in rules:
            paths = [str(item) for item in rule.get("paths", [])]  # type: ignore[union-attr]
            minimum_flow = str(rule.get("minimum_flow", "standard"))
            if paths and minimum_flow != "fast" and matches_any_path(changed, paths):
                risky.append(
                    f"{changed.replace('\\', '/')} "
                    f"(rule={rule.get('id', 'unknown')}, minimum_flow={minimum_flow})"
                )

    if risky and flow == "fast":
        return [
            "flow::fast 命中高风险路径，请改为 flow::standard 或 flow::hotfix："
            + ", ".join(sorted(set(risky)))
        ]
    return []


def check_secrets(paths: Iterable[Path]) -> list[str]:
    findings = []
    for path in paths:
        normalized = path.as_posix()
        while normalized.startswith("./"):
            normalized = normalized[2:]
        if normalized in FORBIDDEN_SECRET_PATHS or normalized.endswith(
            "/.gj/gitlab.local.json"
        ):
            findings.append(f"本地凭据文件不能提交：{path}")
            continue
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
    parser.add_argument("--labels", help="Comma-separated MR labels; defaults to CI labels.")
    args = parser.parse_args()

    description = load_text(args.mr_description)
    changed_files = load_changed_files(args.changed_files)
    labels_text = args.labels if args.labels is not None else os.environ.get("CI_MERGE_REQUEST_LABELS", "")
    rules = parse_workflow_rules(Path(".gj/workflow.yml"))

    errors = []
    warnings = []
    if description:
        flow, flow_errors = resolve_flow(description, labels_text)
        errors.extend(flow_errors)
        warnings.extend(check_required_sections(description, flow))
        errors.extend(check_issue_link(description, flow))
        errors.extend(check_risk_flow(changed_files, rules, flow))
    elif os.environ.get("CI_MERGE_REQUEST_ID"):
        errors.append("CI_MERGE_REQUEST_DESCRIPTION 为空，无法检查 MR 模板。")

    errors.extend(check_secrets(scan_candidate_files(changed_files)))

    if warnings:
        print("policy_check warnings (advisory):")
        for warning in warnings:
            print(f"- {warning}")

    if errors:
        print("policy_check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("policy_check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
