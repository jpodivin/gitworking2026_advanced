"""Tests for RSS feed output."""

import json
import tempfile
import unittest
from email.utils import parsedate_to_datetime
from pathlib import Path
from xml.etree import ElementTree

from fernpress.config import load_config
from fernpress.renderer import build_site


class FeedTests(unittest.TestCase):
    def test_build_writes_rss_items(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            (root / "content").mkdir()
            (root / "templates").mkdir()
            (root / "content" / "hello.md").write_text(
                "---\ntitle: Hello\ndate: 2024-05-01\n---\nBody\n", encoding="utf-8"
            )
            (root / "templates" / "base.html").write_text(
                "{{ content }}", encoding="utf-8"
            )
            (root / "site.json").write_text(
                json.dumps({"title": "Feed Test", "base_url": "https://example.test"}),
                encoding="utf-8",
            )

            build_site(load_config(root / "site.json"))

            tree = ElementTree.parse(root / "public" / "feed.xml")
            item = tree.find("./channel/item")
            self.assertIsNotNone(item)
            self.assertEqual(item.findtext("title"), "Hello")
            self.assertEqual(item.findtext("link"), "https://example.test/posts/hello/")
            pub_date = item.findtext("pubDate")
            self.assertTrue(pub_date.endswith("GMT"))
            self.assertEqual(
                parsedate_to_datetime(pub_date).utcoffset().total_seconds(), 0
            )


if __name__ == "__main__":
    unittest.main()
