#!/usr/bin/env python3
"""Backfill emails from EVERY website we know about, writing incrementally.

For each row in the crawl output still missing an email, unions all candidate
sites (deduped, Instagram links skipped):

  1. the crawl `website` column (IG external_url)
  2. the source sheet's 其他平台連結 / IG 連結
  3. optional Apify dataset externalUrls (--apify <dataset.json>)

Scrapes each site/contact page and writes the first good email straight back
into the crawl CSV after every hit, so a crash never loses progress.

    python3 backfill.py --crawl export/aying/01_ig_crawl.csv --input input/Aying.csv \
                        [--apify export/aying/apify_dataset.json]
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import shutil
import sys
import time

from outreach import igclient
from outreach.sheet import COL_OTHER, COL_URL
from outreach.text import clean
from outreach.websites import email_from_website, email_via_aggregator, is_aggregator


def sheet_links(input_path: str) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for r in list(csv.reader(open(input_path, encoding="utf-8-sig")))[2:]:
        if not r or not r[0].strip():
            continue
        links = [clean(r[i]) for i in (COL_OTHER, COL_URL) if len(r) > i and clean(r[i])]
        out[r[0].strip()] = links
    return out


def apify_exturls(path: str) -> dict[str, str]:
    out: dict[str, str] = {}
    if path and os.path.exists(path):
        for rec in json.load(open(path)):
            ext = rec.get("externalUrls") or []
            if ext:
                url = ext[0].get("url") if isinstance(ext[0], dict) else ext[0]
                if url:
                    out[(rec.get("username") or "").lower()] = url
    return out


def candidate_sites(row: dict, links: dict, exturls: dict) -> list[str]:
    pool = [row.get("website", "")] + links.get(row["row_no"], [])
    h = (row.get("resolved_handle") or "").lower()
    if h in exturls:
        pool.append(exturls[h])
    seen, out = set(), []
    for u in pool:
        u = (u or "").strip()
        if u and "instagram.com" not in u and u.rstrip("/").lower() not in seen:
            seen.add(u.rstrip("/").lower())
            out.append(u)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--crawl", required=True, help="Crawl CSV to backfill in place.")
    ap.add_argument("--input", required=True, help="Source sheet CSV (for extra links).")
    ap.add_argument("--apify", default="", help="Optional Apify dataset JSON.")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--min-delay", type=float, default=1.0)
    ap.add_argument("--max-delay", type=float, default=2.0)
    args = ap.parse_args()

    rows = list(csv.DictReader(open(args.crawl, encoding="utf-8-sig")))
    fields = list(rows[0].keys())
    links, exturls = sheet_links(args.input), apify_exturls(args.apify)

    todo = [r for r in rows if not (r.get("email") or "").strip()]
    todo = [r for r in todo if candidate_sites(r, links, exturls)]
    if args.limit:
        todo = todo[: args.limit]
    print(f"{len(rows)} rows | {len(todo)} missing-email rows have a website to try")

    shutil.copy2(args.crawl, args.crawl + ".bak")

    def flush():
        with open(args.crawl, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)

    with igclient.sync_playwright() as p:
        try:
            _b, _c, page = igclient.connect(p)
        except Exception as e:
            print(f"Connect Chrome first: python3 seed_and_launch.py\n{e}", file=sys.stderr)
            return 2
        filled = 0
        for i, row in enumerate(todo, 1):
            got = ""
            for url in candidate_sites(row, links, exturls):
                try:
                    if is_aggregator(url):
                        # linktr.ee etc. hold no email — follow their outbound sites,
                        # but only the entity's OWN site (guards against publishers).
                        email, src, conf = email_via_aggregator(
                            page, url, handle=row.get("resolved_handle", ""), name=row.get("name", ""))
                    else:
                        email, src, conf = email_from_website(page, url)
                except Exception:
                    email = ""
                if email:
                    row.update(email=email, email_source=src,
                               email_confidence=conf + " (website backfill)")
                    got = email
                    filled += 1
                    break
                time.sleep(random.uniform(args.min_delay, args.max_delay))
            print(f"[{i}/{len(todo)}] {row['name'][:30]:30} -> {got or '-'}", flush=True)
            if got:
                flush()
        flush()
        page.close()
    have = sum(1 for r in rows if (r.get("email") or "").strip())
    print(f"\nDone. filled {filled} | total email {have}/{len(rows)} -> {args.crawl}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
