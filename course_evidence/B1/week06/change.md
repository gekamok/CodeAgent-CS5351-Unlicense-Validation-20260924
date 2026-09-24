# Week 6 — B1 Requirement Boundary Improvement

## Change

`_extract_requirement` now recognizes `/agent` only as a whitespace-delimited command or as a direct `@mention/agent` form. This avoids extracting a request from path-like text such as `prefix/agent ...` or an email-like `mail@builder/agent ...`, while preserving prose-prefixed commands, mentions, and multiline requirement bodies. `_assess_project` trims outer whitespace before keyword classification and size measurement, so padding does not push a 29-character request into the next size band.

The role regression suite adds checks for the two command-like false matches and whitespace-padded type/size assessment. The tests load `main.py` with minimal AstrBot import stubs and call the real B1 helpers.

## Validation performed

- `C:\ProgramData\miniconda3\python.exe -m unittest discover -s tests/roles/b1 -v` — PASS; 9 tests ran.
- `C:\ProgramData\miniconda3\python.exe -m py_compile main.py tests/roles/b1/test_role_baseline.py` — PASS; exit code 0.
- `git diff --check` — PASS; exit code 0. Git reported its configured LF-to-CRLF working-copy warnings for `main.py` and the B1 test file; no whitespace errors were reported.

## Limits

These checks cover the helper methods directly, not AstrBot event dispatch or runtime initialization. No installed AstrBot runtime integration was exercised.
