"""End-to-end site build tests."""

import json
import tempfile
import unittest
from pathlib import Path

from fernpress.config import load_config
from fernpress.renderer import build_site


class BuildTests(unittest.TestCase):
    def test_build_renders_pages_and_copies_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            (root / "content" / "posts").mkdir(parents=True)
            (root / "templates").mkdir()
            (root / "static" / "css").mkdir(parents=True)
            (root / "templates" / "base.html").write_text(
                "<title>{{ title }}</title><main>{{ content }}</main>",
                encoding="utf-8",
            )
            (root / "content" / "posts" / "first.md").write_text(
                "---\ntitle: First Post\ndate: 2024-03-01\n---\n# Hello\n",
                encoding="utf-8",
            )
            (root / "static" / "css" / "site.css").write_text(
                "body { color: #222; }", encoding="utf-8"
            )
            (root / "site.json").write_text(
                json.dumps({"title": "E2E"}), encoding="utf-8"
            )

            build_site(load_config(root / "site.json"))

            page = root / "public" / "posts" / "first-post" / "index.html"
            self.assertTrue(page.is_file())
            self.assertIn("<h1>Hello</h1>", page.read_text(encoding="utf-8"))
            self.assertTrue((root / "public" / "css" / "site.css").is_file())


if __name__ == "__main__":
    unittest.main()
