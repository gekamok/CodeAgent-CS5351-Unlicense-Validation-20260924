import tempfile
import subprocess
import sys
import os
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

SCRIPT_DIR = Path(__file__).resolve().parents[3] / 'skills' / 'CodeAgent' / 'scripts'
sys.path.insert(0, str(SCRIPT_DIR))

from codeagent_sandbox import ResourceLimiter, SandboxConfig, SandboxExecutor, StandardExecutor, TimeoutManager


class SandboxBaselineTests(unittest.TestCase):
    def test_environment_builds_tmp_path_from_string_workspace_root(self):
        with tempfile.TemporaryDirectory() as workspace:
            config = SandboxConfig(workspace_root=workspace)

            env = StandardExecutor(config)._build_env()

            expected_tmp = str(Path(workspace) / 'tmp')
            self.assertEqual(env['TMPDIR'], expected_tmp)
            self.assertEqual(env['TEMP'], expected_tmp)
            self.assertEqual(env['TMP'], expected_tmp)

    def test_resource_limiter_is_a_noop_when_posix_resource_is_unavailable(self):
        with patch('codeagent_sandbox.resource', None):
            ResourceLimiter(SandboxConfig()).apply_limits()

    def test_timeout_manager_uses_a_timer_without_sigalrm(self):
        with patch('codeagent_sandbox.signal', SimpleNamespace()):
            with self.assertRaisesRegex(TimeoutError, '1秒'):
                with TimeoutManager(1):
                    while True:
                        pass

    def test_standard_python_execution_runs_in_a_temporary_workspace(self):
        with tempfile.TemporaryDirectory() as workspace:
            config = SandboxConfig(workspace_root=workspace, use_restricted_python=False)

            result = SandboxExecutor(config).execute(
                'print("sandbox smoke")',
                session_id='baseline',
                language='python',
            )

            self.assertTrue(result['success'], result)
            self.assertIn('sandbox smoke', result['stdout'])

    def test_standard_python_execution_times_out_and_returns_failure(self):
        with tempfile.TemporaryDirectory() as workspace:
            config = SandboxConfig(
                workspace_root=workspace,
                wall_time_limit=1,
                use_restricted_python=False,
            )

            result = SandboxExecutor(config).execute(
                'while True: pass',
                session_id='timeout',
                language='python',
            )

            self.assertFalse(result['success'])
            self.assertIn('超时', result['stderr'])

    def test_standard_executor_kills_a_timed_out_child(self):
        process = SimpleNamespace(
            pid=123,
            communicate=Mock(side_effect=subprocess.TimeoutExpired('python', 1)),
            kill=Mock(),
            wait=Mock(return_value=0),
        )
        with (
            patch('codeagent_sandbox.os.killpg', return_value=None, create=True) as kill_group,
            patch('codeagent_sandbox.os.getpgid', return_value=123, create=True),
            patch('codeagent_sandbox.subprocess.Popen', return_value=process),
        ):
            stdout, stderr, exit_code, _elapsed = StandardExecutor(
                SandboxConfig(wall_time_limit=1)
            ).execute_code('pass', Path.cwd(), 'python', 'main.py')

        self.assertEqual(stdout, '')
        self.assertIn('超时', stderr)
        self.assertEqual(exit_code, -1)
        if os.name == 'nt':
            process.kill.assert_called_once_with()
        else:
            kill_group.assert_called_once()

    def test_standard_executor_reports_failed_child_cleanup(self):
        process = SimpleNamespace(
            pid=123,
            communicate=Mock(side_effect=subprocess.TimeoutExpired('python', 1)),
            kill=Mock(side_effect=PermissionError('simulated kill failure')),
            wait=Mock(side_effect=[
                subprocess.TimeoutExpired('python', 2),
                subprocess.TimeoutExpired('python', 2),
            ]),
        )
        with (
            patch('codeagent_sandbox.os.killpg', return_value=None, create=True),
            patch('codeagent_sandbox.os.getpgid', return_value=123, create=True),
            patch('codeagent_sandbox.subprocess.Popen', return_value=process),
        ):
            stdout, stderr, exit_code, _elapsed = StandardExecutor(
                SandboxConfig(wall_time_limit=1)
            ).execute_code('pass', Path.cwd(), 'python', 'main.py')

        self.assertEqual(stdout, '')
        self.assertIn('进程清理失败', stderr)
        self.assertIn('simulated kill failure', stderr)
        self.assertEqual(exit_code, -1)
        self.assertEqual(process.wait.call_count, 2)


if __name__ == '__main__':
    unittest.main()
