#!/usr/bin/env python3
"""Install GitLab AI workflow assets into a target repository."""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {"__pycache__", ".pytest_cache"}

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


def backup_path(dest: Path, backup_root: Path, target_root: Path, dry_run: bool) -> None:
    rel = dest.relative_to(target_root)
    backup_dest = backup_root / rel
    print(f"backup {dest} -> {backup_dest}")
    if dry_run:
        return
    backup_dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_dir():
        shutil.copytree(dest, backup_dest)
    else:
        shutil.copy2(dest, backup_dest)


def copy_path(
    src: Path,
    dest: Path,
    target_root: Path,
    force: bool,
    only_missing: bool,
    backup_root: Path | None,
    dry_run: bool,
) -> None:
    if dest.exists() and only_missing:
        if src.is_dir() and dest.is_dir():
            for child in sorted(src.rglob("*")):
                if child.is_dir():
                    continue
                if any(part in SKIP_DIRS for part in child.parts):
                    continue
                child_dest = dest / child.relative_to(src)
                if child_dest.exists():
                    print(f"skip existing {child_dest}")
                else:
                    print(f"copy {child} -> {child_dest}")
                    if not dry_run:
                        child_dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(child, child_dest)
        else:
            print(f"skip existing {dest}")
        return
    if dest.exists() and not force:
        print(f"skip existing {dest}")
        return
    print(f"copy {src} -> {dest}")
    if dry_run:
        return
    if dest.exists():
        if backup_root:
            backup_path(dest, backup_root, target_root, dry_run=False)
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()
    if src.is_dir():
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns(*SKIP_DIRS))
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--only-missing", action="store_true")
    parser.add_argument("--backup", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.force and args.only_missing:
        raise RuntimeError("--force and --only-missing cannot be used together")

    target = args.target.resolve()
    if not target.exists():
        raise FileNotFoundError(target)
    if not (target / ".git").exists():
        raise RuntimeError(f"{target} does not look like a Git repository")

    backup_root = None
    if args.backup:
        timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_root = target / ".gj-workflow-backup" / timestamp

    for src_rel, dest_rel in COPY_PATHS:
        copy_path(
            ROOT / src_rel,
            target / dest_rel,
            target,
            args.force,
            args.only_missing,
            backup_root,
            args.dry_run,
        )
    for src_rel, dest_rel in COPY_FILES:
        copy_path(
            ROOT / src_rel,
            target / dest_rel,
            target,
            args.force,
            args.only_missing,
            backup_root,
            args.dry_run,
        )

    print("workflow install complete")
    if args.force and not args.backup:
        print("warning: --force replaced existing assets without --backup")
    print("next: edit .ai/project.yml and push a branch to run GitLab CI")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
