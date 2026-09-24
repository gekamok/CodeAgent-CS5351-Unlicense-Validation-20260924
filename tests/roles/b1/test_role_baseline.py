"""Executable baseline checks for B1's owned requirement helpers."""

import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def load_plugin_type():
    """Load main.py with minimal AstrBot import stubs for isolated helper tests."""
    astrbot = types.ModuleType("astrbot")
    api = types.ModuleType("astrbot.api")
    event = types.ModuleType("astrbot.api.event")
    star = types.ModuleType("astrbot.api.star")

    class Star:
        def __init__(self, context):
            self.context = context

    class AstrMessageEvent:
        pass

    event.filter = types.SimpleNamespace(
        command=lambda _name: (lambda function: function)
    )
    event.AstrMessageEvent = AstrMessageEvent
    star.Context = type("Context", (), {})
    star.Star = Star
    api.logger = types.SimpleNamespace()
    api.AstrBotConfig = type("AstrBotConfig", (), {})
    astrbot.api = api
    api.event = event
    api.star = star

    stubs = {
        "astrbot": astrbot,
        "astrbot.api": api,
        "astrbot.api.event": event,
        "astrbot.api.star": star,
    }
    source_path = REPOSITORY_ROOT / "main.py"
    module_name = "_b1_main_under_test"
    spec = importlib.util.spec_from_file_location(module_name, source_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load plugin source at {source_path}")
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, stubs):
        sys.modules[module_name] = module
        try:
            spec.loader.exec_module(module)
        finally:
            sys.modules.pop(module_name, None)
    return module.CodeAgentPlugin


class B1RequirementBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plugin_type = load_plugin_type()

    def make_plugin(self, config=None):
        plugin = object.__new__(self.plugin_type)
        plugin.config = config or {}
        return plugin

    def test_extract_requirement_from_plain_and_mentioned_commands(self):
        plugin = self.make_plugin()
        self.assertEqual(
            plugin._extract_requirement("Please /agent build a small parser"),
            "build a small parser",
        )
        self.assertEqual(
            plugin._extract_requirement("@builder/agent build a small parser"),
            "build a small parser",
        )

    def test_extract_requirement_preserves_multiline_text_and_trims_edges(self):
        plugin = self.make_plugin()
        message = "/agent build a parser\nwith escape handling  "
        self.assertEqual(
            plugin._extract_requirement(message),
            "build a parser\nwith escape handling",
        )

    def test_extract_requirement_returns_none_without_nonempty_trigger_text(self):
        plugin = self.make_plugin()
        self.assertIsNone(plugin._extract_requirement("Please build a parser"))
        self.assertIsNone(plugin._extract_requirement("/agent   "))

    def test_extract_requirement_ignores_command_like_path_fragments(self):
        plugin = self.make_plugin()
        self.assertIsNone(
            plugin._extract_requirement("prefix/agent build a parser")
        )
        self.assertIsNone(
            plugin._extract_requirement("mail@builder/agent build a parser")
        )

    def test_extract_requirement_handles_crlf_and_whitespace_before_command(self):
        plugin = self.make_plugin()
        self.assertEqual(
            plugin._extract_requirement(
                "notice\r\n/agent \r\n  add report\r\nwith tests\t "
            ),
            "add report\r\nwith tests",
        )

    def test_extract_requirement_accepts_hyphenated_mention_and_rejects_bad_tokens(self):
        plugin = self.make_plugin()
        self.assertEqual(
            plugin._extract_requirement("@builder-bot/agent\tBuild\r\nit  "),
            "Build\r\nit",
        )
        for message in ("/agentbot build", "@/agent build"):
            with self.subTest(message=message):
                self.assertIsNone(plugin._extract_requirement(message))

    def test_blacklist_checks_admin_and_group_ids_after_string_normalization(self):
        plugin = self.make_plugin(
            {"admin_blacklist": [42], "group_blacklist": ["blocked-room"]}
        )
        self.assertTrue(plugin._is_in_blacklist(42, "safe-room"))
        self.assertTrue(plugin._is_in_blacklist("7", "blocked-room"))
        self.assertFalse(plugin._is_in_blacklist("7", "safe-room"))

    def test_blacklist_empty_configuration_allows_request(self):
        plugin = self.make_plugin(
            {"admin_blacklist": [], "group_blacklist": []}
        )
        self.assertFalse(plugin._is_in_blacklist("42", "room"))

    def test_project_type_selection_keeps_ordered_keyword_rules(self):
        plugin = self.make_plugin()
        self.assertEqual(plugin._assess_project("网页工具")["type"], "web")
        self.assertEqual(
            plugin._assess_project("Please write a JavaScript parser")["type"],
            "js",
        )
        self.assertEqual(
            plugin._assess_project("Create an API endpoint")["type"], "api"
        )

    def test_project_size_boundaries(self):
        plugin = self.make_plugin()
        expected_sizes = {29: "S", 30: "M", 99: "M", 100: "L"}
        for length, expected in expected_sizes.items():
            with self.subTest(length=length):
                self.assertEqual(
                    plugin._assess_project("x" * length)["size"], expected
                )

    def test_project_assessment_ignores_outer_whitespace(self):
        plugin = self.make_plugin()
        padded_short_requirement = "\n  " + "x" * 29 + "\t\n"
        self.assertEqual(plugin._assess_project(padded_short_requirement)["size"], "S")
        self.assertEqual(
            plugin._assess_project("\n  JavaScript parser \t")["type"], "js"
        )

    def test_project_size_boundaries_count_unicode_characters(self):
        plugin = self.make_plugin()
        for length, expected in ((29, "S"), (30, "M"), (99, "M"), (100, "L")):
            with self.subTest(length=length):
                self.assertEqual(
                    plugin._assess_project("界" * length)["size"], expected
                )

    def test_project_type_keyword_after_line_break_is_still_classified(self):
        plugin = self.make_plugin()
        self.assertEqual(
            plugin._assess_project("Please build a\nJavaScript parser")["type"],
            "js",
        )


if __name__ == "__main__":
    unittest.main()
