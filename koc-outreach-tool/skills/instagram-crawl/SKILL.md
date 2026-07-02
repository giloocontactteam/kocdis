---
name: instagram-crawl
description: Crawl Instagram profiles from a KOC CSV using a logged-in Chrome session over CDP, extracting followers, bio, website, category and contact email. Use when you need profile data or emails for handles listed in a sheet.
---

# instagram-crawl

Fetches Instagram profile data via your **already-logged-in** Chrome, attached
over the Chrome DevTools Protocol. It calls Instagram's own `web_profile_info`
endpoint from the page so requests carry real session cookies.

## When to use

- You have a KOC CSV with IG handles/links and need profile data + emails.
- You want the contact email Instagram exposes on Business/Creator accounts.

## Account safety

Run under a brand/secondary account, not your personal one — automated profile
fetching carries some rate-limit/flag risk. Use polite delays (defaults are 4–9s).

## Run

```bash
# 1. See which Chrome profiles have an Instagram login (statuses: logged_in / cookies / none)
python3 skills/instagram-crawl/scripts/seed_and_launch.py --list

# 2. Launch an authenticated headless debug Chrome (does NOT touch your main Chrome).
#    Use a profile shown as "logged_in" above — preferably a brand/secondary account.
python3 skills/instagram-crawl/scripts/seed_and_launch.py --profile "<your logged_in profile>"

# 3. Crawl
python3 skills/instagram-crawl/scripts/crawl.py \
    --input  input/Aying.csv \
    --output export/aying/01_ig_crawl.csv

# 4. Stop the debug Chrome
python3 skills/instagram-crawl/scripts/seed_and_launch.py --stop
```

## Output

One row per source row with: `resolved_handle, profile_url, full_name,
followers, following, posts, is_private, is_business, category, email, website,
bio, status`. `status` ∈ ok / not_found / login_required / no_ig_handle / timeout.
Idempotent — re-running skips 序號 already present.

## Limits

- Only Business/Creator accounts expose an email natively (the contact button);
  for the rest, use the **email-discovery** skill.
- Wrong/dead handles return `not_found` — discover correct ones via web search
  then re-crawl.
