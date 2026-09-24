# Week 5 C1 Baseline and Regression Work

## Change

The role baseline in tests/roles/c1/test_debug_snapshot_baseline.py exercises the actual C1 helper methods from main.py. It imports the plugin with a minimal AstrBot API stub and uses a temporary workspace.

The Week 4 implementation had three reproducible gaps: traceback frame lines were reported as 0, ModuleNotFoundError produced only the generic runtime hint, and two saves in one second reused a snapshot filename. The initial command run was:

- Command: C:\ProgramData\miniconda3\python.exe tests\roles\c1\test_debug_snapshot_baseline.py
- Result: 4 tests ran; 3 failed. The failing behaviors were traceback line extraction, missing-module guidance, and same-second snapshot preservation.

The import assertion was then made locale-independent by checking that the missing package name is retained in the hint. It now covers both ImportError and ModuleNotFoundError.

The implementation now retains the last traceback line encountered before the exception, recognizes ModuleNotFoundError in the existing import-fix branch, writes snapshots under nanosecond-based names using exclusive file creation with a collision suffix, and orders matching snapshots by filename when restoring. Only C1-owned regions in main.py were changed.

## Validation

- Command: C:\ProgramData\miniconda3\python.exe tests\roles\c1\test_debug_snapshot_baseline.py
- Result: 4 tests ran; OK; exit code 0.
- Command: C:\ProgramData\miniconda3\python.exe -m py_compile main.py tests\roles\c1\test_debug_snapshot_baseline.py
- Result: exit code 0.

The regression suite checks traceback frame selection, missing-module hints for both exception names, distinct snapshot files when the clock returns the same nanosecond value, restoration of the latest colliding snapshot, and the no-snapshot return path. The plugin framework is stubbed and filesystem behavior uses a temporary directory; no live AstrBot session or cross-role integration run is claimed here.
