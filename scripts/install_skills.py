#!/usr/bin/env python3
"""Install bundled GJ workflow skills into a skills directory."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
SKIP_DIRS = {"__pycache__", ".pytest_cache"}
SUPPORTED_AGENTS = ("codex", "claude-code", "opencode")


def default_dest() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home) / "skills"
    return Path.home() / ".codex" / "skills"


def agent_dest(agent: str, project_root: Path | None) -> Path:
    if project_root is not None:
        if agent == "claude-code":
            return project_root / ".claude" / "skills"
        return project_root / ".agents" / "skills"

    if agent == "codex":
        return default_dest()
    if agent == "claude-code":
        claude_home = os.environ.get("CLAUDE_CONFIG_DIR")
        return Path(claude_home) / "skills" if claude_home else Path.home() / ".claude" / "skills"

    xdg_config = os.environ.get("XDG_CONFIG_HOME")
    config_home = Path(xdg_config) if xdg_config else Path.home() / ".config"
    return config_home / "opencode" / "skills"


def selected_agents(values: list[str]) -> list[str]:
    if "all" in values:
        return list(SUPPORTED_AGENTS)
    return list(dict.fromkeys(values))


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
    parser.add_argument("--dest", type=Path)
    parser.add_argument(
        "--agent",
        action="append",
        choices=[*SUPPORTED_AGENTS, "all"],
        default=[],
        help="Install for one agent; repeat the option or use 'all'.",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        help="Install project-local skills under this repository.",
    )
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dest and (args.agent or args.project_root):
        parser.error("--dest cannot be combined with --agent or --project-root")
    if args.project_root and not args.agent:
        parser.error("--project-root requires --agent")

    if not SKILLS_ROOT.exists():
        raise FileNotFoundError(SKILLS_ROOT)

    agents = selected_agents(args.agent) if args.agent else ["codex"]
    destinations = (
        [args.dest]
        if args.dest
        else list(dict.fromkeys(agent_dest(agent, args.project_root) for agent in agents))
    )

    skills = sorted(path for path in SKILLS_ROOT.iterdir() if path.is_dir())
    for destination in destinations:
        if not args.dry_run:
            destination.mkdir(parents=True, exist_ok=True)
        for skill in skills:
            copy_tree(skill, destination / skill.name, force=args.force, dry_run=args.dry_run)

    print(
        f"skill install complete (count={len(skills)}, "
        f"targets={len(destinations)}, agents={','.join(agents)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
