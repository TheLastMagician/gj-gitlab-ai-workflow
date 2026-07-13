from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_skills", ROOT / "scripts" / "validate_skills.py"
)
assert SPEC and SPEC.loader
validate_skills = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_skills)


class ValidateSkillsTest(unittest.TestCase):
    def test_execution_skills_define_document_decisions(self) -> None:
        for name in [
            "gj-plan-change",
            "gj-develop-change",
            "gj-mr-review",
            "gj-release-readiness",
            "gj-close-loop",
        ]:
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=name):
                self.assertIn("documentation decision", text.lower())

    def test_delivery_skills_define_version_lifecycle(self) -> None:
        expected = {
            "gj-workflow-next": "Target release",
            "gj-plan-change": "Target release",
            "gj-develop-change": "do not bump",
            "gj-mr-review": "version traceability",
            "gj-release-readiness": "final SemVer",
            "gj-close-loop": "released Tag",
        }
        for name, phrase in expected.items():
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=name):
                self.assertIn(phrase.lower(), text.lower())

    def test_skill_name_requires_gj_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            skill = Path(temp) / "plan-change"
            (skill / "agents").mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\n"
                "name: plan-change\n"
                "description: Plan a sufficiently described workflow change "
                "for validation without using the required project namespace.\n"
                "---\n",
                encoding="utf-8",
            )
            (skill / "agents" / "openai.yaml").write_text(
                'interface:\n  default_prompt: "Use $plan-change."\n',
                encoding="utf-8",
            )

            errors = validate_skills.validate_skill(skill)

            self.assertTrue(any("gj- prefix" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
