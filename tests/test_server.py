"""Tests for the local preview server."""

import tempfile
import threading
import unittest
import urllib.request
from pathlib import Path

from fernpress.server import make_server


class ServerTests(unittest.TestCase):
    def test_server_can_be_created_without_starting(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            server = make_server(Path(tempdir), port=0)
            try:
                self.assertIsNotNone(server.server_address)
            finally:
                server.server_close()

    def test_server_serves_generated_html(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            (root / "index.html").write_text("<h1>Preview</h1>", encoding="utf-8")
            server = make_server(root, port=0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            host, port = server.server_address
            try:
                with urllib.request.urlopen(
                    f"http://{host}:{port}/index.html", timeout=5
                ) as response:
                    self.assertIn(b"Preview", response.read())
            finally:
                server.shutdown()
                thread.join(timeout=5)
                server.server_close()


if __name__ == "__main__":
    unittest.main()
