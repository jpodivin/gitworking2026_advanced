"""Load and validate Fernpress site configuration."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Union

DEFAULTS: Dict[str, Any] = {
    "title": "Fernpress site",
    "base_url": "",
    "content_dir": "content",
    "output_dir": "public",
    "template_dir": "templates",
    "static_dir": "static",
    "posts_per_page": 10,
}

PATH_FIELDS = ("content_dir", "output_dir", "template_dir", "static_dir")
KNOWN_KEYS = frozenset(DEFAULTS)


class ConfigError(ValueError):
    """Raised when a site configuration cannot be loaded."""


@dataclass(frozen=True)
class SiteConfig:
    """Resolved settings for one site build."""

    title: str
    base_url: str
    content_dir: Path
    output_dir: Path
    template_dir: Path
    static_dir: Path
    posts_per_page: int


def _read_json(path: Path) -> Mapping[str, Any]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigError(f"Configuration file not found: {path}") from exc
    except OSError as exc:
        raise ConfigError(f"Could not read configuration file {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigError(
            f"Invalid JSON in {path} at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc

    if not isinstance(raw, dict):
        raise ConfigError(f"Configuration in {path} must be a JSON object")
    return raw


def _string_setting(values: Mapping[str, Any], name: str) -> str:
    value = values[name]
    if not isinstance(value, str):
        raise ConfigError(f"Configuration value '{name}' must be a string")
    return value


def _positive_int_setting(values: Mapping[str, Any], name: str) -> int:
    value = values[name]
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ConfigError(f"Configuration value '{name}' must be a positive integer")
    return value


def load_config(path: Union[str, Path]) -> SiteConfig:
    """Load ``site.json`` and resolve its relative paths.

    Relative paths are resolved against the directory containing the
    configuration file. Defaults are used for omitted optional settings.
    """

    config_path = Path(path)
    raw = _read_json(config_path)
    unknown = sorted(set(raw) - KNOWN_KEYS)
    if unknown:
        raise ConfigError(f"Unknown configuration key(s): {', '.join(unknown)}")
    values = {**DEFAULTS, **raw}
    root = config_path.resolve().parent

    paths = {}
    for name in PATH_FIELDS:
        value = _string_setting(values, name)
        paths[name] = (root / value).resolve()

    return SiteConfig(
        title=_string_setting(values, "title"),
        base_url=_string_setting(values, "base_url").rstrip("/"),
        posts_per_page=_positive_int_setting(values, "posts_per_page"),
        **paths,
    )
