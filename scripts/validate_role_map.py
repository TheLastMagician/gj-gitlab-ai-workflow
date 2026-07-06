#!/usr/bin/env python3
"""Validate .ai/role-map.yml placeholders and optional GitLab membership."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path


PLACEHOLDER_RE = re.compile(r"^@[a-z0-9_-]*(owner|lead|developer|reviewer)[a-z0-9_-]*$", re.IGNORECASE)


def parse_role_map(path: Path) -> dict[str, list[str]]:
    if not path.exists():
        raise FileNotFoundError(path)

    roles: dict[str, list[str]] = {}
    current_role: str | None = None
    in_roles = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))

        if stripped == "roles:":
            in_roles = True
            continue
        if not in_roles:
            continue
        if indent == 2 and stripped.endswith(":"):
            current_role = stripped[:-1]
            roles.setdefault(current_role, [])
            continue
        if current_role and "gitlab_users:" in stripped:
            _, value = stripped.split(":", 1)
            users = value.strip()
            if users.startswith("[") and users.endswith("]"):
                users = users[1:-1]
                roles[current_role] = [
                    item.strip().strip('"').strip("'")
                    for item in users.split(",")
                    if item.strip()
                ]

    return roles


def normalize_user(user: str) -> str:
    return user.strip().lstrip("@")


def get_json(url: str, token: str) -> object:
    request = urllib.request.Request(url)
    request.add_header("PRIVATE-TOKEN", token)
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def validate_gitlab_user(
    gitlab_url: str,
    project_id: str,
    token: str,
    username: str,
) -> list[str]:
    errors = []
    base = gitlab_url.rstrip("/")
    encoded_user = urllib.parse.quote(username)
    users_url = f"{base}/api/v4/users?username={encoded_user}"
    users = get_json(users_url, token)
    if not isinstance(users, list) or not users:
        return [f"GitLab user not found: @{username}"]

    user_id = users[0].get("id")
    if not user_id:
        return [f"GitLab user has no id: @{username}"]

    member_url = f"{base}/api/v4/projects/{urllib.parse.quote(project_id, safe='')}/members/all/{user_id}"
    try:
        member = get_json(member_url, token)
    except Exception as exc:  # noqa: BLE001 - keep this dependency-free script simple.
        errors.append(f"GitLab project member check failed for @{username}: {exc}")
    else:
        if not isinstance(member, dict) or member.get("state") != "active":
            errors.append(f"GitLab project member inactive or missing: @{username}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--role-map", type=Path, default=Path(".ai/role-map.yml"))
    parser.add_argument("--gitlab-url", default=os.environ.get("GITLAB_URL", ""))
    parser.add_argument("--project-id", default=os.environ.get("GITLAB_PROJECT_ID", ""))
    parser.add_argument("--token-env", default="GITLAB_TOKEN")
    parser.add_argument("--strict-gitlab", action="store_true")
    parser.add_argument("--allow-placeholders", action="store_true")
    args = parser.parse_args()

    roles = parse_role_map(args.role_map)
    errors: list[str] = []

    if not roles:
        errors.append(f"no roles found in {args.role_map}")

    for role, users in sorted(roles.items()):
        if not users:
            errors.append(f"role has no gitlab_users: {role}")
        for user in users:
            username = normalize_user(user)
            if not username:
                errors.append(f"role has empty GitLab user: {role}")
            elif PLACEHOLDER_RE.match(user) and not args.allow_placeholders:
                errors.append(f"role still uses placeholder user: {role}={user}")

    token = os.environ.get(args.token_env, "")
    has_gitlab_config = bool(args.gitlab_url and args.project_id and token)
    if args.strict_gitlab and not has_gitlab_config:
        errors.append(
            "--strict-gitlab requires --gitlab-url, --project-id, "
            f"and ${args.token_env}"
        )
    if has_gitlab_config:
        for users in roles.values():
            for user in users:
                username = normalize_user(user)
                if username and (args.allow_placeholders or not PLACEHOLDER_RE.match(user)):
                    errors.extend(
                        validate_gitlab_user(
                            args.gitlab_url,
                            args.project_id,
                            token,
                            username,
                        )
                    )

    if errors:
        print("role map validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("role map validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
