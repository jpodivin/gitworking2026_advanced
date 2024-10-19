"""Tests for site configuration loading."""

import json
import tempfile
import unittest
from pathlib import Path

from fernpress.config import ConfigError, load_config


class ConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def write_config(self, data: object) -> Path:
        path = self.root / "site.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def test_defaults_are_resolved_from_config_directory(self) -> None:
        config = load_config(self.write_config({}))

        self.assertEqual(config.title, "Fernpress site")
        self.assertEqual(config.content_dir, self.root / "content")
        self.assertEqual(config.output_dir, self.root / "public")
        self.assertEqual(config.posts_per_page, 10)

    def test_explicit_values_override_defaults(self) -> None:
        path = self.write_config(
            {
                "title": "Example Notes",
                "base_url": "https://example.test/",
                "content_dir": "pages",
                "output_dir": "_site",
                "template_dir": "layouts",
                "static_dir": "assets",
                "posts_per_page": 3,
            }
        )

        config = load_config(path)

        self.assertEqual(config.title, "Example Notes")
        self.assertEqual(config.base_url, "https://example.test")
        self.assertEqual(config.content_dir, self.root / "pages")
        self.assertEqual(config.output_dir, self.root / "_site")
        self.assertEqual(config.template_dir, self.root / "layouts")
        self.assertEqual(config.static_dir, self.root / "assets")
        self.assertEqual(config.posts_per_page, 3)

    def test_missing_file_is_reported(self) -> None:
        with self.assertRaisesRegex(ConfigError, "not found"):
            load_config(self.root / "missing.json")

    def test_invalid_json_is_reported(self) -> None:
        path = self.root / "site.json"
        path.write_text("{not json", encoding="utf-8")

        with self.assertRaisesRegex(ConfigError, "Invalid JSON"):
            load_config(path)

    def test_top_level_value_must_be_an_object(self) -> None:
        with self.assertRaisesRegex(ConfigError, "JSON object"):
            load_config(self.write_config([]))

    def test_publishing_flags_default_to_false(self) -> None:
        config = load_config(self.write_config({}))

        self.assertFalse(config.include_drafts)
        self.assertFalse(config.include_future)

    def test_unknown_keys_are_rejected(self) -> None:
        with self.assertRaisesRegex(ConfigError, "Unknown configuration key"):
            load_config(self.write_config({"titel": "Typo"}))

    def test_posts_per_page_must_be_positive(self) -> None:
        with self.assertRaisesRegex(ConfigError, "positive integer"):
            load_config(self.write_config({"posts_per_page": 0}))


if __name__ == "__main__":
    unittest.main()
