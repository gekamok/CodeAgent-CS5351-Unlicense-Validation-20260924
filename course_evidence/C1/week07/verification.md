# Week 7 C1 Verification

## Expanded coverage

The C1 regression suite now checks that rollback:

- skips malformed JSON and structurally invalid newest snapshots, then restores an earlier valid snapshot;
- returns `None` when all matching candidates have invalid root type, step, timestamp, or file-record shape;
- returns `None` when a candidate cannot be read because of `PermissionError`;
- ignores files for other steps and handles a snapshot path that exists as a regular file;
- keeps the existing no-snapshot and same-timestamp collision regressions passing.

## Validation

- Command: `C:\ProgramData\miniconda3\python.exe tests\roles\c1\test_debug_snapshot_baseline.py`
- Result: 9 tests ran; OK; exit code 0. The command used the authorized execution path because the normal sandbox denied Python's temporary fixture directory operations.
- Command: `C:\ProgramData\miniconda3\python.exe -m py_compile main.py tests\roles\c1\test_debug_snapshot_baseline.py`
- Result: exit code 0.
- Command: `git diff --check`
- Result: exit code 0; Git printed an informational LF-to-CRLF working-copy notice for the test file.

## Coverage gap

These tests exercise C1 methods using the real `main.py` method bodies, an AstrBot API stub, and temporary files. No live AstrBot instance, sandbox subprocess, or end-to-end debug-loop rollback is run; the existing debug loop does not call `_rollback_to_snapshot`.
