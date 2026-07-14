from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/gj-workflow-bootstrap/scripts/bootstrap_from_github.py"
SPEC = importlib.util.spec_from_file_location("bootstrap_from_github", SCRIPT)
assert SPEC and SPEC.loader
bootstrap = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bootstrap)


class BootstrapFromGitHubTest(unittest.TestCase):
    def test_archive_url_uses_requested_repository_and_ref(self) -> None:
        self.assertEqual(
            "https://github.com/org/repo/archive/refs/heads/release/v1.zip",
            bootstrap.archive_url("org/repo", "release/v1"),
        )

    def test_safe_extract_rejects_parent_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive_path = root / "bad.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("../outside.txt", "bad")
            with zipfile.ZipFile(archive_path) as archive:
                with self.assertRaises(RuntimeError):
                    bootstrap.safe_extract(archive, root / "extract")

    def test_find_source_root_accepts_github_archive_layout(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            extracted = Path(temp)
            installer = extracted / "repo-main/scripts/install_workflow.py"
            installer.parent.mkdir(parents=True)
            installer.write_text("", encoding="utf-8")

            self.assertEqual(extracted / "repo-main", bootstrap.find_source_root(extracted))

    def test_bootstrap_archive_installs_into_project_without_source_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive_path = root / "source.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.write(
                    ROOT / "scripts/install_workflow.py",
                    "repo-main/scripts/install_workflow.py",
                )
                for path in (ROOT / "templates").rglob("*"):
                    if path.is_file():
                        archive.write(
                            path,
                            (Path("repo-main/templates") / path.relative_to(ROOT / "templates")).as_posix(),
                        )

            target = root / "project"
            target.mkdir()
            subprocess.run(["git", "init", "--quiet", str(target)], check=True)
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--archive-url",
                    archive_path.resolve().as_uri(),
                    "--target",
                    str(target),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertTrue((target / ".gj/workflow.yml").exists())
            self.assertTrue((target / ".gitlab/gj-workflow-ci.yml").exists())
            self.assertTrue((target / "CODEOWNERS").exists())
            self.assertTrue((target / "orchestrator/orchestrator.py").exists())
            self.assertIn(
                ".gitlab/gj-workflow-ci.yml",
                (target / ".gitlab-ci.yml").read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
