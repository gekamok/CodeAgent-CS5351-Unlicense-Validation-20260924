import tempfile
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

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


if __name__ == '__main__':
    unittest.main()
