#!/usr/bin/env python3
"""Run the project smoke tests."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEST_COMMAND = f"{sys.executable} -m unittest discover -s tests"


def main() -> int:
    command = os.environ.get("GJ_TEST_COMMAND", DEFAULT_TEST_COMMAND)
    print(f"running smoke test: {command}")
    result = subprocess.run(
        command,
        cwd=ROOT,
        shell=True,
        text=True,
    )
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
