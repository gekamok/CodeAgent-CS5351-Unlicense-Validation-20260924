# A1 Week 5 baseline

## Engineering artifact

Added `tests/roles/a1/test_config_contract.py` as a standard-library `unittest` suite. It checks that plugin and Python package names and versions agree, every configuration schema entry has a typed default and operator help, required settings are present, and the production `_get_config` method returns both host values and caller defaults. It also exercises the production JavaScript dependency-preparation method in an isolated harness: npm is requested only when the checker and manifest exist, Node.js is available, and `node_modules` is absent; an existing `node_modules` directory suppresses installation. The harness replaces process execution with mocks, so it does not install packages or access the network.

## Validation run

- `C:\ProgramData\miniconda3\python.exe tests\roles\a1\test_config_contract.py` — PASS; 6 tests ran.
- `C:\ProgramData\miniconda3\python.exe -m py_compile main.py tests\roles\a1\test_config_contract.py` — PASS; no syntax errors.
- `node --check skills\CodeAgent\scripts\codeagent_js_checker.js` — PASS; JavaScript syntax check completed.

The first draft of the role test used temporary fixture files and the same test command failed with `PermissionError` before reaching assertions because the execution environment denied writes to temporary directories. The tests were changed to use an in-memory path fake, then the command above passed all 6 tests without fixture writes.

## Limits

The tests do not start the AstrBot plugin host, execute Node.js installation, invoke a real npm install, or prove runtime availability of Node.js on other platforms. The Node command above checks the existing JavaScript checker syntax only. No A1 business source was changed in this Week 5 increment.
