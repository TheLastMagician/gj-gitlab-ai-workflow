#!/usr/bin/env python3
"""Write a CI workflow summary artifact."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        """# CI Workflow Summary

## Pipeline Stages

1. policy: flow label, MR evidence, changed-file risk, and secret checks.
2. workflow: orchestrator routing and workflow contract checks.
3. test: demo project smoke tests.
4. package: full skill package validation and open-source package artifact.
5. release: release checklist dry run.

## Demo Flow Covered

- GitLab labels, milestone, issues, notes, and MR are recorded in `examples/demo-run/`.
- The order approval demo verifies submit, approve, reject, self-approval blocking, and repeated approval blocking.
- The eight cross-agent workflow skills are validated as repository artifacts.
""",
        encoding="utf-8",
    )
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
