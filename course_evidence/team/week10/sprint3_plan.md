# Week 10: Sprint 3 plan

## Sprint goal

Sprint 3 covers Weeks 10–13. Each role will make and validate an owned engineering improvement in Week 10, strengthen regression and failure-path behavior in Week 11, prepare evidence from real changes and runs in Week 12, then complete a verified Week 13 summary and one final Sprint3 PR. No role-week evidence is created before its week.

## Goals from Sprint 2 review

| Role | Sprint 3 technical goal | Ownership boundary |
| --- | --- | --- |
| A1 | Exercise configuration fallback and Node/npm dependency preparation more deeply, including missing tools and partial dependency state. | `metadata.yaml`, `_conf_schema.json`, `pyproject.toml`, and configuration/dependency-preparation regions of `main.py`. |
| A2 | Strengthen response-stream closure, replacement-session, and shutdown lifecycle behavior with regression coverage. | `CodeAgentPlugin`, `/agent`, `agent_command`, `terminate`, `get_star`, and orchestration regions of `main.py`. |
| B1 | Expand requirement-token boundaries and project classification cases while preserving multiline and Unicode behavior. | `_extract_requirement`, `_is_in_blacklist`, and `_assess_project`. |
| B2 | Harden safe session cleanup and process metadata boundaries, including failure outcomes and stale state. | `_is_exit_command`, `_sanitize_session_id`, `_cleanup_session`, `active_sessions`, and `_create_process_json`. Coordinate the cleanup result contract with A2 without editing A2-owned regions. |
| C1 | Address the Sprint 2 gap that `_rollback_to_snapshot` is not called by the current debug loop; validate recovery behavior through the C1-owned flow. | `_analyze_error`, `_generate_debug_fix`, `_save_snapshot`, `_rollback_to_snapshot`, and the debug loop. |
| C2 | Test packager input/output contracts and failure cleanup through both the packager and the owned `_call_packager` boundary. | `_call_packager`, `codeagent_packager.py`, `ProjectPackager`, and `DependencyGenerator`. |
| D1 | Improve sandbox/checker subprocess reliability and preserve fail-closed behavior when optional tools or runtimes are unavailable. | `codeagent_sandbox.py`, `codeagent_js_checker.js`, `package.json`, `_call_sandbox`, and `_call_js_checker`. |
| D2 | Improve security report schema and rule-boundary coverage; keep scanner limitations explicit where optional tools are unavailable. | `codeagent_security.py`, `SecurityReport`, checker/test classes, and `_call_security_scan`. |

## Weekly checkpoints

- **Week 10:** one owned source, test, checker, script, or config improvement; role `improvement.md`; actual validation; commit `test(<role>): week 10 add sprint 3 improvement`.
- **Week 11:** regression, cleanup, or boundary/failure-path work; role `regression.md`; rescan for forbidden source metadata; actual validation; commit `test(<role>): week 11 run role regression`.
- **Week 12:** `presentation_notes.md` using real Git, test, and PR evidence, with owned module, concrete changes, validation, solved problems, limitations, and contribution; commit `docs(<role>): week 12 prepare presentation evidence`.
- **Week 13:** `final_summary.md`; verify required role evidence for Weeks 1–13, run the role suite, check clean tree and forbidden metadata, commit `docs(<role>): week 13 finalize role evidence`, push, and open one Sprint3/final PR containing only role-owned code/tests and role evidence.

## Integration rules

All eight role branches begin from the Week 9 closeout commit. Each role stays in its assigned worktree and branch. Role workers do not merge or rebase `main`; integration remains a parent gate. Keep `main.py` edits inside the role regions above and inspect overlapping hunks explicitly. A genuine ownership defect returns to its owning role. Each role's final PR will be reviewed individually and merged only after its Week 10–13 evidence and validation are present.

Captain Week 11–13 team evidence will be written only after the corresponding role evidence and integration status exist. Week 11 will record regression status and the forbidden-metadata scan; Week 12 will assemble presentation/report preparation from real role evidence; Week 13 will state final integration and validation status. Existing Sprint 1 and Sprint 2 history remains unchanged.