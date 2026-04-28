"""Basic tests for src/loader.py."""

import os
import tempfile

import pandas as pd
import pytest

from src.loader import load_csv


def _write_temp_csv(content: str, suffix: str = ".csv") -> str:
    """Write *content* to a temp file and return its path."""
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "w") as f:
        f.write(content)
    return path


def test_load_valid_csv():
    path = _write_temp_csv("a,b,c\n1,2,3\n4,5,6\n")
    try:
        info = load_csv(path)
        assert info.rows == 2
        assert info.columns == 3
        assert info.column_names == ["a", "b", "c"]
        assert "a" in info.dtypes
    finally:
        os.unlink(path)


def test_load_returns_correct_dtypes():
    path = _write_temp_csv("name,score\nAlice,10.5\nBob,20.0\n")
    try:
        info = load_csv(path)
        assert "float" in info.dtypes["score"]
        assert "object" in info.dtypes["name"]
    finally:
        os.unlink(path)


def test_empty_csv_exits(tmp_path):
    empty = tmp_path / "empty.csv"
    empty.write_text("")
    with pytest.raises(SystemExit) as exc:
        load_csv(str(empty))
    assert exc.value.code == 1
