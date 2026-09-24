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

Scanned tracked files and commit messages for source-bootstrap provenance such as input paths, external source locations, imported source digests, and source-tracking fields. No forbidden source provenance value was found. A broader repository-token search matched a local repository-root constant in a C1 test, used only to locate that test's fixture files. HTTP-text matches were existing runtime endpoints, checker patterns, and the Unlicense reference; none records a source intake location.

## Limitations

The timeout and missing-script paths are injected boundary cases; npm installation and a live AstrBot host integration remain unrun. Disk exhaustion and external filesystem/device failures remain outside these tests.
