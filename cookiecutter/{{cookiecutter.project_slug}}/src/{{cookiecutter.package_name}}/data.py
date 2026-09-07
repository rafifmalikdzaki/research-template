"""Dataset helpers with a group-safe split contract."""

from __future__ import annotations

import numpy as np
from sklearn.model_selection import GroupShuffleSplit


def group_train_test_indices(
    groups: np.ndarray, *, test_size: float = 0.2, seed: int = 42
) -> tuple[np.ndarray, np.ndarray]:
    """Return indices with no group appearing in both train and test."""
    groups = np.asarray(groups)
    if groups.ndim != 1 or len(groups) == 0:
        raise ValueError("groups must be a non-empty one-dimensional array")
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1")
    train, test = next(
        GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=seed).split(
            np.zeros(len(groups)), groups=groups
        )
    )
    if set(groups[train]) & set(groups[test]):
        raise RuntimeError("group leakage detected")
    return train, test
