"""Held-out evaluation helpers."""

from __future__ import annotations

import numpy as np
from sklearn.metrics import accuracy_score, balanced_accuracy_score, roc_auc_score


def classification_metrics(
    target: np.ndarray, prediction: np.ndarray, probability: np.ndarray
) -> dict[str, float]:
    """Compute basic metrics from per-example held-out predictions."""
    target, prediction, probability = map(np.asarray, (target, prediction, probability))
    if not (len(target) == len(prediction) == len(probability)):
        raise ValueError("target, prediction, and probability must have equal lengths")
    return {
        "accuracy": float(accuracy_score(target, prediction)),
        "balanced_accuracy": float(balanced_accuracy_score(target, prediction)),
        "roc_auc": float(roc_auc_score(target, probability)),
    }
