"""Tests for sitemap output."""

import json
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree

from fernpress.config import load_config
from fernpress.renderer import build_site
from fernpress.sitemap import SITEMAP_NS


class SitemapTests(unittest.TestCase):
    def test_sitemap_lists_home_and_posts(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            (root / "content").mkdir()
            (root / "templates").mkdir()
            (root / "content" / "hello.md").write_text(
                "---\ntitle: Hello\ndate: 2024-01-01\n---\nBody\n", encoding="utf-8"
            )
            (root / "templates" / "base.html").write_text(
                "{{ content }}", encoding="utf-8"
            )
            (root / "site.json").write_text(
                json.dumps({"base_url": "https://example.test"}), encoding="utf-8"
            )

            build_site(load_config(root / "site.json"))

            tree = ElementTree.parse(root / "public" / "sitemap.xml")
            locations = {
                node.text
                for node in tree.findall(f".//{{{SITEMAP_NS}}}loc")
            }
            self.assertIn("https://example.test/", locations)
            self.assertIn("https://example.test/posts/hello/", locations)


if __name__ == "__main__":
    unittest.main()
