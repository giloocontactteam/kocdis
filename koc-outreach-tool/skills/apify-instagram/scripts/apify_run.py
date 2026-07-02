#!/usr/bin/env python3
"""Run Apify's Instagram Scraper as a fallback / cross-check, off your account.

Actor shu8hvrXbJbY3Eb9W (apify/instagram-scraper) runs on Apify's proxies, so it
does NOT risk your own Instagram account. NOTE: this actor does NOT return a
contact email field — it returns followers, bio, and `externalUrls`. Its value
here is surfacing websites to feed back into the email backfill.

Auth once:  apify login   (or export APIFY_TOKEN=apify_api_xxx)

    python3 apify_run.py --gaps-only --crawl export/aying/01_ig_crawl.csv \
                         --dataset export/aying/apify_dataset.json
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys

ACTOR_ID = "shu8hvrXbJbY3Eb9W"


def gap_handles(crawl_csv: str) -> list[str]:
    """Handles that are known but still have no email — worth paying to resolve."""
    gaps: dict[str, None] = {}
    for r in csv.DictReader(open(crawl_csv, encoding="utf-8-sig")):
        h = (r.get("resolved_handle") or "").strip()
        if h and not (r.get("email") or "").strip():
            gaps[h.lower()] = None
    return sorted(gaps)


def all_handles(crawl_csv: str) -> list[str]:
    hs: dict[str, None] = {}
    for r in csv.DictReader(open(crawl_csv, encoding="utf-8-sig")):
        h = (r.get("resolved_handle") or "").strip()
        if h and r.get("status") == "ok":
            hs[h.lower()] = None
    return sorted(hs)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--crawl", required=True)
    ap.add_argument("--dataset", default="export/apify_dataset.json", help="Where to save raw dataset JSON.")
    ap.add_argument("--input-file", default="/tmp/apify_ig_input.json")
    ap.add_argument("--gaps-only", action="store_true", help="Only known-but-no-email handles.")
    ap.add_argument("--build-input", action="store_true", help="Only write the actor input file.")
    args = ap.parse_args()

    handles = gap_handles(args.crawl) if args.gaps_only else all_handles(args.crawl)
    print(f"{len(handles)} handles ({'gaps' if args.gaps_only else 'all ok'})")
    payload = {
        "directUrls": [f"https://www.instagram.com/{h}/" for h in handles],
        "resultsType": "details", "resultsLimit": 1,
        "searchType": "user", "addParentData": False,
    }
    json.dump(payload, open(args.input_file, "w"), ensure_ascii=False, indent=1)
    print(f"wrote {args.input_file}")
    if args.build_input:
        return 0

    cmd = ["apify", "call", ACTOR_ID, "--input-file", args.input_file, "--output-dataset", "--silent"]
    print("running:", " ".join(cmd))
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr[-2000:], file=sys.stderr)
        raise SystemExit("apify call failed — run `apify login` or set APIFY_TOKEN.")
    items = json.loads(proc.stdout)
    os.makedirs(os.path.dirname(args.dataset) or ".", exist_ok=True)
    json.dump(items, open(args.dataset, "w"), ensure_ascii=False)
    have_url = sum(1 for it in items if it.get("externalUrls"))
    print(f"got {len(items)} profiles ({have_url} with externalUrl) -> {args.dataset}")
    print("Next: feed --apify into the email backfill to scrape those sites.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
