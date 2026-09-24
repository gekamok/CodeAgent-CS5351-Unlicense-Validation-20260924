# D1 Week 9 Sprint 2 summary

## Sprint 2 work

- Week 6 added bounded ESLint and TypeScript subprocess execution, structured timeout and analyzer failures, fail-closed handling for silent nonzero exits, and visible temporary-directory cleanup failures.
- Week 7 expanded regression coverage for diagnostic and empty analyzer output, cleanup errors, and empty input.
- Week 8 reviewed current `origin/main` at `578358514b835f7d5ded008bcf66dc2f33c7da07`. No D1 interface changes were present. The D1-owned wrappers now use the active Python interpreter for sandbox launch and fail closed when the checker or Node is unavailable, execution times out, JSON is invalid, or process status contradicts a reported pass.
- Week 9 reran the complete D1 Python and JavaScript role suites, checked JavaScript syntax, exercised the checker CLI with TypeScript input, and scanned the committed D1 changes for forbidden source-tracking metadata.

Sprint commits before this summary: `de735f6` (`test(d1): week 06 verify owned behavior`), `f497a9a` (`test(d1): week 07 expand verification`), and `0ba194f` (`docs(d1): week 08 integration review`).

## Validation performed

| Command/check | Result |
| --- | --- |
| `C:\ProgramData\miniconda3\python.exe -m unittest discover -s tests\roles\d1 -p test_*.py -v` (authorized execution path, rerun after the earlier restricted-path errors) | PASS, 11 tests |
| `C:\ProgramData\miniconda3\python.exe -B -m unittest discover -s tests\roles\d1 -p test_*.py -v` | PASS, 11 tests |
| `node --check skills\CodeAgent\scripts\codeagent_js_checker.js` | PASS |
| `node --check tests\roles\d1\codeagent_js_checker.test.mjs` | PASS |
| `node --test --test-isolation=none tests\roles\d1\codeagent_js_checker.test.mjs` | PASS, 13 tests |
| `node skills\CodeAgent\scripts\codeagent_js_checker.js --code "const value: string = 'typed';" --language typescript` | Returned exit code 1 with `passed: false`; ESLint and TypeScript are unavailable and the result is incomplete, as expected |
| `git diff --check 7f407b7..HEAD` | PASS |
| Tracked D1 commit scan for source repository/path/URL/SHA/ref tracking fields | No matches |

An earlier restricted-path Python run failed with Windows `PermissionError` (`WinError 5`) while creating or cleaning temporary session directories (Week 6: 2 passed, 3 errored; Week 8: 8 passed, 3 errored). Those attempts are environment failures, not passes. The complete 11-test Python suite passed when rerun through the authorized execution path above.

## Limitations and Sprint 3 follow-up

ESLint and TypeScript executables are unavailable, so the checker CLI reports both analyzers as incomplete; their timeout and failure behavior is covered with injected subprocess outcomes. Windows does not provide the POSIX `resource` module here, so resource caps were not exercised. The RestrictedPython runtime was not exercised. Sprint 3 should add another D1-owned failure-path or cleanup improvement, rerun the full role suite, and retain these environment limitations in the final evidence.
