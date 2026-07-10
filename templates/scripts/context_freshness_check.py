#!/usr/bin/env python3
"""Check that durable AI context stays fresh across iterations.

This gate enforces the iteration_policy declared in .ai/context-index.yml:

Structural checks (always enforced):
- Every path listed in recent_iteration_summaries exists.
- recent_iteration_summaries length <= max_recent_summaries_per_module.
- The latest iteration's ai-context-summary.md is the first listed entry.

Release-time checks (enforced once the latest iteration has a non-empty
05-release.md, so mid-iteration MRs are not blocked):
- The latest iteration's ai-context-summary.md exists and has real content.
- docs/context/current-state.md mentions the latest iteration version token
  (e.g. "v1.1"), proving it was rewritten for this iteration.

The YAML parsing below is deliberately minimal (stdlib only, the CI image has
no PyYAML) and only supports the flat structure used by context-index.yml.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTEXT_INDEX = ROOT / ".ai" / "context-index.yml"
CURRENT_STATE = ROOT / "docs" / "context" / "current-state.md"
ITERATIONS_ROOT = ROOT / "docs" / "iterations"

VERSION_TOKEN = re.compile(r"v\d+(?:\.\d+)+")
MIN_SUMMARY_BODY_CHARS = 80


def latest_iteration_dir() -> Path | None:
    if not ITERATIONS_ROOT.exists():
        return None
    candidates = sorted(path for path in ITERATIONS_ROOT.iterdir() if path.is_dir())
    return candidates[-1] if candidates else None


def parse_context_index(text: str) -> tuple[list[list[str]], int | None, bool]:
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


def markdown_body_chars(path: Path) -> int:
    """Count content characters, ignoring headings, comments, and blank lines."""
    count = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("<!--"):
            continue
        count += len(stripped)
    return count


def main() -> int:
    errors: list[str] = []

    if not CONTEXT_INDEX.exists():
        print("context_freshness_check failed:\n- .ai/context-index.yml 不存在")
        return 1

    index_text = CONTEXT_INDEX.read_text(encoding="utf-8")
    summary_groups, max_summaries, require_summary = parse_context_index(index_text)
    iteration = latest_iteration_dir()

    # Structural checks: the index must never reference missing files or
    # exceed its own declared budget.
    for group in summary_groups:
        for entry in group:
            if not (ROOT / entry).exists():
                errors.append(f"context-index.yml 引用的文件不存在：{entry}")
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
                    f"iteration_policy 要求摘要，但 context-index.yml 未引用 {summary_rel}"
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

    if errors:
        print("context_freshness_check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("context_freshness_check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
