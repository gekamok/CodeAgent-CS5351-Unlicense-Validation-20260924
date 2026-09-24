# A1 Week 11 regression

## Regression work

Expanded `tests/roles/a1/test_config_contract.py` with boundary cases for a `node_modules` path that exists as a file and a JSON manifest whose `devDependencies` value is not an object. The checks verify that these invalid states stop before Node/npm is started and leave an explicit warning. Existing regression cases also cover an incomplete install, malformed JSON, empty manifests, missing Node/npm, command timeouts, install failures, and typed configuration fallback.

## Validation run

- `C:\ProgramData\miniconda3\python.exe -m unittest discover -s tests/roles/a1 -p test_*.py -v` — PASS, 20 tests.
- `C:\ProgramData\miniconda3\python.exe -m py_compile main.py tests\roles\a1\test_config_contract.py` — PASS.
- `git diff --check` — PASS; no whitespace errors.

## Forbidden-metadata scan

Scanned the tracked repository for source-tracking fields and web links, and searched course evidence for long hexadecimal identifiers. The field scan found no source-tracking values; the only repository-related match was a local root variable in C1's test loader. Web-link matches were the Unlicense license reference and existing Node.js installer and GitHub API runtime URLs; none point to project source. A Week 13 full-tree check found historical Git commit IDs in earlier course evidence, so the initial Week 11 long-hex search result was incomplete. Those identifiers document this project's Git history, not external-source SHAs. The A1 changes add no external source path, source URL, source SHA, or source-tracking value.

## Limits

Node/npm subprocesses remain mocked in the role suite. The regression run does not perform a live npm repair, start the plugin host, or verify transitive packages in a live installation. No new shell-launch failure occurred; the prior PowerShell `CreateProcessAsUserW` denial and cmd.exe workaround are recorded in Week 10 evidence.
