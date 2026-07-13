from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "templates" / "scripts" / "context_freshness_check.py"
if not SCRIPT.exists():
    SCRIPT = ROOT / "scripts" / "context_freshness_check.py"
SPEC = importlib.util.spec_from_file_location(
    "context_freshness_check",
    SCRIPT,
)
assert SPEC and SPEC.loader
context_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(context_check)


class ContextConfigParsingTests(unittest.TestCase):
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
        groups, maximum, required = context_check.parse_context_config(text)
        self.assertEqual(
            [
                ["docs/iterations/v2/ai-context-summary.md"],
                ["docs/iterations/v1/ai-context-summary.md"],
            ],
            groups,
        )
        self.assertEqual(1, maximum)
        self.assertTrue(required)

    def test_context_budget_rejects_archive_in_always_load(self) -> None:
        text = """global:
  always_load:
    - "docs/context/current-state.md"
    - "docs/context/module-map.md"
    - "docs/context/glossary.md"
    - "docs/iterations/v1/ai-context-summary.md"
context_budget:
  max_always_load_files: 3
  max_always_load_chars: 24000
  max_module_docs_per_module: 5
  max_module_context_chars: 40000
  allow_iteration_archives_in_always_load: false
"""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for entry in context_check.parse_list_groups(text, "always_load")[0]:
                path = root / entry
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("content", encoding="utf-8")
            errors = context_check.validate_context_budget(text, root)

        self.assertTrue(any("max_always_load_files" in error for error in errors))
        self.assertTrue(any("不得包含历史迭代" in error for error in errors))

    def test_context_budget_rejects_oversized_module_bundle(self) -> None:
        text = """modules:
  app:
    docs:
      - "docs/modules/app.md"
context_budget:
  max_module_context_chars: 10
"""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "docs/modules/app.md"
            path.parent.mkdir(parents=True)
            path.write_text("x" * 11, encoding="utf-8")
            errors = context_check.validate_context_budget(text, root)

        self.assertTrue(any("max_module_context_chars=10" in error for error in errors))

    def test_template_defaults_to_one_recent_summary(self) -> None:
        config = ROOT / "templates/gj/context.yml"
        if not config.exists():
            config = ROOT / ".gj/context.yml"
        text = config.read_text(encoding="utf-8")
        _, maximum, _ = context_check.parse_context_config(text)
        budget = context_check.parse_context_budget(text)

        self.assertEqual(1, maximum)
        self.assertEqual(3, budget["max_always_load_files"])
        self.assertEqual(24_000, budget["max_always_load_chars"])

    def test_findings_are_advisory_unless_strict(self) -> None:
        self.assertEqual(0, context_check.report_findings(["oversized"], strict=False))
        self.assertEqual(1, context_check.report_findings(["oversized"], strict=True))


if __name__ == "__main__":
    unittest.main()
