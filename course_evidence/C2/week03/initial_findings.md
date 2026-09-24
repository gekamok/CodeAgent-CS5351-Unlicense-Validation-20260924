WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.

# C2 Initial Findings

These notes were made during the Week 4 retrospective review of the packaging code present in the earlier Week 3 stage. They do not claim that the findings were recorded or acted on during Week 3.

- Packaging combines caller-supplied file names with filesystem paths when constructing the temporary project tree. The reviewed code has no explicit check that these names remain relative to the intended project directory; add executable path-boundary coverage before relying on that input boundary.
- Dependency discovery uses AST parsing for Python imports and regular-expression matching for Node imports. The parsing rules and generated metadata should be exercised with representative inputs.
- The CLI and `_call_packager` communicate through JSON, so malformed output and subprocess failure paths merit verification.

These are static review observations and verification targets only. No command, test, defect reproduction, or PASS result is claimed for Week 3.
