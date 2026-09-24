"""Focused regression checks for the D2 security report contract."""

import json
import importlib
import subprocess
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
    CodeSecurityScanner,
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

    def test_scanner_report_declares_schema_and_heuristic_limit(self):
        scanner = CodeSecurityScanner()
        scanner.ruff_checker.check = lambda *_args, **_kwargs: {"error": "not installed"}
        scanner.mypy_checker.check = lambda *_args, **_kwargs: {"error": "not installed"}
        scanner.bandit_checker.check = lambda *_args, **_kwargs: {"error": "not installed"}

        encoded = json.loads(scanner.scan_python("print('ok')").to_json())

        self.assertEqual(encoded["schema_version"], 1)
        self.assertEqual(encoded["scanner_status"]["pattern_checker"], "available")
        self.assertEqual(encoded["scanner_status"]["ruff"], "unavailable")
        self.assertEqual(encoded["scanner_status"]["mypy"], "unavailable")
        self.assertEqual(encoded["scanner_status"]["bandit"], "unavailable")
        self.assertTrue(any("rule completeness" in note for note in encoded["limitations"]))
        self.assertTrue(any("coverage is incomplete" in note for note in encoded["limitations"]))


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
            cls.main_module = importlib.import_module("main")
            cls.plugin_class = cls.main_module.CodeAgentPlugin

    def _call_with_report(self, report_json, returncode=0):
        plugin = object.__new__(self.plugin_class)
        plugin.scripts_dir = SECURITY_SCRIPTS
        process = types.SimpleNamespace(returncode=returncode, stdout=report_json, stderr="")
        with patch.object(self.main_module.subprocess, "run", return_value=process):
            return plugin._call_security_scan("print('ok')", "python")

    @staticmethod
    def _valid_report():
        return {
            "risk_level": "safe",
            "passed": True,
            "findings": [],
            "summary": "scan complete",
        }

    @classmethod
    def _versioned_report(cls):
        return {
            **cls._valid_report(),
            "schema_version": 1,
            "scanner_status": {"pattern_checker": "available", "bandit": "unavailable"},
            "limitations": ["Built-in checks are heuristic."],
        }

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

    def test_wrapper_fails_closed_on_invalid_json(self):
        report = self._call_with_report("{not-json")

        self.assertFalse(report["passed"])
        self.assertIn("Security scan unavailable", report["summary"])

    def test_wrapper_fails_closed_on_invalid_report_schema(self):
        invalid_reports = [
            [],
            {**self._valid_report(), "passed": "true"},
            {**self._valid_report(), "findings": {}},
            {**self._valid_report(), "findings": [{"level": "unknown", "message": "bad"}]},
            {**self._valid_report(), "summary": None},
            {**self._versioned_report(), "schema_version": True},
            {**self._versioned_report(), "schema_version": 2},
            {**self._versioned_report(), "scanner_status": {"bandit": "missing"}},
            {**self._versioned_report(), "scanner_status": {"bandit": []}},
            {**self._versioned_report(), "limitations": [None]},
        ]

        for payload in invalid_reports:
            with self.subTest(payload=payload):
                report = self._call_with_report(json.dumps(payload))

                self.assertFalse(report["passed"])
                self.assertEqual(report["risk_level"], "high")
                self.assertIn("Security scan unavailable", report["summary"])

    def test_wrapper_accepts_a_well_formed_report(self):
        payload = self._valid_report()

        report = self._call_with_report(json.dumps(payload))

        self.assertEqual(report, payload)

    def test_wrapper_accepts_versioned_scanner_metadata(self):
        payload = self._versioned_report()

        report = self._call_with_report(json.dumps(payload))

        self.assertEqual(report, payload)

    def test_wrapper_fails_closed_when_exit_code_conflicts_with_report(self):
        cases = [
            (0, {**self._valid_report(), "passed": False}),
            (1, self._valid_report()),
            (1, {**self._valid_report(), "risk_level": "critical"}),
        ]

        for returncode, payload in cases:
            with self.subTest(returncode=returncode, payload=payload):
                report = self._call_with_report(json.dumps(payload), returncode=returncode)

                self.assertFalse(report["passed"])
                self.assertIn("Security scan unavailable", report["summary"])

    def test_wrapper_fails_closed_on_timeout(self):
        plugin = object.__new__(self.plugin_class)
        plugin.scripts_dir = SECURITY_SCRIPTS
        timeout = subprocess.TimeoutExpired("security scan", 60)
        with patch.object(self.main_module.subprocess, "run", side_effect=timeout):
            report = plugin._call_security_scan("print('ok')", "python")

        self.assertFalse(report["passed"])
        self.assertEqual(report["risk_level"], "high")
        self.assertIn("timed out", report["error"])


if __name__ == "__main__":
    unittest.main()
