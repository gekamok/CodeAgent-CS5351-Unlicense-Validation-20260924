# Week 11 — Classification Boundary Regression

## Regression and cleanup

Refactored the B1-owned `_assess_project` language matching to extract ASCII identifier tokens once, then compare against explicit aliases. This keeps punctuation and Chinese-text boundaries clear and avoids repeating a regex search for each classification rule. Extended the regression matrix for `Node.js`, hyphenated JavaScript, `TS-node`, and lookalike tokens such as `TStools` and `bashful`; existing tests continue to protect multiline triggers and Unicode size boundaries.

## Validation performed

- `C:\ProgramData\miniconda3\python.exe -m unittest discover -s tests/roles/b1 -v` — PASS; 14 tests ran.
- `C:\ProgramData\miniconda3\python.exe -m py_compile main.py tests/roles/b1/test_role_baseline.py` — PASS; exit code 0.
- `git diff --check` — PASS; exit code 0. Git emitted only configured LF-to-CRLF working-copy warnings for the two Python files.

## Forbidden source-metadata scan

The tracked-file scan found no source-provenance field candidates in the B1 changes. Broader identifier searches found only local test-file loader names in the C1 and B1 helper suites; those refer to local fixture files, not external source or revision metadata. No external source address, revision identifier, or provenance field was added in the B1 Week 11 diff.

The test suite still uses minimal AstrBot import stubs; it does not exercise installed-runtime dispatch or upstream message parsing.
