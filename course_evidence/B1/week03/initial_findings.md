WEEK4_CATCH_UP
Created during Week 4 to document an earlier course stage.

# Week 3 — Initial Findings

This is a Week 4 retrospective static review of the Week 4 baseline. It does not represent Week 3 test execution or observed runtime behavior.

- `_extract_requirement` tries two `/agent` trigger patterns and strips leading and trailing whitespace from the captured text. The `.` capture does not span newline characters, so a multi-line requirement is a candidate regression case.
- `_is_in_blacklist` reads two configuration lists and stringifies both configured values and the incoming identifiers before membership checks. Empty or absent lists do not block a request.
- `_assess_project` uses ordered substring checks to choose a project type, then labels size from requirement character count (`S` below 30, `M` below 100, otherwise `L`). Keyword overlap and boundary values deserve explicit regression coverage.

These are static observations from the source, not verified defects. No tests or runtime commands were run for the reconstructed Week 3 stage. Sprint 1 work should establish executable checks before making any behavior claim.
