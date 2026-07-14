#!/usr/bin/env python3
"""Build a distributable source package for the workflow project."""

from __future__ import annotations

import argparse
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_DIRS = {
    ".git",
    ".gj-workflow-backup",
    "__pycache__",
    ".pytest_cache",
    ".idea",
    ".vscode",
    "dist",
    "build",
}
EXCLUDE_FILES = {"gitlab-api.ps1"}
EXCLUDE_PATHS = {Path(".gj/gitlab.local.json")}


def should_include(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if rel in EXCLUDE_PATHS:
        return False
    if any(part in EXCLUDE_DIRS for part in rel.parts):
        return False
    if path.name in EXCLUDE_FILES:
        return False
    return path.is_file()


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    return [
        ROOT / entry.decode("utf-8", errors="surrogateescape")
        for entry in result.stdout.split(b"\0")
        if entry
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(tracked_files()):
            if should_include(path):
                archive.write(path, path.relative_to(ROOT).as_posix())

    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
