"""Load a CSV file into a pandas DataFrame and extract basic structural information."""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Dict

import pandas as pd


@dataclass
class DatasetInfo:
    """Holds structural metadata extracted from a CSV file."""

    df: pd.DataFrame
    rows: int
    columns: int
    column_names: list[str]
    dtypes: Dict[str, str] = field(default_factory=dict)


def load_csv(csv_path: str) -> DatasetInfo:
    """Load *csv_path* into a DataFrame and return structural metadata."""
    try:
        df = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{csv_path}' is empty or contains no data.")
        sys.exit(1)
    except pd.errors.ParserError as exc:
        print(f"Error: Could not parse '{csv_path}' as a valid CSV file. {exc}")
        sys.exit(1)

    rows, columns = df.shape
    column_names = df.columns.tolist()
    dtypes = {col: str(df[col].dtype) for col in column_names}

    return DatasetInfo(
        df=df,
        rows=rows,
        columns=columns,
        column_names=column_names,
        dtypes=dtypes,
    )
