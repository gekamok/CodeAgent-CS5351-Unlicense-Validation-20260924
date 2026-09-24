# Week 11: team regression status

> Created during Week 13 final integration from the already committed Week 11 role evidence. The previous takeover parent was cancelled before this team-level synthesis was committed; this file uses the real current Git date and does not claim earlier existence.

## Role regression status

| Role | Week 11 evidence | Final-gate rerun status |
| --- | --- | --- |
| A1 | Present | PASS — 20 Python tests |
| A2 | Present | PASS — 17 Python tests |
| B1 | Present | PASS — 14 Python tests |
| B2 | Present | PASS — 14 Python tests |
| C1 | Present | PASS — 11 Python tests |
| C2 | Present | PASS — 5 boundary tests plus 11 path tests |
| D1 | Present | PASS — 17 Python tests plus 13 Node tests; Node syntax checks PASS |
| D2 | Present | PASS — 13 Python tests |

The final-gate reruns used each role's own worktree and a writable temporary directory inside that worktree to avoid the previously documented Windows temporary-directory access failures. Those earlier environment failures remain recorded in the role evidence.

## Integration risks carried forward

- Shared `main.py` changes require per-role ownership review before merge.
- Optional external analyzers are not available for every security/checker path; role evidence records those limitations rather than treating unavailable analyzers as validated.
- Live AstrBot host integration is not established by these unit/regression suites.

No Week 14 or later team evidence was created.
