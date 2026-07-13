#!/usr/bin/env python3
"""Report whether durable AI context stays fresh across iterations.

The default mode is advisory and exits successfully after printing warnings.
Use --strict for an explicit documentation-governance audit.

This gate enforces the iteration_policy declared in .gj/context.yml:

Structural checks (always enforced):
- always_load stays within its file-count and total-character budget.
- always_load never points into docs/iterations.
- Per-module docs stay within their file-count and total-character budget.
- Every path listed in recent_iteration_summaries exists.
- recent_iteration_summaries length <= max_recent_summaries_per_module.
- The latest iteration's ai-context-summary.md is the first listed entry.

Release-time checks (enforced once the latest iteration has a non-empty
05-release.md, so mid-iteration MRs are not blocked):
- The latest iteration's ai-context-summary.md exists and has real content.
- docs/context/current-state.md mentions the latest iteration version token
  (e.g. "v1.1"), proving it was rewritten for this iteration.

The YAML parsing below is deliberately minimal (stdlib only, the CI image has
no PyYAML) and only supports the flat structure used by .gj/context.yml.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTEXT_CONFIG = ROOT / ".gj" / "context.yml"
CURRENT_STATE = ROOT / "docs" / "context" / "current-state.md"
ITERATIONS_ROOT = ROOT / "docs" / "iterations"

VERSION_TOKEN = re.compile(r"v\d+(?:\.\d+)+")
MIN_SUMMARY_BODY_CHARS = 80
DEFAULT_MAX_ALWAYS_LOAD_FILES = 3
DEFAULT_MAX_ALWAYS_LOAD_CHARS = 24_000
DEFAULT_MAX_MODULE_DOCS = 5
DEFAULT_MAX_MODULE_CONTEXT_CHARS = 40_000


def latest_iteration_dir() -> Path | None:
    if not ITERATIONS_ROOT.exists():
        return None
    candidates = sorted(path for path in ITERATIONS_ROOT.iterdir() if path.is_dir())
    return candidates[-1] if candidates else None


def parse_context_config(text: str) -> tuple[list[list[str]], int | None, bool]:
    """Extract per-module summaries and the iteration policy."""
    summary_groups: list[list[str]] = []
    current_group: list[str] | None = None
    in_summaries = False
    summaries_indent = 0
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))
        if stripped.startswith("recent_iteration_summaries:"):
            in_summaries = True
            summaries_indent = indent
            current_group = []
            summary_groups.append(current_group)
            continue
        if in_summaries:
            if indent > summaries_indent and stripped.startswith("- "):
                assert current_group is not None
                current_group.append(stripped[2:].strip().strip('"').strip("'"))
                continue
            if stripped and indent <= summaries_indent and not stripped.startswith("#"):
                in_summaries = False

    max_match = re.search(r"max_recent_summaries_per_module:\s*(\d+)", text)
    max_summaries = int(max_match.group(1)) if max_match else None
    require_match = re.search(r"require_ai_context_summary:\s*(true|false)", text, re.IGNORECASE)
    require_summary = bool(require_match and require_match.group(1).lower() == "true")
    return summary_groups, max_summaries, require_summary


def parse_list_groups(text: str, key: str) -> list[list[str]]:
    """Extract YAML list groups for one exact key using the supported shape."""
    groups: list[list[str]] = []
    current: list[str] | None = None
    in_group = False
    group_indent = 0
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))
        if stripped == f"{key}:":
            in_group = True
            group_indent = indent
            current = []
            groups.append(current)
            continue
        if in_group:
            if indent > group_indent and stripped.startswith("- "):
                assert current is not None
                current.append(stripped[2:].strip().strip('"').strip("'"))
                continue
            if stripped and indent <= group_indent and not stripped.startswith("#"):
                in_group = False
    return groups


def parse_context_budget(text: str) -> dict[str, int | bool]:
    def integer(name: str, default: int) -> int:
        match = re.search(rf"{name}:\s*(\d+)", text)
        return int(match.group(1)) if match else default

    archive_match = re.search(
        r"allow_iteration_archives_in_always_load:\s*(true|false)",
        text,
        re.IGNORECASE,
    )
    return {
        "max_always_load_files": integer(
            "max_always_load_files", DEFAULT_MAX_ALWAYS_LOAD_FILES
        ),
        "max_always_load_chars": integer(
            "max_always_load_chars", DEFAULT_MAX_ALWAYS_LOAD_CHARS
        ),
        "max_module_docs_per_module": integer(
            "max_module_docs_per_module", DEFAULT_MAX_MODULE_DOCS
        ),
        "max_module_context_chars": integer(
            "max_module_context_chars", DEFAULT_MAX_MODULE_CONTEXT_CHARS
        ),
        "allow_iteration_archives_in_always_load": bool(
            archive_match and archive_match.group(1).lower() == "true"
        ),
    }


def listed_file_chars(root: Path, entries: list[str], errors: list[str]) -> int:
    total = 0
    for entry in entries:
        path = root / entry
        if not path.exists():
            errors.append(f".gj/context.yml 引用的文件不存在：{entry}")
            continue
        if path.is_file():
            total += len(path.read_text(encoding="utf-8"))
    return total


def validate_context_budget(text: str, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    budget = parse_context_budget(text)
    always_groups = parse_list_groups(text, "always_load")
    always_load = always_groups[0] if always_groups else []
    if len(always_load) > budget["max_always_load_files"]:
        errors.append(
            f"always_load 有 {len(always_load)} 个文件，超过 "
            f"max_always_load_files={budget['max_always_load_files']}"
        )
    if not budget["allow_iteration_archives_in_always_load"]:
        archived = [entry for entry in always_load if entry.startswith("docs/iterations/")]
        if archived:
            errors.append("always_load 不得包含历史迭代文档：" + ", ".join(archived))
    always_chars = listed_file_chars(root, always_load, errors)
    if always_chars > budget["max_always_load_chars"]:
        errors.append(
            f"always_load 总字符数 {always_chars}，超过 "
            f"max_always_load_chars={budget['max_always_load_chars']}"
        )

    for group in parse_list_groups(text, "docs"):
        if len(group) > budget["max_module_docs_per_module"]:
            errors.append(
                f"某模块 docs 有 {len(group)} 个文件，超过 "
                f"max_module_docs_per_module={budget['max_module_docs_per_module']}"
            )
        module_chars = listed_file_chars(root, group, errors)
        if module_chars > budget["max_module_context_chars"]:
            errors.append(
                f"某模块 docs 总字符数 {module_chars}，超过 "
                f"max_module_context_chars={budget['max_module_context_chars']}"
            )
    return errors


def markdown_body_chars(path: Path) -> int:
    """Count content characters, ignoring headings, comments, and blank lines."""
    count = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("<!--"):
            continue
        count += len(stripped)
    return count


def report_findings(errors: list[str], strict: bool) -> int:
    if not errors:
        print("context_freshness_check passed")
        return 0
    heading = "context_freshness_check failed" if strict else "context_freshness_check warnings"
    print(f"{heading}:")
    for error in errors:
        print(f"- {error}")
    if not strict:
        print("advisory only; rerun with --strict to use a non-zero exit code")
    return 1 if strict else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []

    if not CONTEXT_CONFIG.exists():
        return report_findings([".gj/context.yml 不存在"], args.strict)

    config_text = CONTEXT_CONFIG.read_text(encoding="utf-8")
    summary_groups, max_summaries, require_summary = parse_context_config(config_text)
    iteration = latest_iteration_dir()
    errors.extend(validate_context_budget(config_text))

    # Structural checks: the index must never reference missing files or
    # exceed its own declared budget.
    for group in summary_groups:
        for entry in group:
            if not (ROOT / entry).exists():
                errors.append(f".gj/context.yml 引用的文件不存在：{entry}")
        if max_summaries is not None and len(group) > max_summaries:
            errors.append(
                f"某模块 recent_iteration_summaries 有 {len(group)} 条，"
                f"超过 max_recent_summaries_per_module={max_summaries}，"
                "请在迭代收尾时修剪旧条目"
            )

    if iteration is not None:
        summary_path = iteration / "ai-context-summary.md"
        summary_rel = summary_path.relative_to(ROOT).as_posix()
        release_doc = iteration / "05-release.md"
        releasing = release_doc.exists() and markdown_body_chars(release_doc) > 0

        first_entries = [group[0] for group in summary_groups if group]
        if first_entries and summary_rel not in first_entries:
            errors.append(
                f"至少一个模块的 recent_iteration_summaries 首条应为最新迭代的 "
                f"{summary_rel}"
            )

        # Release-time checks: once the release doc is written, the writeback
        # must be complete before the iteration can close.
        if releasing:
            listed_summaries = {entry for group in summary_groups for entry in group}
            if require_summary and summary_rel not in listed_summaries:
                errors.append(
                    f"iteration_policy 要求摘要，但 .gj/context.yml 未引用 {summary_rel}"
                )
            if not summary_path.exists():
                errors.append(f"最新迭代缺少 {summary_rel}")
            elif markdown_body_chars(summary_path) < MIN_SUMMARY_BODY_CHARS:
                errors.append(f"{summary_rel} 内容为空或过短，回写未完成")

            version = VERSION_TOKEN.search(iteration.name)
            if version and CURRENT_STATE.exists():
                if version.group(0) not in CURRENT_STATE.read_text(encoding="utf-8"):
                    errors.append(
                        f"docs/context/current-state.md 未提及最新迭代版本 "
                        f"{version.group(0)}，请覆盖重写以反映当前事实"
                    )

    return report_findings(errors, args.strict)


if __name__ == "__main__":
    sys.exit(main())
