"""Contract tests for the C2 subprocess boundary used to publish archives."""

import importlib.util
import json
import os
import sys
import tempfile
import types
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[3]


def load_plugin_module():
    astrbot = types.ModuleType("astrbot")
    api = types.ModuleType("astrbot.api")
    event_module = types.ModuleType("astrbot.api.event")
    star_module = types.ModuleType("astrbot.api.star")

    class Star:
        def __init__(self, context):
            self.context = context

    class AstrBotConfig(dict):
        pass

    event_module.filter = types.SimpleNamespace(
        command=lambda _name: lambda function: function
    )
    event_module.AstrMessageEvent = object
    star_module.Context = object
    star_module.Star = Star
    api.AstrBotConfig = AstrBotConfig
    api.logger = types.SimpleNamespace(
        info=lambda *_args, **_kwargs: None,
        warning=lambda *_args, **_kwargs: None,
        error=lambda *_args, **_kwargs: None,
    )
    astrbot.api = api
    api.event = event_module
    api.star = star_module
    stub_modules = {
        "astrbot": astrbot,
        "astrbot.api": api,
        "astrbot.api.event": event_module,
        "astrbot.api.star": star_module,
    }
    spec = importlib.util.spec_from_file_location("c2_plugin_under_test", REPO_ROOT / "main.py")
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, stub_modules):
        spec.loader.exec_module(module)
    return module


PLUGIN_MODULE = load_plugin_module()


class PackagerBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(
            prefix="c2-boundary-test-", dir=REPO_ROOT
        )
        self.temp_root = Path(self.temp_dir.name)
        self.previous_cwd = Path.cwd()
        self.addCleanup(self.temp_dir.cleanup)
        self.addCleanup(self._restore_cwd)
        self.plugin = PLUGIN_MODULE.CodeAgentPlugin.__new__(PLUGIN_MODULE.CodeAgentPlugin)
        self.plugin.scripts_dir = REPO_ROOT / "skills" / "CodeAgent" / "scripts"

    def _restore_cwd(self):
        os.chdir(self.previous_cwd)

    def test_real_packager_subprocess_publishes_a_readable_archive(self):
        os.chdir(self.temp_root)
        temp_env = {
            "TEMP": str(self.temp_root),
            "TMP": str(self.temp_root),
        }
        with patch.dict(os.environ, temp_env):
            result = self.plugin._call_packager(
                files=[{"name": "main.py", "content": "print('boundary smoke')\n"}],
                test_files=[{"name": "test_main.py", "content": "def test_smoke(): assert True\n"}],
                name="boundary-project",
            )

        self.assertTrue(result["success"], result["error"])
        self.assertEqual(result["file_count"], 6)
        self.assertGreater(result["size"], 0)
        archive_path = Path(result["zip_path"])
        self.assertTrue(archive_path.is_file())
        with zipfile.ZipFile(archive_path) as archive:
            self.assertIsNone(archive.testzip())
            self.assertIn("boundary-project/src/main.py", archive.namelist())
            self.assertIn("boundary-project/tests/test_main.py", archive.namelist())

    def test_cli_validation_failure_returns_error_without_archive(self):
        os.chdir(self.temp_root)
        temp_env = {
            "TEMP": str(self.temp_root),
            "TMP": str(self.temp_root),
        }
        with patch.dict(os.environ, temp_env):
            result = self.plugin._call_packager(
                files=[{"name": "main.py", "content": 42}],
                name="invalid-project",
            )

        self.assertFalse(result["success"])
        self.assertIn("content must be text", result["error"])
        self.assertEqual(result["zip_path"], "")
        self.assertEqual(list((self.temp_root / "codeagent_workspace" / "archive").glob("*.zip")), [])

    def test_malformed_output_and_non_object_json_fail_closed(self):
        responses = (
            ("not-json", "traceback from child", "Packager returned invalid JSON"),
            (json.dumps(["unexpected"]), "", "not an object"),
            (json.dumps({}), "", "missing a boolean success field"),
        )
        for stdout, stderr, message in responses:
            with self.subTest(stdout=stdout):
                proc = types.SimpleNamespace(returncode=0, stdout=stdout, stderr=stderr)
                with patch.object(PLUGIN_MODULE.subprocess, "run", return_value=proc):
                    result = self.plugin._call_packager(files=[], name="sample")
                self.assertFalse(result["success"])
                self.assertIn(message, result["error"])
                if stderr:
                    self.assertIn(stderr, result["error"])

    def test_inconsistent_success_payloads_fail_closed(self):
        payloads = (
            ({"success": True, "zip_path": "missing.zip", "file_count": 1, "size": 5}, 0,
             "archive is missing"),
            ({"success": True, "zip_path": "sample.zip", "file_count": 1, "size": 5}, 7,
             "exited with code 7"),
            ({"success": True, "zip_path": "sample.zip", "file_count": "1", "size": 5}, 0,
             "invalid archive metadata"),
            ({"success": True, "file_count": 1, "size": 5}, 0, "without an archive path"),
        )
        for payload, returncode, message in payloads:
            with self.subTest(payload=payload, returncode=returncode):
                proc = types.SimpleNamespace(
                    returncode=returncode,
                    stdout=json.dumps(payload),
                    stderr="child diagnostic",
                )
                with patch.object(PLUGIN_MODULE.subprocess, "run", return_value=proc):
                    result = self.plugin._call_packager(files=[], name="sample")
                self.assertFalse(result["success"])
                self.assertIn(message, result["error"])


if __name__ == "__main__":
    unittest.main()
