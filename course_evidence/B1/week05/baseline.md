# Week 5 — B1 Executable Baseline

## Change

The B1 baseline exposed two requirement-extraction edge cases. The original `.` capture stopped at a newline, truncating a multi-line request. Expanding the capture alone also allowed a whitespace-only `/agent` request to produce an empty string. `_extract_requirement` now captures across line breaks while requiring a non-whitespace first character after the command separator; trimming still removes trailing whitespace.

`tests/roles/b1/test_role_baseline.py` exercises the actual three B1 helper methods with minimal AstrBot import stubs. Coverage includes plain and mentioned triggers, multi-line and empty requirements, admin/group blacklist normalization, project keyword precedence, and size boundaries at 29, 30, 99, and 100 characters.

## Validation performed

- `C:\ProgramData\miniconda3\python.exe -m unittest discover -s tests/roles/b1 -v` — PASS; 7 tests ran, all passed.
- `C:\ProgramData\miniconda3\python.exe -m py_compile main.py tests/roles/b1/test_role_baseline.py` — PASS; exit code 0, no output.
- `git diff --check` — PASS; exit code 0. Git emitted its configured LF-to-CRLF working-copy warning for `main.py`; no whitespace errors were reported.

## Limits

The role tests instantiate the class without running its plugin initializer and stub only its AstrBot imports. They verify the owned helper implementations, but do not exercise AstrBot event dispatch, initialization side effects, or an installed AstrBot runtime. No claims are made about those integration paths.
