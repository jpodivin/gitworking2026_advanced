# Excerpts

Every page exposes an `excerpt` value to its layout template. It is generated
from the Markdown source, stripped of common formatting markers, whitespace
normalized, and shortened to roughly 160 characters.

```html
<article>
  <h2>{{ title }}</h2>
  <p>{{ excerpt }}</p>
  <a href="/posts/{{ slug }}/">Read more</a>
</article>
```

The excerpt is plain text and is escaped by the template renderer. It is
intended for summaries and index cards, not full article bodies.
