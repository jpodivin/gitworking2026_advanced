"""Small incremental-build cache."""

import json
from pathlib import Path
from typing import Dict


class BuildCache:
    """Record source modification times between builds."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.entries: Dict[str, int] = {}
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                self.entries = {
                    str(key): int(value) for key, value in raw.items() if isinstance(value, int)
                }
        except (OSError, ValueError, TypeError):
            self.entries = {}

    def is_fresh(self, source: Path) -> bool:
        return self.entries.get(str(source.resolve())) == int(source.stat().st_mtime)

    def record(self, source: Path) -> None:
        self.entries[str(source.resolve())] = int(source.stat().st_mtime)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self.entries, indent=2, sort_keys=True), encoding="utf-8"
        )
