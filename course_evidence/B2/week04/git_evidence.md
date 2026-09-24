# Week 04: B2 Git evidence

After the Week 1–3 retrospective commits and before the Week 4 evidence was added, the following checks were run from `course/b2`:

- `git status --short --branch` reported `## course/b2...origin/main [ahead 3]` with no working-tree entries.
- `git diff --exit-code origin/main -- main.py` returned exit code 0.
- `git diff --stat origin/main -- main.py` printed no changes.
- `git log --oneline -4` showed the three B2 documentation commits above the Week 4 integration commit.

This verifies that B2's `main.py` source remained unchanged through the Week 4 retrospective gate. The documentation commits were limited to `course_evidence/B2/**`.
