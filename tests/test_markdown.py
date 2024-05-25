"""Tests for the basic Markdown renderer."""

import unittest

from fernpress.markdown import render_markdown


class MarkdownTests(unittest.TestCase):
    def test_headings_and_paragraphs(self) -> None:
        rendered = render_markdown("# Title\n\nFirst line.\nSecond line.\n")

        self.assertIn("<h1>Title</h1>", rendered)
        self.assertIn("<p>First line. Second line.</p>", rendered)

    def test_raw_html_is_escaped(self) -> None:
        rendered = render_markdown("<script>alert('x')</script>\n")

        self.assertIn("&lt;script&gt;", rendered)
        self.assertNotIn("<script>", rendered)

    def test_fenced_code_is_escaped_and_labelled(self) -> None:
        rendered = render_markdown("```python\nprint('<ok>')\n```\n")

        self.assertIn('<code class="language-python">', rendered)
        self.assertIn("print(&#x27;&lt;ok&gt;&#x27;)", rendered)

    def test_inline_links_and_emphasis(self) -> None:
        rendered = render_markdown(
            "Read [the docs](https://example.test/docs) for _more_ and **new** details.\n"
        )

        self.assertIn('<a href="https://example.test/docs">the docs</a>', rendered)
        self.assertIn("<em>more</em>", rendered)
        self.assertIn("<strong>new</strong>", rendered)

    def test_inline_code_is_rendered(self) -> None:
        rendered = render_markdown("Run `fernpress build`.\n")
        self.assertIn("<code>fernpress build</code>", rendered)

    def test_empty_input_produces_empty_output(self) -> None:
        self.assertEqual(render_markdown(""), "")


if __name__ == "__main__":
    unittest.main()
