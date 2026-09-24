# Week 6: Validate security scan report contracts

## Change

`_call_security_scan()` now fails closed when decoded scanner output lacks a valid `passed` boolean, findings list, finding severity/message, or summary. This keeps malformed scanner output from being treated as a usable scan report. D2 regression tests cover invalid JSON, non-object output, missing or mistyped schema fields, and acceptance of a well-formed report.

## Validation

- `C:\ProgramData\miniconda3\python.exe .worktrees\d2\tests\roles\d2\test_security_report.py` — PASS, 7 tests.
- `C:\ProgramData\miniconda3\python.exe -m py_compile .worktrees\d2\main.py .worktrees\d2\tests\roles\d2\test_security_report.py` — PASS, exit code 0.

The tests stub subprocess output for malformed cases; the existing test also invokes the real scanner for one high-risk case. This week does not measure the completeness of scanner rules.
