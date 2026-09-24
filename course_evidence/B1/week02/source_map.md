WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.

# Week 2 — Owned Source Map

This retrospective source map was prepared during Week 4. It records the Week 4 baseline layout, not a contemporaneous Week 2 inspection.

| Owned method | Week 4 location | Inputs and dependencies | Responsibility |
| --- | --- | --- | --- |
| `CodeAgentPlugin._extract_requirement` | `main.py`, lines 43–52 | Message text; Python `re` | Returns trimmed text after an `/agent` trigger or `None`. |
| `CodeAgentPlugin._is_in_blacklist` | `main.py`, lines 60–67 | `_get_config`, `admin_blacklist`, `group_blacklist` | String-normalizes identifiers before membership checks. |
| `CodeAgentPlugin._assess_project` | `main.py`, lines 401–428 | Requirement string; string operations | Selects a project type and size label. |

The three methods share `main.py` with other role-owned regions. B1 source edits must be confined to these method bodies. B1 verification material belongs under `tests/roles/b1/`; retrospective and sprint evidence belongs under `course_evidence/B1/`.

No dynamic checks were run for this Week 2 retrospective. The location and behavior notes come from static reading of the Week 4 baseline.
