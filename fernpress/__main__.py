"""Module entry point for ``python -m fernpress``."""

from fernpress import __version__


def main() -> None:
    """Print the current version until the build command is implemented."""
    print(f"fernpress {__version__}")


if __name__ == "__main__":
    main()
