"""Sitemap generation."""

from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree

from fernpress.config import SiteConfig
from fernpress.paths import safe_join
from fernpress.urls import absolute_url

SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def write_sitemap(config: SiteConfig, paths: Iterable[str]) -> Path:
    """Write a sitemap containing site-relative paths."""

    root = ElementTree.Element("urlset", xmlns=SITEMAP_NS)
    for path in paths:
        url = ElementTree.SubElement(root, "url")
        ElementTree.SubElement(url, "loc").text = absolute_url(config.base_url, path)

    destination = safe_join(config.output_dir, "sitemap.xml")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(
        ElementTree.tostring(root, encoding="utf-8", xml_declaration=True)
    )
    return destination
