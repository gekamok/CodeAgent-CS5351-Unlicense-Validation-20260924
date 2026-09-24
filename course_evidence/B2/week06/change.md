# Week 06: B2 cleanup outcome contract

## Engineering change

`CodeAgentPlugin._cleanup_session` now returns a boolean outcome. It reports `False` for malformed IDs, symlink targets, paths outside the resolved workspace, non-directory targets, and filesystem errors. It removes a valid child directory without suppressing `shutil.rmtree` errors, reports whether removal completed, and treats an already-absent session directory as an idempotent success.

The change is limited to the B2-owned cleanup helper. Its current call sites still invoke cleanup for its side effect and do not consume the returned outcome; response handling for a failed cleanup remains an integration limitation.

## Regression coverage

`tests/roles/b2/test_session_lifecycle.py` adds coverage for successful removal, repeated cleanup of an absent directory, and a simulated `PermissionError` that must be returned as failure while leaving the directory in place.

## Validation performed

Command:

```text
C:\ProgramData\miniconda3\python.exe -m unittest discover -s tests\roles\b2 -v
```

Result: **PASS** — 6 tests ran; all passed. The initial default-sandbox attempt failed during fixture setup because temporary directory creation under the worktree was denied; the identical command passed when retried through the authorized workspace-write execution path.

`git diff --check` also passed. The focused suite parses `main.py` and executes extracted B2 method bodies; it does not import AstrBot or validate full plugin startup and event dispatch.
