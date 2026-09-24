# Week 10: debug-loop recovery checkpoint

## Change

The Sprint 2 review found that `_rollback_to_snapshot` was tested directly but never called by the debug loop. The loop now saves a `debug_recovery` snapshot before the first sandbox run. Before retrying a failed run, it restores that checkpoint and then applies the diagnostic fix to the restored code. If the checkpoint cannot be read, the loop stops retrying and reports that recovery failed. This prevents retry edits from accumulating on top of an untrusted intermediate version.

The change is limited to C1-owned debug-loop code in `main.py` and the C1 role regression file. The regression runs the real `agent_command` async flow with the first sandbox attempt mocked to fail and the second to succeed; it verifies the actual rollback helper is called and that the retry is derived from restored checkpoint code. Security scanning and packaging are mocked at their boundaries.

## Validation

- `C:\ProgramData\miniconda3\python.exe -B .testtmp\run_role_tests.py` from this worktree using `cmd.exe` and the pre-created `.testtmp\workspace`: **PASS**, 10 tests.
- `C:\ProgramData\miniconda3\python.exe -B .testtmp\run_syntax_check.py`: **PASS**, parsed `main.py` and `tests/roles/c1/test_debug_snapshot_baseline.py`.
- `git diff --check`: **PASS**, exit 0.

The first two normal, restricted test attempts failed with `WinError 5` while creating or cleaning temporary snapshot fixtures. The successful test run used the authorized worktree path with the `cmd.exe` workaround and elevated filesystem access. Those failed attempts are retained here as environment evidence; they are not counted as passing validations.

## Limits

The async orchestration and rollback path were exercised, but sandbox execution, AstrBot, security scanning, and packaging were stubbed. This test does not prove behavior against a live bot or subprocess sandbox.
