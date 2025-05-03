# JSON index

Each build writes `index.json` to the output root. It contains one object per
published page, in publication order.

```json
[
  {
    "title": "Hello, Fernpress",
    "url": "/posts/hello-fernpress/",
    "date": "2024-03-08",
    "tags": ["release", "notes"]
  }
]
```

## Fields

- `title`: the page title as rendered in templates.
- `url`: the site-relative post URL.
- `date`: ISO 8601 date, or `null` when no date was supplied.
- `tags`: the page's tag names, preserving their declared spelling.

The index is intended for client-side search, archives, and small tools. It is
not a replacement for the RSS feed or sitemap.
