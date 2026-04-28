"""Basic tests for src/quality.py."""

import pandas as pd

from src.quality import compute_quality


def test_no_missing_no_duplicates():
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    result = compute_quality(df)
    for col in ["a", "b"]:
        assert result["missing"][col]["missing_count"] == 0
        assert result["missing"][col]["missing_pct"] == 0.0
    assert result["duplicates"] == 0


def test_missing_values_counted():
    df = pd.DataFrame({"a": [1, None, 3], "b": [None, None, "z"]})
    result = compute_quality(df)
    assert result["missing"]["a"]["missing_count"] == 1
    assert result["missing"]["b"]["missing_count"] == 2
    assert result["missing"]["b"]["missing_pct"] == round(2 / 3 * 100, 2)


def test_duplicate_rows_counted():
    df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]})
    result = compute_quality(df)
    assert result["duplicates"] == 1


def test_all_columns_present_in_missing():
    df = pd.DataFrame({"num": [1.0, 2.0], "text": ["a", "b"]})
    result = compute_quality(df)
    assert set(result["missing"].keys()) == {"num", "text"}
