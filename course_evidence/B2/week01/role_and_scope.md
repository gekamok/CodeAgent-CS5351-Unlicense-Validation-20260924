WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.

# Week 01: B2 role and scope

This retrospective records the B2 ownership established for the session lifecycle and process metadata portions of `main.py`. B2 owns `_is_exit_command`, `_sanitize_session_id`, `_cleanup_session`, the `active_sessions` state, and `_create_process_json`.

The work is limited to recognizing exit commands, deriving safe per-user session identifiers, cleaning session directories, tracking active work, and writing process metadata. Changes to orchestration outside the named state-management regions belong to other roles.

This record was written during Week 4 from the repository state available then. It does not claim a Week 1 meeting, implementation, or test run.
