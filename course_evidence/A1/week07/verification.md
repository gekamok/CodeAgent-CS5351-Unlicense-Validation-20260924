# A1 Week 7 verification

## Expanded boundary and failure coverage

The A1 suite now checks that dependency setup avoids probing Node.js when the checker, package manifest, or `node_modules` directory makes an installation unnecessary. It covers missing Node.js/npm executables, a Node.js probe timeout or nonzero exit, npm timeout, and a nonzero npm result with no stderr. These checks run the production methods in an isolated harness with subprocess calls mocked.

The dependency path now checks all installation prerequisites before invoking Node.js, reports probe failures, and gives npm failures a useful fallback message when subprocess output is empty. The five-second Node.js probe timeout and typed config fallback from Week 6 remain covered by the role suite.

## Validation run

- `C:\ProgramData\miniconda3\python.exe tests\roles\a1\test_config_contract.py` — PASS; 15 tests ran.
- `C:\ProgramData\miniconda3\python.exe -m py_compile main.py tests\roles\a1\test_config_contract.py` — PASS; no syntax errors.
- `node --check skills\CodeAgent\scripts\codeagent_js_checker.js` — PASS; JavaScript syntax check completed.
- `git diff --check` — PASS; no whitespace errors.

## Remaining gaps

The Node.js/npm failure branches are simulated; a real npm install and AstrBot host startup were NOT_RUN. Automatic Node.js installation by platform, partially populated `node_modules`, and runtime behavior on other operating systems remain unverified.
