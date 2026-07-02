#!/usr/bin/env python3
"""Crawl Instagram profiles listed in a KOC CSV via the logged-in debug Chrome.

Reads every row, resolves an IG handle (from the handle column or IG link),
fetches profile data (followers, bio, website, contact email) and writes one row
per source row. Idempotent: re-running skips 序號 already in the output.

    python3 crawl.py --input input/Aying.csv --output export/aying/01_ig_crawl.csv
"""
from __future__ import annotations

import argparse
import csv
import os
import random
import sys
import time
from dataclasses import asdict

from outreach import igclient
from outreach.sheet import load_rows, load_done


def write_row(out_path: str, prof: igclient.Profile, row: dict) -> None:
    prof.name = row["name"]
    prof.row_no = row["row_no"]
    new = not os.path.exists(out_path)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "a", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(asdict(prof).keys()))
        if new:
            w.writeheader()
        w.writerow(asdict(prof))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--min-delay", type=float, default=4.0)
    ap.add_argument("--max-delay", type=float, default=9.0)
    args = ap.parse_args()

    rows = load_rows(args.input)
    done = load_done(args.output)
    pending = [r for r in rows if r["key"] not in done]
    if args.limit:
        pending = pending[: args.limit]
    with_handle = sum(1 for r in pending if r["handle"])
    print(f"rows {len(rows)} | done {len(done)} | pending {len(pending)} "
          f"({with_handle} to crawl, {len(pending) - with_handle} no-IG)")
    if not pending:
        print("Nothing to do.")
        return 0

    with igclient.sync_playwright() as p:
        try:
            _browser, _ctx, page = igclient.connect(p)
        except Exception as e:
            print(f"Connect Chrome first: python3 seed_and_launch.py\n{e}", file=sys.stderr)
            return 2
        ok = 0
        for i, r in enumerate(pending, 1):
            if r["handle"]:
                print(f"[{i}/{len(pending)}] @{r['handle']} ...", end=" ", flush=True)
                try:
                    prof = igclient.scrape_profile(page, r["handle"], fallback_email=r["source_email"])
                except Exception as e:
                    prof = igclient.Profile(resolved_handle=r["handle"],
                                            status=f"error: {type(e).__name__}",
                                            email=r["source_email"])
            else:
                print(f"[{i}/{len(pending)}] (no IG) {r['name'][:30]} ...", end=" ", flush=True)
                prof = igclient.Profile(email=r["source_email"], status="no_ig_handle")
            write_row(args.output, prof, r)
            print(f"{prof.status} | email={prof.email or '-'}")
            ok += prof.status == "ok"
            if r["handle"] and i < len(pending):
                time.sleep(random.uniform(args.min_delay, args.max_delay))
        page.close()
    print(f"\nDone. {ok} crawled OK | {len(pending)} processed -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
