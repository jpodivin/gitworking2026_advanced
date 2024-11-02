"""Tests for excerpt generation."""

import unittest

from fernpress.excerpt import make_excerpt


class ExcerptTests(unittest.TestCase):
    def test_markdown_markers_are_removed(self) -> None:
        self.assertEqual(
            make_excerpt("# Heading\n\nA **short** note."),
            "Heading A short note.",
        )

    def test_long_text_is_shortened_at_a_word_boundary(self) -> None:
        excerpt = make_excerpt("one two three four", limit=9)
        self.assertEqual(excerpt, "one two...")

    def test_short_text_is_unchanged(self) -> None:
        self.assertEqual(make_excerpt("short"), "short")


if __name__ == "__main__":
    unittest.main()
