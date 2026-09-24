# A1 Week 11 regression

## Regression work

Expanded `tests/roles/a1/test_config_contract.py` with boundary cases for a `node_modules` path that exists as a file and a JSON manifest whose `devDependencies` value is not an object. The checks verify that these invalid states stop before Node/npm is started and leave an explicit warning. Existing regression cases also cover an incomplete install, malformed JSON, empty manifests, missing Node/npm, command timeouts, install failures, and typed configuration fallback.

## Validation run

- `C:\ProgramData\miniconda3\python.exe -m unittest discover -s tests/roles/a1 -p test_*.py -v` — PASS, 20 tests.
- `C:\ProgramData\miniconda3\python.exe -m py_compile main.py tests\roles\a1\test_config_contract.py` — PASS.
- `git diff --check` — PASS; no whitespace errors.

## Forbidden-metadata scan

Scanned the tracked repository with `git grep -n _SOURCE_URL`, `git grep -n _COMMIT`, `git grep -n _REPO`, and `git grep -n https://`; searched tracked course evidence for 40-character hexadecimal strings. `_SOURCE_URL` and `_COMMIT` had no matches. The `_REPO` scan found only `_REPO_ROOT` in C1's test loader. URL matches were the Unlicense license reference and existing Node.js installer and GitHub API runtime URLs; none are source-provenance fields. No 40-character hexadecimal strings appeared in the course evidence. The A1 Week 10–11 changes add no external source path, source URL, source SHA, or source-tracking field.

## Limits

Node/npm subprocesses remain mocked in the role suite. The regression run does not perform a live npm repair, start the plugin host, or verify transitive packages in a live installation. No new shell-launch failure occurred; the prior PowerShell `CreateProcessAsUserW` denial and cmd.exe workaround are recorded in Week 10 evidence.
