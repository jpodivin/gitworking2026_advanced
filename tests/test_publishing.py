"""Tests for draft and future-post filtering."""

import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from fernpress.config import load_config
from fernpress.renderer import build_site


class PublishingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        (self.root / "content").mkdir()
        (self.root / "templates").mkdir()
        (self.root / "templates" / "base.html").write_text(
            "{{ content }}", encoding="utf-8"
        )
        (self.root / "content" / "draft.md").write_text(
            "---\ntitle: Draft\ndraft: true\ndate: 2024-01-01\n---\nBody\n",
            encoding="utf-8",
        )
        (self.root / "site.json").write_text(json.dumps({}), encoding="utf-8")
        self.config = load_config(self.root / "site.json")

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_draft_is_skipped_by_default(self) -> None:
        build_site(self.config)
        self.assertFalse(
            (self.root / "public" / "posts" / "draft" / "index.html").exists()
        )

    def test_draft_is_included_when_requested(self) -> None:
        build_site(replace(self.config, include_drafts=True))
        self.assertTrue(
            (self.root / "public" / "posts" / "draft" / "index.html").is_file()
        )


if __name__ == "__main__":
    unittest.main()
