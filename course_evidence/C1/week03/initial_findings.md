WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.

# Initial Findings

Static source inspection found two behaviors worth verifying in C1's owned code:

1. A typical Python traceback places the source line on a File frame and the exception type on a later line. The current error analyzer only searches the exception line for a line number, so it can report line 0 for that traceback.
2. Snapshot filenames use whole-second timestamps. Two saves for the same session and step during one second can target the same file and overwrite earlier state.

These are source-based hypotheses recorded during Week 4, not executed findings. No test, meeting, user observation, or runtime PASS is claimed for Weeks 1–3.
