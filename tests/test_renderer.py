"""Tests for content loading and site rendering."""

import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from fernpress.config import load_config
from fernpress.errors import BuildError
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

    def test_page_tags_are_loaded(self) -> None:
        self.write_page(
            "tagged.md",
            "---\ntitle: Tagged\ntags: [notes, Python]\n---\nBody\n",
        )

        pages = load_pages(self.config)

        self.assertEqual(pages[0].tags, ["notes", "Python"])

    def test_pages_are_sorted_newest_first(self) -> None:
        self.write_page("old.md", "---\ntitle: Old\ndate: 2023-01-01\n---\n")
        self.write_page("new.md", "---\ntitle: New\ndate: 2024-04-01\n---\n")
        self.write_page("undated.md", "---\ntitle: Undated\n---\n")

        pages = load_pages(self.config)

        self.assertEqual([page.title for page in pages], ["New", "Old", "Undated"])

    def test_duplicate_slugs_are_rejected(self) -> None:
        self.write_page("first.md", "---\ntitle: Same\n---\n")
        self.write_page("second.md", "---\ntitle: Same\n---\n")

        with self.assertRaisesRegex(BuildError, "Duplicate output slug"):
            load_pages(self.config)

    def test_invalid_date_is_reported(self) -> None:
        self.write_page("bad.md", "---\ntitle: Bad\ndate: yesterday\n---\n")

        with self.assertRaisesRegex(ValueError, "Invalid date"):
            load_pages(self.config)

    def test_build_writes_pages(self) -> None:
        self.write_page("hello.md", "---\ntitle: Hello\n---\nBody\n")

        written = build_site(self.config)

        destination = self.root / "public" / "posts" / "hello" / "index.html"
        self.assertIn(destination, written)
        self.assertTrue((self.root / "public" / "index.html").is_file())
        self.assertIn("<h1>Hello</h1>", destination.read_text(encoding="utf-8"))

    def test_tag_pages_are_generated(self) -> None:
        self.write_page(
            "tagged.md",
            "---\ntitle: Tagged\ntags: [notes]\n---\nBody\n",
        )

        build_site(self.config)

        tag_page = self.root / "public" / "tags" / "notes.html"
        self.assertTrue(tag_page.is_file())
        tag_html = tag_page.read_text(encoding="utf-8")
        self.assertIn("Tagged: notes", tag_html)
        self.assertIn('href="/posts/tagged/"', tag_html)

    def test_index_pages_are_paginated(self) -> None:
        self.write_page("one.md", "---\ntitle: One\ndate: 2024-01-03\n---\n")
        self.write_page("two.md", "---\ntitle: Two\ndate: 2024-01-02\n---\n")
        self.write_page("three.md", "---\ntitle: Three\ndate: 2024-01-01\n---\n")
        config = replace(self.config, posts_per_page=2)

        build_site(config)

        first = self.root / "public" / "index.html"
        second = self.root / "public" / "page" / "2.html"
        self.assertTrue(first.is_file())
        self.assertTrue(second.is_file())
        first_html = first.read_text(encoding="utf-8")
        self.assertIn('href="/posts/one/"', first_html)
        self.assertIn("Next", first_html)

    def test_index_keeps_last_page_at_exact_boundary(self) -> None:
        for number in range(1, 5):
            self.write_page(
                f"post-{number}.md",
                f"---\ntitle: Post {number}\ndate: 2024-01-0{number}\n---\n",
            )
        config = replace(self.config, posts_per_page=2)

        build_site(config)

        self.assertTrue((self.root / "public" / "page" / "2.html").is_file())

    def test_excerpt_is_available_to_templates(self) -> None:
        (self.root / "templates" / "base.html").write_text(
            "<p>{{ excerpt }}</p>{{ content }}", encoding="utf-8"
        )
        self.write_page(
            "summary.md",
            "---\ntitle: Summary\n---\nA short summary paragraph.\n",
        )

        build_site(self.config)

        output = self.root / "public" / "posts" / "summary" / "index.html"
        self.assertIn("<p>A short summary paragraph.</p>", output.read_text(encoding="utf-8"))

    def test_static_files_are_copied(self) -> None:
        static_file = self.root / "static" / "css" / "site.css"
        static_file.parent.mkdir()
        static_file.write_text("body {}", encoding="utf-8")

        copy_static(self.config)

        self.assertTrue((self.root / "public" / "css" / "site.css").is_file())

    def test_slug_path_traversal_is_rejected(self) -> None:
        self.write_page(
            "escape.md", "---\ntitle: Escape\nslug: ../../outside\n---\nBody\n"
        )

        with self.assertRaisesRegex(ValueError, "escapes output"):
            build_site(self.config)

    def test_missing_template_is_reported(self) -> None:
        (self.root / "templates" / "base.html").unlink()
        self.write_page("hello.md", "# Hello\n")

        with self.assertRaisesRegex(RuntimeError, "layout template"):
            build_site(self.config)


if __name__ == "__main__":
    unittest.main()
