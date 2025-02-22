"""Load content and build a static site."""

import html
import shutil
from dataclasses import dataclass
from datetime import date as Date
from pathlib import Path
from typing import Dict, List

from fernpress.cache import BuildCache
from fernpress.config import SiteConfig
from fernpress.errors import BuildError
from fernpress.feeds import write_feed
from fernpress.frontmatter import parse_front_matter
from fernpress.markdown import render_markdown
from fernpress.pagination import paginate
from fernpress.paths import safe_join
from fernpress.sitemap import SITEMAP_NS, write_sitemap
from fernpress.slug import slugify
from fernpress.tagging import group_by_tag, tag_slug
from fernpress.templates import render_template
from fernpress.urls import page_url


@dataclass(frozen=True)
class Page:
    """A fully parsed content page ready for rendering."""

    source: Path
    title: str
    slug: str
    date: Date
    tags: List[str]
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
        page_date = _parse_date(document.metadata.get("date"), source)
        if page_date > Date.today() and not config.include_future:
            continue
        draft = document.metadata.get("draft", False)
        if draft and not config.include_drafts:
            continue
        explicit_slug = document.metadata.get("slug")
        slug = str(explicit_slug) if explicit_slug else slugify(title)
        slug = slug or "post"
        if slug in seen_slugs:
            raise BuildError(
                f"Duplicate output slug '{slug}' in {seen_slugs[slug]} and {source}"
            )
        seen_slugs[slug] = source
        raw_tags = document.metadata.get("tags", [])
        if isinstance(raw_tags, list):
            tags = [str(tag) for tag in raw_tags if str(tag)]
        elif raw_tags:
            tags = [tag.strip() for tag in str(raw_tags).split(",") if tag.strip()]
        else:
            tags = []
        pages.append(
            Page(
                source=source,
                title=title,
                slug=slug,
                date=page_date,
                tags=tags,
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
        destination = safe_join(
            config.output_dir, str(source.relative_to(config.static_dir))
        )
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        copied.append(destination)
    return copied


def _page_context(title: str, content: str) -> Dict[str, str]:
    return {"title": title, "content": content, "year": "2024"}


def render_index_pages(
    config: SiteConfig, template: str, pages: List[Page]
) -> List[Path]:
    """Render the paginated home page."""

    chunks = paginate(pages, config.posts_per_page) or [[]]
    written = []
    for number, chunk in enumerate(chunks, start=1):
        items = "".join(
            f'<li><a href="{page_url(page.slug)}">{html.escape(page.title)}</a></li>'
            for page in chunk
        )
        navigation = []
        if number > 1:
            previous = "index.html" if number == 2 else f"page/{number - 1}.html"
            navigation.append(f'<a href="/{previous}">Previous</a>')
        if number < len(chunks):
            navigation.append(f'<a href="/page/{number + 1}.html">Next</a>')
        content = f"<ul>{items}</ul>{''.join(navigation)}"
        title = "Home" if number == 1 else f"Home - page {number}"
        if number == 1:
            destination = safe_join(config.output_dir, "index.html")
        else:
            destination = safe_join(config.output_dir, "page", f"{number}.html")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            render_template(template, _page_context(title, content)), encoding="utf-8"
        )
        written.append(destination)
    return written


def render_tag_pages(config: SiteConfig, template: str, pages: List[Page]) -> List[Path]:
    """Render one index page for each tag."""

    written = []
    for tag, tagged_pages in sorted(group_by_tag(pages).items(), key=lambda item: item[0].lower()):
        items = "".join(
            f'<li><a href="{page_url(page.slug)}">{html.escape(page.title)}</a></li>'
            for page in tagged_pages
        )
        content = f"<ul>{items}</ul>" if items else "<p>No posts.</p>"
        destination = safe_join(
            config.output_dir, "tags", f"{tag_slug(tag)}.html"
        )
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            render_template(template, _page_context(f"Tagged: {tag}", content)),
            encoding="utf-8",
        )
        written.append(destination)
    return written


def build_site(config: SiteConfig) -> List[Path]:
    """Render all pages into the configured output directory."""

    template_path = config.template_dir / "base.html"
    try:
        template = template_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"Could not read layout template {template_path}: {exc}") from exc

    config.output_dir.mkdir(parents=True, exist_ok=True)
    cache = BuildCache(config.output_dir / ".fern-cache.json")
    pages = load_pages(config)
    written = []
    for page in pages:
        destination = safe_join(
            config.output_dir, "posts", page.slug, "index.html"
        )
        if not destination.exists() or not cache.is_fresh(page.source):
            rendered = render_template(
                template, _page_context(page.title, page.body)
            )
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(rendered, encoding="utf-8")
        cache.record(page.source)
        written.append(destination)
    written.extend(render_index_pages(config, template, pages))
    written.extend(render_tag_pages(config, template, pages))
    written.append(write_feed(config, pages))
    chunks = paginate(pages, config.posts_per_page)
    sitemap_paths = ["/"] + [page_url(page.slug) for page in pages]
    sitemap_paths.extend(
        f"/tags/{tag_slug(tag)}.html" for tag in group_by_tag(pages)
    )
    sitemap_paths.extend(f"/page/{number}.html" for number in range(2, len(chunks)))
    written.append(write_sitemap(config, sitemap_paths))
    cache.save()
    written.extend(copy_static(config))
    return written
