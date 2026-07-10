from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "context_freshness_check",
    ROOT / "templates" / "scripts" / "context_freshness_check.py",
)
assert SPEC and SPEC.loader
context_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(context_check)


class ContextIndexParsingTests(unittest.TestCase):
    def test_summaries_are_grouped_per_module(self) -> None:
        text = """modules:
  app:
    recent_iteration_summaries:
      - "docs/iterations/v2/ai-context-summary.md"
  billing:
    recent_iteration_summaries:
      - "docs/iterations/v1/ai-context-summary.md"
iteration_policy:
  require_ai_context_summary: true
  max_recent_summaries_per_module: 1
"""
        groups, maximum, required = context_check.parse_context_index(text)
        self.assertEqual(
            [
                ["docs/iterations/v2/ai-context-summary.md"],
                ["docs/iterations/v1/ai-context-summary.md"],
            ],
            groups,
        )
        self.assertEqual(1, maximum)
        self.assertTrue(required)


if __name__ == "__main__":
    unittest.main()
