#!/usr/bin/env python3
"""Run the demo project's smoke tests."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    test_dir = ROOT / "examples" / "demo-project" / "tests"
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(test_dir)],
        cwd=ROOT,
        text=True,
    )
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
