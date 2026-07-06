#!/usr/bin/env python3
"""Install GitLab AI workflow assets into a target repository."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

COPY_PATHS = [
    ("templates/gitlab/.gitlab", ".gitlab"),
    ("templates/ai", ".ai"),
    ("templates/docs/context", "docs/context"),
    ("templates/docs/modules", "docs/modules"),
    ("templates/docs/standards", "docs/standards"),
    ("templates/docs/product", "docs/product"),
    ("templates/docs/technical", "docs/technical"),
    ("templates/docs/qa", "docs/qa"),
    ("templates/docs/releases", "docs/releases"),
    ("templates/scripts", "scripts"),
]

COPY_FILES = [
    ("templates/gitlab/.gitlab-ci.yml", ".gitlab-ci.yml"),
    ("CODEOWNERS", "CODEOWNERS"),
]


def copy_path(src: Path, dest: Path, force: bool, dry_run: bool) -> None:
    if dest.exists() and not force:
        print(f"skip existing {dest}")
        return
    print(f"copy {src} -> {dest}")
    if dry_run:
        return
    if dest.exists():
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()
    if src.is_dir():
        shutil.copytree(src, dest)
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    target = args.target.resolve()
    if not target.exists():
        raise FileNotFoundError(target)
    if not (target / ".git").exists():
        raise RuntimeError(f"{target} does not look like a Git repository")

    for src_rel, dest_rel in COPY_PATHS:
        copy_path(ROOT / src_rel, target / dest_rel, args.force, args.dry_run)
    for src_rel, dest_rel in COPY_FILES:
        copy_path(ROOT / src_rel, target / dest_rel, args.force, args.dry_run)

    print("workflow install complete")
    print("next: edit .ai/project.yml and push a branch to run GitLab CI")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
