# Databricks notebook source
# CSV Data Summariser — Databricks Notebook
# Separate cells with: # COMMAND ----------

# COMMAND ----------

# MAGIC %pip install pandas

# COMMAND ----------

import os
import sys

# Allow imports from project root when running in Databricks
# (Adjust REPO_PATH to your Databricks Repos checkout path if needed)
REPO_PATH = "/Workspace/Repos/csv_summariser"
if REPO_PATH not in sys.path:
    sys.path.insert(0, REPO_PATH)

# COMMAND ----------

# Widget to accept the CSV path (can be a DBFS path, e.g. /dbfs/mnt/data/sample.csv)
dbutils.widgets.text("csv_path", "/dbfs/mnt/data/sample.csv", "CSV File Path")
csv_path = dbutils.widgets.get("csv_path")
print(f"Analysing: {csv_path}")

# COMMAND ----------

# Validate the path
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"File not found: {csv_path}")
if not csv_path.lower().endswith(".csv"):
    raise ValueError(f"File must be a CSV: {csv_path}")

# COMMAND ----------

# Load CSV
from src.loader import load_csv

info = load_csv(csv_path)
print(f"Loaded  |  Rows: {info.rows}  |  Columns: {info.columns}")
display(info.df.head(10))

# COMMAND ----------

# Descriptive statistics
from src.statistics import compute_statistics
import pandas as pd

stats = compute_statistics(info.df)

if stats:
    stats_rows = [
        {
            "Column": col,
            "Min": v["min"],
            "Max": v["max"],
            "Mean": v["mean"],
            "Median": v["median"],
            "Std Dev": v["std"],
        }
        for col, v in stats.items()
    ]
    display(pd.DataFrame(stats_rows))
else:
    print("No numeric columns found.")

# COMMAND ----------

# Data quality
from src.quality import compute_quality

quality = compute_quality(info.df)

missing_rows = [
    {
        "Column": col,
        "Missing Count": m["missing_count"],
        "Missing %": f"{m['missing_pct']:.2f}%",
    }
    for col, m in quality["missing"].items()
]
display(pd.DataFrame(missing_rows))
print(f"Total duplicate rows: {quality['duplicates']}")

# COMMAND ----------

# Full console-style report (printed to driver stdout / notebook output)
from src.reporter import print_report

print_report(csv_path, info, stats, quality)
