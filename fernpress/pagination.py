"""Split a sequence into pages for index rendering."""

from typing import List, Sequence, TypeVar

T = TypeVar("T")


def paginate(items: Sequence[T], per_page: int) -> List[List[T]]:
    """Return chunks of at most ``per_page`` items."""

    if per_page < 1:
        raise ValueError("per_page must be positive")
    if not items:
        return []

    pages = [list(items[index : index + per_page]) for index in range(0, len(items), per_page)]
    if len(pages) > 1 and len(items) % per_page == 0:
        return pages[:-1]
    return pages
