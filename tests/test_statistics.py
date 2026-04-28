"""Basic tests for src/statistics.py."""

import warnings

import pandas as pd
import pytest

from src.statistics import compute_statistics


def test_basic_stats():
    df = pd.DataFrame({"a": [1.0, 2.0, 3.0, 4.0, 5.0]})
    result = compute_statistics(df)
    assert "a" in result
    s = result["a"]
    assert s["min"] == 1.0
    assert s["max"] == 5.0
    assert s["mean"] == 3.0
    assert s["median"] == 3.0
    assert round(s["std"], 4) == s["std"]  # already rounded


def test_non_numeric_skipped():
    df = pd.DataFrame({"name": ["Alice", "Bob"], "score": [10.0, 20.0]})
    result = compute_statistics(df)
    assert "name" not in result
    assert "score" in result


def test_no_numeric_columns_returns_empty():
    df = pd.DataFrame({"city": ["London", "Paris"]})
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = compute_statistics(df)
    assert result == {}
    assert any("No numeric columns" in str(warning.message) for warning in w)


def test_rounding_to_4dp():
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5, 6, 7]})
    result = compute_statistics(df)
    for val in result["x"].values():
        assert len(str(val).split(".")[-1]) <= 4
