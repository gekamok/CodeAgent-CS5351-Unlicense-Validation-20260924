# D1 Week 5 baseline

## Engineering changes

- The JavaScript checker now discovers command-line tools with the platform's locator, uses a unique temporary directory for each check, and can be imported without launching its command-line interface.
- A requested analysis that is unavailable or fails now produces an incomplete result instead of a passing result. `package.json` runs the D1 regression suite through `npm test` and retains the old demo under `test:demo`.
- The sandbox can import on Windows when the POSIX `resource` module is absent. Its resource limiter becomes a no-op on that platform; its timeout manager uses a timer fallback when `SIGALRM` is unavailable.
- Standard sandbox execution now uses the active Python interpreter on Windows, preserves the Windows command search path, constructs the temporary directory path from the string configuration, and relies on the child-process timeout to terminate standard executions.
- Added six JavaScript checker regression tests and five Python sandbox tests under `tests/roles/d1/`.

## Validation performed

| Command | Result |
| --- | --- |
| `node --check skills/CodeAgent/scripts/codeagent_js_checker.js` | PASS |
| `node --check tests/roles/d1/codeagent_js_checker.test.mjs` | PASS |
| `npm test --prefix skills/CodeAgent/scripts` | PASS, 6 tests |
| `$env:PYTHONDONTWRITEBYTECODE='1'; C:\ProgramData\miniconda3\python.exe -m unittest discover -s tests/roles/d1 -p 'test_*.py' -v` | PASS, 5 tests |
| `git diff --check` | PASS |
| `node skills/CodeAgent/scripts/codeagent_js_checker.js --code "const message: string = 'hello';" --language typescript` | Ran and returned exit code 1 with `passed: false`; ESLint and TypeScript were unavailable, so this is an incomplete check, not a TypeScript pass. |

The JavaScript unit tests stub successful analyzer results for security and result-reset cases, so those checks do not depend on optional global tools. A separate test verifies that an unavailable requested analyzer is reported as incomplete. The Python tests exercise string workspace configuration, the no-`resource` fallback, timer fallback, standard Python execution, and child-process timeout handling.

## Validation limits

The available Windows Python did not provide the POSIX `resource` module. CPU, memory, file-size, process-count, and descriptor limits therefore were not exercised on this platform. Standard subprocess execution and its timeout were exercised; execution through the actual RestrictedPython dependency was not run. ESLint and TypeScript command integrations were unavailable and are reported as incomplete by the checker.
