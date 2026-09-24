# D1 Week 8 integration review

## Main review

Fetched `origin` on the Week8 review date. Latest `origin/main` is `578358514b835f7d5ded008bcf66dc2f33c7da07`; the D1 branch remains based at merge base `7f407b74b7e78fa0956eb4916c7515fa46f13028`. Comparing that base with `origin/main` showed only the team Week7 verification status and Week8 integration review documents; no source or D1 interface changes arrived on main. Main was not merged into this role branch.

The D1 checker result remains a JSON object with its existing `passed`, `issues`, and `summary` fields. `main.py::_call_js_checker` parses that shape, so timeout and cleanup issue records remain compatible. Review found the wrapper reported `passed: true` when the checker script or Node was unavailable and when a subprocess timed out; a nonzero process could also return a contradictory pass. These D1-owned paths now fail closed. `_call_sandbox` now launches the active Python interpreter (`sys.executable`) instead of assuming a `python3` command exists.

## Validation performed

| Command | Result |
| --- | --- |
| `git fetch origin` | PASS |
| `node --check skills/CodeAgent/scripts/codeagent_js_checker.js` | PASS |
| `node --check tests/roles/d1/codeagent_js_checker.test.mjs` | PASS |
| `node --test --test-isolation=none tests/roles/d1/codeagent_js_checker.test.mjs` | PASS, 13 tests |
| `C:\ProgramData\miniconda3\python.exe -B -m unittest discover -s tests\roles\d1 -p test_wrappers.py -v` | PASS, 6 tests |
| `C:\ProgramData\miniconda3\python.exe -B -m unittest discover -s tests\roles\d1 -p test_*.py -v` | FAIL, 8 passed and 3 sandbox tests errored with Windows `PermissionError` (`WinError 5`) creating or cleaning temporary workspace directories |
| `git diff --check` | PASS |

The wrapper tests simulate missing Node/script, timeout, invalid JSON, and contradictory exit/result status. They also verify the sandbox wrapper selects the running Python interpreter. The sandbox failures are recorded as environment errors, not passes.

## Limitations

ESLint and TypeScript executables remain unavailable; their timeout and process-error cases are injected in the JavaScript tests. The Windows interpreter does not provide POSIX `resource` limits, and the RestrictedPython runtime remains unverified.
