# Week 6 C1 Change

## Change

`_rollback_to_snapshot` now examines matching snapshots from newest to oldest and skips unreadable JSON or payloads that do not match the saved snapshot contract. It returns the first usable snapshot with a matching step, numeric timestamp, string code, and list of file records; it returns `None` when the directory has no usable candidate. The C1 regression suite now covers fallback from both malformed JSON and a structurally invalid newest snapshot.

## Validation

- Command: `C:\ProgramData\miniconda3\python.exe tests\roles\c1\test_debug_snapshot_baseline.py`
- Result: 5 tests ran; OK; exit code 0. The command used the authorized execution path because the normal sandbox denied Python's temporary fixture directory operations.
- Command: `C:\ProgramData\miniconda3\python.exe -m py_compile main.py tests\roles\c1\test_debug_snapshot_baseline.py`
- Result: exit code 0.
- Command: `git diff --check`
- Result: exit code 0; Git printed informational LF-to-CRLF working-copy notices for the two changed Python files.

## Limitations

The regression suite loads the real C1 methods with a minimal AstrBot API stub and a temporary workspace. It does not start AstrBot or run a live sandbox session. In the current workflow, the debug loop does not call `_rollback_to_snapshot`; this change improves the rollback helper's failure recovery but does not claim end-to-end debug-loop rollback integration.
