"""Machine-readable index of published content."""

import json
from datetime import date as Date
from pathlib import Path
from typing import Any, Iterable

from fernpress.config import SiteConfig
from fernpress.paths import safe_join
from fernpress.urls import page_url


def write_json_index(config: SiteConfig, pages: Iterable[Any]) -> Path:
    """Write a compact JSON index for search and client-side tooling."""

    records = []
    for page in pages:
        records.append(
            {
                "title": page.title,
                "url": page_url(page.slug),
                "date": None if page.date == Date.min else page.date.isoformat(),
                "tags": list(page.tags),
            }
        )
    destination = safe_join(config.output_dir, "index.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(records, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return destination
