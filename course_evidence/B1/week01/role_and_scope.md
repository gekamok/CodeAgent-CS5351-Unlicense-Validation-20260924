WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.

# Week 1 — Role and Scope

This is a retrospective record written during Week 4. It does not claim that a Week 1 artifact or activity occurred at the time.

B1 owns three requirement and access-assessment helpers in `main.py`:

- `CodeAgentPlugin._extract_requirement`: identify the requirement text following the `/agent` trigger.
- `CodeAgentPlugin._is_in_blacklist`: compare user and group identifiers with configured deny lists.
- `CodeAgentPlugin._assess_project`: classify a requirement and estimate its size.

The role boundary is limited to these methods and role-specific B1 evidence or verification files. Other `main.py` methods remain owned by their assigned roles. Any shared-file edit must stay inside the three named method bodies.

No Week 1 implementation or validation is asserted here. This scope statement was reconstructed from the Week 4 course baseline and role assignment.
