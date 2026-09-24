# Week 12 — B1 Presentation Notes

## Owned module and contribution

B1 owns `main.py` requirement extraction, blacklist checks, and project assessment, with executable regressions in `tests/roles/b1/test_role_baseline.py`. The Sprint 3 work so far is confined to `_assess_project` and that B1 test file.

The Week 10 change replaced substring-based language checks with whole ASCII identifier-token matching. It keeps `JS`, `JavaScript`, `TS`, `TypeScript`, `API`/`APIs`, `shell`, and `Bash` aliases, including aliases adjacent to Chinese text, while rejecting false matches such as `unit tests` as TypeScript and `capital costs` as API. Week 11 extracts the requirement tokens once and adds punctuation and embedded-lookalike regressions.

## Integration and Git evidence

- Sprint 1 B1 PR **#3** is recorded as **MERGED** in the Week 5 closeout; merge commit `a68e29410a5bf1f754df7dc0d37372c0a29bf2af`.
- Sprint 2 B1 PR **#9** appears as merge commit `2c07f33c44fe7e1710e0f9c7021e635ba5e39431` in the current branch history; Sprint 2 closeout records all eight role PRs merged.
- Week 10 commit: `61fd394` — `test(b1): week 10 add sprint 3 improvement`.
- Week 11 commit: `ba54f1c` — `test(b1): week 11 run role regression`.
- At note preparation, `HEAD` was `ba54f1ce8b638d6c79ef58e9390dc072ae5e51e3`; the working tree was clean and the branch was two commits ahead of `origin/course/b1`. Those Week 10 and 11 commits had not yet been pushed.

## Validation evidence

- `C:\ProgramData\miniconda3\python.exe -m unittest discover -s tests/roles/b1 -v` — PASS; 14 tests ran after both Week 10 and Week 11 changes.
- `C:\ProgramData\miniconda3\python.exe -m py_compile main.py tests/roles/b1/test_role_baseline.py` — PASS; exit code 0 after both changes.
- `git diff --check` — PASS after both changes; only Git's configured LF-to-CRLF working-copy warnings appeared.

These tests exercise the actual B1 helpers with minimal AstrBot import stubs. They do not validate installed AstrBot initialization, upstream message serialization, or event dispatch. The token rules intentionally recognize exact ASCII identifiers and retain the existing project-type precedence; they do not attempt natural-language inference beyond the supported aliases and Chinese keywords.
