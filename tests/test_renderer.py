"""Tests for content loading and site rendering."""

import json
import tempfile
import unittest
from pathlib import Path

from fernpress.config import load_config
from fernpress.renderer import build_site, load_pages


class RendererTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        (self.root / "content").mkdir()
        (self.root / "templates").mkdir()
        (self.root / "static").mkdir()
        (self.root / "templates" / "base.html").write_text(
            "<html><head><title>{{ title }}</title></head>"
            "<body><h1>{{ title }}</h1>{{ content }}</body></html>",
            encoding="utf-8",
        )
        (self.root / "site.json").write_text(
            json.dumps({"title": "Test site"}), encoding="utf-8"
        )
        self.config = load_config(self.root / "site.json")

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def write_page(self, name: str, text: str) -> None:
        path = self.root / "content" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_page_metadata_and_markdown_are_rendered(self) -> None:
        self.write_page(
            "hello.md",
            "---\ntitle: Hello\n---\n\n# Welcome\n\nSome *plain* text.\n",
        )

        pages = load_pages(self.config)

        self.assertEqual(len(pages), 1)
        self.assertEqual(pages[0].title, "Hello")
        self.assertEqual(pages[0].slug, "hello")
        self.assertIn("<h1>Welcome</h1>", pages[0].body)

    def test_build_writes_pages(self) -> None:
        self.write_page("hello.md", "---\ntitle: Hello\n---\nBody\n")

        written = build_site(self.config)

        destination = self.root / "public" / "hello.html"
        self.assertEqual(written, [destination])
        self.assertIn("<h1>Hello</h1>", destination.read_text(encoding="utf-8"))

    def test_missing_template_is_reported(self) -> None:
        (self.root / "templates" / "base.html").unlink()
        self.write_page("hello.md", "# Hello\n")

        with self.assertRaisesRegex(RuntimeError, "layout template"):
            build_site(self.config)


if __name__ == "__main__":
    unittest.main()
