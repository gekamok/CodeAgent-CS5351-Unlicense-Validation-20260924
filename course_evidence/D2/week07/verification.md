# Week 7: Security scan boundary verification

## Coverage added

The D2 regression suite now checks that scanner timeouts fail closed and that process exit status agrees with the returned report. It rejects a passing exit code paired with a failed report, a failing exit code paired with a passing report, and a high-risk report marked as passed. Week 6 tests also cover invalid JSON and malformed report fields.

## Validation

- `C:\ProgramData\miniconda3\python.exe .worktrees\d2\tests\roles\d2\test_security_report.py` — PASS, 9 tests.
- `C:\ProgramData\miniconda3\python.exe -m py_compile .worktrees\d2\main.py .worktrees\d2\skills\CodeAgent\scripts\codeagent_security.py .worktrees\d2\tests\roles\d2\test_security_report.py` — PASS, exit code 0.

The timeout and status-mismatch cases use controlled subprocess results. The suite still does not establish the completeness of security rules or the behavior of optional Ruff, Mypy, and Bandit integrations.
