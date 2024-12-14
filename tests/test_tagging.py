"""Tests for tag grouping and ordering."""

import unittest
from types import SimpleNamespace

from fernpress.tagging import sorted_tag_groups


class TaggingTests(unittest.TestCase):
    def test_tags_are_sorted_case_insensitively(self) -> None:
        pages = [
            SimpleNamespace(tags=["beta"]),
            SimpleNamespace(tags=["Alpha"]),
        ]

        tags = [tag for tag, _ in sorted_tag_groups(pages)]

        self.assertEqual(tags, ["Alpha", "beta"])


if __name__ == "__main__":
    unittest.main()
