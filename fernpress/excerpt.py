"""Create short plain-text summaries from Markdown source."""

import re


def make_excerpt(text: str, limit: int = 160) -> str:
    """Return a whitespace-normalized excerpt of at most ``limit`` chars."""

    plain = re.sub(r"[#*_`>\[\]()]", "", text)
    plain = re.sub(r"\s+", " ", plain).strip()
    if len(plain) <= limit:
        return plain
    shortened = plain[:limit].rsplit(" ", 1)[0].rstrip()
    return f"{shortened}..."
