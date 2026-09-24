import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "skills" / "CodeAgent" / "scripts"))

from codeagent_packager import ProjectPackager  # noqa: E402


class ProjectPackagerPathTests(unittest.TestCase):
    def setUp(self):
        self.test_root_context = tempfile.TemporaryDirectory(
            prefix="c2-packager-test-", dir=REPO_ROOT
        )
        self.test_root = Path(self.test_root_context.name)
        self.original_tempdir = tempfile.tempdir
        tempfile.tempdir = str(self.test_root)
        self.addCleanup(self._restore_tempdir)
        self.addCleanup(self.test_root_context.cleanup)

    def _restore_tempdir(self):
        tempfile.tempdir = self.original_tempdir

    def test_safe_relative_paths_are_written_inside_archive(self):
        output_dir = self.test_root / "archives"
        packager = ProjectPackager(str(output_dir))

        result = packager.pack(
            files=[
                {"name": "main.py", "content": "print('hello')\n"},
                {"name": "pkg/helper.py", "content": "VALUE = 1\n"},
            ],
            test_files=[
                {"name": "test_main.py", "content": "def test_smoke(): assert True\n"}
            ],
            name="safe-project",
            extra_files=[{"name": "docs/notes.txt", "content": "included\n"}],
        )

        self.assertTrue(result["success"], result["error"])
        with zipfile.ZipFile(result["zip_path"]) as archive:
            names = set(archive.namelist())

        self.assertIn("safe-project/src/main.py", names)
        self.assertIn("safe-project/src/pkg/helper.py", names)
        self.assertIn("safe-project/tests/test_main.py", names)
        self.assertIn("safe-project/docs/notes.txt", names)

    def _assert_rejected(self, **pack_kwargs):
        output_dir = self.test_root / "archives"
        result = ProjectPackager(str(output_dir)).pack(**pack_kwargs)

        self.assertFalse(result["success"])
        self.assertTrue(result["error"])
        self.assertEqual(result["zip_path"], "")
        self.assertEqual(list(output_dir.glob("*.zip")), [])

    def test_rejects_traversal_and_absolute_project_file_names(self):
        unsafe_names = (
            "../escape.py",
            "nested/../../escape.py",
            r"..\..\escape.py",
            r"C:\temp\escape.py",
            "/tmp/escape.py",
        )
        for name in unsafe_names:
            with self.subTest(name=name):
                self._assert_rejected(files=[{"name": name, "content": "x"}])

    def test_rejects_unsafe_test_and_extra_file_names(self):
        self._assert_rejected(
            files=[{"name": "main.py", "content": "pass\n"}],
            test_files=[{"name": "../../outside.py", "content": "pass\n"}],
        )
        self._assert_rejected(
            files=[{"name": "main.py", "content": "pass\n"}],
            extra_files=[{"name": "../outside.txt", "content": "outside\n"}],
        )

    def test_rejects_project_names_that_escape_the_temporary_root(self):
        for name in ("..", "folder/project", r"..\project", r"C:\escape", "/absolute"):
            with self.subTest(name=name):
                self._assert_rejected(name=name, files=[])


if __name__ == "__main__":
    unittest.main()
