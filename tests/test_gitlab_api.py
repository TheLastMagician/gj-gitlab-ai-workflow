from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("gitlab_api", ROOT / "scripts" / "gitlab_api.py")
assert SPEC and SPEC.loader
gitlab_api = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gitlab_api
SPEC.loader.exec_module(gitlab_api)


class GitLabApiTest(unittest.TestCase):
    def test_loads_local_config_and_allows_environment_override(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "gitlab.local.json"
            path.write_text(
                json.dumps(
                    {
                        "gitlab_url": "https://gitlab.example.com",
                        "project_id": "group/project",
                        "token": "local-token",
                    }
                ),
                encoding="utf-8",
            )
            config = gitlab_api.load_config(path, {"GITLAB_TOKEN": "ci-token"})

        self.assertEqual("https://gitlab.example.com", config.url)
        self.assertEqual("group/project", config.project_id)
        self.assertEqual("ci-token", config.token)

    def test_expands_project_and_rejects_absolute_url(self) -> None:
        self.assertEqual(
            "projects/group%2Fproject/issues?state=opened",
            gitlab_api.normalize_api_path(
                "projects/:project/issues?state=opened", "group/project"
            ),
        )
        with self.assertRaises(RuntimeError):
            gitlab_api.normalize_api_path("https://other.example/api/v4/user", "1")

    def test_endpoint_allowlist_blocks_secrets(self) -> None:
        self.assertTrue(
            gitlab_api.endpoint_allowed(
                "GET", "projects/group%2Fproject/merge_requests/3/discussions", "group/project"
            )
        )
        self.assertTrue(
            gitlab_api.endpoint_allowed(
                "POST", "projects/group%2Fproject/issues/16/notes", "group/project"
            )
        )
        self.assertFalse(
            gitlab_api.endpoint_allowed(
                "GET", "projects/group%2Fproject/variables", "group/project"
            )
        )

    def test_remote_identity_supports_https_and_ssh(self) -> None:
        expected = ("gitlab.example.com", "group/project")
        self.assertEqual(
            expected,
            gitlab_api.remote_identity("https://gitlab.example.com/group/project.git"),
        )
        self.assertEqual(expected, gitlab_api.remote_identity("git@gitlab.example.com:group/project.git"))

    def test_write_requires_explicit_confirmation(self) -> None:
        client = gitlab_api.GitLabClient(
            gitlab_api.GitLabConfig("https://gitlab.example.com", "group/project", "token")
        )
        args = Namespace(
            method="POST",
            path="projects/:project/issues/16/notes",
            body_json='{"body":"test"}',
            body_file=None,
            confirm_write=False,
        )

        with self.assertRaisesRegex(RuntimeError, "--confirm-write"):
            gitlab_api.command_request(args, client)


if __name__ == "__main__":
    unittest.main()
