#!/usr/bin/env python3
"""Write a business-project release dry-run artifact."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_WORKFLOW_ASSETS = [
    ".gj/workflow.yml",
    ".gj/context.yml",
    "docs/context/current-state.md",
]
RELEASE_DOCS = [
    "04-test-report.md",
    "05-release.md",
    "ai-context-summary.md",
]


def latest_iteration_dir() -> Path | None:
    iterations_root = ROOT / "docs" / "iterations"
    if not iterations_root.exists():
        return None
    candidates = sorted(path for path in iterations_root.iterdir() if path.is_dir())
    if not candidates:
        return None
    return candidates[-1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="build/release-dry-run.md")
    args = parser.parse_args()

    output = ROOT / args.output
    missing = [path for path in REQUIRED_WORKFLOW_ASSETS if not (ROOT / path).exists()]
    if missing:
        raise RuntimeError(f"release dry run is missing workflow assets: {missing}")

    iteration = latest_iteration_dir()
    release_doc_lines = []
    if iteration is None:
        release_doc_lines.append("- No iteration directory found under `docs/iterations`.")
    else:
        release_doc_lines.append(f"- Latest iteration: `{iteration.relative_to(ROOT)}`.")
        for doc in RELEASE_DOCS:
            state = "present" if (iteration / doc).exists() else "missing"
            release_doc_lines.append(f"- `{doc}`: {state}.")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        f"""# Release Dry Run

## Result

Workflow assets are present. Review the release document status below before a
human-authorized release.

## Release Documents

{chr(10).join(release_doc_lines)}

## Required Manual Release Checks

- Product owner confirms the acceptance criteria are still correct.
- Reviewer confirms the MR can be approved or merged with human authorization.
- QA confirms the latest test report is acceptable.
- DevOps confirms rollback target and previous deployed version are known.
- PM confirms `ai-context-summary.md` is updated after release.
""",
        encoding="utf-8",
    )
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
