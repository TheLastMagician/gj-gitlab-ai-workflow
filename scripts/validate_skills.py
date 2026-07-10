#!/usr/bin/env python3
"""Validate project-local draft skills without external dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9-]{1,63}$")
REQUIRED_SKILLS = {
    "gj-workflow-bootstrap",
    "gj-codebase-map",
    "gj-workflow-next",
    "gj-plan-change",
    "gj-develop-change",
    "gj-mr-review",
    "gj-release-readiness",
    "gj-close-loop",
}


def validate_catalog(actual: set[str]) -> list[str]:
    path = ROOT / "skills.sh.json"
    if not path.exists():
        return ["missing skills.sh.json package catalog"]
    try:
        catalog = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return [f"invalid skills.sh.json: {exc}"]

    listed = [
        skill
        for grouping in catalog.get("groupings", [])
        for skill in grouping.get("skills", [])
    ]
    errors: list[str] = []
    if len(listed) != len(set(listed)):
        errors.append("skills.sh.json contains duplicate skills")
    missing = sorted(actual - set(listed))
    unknown = sorted(set(listed) - actual)
    if missing:
        errors.append("skills.sh.json is missing: " + ", ".join(missing))
    if unknown:
        errors.append("skills.sh.json contains unknown skills: " + ", ".join(unknown))
    return errors


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("frontmatter is not closed")
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def validate_skill(skill_dir: Path) -> list[str]:
    errors = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_dir.name}: missing SKILL.md"]

    try:
        frontmatter = parse_frontmatter(skill_md)
    except ValueError as exc:
        return [f"{skill_dir.name}: {exc}"]

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if name != skill_dir.name:
        errors.append(f"{skill_dir.name}: frontmatter name does not match folder")
    if not NAME_RE.match(name):
        errors.append(f"{skill_dir.name}: invalid skill name")
    if not name.startswith("gj-"):
        errors.append(f"{skill_dir.name}: skill name must use the gj- prefix")
    if len(description) < 80:
        errors.append(f"{skill_dir.name}: description is too short for reliable trigger")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        errors.append(f"{skill_dir.name}: missing agents/openai.yaml")
    else:
        content = openai_yaml.read_text(encoding="utf-8")
        if "default_prompt:" not in content or f"${skill_dir.name}" not in content:
            errors.append(f"{skill_dir.name}: default_prompt must mention ${skill_dir.name}")

    return errors


def main() -> int:
    if not SKILLS_ROOT.exists():
        print("skills directory is missing")
        return 1

    errors: list[str] = []
    actual = {path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()}
    for name in sorted(REQUIRED_SKILLS - actual):
        errors.append(f"missing required skill: {name}")
    extra = sorted(actual - REQUIRED_SKILLS)
    if extra:
        errors.append("extra skill directories: " + ", ".join(extra))

    for skill_dir in sorted(path for path in SKILLS_ROOT.iterdir() if path.is_dir()):
        errors.extend(validate_skill(skill_dir))
    errors.extend(validate_catalog(actual))

    if errors:
        print("skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("skill validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
