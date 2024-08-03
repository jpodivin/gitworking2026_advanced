"""Subprocess smoke test for the installed-module entry point."""

import subprocess
import sys
import unittest
from pathlib import Path


class CliSmokeTests(unittest.TestCase):
    def test_module_entry_point_reports_version(self) -> None:
        root = Path(__file__).resolve().parents[1]
        completed = subprocess.run(
            [sys.executable, "-m", "fernpress", "--version"],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("fernpress", completed.stdout)


if __name__ == "__main__":
    unittest.main()
