from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InstallerTests(unittest.TestCase):
    def make_repo(self, parent: Path, name: str) -> Path:
        target = parent / name
        target.mkdir()
        subprocess.run(["git", "init", "--quiet", str(target)], check=True)
        return target

    def install_workflow(self, target: Path) -> None:
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "install_workflow.py"),
                "--target",
                str(target),
            ],
            check=True,
            capture_output=True,
            text=True,
        )

    def test_workflow_installs_all_assets_once(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = self.make_repo(Path(temp), "project")
            self.install_workflow(target)

            self.assertTrue((target / ".ai" / "role-map.yml").exists())
            self.assertTrue((target / "scripts" / "gitlab_api.py").exists())
            self.assertTrue((target / "scripts" / "release_dry_run.py").exists())
            self.assertIn(
                ".ai/gitlab.local.json",
                (target / ".gitignore").read_text(encoding="utf-8"),
            )
            self.assertTrue((target / "docs" / "product" / "requirements" / "PRD.md").exists())
            subprocess.run(
                [sys.executable, "scripts/workflow_assets_check.py"],
                cwd=target,
                check=True,
                capture_output=True,
                text=True,
            )

    def test_skill_installer_installs_complete_set(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "skills"
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "install_skills.py"),
                    "--dest",
                    str(destination),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            installed = {path.name for path in destination.iterdir() if path.is_dir()}
            self.assertEqual(8, len(installed))
            self.assertTrue(
                {"gj-develop-change", "gj-mr-review", "gj-plan-change", "gj-workflow-next"}
                <= installed
            )

    def test_skill_installer_supports_three_agents_from_one_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "project"
            project.mkdir()
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "install_skills.py"),
                    "--agent",
                    "all",
                    "--project-root",
                    str(project),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            shared = project / ".agents" / "skills"
            claude = project / ".claude" / "skills"
            self.assertEqual(8, len([path for path in shared.iterdir() if path.is_dir()]))
            self.assertEqual(8, len([path for path in claude.iterdir() if path.is_dir()]))
            self.assertTrue((shared / "gj-workflow-next" / "SKILL.md").exists())
            self.assertTrue((claude / "gj-workflow-next" / "SKILL.md").exists())

if __name__ == "__main__":
    unittest.main()
