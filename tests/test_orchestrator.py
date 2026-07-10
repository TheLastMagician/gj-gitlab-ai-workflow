from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "orchestrator", ROOT / "orchestrator" / "orchestrator.py"
)
assert SPEC and SPEC.loader
orchestrator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = orchestrator
SPEC.loader.exec_module(orchestrator)


class OrchestratorTest(unittest.TestCase):
    def test_only_simplified_comment_commands_are_public(self) -> None:
        self.assertEqual(
            {
                "/ai-next": "gj-workflow-next",
                "/ai-plan": "gj-plan-change",
                "/ai-develop": "gj-develop-change",
                "/ai-review": "gj-mr-review",
                "/ai-release": "gj-release-readiness",
                "/ai-close": "gj-close-loop",
            },
            orchestrator.COMMAND_TO_SKILL,
        )

    def test_requirement_routes_to_plan(self) -> None:
        route = orchestrator.route_event(
            {"object_kind": "issue", "labels": [{"title": "type-requirement"}]}
        )

        self.assertEqual("gj-plan-change", route.skill)

    def test_bug_requires_flow_before_development(self) -> None:
        pending = orchestrator.route_event(
            {"object_kind": "issue", "labels": [{"title": "type-bug"}]}
        )
        confirmed = orchestrator.route_event(
            {
                "object_kind": "issue",
                "labels": [
                    {"title": "type-bug"},
                    {"title": "flow::standard"},
                ],
            }
        )

        self.assertEqual("gj-workflow-next", pending.skill)
        self.assertEqual("gj-develop-change", confirmed.skill)

    def test_hotfix_and_failed_pipeline_use_new_routes(self) -> None:
        hotfix = orchestrator.route_event(
            {
                "object_kind": "issue",
                "labels": [
                    {"title": "type-hotfix"},
                    {"title": "flow::hotfix"},
                ],
            }
        )
        failed = orchestrator.route_event(
            {"object_kind": "pipeline", "object_attributes": {"status": "failed"}}
        )

        self.assertEqual("gj-develop-change", hotfix.skill)
        self.assertEqual("gj-workflow-next", failed.skill)


if __name__ == "__main__":
    unittest.main()
