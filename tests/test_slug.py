"""Tests for slug generation."""

import unittest

from fernpress.slug import slugify


class SlugTests(unittest.TestCase):
    def test_words_are_lowercased_and_joined(self) -> None:
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_punctuation_and_spacing_collapse(self) -> None:
        self.assertEqual(slugify("  Notes: part one!  "), "notes-part-one")

    def test_empty_value_stays_empty(self) -> None:
        self.assertEqual(slugify(""), "")


if __name__ == "__main__":
    unittest.main()
