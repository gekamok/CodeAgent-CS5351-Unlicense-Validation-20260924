WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
Evidence subject: `docs(d2): week 03 record initial findings`

# Week 3: Initial findings

This is a Week 4 retrospective. The notes describe source behavior visible in the Week 4 staged tree and do not claim earlier testing.

- `SecurityReport.to_json()` used `dataclasses.asdict()` followed by `default=str`; enum values therefore serialize as names such as `RiskLevel.HIGH`, while `_call_security_scan` checks for the lowercase string `high` or `critical`.
- `_generate_summary()` assigns `summary` dynamically, but the dataclass conversion omitted that non-field attribute from the JSON report.
- `_call_security_scan()` invoked a literal `python3` executable and treated any exception as a passing scan, which could let an unavailable or malformed scan result proceed.

These are review findings, not claims that a vulnerability exploit or runtime failure was observed before Week 4.
