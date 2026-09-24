# D1 Week 12: presentation notes

## Role and contribution

D1 owns the sandbox and JavaScript checker boundary: `skills/CodeAgent/scripts/codeagent_sandbox.py`, `skills/CodeAgent/scripts/codeagent_js_checker.js`, `skills/CodeAgent/scripts/package.json`, and the `_call_sandbox` / `_call_js_checker` regions of `main.py`.

In Sprint 3, D1 hardened the wrapper contracts and timeout cleanup:

- Commit `03e27b1` (`test(d1): week 10 add sprint 3 improvement`) validates sandbox and checker JSON shapes and aligns checker exit status with pass/fail and blocking findings. Invalid or contradictory subprocess results now fail closed.
- Commit `b9c4809` (`test(d1): week 11 run role regression`) makes sandbox child cleanup platform-aware, retries termination and reaping, and returns an explicit cleanup failure if a timed-out child remains alive.
- Added Python regression cases in `tests/roles/d1/test_wrappers.py` and `tests/roles/d1/test_sandbox.py`; the existing Node checker suite remains the checker behavior suite.

## Integration PR record

- Sprint 1: PR #8 (D1), **MERGED**, merge commit `d025da3`.
- Sprint 2: PR #16 (D1), **MERGED**, merge commit `8578829`.
- Sprint 3 final PR: not created at the Week 12 checkpoint; the assignment creates one after Week 13 role evidence is complete.

The PR states and merge commits are recorded in the team Week 5 and Week 9 closeouts. The Week 10 and Week 11 D1 commits are present on local `course/d1`; they had not yet been pushed at this checkpoint.

## Validation evidence

| Commit | Actual validation |
| --- | --- |
| `03e27b1` | D1 Python role suite: PASS, 15 tests via a transient fixed-workspace runner and `C:\ProgramData\miniconda3\python.exe -B`; Node checker and test syntax checks: PASS; Node role tests: PASS, 13 tests; `git diff --check`: PASS. |
| `b9c4809` | D1 Python role suite: PASS, 17 tests via a transient fixed-workspace runner and `C:\ProgramData\miniconda3\python.exe -B`; Node checker and test syntax checks: PASS; Node role tests: PASS, 13 tests; `git diff --check`: PASS; D1 source-tracking metadata scan: no matches. |

The ordinary `TemporaryDirectory` test path remains blocked by Windows `WinError 5`; the successful role-suite runs mapped the tests to a pre-created workspace inside the authorized D1 worktree. The Week 10 and Week 11 evidence records the exact commands and the failed attempts as well as the successful runs.

## Problems solved and limitations

The wrappers no longer trust parseable but malformed or contradictory subprocess output. Sandbox timeouts now preserve the distinction between a timeout and a child cleanup failure. The regression tests cover invalid output, inconsistent status, unavailable Node, checker timeout, child termination, and failed cleanup.

ESLint and TypeScript executables are unavailable, so analyzer integration reports incomplete status and is tested through injected outcomes. RestrictedPython and POSIX resource limits were not exercised. This Windows run exercised direct child termination; POSIX process-group signaling was not exercised. No live AstrBot host or end-to-end plugin session was validated.
