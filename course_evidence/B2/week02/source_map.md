WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.

# Week 02: B2 source map

This retrospective maps the owned session-lifecycle code in `main.py`:

- `active_sessions` is initialized in `CodeAgentPlugin.__init__` and holds per-session activity metadata.
- `_is_exit_command` recognizes the session termination command before request processing.
- `_sanitize_session_id` constructs the key used for session lookup and its workspace directory.
- `_cleanup_session` removes that session's workspace directory.
- `_create_process_json` creates `process.json` under the selected session directory with request and progress fields.

The command handler reads and updates the same session map around execution. The rest of the request orchestration is outside this B2 map. This record was written during Week 4; no Week 2 code edits or tests are claimed.
