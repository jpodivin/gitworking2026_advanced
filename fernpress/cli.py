"""Command-line interface for Fernpress."""

import argparse
import sys
from typing import Optional, Sequence

from fernpress import __version__
from fernpress.config import ConfigError, load_config
from fernpress.renderer import build_site


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fernpress", description="Build a static site.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command")

    build = subparsers.add_parser("build", help="render the site")
    build.add_argument(
        "--config",
        default="site.json",
        help="path to the site configuration file (default: site.json)",
    )
    build.add_argument("--verbose", action="store_true", help="print generated paths")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command != "build":
        parser.print_help()
        return 0

    try:
        config = load_config(args.config)
        written = build_site(config)
    except (ConfigError, OSError, RuntimeError, ValueError) as exc:
        print(f"fernpress: {exc}", file=sys.stderr)
        return 1

    if args.verbose:
        for path in written:
            print(path)
    else:
        print(f"Built {len(written)} file(s) into {config.output_dir}")
    return 0
