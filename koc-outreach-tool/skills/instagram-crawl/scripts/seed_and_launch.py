#!/usr/bin/env python3
"""Start (or stop) an authenticated headless debug Chrome for crawling.

    python3 seed_and_launch.py --list                  # show profiles w/ IG login
    python3 seed_and_launch.py --profile "<profile>"   # seed + launch a logged_in profile
    python3 seed_and_launch.py --stop                  # shut it down

Profiles with an Instagram session are auto-detected; pick one that's logged
into the account you want to crawl under.
"""
from __future__ import annotations

import argparse
import sys

from outreach import browser


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--profile", default="Default", help='Chrome profile dir to copy cookies from.')
    ap.add_argument("--port", type=int, default=browser.DEFAULT_PORT)
    ap.add_argument("--list", action="store_true", help="List profiles and their IG login status.")
    ap.add_argument("--stop", action="store_true", help="Stop the debug Chrome and exit.")
    args = ap.parse_args()

    if args.list:
        for prof, status in browser.list_ig_profiles():
            print(f"{prof:12} {status}")
        return 0
    if args.stop:
        browser.stop()
        print("Stopped debug Chrome (if running).")
        return 0

    try:
        proc = browser.seed_and_launch(args.profile, args.port)
    except Exception as e:
        print(f"Failed to launch: {e}", file=sys.stderr)
        return 1
    print(f"Debug Chrome up (pid {proc.pid}) on port {args.port}, profile {args.profile!r}.")
    print("Now run:  python3 skills/instagram-crawl/scripts/crawl.py ...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
