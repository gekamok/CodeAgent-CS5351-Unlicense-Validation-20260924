# Week 04: B2 review of staged integration

The Week 4 source review confirmed that session identity feeds both `active_sessions` lookups and workspace paths. The current `_sanitize_session_id` does not cover all path separators or constrain dot segments, while `_cleanup_session` recursively removes the joined path. `_create_process_json` likewise uses the caller-provided ID to choose its output directory.

The exit-command check is a substring search and can match text that merely contains the command token. These observations identify concrete Week 5 regression targets: restrict exit-command matching to a command token, constrain session IDs to safe single path components, and ensure cleanup and metadata creation cannot escape the configured workspace.

No Week 4 code change or test execution is claimed for B2. The source remained unchanged through this review, as recorded in `git_evidence.md`.
