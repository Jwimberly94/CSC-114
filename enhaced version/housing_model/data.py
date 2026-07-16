"""Data loading and preprocessing helpers."""

from __future__ import annotations

import csv
import os
from dataclasses import dataclass

import numpy as np

from .config import FEATURE_COLUMNS, TARGET_COLUMN


@dataclass
class DataBundle:
    features: np.ndarray
    targets: np.ndarray
    months: np.ndarray
    county_names: np.ndarray


@dataclass
class SplitBundle:
    x_train: np.ndarray
    x_test: np.ndarray
    y_train: np.ndarray
    y_test: np.ndarray
    test_months: np.ndarray
    test_county_names: np.ndarray
    test_sqft: np.ndarray
    train_data_shape: tuple[int, ...]
    test_data_shape: tuple[int, ...]


def resolve_data_path(cwd: str) -> str:
    primary = os.path.join(cwd, "alabama_housing (1).csv")
    if os.path.exists(primary):
        return primary

    fallback = os.path.join(cwd, "alabama_housing.csv")
    if os.path.exists(fallback):
        return fallback

    raise FileNotFoundError(
        "Could not find alabama_housing (1).csv or alabama_housing.csv in current folder."
    )


def load_data(cwd: str) -> DataBundle:
    data_path = resolve_data_path(cwd)

    features = []
    targets = []
    months = []
    county_names = []

    with open(data_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            months.append(int(row["month_date_yyyymm"]))
            county_names.append(row.get("county_name", "Unknown"))
            features.append([float(row[col]) for col in FEATURE_COLUMNS])
            targets.append(float(row[TARGET_COLUMN]))

    return DataBundle(
        features=np.array(features, dtype="float32"),
        targets=np.array(targets, dtype="float32"),
        months=np.array(months, dtype="int32"),
        county_names=np.array(county_names, dtype=object),
    )


def prepare_split(bundle: DataBundle) -> SplitBundle:
    train_idx = np.where(bundle.months <= 202412)[0]
    test_idx = np.where(bundle.months >= 202501)[0]

    if len(train_idx) == 0 or len(test_idx) == 0:
        raise ValueError(
            "Chronological split failed: expected rows for train (<=202412) and test (>=202501)."
        )

    train_data = bundle.features[train_idx]
    test_data = bundle.features[test_idx]
    train_targets = bundle.targets[train_idx]
    test_targets = bundle.targets[test_idx]

    mean = train_data.mean(axis=0)
    std = train_data.std(axis=0)
    x_train = (train_data - mean) / std
    x_test = (test_data - mean) / std

    y_train = train_targets / 100000
    y_test = test_targets / 100000

    sqft_idx = FEATURE_COLUMNS.index("median_square_feet")

    return SplitBundle(
        x_train=x_train,
        x_test=x_test,
        y_train=y_train,
        y_test=y_test,
        test_months=bundle.months[test_idx],
        test_county_names=bundle.county_names[test_idx],
        test_sqft=bundle.features[test_idx, sqft_idx],
        train_data_shape=train_data.shape,
        test_data_shape=test_data.shape,
    )
