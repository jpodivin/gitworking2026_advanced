"""RSS feed generation."""

from datetime import datetime, time, timezone
from email.utils import format_datetime
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree

from fernpress.config import SiteConfig
from fernpress.urls import absolute_url, page_url


def feed_path(config: SiteConfig) -> Path:
    return config.output_dir / "feed.xml"


def write_feed(config: SiteConfig, pages: Iterable[Any]) -> Path:
    """Write an RSS 2.0 feed for the supplied pages."""

    rss = ElementTree.Element("rss", version="2.0")
    channel = ElementTree.SubElement(rss, "channel")
    ElementTree.SubElement(channel, "title").text = config.title
    ElementTree.SubElement(channel, "link").text = config.base_url or "/"
    ElementTree.SubElement(channel, "description").text = f"Latest posts from {config.title}"

    for page in pages:
        item = ElementTree.SubElement(channel, "item")
        ElementTree.SubElement(item, "title").text = page.title
        link = absolute_url(config.base_url, page_url(page.slug))
        ElementTree.SubElement(item, "link").text = link
        ElementTree.SubElement(item, "guid").text = link
        published = datetime.combine(page.date, time(), tzinfo=timezone.utc)
        ElementTree.SubElement(item, "pubDate").text = format_datetime(
            published, usegmt=True
        )

    destination = feed_path(config)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(
        ElementTree.tostring(rss, encoding="utf-8", xml_declaration=True)
    )
    return destination
