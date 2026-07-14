#!/usr/bin/env python3
"""Write a version-aware business-project release dry-run artifact."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from release_version_check import load_policy, release_version_errors, resolve_version


ROOT = Path.cwd().resolve()
REQUIRED_WORKFLOW_ASSETS = [
    ".gj/workflow.yml",
    ".gj/context.yml",
    "docs/context/current-state.md",
    "scripts/release_version_check.py",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="build/release-dry-run.md")
    parser.add_argument("--tag", default=os.environ.get("CI_COMMIT_TAG", ""))
    args = parser.parse_args()

    output = ROOT / args.output
    missing = [path for path in REQUIRED_WORKFLOW_ASSETS if not (ROOT / path).exists()]
    if missing:
        raise RuntimeError(f"release dry run is missing workflow assets: {missing}")

    policy = load_policy(ROOT / ".gj" / "workflow.yml")
    version_lines: list[str] = [f"- 版本方案：`{policy.scheme}`。"]
    findings: list[str] = []
    if args.tag:
        version = resolve_version(args.tag, policy)
        version_lines.append(f"- 发布 Tag：`{args.tag}`。")
        if version:
            relative = policy.release_note_pattern.format(tag=args.tag, version=version)
            version_lines.append(f"- 发布说明：`{relative}`。")
        findings = release_version_errors(ROOT, args.tag, policy)
    else:
        version_lines.extend(
            [
                "- 发布 Tag 尚未锁定；使用 GitLab Milestone 记录目标版本。",
                "- 普通功能 MR 不修改 manifest 或仓库版本。",
            ]
        )
        findings.append("未提供 Tag，未检查 Tag 与发布说明的一致性。")

    finding_lines = (
        [f"- {finding}" for finding in findings]
        if findings
        else ["- 未发现 Tag 与发布说明不一致。"]
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        f"""# 发布预演

## 版本

{chr(10).join(version_lines)}

## 检查结果

{chr(10).join(finding_lines)}

## 必须人工确认的发布检查

- 确认最终 SemVer 和对应的 GitLab Milestone。
- 确认包含的 Issue/MR、测试报告、来源提交和 Pipeline。
- 确认配置、数据、权限、发布、监控和回滚影响。
- 由人决定是否创建并推送发布 Tag。
- 部署后记录实际 Tag、提交、Pipeline、环境和验证结果。
""",
        encoding="utf-8",
    )
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
