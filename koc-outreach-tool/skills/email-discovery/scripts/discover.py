#!/usr/bin/env python3
"""Email-first contact discovery: try multiple strategies until an email is found.

The real goal is a CONTACT EMAIL per KOC; the IG handle is just one route. For
each row still missing an email, runs a cascade (highest-precision first):

  1. ig_api          — known handle -> business/public email or bio email
  2. website_scrape  — fetch website + /contact /about ... for emails
  3. ig_from_website — no handle? find the IG link on the website, then ig_api

Use --skip-ig once profiles are already crawled (website scraping only) so we
don't re-hit Instagram and risk the account.

    python3 discover.py --input input/Aying.csv --crawl export/aying/01_ig_crawl.csv \
                        --output export/aying/02_contacts.csv [--skip-ig]
"""
from __future__ import annotations

import argparse
import csv
import os
import random
import sys
import time

from outreach import igclient
from outreach.emails import good_emails
from outreach.sheet import load_rows
from outreach.websites import email_from_website, ig_handle_from_website


def email_from_ig(page, handle: str) -> tuple[str, str]:
    if not handle:
        return "", ""
    try:
        res = igclient.scrape_profile(page, handle)
    except Exception:
        return "", ""
    if res.status != "ok":
        return "", ""
    if res.email:
        return res.email, "high"
    found = good_emails(res.bio or "")
    return (found[0], "medium") if found else ("", "")


def known_email_and_handle(crawl_path: str) -> tuple[dict, dict]:
    emails, handles = {}, {}
    if os.path.exists(crawl_path):
        for r in csv.DictReader(open(crawl_path, encoding="utf-8-sig")):
            if (r.get("email") or "").strip():
                emails[r["row_no"]] = r["email"]
            h = (r.get("resolved_handle") or "").strip()
            if h and r.get("status") == "ok":
                handles[r["row_no"]] = h
    return emails, handles


def discover(page, row: dict, delay, skip_ig: bool) -> dict:
    rec = dict(row, email_strategy="", email_confidence="", email_source="")
    if rec["email"]:
        rec["email_strategy"] = "already_known"
        return rec
    if not skip_ig:
        email, conf = email_from_ig(page, rec["handle"])
        if email:
            rec.update(email=email, email_strategy="ig_api", email_confidence=conf,
                       email_source=f"https://www.instagram.com/{rec['handle']}/")
            return rec
    email, src, conf = email_from_website(page, rec["website"])
    if email:
        rec.update(email=email, email_strategy="website_scrape", email_confidence=conf, email_source=src)
        return rec
    if not skip_ig and not rec["handle"] and rec["website"]:
        h = ig_handle_from_website(page, rec["website"])
        if h:
            rec["handle"] = h
            time.sleep(random.uniform(*delay))
            email, conf = email_from_ig(page, h)
            if email:
                rec.update(email=email, email_strategy="ig_from_website", email_confidence=conf,
                           email_source=f"https://www.instagram.com/{h}/")
                return rec
    rec["email_strategy"] = "not_found"
    return rec


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True)
    ap.add_argument("--crawl", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--skip-ig", action="store_true")
    ap.add_argument("--min-delay", type=float, default=2.5)
    ap.add_argument("--max-delay", type=float, default=4.5)
    args = ap.parse_args()

    rows = load_rows(args.input)
    emails, handles = known_email_and_handle(args.crawl)
    for r in rows:
        r["email"] = emails.get(r["row_no"], "")
        r["handle"] = r["handle"] or handles.get(r["row_no"], "")
    missing = [r for r in rows if not r["email"]]
    todo = missing[: args.limit] if args.limit else missing
    print(f"{len(rows)} rows | {len(rows) - len(missing)} have email | "
          f"{len(missing)} missing | attempting {len(todo)}")

    results = {r["row_no"]: r for r in rows}
    by_strategy: dict[str, int] = {}
    with igclient.sync_playwright() as p:
        try:
            _b, _c, page = igclient.connect(p)
        except Exception as e:
            print(f"Connect Chrome first: python3 seed_and_launch.py\n{e}", file=sys.stderr)
            return 2
        for i, row in enumerate(todo, 1):
            rec = discover(page, row, (args.min_delay, args.max_delay), args.skip_ig)
            results[rec["row_no"]] = rec
            by_strategy[rec["email_strategy"]] = by_strategy.get(rec["email_strategy"], 0) + 1
            print(f"[{i}/{len(todo)}] {row['name'][:32]:32} -> {rec['email_strategy']:16} {rec['email'] or '-'}", flush=True)
            time.sleep(random.uniform(args.min_delay, args.max_delay))
        page.close()

    fields = ["row_no", "name", "email", "email_strategy", "email_confidence", "email_source", "handle", "website"]
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for rn in sorted(results, key=lambda x: int(x) if x.isdigit() else 0):
            w.writerow({k: results[rn].get(k, "") for k in fields})
    have = sum(1 for r in results.values() if r.get("email"))
    print(f"\nDone. email coverage {have}/{len(results)} "
          f"({100*have//max(len(results),1)}%). -> {args.output}")
    print("strategies:", by_strategy)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
