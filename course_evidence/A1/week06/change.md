# A1 Week 6 change

## Engineering change

`_get_config` now falls back to the caller's default when the host config is absent, its getter raises, or a setting is `None` or has the wrong type. Correctly typed falsey values such as `False`, `0`, and an empty list remain valid. The JavaScript dependency preparation path now bounds its Node.js version probe to five seconds and reports missing, timed-out, or failing Node.js checks. It also reports a missing npm executable and handles failed npm output without assuming stderr is present.

The A1 regression suite exercises these production methods in an isolated harness. Subprocess calls for Node.js and npm are mocked; no package installation is claimed.

## Validation run

- `C:\ProgramData\miniconda3\python.exe tests\roles\a1\test_config_contract.py` — PASS; 10 tests ran.
- `C:\ProgramData\miniconda3\python.exe -m py_compile main.py tests\roles\a1\test_config_contract.py` — PASS; no syntax errors.
- `node --check skills\CodeAgent\scripts\codeagent_js_checker.js` — PASS; JavaScript syntax check completed.
- `git diff --check` — PASS; no whitespace errors.

## Limits

Node.js/npm availability branches were simulated with mocks. A real npm install, AstrBot host startup, and runtime behavior on other platforms were NOT_RUN.
