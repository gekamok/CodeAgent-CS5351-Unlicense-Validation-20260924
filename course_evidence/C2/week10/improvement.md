# C2 Week 10 Improvement

## Owned engineering change

Hardened the owned `main.py::_call_packager` boundary. It now invokes the packager with the active Python interpreter, rejects malformed or non-object JSON, requires a boolean `success` value, refuses a success result paired with a nonzero process exit, validates archive metadata, and verifies the reported archive exists before returning success.

Added `tests/roles/c2/test_packager_boundary.py` with a real subprocess publication check, invalid-input CLI failure coverage, malformed-output cases, and inconsistent success-payload cases. The real subprocess test opens the published ZIP, checks its integrity, and confirms the source and test members are present. The existing packager suite continues to cover injected source-write, archive-write, and integrity-check failures and verifies that failed builds do not leave published archives.

## Validation evidence

Command run from the C2 worktree through `cmd.exe` with the required interpreter:

```text
C:\ProgramData\miniconda3\python.exe -B -m unittest discover -s tests\roles\c2 -v
```

Result: **PASS**, 15 tests ran and reported `OK`. This includes the real `_call_packager` subprocess success and invalid-input failure paths. The successful boundary case published a readable ZIP containing the expected source and test files; the invalid-input case returned a failure and left no ZIP in its isolated output directory.

An initial run under the restricted default process token failed with WinError 5 while creating or entering temporary fixture paths. The same C2 identity reran the suite using the authorized `cmd.exe` elevated invocation and worktree-local temporary directories; that run passed. The initial environment failure is retained here as part of the validation record.

## Limitations

The suite does not run npm installation or a live AstrBot host integration. It validates the packager subprocess contract and archive publication locally; it does not establish behavior under real disk exhaustion or external filesystem/device failure.
