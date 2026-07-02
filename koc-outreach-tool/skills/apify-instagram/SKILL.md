---
name: apify-instagram
description: Run Apify's Instagram Scraper actor (off your own account, via Apify proxies) to fetch profile data and external website links as a fallback or cross-check. Use when you want robust profile data without account risk, or to surface websites for email backfill.
---

# apify-instagram

Runs actor `shu8hvrXbJbY3Eb9W` (apify/instagram-scraper) on Apify's
infrastructure — its proxies, not your Instagram session, so there is **no risk
to your account**.

## Important limitation

This actor does **not** return a contact email field. It returns followers,
bio, and `externalUrls`. Its value in this toolkit is surfacing **websites** for
handles we couldn't get an email for — then feed those into `email-discovery`'s
`backfill.py --apify`.

## Auth (once)

```bash
curl -fsSL https://apify.com/install-cli.sh | bash   # install CLI
apify login                                          # or export APIFY_TOKEN=...
```

## Run (gaps only = cheapest)

```bash
python3 skills/apify-instagram/scripts/apify_run.py \
    --gaps-only \
    --crawl   export/aying/01_ig_crawl.csv \
    --dataset export/aying/apify_dataset.json

# then backfill emails from the websites it found:
python3 skills/email-discovery/scripts/backfill.py \
    --crawl export/aying/01_ig_crawl.csv \
    --input input/Aying.csv \
    --apify export/aying/apify_dataset.json
```

`--gaps-only` targets handles that are known but still have no email (lowest
cost). Drop it to re-pull all `ok` handles. `--build-input` writes the actor
input without calling (free dry run).

## Cost

~$2.30 / 1,000 results (≈$1 for ~250 profiles). Prefer the free
**instagram-crawl** + **email-discovery** path first; use this for gaps,
cross-checking, or when you want to keep your own account out of it.
