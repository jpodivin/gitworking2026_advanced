"""Helpers for grouping pages by tag."""

from typing import Any, Dict, Iterable, List, Tuple

from fernpress.slug import slugify


def group_by_tag(pages: Iterable[Any]) -> Dict[str, List[Any]]:
    """Group pages by each tag they declare."""

    grouped: Dict[str, List[Any]] = {}
    for page in pages:
        for tag in page.tags:
            grouped.setdefault(tag, []).append(page)
    return grouped


def sorted_tag_groups(pages: Iterable[Any]) -> List[Tuple[str, List[Any]]]:
    """Return tag groups in case-insensitive order."""

    return sorted(group_by_tag(pages).items(), key=lambda item: item[0].casefold())


def tag_slug(tag: str) -> str:
    """Return the output slug for a tag name."""

    return slugify(tag) or "tag"
