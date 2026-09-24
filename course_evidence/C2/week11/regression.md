# C2 Week 11 Regression

## Regression and boundary work

Extended the `_call_packager` boundary regressions for a missing script, a subprocess timeout, a nonzero child exit without an error message, and a failure payload whose `error` field is not text. The wrapper now supplies a useful fallback diagnostic for those invalid failure payloads. Existing tests continue to exercise actual CLI validation failure, successful archive publication, malformed output, and packager cleanup after injected source-write, archive-write, and integrity-check errors.

## Validation

Command run from the C2 worktree through `cmd.exe` with the required interpreter:

```text
C:\ProgramData\miniconda3\python.exe -B -m unittest discover -s tests\roles\c2 -v
```

Result: **PASS**, 16 tests ran and reported `OK`. The real subprocess publication test validated the ZIP and its members; the invalid-input test confirmed a failed CLI call leaves no ZIP in its isolated output directory. `git diff --check` also passed.

## Forbidden source metadata scan

Scanned tracked files for `BOOTSTRAP_SOURCE_DIR`, `_SOURCE_URL`, `_SOURCE_SHA`, `_SOURCE_REPO`, `_SOURCE_COMMIT`, the recorded bootstrap archive SHA prefix `2131e963`, and HTTP URL text. Scanned commit messages for `BOOTSTRAP_SOURCE_DIR`, `_SOURCE_URL`, and `_COMMIT` fields. No bootstrap path, source URL, source SHA, source repository, or source commit tracking value was found. The broad `_REPO` search matched only the unrelated `tests/roles/c1/test_debug_snapshot_baseline.py` `_REPO_ROOT` local test path constant. HTTP matches were existing runtime endpoints, checker patterns, and the Unlicense reference; none records a source intake location.

## Limitations

The timeout and missing-script paths are injected boundary cases; npm installation and a live AstrBot host integration remain unrun. Disk exhaustion and external filesystem/device failures remain outside these tests.
