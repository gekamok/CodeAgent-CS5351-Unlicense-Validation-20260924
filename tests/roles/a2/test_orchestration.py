"""Focused A2 regression tests that do not require a running AstrBot host."""

import asyncio
import importlib.util
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch


def load_plugin_module():
    """Load main.py with the smallest AstrBot API surface used by this plugin."""
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
    spec = importlib.util.spec_from_file_location("a2_plugin_under_test", source)
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, stub_modules):
        spec.loader.exec_module(module)
    return module


PLUGIN_MODULE = load_plugin_module()


class FakeEvent:
    def __init__(self, message, group_id="group", sender_id="user"):
        self.message_str = message
        self._group_id = group_id
        self._sender_id = sender_id

    def get_sender_id(self):
        return self._sender_id

    def get_group_id(self):
        return self._group_id

    @staticmethod
    def plain_result(message):
        return message


class A2OrchestrationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(
            dir=Path(__file__).resolve().parents[3]
        )
        self.addCleanup(self.temp_dir.cleanup)
        self.plugin = PLUGIN_MODULE.CodeAgentPlugin.__new__(
            PLUGIN_MODULE.CodeAgentPlugin
        )
        self.plugin.config = {}
        self.plugin.workspace = Path(self.temp_dir.name)
        self.plugin.active_sessions = {}
        self.plugin.logger = types.SimpleNamespace(
            info=lambda *_args, **_kwargs: None,
            warning=lambda *_args, **_kwargs: None,
            error=lambda *_args, **_kwargs: None,
        )

    @staticmethod
    def collect(async_generator):
        async def collect_results():
            return [item async for item in async_generator]

        return asyncio.run(collect_results())

    def test_factory_accepts_context_with_or_without_configuration(self):
        context = object()
        config = {"quality_threshold": 88}
        previous_cwd = os.getcwd()
        try:
            os.chdir(self.temp_dir.name)
            with (
                patch.object(PLUGIN_MODULE.CodeAgentPlugin, "_ensure_nodejs"),
                patch.object(
                    PLUGIN_MODULE.CodeAgentPlugin, "_ensure_js_dependencies"
                ),
            ):
                configured = PLUGIN_MODULE.get_star(context, config)
                defaults = PLUGIN_MODULE.get_star(context)
            self.assertIs(configured.context, context)
            self.assertIs(configured.config, config)
            self.assertEqual(defaults.config, {})
        finally:
            os.chdir(previous_cwd)

    def test_missing_requirement_prompts_without_opening_session(self):
        replies = self.collect(
            self.plugin.agent_command(FakeEvent("/agent"))
        )
        self.assertEqual(len(replies), 1)
        self.assertIn("请提供具体的需求描述", replies[0])
        self.assertEqual(self.plugin.active_sessions, {})

    def test_blacklisted_user_is_ignored(self):
        self.plugin.config = {"admin_blacklist": ["user"]}
        replies = self.collect(
            self.plugin.agent_command(FakeEvent("/agent build a calculator"))
        )
        self.assertEqual(replies, [])
        self.assertEqual(self.plugin.active_sessions, {})

    def test_duplicate_session_is_refused(self):
        session_id = "group_user"
        self.plugin.active_sessions[session_id] = {"active": True}
        replies = self.collect(
            self.plugin.agent_command(FakeEvent("/agent build a calculator"))
        )
        self.assertEqual(len(replies), 1)
        self.assertIn("已有 Agent 任务", replies[0])
        self.assertEqual(self.plugin.active_sessions[session_id], {"active": True})

    def test_exit_command_removes_active_session_and_workspace(self):
        session_id = "group_user"
        session_dir = self.plugin.workspace / session_id
        session_dir.mkdir()
        (session_dir / "temporary.txt").write_text("temporary", encoding="utf-8")
        self.plugin.active_sessions[session_id] = {"active": True}

        replies = self.collect(
            self.plugin.agent_command(FakeEvent("/exitconver"))
        )

        self.assertEqual(len(replies), 1)
        self.assertIn("已终止 Agent 任务", replies[0])
        self.assertNotIn(session_id, self.plugin.active_sessions)
        self.assertFalse(session_dir.exists())

    def test_terminate_cleans_all_sessions(self):
        session_ids = ("first", "second")
        for session_id in session_ids:
            (self.plugin.workspace / session_id).mkdir()
            self.plugin.active_sessions[session_id] = {"active": True}

        asyncio.run(self.plugin.terminate())

        self.assertEqual(self.plugin.active_sessions, {})
        for session_id in session_ids:
            self.assertFalse((self.plugin.workspace / session_id).exists())


if __name__ == "__main__":
    unittest.main()
