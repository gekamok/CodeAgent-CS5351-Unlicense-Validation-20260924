# Week 10 — Requirement Classification Improvement

## Change

In the B1-owned `_assess_project` helper, JavaScript, TypeScript, API, shell, and Bash names now match complete ASCII identifier tokens instead of arbitrary substrings. This prevents ordinary phrases such as “unit tests” and “capital costs” from being mistaken for TypeScript or API requests. Explicit plural `APIs` remains supported, and the token boundary allows a language name to touch Chinese text. Existing classification order, helper interface, trimming, and Unicode character-count sizing remain unchanged.

Added role regressions for `JS`, `JavaScript` adjacent to Chinese text, `TypeScript`, plural `APIs`, `Bash`, and false-positive phrases containing `tests` or `capital`.

## Validation performed

- `C:\ProgramData\miniconda3\python.exe -m unittest discover -s tests/roles/b1 -v` — PASS; 14 tests ran.
- `C:\ProgramData\miniconda3\python.exe -m py_compile main.py tests/roles/b1/test_role_baseline.py` — PASS; exit code 0.
- `git diff --check` — PASS; exit code 0. Git emitted only its configured LF-to-CRLF working-copy warnings for `main.py` and the B1 test file.

The suite loads the actual B1 helpers with minimal AstrBot import stubs. It does not exercise platform message parsing or installed-runtime event dispatch.
