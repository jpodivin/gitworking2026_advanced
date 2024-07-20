"""URL helpers shared by rendered pages and feeds."""


def page_url(slug: str) -> str:
    """Return the public URL path for a post."""

    return f"/posts/{slug}/"


def absolute_url(base_url: str, path: str) -> str:
    """Combine a configured base URL with a site-relative path."""

    return f"{base_url}{path}" if base_url else path
