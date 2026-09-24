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

    def test_unrelated_message_is_not_dispatched(self):
        replies = self.collect(self.plugin.agent_command(FakeEvent("hello")))
        self.assertEqual(replies, [])
        self.assertEqual(self.plugin.active_sessions, {})

    def test_blacklisted_user_is_ignored(self):
        self.plugin.config = {"admin_blacklist": ["user"]}
        replies = self.collect(
            self.plugin.agent_command(FakeEvent("/agent build a calculator"))
        )
        self.assertEqual(replies, [])
        self.assertEqual(self.plugin.active_sessions, {})

    def test_duplicate_session_is_refused(self):
        session_id = self.plugin._sanitize_session_id("group", "user")
        self.plugin.active_sessions[session_id] = {"active": True}
        replies = self.collect(
            self.plugin.agent_command(FakeEvent("/agent build a calculator"))
        )
        self.assertEqual(len(replies), 1)
        self.assertIn("已有 Agent 任务", replies[0])
        self.assertEqual(self.plugin.active_sessions[session_id], {"active": True})

    def test_closed_response_stream_releases_started_session(self):
        async def exercise():
            stream = self.plugin.agent_command(
                FakeEvent("/agent build a calculator")
            )
            self.assertIn("正在分析需求", await anext(stream))
            self.assertIn("需求分析完成", await anext(stream))
            self.assertIn("开始编写核心代码", await anext(stream))

            session_id = next(iter(self.plugin.active_sessions))
            session_dir = self.plugin.workspace / session_id
            self.assertTrue((session_dir / "process.json").is_file())

            await stream.aclose()

            self.assertEqual(self.plugin.active_sessions, {})
            self.assertFalse(session_dir.exists())

        asyncio.run(exercise())

    def test_error_response_stream_close_cleans_failed_session(self):
        async def exercise():
            def fail_assessment(_requirement):
                session_id = next(iter(self.plugin.active_sessions))
                session_dir = self.plugin.workspace / session_id
                session_dir.mkdir()
                (session_dir / "partial.txt").write_text(
                    "partial work", encoding="utf-8"
                )
                raise RuntimeError("assessment unavailable")

            stream = self.plugin.agent_command(
                FakeEvent("/agent build a calculator")
            )
            self.assertIn("正在分析需求", await anext(stream))
            with patch.object(
                self.plugin, "_assess_project", side_effect=fail_assessment
            ):
                error_reply = await anext(stream)
            self.assertIn("执行出错: assessment unavailable", error_reply)

            session_id = self.plugin._sanitize_session_id("group", "user")
            session_dir = self.plugin.workspace / session_id
            self.assertTrue(session_dir.exists())
            await stream.aclose()

            self.assertEqual(self.plugin.active_sessions, {})
            self.assertFalse(session_dir.exists())

        asyncio.run(exercise())

    def test_response_stream_close_logs_cleanup_failure(self):
        async def exercise():
            errors = []
            self.plugin.logger.error = lambda message: errors.append(message)
            stream = self.plugin.agent_command(
                FakeEvent("/agent build a calculator")
            )
            self.assertIn("正在分析需求", await anext(stream))
            session_id = self.plugin._sanitize_session_id("group", "user")
            session_state = self.plugin.active_sessions[session_id]

            with patch.object(self.plugin, "_cleanup_session", return_value=False):
                await stream.aclose()

            self.assertFalse(session_state["active"])
            self.assertNotIn(session_id, self.plugin.active_sessions)
            self.assertTrue(any(session_id in message for message in errors))

        asyncio.run(exercise())

    def test_stale_stream_does_not_remove_replacement_session(self):
        async def exercise():
            stream = self.plugin.agent_command(
                FakeEvent("/agent build a calculator")
            )
            self.assertIn("正在分析需求", await anext(stream))
            session_id = self.plugin._sanitize_session_id("group", "user")
            session_dir = self.plugin.workspace / session_id
            session_dir.mkdir()
            sentinel = session_dir / "keep.txt"
            sentinel.write_text("replacement session", encoding="utf-8")
            original_state = self.plugin.active_sessions[session_id]
            replacement_state = {"active": True, "requirement": "new request"}
            self.plugin.active_sessions[session_id] = replacement_state

            await stream.aclose()

            self.assertFalse(original_state["active"])
            self.assertIs(self.plugin.active_sessions[session_id], replacement_state)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "replacement session")

        asyncio.run(exercise())

    def test_exit_command_removes_active_session_and_workspace(self):
        session_id = self.plugin._sanitize_session_id("group", "user")
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

    def test_exit_command_reports_cleanup_failure_truthfully(self):
        session_id = self.plugin._sanitize_session_id("group", "user")
        state = {"active": True}
        self.plugin.active_sessions[session_id] = state
        errors = []
        self.plugin.logger.error = lambda message: errors.append(message)

        with patch.object(self.plugin, "_cleanup_session", return_value=False):
            replies = self.collect(
                self.plugin.agent_command(FakeEvent("/exitconver"))
            )

        self.assertFalse(state["active"])
        self.assertNotIn(session_id, self.plugin.active_sessions)
        self.assertIn("清理未完成", replies[0])
        self.assertTrue(any(session_id in message for message in errors))

    def test_terminate_cleans_all_sessions(self):
        session_ids = (
            self.plugin._sanitize_session_id("first", "user"),
            self.plugin._sanitize_session_id("second", "user"),
        )
        for session_id in session_ids:
            (self.plugin.workspace / session_id).mkdir()
            self.plugin.active_sessions[session_id] = {"active": True}

        asyncio.run(self.plugin.terminate())

        self.assertEqual(self.plugin.active_sessions, {})
        for session_id in session_ids:
            self.assertFalse((self.plugin.workspace / session_id).exists())

    def test_terminate_continues_after_cleanup_error(self):
        session_ids = (
            self.plugin._sanitize_session_id("first", "user"),
            self.plugin._sanitize_session_id("second", "user"),
        )
        session_records = {}
        for session_id in session_ids:
            (self.plugin.workspace / session_id).mkdir()
            record = {"active": True}
            session_records[session_id] = record
            self.plugin.active_sessions[session_id] = record

        attempted = []
        cleanup = self.plugin._cleanup_session

        def fail_first_cleanup(session_id):
            attempted.append(session_id)
            if session_id == session_ids[0]:
                raise OSError("injected cleanup failure")
            cleanup(session_id)

        with patch.object(self.plugin, "_cleanup_session", side_effect=fail_first_cleanup):
            asyncio.run(self.plugin.terminate())

        self.assertEqual(attempted, list(session_ids))
        self.assertTrue(all(not state["active"] for state in session_records.values()))
        self.assertEqual(self.plugin.active_sessions, {})
        self.assertTrue((self.plugin.workspace / session_ids[0]).exists())
        self.assertFalse((self.plugin.workspace / session_ids[1]).exists())

    def test_terminate_logs_false_cleanup_result_and_continues(self):
        session_ids = (
            self.plugin._sanitize_session_id("first", "user"),
            self.plugin._sanitize_session_id("second", "user"),
        )
        for session_id in session_ids:
            (self.plugin.workspace / session_id).mkdir()
            self.plugin.active_sessions[session_id] = {"active": True}
        session_states = list(self.plugin.active_sessions.values())

        errors = []
        self.plugin.logger.error = lambda message: errors.append(message)
        attempted = []

        def fail_first_cleanup(session_id):
            attempted.append(session_id)
            if session_id == session_ids[0]:
                return False
            return True

        with patch.object(
            self.plugin, "_cleanup_session", side_effect=fail_first_cleanup
        ):
            asyncio.run(self.plugin.terminate())

        self.assertEqual(attempted, list(session_ids))
        self.assertTrue(all(not state["active"] for state in session_states))
        self.assertEqual(self.plugin.active_sessions, {})
        self.assertTrue(any(session_ids[0] in message for message in errors))


if __name__ == "__main__":
    unittest.main()
