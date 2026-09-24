# A1 Week 13 final summary

## Evidence completeness

A1 has role evidence for each required week:

| Week | Evidence |
| --- | --- |
| 01 | `role_and_scope.md` |
| 02 | `source_map.md` |
| 03 | `initial_findings.md` |
| 04 | `review.md`, `git_evidence.md` |
| 05 | `baseline.md` |
| 06 | `change.md` |
| 07 | `verification.md` |
| 08 | `integration_review.md` |
| 09 | `sprint2_summary.md` |
| 10 | `improvement.md` |
| 11 | `regression.md` |
| 12 | `presentation_notes.md` |
| 13 | `final_summary.md` |

No A1 Week 14 evidence is part of this course record.

## Owned work and contribution

A1 owns plugin/config/package metadata and the configuration and JavaScript dependency-preparation regions of `main.py`. Sprint 3 improved `_ensure_js_dependencies` to read the package manifest and check for each declared package under `node_modules`, so a partial install invokes npm repair instead of being mistaken for a complete install. Empty manifests skip unnecessary work; malformed manifests and a non-directory dependency path produce clear outcomes. The A1 role suite covers these cases, typed configuration fallback, missing tools, timeouts, and npm failure responses.

Week 11 added failure-boundary regressions without editing other roles' `main.py` regions. Week 12 presentation notes use observed Git commits, test results, and PR status. The Week 11 metadata note was corrected during this final full-tree review: historical full-length hashes in earlier course evidence are internal Git commit IDs, not external-source SHAs.

## Final A1 validation

- `C:\ProgramData\miniconda3\python.exe -m unittest discover -s tests/roles/a1 -p test_*.py -v` — PASS, 20 tests.
- `C:\ProgramData\miniconda3\python.exe -m py_compile main.py tests\roles\a1\test_config_contract.py` — PASS.
- `node --check skills\CodeAgent\scripts\codeagent_js_checker.js` — PASS.
- `git diff --check` — PASS; no whitespace errors in the A1 Sprint 3 changes and evidence.
- Tracked-content scan: no values for source-tracking fields and no repository URL. The only URL matches are the Unlicense license reference and existing Node.js installer/GitHub API runtime URLs. The only repository-marker match is C1's local test-loader root variable. Forty-character hexadecimal matches are historic project Git commits in course evidence; none are external-source SHAs. The full commit-subject scan found no source-tracking values.
- Sprint2 A1 PR #11 is merged according to the fresh GitHub API result and remote main history; the stale HTML observation is retained and explained in Week 12 evidence.

## Limitations and environment

Node.js/npm subprocesses are mocked in the A1 role suite. No live npm install, AstrBot host startup, or transitive-package integrity check is claimed. A non-directory `node_modules` path is reported but not deleted automatically. One PowerShell child-process launch failed with `CreateProcessAsUserW` access denied; the same A1 identity and worktree were retained, and validation completed through `cmd.exe` as recorded in Week 10 evidence.
