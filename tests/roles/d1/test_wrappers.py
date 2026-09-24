"""D1 integration contracts for sandbox and checker subprocess wrappers."""

import importlib.util
import json
import subprocess
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


def load_plugin_module():
    astrbot = types.ModuleType("astrbot")
    api = types.ModuleType("astrbot.api")
    event_module = types.ModuleType("astrbot.api.event")
    star_module = types.ModuleType("astrbot.api.star")

    class Filter:
        @staticmethod
        def command(_name):
            return lambda function: function

    class Star:
        def __init__(self, context):
            self.context = context

    class AstrBotConfig(dict):
        pass

    logger = types.SimpleNamespace(
        info=lambda *_args, **_kwargs: None,
        warning=lambda *_args, **_kwargs: None,
        error=lambda *_args, **_kwargs: None,
    )
    event_module.filter = Filter()
    event_module.AstrMessageEvent = object
    star_module.Context = object
    star_module.Star = Star
    api.AstrBotConfig = AstrBotConfig
    api.logger = logger
    astrbot.api = api
    api.event = event_module
    api.star = star_module

    stub_modules = {
        "astrbot": astrbot,
        "astrbot.api": api,
        "astrbot.api.event": event_module,
        "astrbot.api.star": star_module,
    }
    source = Path(__file__).resolve().parents[3] / "main.py"
    spec = importlib.util.spec_from_file_location("d1_plugin_under_test", source)
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, stub_modules):
        spec.loader.exec_module(module)
    return module


PLUGIN_MODULE = load_plugin_module()


class D1WrapperTests(unittest.TestCase):
    def setUp(self):
        self.plugin = PLUGIN_MODULE.CodeAgentPlugin.__new__(
            PLUGIN_MODULE.CodeAgentPlugin
        )
        self.plugin.config = {}
        self.plugin.scripts_dir = (
            Path(__file__).resolve().parents[3]
            / "skills"
            / "CodeAgent"
            / "scripts"
        )

    def test_sandbox_uses_the_running_python_interpreter(self):
        payload = {
            "success": True, "stdout": "ok", "stderr": "", "exit_code": 0, "error": None
        }
        completed = subprocess.CompletedProcess(
            args=[sys.executable],
            returncode=0,
            stdout=json.dumps(payload),
            stderr="",
        )

        with patch.object(PLUGIN_MODULE.subprocess, "run", return_value=completed) as run:
            result = self.plugin._call_sandbox("print('ok')", "session")

        self.assertEqual(run.call_args.args[0][0], sys.executable)
        self.assertEqual(result, payload)

    def test_sandbox_rejects_non_object_json_results(self):
        completed = subprocess.CompletedProcess(
            args=[sys.executable], returncode=0, stdout='[]', stderr=''
        )
        with patch.object(PLUGIN_MODULE.subprocess, "run", return_value=completed):
            result = self.plugin._call_sandbox("print('ok')", "session")

        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Sandbox returned an invalid result")

    def test_sandbox_rejects_success_with_nonzero_exit_code(self):
        payload = {
            "success": True, "stdout": "ok", "stderr": "", "exit_code": 1, "error": None
        }
        completed = subprocess.CompletedProcess(
            args=[sys.executable], returncode=0, stdout=json.dumps(payload), stderr=""
        )
        with patch.object(PLUGIN_MODULE.subprocess, "run", return_value=completed):
            result = self.plugin._call_sandbox("print('ok')", "session")

        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Sandbox returned an inconsistent result")

    def test_missing_checker_script_fails_closed(self):
        self.plugin.scripts_dir = self.plugin.scripts_dir / "missing"

        result = self.plugin._call_js_checker("const x = 1;")

        self.assertFalse(result["passed"])
        self.assertEqual(result["error"], "JS Checker script not found")

    def test_unavailable_node_fails_closed(self):
        with patch.object(
            PLUGIN_MODULE.subprocess, "run", side_effect=FileNotFoundError("node")
        ):
            result = self.plugin._call_js_checker("const x = 1;")

        self.assertFalse(result["passed"])
        self.assertIn("Node.js unavailable", result["error"])

    def test_checker_timeout_fails_closed(self):
        version = subprocess.CompletedProcess(
            args=["node", "-v"], returncode=0, stdout="v26", stderr=""
        )
        timeout = subprocess.TimeoutExpired("node", 60)
        with patch.object(
            PLUGIN_MODULE.subprocess, "run", side_effect=[version, timeout]
        ):
            result = self.plugin._call_js_checker("const x = 1;")

        self.assertFalse(result["passed"])
        self.assertEqual(result["error"], "JS Checker timeout")

    def test_nonzero_checker_exit_cannot_return_a_pass(self):
        version = subprocess.CompletedProcess(
            args=["node", "-v"], returncode=0, stdout="v26", stderr=""
        )
        payload = {"passed": True, "issues": [], "summary": "complete"}
        checker = subprocess.CompletedProcess(
            args=["node", "checker.js"],
            returncode=1,
            stdout=json.dumps(payload),
            stderr="",
        )
        with patch.object(
            PLUGIN_MODULE.subprocess, "run", side_effect=[version, checker]
        ):
            result = self.plugin._call_js_checker("const x = 1;")

        self.assertFalse(result["passed"])
        self.assertEqual(result["error"], "JS Checker exit code 1 contradicts its result")

    def test_checker_rejects_a_pass_with_blocking_findings(self):
        version = subprocess.CompletedProcess(
            args=["node", "-v"], returncode=0, stdout="v26", stderr=""
        )
        payload = {
            "passed": True,
            "issues": [{"level": "high", "message": "unsafe"}],
            "summary": "clean",
        }
        checker = subprocess.CompletedProcess(
            args=["node", "checker.js"],
            returncode=0,
            stdout=json.dumps(payload),
            stderr="",
        )
        with patch.object(
            PLUGIN_MODULE.subprocess, "run", side_effect=[version, checker]
        ):
            result = self.plugin._call_js_checker("const x = 1;")

        self.assertFalse(result["passed"])
        self.assertEqual(
            result["error"], "JS Checker exit code 0 contradicts its result"
        )

    def test_checker_rejects_an_unexpected_process_exit_code(self):
        version = subprocess.CompletedProcess(
            args=["node", "-v"], returncode=0, stdout="v26", stderr=""
        )
        payload = {"passed": False, "issues": [], "summary": "incomplete"}
        checker = subprocess.CompletedProcess(
            args=["node", "checker.js"],
            returncode=2,
            stdout=json.dumps(payload),
            stderr="tool error",
        )
        with patch.object(
            PLUGIN_MODULE.subprocess, "run", side_effect=[version, checker]
        ):
            result = self.plugin._call_js_checker("const x = 1;")

        self.assertFalse(result["passed"])
        self.assertEqual(
            result["error"], "JS Checker exit code 2 contradicts its result"
        )

    def test_invalid_checker_json_fails_closed(self):
        version = subprocess.CompletedProcess(
            args=["node", "-v"], returncode=0, stdout="v26", stderr=""
        )
        checker = subprocess.CompletedProcess(
            args=["node", "checker.js"],
            returncode=0,
            stdout="not json",
            stderr="invalid output",
        )
        with patch.object(
            PLUGIN_MODULE.subprocess, "run", side_effect=[version, checker]
        ):
            result = self.plugin._call_js_checker("const x = 1;")

        self.assertFalse(result["passed"])
        self.assertIn("Expecting value", result["error"])


if __name__ == "__main__":
    unittest.main()
