# D1 Week 6 change

## Engineering change

The JavaScript/TypeScript checker now bounds ESLint and TypeScript subprocesses to 15 seconds. Timeouts and nonzero exits without diagnostics are reported as incomplete checks instead of being treated as successful analysis. Unexpected checker exceptions are returned in the structured result, and temporary-directory cleanup failures mark the result as failed while preserving the cleanup detail.

Added regressions for analyzer timeout reporting and timeout options, silent TypeScript process failure, and cleanup after an unexpected analyzer exception.

## Validation performed

| Command | Result |
| --- | --- |
| `node --check skills/CodeAgent/scripts/codeagent_js_checker.js` | PASS |
| `node --check tests/roles/d1/codeagent_js_checker.test.mjs` | PASS |
| `node --test --test-isolation=none tests/roles/d1/codeagent_js_checker.test.mjs` | PASS, 9 tests |
| `node skills/CodeAgent/scripts/codeagent_js_checker.js --code "const value: string = 'typed';" --language typescript` | Returned exit code 1 and `passed: false`; ESLint and TypeScript are unavailable, reported as incomplete |
| `C:\ProgramData\miniconda3\python.exe -m unittest discover -s tests\roles\d1 -p test_*.py -v` | FAIL, 2 tests passed and 3 errored with Windows `PermissionError` (`WinError 5`) while creating or cleaning temporary workspace directories |
| `git diff --check` | PASS |

The JavaScript tests inject analyzer timeout and process-exit errors; they do not claim that global ESLint or TypeScript ran. Python sandbox tests were attempted but could not complete under the current filesystem permissions.

## Limitations

The Windows interpreter has no POSIX `resource` module, so CPU, memory, file-size, process-count, and descriptor limits remain unverified. The RestrictedPython execution path was not run. The Python test errors are recorded as environment failures, not passes.
