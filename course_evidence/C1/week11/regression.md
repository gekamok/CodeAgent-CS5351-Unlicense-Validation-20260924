# Week 11: recovery failure boundary

## Regression work

Added a regression for the debug loop's checkpoint lookup failure. When a sandbox attempt fails and `_rollback_to_snapshot` cannot return a checkpoint, the loop now has an explicit tested boundary: it reports the recovery failure and stops without making a second sandbox call. The test exercises `agent_command` through its async event flow, with only the rollback result and sandbox outcome stubbed.

## Validation

- `C:\ProgramData\miniconda3\python.exe -B .testtmp\run_role_tests.py` from the C1 worktree using `cmd.exe`, the pre-created `.testtmp\workspace`, and elevated filesystem access: **PASS**, 11 tests.
- `C:\ProgramData\miniconda3\python.exe -B .testtmp\run_syntax_check.py`: **PASS**, `main.py` and the C1 regression module parsed.
- `git diff --check`: **PASS**, exit 0.
- Targeted metadata scan over `main.py`, `tests/roles/c1`, and `course_evidence/C1` for provenance field names, URL markers, and full 40-character hexadecimal strings: **no matches**.

The suite still uses an AstrBot stub and mocks the sandbox process; it verifies C1's control flow and failure boundary, not a live sandbox or bot runtime. Normal restricted test execution continues to hit the documented Windows `WinError 5` temporary-path limitation; the reported PASS is from the authorized elevated `cmd.exe` run above.
