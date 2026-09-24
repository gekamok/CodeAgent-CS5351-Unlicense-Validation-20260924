# D1 Week 10: sandbox and checker result contracts

## Owned improvement

Updated the D1-owned `_call_sandbox` and `_call_js_checker` boundaries in `main.py`, with regression coverage in `tests/roles/d1/test_wrappers.py`.

- Sandbox JSON must now be an object with boolean `success`, string `stdout` and `stderr`, an integer `exit_code`, and an optional string `error`. A reported pass must also have exit code zero and no error.
- Checker JSON must include a boolean `passed`, an issue list with recognized severity levels, and a summary string. The wrapper now enforces the checker CLI's exit contract: code 1 for incomplete/failed checks or critical/high findings, and code 0 for a clean pass. Contradictory results fail closed while preserving available issues and summary.
- Added regression cases for a non-object sandbox result, a contradictory sandbox pass, checker blocking findings reported as a pass, and unexpected checker process status.

## Validation performed

| Command/check | Result |
| --- | --- |
| `C:\ProgramData\miniconda3\python.exe -B .testtmp\run_role_tests.py` from `.worktrees\d1` using a pre-created `.testtmp\workspace` and a fixed `TemporaryDirectory` test fixture | PASS, all 15 D1 Python tests |
| `node --check skills\CodeAgent\scripts\codeagent_js_checker.js` | PASS |
| `node --check tests\roles\d1\codeagent_js_checker.test.mjs` | PASS |
| `node --test --test-isolation=none tests\roles\d1\codeagent_js_checker.test.mjs` | PASS, 13 tests |
| `git diff --check` | PASS |

The first ordinary Python suite invocation failed in three sandbox tests with `PermissionError` / `WinError 5` when the test-created temporary workspace attempted writes or cleanup. Pointing Python's temporary root into the D1 worktree still failed for newly generated temporary subdirectories. The passing rerun used a pre-created fixed workspace inside the authorized D1 worktree; the transient test runner and workspace are not part of this change. A PowerShell child-shell launch also failed with `CreateProcessAsUserW` access denied, so the successful commands used `cmd.exe`. Earlier Week 6 and Week 8 restricted-path WinError 5 attempts remain documented in [Week 9 summary](../week09/sprint2_summary.md).

## Limitations

ESLint and TypeScript remain unavailable in this environment, as recorded in the Week 9 summary. Their unavailability is surfaced as an incomplete checker result. This change validates subprocess result consistency; it does not install or exercise those optional analyzers.
