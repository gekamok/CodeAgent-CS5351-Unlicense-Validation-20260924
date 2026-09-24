# Week 9 C1 Sprint2 Summary

## Week 6–9 work

- Week 6 changed `_rollback_to_snapshot` to scan newest-to-oldest candidates, skip unreadable or structurally invalid snapshots, and return the first valid earlier snapshot. The Week6 implementation and regression are in `main.py` and `tests/roles/c1/test_debug_snapshot_baseline.py`.
- Week 7 expanded contract and failure-path checks for malformed JSON, invalid payload shapes, unreadable files, unrelated steps, a non-directory snapshot path, and the no-valid-candidate result.
- Week 8 fetched `origin/main` at `7f407b7`. It matched the C1 branch base, with no fetched main commits missing from the role branch. Review found no cross-role overlap or return-contract change.

## Full C1 validation

- Command: `C:\ProgramData\miniconda3\python.exe tests\roles\c1\test_debug_snapshot_baseline.py`
- Result: 9 tests ran; OK; exit code 0. The command used the authorized execution path because the normal sandbox denied Python's temporary fixture directory operations.
- Command: `C:\ProgramData\miniconda3\python.exe -m py_compile main.py tests\roles\c1\test_debug_snapshot_baseline.py`
- Result: exit code 0.
- Command: `git diff --check`
- Result: exit code 0.
- Command: `git grep -n -I -i -E "https?://|[0-9a-f]{40}"`
- Result: no tracked text matched a URL or a full-length commit hash (Git exit code 1). The C1 evidence was also reviewed for forbidden source paths and tracking fields; no such source metadata was found.
- GitHub check before closeout: searching PRs for head branch `course/c1` returned no existing PR. The C1 Sprint2 PR will be opened after this closeout commit is pushed.

## Limitations and Sprint3 goal

Tests exercise C1 methods from the real `main.py` with an AstrBot API stub and temporary files; no live AstrBot or sandbox subprocess run was performed. The current debug loop does not call `_rollback_to_snapshot`, so the helper's recovery behavior is tested directly rather than through a live debug-loop rollback. For Sprint3, review whether the product flow should create explicit recovery points before retrying and add an end-to-end test only if the ownership and recovery contract can be made clear.
