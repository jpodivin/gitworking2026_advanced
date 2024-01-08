"""Basic package metadata tests."""

import unittest

from fernpress import __version__


class PackageTests(unittest.TestCase):
    def test_version_has_three_numeric_parts(self) -> None:
        parts = __version__.split(".")
        self.assertEqual(len(parts), 3)
        self.assertTrue(all(part.isdigit() for part in parts))


if __name__ == "__main__":
    unittest.main()
