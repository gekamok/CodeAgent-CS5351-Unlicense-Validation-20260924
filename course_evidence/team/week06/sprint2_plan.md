# Sprint 2 plan — Weeks 6–9

## Gate and planning basis

Sprint 1 is closed: PRs #1–#8 are merged, and all eight role branches were fast-forwarded to the Sprint 1 closeout commit. Planning starts from the real Week 5 source changes, role baselines, tests, and limitations already in the repository. These are planned objectives; this file does not claim Week 6–9 work or validation has happened.

## Role goals

| Role | Week 5 starting point | Sprint 2 engineering and verification goal |
| --- | --- | --- |
| A1 | Configuration contract suite for metadata/schema defaults, `_get_config`, and dependency preparation; tests mock process execution. | Tighten configuration and dependency-preparation behavior in A1-owned regions. Add executable checks for malformed or missing config values and unavailable Node/npm paths; keep mocked process checks distinct from actual installation claims. |
| A2 | Plugin factory/orchestration baseline covers construction, prompting, blacklist rejection, duplicate sessions, and cleanup. | Improve the `/agent` command orchestration path for a concrete request/response failure case. Expand tests for command dispatch and shutdown/termination behavior while leaving B1 requirement logic and B2 session internals to those owners. |
| B1 | Multi-line requirement extraction and boundary classification tests cover empty input, blacklist normalization, project keywords, and size limits. | Strengthen requirement extraction and project assessment for whitespace, mentions, and multi-line boundary cases; add executable regression checks around any behavior changed. |
| B2 | Session lifecycle work sanitizes identifiers and constrains cleanup/process metadata to the workspace. | Harden session lifecycle handling for malformed, colliding, or stale session state. Expand tests for path containment and cleanup failure behavior within B2-owned state methods. |
| C1 | Debug/snapshot baseline fixes traceback location, missing-module hints, and same-time snapshot collisions. | Improve snapshot/debug-loop recovery when a snapshot is unavailable or invalid, with focused failure-path tests for C1-owned methods. |
| C2 | Packager rejects unsafe paths and uses platform-appropriate temporary output; tests cover archive membership and traversal. | Make package creation more robust against partial output or invalid archive inputs. Add regressions for failure cleanup and safe nested paths within the packager ownership boundary. |
| D1 | Windows compatibility fallbacks, per-run checker temp directories, incomplete-tool reporting, and sandbox tests; POSIX limits and RestrictedPython runtime remain unverified. | Improve D1-owned failure reporting and cleanup around checker/sandbox execution, including timeouts or unavailable analyzers. Keep unsupported platform/resource limits explicitly incomplete and add executable tests for observed behavior. |
| D2 | Security report serialization includes machine-readable severity and summary; scan wrapper fails closed for missing or malformed results. | Expand security scan contract tests for invalid JSON/schema, timeout, and inconsistent exit/report combinations. Make only D2-owned scan/report changes supported by tests. |

## Week gates and role deliverables

- **Week 6:** each role makes a real owned engineering or executable-verification improvement, runs its validation, writes `course_evidence/<ROLE>/week06/change.md`, and commits `test(<role>): week 06 verify owned behavior`.
- **Week 7:** each role expands boundary, contract, regression, or failure-path verification; writes `course_evidence/<ROLE>/week07/verification.md`; and commits `test(<role>): week 07 expand verification`. The captain records team verification status after checking actual results.
- **Week 8:** each role fetches and reviews the latest available `main`, reruns role validation, records interface impact in `course_evidence/<ROLE>/week08/integration_review.md`, and commits `docs(<role>): week 08 integration review`. Resolve overlap only with the affected owner and captain; no blind conflict selection.
- **Week 9:** each role completes `course_evidence/<ROLE>/week09/sprint2_summary.md`, runs its full role validation, commits `docs(<role>): week 09 close sprint 2`, pushes, and opens exactly one Sprint 2 PR containing only its owned business/test files and role evidence. The captain reviews and merges accepted PRs one at a time, then synchronizes every role branch to the resulting `main` before Sprint 3.

Every role must include at least one non-document engineering artifact during this sprint. Any unavailable tool, unrun check, or environment failure must be recorded as such; no planned work is reported as complete before its gate.
