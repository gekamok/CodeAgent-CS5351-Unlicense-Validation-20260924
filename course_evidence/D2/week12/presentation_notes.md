# Week 12: D2 presentation notes

## Owned module and contribution

D2 owns `skills/CodeAgent/scripts/codeagent_security.py`, the `SecurityReport` and scanner/checker code, the D2 security report tests, and `_call_security_scan()` in `main.py`.

- Sprint 1 added the security scanner and its D2 tests. The Week 5 team closeout records D2 PR #1 as MERGED at `32eb9f5` and records a high-risk scanner smoke check with the expected critical finding and `passed=false` result.
- Sprint 2 hardened `_call_security_scan()` against malformed JSON and report schemas, contradictory process/report status, and high-risk reports marked passed. The Week 9 closeout records D2 PR #12 as MERGED at `a3b7eb3`; its recorded role validation was 9 tests, `py_compile`, `git diff --check`, and a source-metadata scan.
- Sprint 3 Week 10 added SecurityReport schema version 1, analyzer availability status, explicit heuristic/incomplete-coverage limitations, and wrapper validation for versioned metadata. Commit `7b01245` is `test(d2): week 10 add sprint 3 improvement`.
- Sprint 3 Week 11 made the scanner JSON boundary reject duplicate keys and added a conflicting-risk-level regression. Commit `f475faf` is `test(d2): week 11 run role regression`.

## Validation and solved problems

- Week 10: the D2 suite passed 11 tests; `py_compile` and `git diff --check` passed. A direct scanner invocation returned exit code 0 and identified the unavailable optional analyzers in its versioned report.
- Week 11: the D2 suite passed 12 tests, including duplicate JSON field rejection; `py_compile`, `git diff --check`, and the forbidden source-metadata scan passed.
- The scanner report now distinguishes a clean result from analyzer availability and states that built-in patterns are heuristic. The wrapper also rejects malformed or ambiguous subprocess output instead of accepting a parser-selected duplicate value.

## Limitations

- The Week 10 direct run reported Ruff, Mypy, and Bandit unavailable. Those checks therefore remain unverified.
- Built-in security patterns do not establish rule completeness. The tests exercise scanner and wrapper boundaries; they do not prove a complete threat model or live AstrBot integration.
- The Week 10 compile and diff checks initially encountered a PowerShell `CreateProcessAsUserW` access denial when launched in parallel. Both passed when rerun through `cmd.exe` under the same D2 identity.
