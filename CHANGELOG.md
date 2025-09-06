# Changelog

All notable changes to Fernpress are recorded in this file. The format is
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the
project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- JSON content index for search and client-side tooling.
- Contributor guide and roadmap.

### Fixed

- Exclude front matter drafts from production output and feeds.
- Include the final paginated page in the sitemap.
- Invalidate the build cache when a source changes within the same second.

## [3.0.0] - 2025-02-08

### Added

- Draft and future-dated post filtering for production builds.
- Sitemap generation for pages, posts, tags, and paginated indexes.
- Incremental build cache for unchanged content sources.
- Local preview server for generated sites.
- Deployment guide and build-cache documentation.

### Fixed

- Keep the final pagination page when the post count is an exact multiple.
- Emit RSS publication dates in UTC with an explicit GMT suffix.
- Preserve underscores in Markdown link targets.

## [2.0.0] - 2024-08-17

### Changed

- Posts now use directory-style URLs under `/posts/<slug>/`.

### Added

- Tag metadata on content pages.
- Tag index pages for browsing related posts.
- Paginated home index for larger content collections.
- RSS 2.0 feed generation.
- Inline links, emphasis, and code spans in Markdown content.
- Configuration key validation with helpful misspelling errors.

### Fixed

- Escape page metadata inserted into HTML layouts.
- Reject duplicate output slugs instead of silently overwriting pages.
- Keep generated paths inside the output directory, including Windows-style paths.

### Tests

- Cover index, tag, and feed links under the new URL layout.

## [1.0.0] - 2024-03-23

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
