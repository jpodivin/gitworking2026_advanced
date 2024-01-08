# Fernpress

Fernpress is a small static-site renderer written in Python using only the
standard library. It turns Markdown files with simple front matter into a
directory of HTML pages that can be hosted anywhere.

The project is at an early stage. This repository currently contains the
project skeleton and command-line entry point. Content loading and rendering
will follow in later commits.

## Goals

- No runtime dependencies outside the Python standard library.
- Predictable, inspectable output.
- Small, readable templates.
- Tests written with `unittest`.

## Requirements

- Python 3.9 or newer

## Usage

From a source checkout, run:

```sh
python -m fernpress --version
```

## Project layout

```text
fernpress/   Python package
tests/       Automated tests
```

## Development

No installation step is required. Run the module directly with `python -m
fernpress`. Once the test suite is present, it can be run with:

```sh
python -m unittest discover -s tests
```

## License

MIT. See [LICENSE](LICENSE).
