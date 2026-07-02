---
name: email-discovery
description: Find a contact email for every KOC by trying multiple sources (Instagram profile, website + contact pages, and IG-link-from-website) until one is found, then backfill the crawl CSV. Use when rows are missing emails after crawling.
---

# email-discovery

Treats **email as the KPI** — the IG handle is just one route. For each row
still missing an email, runs a precision-ordered cascade until it finds one.

## Two scripts

### discover.py — full cascade

1. `ig_api` — known handle → business/public email or an email in the bio
2. `website_scrape` — fetch website + `/contact` `/about` … for emails
3. `ig_from_website` — no handle? find the IG link on the website, then `ig_api`

```bash
python3 skills/email-discovery/scripts/discover.py \
    --input  input/Aying.csv \
    --crawl  export/aying/01_ig_crawl.csv \
    --output export/aying/02_contacts.csv \
    --skip-ig          # website-only; use once IG profiles are already crawled
```

### backfill.py — scrape every known website, write in place

Unions websites from the crawl output, the source sheet, and (optionally) an
Apify dataset's `externalUrls`. Writes each email back **incrementally** so a
crash never loses progress.

```bash
python3 skills/email-discovery/scripts/backfill.py \
    --crawl export/aying/01_ig_crawl.csv \
    --input input/Aying.csv \
    --apify export/aying/apify_dataset.json   # optional
```

## Quality safeguards

- Junk filter drops `no-reply@`, placeholders, image filenames, infra emails.
- Same-domain emails are preferred (`info@theirsite.com` over a third party);
  off-domain hits are flagged lower confidence in `email_confidence`.
- Every email records `email_source` + `email_confidence` for auditing.

## Prereq

An authenticated debug Chrome on port 9222 (see the **instagram-crawl** skill's
`seed_and_launch.py`). Use `--skip-ig` to avoid re-hitting Instagram.
