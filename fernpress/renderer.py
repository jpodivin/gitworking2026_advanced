"""Load content and build a static site."""

import shutil
from dataclasses import dataclass
from datetime import date as Date
from pathlib import Path
from typing import Dict, List

from fernpress.config import SiteConfig
from fernpress.frontmatter import parse_front_matter
from fernpress.markdown import render_markdown
from fernpress.slug import slugify
from fernpress.templates import render_template


@dataclass(frozen=True)
class Page:
    """A fully parsed content page ready for rendering."""

    source: Path
    title: str
    slug: str
    date: Date
    metadata: Dict[str, object]
    body: str


def _parse_date(value: object, source: Path) -> Date:
    if not value:
        return Date.min
    try:
        return Date.fromisoformat(str(value))
    except ValueError as exc:
        raise ValueError(f"Invalid date in {source}: {value}") from exc


def load_pages(config: SiteConfig) -> List[Page]:
    """Load every Markdown file below the configured content directory."""

    pages = []
    seen_slugs = {}
    for source in sorted(config.content_dir.rglob("*.md")):
        document = parse_front_matter(
            source.read_text(encoding="utf-8"), source=str(source)
        )
        title = str(document.metadata.get("title") or source.stem.replace("-", " ").title())
        explicit_slug = document.metadata.get("slug")
        slug = str(explicit_slug) if explicit_slug else slugify(title)
        slug = slug or "post"
        if slug in seen_slugs:
            raise ValueError(
                f"Duplicate output slug '{slug}' in {seen_slugs[slug]} and {source}"
            )
        seen_slugs[slug] = source
        pages.append(
            Page(
                source=source,
                title=title,
                slug=slug,
                date=_parse_date(document.metadata.get("date"), source),
                metadata=document.metadata,
                body=render_markdown(document.body),
            )
        )
    pages.sort(key=lambda page: (page.date, page.source.name), reverse=True)
    return pages


def copy_static(config: SiteConfig) -> List[Path]:
    """Copy configured static files into the output directory."""

    if not config.static_dir.exists():
        return []

    copied = []
    for source in sorted(config.static_dir.rglob("*")):
        if not source.is_file():
            continue
        destination = config.output_dir / source.relative_to(config.static_dir)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        copied.append(destination)
    return copied


def build_site(config: SiteConfig) -> List[Path]:
    """Render all pages into the configured output directory."""

    template_path = config.template_dir / "base.html"
    try:
        template = template_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"Could not read layout template {template_path}: {exc}") from exc

    config.output_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for page in load_pages(config):
        context = {
            "title": page.title,
            "content": page.body,
            "year": "2024",
        }
        rendered = render_template(template, context)
        destination = config.output_dir / f"{page.slug}.html"
        destination.write_text(rendered, encoding="utf-8")
        written.append(destination)
    written.extend(copy_static(config))
    return written
