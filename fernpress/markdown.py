"""A deliberately small Markdown renderer."""

import html
import re

_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_FENCE = re.compile(r"^```([A-Za-z0-9_+-]*)\s*$")


def _paragraph(lines: list) -> str:
    text = " ".join(line.strip() for line in lines)
    return f"<p>{html.escape(text)}</p>"


def render_markdown(text: str) -> str:
    """Render headings, paragraphs, and fenced code blocks as HTML.

    Raw HTML is escaped. More inline syntax is intentionally left for a later
    release so the initial renderer stays small and predictable.
    """

    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    output = []
    index = 0

    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue

        fence = _FENCE.match(line)
        if fence:
            language = fence.group(1)
            index += 1
            code_lines = []
            while index < len(lines) and not _FENCE.match(lines[index]):
                code_lines.append(lines[index])
                index += 1
            if index < len(lines):
                index += 1
            code = html.escape("\n".join(code_lines))
            class_name = f' class="language-{language}"' if language else ""
            output.append(f"<pre><code{class_name}>{code}</code></pre>")
            continue

        heading = _HEADING.match(line)
        if heading:
            level = len(heading.group(1))
            output.append(f"<h{level}>{html.escape(heading.group(2))}</h{level}>")
            index += 1
            continue

        paragraph_lines = []
        while index < len(lines):
            candidate = lines[index]
            if not candidate.strip() or _HEADING.match(candidate) or _FENCE.match(candidate):
                break
            paragraph_lines.append(candidate)
            index += 1
        output.append(_paragraph(paragraph_lines))

    return "\n".join(output) + ("\n" if output else "")
