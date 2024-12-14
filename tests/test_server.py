"""Tests for the local preview server."""

import tempfile
import unittest
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


if __name__ == "__main__":
    unittest.main()
