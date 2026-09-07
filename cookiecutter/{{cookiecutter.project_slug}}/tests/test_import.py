import numpy as np

import {{ cookiecutter.package_name }}
from {{ cookiecutter.package_name }}.data import group_train_test_indices
from {{ cookiecutter.package_name }}.evaluate import classification_metrics


def test_package_imports():
    assert {{ cookiecutter.package_name }}.__doc__


def test_group_split_has_no_overlap():
    groups = np.repeat(np.arange(20), 2)
    train, test = group_train_test_indices(groups, seed=42)
    assert not set(groups[train]) & set(groups[test])


def test_metrics_are_recomputable():
    metrics = classification_metrics(np.array([0, 1]), np.array([0, 1]), np.array([0.1, 0.9]))
    assert metrics["accuracy"] == 1.0
