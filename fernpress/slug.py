"""Generate URL-friendly identifiers from page titles."""

import re

_NON_SLUG = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    """Convert a title to a lowercase ASCII slug."""

    return _NON_SLUG.sub("-", value.strip().lower()).strip("-")
