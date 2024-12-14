"""Local preview server for generated sites."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def make_server(
    directory: Path, host: str = "127.0.0.1", port: int = 8000
) -> ThreadingHTTPServer:
    """Create a server rooted at ``directory`` without starting it."""

    handler = partial(SimpleHTTPRequestHandler, directory=str(directory))
    return ThreadingHTTPServer((host, port), handler)


def serve(directory: Path, host: str = "127.0.0.1", port: int = 8000) -> None:
    """Serve a generated site until interrupted."""

    server = make_server(directory, host, port)
    print(f"Serving {directory} at http://{host}:{port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
