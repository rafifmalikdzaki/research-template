"""A download-free synthetic baseline with an auditable artifact bundle."""

import argparse
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import numpy as np
import pandas as pd
import yaml
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, roc_auc_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_state() -> dict:
    try:
        revision = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True
        ).strip()
        dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], text=True))
        return {"commit": revision, "dirty": dirty}
    except (FileNotFoundError, subprocess.CalledProcessError):
        return {"commit": None, "dirty": None}


def run_demo(config: Path, output_root: Path) -> Path:
    settings = yaml.safe_load(config.read_text())
    if not isinstance(settings, dict) or set(settings) != {"seed", "n_groups", "test_size"}:
        raise ValueError("Demo config must contain exactly seed, n_groups, and test_size")
    seed, n_groups, test_size = (settings[k] for k in ("seed", "n_groups", "test_size"))
    if type(seed) is not int or not 0 <= seed < 2**32:
        raise ValueError("seed must be an integer in [0, 2**32)")
    if type(n_groups) is not int or n_groups < 20:
        raise ValueError("n_groups must be an integer >= 20")
    if type(test_size) not in (int, float) or not 0.1 <= test_size <= 0.5:
        raise ValueError("test_size must be between 0.1 and 0.5")

    # Each synthetic subject has two observations; split subjects, not observations.
    base_x, base_y = make_classification(
        n_samples=n_groups, n_features=12, n_informative=6, random_state=seed
    )
    groups = np.repeat(np.arange(n_groups), 2)
    rng = np.random.default_rng(seed)
    x = np.repeat(base_x, 2, axis=0) + rng.normal(0, 0.05, (2 * n_groups, 12))
    y = np.repeat(base_y, 2)
    train, test = next(
        GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=seed).split(x, y, groups)
    )
    if set(groups[train]) & set(groups[test]):
        raise RuntimeError("Group leakage detected")
    if len(np.unique(y[train])) != 2 or len(np.unique(y[test])) != 2:
        raise ValueError("Both splits need both classes; increase n_groups or change seed")
    model = make_pipeline(StandardScaler(), LogisticRegression(random_state=seed, max_iter=1000))
    model.fit(x[train], y[train])
    probability = model.predict_proba(x[test])[:, 1]
    prediction = (probability >= 0.5).astype(int)
    metrics = {
        "accuracy": float(accuracy_score(y[test], prediction)),
        "balanced_accuracy": float(balanced_accuracy_score(y[test], prediction)),
        "roc_auc": float(roc_auc_score(y[test], probability)),
    }
    run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]
    destination = output_root / run_id
    destination.mkdir(parents=True, exist_ok=False)
    (destination / "config.yaml").write_text(yaml.safe_dump(settings, sort_keys=True))
    (destination / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    pd.DataFrame(
        {
            "sample_id": test,
            "group_id": groups[test],
            "target": y[test],
            "prediction": prediction,
            "probability": probability,
        }
    ).to_csv(destination / "predictions.csv", index=False)
    split = np.full(len(y), "train", dtype=object)
    split[test] = "test"
    pd.DataFrame(
        {
            "sample_id": np.arange(len(y)),
            "group_id": groups,
            "split": split,
        }
    ).to_csv(destination / "splits.csv", index=False)
    versions = {
        dist.metadata["Name"]: dist.version
        for dist in importlib.metadata.distributions()
        if dist.metadata["Name"]
    }
    (destination / "environment.json").write_text(
        json.dumps(
            {
                "python": sys.version,
                "platform": platform.platform(),
                "packages": versions,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    manifest = {
        "schema_version": 1,
        "run_id": run_id,
        "status": "completed",
        "evidence": "synthetic_smoke_only",
        "dataset": "sklearn.make_classification",
        "dataset_sha256": hashlib.sha256(x.tobytes() + y.tobytes()).hexdigest(),
        "evaluation": "group-held-out; fixed baseline; no hyperparameter selection",
        "metric_unit": "observation",
        "seed": seed,
        "git": git_state(),
        "argv": sys.argv,
        "checkpoint": None,
        "lock_sha256": sha256(Path("uv.lock")) if Path("uv.lock").exists() else None,
        "files": {p.name: sha256(p) for p in sorted(destination.iterdir())},
    }
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    demo = subcommands.add_parser("demo", help="Run a synthetic grouped tabular baseline")
    demo.add_argument("--config", type=Path, default=Path("configs/demo.yaml"))
    demo.add_argument("--output-root", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    try:
        destination = run_demo(args.config, args.output_root)
    except (ValueError, OSError, yaml.YAMLError) as exc:
        parser.exit(2, f"error: {exc}\n")
    print(f"Synthetic smoke test completed: {destination}")


if __name__ == "__main__":
    main()
