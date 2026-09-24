# Sprint 2 verification status — Week 7 gate

## Gate basis

Sprint 1 closed at `279292e`; Sprint 2 began from main `7f407b7` after the Week 6 plan and branch synchronization. This status was first recorded when B1 reported its completed Week 7 verification. It is a point-in-time gate record; a role without a report below is not counted as passed.

## Role evidence received

| Role | Week 7 evidence | Actual validation reported | Coverage limits |
| --- | --- | --- | --- |
| A1 | Commit `f42fc39`; `course_evidence/A1/week07/verification.md`; source/test changes include malformed/missing config and dependency-preparation boundary checks. | `C:\ProgramData\miniconda3\python.exe tests\roles\a1\test_config_contract.py` — PASS, 15 tests; `py_compile main.py tests/roles/a1/test_config_contract.py` — PASS; `node --check skills/CodeAgent/scripts/codeagent_js_checker.js` — PASS; `git diff --check` — PASS. | Node/npm subprocess behavior is mocked; no real npm installation, AstrBot host startup, platform auto-install, or partial `node_modules` validation. |
| A2 | Commit `fc4da16` (`test(a2): week 07 expand verification`); `course_evidence/A2/week07/verification.md`; expanded dispatch, stream-closure, replacement-record, and cleanup-error paths. | `C:\ProgramData\miniconda3\python.exe -m unittest discover -s tests\roles\a2 -v` — PASS, 11 tests; `compileall -q main.py tests\roles\a2` — exit 0; `git diff --check` — exit 0. | AstrBot imports and generator dispatch are stubbed; real transport, plugin-host shutdown, and filesystem cleanup failure are not exercised. |
| B1 | Commit `b7c41a2` (`test(b1): week 07 expand verification`); `course_evidence/B1/week07/verification.md`; expanded `tests/roles/b1/test_role_baseline.py` from 7 to 13 tests. | `C:\ProgramData\miniconda3\python.exe -m unittest discover -s tests/roles/b1 -v` — PASS, 13 tests; `py_compile main.py tests/roles/b1/test_role_baseline.py` — PASS; `git diff --check` — PASS (line-ending warning only). | The helper tests use minimal AstrBot stubs; event dispatch, plugin initialization, installed-runtime integration, and non-string inputs outside the annotated `str` contract are not covered. |
| B2 | Commit `214ef68` (`test(b2): week 07 expand verification`); `course_evidence/B2/week07/verification.md`; added malformed/stale session-state, cleanup path containment, and process metadata path checks. | `C:\ProgramData\miniconda3\python.exe -m unittest discover -s tests\roles\b2 -v` — PASS, 9 tests; `git diff --check` — PASS. | Symlink/junction and concurrent-replacement cases are mocked; plugin startup/event dispatch and callers' handling of cleanup failure are not verified. |
| C1 | Commit `d201f02` (`test(c1): week 07 expand verification`); `course_evidence/C1/week07/verification.md`; added invalid/missing snapshot and recovery-path verification. | `C:\ProgramData\miniconda3\python.exe tests\roles\c1\test_debug_snapshot_baseline.py` — PASS, 9 tests; `py_compile main.py tests\roles\c1\test_debug_snapshot_baseline.py` — exit 0; `git diff --check` — exit 0. | AstrBot stubs and temp fixtures are used; no live sandbox or end-to-end debug-loop rollback. The current debug loop does not call `_rollback_to_snapshot`. |
| C2 | Commit `ce3c916` (`test(c2): week 07 expand verification`); `course_evidence/C2/week07/verification.md`; expanded direct packager boundary tests. | `C:\ProgramData\miniconda3\python.exe -B -m unittest discover -s tests\roles\c2 -v` — PASS, 11 tests; `git diff --check` — no whitespace errors (line-ending normalization warning only). | Tests do not exercise `main.py::_call_packager`, npm installation, or real storage-device failures. |
| D2 | Commit `86af032`; `course_evidence/D2/week07/verification.md`; added invalid JSON/schema, timeout, and inconsistent scanner return/report verification. | `C:\ProgramData\miniconda3\python.exe .worktrees\d2\tests\roles\d2\test_security_report.py` — PASS, 9 tests; `py_compile` of main/scanner/test — PASS; `git diff --check` — exit 0. | Timeout/status-mismatch paths are simulated; scanner-rule completeness and optional Ruff/Mypy/Bandit integrations are not validated. |

## Remaining role reports

At this update, seven roles have reported their Week 7 milestone evidence. D1 has not yet reported, so its Week 7 status remains **NOT YET VERIFIED**; no pass is inferred from silence. Any tool or environment failure remains recorded as a failure or `NOT_RUN`, not converted to a pass.

## Gate note

A1, A2, B1, B2, C1, C2, and D2 increased executable boundary/regression coverage and ran the reported checks. Overall team verification status remains **IN PROGRESS** until D1 reports and its actual commands are recorded.
