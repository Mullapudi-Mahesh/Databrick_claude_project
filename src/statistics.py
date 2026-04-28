"""Compute descriptive statistics for numeric columns in a DataFrame."""

from __future__ import annotations

import warnings
from typing import Dict

import pandas as pd


def compute_statistics(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """Return min/max/mean/median/std for every numeric column, rounded to 4 d.p.

    Returns an empty dict if no numeric columns exist (a warning is printed).
    """
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        warnings.warn("Warning: No numeric columns found.")
        return {}

    stats: Dict[str, Dict[str, float]] = {}
    for col in numeric_df.columns:
        series = numeric_df[col]
        stats[col] = {
            "min": round(float(series.min()), 4),
            "max": round(float(series.max()), 4),
            "mean": round(float(series.mean()), 4),
            "median": round(float(series.median()), 4),
            "std": round(float(series.std()), 4),
        }

    return stats
