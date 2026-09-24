WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.

# D1 initial findings — Week 3 retrospective

This retrospective records findings from the Week 4 catch-up inspection, before Week 5 changes. It does not attribute these observations or any tests to Week 3 itself.

## Findings from inspection

- Checker tool discovery used the POSIX `which` command, which is not the Windows command locator.
- Checker runs reused one fixed temporary directory and removed it recursively, so concurrent processes could overwrite or remove one another's inputs.
- The checker invoked its CLI unconditionally on module load, which prevented direct library imports for focused tests.
- The sandbox imported the POSIX-only `resource` module unconditionally. The available Windows Python reported `ModuleNotFoundError` for that module.
- `StandardExecutor._build_env` treated `workspace_root` as a `Path` even though its configuration type and default are strings.
- The timeout manager assumed `SIGALRM`; a Windows execution path needs a platform-aware timeout mechanism.

These were inspection and environment findings only. No Week 3 test or fix is claimed. Week 5 work will add regression coverage and address the bounded checker and sandbox issues above.
