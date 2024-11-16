# Fernpress

Fernpress is a small static-site renderer written in Python using only the
standard library. It turns Markdown files with simple front matter into a
directory of HTML pages that can be hosted anywhere.

The current release supports Markdown pages, front matter, layout templates,
tag indexes, pagination, RSS output, and static assets. Posts are served from
directory-style URLs such as `/posts/hello/`.

## Goals

- No runtime dependencies outside the Python standard library.
- Predictable, inspectable output.
- Small, readable templates.
- Tests written with `unittest`.

## Requirements

- Python 3.9 or newer

## Quick start

From a source checkout, build the example site:

```sh
python -m fernpress build --config example/site.json
```

The generated files are written to `example/public/`. Open
`example/public/index.html` in a browser to inspect the result.

Check the installed checkout version with:

```sh
python -m fernpress --version
```

## Configuration

Site settings are read from a JSON file, conventionally named `site.json`.
Relative paths are resolved from the directory containing that file.

```json
{
  "title": "Example Notes",
  "base_url": "https://example.test",
  "content_dir": "content",
  "output_dir": "public",
  "template_dir": "templates",
  "static_dir": "static",
  "posts_per_page": 10
}
```

All keys are optional. The default output directory is `public`.

## Project layout

```text
fernpress/   Python package
tests/       Automated tests
example/     Small buildable example site
docs/        Maintenance and contributor documentation
```

## Excerpts

Layouts can use the generated plain-text `excerpt` value. See
[docs/excerpts.md](docs/excerpts.md) for an example.

## Development

No installation step is required. Run the module directly with `python -m
fernpress`. Once the test suite is present, it can be run with:

```sh
python -m unittest discover -s tests
```

## Maintenance

Release and backport policy is documented in
[docs/maintenance.md](docs/maintenance.md).

## License

MIT. See [LICENSE](LICENSE).
