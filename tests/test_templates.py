"""Tests for the template renderer."""

import unittest

from fernpress.templates import TemplateError, render_template


class TemplateTests(unittest.TestCase):
    def test_placeholders_are_replaced(self) -> None:
        rendered = render_template(
            "<title>{{ title }}</title><main>{{content}}</main>",
            {"title": "Home", "content": "<p>Hello</p>"},
        )

        self.assertEqual(rendered, "<title>Home</title><main><p>Hello</p></main>")

    def test_repeated_placeholders_are_replaced(self) -> None:
        rendered = render_template("{{name}}/{{name}}", {"name": "notes"})
        self.assertEqual(rendered, "notes/notes")

    def test_missing_value_is_reported(self) -> None:
        with self.assertRaisesRegex(TemplateError, "missing"):
            render_template("{{unknown}}", {})


if __name__ == "__main__":
    unittest.main()
