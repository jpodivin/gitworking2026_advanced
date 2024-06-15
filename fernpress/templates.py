"""Small ``{{ key }}`` template renderer."""

import html
import re
from typing import Mapping

_PLACEHOLDER = re.compile(r"{{\s*([A-Za-z_][A-Za-z0-9_]*)\s*}}")


class TemplateError(ValueError):
    """Raised when a template cannot be rendered."""


def render_template(
    template: str,
    context: Mapping[str, object],
    raw_keys: tuple = ("content",),
) -> str:
    """Replace placeholder names with values from ``context``.

    Values are treated as text and HTML-escaped by default. The ``content``
    value is inserted as pre-rendered HTML.
    """

    def replace(match: re.Match) -> str:
        key = match.group(1)
        try:
            value = context[key]
        except KeyError as exc:
            raise TemplateError(f"Template is missing value for '{key}'") from exc
        rendered = str(value)
        return rendered if key in raw_keys else html.escape(rendered, quote=True)

    return _PLACEHOLDER.sub(replace, template)
