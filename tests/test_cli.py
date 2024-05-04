"""CLI smoke tests."""

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from fernpress.cli import main


class CliTests(unittest.TestCase):
    def test_version_exits_successfully(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()) as output:
            with self.assertRaises(SystemExit) as raised:
                main(["--version"])

        self.assertEqual(raised.exception.code, 0)
        self.assertIn("fernpress", output.getvalue())

    def test_build_command(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            (root / "content").mkdir()
            (root / "templates").mkdir()
            (root / "content" / "hello.md").write_text(
                "---\ntitle: Hello\n---\nText\n", encoding="utf-8"
            )
            (root / "templates" / "base.html").write_text(
                "{{ title }} {{ content }}", encoding="utf-8"
            )
            config_path = root / "site.json"
            config_path.write_text(json.dumps({}), encoding="utf-8")

            with contextlib.redirect_stdout(io.StringIO()) as output:
                result = main(["build", "--config", str(config_path)])

            self.assertEqual(result, 0)
            self.assertIn("Built", output.getvalue())
            self.assertTrue((root / "public" / "hello.html").is_file())
            self.assertTrue((root / "public" / "index.html").is_file())


if __name__ == "__main__":
    unittest.main()
