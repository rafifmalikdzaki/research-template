import json

import pandas as pd
import pytest
import yaml
from sklearn.metrics import accuracy_score, roc_auc_score

from research_template.cli import run_demo, sha256


def test_reproducible_grouped_bundle(tmp_path):
    config = tmp_path / "demo.yaml"
    config.write_text(yaml.safe_dump({"seed": 42, "n_groups": 100, "test_size": 0.2}))
    first = run_demo(config, tmp_path / "runs")
    second = run_demo(config, tmp_path / "runs")
    assert first != second
    assert (first / "predictions.csv").read_bytes() == (second / "predictions.csv").read_bytes()
    splits = pd.read_csv(first / "splits.csv")
    assert splits.groupby("group_id")["split"].nunique().eq(1).all()
    assert splits.sample_id.is_unique
    predictions = pd.read_csv(first / "predictions.csv")
    assert set(predictions.sample_id) == set(splits.loc[splits.split == "test", "sample_id"])
    metrics = json.loads((first / "metrics.json").read_text())
    assert metrics["accuracy"] == accuracy_score(predictions.target, predictions.prediction)
    assert metrics["roc_auc"] == roc_auc_score(predictions.target, predictions.probability)
    manifest = json.loads((first / "manifest.json").read_text())
    assert manifest["evidence"] == "synthetic_smoke_only"
    for name, checksum in manifest["files"].items():
        assert sha256(first / name) == checksum


@pytest.mark.parametrize(
    "settings",
    [
        {},
        {"seed": 42, "n_groups": 2, "test_size": 0.2},
        {"seed": 42, "n_groups": 100, "test_size": 1.0},
        {"seed": -1, "n_groups": 100, "test_size": 0.2},
    ],
)
def test_invalid_config_does_not_create_run(tmp_path, settings):
    config = tmp_path / "bad.yaml"
    config.write_text(yaml.safe_dump(settings))
    with pytest.raises(ValueError):
        run_demo(config, tmp_path / "runs")
    assert not (tmp_path / "runs").exists()
