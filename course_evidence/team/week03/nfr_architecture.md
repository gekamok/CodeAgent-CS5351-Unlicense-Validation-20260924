WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.

# Nonfunctional Requirements and Architecture Targets

This retrospective defines requirements to verify; it does not claim runtime behavior has passed.

## Security

- Treat project paths, task text, and subprocess inputs as untrusted.
- Keep execution restrictions and security checks reviewable as separate boundaries.
- Avoid exposing credentials or unrelated filesystem contents in reports.

## Reliability

- Make subprocess completion, session cleanup, and error reporting deterministic.
- Keep snapshot and rollback behavior bounded and testable.
- Preserve useful diagnostics when a workflow stage fails.

## Performance and Resource Control

- Bound subprocess duration, captured output, and concurrent work.
- Avoid repeated dependency work where safe caching is possible.
- Measure resource behavior with repeatable tests before claiming performance.

## Static Component Map

The staged design separates packaging, sandbox execution, security reporting, and JavaScript checks into named modules under the CodeAgent skill scripts. Their runtime contracts remain subject to Week 5 and later validation.