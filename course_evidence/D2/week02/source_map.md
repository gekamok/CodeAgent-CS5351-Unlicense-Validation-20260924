WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.
Evidence subject: `docs(d2): week 02 map owned source`

# Week 2: Owned source map

This retrospective source map was written during Week 4 from the staged course tree.

| Source | D2 region | Review concern |
| --- | --- | --- |
| `skills/CodeAgent/scripts/codeagent_security.py` | `SecurityReport`, scanner, checkers, report serialization | Keep severity and report fields stable for callers. |
| `main.py` | `CodeAgentPlugin._call_security_scan` only | Launch the scanner and return a trustworthy structured result. |
| `tests/roles/d2/` | D2 regression artifact | Exercise the D2 report/serialization contract with executable checks. |

The staged project keeps the security scanner as a separate script under the CodeAgent skill directory. This mapping records ownership and source location, not historical implementation activity.
