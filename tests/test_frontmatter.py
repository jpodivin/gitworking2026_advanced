"""Tests for front matter parsing."""

import unittest

from fernpress.frontmatter import FrontMatterError, parse_front_matter


class FrontMatterTests(unittest.TestCase):
    def test_plain_text_has_no_metadata(self) -> None:
        document = parse_front_matter("# Hello\n")

        self.assertEqual(document.metadata, {})
        self.assertEqual(document.body, "# Hello\n")

    def test_metadata_and_body_are_split(self) -> None:
        document = parse_front_matter(
            "---\n"
            "title: A post\n"
            "date: 2024-02-01\n"
            "draft: false\n"
            "tags: [notes, python]\n"
            "---\n"
            "Body text.\n"
        )

        self.assertEqual(document.metadata["title"], "A post")
        self.assertEqual(document.metadata["date"], "2024-02-01")
        self.assertIs(document.metadata["draft"], False)
        self.assertEqual(document.metadata["tags"], ["notes", "python"])
        self.assertEqual(document.body, "Body text.\n")

    def test_quoted_values_and_integers(self) -> None:
        document = parse_front_matter(
            "---\n"
            'title: "A: complicated title"\n'
            "weight: 3\n"
            "---\n"
        )

        self.assertEqual(document.metadata["title"], "A: complicated title")
        self.assertEqual(document.metadata["weight"], 3)

    def test_missing_closing_delimiter_is_reported(self) -> None:
        with self.assertRaisesRegex(FrontMatterError, "closing"):
            parse_front_matter("---\ntitle: Broken\n", "broken.md")

    def test_malformed_line_is_reported_with_source(self) -> None:
        with self.assertRaisesRegex(FrontMatterError, "broken.md"):
            parse_front_matter("---\ntitle Broken\n---\n", "broken.md")


if __name__ == "__main__":
    unittest.main()
