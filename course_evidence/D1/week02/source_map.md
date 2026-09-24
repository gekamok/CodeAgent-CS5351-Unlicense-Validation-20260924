WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.

# D1 source map — Week 2 retrospective

This map was written during the Week 4 catch-up from the D1 ownership assignment and the current code layout. It is not evidence that the mapping was completed during Week 2.

| Area | Owned artifact | Boundary and observed responsibility |
| --- | --- | --- |
| Sandbox execution | `skills/CodeAgent/scripts/codeagent_sandbox.py` | Configuration, resource and time limits, session workspaces, and standard or restricted execution. |
| JavaScript and TypeScript checks | `skills/CodeAgent/scripts/codeagent_js_checker.js` | Language detection, optional ESLint and TypeScript runs, security findings, quality scoring, and the command-line interface. |
| Checker package setup | `skills/CodeAgent/scripts/package.json` | Node engine declaration, optional development dependencies, and checker scripts. |
| Sandbox wrapper | `_call_sandbox` in `main.py` | Resolves the sandbox script under the shared scripts directory, invokes Python, and converts process output to the caller result. |
| Checker wrapper | `_call_js_checker` in `main.py` | Resolves the checker under the shared scripts directory, invokes Node, and parses checker output. |

The two wrapper functions are D1's only `main.py` ownership. Edits to neighboring orchestration functions require coordination and are outside this assignment.
