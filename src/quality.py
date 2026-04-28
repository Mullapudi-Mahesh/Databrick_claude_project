"""Data quality analysis: missing values per column and duplicate row count."""

from __future__ import annotations

from typing import Any, Dict

import pandas as pd


def compute_quality(df: pd.DataFrame) -> Dict[str, Any]:
    """Return missing-value stats per column and total duplicate row count.

    Return structure::

        {
            "missing": {
                "<col>": {"missing_count": int, "missing_pct": float},
                ...
            },
            "duplicates": int,
        }
    """
    total_rows = len(df)

    missing: Dict[str, Dict[str, Any]] = {}
    for col in df.columns:
        count = int(df[col].isnull().sum())
        pct = round((count / total_rows) * 100, 2) if total_rows > 0 else 0.0
        missing[col] = {"missing_count": count, "missing_pct": pct}

    duplicates = int(df.duplicated().sum())

    return {"missing": missing, "duplicates": duplicates}
