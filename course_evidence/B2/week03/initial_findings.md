WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.

# Week 03: initial findings

The reviewed implementation had these initial risks within B2's owned scope:

- `_is_exit_command` searched for `/exitconver` anywhere in the text, so a longer token or quoted text could be treated as a command.
- `_sanitize_session_id` replaced forward slashes and colons, but left other path-significant characters such as backslashes and dot segments unchanged.
- `_cleanup_session` passed `workspace / session_id` directly to recursive deletion without verifying that the resolved target remained inside the workspace.
- `_create_process_json` created the session directory and wrote JSON, but accepted the supplied session identifier without a containment check.

These are source-review observations, not reproduced defects or test results. This retrospective was written during Week 4; no Week 3 implementation or test run is claimed.
