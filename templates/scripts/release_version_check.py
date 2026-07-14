#!/usr/bin/env python3
"""Validate a release tag against the configured release note."""

from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from pathlib import Path


SEMVER = (
    r"(?:0|[1-9]\d*)\."
    r"(?:0|[1-9]\d*)\."
    r"(?:0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
)


@dataclass(frozen=True)
class VersioningPolicy:
    scheme: str = "semver"
    tag_pattern: str = "v{version}"
    release_note_pattern: str = "docs/releases/{tag}.md"


def top_level_block(text: str, key: str) -> str:
    match = re.search(
        rf"(?ms)^{re.escape(key)}:\s*\n(.*?)(?=^[A-Za-z0-9_.-]+:\s*(?:#.*)?$|\Z)",
        text,
    )
    return match.group(1) if match else ""


def scalar(block: str, key: str, default: str) -> str:
    match = re.search(rf"(?m)^\s{{2}}{re.escape(key)}:\s*(.+?)\s*$", block)
    if not match:
        return default
    return match.group(1).strip().strip('"').strip("'")


def load_policy(path: Path) -> VersioningPolicy:
    if not path.exists():
        return VersioningPolicy()
    block = top_level_block(path.read_text(encoding="utf-8"), "versioning")
    if not block:
        return VersioningPolicy()
    return VersioningPolicy(
        scheme=scalar(block, "scheme", "semver").lower(),
        tag_pattern=scalar(block, "tag_pattern", "v{version}"),
        release_note_pattern=scalar(
            block, "release_note_pattern", "docs/releases/{tag}.md"
        ),
    )


def resolve_version(tag: str, policy: VersioningPolicy) -> str | None:
    if policy.scheme != "semver" or policy.tag_pattern.count("{version}") != 1:
        return None
    pattern = re.escape(policy.tag_pattern).replace(
        re.escape("{version}"), f"(?P<version>{SEMVER})"
    )
    match = re.fullmatch(pattern, tag)
    return match.group("version") if match else None


def metadata(text: str, key: str) -> str:
    match = re.search(rf"(?mi)^-\s*{re.escape(key)}[:：]\s*(.*?)\s*$", text)
    return match.group(1).strip() if match else ""


def release_version_errors(root: Path, tag: str, policy: VersioningPolicy) -> list[str]:
    errors: list[str] = []
    version = resolve_version(tag, policy)
    if policy.scheme != "semver":
        return [f"不支持的版本方案：{policy.scheme};当前只支持 semver"]
    if policy.tag_pattern.count("{version}") != 1:
        return ["versioning.tag_pattern 必须且只能包含一个 {version}"]
    if version is None:
        return [f"Tag {tag} 不符合 {policy.tag_pattern} 的 SemVer 格式"]

    relative = policy.release_note_pattern.format(tag=tag, version=version)
    note = (root / relative).resolve()
    try:
        note.relative_to(root.resolve())
    except ValueError:
        return ["versioning.release_note_pattern 不能指向项目目录之外"]
    if not note.is_file():
        return [f"发布 Tag {tag} 缺少发布说明：{relative}"]

    text = note.read_text(encoding="utf-8")
    declared = metadata(text, "版本")
    if declared != tag:
        errors.append(f"{relative} 的版本必须是 {tag}，当前为 {declared or '空'}")
    declared_tag = metadata(text, "Tag")
    if declared_tag != tag:
        errors.append(f"{relative} 的 Tag 必须是 {tag}，当前为 {declared_tag or '空'}")
    status = metadata(text, "状态").lower()
    if status not in {"ready", "released"}:
        errors.append(f"{relative} 的状态必须是 ready 或 released，当前为 {status or '空'}")
    for heading in ["范围和包含的 Issue/MR", "验证和测试报告", "发布、监控和回滚"]:
        if not re.search(rf"(?m)^##\s+{re.escape(heading)}\s*$", text):
            errors.append(f"{relative} 缺少章节：{heading}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default=os.environ.get("CI_COMMIT_TAG", ""))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    if not args.tag:
        print("release_version_check skipped: no release tag")
        return 0
    root = args.root.resolve()
    policy = load_policy(root / ".gj" / "workflow.yml")
    errors = release_version_errors(root, args.tag, policy)
    if errors:
        print("release_version_check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"release_version_check passed: {args.tag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
