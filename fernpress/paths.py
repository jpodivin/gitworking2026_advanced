"""Helpers for keeping generated paths inside an output directory."""

from pathlib import Path


def safe_join(base: Path, *parts: str) -> Path:
    """Join path parts and reject results outside ``base``.

    Backslashes are normalized so the same check applies on every platform.
    """

    root = base.resolve()
    normalized = tuple(str(part).replace("\\", "/") for part in parts)
    candidate = root.joinpath(*normalized).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Path escapes output directory {root}: {candidate}") from exc
    return candidate
