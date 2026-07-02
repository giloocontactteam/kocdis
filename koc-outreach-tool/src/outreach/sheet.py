"""Read the KOC source sheet and the crawl output.

The source CSVs (exported from the KOC Excel workbook) have TWO header rows:
row 0 is a section banner ("A. 基本識別" ...), row 1 holds the real column names.
Column order is fixed:

    0 序號 | 1 KOC 名稱 | 2 IG Handle | 3 IG 連結 | 4 Email | 5 其他平台連結 | ...
"""
from __future__ import annotations

import csv
import os

from .text import clean, normalize_handle

COL_NO, COL_NAME, COL_HANDLE, COL_URL, COL_EMAIL, COL_OTHER = 0, 1, 2, 3, 4, 5


def load_rows(path: str) -> list[dict]:
    """Return EVERY data row with a stable ``key`` (序號) for de-duplication.

    ``handle`` is the resolved IG handle (may be empty); ``website`` prefers a
    non-Instagram link from 其他平台連結, falling back to the IG 連結 column.
    """
    out: list[dict] = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    for idx, raw in enumerate(rows[2:]):  # skip the 2 header rows
        if not raw or not any(clean(c) for c in raw):
            continue
        get = lambda i: raw[i] if len(raw) > i else ""  # noqa: E731
        row_no = clean(get(COL_NO))
        ig_url = clean(get(COL_URL))
        other = clean(get(COL_OTHER))
        website = next((u for u in (other, ig_url) if u and "instagram.com" not in u), "")
        out.append({
            "key": row_no or f"#idx{idx}",
            "row_no": row_no,
            "name": clean(get(COL_NAME)),
            "source_handle": clean(get(COL_HANDLE)),
            "source_url": ig_url,
            "source_email": clean(get(COL_EMAIL)),
            "handle": normalize_handle(get(COL_HANDLE), ig_url),
            "website": website,
        })
    return out


def load_done(path: str, key: str = "row_no") -> set[str]:
    """Return the set of values already present in an output CSV's ``key`` column."""
    if not os.path.exists(path):
        return set()
    done = set()
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            v = (row.get(key) or "").strip()
            if v:
                done.add(v)
    return done
