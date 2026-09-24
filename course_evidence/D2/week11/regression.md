# Week 11: D2 scanner regression

## Regression and boundary change

`_call_security_scan()` now rejects duplicate keys anywhere in subprocess JSON. Python's default decoder silently keeps one duplicate value; the wrapper now fails closed with an explicit duplicate-field error. Added a regression case with conflicting `risk_level` keys and verified it returns a high-risk unavailable result.

## Validation performed

- `C:\ProgramData\miniconda3\python.exe tests\roles\d2\test_security_report.py` — PASS, 12 tests.
- `C:\ProgramData\miniconda3\python.exe -m py_compile main.py skills\CodeAgent\scripts\codeagent_security.py tests\roles\d2\test_security_report.py` — PASS, exit code 0.
- `git diff --check` — PASS, exit code 0.
- Forbidden source-metadata scan — PASS, no matches (exit code 1 means no matches).

## Limitations

- Ruff, Mypy, and Bandit were unavailable in the actual Week10 scanner smoke run; security checks from those tools remain unverified in this environment.
- Duplicate-key rejection improves report integrity but does not increase the built-in rule set or establish scanner-rule completeness.
