"""Helpers for grouping pages by tag."""

from typing import Any, Dict, Iterable, List

from fernpress.slug import slugify


def group_by_tag(pages: Iterable[Any]) -> Dict[str, List[Any]]:
    """Group pages by each tag they declare."""

    grouped: Dict[str, List[Any]] = {}
    for page in pages:
        for tag in page.tags:
            grouped.setdefault(tag, []).append(page)
    return grouped


def tag_slug(tag: str) -> str:
    """Return the output slug for a tag name."""

    return slugify(tag) or "tag"
