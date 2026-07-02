---
name: xlsx-to-csv
description: Break an Excel (.xlsx) workbook into one UTF-8 CSV per sheet. Use when starting from a KOC workbook and you need per-sheet CSVs to crawl or enrich.
---

# xlsx-to-csv

Splits every sheet of an Excel workbook into its own CSV, written with a UTF-8
BOM so Chinese text opens correctly in Excel. Raw cell content is preserved (no
header assumption) because KOC sheets carry two banner/header rows.

## When to use

- You have a `.xlsx` KOC workbook in `input/` and need CSVs for the pipeline.
- A sheet was updated and you need to re-export.

## Run

```bash
python3 skills/xlsx-to-csv/scripts/xlsx_to_csv.py \
    --input "input/北美 KOC 分潤計畫名單.xlsx" \
    --outdir export/_sheets
```

Each sheet → `export/_sheets/<sheet name>.csv`. Move the one you want to enrich
into `input/` (e.g. `input/Aying.csv`) before running the crawl skill.

## Notes

- Depends only on `pandas` + `openpyxl`.
- Sheet names with `/ \ : * ? " < > |` are sanitized to `_`.
