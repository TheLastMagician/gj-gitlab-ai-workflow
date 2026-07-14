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

    def install_workflow(
        self, target: Path, *extra: str, check: bool = True
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "install_workflow.py"),
                "--target",
                str(target),
                *extra,
            ],
            check=check,
            capture_output=True,
            text=True,
        )

    def test_workflow_installs_all_assets_once(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = self.make_repo(Path(temp), "project")
            self.install_workflow(target)

            self.assertTrue((target / ".gj" / "workflow.yml").exists())
            self.assertTrue((target / ".gj" / "context.yml").exists())
            self.assertFalse((target / "docs" / "iterations").exists())
            self.assertFalse((target / "docs" / "codebase").exists())
            context_config = (target / ".gj" / "context.yml").read_text(
                encoding="utf-8"
            )
            self.assertNotIn("recent_" + "iteration_summaries", context_config)
            self.assertNotIn("iteration_" + "policy", context_config)
            self.assertTrue((target / ".gitlab" / "gj-workflow-ci.yml").exists())
            self.assertIn(
                ".gitlab/gj-workflow-ci.yml",
                (target / ".gitlab-ci.yml").read_text(encoding="utf-8"),
            )
            legacy_dir = "." + "ai"
            self.assertFalse((target / legacy_dir).exists())
            workflow = (target / ".gj" / "workflow.yml").read_text(encoding="utf-8")
            self.assertIn("roles:", workflow)
            self.assertIn("rules:", workflow)
            self.assertTrue((target / "scripts" / "gitlab_api.py").exists())
            self.assertTrue((target / "scripts" / "release_dry_run.py").exists())
            self.assertTrue((target / "scripts" / "release_version_check.py").exists())
            self.assertIn(
                ".gj/gitlab.local.json",
                (target / ".gitignore").read_text(encoding="utf-8"),
            )
            self.assertTrue(
                (target / ".gj" / "doc-templates" / "product-requirement.md").exists()
            )
            self.assertFalse(
                (target / "docs" / "product" / "requirements" / "PRD.md").exists()
            )
            governance = (
                target / "docs" / "standards" / "12-context-governance.md"
            ).read_text(encoding="utf-8")
            self.assertIn("阶段、产物和完成门", governance)
            self.assertIn("变更影响决定文档类型", governance)
            self.assertIn("Skill 的文档决策输出", governance)
            development_standard = (
                target / "docs" / "standards" / "01-development-standard.md"
            ).read_text(encoding="utf-8")
            self.assertIn("## 项目技术基线", development_standard)
            self.assertIn("### 前端", development_standard)
            self.assertIn("### 后端", development_standard)
            test_standard = (
                target / "docs" / "standards" / "07-test-standard.md"
            ).read_text(encoding="utf-8")
            self.assertIn("## 项目测试基线", test_standard)
            prd = (
                target / ".gj" / "doc-templates" / "product-requirement.md"
            ).read_text(encoding="utf-8")
            self.assertIn("## 拒绝条件和反例", prd)
            workflow = (target / ".gj" / "workflow.yml").read_text(encoding="utf-8")
            self.assertIn("versioning:", workflow)
            self.assertIn('tag_pattern: "v{version}"', workflow)
            subprocess.run(
                [sys.executable, "scripts/workflow_assets_check.py"],
                cwd=target,
                check=True,
                capture_output=True,
                text=True,
            )
            self.install_workflow(target)

    def test_force_never_deletes_unrelated_project_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = self.make_repo(Path(temp), "existing")
            script = target / "scripts" / "deploy.ps1"
            script.parent.mkdir()
            script.write_text("Write-Output deploy\n", encoding="utf-8")
            context = target / "docs" / "context" / "business.md"
            context.parent.mkdir(parents=True)
            context.write_text("business facts\n", encoding="utf-8")
            root_ci = target / ".gitlab-ci.yml"
            root_ci.write_text("stages: [build, test]\n", encoding="utf-8")

            self.install_workflow(target, "--force")

            self.assertEqual("Write-Output deploy\n", script.read_text(encoding="utf-8"))
            self.assertEqual("business facts\n", context.read_text(encoding="utf-8"))
            ci_text = root_ci.read_text(encoding="utf-8")
            self.assertIn(".gitlab/gj-workflow-ci.yml", ci_text)
            self.assertIn("stages: [build, test]", ci_text)
            backups = list((target / ".gj-workflow-backup").rglob(".gitlab-ci.yml"))
            self.assertEqual(1, len(backups))

    def test_existing_complex_include_requires_manual_merge(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = self.make_repo(Path(temp), "existing")
            root_ci = target / ".gitlab-ci.yml"
            original = "include:\n  - project: company/common-ci\n    file: base.yml\n"
            root_ci.write_text(original, encoding="utf-8")

            result = self.install_workflow(target, check=False)

            self.assertEqual(2, result.returncode)
            self.assertIn("manual action required", result.stdout)
            self.assertEqual(original, root_ci.read_text(encoding="utf-8"))
            self.assertTrue((target / ".gitlab/gj-workflow-ci.yml").exists())
            subprocess.run(
                [sys.executable, "scripts/context_freshness_check.py", "--strict"],
                cwd=target,
                check=True,
                capture_output=True,
                text=True,
            )

    def test_restrictive_workflow_rules_require_manual_merge_request_entry(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = self.make_repo(Path(temp), "existing")
            root_ci = target / ".gitlab-ci.yml"
            root_ci.write_text(
                "workflow:\n  rules:\n    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'\n",
                encoding="utf-8",
            )

            result = self.install_workflow(target, check=False)

            self.assertEqual(2, result.returncode)
            self.assertIn("workflow.rules must allow", result.stdout)
            self.assertIn(
                ".gitlab/gj-workflow-ci.yml", root_ci.read_text(encoding="utf-8")
            )
            subprocess.run(
                [
                    sys.executable,
                    "scripts/validate_role_map.py",
                    "--allow-placeholders",
                ],
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
            installed_text = "\n".join(
                path.read_text(encoding="utf-8")
                for path in destination.rglob("*.md")
            )
            self.assertNotIn("docs/" + "iterations", installed_text)
            self.assertNotIn("ai-context-" + "summary", installed_text)

    def test_optional_templates_are_not_core_gates(self) -> None:
        import importlib.util

        script = ROOT / "templates/scripts/workflow_assets_check.py"
        spec = importlib.util.spec_from_file_location("workflow_assets_check", script)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.assertIn(
            ".gj/doc-templates/product-requirement.md", module.OPTIONAL_ASSETS
        )
        self.assertNotIn(
            ".gj/doc-templates/product-requirement.md", module.CORE_REQUIRED
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
            self.assertTrue(
                (shared / "gj-workflow-bootstrap/scripts/bootstrap_from_github.py").exists()
            )
            self.assertTrue(
                (claude / "gj-workflow-bootstrap/scripts/bootstrap_from_github.py").exists()
            )

if __name__ == "__main__":
    unittest.main()
