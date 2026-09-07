"""Versioned YAML configuration loading."""

from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Load one mapping from YAML and fail early on an unexpected root value."""
    value = yaml.safe_load(Path(path).read_text())
    if not isinstance(value, dict):
        raise ValueError(f"Expected a YAML mapping in {path}")
    return value
