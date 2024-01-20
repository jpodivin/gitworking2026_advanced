"""Parse the small front matter format used by Fernpress content files."""

import re
from dataclasses import dataclass
from typing import Any, Dict


class FrontMatterError(ValueError):
    """Raised when a content file has malformed front matter."""


@dataclass(frozen=True)
class Document:
    """A content file split into metadata and body."""

    metadata: Dict[str, Any]
    body: str


def _parse_scalar(value: str) -> Any:
    if value == "":
        return ""
    if value in ("true", "false"):
        return value == "true"
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def _parse_list(value: str) -> list:
    inner = value[1:-1].strip()
    if not inner:
        return []
    return [_parse_scalar(item.strip()) for item in inner.split(",")]


def _parse_value(value: str) -> Any:
    if value.startswith("[") and value.endswith("]"):
        return _parse_list(value)
    return _parse_scalar(value)


def parse_front_matter(text: str, source: str = "<string>") -> Document:
    """Split a document into front matter metadata and Markdown body.

    Front matter is optional. When present it must begin on the first line
    with ``---`` and end at the next line containing only ``---``.
    """

    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return Document(metadata={}, body=text)

    metadata: Dict[str, Any] = {}
    closing_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing_index = index
            break
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            raise FrontMatterError(
                f"{source}: front matter line {index + 1} is missing ':'"
            )
        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        if not key:
            raise FrontMatterError(
                f"{source}: front matter line {index + 1} has an empty key"
            )
        metadata[key] = _parse_value(raw_value.strip())

    if closing_index is None:
        raise FrontMatterError(f"{source}: front matter is missing its closing '---'")

    body = "".join(lines[closing_index + 1 :])
    return Document(metadata=metadata, body=body)
