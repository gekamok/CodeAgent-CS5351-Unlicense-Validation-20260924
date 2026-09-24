# Week 07: B2 boundary and failure-path verification

## Coverage added

The B2 lifecycle suite now checks that:

- cleanup rejects malformed session IDs and preserves a non-directory stale target;
- cleanup refuses a resolved target outside the workspace and leaves both the candidate and outside sentinel intact;
- process metadata creation rejects a symbolic-link target and a resolved path outside the workspace;
- Week06 cleanup outcome behavior remains covered for successful, repeated, and failed removal.

Path resolution and symlink detection branches are exercised with mocks so these checks run on Windows without requiring symlink-creation privileges. The suite still includes lexical traversal rejection against the real temporary workspace.

## Validation performed

Command:

```text
C:\ProgramData\miniconda3\python.exe -m unittest discover -s tests\roles\b2 -v
```

Result: **PASS** — 9 tests ran; all passed. The command ran through the authorized workspace-write execution path because the default sandbox blocks this suite's temporary fixture writes.

## Coverage limits

No actual filesystem symlink or junction was created, and concurrent path replacement races were not exercised. The suite executes extracted B2 helper bodies without importing AstrBot; full plugin startup, event dispatch, and how current callers act on a `False` cleanup outcome remain unverified.
