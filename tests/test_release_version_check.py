from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "templates" / "scripts" / "release_version_check.py"
if not SCRIPT.exists():
    SCRIPT = ROOT / "scripts" / "release_version_check.py"
SPEC = importlib.util.spec_from_file_location("release_version_check", SCRIPT)
assert SPEC and SPEC.loader
release_version_check = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = release_version_check
SPEC.loader.exec_module(release_version_check)


class ReleaseVersionCheckTest(unittest.TestCase):
    def make_project(self, root: Path, note_version: str = "v1.3.0") -> None:
        (root / ".gj").mkdir(parents=True)
        (root / ".gj" / "workflow.yml").write_text(
            """version: 1
versioning:
  scheme: semver
  tag_pattern: "v{version}"
  release_note_pattern: "docs/releases/{tag}.md"
""",
            encoding="utf-8",
        )
        notes = root / "docs" / "releases"
        notes.mkdir(parents=True)
        (notes / "v1.3.0.md").write_text(
            f"""# Release v1.3.0

## Metadata

- Version: {note_version}
- Tag: v1.3.0
- Status: ready

## Included Issues And MRs

- #123 / !45

## Validation

- passed

## Rollback Plan

- redeploy v1.2.3
""",
            encoding="utf-8",
        )

    def test_matching_semver_tag_and_release_note_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_project(root)
            policy = release_version_check.load_policy(root / ".gj" / "workflow.yml")

            self.assertEqual(
                [], release_version_check.release_version_errors(root, "v1.3.0", policy)
            )

    def test_invalid_tag_is_rejected(self) -> None:
        policy = release_version_check.VersioningPolicy()

        errors = release_version_check.release_version_errors(
            Path.cwd(), "release-1.3", policy
        )

        self.assertTrue(any("SemVer" in error for error in errors))

    def test_release_note_version_must_match_tag(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_project(root, note_version="v1.2.9")
            policy = release_version_check.load_policy(root / ".gj" / "workflow.yml")

            errors = release_version_check.release_version_errors(root, "v1.3.0", policy)

            self.assertTrue(any("Version 必须是 v1.3.0" in error for error in errors))

    def test_missing_release_note_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".gj").mkdir()
            (root / ".gj" / "workflow.yml").write_text(
                "versioning:\n  scheme: semver\n", encoding="utf-8"
            )
            policy = release_version_check.load_policy(root / ".gj" / "workflow.yml")

            errors = release_version_check.release_version_errors(root, "v1.3.0", policy)

            self.assertTrue(any("缺少发布说明" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
