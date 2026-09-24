WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.

# Owned Source Map

This retrospective map is based on the Week 4 integrated main.py.

- _analyze_error scans stderr for an Error or Exception type, extracts a line number when the matching line contains one, and retains a bounded error excerpt.
- _generate_debug_fix maps recognized import, name, type, file, connection, permission, key, index, value, and syntax errors to a repair hint.
- _save_snapshot writes the step, timestamp, generated code, and file list as JSON under the session snapshots directory.
- _rollback_to_snapshot searches that directory for files matching the requested step and reads the newest file by modification time; missing or unreadable snapshots return None.
- The debug loop invokes the sandbox, calls the two error helpers after a failed run, appends the suggested change, and retries up to the configured limit.

The debug loop also calls the sandbox helper, which is outside C1's ownership. Configuration and the surrounding command handler have other role owners. C1 changes must stay within the listed debug loop and helper methods.
