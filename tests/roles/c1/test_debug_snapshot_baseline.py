"""Executable regression checks for C1's debug and snapshot helpers.

The plugin's owned methods are loaded from main.py with a minimal AstrBot API
stub so these tests exercise the real method bodies without installing or
starting the bot framework.
"""
import importlib.util
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch


def _install_astrbot_stubs():
    astrbot = types.ModuleType("astrbot")
    astrbot.__path__ = []
    api = types.ModuleType("astrbot.api")
    api.__path__ = []
    event = types.ModuleType("astrbot.api.event")
    star = types.ModuleType("astrbot.api.star")

    def command(*_args, **_kwargs):
        return lambda function: function

    event.filter = types.SimpleNamespace(command=command)
    event.AstrMessageEvent = type("AstrMessageEvent", (), {})
    star.Context = type("Context", (), {})
    star.Star = object
    api.logger = types.SimpleNamespace(info=lambda *_: None, warning=lambda *_: None, error=lambda *_: None)
    api.AstrBotConfig = dict
    astrbot.api = api
    api.event = event
    api.star = star
    sys.modules.update({
        "astrbot": astrbot,
        "astrbot.api": api,
        "astrbot.api.event": event,
        "astrbot.api.star": star,
    })


_install_astrbot_stubs()
_REPO_ROOT = Path(__file__).resolve().parents[3]
_SPEC = importlib.util.spec_from_file_location("c1_tested_main", _REPO_ROOT / "main.py")
_MAIN = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _MAIN
_SPEC.loader.exec_module(_MAIN)


class DebugAndSnapshotRegressionTests(unittest.TestCase):
    def setUp(self):
        self._temporary_directory = tempfile.TemporaryDirectory()
        self.plugin = _MAIN.CodeAgentPlugin.__new__(_MAIN.CodeAgentPlugin)
        self.plugin.workspace = Path(self._temporary_directory.name)

    def tearDown(self):
        self._temporary_directory.cleanup()

    def test_analyze_error_uses_last_traceback_frame(self):
        stderr = (
            "Traceback (most recent call last):\n"
            '  File "runner.py", line 2, in main\n'
            '  File "generated.py", line 9, in build\n'
            "ValueError: invalid value\n"
        )

        result = self.plugin._analyze_error(stderr)

        self.assertEqual(result["error_type"], "ValueError")
        self.assertEqual(result["error_line"], 9)
        self.assertEqual(result["error_message"], stderr[:500])

    def test_generate_debug_fix_identifies_missing_import(self):
        for error_type in ("ModuleNotFoundError", "ImportError"):
            with self.subTest(error_type=error_type):
                result = self.plugin._generate_debug_fix({
                    "error_type": error_type,
                    "error_message": "No module named 'tomli'",
                })

                self.assertIn("tomli", result)

    def test_same_tick_snapshots_are_unique_and_latest_can_be_restored(self):
        tick = 1_750_000_000_123_456_789
        with patch.object(_MAIN.time, "time", return_value=1_750_000_000.0), patch.object(
            _MAIN.time, "time_ns", side_effect=[tick, tick]
        ):
            first_path = self.plugin._save_snapshot(
                "session", "build", "first version", [{"name": "app.py"}]
            )
            second_path = self.plugin._save_snapshot(
                "session", "build", "second version", [{"name": "app.py"}]
            )

        self.assertNotEqual(first_path, second_path)
        snapshot_paths = list(
            (self.plugin.workspace / "session" / "snapshots").glob("build_*.json")
        )
        self.assertEqual(len(snapshot_paths), 2)
        self.assertEqual(json.loads(Path(first_path).read_text(encoding="utf-8"))["code"], "first version")
        restored = self.plugin._rollback_to_snapshot("session", "build")
        self.assertEqual(restored["code"], "second version")

    def test_rollback_returns_none_when_step_has_no_snapshot(self):
        self.assertIsNone(self.plugin._rollback_to_snapshot("session", "missing"))

    def test_rollback_skips_invalid_newest_snapshot_and_restores_previous(self):
        snapshot_dir = self.plugin.workspace / "session" / "snapshots"
        snapshot_dir.mkdir(parents=True)
        valid_snapshot = {
            "step": "build",
            "timestamp": 1.0,
            "code": "previous valid code",
            "files": [],
        }
        (snapshot_dir / "build_0001.json").write_text(
            json.dumps(valid_snapshot), encoding="utf-8"
        )
        (snapshot_dir / "build_0002.json").write_text("{", encoding="utf-8")
        (snapshot_dir / "build_0003.json").write_text(
            json.dumps({**valid_snapshot, "code": None}), encoding="utf-8"
        )

        restored = self.plugin._rollback_to_snapshot("session", "build")

        self.assertEqual(restored, valid_snapshot)

    def test_rollback_returns_none_when_candidates_violate_snapshot_contract(self):
        snapshot_dir = self.plugin.workspace / "session" / "snapshots"
        snapshot_dir.mkdir(parents=True)
        valid_shape = {
            "step": "build",
            "timestamp": 1.0,
            "code": "code",
            "files": [],
        }
        invalid_candidates = [
            [],
            {**valid_shape, "step": "different"},
            {**valid_shape, "timestamp": True},
            {**valid_shape, "files": ["not a file record"]},
        ]
        for index, candidate in enumerate(invalid_candidates, start=1):
            (snapshot_dir / f"build_{index:04d}.json").write_text(
                json.dumps(candidate), encoding="utf-8"
            )

        self.assertIsNone(self.plugin._rollback_to_snapshot("session", "build"))

    def test_rollback_returns_none_when_snapshot_file_is_unreadable(self):
        snapshot_dir = self.plugin.workspace / "session" / "snapshots"
        snapshot_dir.mkdir(parents=True)
        (snapshot_dir / "build_0001.json").write_text("{}", encoding="utf-8")

        with patch("builtins.open", side_effect=PermissionError("read denied")):
            restored = self.plugin._rollback_to_snapshot("session", "build")

        self.assertIsNone(restored)

    def test_rollback_ignores_files_for_a_different_step(self):
        snapshot_dir = self.plugin.workspace / "session" / "snapshots"
        snapshot_dir.mkdir(parents=True)
        (snapshot_dir / "other_0001.json").write_text("{}", encoding="utf-8")

        self.assertIsNone(self.plugin._rollback_to_snapshot("session", "build"))

    def test_rollback_returns_none_when_snapshot_path_is_not_a_directory(self):
        snapshot_path = self.plugin.workspace / "session" / "snapshots"
        snapshot_path.parent.mkdir(parents=True)
        snapshot_path.write_text("not a directory", encoding="utf-8")

        self.assertIsNone(self.plugin._rollback_to_snapshot("session", "build"))


if __name__ == "__main__":
    unittest.main()
