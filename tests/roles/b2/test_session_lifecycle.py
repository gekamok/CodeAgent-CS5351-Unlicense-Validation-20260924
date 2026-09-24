"""Focused regression checks for the B2-owned session lifecycle methods."""

import ast
import json
import re
import shutil
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SOURCE_FILE = REPOSITORY_ROOT / "main.py"
B2_METHODS = {
    "_is_exit_command",
    "_sanitize_session_id",
    "_cleanup_session",
    "_create_process_json",
}


def load_owned_methods():
    """Compile the production method bodies without importing AstrBot."""
    source_tree = ast.parse(SOURCE_FILE.read_text(encoding="utf-8"))
    plugin_class = next(
        node
        for node in source_tree.body
        if isinstance(node, ast.ClassDef) and node.name == "CodeAgentPlugin"
    )
    methods = [
        node
        for node in plugin_class.body
        if isinstance(node, ast.FunctionDef) and node.name in B2_METHODS
    ]
    found = {method.name for method in methods}
    if found != B2_METHODS:
        raise AssertionError(f"B2 source methods not found: {sorted(B2_METHODS - found)}")

    extracted_class = ast.ClassDef(
        name="B2Methods",
        bases=[],
        keywords=[],
        body=methods,
        decorator_list=[],
    )
    module = ast.fix_missing_locations(ast.Module(body=[extracted_class], type_ignores=[]))
    namespace = {"Path": Path, "json": json, "re": re, "shutil": shutil, "time": time}
    exec(compile(module, str(SOURCE_FILE), "exec"), namespace)
    return namespace["B2Methods"]


class SessionLifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plugin_type = load_owned_methods()

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT)
        self.workspace = Path(self.temp_dir.name) / "workspace"
        self.workspace.mkdir()
        self.plugin = object.__new__(self.plugin_type)
        self.plugin.workspace = self.workspace

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_exit_command_requires_a_standalone_token(self):
        self.assertTrue(self.plugin._is_exit_command("/exitconver"))
        self.assertTrue(self.plugin._is_exit_command("@bot /EXITCONVER"))
        self.assertFalse(self.plugin._is_exit_command("/exitconversation"))
        self.assertFalse(self.plugin._is_exit_command("quoted: '/exitconver'"))

    def test_session_id_encoding_is_safe_and_collision_resistant(self):
        session_id = self.plugin._sanitize_session_id(r"..\outside", "user/1")
        self.assertRegex(session_id, r"\Ag[A-Za-z0-9_%\-]*_u[A-Za-z0-9_%\-]*\Z")
        self.assertNotIn("/", session_id)
        self.assertNotIn("\\", session_id)
        self.assertNotIn("..", session_id)
        self.assertNotEqual(
            self.plugin._sanitize_session_id("a/b", "c"),
            self.plugin._sanitize_session_id("a%00002fb", "c"),
        )

    def test_cleanup_removes_only_a_safe_child_directory(self):
        session_dir = self.workspace / "g123_u456"
        session_dir.mkdir()
        (session_dir / "temporary.txt").write_text("temporary", encoding="utf-8")
        outside_dir = Path(self.temp_dir.name) / "outside"
        outside_dir.mkdir()
        sentinel = outside_dir / "keep.txt"
        sentinel.write_text("keep", encoding="utf-8")

        self.plugin._cleanup_session("g123_u456")
        self.plugin._cleanup_session("..\\outside")

        self.assertFalse(session_dir.exists())
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")

    def test_cleanup_reports_success_and_removal_failure(self):
        session_dir = self.workspace / "g123_u456"
        session_dir.mkdir()

        self.assertTrue(self.plugin._cleanup_session("g123_u456"))
        self.assertFalse(session_dir.exists())
        self.assertTrue(self.plugin._cleanup_session("g123_u456"))

        session_dir.mkdir()
        with patch("shutil.rmtree", side_effect=PermissionError("cleanup denied")):
            self.assertFalse(self.plugin._cleanup_session("g123_u456"))
        self.assertTrue(session_dir.is_dir())

    def test_cleanup_rejects_malformed_ids_and_non_directory_stale_state(self):
        stale_file = self.workspace / "g123_u456"
        stale_file.write_text("stale", encoding="utf-8")

        self.assertFalse(self.plugin._cleanup_session("..\\outside"))
        self.assertFalse(self.plugin._cleanup_session("g123_u456"))
        self.assertEqual(stale_file.read_text(encoding="utf-8"), "stale")

    def test_cleanup_rejects_resolved_path_escape(self):
        session_dir = self.workspace / "g123_u456"
        session_dir.mkdir()
        outside_dir = Path(self.temp_dir.name) / "outside"
        outside_dir.mkdir()
        sentinel = outside_dir / "keep.txt"
        sentinel.write_text("keep", encoding="utf-8")

        with patch.object(Path, "resolve", side_effect=[self.workspace, outside_dir]):
            self.assertFalse(self.plugin._cleanup_session("g123_u456"))

        self.assertTrue(session_dir.is_dir())
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")

    def test_process_metadata_is_created_inside_workspace(self):
        data = self.plugin._create_process_json("g123_u456", "make a tool", "py", "S")
        process_file = self.workspace / "g123_u456" / "process.json"

        self.assertTrue(process_file.is_file())
        self.assertEqual(json.loads(process_file.read_text(encoding="utf-8")), data)
        self.assertEqual(data["status"], "init")
        self.assertEqual(data["session_id"], "g123_u456")

    def test_process_metadata_rejects_path_traversal(self):
        with self.assertRaises(ValueError):
            self.plugin._create_process_json("..\\outside", "x", "py", "S")
        with self.assertRaises(ValueError):
            self.plugin._create_process_json("CON", "x", "py", "S")
        self.assertFalse((Path(self.temp_dir.name) / "outside").exists())

    def test_process_metadata_rejects_symlink_and_resolved_escape(self):
        with patch.object(Path, "is_symlink", return_value=True):
            with self.assertRaises(ValueError):
                self.plugin._create_process_json("g123_u456", "x", "py", "S")

        outside_dir = Path(self.temp_dir.name) / "outside"
        outside_dir.mkdir()
        with patch.object(Path, "resolve", side_effect=[self.workspace, outside_dir]):
            with self.assertRaises(ValueError):
                self.plugin._create_process_json("g123_u456", "x", "py", "S")
        self.assertFalse((outside_dir / "process.json").exists())


if __name__ == "__main__":
    unittest.main()
