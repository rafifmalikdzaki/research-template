"""Command-line checks for a newly created study repository."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import load_yaml
from .provenance import git_revision


def main() -> None:
    parser = argparse.ArgumentParser(description="{{ cookiecutter.project_name }} research tools")
    subcommands = parser.add_subparsers(dest="command", required=True)
    doctor = subcommands.add_parser("doctor", help="check the generated study skeleton")
    doctor.add_argument("--config", type=Path, default=Path("configs/baseline.yaml"))
    args = parser.parse_args()
    if args.command == "doctor":
        config = load_yaml(args.config)
        print(json.dumps({"status": "ready", "config": config, "git_revision": git_revision()}))
