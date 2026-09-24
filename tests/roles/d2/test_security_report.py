"""Focused regression checks for the D2 security report contract."""

import json
import importlib
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SECURITY_SCRIPTS = REPOSITORY_ROOT / "skills" / "CodeAgent" / "scripts"
sys.path.insert(0, str(SECURITY_SCRIPTS))
sys.path.insert(0, str(REPOSITORY_ROOT))

from codeagent_security import (  # noqa: E402
    RiskLevel,
    SecurityFinding,
    SecurityReport,
)


class SecurityReportSerializationTests(unittest.TestCase):
    def test_json_uses_stable_severity_values_and_includes_summary(self):
        report = SecurityReport(
            file_path="sample.py",
            risk_level=RiskLevel.HIGH,
            passed=False,
            summary="1 high-risk issue",
        )
        report.add_finding(
            SecurityFinding(
                level=RiskLevel.HIGH,
                category="dangerous_pattern",
                message="command execution",
                line=3,
            )
        )

        encoded = json.loads(report.to_json())

        self.assertEqual(encoded["risk_level"], "high")
        self.assertEqual(encoded["findings"][0]["level"], "high")
        self.assertEqual(encoded["summary"], "1 high-risk issue")
        self.assertFalse(encoded["passed"])

    def test_safe_report_json_keeps_the_safe_value_machine_readable(self):
        report = SecurityReport(file_path="safe.py", summary="scan complete")

        encoded = json.loads(report.to_json())

        self.assertEqual(encoded["risk_level"], "safe")
        self.assertEqual(encoded["summary"], "scan complete")


class SecurityScanBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class FilterStub:
            @staticmethod
            def command(*_args, **_kwargs):
                return lambda function: function

        astrbot = types.ModuleType("astrbot")
        astrbot.__path__ = []
        api = types.ModuleType("astrbot.api")
        api.__path__ = []
        api.logger = None
        api.AstrBotConfig = object
        event = types.ModuleType("astrbot.api.event")
        event.filter = FilterStub()
        event.AstrMessageEvent = object
        star = types.ModuleType("astrbot.api.star")
        star.Context = object
        star.Star = object

        modules = {
            "astrbot": astrbot,
            "astrbot.api": api,
            "astrbot.api.event": event,
            "astrbot.api.star": star,
        }
        with patch.dict(sys.modules, modules):
            cls.plugin_class = importlib.import_module("main").CodeAgentPlugin

    def test_wrapper_parses_a_real_high_risk_scanner_result(self):
        plugin = object.__new__(self.plugin_class)
        plugin.scripts_dir = SECURITY_SCRIPTS

        report = plugin._call_security_scan("eval(input())", "python")

        self.assertEqual(report["risk_level"], "critical")
        self.assertFalse(report["passed"])
        self.assertTrue(report["summary"])

    def test_wrapper_fails_closed_when_scanner_is_missing(self):
        plugin = object.__new__(self.plugin_class)
        plugin.scripts_dir = REPOSITORY_ROOT / "missing-d2-security-script"

        report = plugin._call_security_scan("print('safe')", "python")

        self.assertEqual(report["risk_level"], "high")
        self.assertFalse(report["passed"])
        self.assertIn("not found", report["error"])


if __name__ == "__main__":
    unittest.main()
