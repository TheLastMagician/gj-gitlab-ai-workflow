from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "package_open_source", ROOT / "scripts" / "package_open_source.py"
)
assert SPEC and SPEC.loader
package_open_source = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = package_open_source
SPEC.loader.exec_module(package_open_source)


class PackageOpenSourceTest(unittest.TestCase):
    def test_local_gitlab_credentials_are_never_packaged(self) -> None:
        self.assertFalse(package_open_source.should_include(ROOT / ".gj" / "gitlab.local.json"))

    def test_only_git_tracked_files_are_package_candidates(self) -> None:
        result = subprocess.CompletedProcess(
            args=["git", "ls-files"],
            returncode=0,
            stdout=b"README.md\0templates/gj/workflow.yml\0",
        )

        with mock.patch.object(package_open_source.subprocess, "run", return_value=result):
            paths = package_open_source.tracked_files()

        self.assertEqual(
            [ROOT / "README.md", ROOT / "templates/gj/workflow.yml"],
            paths,
        )


if __name__ == "__main__":
    unittest.main()
