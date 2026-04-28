"""Format and print the human-readable CSV summary report to stdout."""

from __future__ import annotations

import os
from typing import Any, Dict

from src.loader import DatasetInfo

_WIDTH = 80
_DIV = "=" * _WIDTH
_THIN = "-" * _WIDTH


def _col_w(*widths: int) -> list[int]:
    """Helper – return a list of column widths."""
    return list(widths)


def print_report(
    csv_path: str,
    info: DatasetInfo,
    stats: Dict[str, Dict[str, float]],
    quality: Dict[str, Any],
) -> None:
    """Print the full summary report to stdout."""
    filename = os.path.basename(csv_path)

    # ------------------------------------------------------------------
    # Header
    # ------------------------------------------------------------------
    print(_DIV)
    title = f"CSV Summary Report: {filename}"
    print(title.center(_WIDTH))
    print(_DIV)

    # ------------------------------------------------------------------
    # Dataset Overview
    # ------------------------------------------------------------------
    print("\nDATASET OVERVIEW")
    print(f"  Rows: {info.rows}  |  Columns: {info.columns}")
    col_list = ", ".join(f"{c} ({info.dtypes[c]})" for c in info.column_names)
    # Wrap long column lists
    print(f"  Columns: {col_list}")

    # ------------------------------------------------------------------
    # Descriptive Statistics
    # ------------------------------------------------------------------
    print(f"\n{_THIN}")
    print("DESCRIPTIVE STATISTICS")
    if not stats:
        print("  (No numeric columns found — statistics not available.)")
    else:
        c0, c1, c2, c3, c4, c5 = 20, 10, 10, 10, 10, 10
        header = (
            "  "
            + "Column".ljust(c0)
            + "Min".rjust(c1)
            + "Max".rjust(c2)
            + "Mean".rjust(c3)
            + "Median".rjust(c4)
            + "Std Dev".rjust(c5)
        )
        print(header)
        print("  " + "-" * (c0 + c1 + c2 + c3 + c4 + c5))
        for col, s in stats.items():
            row = (
                "  "
                + col[:c0].ljust(c0)
                + str(s["min"]).rjust(c1)
                + str(s["max"]).rjust(c2)
                + str(s["mean"]).rjust(c3)
                + str(s["median"]).rjust(c4)
                + str(s["std"]).rjust(c5)
            )
            print(row)

    # ------------------------------------------------------------------
    # Data Quality
    # ------------------------------------------------------------------
    print(f"\n{_THIN}")
    print("DATA QUALITY")
    missing_data = quality["missing"]
    c0, c1, c2 = 20, 12, 12
    header = (
        "  "
        + "Column".ljust(c0)
        + "Missing".rjust(c1)
        + "Missing %".rjust(c2)
    )
    print(header)
    print("  " + "-" * (c0 + c1 + c2))
    for col, m in missing_data.items():
        row = (
            "  "
            + col[:c0].ljust(c0)
            + str(m["missing_count"]).rjust(c1)
            + f"{m['missing_pct']:.2f}%".rjust(c2)
        )
        print(row)
    print(f"\n  Duplicate rows: {quality['duplicates']}")
    print(_DIV)
