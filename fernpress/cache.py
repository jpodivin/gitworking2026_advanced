"""Small incremental-build cache."""

import json
from pathlib import Path
from typing import Dict, List


class BuildCache:
    """Record source modification times between builds."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.entries: Dict[str, List[int]] = {}
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                self.entries = {
                    str(key): [int(value[0]), int(value[1])]
                    for key, value in raw.items()
                    if isinstance(value, list) and len(value) == 2
                }
        except (OSError, ValueError, TypeError, IndexError):
            self.entries = {}

    def _fingerprint(self, source: Path) -> List[int]:
        stat = source.stat()
        return [stat.st_mtime_ns, stat.st_size]

    def is_fresh(self, source: Path) -> bool:
        return self.entries.get(str(source.resolve())) == self._fingerprint(source)

    def record(self, source: Path) -> None:
        self.entries[str(source.resolve())] = self._fingerprint(source)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self.entries, indent=2, sort_keys=True), encoding="utf-8"
        )
