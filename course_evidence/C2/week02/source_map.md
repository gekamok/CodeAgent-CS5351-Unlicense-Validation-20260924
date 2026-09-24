WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.

# C2 Source Map

This map was reconstructed during Week 4 from the Week 2 repository state. It identifies the C2 code surfaces without claiming earlier inspection or test activity.

- `main.py`, `CodeAgentPlugin._call_packager`: constructs the helper command, passes files and optional tests as JSON, then decodes the helper's JSON output.
- `skills/CodeAgent/scripts/codeagent_packager.py`, `DependencyGenerator`: detects Python and Node dependencies and generates requirements, `pyproject.toml`, or `package.json` content.
- `skills/CodeAgent/scripts/codeagent_packager.py`, `ProjectPackager`: builds project metadata and files, writes a temporary project tree, generates supporting files, cleans temporary artifacts, and creates a ZIP archive.
- `skills/CodeAgent/scripts/codeagent_packager.py`, `create_project_file`: maps file extensions to language names and records content size and description.

This is a source-location map, not a runtime correctness assessment. No C2 command or test result is asserted for Week 2.
