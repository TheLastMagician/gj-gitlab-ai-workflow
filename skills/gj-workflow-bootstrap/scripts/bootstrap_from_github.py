#!/usr/bin/env python3
"""Fetch the trusted GJ workflow source archive and install its project assets."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path


DEFAULT_REPOSITORY = "TheLastMagician/gj-gitlab-ai-workflow"


def archive_url(repository: str, ref: str) -> str:
    safe_repository = repository.strip().strip("/")
    safe_ref = urllib.parse.quote(ref.strip(), safe="/")
    return f"https://github.com/{safe_repository}/archive/refs/heads/{safe_ref}.zip"


def safe_extract(archive: zipfile.ZipFile, destination: Path) -> None:
    root = destination.resolve()
    for member in archive.infolist():
        target = (destination / member.filename).resolve()
        if target != root and root not in target.parents:
            raise RuntimeError(f"unsafe archive member: {member.filename}")
    archive.extractall(destination)


def find_source_root(extracted: Path) -> Path:
    direct = extracted / "scripts" / "install_workflow.py"
    if direct.exists():
        return extracted
    candidates = [
        path.parent.parent
        for path in extracted.glob("*/scripts/install_workflow.py")
        if path.is_file()
    ]
    if len(candidates) != 1:
        raise RuntimeError("archive does not contain one GJ workflow source root")
    return candidates[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, default=Path.cwd())
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY)
    parser.add_argument("--ref", default="main")
    parser.add_argument("--archive-url", help=argparse.SUPPRESS)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    target = args.target.resolve()
    url = args.archive_url or archive_url(args.repository, args.ref)
    print(f"fetch workflow assets from {url}")
    with tempfile.TemporaryDirectory(prefix="gj-workflow-") as temp:
        temp_root = Path(temp)
        archive_path = temp_root / "source.zip"
        urllib.request.urlretrieve(url, archive_path)
        extracted = temp_root / "source"
        extracted.mkdir()
        with zipfile.ZipFile(archive_path) as archive:
            safe_extract(archive, extracted)
        source_root = find_source_root(extracted)
        command = [
            sys.executable,
            str(source_root / "scripts" / "install_workflow.py"),
            "--target",
            str(target),
        ]
        if args.force:
            command.append("--force")
        if args.dry_run:
            command.append("--dry-run")
        return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
