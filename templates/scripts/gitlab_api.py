#!/usr/bin/env python3
"""Call approved GitLab workflow endpoints with project-local credentials."""

from __future__ import annotations

import argparse
import getpass
import json
import os
import re
import stat
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / ".gj" / "gitlab.local.json"
IGNORE_ENTRY = ".gj/gitlab.local.json"
WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
SENSITIVE_PATH_PARTS = {
    "access_tokens",
    "deploy_tokens",
    "hooks",
    "runners",
    "variables",
}


@dataclass(frozen=True)
class GitLabConfig:
    url: str
    project_id: str
    token: str


def resolve_config_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def load_config(
    path: Path = DEFAULT_CONFIG,
    environ: Mapping[str, str] | None = None,
) -> GitLabConfig:
    env = os.environ if environ is None else environ
    data: dict[str, object] = {}
    if path.exists():
        loaded = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(loaded, dict):
            raise RuntimeError(f"GitLab config must be a JSON object: {path}")
        data = loaded

    url = env.get("GITLAB_URL") or str(data.get("gitlab_url", ""))
    project_id = env.get("GITLAB_PROJECT_ID") or str(data.get("project_id", ""))
    token = env.get("GITLAB_TOKEN") or str(data.get("token", ""))
    missing = [
        name
        for name, value in (
            ("gitlab_url", url),
            ("project_id", project_id),
            ("token", token),
        )
        if not value.strip()
    ]
    if missing:
        raise RuntimeError(
            f"GitLab config is missing {', '.join(missing)}; run "
            "`python scripts/gitlab_api.py configure ...`"
        )

    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise RuntimeError("gitlab_url must be an http(s) URL")
    return GitLabConfig(url.rstrip("/"), project_id.strip(), token.strip())


def ensure_gitignore(root: Path = ROOT) -> None:
    path = root / ".gitignore"
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    if IGNORE_ENTRY in {line.strip() for line in lines}:
        return
    prefix = "\n" if lines else ""
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(f"{prefix}# Local GitLab credentials\n{IGNORE_ENTRY}\n")


def write_config(path: Path, config: GitLabConfig, force: bool = False) -> None:
    if path.exists() and not force:
        raise RuntimeError(f"GitLab config already exists: {path}; use --force to replace it")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "gitlab_url": config.url,
        "project_id": config.project_id,
        "token": config.token,
    }
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    try:
        temporary.chmod(stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass
    temporary.replace(path)


def normalize_api_path(raw_path: str, project_id: str) -> str:
    value = raw_path.strip().lstrip("/")
    if value.lower().startswith("api/v4/"):
        value = value[7:]
    if not value or "://" in value or value.startswith("../") or "/../" in value:
        raise RuntimeError("API path must be a relative GitLab v4 path")
    encoded_project = urllib.parse.quote(project_id, safe="")
    return value.replace(":project", encoded_project).replace("{project}", encoded_project)


def endpoint_path(api_path: str) -> str:
    return urllib.parse.unquote(api_path.split("?", 1)[0]).strip("/")


def endpoint_allowed(method: str, api_path: str, project_id: str) -> bool:
    path = endpoint_path(api_path)
    parts = set(path.split("/"))
    if parts & SENSITIVE_PATH_PARTS:
        return False

    project = re.escape(project_id.strip("/"))
    read_patterns = [
        r"user",
        r"users",
        r"todos(?:/\d+)?",
        rf"projects/{project}",
        rf"projects/{project}/issues(?:/\d+)?(?:/notes(?:/\d+)?)?",
        rf"projects/{project}/merge_requests(?:/\d+)?(?:/(?:notes|discussions|pipelines)(?:/\d+)?)?",
        rf"projects/{project}/pipelines(?:/\d+)?(?:/jobs)?",
        rf"projects/{project}/members(?:/all)?(?:/\d+)?",
        rf"projects/{project}/labels(?:/\d+)?",
        rf"projects/{project}/milestones(?:/\d+)?",
    ]
    write_patterns = [
        rf"projects/{project}/issues(?:/\d+)?(?:/notes)?",
        rf"projects/{project}/merge_requests(?:/\d+)?(?:/notes)?",
        rf"projects/{project}/labels(?:/\d+)?",
        rf"projects/{project}/milestones(?:/\d+)?",
    ]
    patterns = read_patterns if method == "GET" else write_patterns
    return any(re.fullmatch(pattern, path) for pattern in patterns)


def remote_identity(remote: str) -> tuple[str, str]:
    value = remote.strip()
    if "://" in value:
        parsed = urllib.parse.urlparse(value)
        host = parsed.hostname or ""
        path = parsed.path
    else:
        match = re.fullmatch(r"(?:[^@]+@)?([^:]+):(.+)", value)
        if not match:
            raise RuntimeError(f"Unsupported Git remote URL: {value}")
        host, path = match.groups()
    normalized_path = path.strip("/")
    if normalized_path.endswith(".git"):
        normalized_path = normalized_path[:-4]
    return host.lower(), normalized_path.lower()


class GitLabClient:
    def __init__(self, config: GitLabConfig) -> None:
        self.config = config

    def request(self, method: str, api_path: str, body: object | None = None) -> object:
        url = f"{self.config.url}/api/v4/{api_path}"
        data = None
        headers = {"PRIVATE-TOKEN": self.config.token}
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                content = response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:1000]
            detail = detail.replace(self.config.token, "<redacted>")
            raise RuntimeError(f"GitLab API {exc.code} for {method} {api_path}: {detail}") from exc
        if not content:
            return {"status": "ok"}
        return json.loads(content.decode("utf-8"))


