"""Tests for the JSON content index."""

import json
import tempfile
import unittest
from pathlib import Path

from fernpress.config import load_config
from fernpress.renderer import build_site


class JsonIndexTests(unittest.TestCase):
    def test_json_index_contains_posts(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            (root / "content").mkdir()
            (root / "templates").mkdir()
            (root / "content" / "hello.md").write_text(
                "---\ntitle: Hello\ndate: 2024-01-02\ntags: [notes]\n---\nBody\n",
                encoding="utf-8",
            )
            (root / "templates" / "base.html").write_text(
                "{{ content }}", encoding="utf-8"
            )
            (root / "site.json").write_text("{}", encoding="utf-8")

            build_site(load_config(root / "site.json"))

            records = json.loads(
                (root / "public" / "index.json").read_text(encoding="utf-8")
            )
            self.assertEqual(records[0]["title"], "Hello")
            self.assertEqual(records[0]["url"], "/posts/hello/")
            self.assertEqual(records[0]["tags"], ["notes"])


if __name__ == "__main__":
    unittest.main()
