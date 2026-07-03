#!/usr/bin/env python3
"""Install bundled GJ workflow skills into a Codex skills directory."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
SKIP_DIRS = {"__pycache__", ".pytest_cache"}


def default_dest() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home) / "skills"
    return Path.home() / ".codex" / "skills"


def copy_tree(src: Path, dest: Path, force: bool, dry_run: bool) -> None:
    if dest.exists() and not force:
        print(f"skip existing {dest}")
        return
    print(f"install {src.name} -> {dest}")
    if dry_run:
        return
    if dest.exists():
        shutil.rmtree(dest)
    ignore = shutil.ignore_patterns(*SKIP_DIRS)
    shutil.copytree(src, dest, ignore=ignore)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dest", type=Path, default=default_dest())
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not SKILLS_ROOT.exists():
        raise FileNotFoundError(SKILLS_ROOT)

    if not args.dry_run:
        args.dest.mkdir(parents=True, exist_ok=True)

    for skill in sorted(path for path in SKILLS_ROOT.iterdir() if path.is_dir()):
        copy_tree(skill, args.dest / skill.name, force=args.force, dry_run=args.dry_run)

    print("skill install complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
