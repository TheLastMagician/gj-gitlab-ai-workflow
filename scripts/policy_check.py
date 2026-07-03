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
    "AI 使用范围",
]

HIGH_RISK_PATTERNS = [
    re.compile(r"(^|/)db/(migration|migrations)/", re.IGNORECASE),
    re.compile(r"(^|/)(auth|permission|permissions)(/|$)", re.IGNORECASE),
    re.compile(r"(^|/)orchestrator/", re.IGNORECASE),
    re.compile(r"(^|/)scripts/policy_check\.py$", re.IGNORECASE),
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


def check_high_risk_ack(description: str, changed_files: Iterable[str]) -> list[str]:
    risky = []
    for changed in changed_files:
        normalized = changed.replace("\\", "/")
        if any(pattern.search(normalized) for pattern in HIGH_RISK_PATTERNS):
            risky.append(normalized)

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

    errors = []
    if description:
        errors.extend(check_required_sections(description))
        errors.extend(check_high_risk_ack(description, changed_files))
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
