from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("policy_check", ROOT / "scripts" / "policy_check.py")
assert SPEC and SPEC.loader
policy_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(policy_check)


def description(flow: str, issue: str = "") -> str:
    return f"""# Merge Request

## 关联 Issue
{issue}

## 变更内容
更新按钮文案。

## 自测结果
单元测试通过。

## 风险点
无已知风险。

## 回滚方案
回滚本 MR。

## 文档影响
不需要更新，原因：不改变持久规则。

## AI 使用范围
未使用。
"""


class PolicyFlowTests(unittest.TestCase):
    def test_fast_allows_mr_without_issue(self) -> None:
        text = description("Fast")
        flow, errors = policy_check.resolve_flow(text, "type-bug,flow::fast")
        self.assertEqual("fast", flow)
        self.assertEqual([], errors)
        self.assertEqual([], policy_check.check_required_sections(text, "fast"))

    def test_standard_requires_issue(self) -> None:
        errors = policy_check.check_required_sections(description("Standard"), "standard")
        self.assertIn("MR 章节内容为空：关联 Issue", errors)
        self.assertIn("MR 描述需要 Closes #<数字> 关联具体 Issue", errors)

    def test_fast_rejects_high_risk_paths(self) -> None:
        rules = [
            {
                "id": "security",
                "paths": ["src/**/auth/**"],
                "minimum_flow": "standard",
            }
        ]
        errors = policy_check.check_risk_flow(
            ["src/app/auth/login.py"], rules, "fast"
        )
        self.assertEqual(1, len(errors))
        self.assertIn("flow::standard 或 flow::hotfix", errors[0])

    def test_standard_accepts_high_risk_paths(self) -> None:
        rules = [
            {
                "id": "security",
                "paths": ["src/**/auth/**"],
                "minimum_flow": "standard",
            }
        ]
        errors = policy_check.check_risk_flow(
            ["src/app/auth/login.py"], rules, "standard"
        )
        self.assertEqual([], errors)

    def test_missing_flow_label_is_rejected(self) -> None:
        flow, errors = policy_check.resolve_flow(description(""), "type-bug")
        self.assertEqual("standard", flow)
        self.assertEqual(1, len(errors))
        self.assertIn("缺少工作流标签", errors[0])

    def test_multiple_flow_labels_are_rejected(self) -> None:
        flow, errors = policy_check.resolve_flow(
            description(""), "flow::fast,flow::standard"
        )
        self.assertEqual("standard", flow)
        self.assertEqual(1, len(errors))
        self.assertIn("只能选择一个", errors[0])

    def test_rule_map_uses_minimum_flow(self) -> None:
        rules = policy_check.parse_simple_yaml_rule_map(ROOT / "templates" / "ai" / "rule-map.yml")

        self.assertTrue(rules)
        self.assertTrue(all(rule.get("minimum_flow") == "standard" for rule in rules))

    def test_local_gitlab_config_is_never_committable(self) -> None:
        findings = policy_check.check_secrets([Path(".ai/gitlab.local.json")])

        self.assertEqual(1, len(findings))
        self.assertIn("本地凭据文件不能提交", findings[0])


if __name__ == "__main__":
    unittest.main()
