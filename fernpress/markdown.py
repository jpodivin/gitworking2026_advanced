"""A deliberately small Markdown renderer."""

import html
import re

_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_FENCE = re.compile(r"^```([A-Za-z0-9_+-]*)\s*$")


def _inline(text: str) -> str:
    value = html.escape(text, quote=False)
    value = re.sub(r"_([^_]+)_", r"<em>\1</em>", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", value)
    value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
    value = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', value)
    return value


def _paragraph(lines: list) -> str:
    text = " ".join(line.strip() for line in lines)
    return f"<p>{_inline(text)}</p>"


def render_markdown(text: str) -> str:
    """Render headings, paragraphs, inline spans, and fenced code as HTML.

    Raw HTML is escaped before the small inline syntax is applied.
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
            output.append(f"<h{level}>{_inline(heading.group(2))}</h{level}>")
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
