# Week 7 — B1 Boundary and Contract Verification

## Expanded verification

The B1 role suite now covers command extraction with LF/CRLF multiline bodies, whitespace before commands, direct hyphenated mentions, malformed command tokens, and command-like path/email fragments. Project assessment checks outer-whitespace normalization, keywords after line breaks, and size thresholds at 29, 30, 99, and 100 Unicode characters. Existing tests continue to cover empty requirements, blacklist normalization, and ordered project-type rules.

## Validation performed

- `C:\ProgramData\miniconda3\python.exe -m unittest discover -s tests/roles/b1 -v` — PASS; 13 tests ran.
- `C:\ProgramData\miniconda3\python.exe -m py_compile main.py tests/roles/b1/test_role_baseline.py` — PASS; exit code 0.
- `git diff --check` — PASS; exit code 0. Git reported its configured LF-to-CRLF working-copy warning for the B1 test file; no whitespace errors were reported.

## Coverage gap

Tests load the actual helpers with minimal AstrBot import stubs. They do not exercise event dispatch, upstream message parsing, plugin initialization, or an installed AstrBot runtime. Non-string input is outside the helpers' annotated `str` contract and was not tested.
