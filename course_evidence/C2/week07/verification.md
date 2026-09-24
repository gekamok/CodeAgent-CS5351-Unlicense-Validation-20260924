# C2 Week 7 Verification

## Verification expansion

Extended `tests/roles/c2/test_packager_paths.py` to cover malformed collections and entries, non-text content, duplicate member names, file/directory prefix collisions, collisions with generated and user files, cleanup after a project-tree write failure, cleanup when archive integrity verification fails, and the successful nested-path contract. The failure tests assert that neither a published ZIP nor a temporary project/archive remains.

## Validation

Command:

```text
C:\ProgramData\miniconda3\python.exe -B -m unittest discover -s tests\roles\c2 -v
```

Result: **PASS**, 11 tests ran and reported `OK`.

`git diff --check` completed without whitespace errors; Git emitted only its line-ending normalization warning for the modified test file.

## Remaining coverage gap

The suite tests `ProjectPackager` directly. It does not exercise the full `main.py::_call_packager` subprocess contract or npm dependency installation, and it uses injected write/integrity failures rather than a real storage-device failure.
