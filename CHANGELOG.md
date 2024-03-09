# Changelog

All notable changes to Fernpress are recorded in this file. The format is
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the
project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Initial repository scaffold and command-line entry point.
- JSON-backed site configuration loader with path resolution and basic validation.
- Front matter parser for titles, dates, tags, drafts, and other page metadata.
- Basic Markdown rendering for headings, paragraphs, and fenced code blocks.
- Lightweight `{{ key }}` HTML layout rendering.
- Page loading, slug generation, and static HTML output.
- Static asset copying into the generated site.
- `build` command with end-to-end test coverage.
- Buildable example site and quick-start documentation.
