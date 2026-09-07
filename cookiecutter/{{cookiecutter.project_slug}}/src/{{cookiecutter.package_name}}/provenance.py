"""Small provenance helpers for reproducible run bundles."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


def sha256(path: str | Path) -> str:
    """Return the SHA-256 digest of a file."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git_revision() -> str | None:
    """Return the current Git revision, or None outside a Git checkout."""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def write_json(path: str | Path, value: dict[str, Any]) -> None:
    """Write stable, human-readable JSON metadata."""
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
