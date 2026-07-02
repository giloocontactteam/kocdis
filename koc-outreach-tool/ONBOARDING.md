# Onboarding

Setup guide for a new owner of this repo. If you're an AI agent (Claude/Codex)
helping someone onboard, walk them through these steps in order and stop at each
checkpoint until it passes.

## What you must provide

| Thing                                               | Why                                                                   | Cost                   |
| --------------------------------------------------- | --------------------------------------------------------------------- | ---------------------- |
| **Google Chrome**, logged into an Instagram account | The crawler reuses your real, logged-in session over CDP              | free                   |
| **A brand / secondary IG account** (recommended)    | Automated crawling carries account risk — don't use your personal one | free                   |
| **An Apify account** (optional)                     | Fallback scraping off your own IG account                             | ~$2.30 / 1,000 results |

You do **not** need anyone else's credentials — every secret is your own and
stays on your machine. Nothing here ships with logins baked in.

## Step 1 — Python deps

```bash
python3 -m pip install -e .     # Python >= 3.9; installs playwright/pandas/openpyxl
```

No `playwright install` step is needed — the crawler attaches to your _real_
Chrome, not Playwright's bundled browser.

✅ Checkpoint: `python3 -c "import outreach; print(outreach.__version__)"` prints a version.

## Step 2 — Chrome + Instagram login

1. Open Google Chrome and log into Instagram (use a brand/secondary account).
2. Detect which Chrome profile holds that login:
   ```bash
   python3 skills/instagram-crawl/scripts/seed_and_launch.py --list
   ```
   You'll see each profile with `logged_in` / `cookies` / `none`. Pick a
   `logged_in` one.
   - Non-standard install? Set `CHROME_BINARY` and/or `CHROME_USER_DATA` env vars.

✅ Checkpoint: at least one profile shows `logged_in`.

## Step 3 — Launch the debug browser & smoke-test a crawl

```bash
python3 skills/instagram-crawl/scripts/seed_and_launch.py --profile "<your logged_in profile>"
python3 skills/instagram-crawl/scripts/crawl.py \
    --input input/<your-list>.csv --output export/<list>/01_ig_crawl.csv --limit 3
python3 skills/instagram-crawl/scripts/seed_and_launch.py --stop
```

This seeds a throwaway debug profile from your cookies and runs headless — your
main Chrome is never touched.

✅ Checkpoint: the 3 rows print `status=ok` with follower counts.

## Step 4 — Apify (optional)

```bash
curl -fsSL https://apify.com/install-cli.sh | bash   # install CLI
apify login                                          # your account (or export APIFY_TOKEN=...)
```

Then see `skills/apify-instagram/SKILL.md`. Remember: this actor returns
websites, **not** emails — its job is feeding sites into the email backfill.

## House rules (read before running at scale)

- **Account safety / ToS:** automated IG fetching breaks Instagram's terms;
  worst case is an account block. Use a secondary account, keep the built-in
  delays, prefer `--skip-ig` once profiles are crawled, and use Apify when you'd
  rather keep your own account out of it.
- **PII:** `input/` and `export/` hold scraped emails and are **gitignored** —
  never `git add -f` them or share the CSVs loosely.
- **Provenance:** every discovered email keeps `email_source` +
  `email_confidence`; don't strip these — they're how you audit a list.

## Where to go next

- `README.md` — full pipeline + layout.
- `CLAUDE.md` / `AGENTS.md` — agent working rules.
- `skills/*/SKILL.md` — per-capability detail.