def configured_project(client: GitLabClient) -> dict[str, object]:
    project_path = normalize_api_path("projects/:project", client.config.project_id)
    project = client.request("GET", project_path)
    if not isinstance(project, dict):
        raise RuntimeError("GitLab project response is not an object")
    return project


def verify_remote_matches(client: GitLabClient, root: Path = ROOT) -> dict[str, object]:
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    remote = result.stdout.strip()
    remote_host, remote_path = remote_identity(remote)
    project = configured_project(client)
    web_url = str(project.get("web_url", ""))
    project_host, project_path = remote_identity(web_url)
    if (remote_host, remote_path) != (project_host, project_path):
        raise RuntimeError(
            "Configured GitLab project does not match git remote origin: "
            f"configured={project_host}/{project_path}, remote={remote_host}/{remote_path}"
        )
    return project


def parse_body(args: argparse.Namespace) -> object | None:
    if args.body_json:
        return json.loads(args.body_json)
    if args.body_file:
        return json.loads(Path(args.body_file).read_text(encoding="utf-8"))
    return None


def print_json(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def command_configure(args: argparse.Namespace, config_path: Path) -> int:
    token = os.environ.get(args.token_env, "")
    if not token:
        token = getpass.getpass("GitLab Access Token: ")
    if not token:
        raise RuntimeError("GitLab token cannot be empty")
    config = GitLabConfig(args.url.rstrip("/"), args.project_id, token)
    write_config(config_path, config, force=args.force)
    ensure_gitignore(ROOT)
    print(f"GitLab config written to {config_path} (token hidden)")
    return 0


def command_doctor(client: GitLabClient) -> int:
    project = verify_remote_matches(client)
    user = client.request("GET", "user")
    if not isinstance(user, dict):
        raise RuntimeError("GitLab user response is not an object")
    print_json(
        {
            "status": "ok",
            "gitlab_url": client.config.url,
            "project_id": client.config.project_id,
            "project_path": project.get("path_with_namespace"),
            "username": user.get("username"),
            "remote_matches": True,
        }
    )
    return 0


def command_request(args: argparse.Namespace, client: GitLabClient) -> int:
    method = args.method.upper()
    raw_path = args.path
    api_path = normalize_api_path(raw_path, client.config.project_id)
    if not endpoint_allowed(method, api_path, client.config.project_id):
        raise RuntimeError(f"Endpoint is not allowed by the workflow helper: {method} {raw_path}")
    if method in WRITE_METHODS:
        if not args.confirm_write:
            raise RuntimeError("Write requests require --confirm-write after human confirmation")
        if ":project" not in raw_path and "{project}" not in raw_path:
            raise RuntimeError("Write paths must use :project or {project}")
        verify_remote_matches(client)
    print_json(client.request(method, api_path, parse_body(args)))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    subparsers = parser.add_subparsers(dest="command", required=True)

    configure = subparsers.add_parser("configure")
    configure.add_argument("--url", required=True)
    configure.add_argument("--project-id", required=True)
    configure.add_argument("--token-env", default="GITLAB_TOKEN")
    configure.add_argument("--force", action="store_true")

    subparsers.add_parser("doctor")

    request = subparsers.add_parser("request")
    request.add_argument("--method", choices=["GET", "POST", "PUT", "PATCH", "DELETE"], default="GET")
    request.add_argument("--path", required=True)
    body = request.add_mutually_exclusive_group()
    body.add_argument("--body-json")
    body.add_argument("--body-file")
    request.add_argument("--confirm-write", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    config_path = resolve_config_path(args.config)
    try:
        if args.command == "configure":
            return command_configure(args, config_path)
        client = GitLabClient(load_config(config_path))
        if args.command == "doctor":
            return command_doctor(client)
        return command_request(args, client)
    except (RuntimeError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"gitlab_api failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
