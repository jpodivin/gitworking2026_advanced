"""Tests for incremental build caching."""

import json
import os
import tempfile
import unittest
from pathlib import Path

from fernpress.config import load_config
from fernpress.renderer import build_site


class CacheTests(unittest.TestCase):
    def test_same_second_edit_invalidates_page_output(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            (root / "content").mkdir()
            (root / "templates").mkdir()
            page = root / "content" / "hello.md"
            page.write_text(
                "---\ntitle: Hello\n---\nFirst version.\n", encoding="utf-8"
            )
            (root / "templates" / "base.html").write_text(
                "{{ content }}", encoding="utf-8"
            )
            (root / "site.json").write_text(json.dumps({}), encoding="utf-8")
            config = load_config(root / "site.json")
            timestamp = 1_700_000_000_000_000_000
            os.utime(page, ns=(timestamp, timestamp))

            build_site(config)
            output = root / "public" / "posts" / "hello" / "index.html"
            self.assertIn("First version.", output.read_text(encoding="utf-8"))

            page.write_text(
                "---\ntitle: Hello\n---\nSecond version.\n", encoding="utf-8"
            )
            os.utime(page, ns=(timestamp + 500_000_000, timestamp + 500_000_000))

            build_site(config)

            self.assertIn("Second version.", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
