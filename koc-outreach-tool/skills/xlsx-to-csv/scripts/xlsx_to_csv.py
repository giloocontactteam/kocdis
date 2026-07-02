#!/usr/bin/env python3
"""Break every sheet of an Excel workbook into its own CSV (UTF-8 BOM).

Usage:
    python3 xlsx_to_csv.py --input input/北美\\ KOC\\ 分潤計畫名單.xlsx --outdir export/_sheets
"""
from __future__ import annotations

import argparse
import os
import re

import pandas as pd


def safe_name(name: str) -> str:
    return re.sub(r'[/\\:*?"<>|]', "_", name).strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, help="Path to the .xlsx workbook.")
    ap.add_argument("--outdir", default="export/_sheets", help="Directory for the CSVs.")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    sheets = pd.read_excel(args.input, sheet_name=None, header=None)
    for name, df in sheets.items():
        path = os.path.join(args.outdir, f"{safe_name(name)}.csv")
        df.to_csv(path, index=False, header=False, encoding="utf-8-sig")
        print(f"{name!r} -> {path}  ({df.shape[0]} rows x {df.shape[1]} cols)")
    print(f"\nWrote {len(sheets)} sheets to {args.outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
