"""Small ``{{ key }}`` template renderer."""

import re
from typing import Mapping

_PLACEHOLDER = re.compile(r"{{\s*([A-Za-z_][A-Za-z0-9_]*)\s*}}")


class TemplateError(ValueError):
    """Raised when a template cannot be rendered."""


def render_template(template: str, context: Mapping[str, object]) -> str:
    """Replace placeholder names with values from ``context``."""

    def replace(match: re.Match) -> str:
        key = match.group(1)
        try:
            value = context[key]
        except KeyError as exc:
            raise TemplateError(f"Template is missing value for '{key}'") from exc
        return str(value)

    return _PLACEHOLDER.sub(replace, template)
