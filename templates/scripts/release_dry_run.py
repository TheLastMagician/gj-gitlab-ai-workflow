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
    version_lines: list[str] = [f"- Scheme: `{policy.scheme}`."]
    findings: list[str] = []
    if args.tag:
        version = resolve_version(args.tag, policy)
        version_lines.append(f"- Release tag: `{args.tag}`.")
        if version:
            relative = policy.release_note_pattern.format(tag=args.tag, version=version)
            version_lines.append(f"- Release note: `{relative}`.")
        findings = release_version_errors(ROOT, args.tag, policy)
    else:
        version_lines.extend(
            [
                "- Release tag: not locked; use the GitLab Milestone as the target release.",
                "- No manifest or repository version is bumped during ordinary feature MRs.",
            ]
        )
        findings.append("No Tag supplied; Tag/release-note consistency was not evaluated.")

    finding_lines = (
        [f"- {finding}" for finding in findings]
        if findings
        else ["- No tag/release-note consistency issue found for the supplied input."]
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        f"""# Release Dry Run

## Version

{chr(10).join(version_lines)}

## Findings

{chr(10).join(finding_lines)}

## Required Manual Release Checks

- Confirm the final SemVer and matching GitLab Milestone.
- Confirm included Issues/MRs, test report, source commit, and Pipeline.
- Confirm configuration, data, permission, rollout, monitoring, and rollback impact.
- A human decides whether to create and push the release Tag.
- After deployment, record the actual Tag, commit, Pipeline, environment, and validation.
""",
        encoding="utf-8",
    )
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
