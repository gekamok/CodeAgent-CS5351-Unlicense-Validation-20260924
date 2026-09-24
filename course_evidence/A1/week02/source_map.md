WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.

# A1 source map

This retrospective maps the A1-owned Week 2 areas as observed during the Week 4 catch-up:

- `metadata.yaml` identifies the AstrBot plugin, its Python entry point, compatibility declaration, supported platforms, and tags.
- `_conf_schema.json` defines configuration keys, types, defaults, and operator-facing hints. The implementation reads these values through `CodeAgentPlugin._get_config` in `main.py`.
- `pyproject.toml` declares the Python package name, version, minimum Python version, runtime dependencies, and optional build tools.
- In `main.py`, `_get_config` delegates key/default lookup to the host configuration object. `_ensure_nodejs` checks for Node.js and chooses an installation path by platform. `_ensure_js_dependencies` checks for the JavaScript checker and package manifest and attempts npm dependency installation when `node_modules` is absent.
- The JavaScript checker and its manifest are under `skills/CodeAgent/scripts/`; A1's ownership here covers only the startup preparation path in `main.py`, not the checker implementation.

This file was created during Week 4 from repository inspection. No runtime result or earlier source-map activity is asserted.
