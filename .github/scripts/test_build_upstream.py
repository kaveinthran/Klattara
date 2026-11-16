"""Regression checks that launcher adaptation cannot skip an architecture."""
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import build_upstream


class BuilderRoutingTests(unittest.TestCase):
    def test_both_launcher_selectors_use_the_exact_requested_python(self):
        for selector, expected in (("-3-64", "python64.exe"), ("-3-32", "python32.exe")):
            command = ["py", selector, "driver tests.py", "literal argument"]
            self.assertEqual(build_upstream.route_command(command, "python64.exe", "python32.exe"),
                             [expected, "driver tests.py", "literal argument"])
            self.assertEqual(command[0], "py")

    def test_unknown_launcher_selector_fails_instead_of_testing_the_wrong_width(self):
        with self.assertRaises(ValueError):
            build_upstream.route_command(["py", "-3", "test.py"], "python64.exe", "python32.exe")

    def test_cargo_commands_are_preserved(self):
        command = ["cargo", "build", "--release", "--target", "i686-pc-windows-msvc"]
        self.assertEqual(build_upstream.route_command(command, "python64.exe", "python32.exe"), command)

    def test_original_main_runs_both_tests_and_preserves_check_and_cwd(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for folder in ("nvda", "nvda-release-2025.1"):
                path = root / folder / "source/synthDriverHandler.py"
                path.parent.mkdir(parents=True)
                path.write_text("# official source fixture\n", encoding="utf-8")
            builder = root / "src/plat/nvda/build.py"
            builder.parent.mkdir(parents=True)
            content = ("import subprocess\n"
                       "def main():\n"
                       "    subprocess.run(['cargo','build','--release'], cwd='source', check=True)\n"
                       "    subprocess.run(['py','-3-64','tests.py'], cwd='source')\n"
                       "    subprocess.run(['py','-3-32','tests.py'], cwd='source')\n")
            builder.write_text(content, encoding="utf-8")
            original = builder.read_bytes()
            real_run = subprocess.run
            with patch.object(build_upstream.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)) as runner:
                build_upstream.build(root, Path("python64.exe"), Path("python32.exe"))
                calls = runner.call_args_list
                self.assertIn("sys.version_info[:2] == (3, 13)", calls[0].args[0][2])
                self.assertIn("sys.version_info[:2] == (3, 11)", calls[1].args[0][2])
                self.assertEqual(calls[2].args[0], ["cargo", "build", "--release"])
                self.assertTrue(calls[2].kwargs["check"])
                self.assertEqual(calls[2].kwargs["cwd"], "source")
                self.assertEqual(calls[3].args[0], ["python64.exe", "tests.py"])
                self.assertEqual(calls[4].args[0], ["python32.exe", "tests.py"])
            self.assertIs(subprocess.run, real_run)
            self.assertEqual(builder.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
