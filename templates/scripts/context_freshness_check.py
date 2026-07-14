#!/usr/bin/env python3
"""Report whether durable AI context stays within its configured boundaries.

The default mode is advisory and exits successfully after printing warnings.
Use --strict for an explicit documentation-governance audit.

Checks:
- always_load stays within its file-count and total-character budget.
- Per-module docs stay within their file-count and total-character budget.
- Every configured document path exists.
- Project fact documents use semantic names, required metadata, and valid states.
- Version evidence is named after a SemVer tag.

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
DEFAULT_MAX_ALWAYS_LOAD_FILES = 3
DEFAULT_MAX_ALWAYS_LOAD_CHARS = 24_000
DEFAULT_MAX_MODULE_DOCS = 5
DEFAULT_MAX_MODULE_CONTEXT_CHARS = 40_000
COMMON_FACT_FIELDS = (
    "负责人",
    "状态",
    "来源 Issue",
    "目标版本",
    "生效范围",
    "实现 MR",
    "相关文档",
    "最后核验日期",
)
FACT_DOC_DIRS = (
    "docs/product/requirements",
    "docs/product/designs",
    "docs/product/prototypes",
    "docs/technical/solutions",
    "docs/technical/apis",
    "docs/technical/database",
    "docs/technical/decisions",
    "docs/modules",
    "docs/qa/test-plans",
)
TEMPLATE_FILENAMES = {
    "PRD.md",
    "product-design.md",
    "prototype-record.md",
    "solution-design.md",
    "test-plan.md",
    "test-report.md",
    "release-note.md",
}
SEMANTIC_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
ADR_NAME = re.compile(r"^ADR-\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
TAG_NAME = re.compile(r"^v\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?\.md$")


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


def markdown_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"^-\s+([^:：]+)[:：]\s*(.*)$", line.strip())
        if match:
            fields[match.group(1).strip()] = match.group(2).strip()
    return fields


def validate_fact_document(path: Path, root: Path) -> list[str]:
    relative = path.relative_to(root).as_posix()
    errors: list[str] = []
    if path.name in TEMPLATE_FILENAMES:
        errors.append(f"项目事实目录含通用模板文件：{relative}")
    decisions_dir = (root / "docs/technical/decisions").resolve()
    pattern = ADR_NAME if decisions_dir in path.resolve().parents else SEMANTIC_NAME
    if not pattern.fullmatch(path.name):
        errors.append(f"项目事实文档未使用语义文件名：{relative}")

    fields = markdown_fields(path.read_text(encoding="utf-8"))
    for field in COMMON_FACT_FIELDS:
        if not fields.get(field):
            errors.append(f"项目事实文档缺少非空元数据 {field}：{relative}")
    status = fields.get("状态")
    if status and status not in {"draft", "confirmed"}:
        errors.append(f"项目事实文档状态非法({status})：{relative}")
    return errors


def validate_evidence_document(
    path: Path,
    root: Path,
    allowed_statuses: set[str],
    required_fields: tuple[str, ...],
) -> list[str]:
    relative = path.relative_to(root).as_posix()
    errors: list[str] = []
    if path.name in TEMPLATE_FILENAMES or not TAG_NAME.fullmatch(path.name):
        errors.append(f"版本证据必须使用 <tag>.md 命名：{relative}")
    fields = markdown_fields(path.read_text(encoding="utf-8"))
    for field in required_fields:
        if not fields.get(field):
            errors.append(f"版本证据缺少非空元数据 {field}：{relative}")
    status = fields.get("状态")
    if status and status not in allowed_statuses:
        errors.append(f"版本证据状态非法({status})：{relative}")
    return errors


def validate_document_contracts(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for directory in FACT_DOC_DIRS:
        base = root / directory
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            errors.extend(validate_fact_document(path, root))

    test_reports = root / "docs/qa/test-reports"
    if test_reports.exists():
        for path in sorted(test_reports.rglob("*.md")):
            errors.extend(
                validate_evidence_document(
                    path,
                    root,
                    {"draft", "passed", "failed", "blocked"},
                    (
                        "负责人",
                        "状态",
                        "版本",
                        "Tag",
                        "提交",
                        "Pipeline",
                        "环境",
                        "关联 Issue/MR",
                        "相关文档",
                        "最后核验日期",
                    ),
                )
            )

    releases = root / "docs/releases"
    if releases.exists():
        for path in sorted(releases.rglob("*.md")):
            errors.extend(
                validate_evidence_document(
                    path,
                    root,
                    {"draft", "ready", "released", "rolled-back"},
                    (
                        "负责人",
                        "状态",
                        "版本",
                        "Tag",
                        "来源提交",
                        "Pipeline",
                        "里程碑",
                        "发布 Issue",
                        "相关文档",
                        "最后核验日期",
                    ),
                )
            )
    return errors


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
    errors.extend(validate_context_budget(config_text))
    errors.extend(validate_document_contracts())

    return report_findings(errors, args.strict)


if __name__ == "__main__":
    sys.exit(main())
