# Week 12: presentation notes

## Role and owned module

C1 owns the debugging helpers and retry loop in `main.py`: `_analyze_error`, `_generate_debug_fix`, `_save_snapshot`, `_rollback_to_snapshot`, and the debug loop in `agent_command`. C1's regression coverage is in `tests/roles/c1/test_debug_snapshot_baseline.py`.

## Concrete changes and problem solved

The Sprint 2 review found `_rollback_to_snapshot` had direct helper tests but the debug loop never called it. Week 10 added a stable `debug_recovery` checkpoint before sandbox execution and restores that checkpoint before applying a retry fix. If recovery returns no valid checkpoint, the loop stops instead of retrying with untrusted intermediate code. Week 11 added an async-flow regression proving this failure boundary makes only one sandbox attempt.

## Git and PR evidence

- Current C1 Sprint 3 commits are `737cdfa` (`test(c1): week 10 add sprint 3 improvement`) and `0be5361` (`test(c1): week 11 run role regression`), on the Week 10 team-plan baseline `f17b0fa`.
- The team Week 5 closeout records C1's Sprint 1 PR #4 as merged.
- GitHub state in the team Week 9 closeout records C1's Sprint 2 PR #14 as merged at `d946a38`.
- No Sprint 3 PR had been opened when these notes were prepared.

## Validation evidence

- Week 10 C1 suite: **10 tests passed** with `C:\ProgramData\miniconda3\python.exe`.
- Week 11 C1 suite: **11 tests passed** with `C:\ProgramData\miniconda3\python.exe`.
- Week 10 and 11 Python syntax checks passed for `main.py` and the C1 test module; both weeks' `git diff --check` returned exit 0.
- Week 11 scan found no provenance field names, URLs, or full-length SHA patterns in C1 `main.py`, tests, or evidence.

The successful suite runs used `cmd.exe`, a pre-created `.testtmp\workspace` fixture root, and elevated filesystem access because normal restricted runs raised `WinError 5` on temporary-path operations. The failed attempts are recorded in the Week 10 and Week 11 evidence and are not counted as passes.

## Contribution, solved problems, and limits

C1 connected snapshot recovery to the real async orchestration path, added regressions for successful retry after restoration and for failure to restore, and preserved a fail-closed boundary when the checkpoint is unavailable. Work stayed in C1's assigned `main.py` region and the C1 test/evidence paths.

Tests stub AstrBot and mock sandbox outcomes, security scanning, and packaging. They validate C1 control flow and snapshot handling but do not validate a live bot, external sandbox process, security scanner, or packaging service.
