#!/usr/bin/env python3
"""Install GJ workflow assets into a target repository without deleting project files."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {"__pycache__", ".pytest_cache"}
GJ_CI_INCLUDE = '.gitlab/gj-workflow-ci.yml'

COPY_PATHS = [
    ("templates/gitlab/.gitlab", ".gitlab"),
    ("templates/gj", ".gj"),
    ("templates/docs/context", "docs/context"),
    ("templates/docs/standards", "docs/standards"),
    ("templates/scripts", "scripts"),
    ("templates/orchestrator", "orchestrator"),
]

COPY_FILES = [("templates/CODEOWNERS", "CODEOWNERS")]
ENSURE_DIRS = [
    "docs/product/requirements",
    "docs/product/designs",
    "docs/product/prototypes",
    "docs/technical/solutions",
    "docs/technical/apis",
    "docs/technical/database",
    "docs/technical/decisions",
    "docs/modules",
    "docs/qa/test-plans",
    "docs/qa/test-reports",
    "docs/releases",
]
GITIGNORE_ENTRIES = [".gj/gitlab.local.json", ".gj-workflow-backup/"]


def same_file(left: Path, right: Path) -> bool:
    return left.read_bytes() == right.read_bytes()


def backup_file(dest: Path, backup_root: Path, target_root: Path) -> None:
    backup_dest = backup_root / dest.relative_to(target_root)
    backup_dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(dest, backup_dest)
    print(f"backup {dest} -> {backup_dest}")


def install_file(
    src: Path,
    dest: Path,
    target_root: Path,
    force: bool,
    backup_root: Path,
    dry_run: bool,
) -> bool:
    if dest.exists():
        if dest.is_dir():
            print(f"conflict: expected file but found directory {dest}")
            return False
        if same_file(src, dest):
            print(f"keep unchanged {dest}")
            return True
        if not force:
            print(f"conflict: keep existing {dest}; rerun with --force to replace this file")
            return False
        print(f"replace {dest} from {src}")
        if dry_run:
            return True
        backup_file(dest, backup_root, target_root)
    else:
        print(f"copy {src} -> {dest}")
        if dry_run:
            return True

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return True


def install_path(
    src: Path,
    dest: Path,
    target_root: Path,
    force: bool,
    backup_root: Path,
    dry_run: bool,
) -> list[Path]:
    conflicts: list[Path] = []
    if src.is_file():
        if not install_file(src, dest, target_root, force, backup_root, dry_run):
            conflicts.append(dest)
        return conflicts

    for child in sorted(path for path in src.rglob("*") if path.is_file()):
        if any(part in SKIP_DIRS for part in child.parts):
            continue
        child_dest = dest / child.relative_to(src)
        if not install_file(child, child_dest, target_root, force, backup_root, dry_run):
            conflicts.append(child_dest)
    return conflicts


def ensure_gitignore_entries(target: Path, dry_run: bool) -> None:
    path = target / ".gitignore"
    existing = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    normalized = {line.strip() for line in existing}
    missing = [entry for entry in GITIGNORE_ENTRIES if entry not in normalized]
    for entry in missing:
        print(f"add gitignore entry {entry} -> {path}")
    if dry_run or not missing:
        return
    prefix = "\n" if existing else ""
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(f"{prefix}# Local GitLab credentials\n")
        for entry in missing:
            handle.write(f"{entry}\n")


def ensure_ci_include(target: Path, backup_root: Path, dry_run: bool) -> bool:
    root_ci = target / ".gitlab-ci.yml"
    include_block = f'include:\n  - local: "{GJ_CI_INCLUDE}"\n'
    if not root_ci.exists():
        print(f"create {root_ci} with GJ workflow include")
        if not dry_run:
            root_ci.write_text(include_block, encoding="utf-8", newline="\n")
        return True

    text = root_ci.read_text(encoding="utf-8")
    if GJ_CI_INCLUDE in text:
        print(f"keep existing GJ workflow include in {root_ci}")
    elif re.search(r"(?m)^include\s*:", text):
        print(f"manual action required: add this entry to the existing include in {root_ci}:")
        print(f'  - local: "{GJ_CI_INCLUDE}"')
        return False
    else:
        print(f"prepend GJ workflow include to {root_ci}")
        if not dry_run:
            backup_file(root_ci, backup_root, target)
            root_ci.write_text(f"{include_block}\n{text}", encoding="utf-8", newline="\n")

    workflow = re.search(
        r"(?ms)^workflow:\s*\n(.*?)(?=^[A-Za-z0-9_.-]+:\s*(?:#.*)?$|\Z)",
        text,
    )
    if workflow and "merge_request_event" not in workflow.group(1):
        print(
            "manual action required: existing workflow.rules must allow "
            "CI_PIPELINE_SOURCE == merge_request_event"
        )
        return False
    return True


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

    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = target / ".gj-workflow-backup" / timestamp
    conflicts: list[Path] = []

    for src_rel, dest_rel in [*COPY_PATHS, *COPY_FILES]:
        conflicts.extend(
            install_path(
                ROOT / src_rel,
                target / dest_rel,
                target,
                args.force,
                backup_root,
                args.dry_run,
            )
        )

    for directory in ENSURE_DIRS:
        destination = target / directory
        print(f"ensure directory {destination}")
        if not args.dry_run:
            destination.mkdir(parents=True, exist_ok=True)

    ensure_gitignore_entries(target, args.dry_run)
    ci_ready = ensure_ci_include(target, backup_root, args.dry_run)

    print("workflow asset installation finished")
    if conflicts:
        print("conflicting files kept unchanged:")
        for conflict in conflicts:
            print(f"- {conflict}")
    if not ci_ready:
        print("workflow install incomplete: GitLab CI include requires manual integration")
        return 2
    print("next: edit .gj/workflow.yml and push an MR to verify the GJ jobs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
