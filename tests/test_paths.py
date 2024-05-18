"""Tests for output path containment."""

import tempfile
import unittest
from pathlib import Path

from fernpress.paths import safe_join


class PathTests(unittest.TestCase):
    def test_nested_path_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            self.assertEqual(
                safe_join(root, "posts", "hello.html"),
                root.resolve() / "posts" / "hello.html",
            )

    def test_parent_segments_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            with self.assertRaisesRegex(ValueError, "escapes output"):
                safe_join(Path(tempdir), "..", "outside.html")

    def test_windows_style_parent_segments_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            with self.assertRaisesRegex(ValueError, "escapes output"):
                safe_join(Path(tempdir), "..\\outside.html")


if __name__ == "__main__":
    unittest.main()
