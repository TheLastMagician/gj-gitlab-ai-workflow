from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "templates/scripts/workflow_assets_check.py"
SPEC = importlib.util.spec_from_file_location("workflow_assets_check", SCRIPT)
assert SPEC and SPEC.loader
workflow_assets_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(workflow_assets_check)


class WorkflowAssetsCheckTest(unittest.TestCase):
    def test_distributed_ci_has_mr_hard_gates(self) -> None:
        root_ci = (ROOT / "templates/gitlab/.gitlab-ci.yml").read_text(encoding="utf-8")
        gj_ci = (ROOT / "templates/gitlab/.gitlab/gj-workflow-ci.yml").read_text(
            encoding="utf-8"
        )

        self.assertEqual([], workflow_assets_check.root_ci_errors(root_ci))
        self.assertEqual([], workflow_assets_check.gj_ci_errors(gj_ci))

    def test_missing_mr_rule_is_detected(self) -> None:
        gj_ci = (ROOT / "templates/gitlab/.gitlab/gj-workflow-ci.yml").read_text(
            encoding="utf-8"
        )
        broken = gj_ci.replace(
            "    - if: '$CI_PIPELINE_SOURCE == \"merge_request_event\"'\n",
            "",
            1,
        )

        self.assertTrue(workflow_assets_check.gj_ci_errors(broken))


if __name__ == "__main__":
    unittest.main()
