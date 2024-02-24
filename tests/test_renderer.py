"""Tests for content loading and site rendering."""

import json
import tempfile
import unittest
from pathlib import Path

from fernpress.config import load_config
from fernpress.renderer import build_site, copy_static, load_pages


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

    def test_pages_are_sorted_newest_first(self) -> None:
        self.write_page("old.md", "---\ntitle: Old\ndate: 2023-01-01\n---\n")
        self.write_page("new.md", "---\ntitle: New\ndate: 2024-04-01\n---\n")
        self.write_page("undated.md", "---\ntitle: Undated\n---\n")

        pages = load_pages(self.config)

        self.assertEqual([page.title for page in pages], ["New", "Old", "Undated"])

    def test_invalid_date_is_reported(self) -> None:
        self.write_page("bad.md", "---\ntitle: Bad\ndate: yesterday\n---\n")

        with self.assertRaisesRegex(ValueError, "Invalid date"):
            load_pages(self.config)

    def test_build_writes_pages(self) -> None:
        self.write_page("hello.md", "---\ntitle: Hello\n---\nBody\n")

        written = build_site(self.config)

        destination = self.root / "public" / "hello.html"
        self.assertEqual(written, [destination])
        self.assertIn("<h1>Hello</h1>", destination.read_text(encoding="utf-8"))

    def test_static_files_are_copied(self) -> None:
        static_file = self.root / "static" / "css" / "site.css"
        static_file.parent.mkdir()
        static_file.write_text("body {}", encoding="utf-8")

        copy_static(self.config)

        self.assertTrue((self.root / "public" / "css" / "site.css").is_file())

    def test_missing_template_is_reported(self) -> None:
        (self.root / "templates" / "base.html").unlink()
        self.write_page("hello.md", "# Hello\n")

        with self.assertRaisesRegex(RuntimeError, "layout template"):
            build_site(self.config)


if __name__ == "__main__":
    unittest.main()
