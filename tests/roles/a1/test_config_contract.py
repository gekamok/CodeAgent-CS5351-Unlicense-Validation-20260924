"""A1 regression checks for plugin identity and configuration contracts.

This suite uses only the Python standard library so it can run before the
host AstrBot runtime is installed.
"""

import ast
import json
import re
import subprocess
import unittest
from pathlib import Path
from unittest.mock import Mock, call, patch


ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = ROOT / "_conf_schema.json"
METADATA_PATH = ROOT / "metadata.yaml"
PYPROJECT_PATH = ROOT / "pyproject.toml"
MAIN_PATH = ROOT / "main.py"

CONFIG_TYPES = {
    "bool": bool,
    "float": float,
    "int": int,
    "list": list,
    "string": str,
}

A1_SETTINGS = {
    "admin_blacklist",
    "group_blacklist",
    "code_running_time",
    "memory_limit",
    "max_file_size",
    "max_debug_rounds",
    "quality_threshold",
}


def read_yaml_scalar(path: Path, key: str) -> str:
    """Read a simple top-level scalar without adding a YAML dependency."""
    match = re.search(
        rf"(?m)^{re.escape(key)}:\s*([^\r\n#]+?)\s*$",
        path.read_text(encoding="utf-8-sig"),
    )
    if not match:
        raise AssertionError(f"Missing top-level YAML scalar: {key}")
    return match.group(1).strip().strip("\"'")


def read_project_scalar(text: str, key: str) -> str:
    """Read a quoted scalar from the TOML [project] section."""
    section = re.search(
        r"(?ms)^\[project\]\s*$([\s\S]*?)(?=^\[|\Z)", text
    )
    if not section:
        raise AssertionError("Missing [project] section in pyproject.toml")
    value = re.search(rf'(?m)^{re.escape(key)}\s*=\s*"([^"]+)"\s*$', section.group(1))
    if not value:
        raise AssertionError(f"Missing quoted project scalar: {key}")
    return value.group(1)


def compile_main_method(method_name: str):
    """Compile one production method, avoiding imports from the host plugin."""
    module = ast.parse(MAIN_PATH.read_text(encoding="utf-8-sig"), filename=str(MAIN_PATH))
    plugin = next(
        node
        for node in module.body
        if isinstance(node, ast.ClassDef) and node.name == "CodeAgentPlugin"
    )
    method = next(
        node
        for node in plugin.body
        if isinstance(node, ast.FunctionDef) and node.name == method_name
    )
    isolated_class = ast.ClassDef(
        name="ConfigReader",
        bases=[],
        keywords=[],
        body=[method],
        decorator_list=[],
    )
    isolated_module = ast.fix_missing_locations(
        ast.Module(body=[isolated_class], type_ignores=[])
    )
    namespace = {"subprocess": subprocess}
    exec(compile(isolated_module, str(MAIN_PATH), "exec"), namespace)
    return namespace["ConfigReader"]


class FakeScriptPath:
    """Minimal pathlib-like objects for dependency setup without filesystem writes."""

    def __init__(self, present_names, name="scripts"):
        self.present_names = present_names
        self.name = name

    def __truediv__(self, child_name):
        return FakeScriptPath(self.present_names, child_name)

    def exists(self):
        return self.name in self.present_names

    def __str__(self):
        return "mock-scripts" if self.name == "scripts" else self.name


class ConfigContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8-sig"))

    def test_plugin_identity_matches_python_package(self):
        project = PYPROJECT_PATH.read_text(encoding="utf-8-sig")
        self.assertEqual(read_yaml_scalar(METADATA_PATH, "name"), read_project_scalar(project, "name"))
        self.assertEqual(read_yaml_scalar(METADATA_PATH, "version"), read_project_scalar(project, "version"))

    def test_schema_entries_have_typed_defaults_and_operator_help(self):
        self.assertTrue(self.schema, "configuration schema must not be empty")
        for key, item in self.schema.items():
            with self.subTest(key=key):
                self.assertIn("type", item)
                self.assertIn("default", item)
                self.assertIn("description", item)
                self.assertIn("hint", item)
                self.assertIn(item["type"], CONFIG_TYPES)
                self.assertIs(type(item["default"]), CONFIG_TYPES[item["type"]])
                self.assertTrue(item["description"].strip())
                self.assertTrue(item["hint"].strip())

    def test_settings_used_by_plugin_have_schema_entries(self):
        self.assertTrue(A1_SETTINGS.issubset(self.schema.keys()))

    def test_get_config_returns_host_value_or_caller_default(self):
        reader_type = compile_main_method("_get_config")
        reader = reader_type()
        reader.config = {"configured": 17}

        self.assertEqual(reader._get_config("configured", 3), 17)
        self.assertEqual(reader._get_config("missing", 3), 3)

    def test_get_config_falls_back_for_missing_or_malformed_values(self):
        reader_type = compile_main_method("_get_config")
        reader = reader_type()

        self.assertEqual(reader._get_config("missing", 3), 3)
        reader.config = None
        self.assertEqual(reader._get_config("configured", 3), 3)
        reader.config = {"configured": None}
        self.assertEqual(reader._get_config("configured", 3), 3)
        reader.config = {"configured": "three"}
        self.assertEqual(reader._get_config("configured", 3), 3)

        class BrokenConfig:
            def get(self, key, default):
                raise RuntimeError("config backend unavailable")

        reader.config = BrokenConfig()
        self.assertEqual(reader._get_config("configured", 3), 3)

    def test_get_config_preserves_valid_falsey_values(self):
        reader_type = compile_main_method("_get_config")
        reader = reader_type()
        reader.config = {"enabled": False, "limit": 0, "items": []}

        self.assertIs(reader._get_config("enabled", True), False)
        self.assertEqual(reader._get_config("limit", 5), 0)
        self.assertEqual(reader._get_config("items", ["fallback"]), [])

    def test_js_dependency_preparation_installs_only_when_needed(self):
        method_type = compile_main_method("_ensure_js_dependencies")
        scripts_dir = FakeScriptPath({"codeagent_js_checker.js", "package.json"})
        harness = method_type()
        harness.scripts_dir = scripts_dir
        harness.logger = Mock()
        node_result = subprocess.CompletedProcess(["node", "-v"], 0)
        npm_result = subprocess.CompletedProcess(
            ["npm", "install", "--production=false"], 0, stdout="", stderr=""
        )

        with patch("subprocess.run", side_effect=[node_result, npm_result]) as run:
            harness._ensure_js_dependencies()

        self.assertEqual(run.call_args_list, [
            call(
                ["node", "-v"],
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            ),
            call(
                ["npm", "install", "--production=false"],
                cwd=str(scripts_dir),
                capture_output=True,
                text=True,
                timeout=180,
            ),
        ])

    def test_js_dependency_preparation_skips_existing_node_modules(self):
        method_type = compile_main_method("_ensure_js_dependencies")
        scripts_dir = FakeScriptPath(
            {"codeagent_js_checker.js", "package.json", "node_modules"}
        )
        harness = method_type()
        harness.scripts_dir = scripts_dir
        harness.logger = Mock()
        node_result = subprocess.CompletedProcess(["node", "-v"], 0)

        with patch("subprocess.run", return_value=node_result) as run:
            harness._ensure_js_dependencies()

        run.assert_called_once_with(
            ["node", "-v"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )

    def test_js_dependency_preparation_reports_missing_node(self):
        method_type = compile_main_method("_ensure_js_dependencies")
        scripts_dir = FakeScriptPath({"codeagent_js_checker.js", "package.json"})
        harness = method_type()
        harness.scripts_dir = scripts_dir
        harness.logger = Mock()

        with patch("subprocess.run", side_effect=FileNotFoundError("node")) as run:
            harness._ensure_js_dependencies()

        run.assert_called_once()
        self.assertEqual(run.call_args.args[0], ["node", "-v"])
        harness.logger.warning.assert_called_once()
        self.assertIn("Node.js executable not found", harness.logger.warning.call_args.args[0])

    def test_js_dependency_preparation_reports_missing_npm(self):
        method_type = compile_main_method("_ensure_js_dependencies")
        scripts_dir = FakeScriptPath({"codeagent_js_checker.js", "package.json"})
        harness = method_type()
        harness.scripts_dir = scripts_dir
        harness.logger = Mock()
        node_result = subprocess.CompletedProcess(["node", "-v"], 0, stdout="v20", stderr="")

        with patch(
            "subprocess.run", side_effect=[node_result, FileNotFoundError("npm")]
        ) as run:
            harness._ensure_js_dependencies()

        self.assertEqual(run.call_count, 2)
        self.assertEqual(run.call_args.args[0], ["npm", "install", "--production=false"])
        harness.logger.warning.assert_called_once()
        self.assertIn("npm executable not found", harness.logger.warning.call_args.args[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
