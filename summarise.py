"""Entry point for the CSV Data Summariser tool.

Usage:
    python summarise.py <csv_path>
"""

from __future__ import annotations

import argparse
import os
import sys


def parse_args() -> argparse.Namespace:
    """Parse and return CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Summarise a CSV file: statistics, data types, and quality report."
    )
    parser.add_argument("csv_path", help="Path to the CSV file to analyse.")
    return parser.parse_args()


def validate_path(csv_path: str) -> None:
    """Validate that *csv_path* exists and has a .csv extension."""
    if not os.path.exists(csv_path):
        print(f"Error: File not found: {csv_path}")
        sys.exit(1)
    if not csv_path.lower().endswith(".csv"):
        print(f"Error: File must be a CSV: {csv_path}")
        sys.exit(1)


def main() -> None:
    """Orchestrate input validation, data loading, analysis, and reporting."""
    args = parse_args()
    csv_path = args.csv_path

    validate_path(csv_path)

    # Lazy imports keep startup fast and avoid hard-crashing if pandas is missing
    try:
        from src.loader import load_csv
        from src.quality import compute_quality
        from src.reporter import print_report
        from src.statistics import compute_statistics
    except ImportError as exc:
        print(f"Error: Missing dependency — {exc}")
        print("Install requirements with: pip install -r requirements.txt")
        sys.exit(1)

    info = load_csv(csv_path)
    stats = compute_statistics(info.df)
    quality = compute_quality(info.df)
    print_report(csv_path, info, stats, quality)


if __name__ == "__main__":
    main()
