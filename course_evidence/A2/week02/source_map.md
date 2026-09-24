WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.

# Owned Source Map

This retrospective maps A2's scope within the assembled plugin source. It was prepared during Week 4 by static inspection.

| Area | A2 responsibility | Boundary |
| --- | --- | --- |
| `CodeAgentPlugin` lifecycle | Plugin lifecycle and orchestration points used by the user command | Configuration reads and Node/dependency preparation belong to A1. |
| `/agent` and `agent_command` | Event handling, command responses, and calls into the project workflow | Requirement parsing and project assessment belong to B1; session identity and process helpers belong to B2. |
| Main orchestration | Sequence calls to debugging, security, JavaScript, sandbox, snapshot, and packaging components | The component implementations belong to C1, C2, D1, and D2. |
| `terminate` | Shutdown cleanup for active plugin sessions | Session/process helper behavior remains B2's scope. |
| `get_star` | Plugin construction entry point | Configuration schema and config-reading implementation remain A1's scope. |

This map records code boundaries, not completed tests or runtime behavior. The Week 4 retrospective does not claim this evidence existed during Week 2.
