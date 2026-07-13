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
    def test_context_budget_rejects_too_many_always_load_files(self) -> None:
        text = """global:
  always_load:
    - "docs/context/current-state.md"
    - "docs/context/module-map.md"
    - "docs/context/glossary.md"
    - "docs/context/extra.md"
context_budget:
  max_always_load_files: 3
  max_always_load_chars: 24000
  max_module_docs_per_module: 5
  max_module_context_chars: 40000
"""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for entry in context_check.parse_list_groups(text, "always_load")[0]:
                path = root / entry
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("content", encoding="utf-8")
            errors = context_check.validate_context_budget(text, root)

        self.assertTrue(any("max_always_load_files" in error for error in errors))

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

    def test_template_context_budget_defaults(self) -> None:
        config = ROOT / "templates/gj/context.yml"
        if not config.exists():
            config = ROOT / ".gj/context.yml"
        text = config.read_text(encoding="utf-8")
        budget = context_check.parse_context_budget(text)

        self.assertEqual(3, budget["max_always_load_files"])
        self.assertEqual(24_000, budget["max_always_load_chars"])

    def test_findings_are_advisory_unless_strict(self) -> None:
        self.assertEqual(0, context_check.report_findings(["oversized"], strict=False))
        self.assertEqual(1, context_check.report_findings(["oversized"], strict=True))

    def test_document_contract_rejects_template_name_and_missing_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "docs/product/requirements/PRD.md"
            path.parent.mkdir(parents=True)
            path.write_text("# Placeholder\n", encoding="utf-8")

            errors = context_check.validate_document_contracts(root)

        self.assertTrue(any("通用模板文件" in error for error in errors))
        self.assertTrue(any("Owner" in error for error in errors))

    def test_document_contract_accepts_semantic_current_fact(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "docs/modules/order.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                """# Order

## Metadata

- Owner: order-team
- Status: confirmed
- Source Issue: #9
- Target release: v1.1.0
- Effective from: pending
- Implemented by: !3
- Related documents: docs/product/requirements/order-approval.md
- Last verified: 2026-07-13
""",
                encoding="utf-8",
            )

            errors = context_check.validate_document_contracts(root)

        self.assertEqual([], errors)

    def test_document_contract_requires_tag_named_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "docs/releases/release-note.md"
            path.parent.mkdir(parents=True)
            path.write_text("- Status: ready\n", encoding="utf-8")

            errors = context_check.validate_document_contracts(root)

        self.assertTrue(any("<tag>.md" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
