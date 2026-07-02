# outreach

A **skill-based** toolkit for enriching KOC (key opinion consumer) outreach
lists: split an Excel workbook into CSVs, crawl Instagram profiles, and discover
a contact **email** for every row through multiple fallback strategies.

Designed to be driven by AI coding agents (Claude Code and OpenAI Codex) as well
as run by hand. The goal that organizes everything: **a contact email per KOC.**

## Layout

```
input/           # source data you provide (xlsx, per-list CSVs) — gitignored
export/          # results, one folder per list, staged files — gitignored
  <list>/
    01_ig_crawl.csv     # instagram-crawl output
    02_contacts.csv     # email-discovery output
    apify_dataset.json  # optional apify-instagram raw data
skills/          # the capabilities, each a SKILL.md + scripts/
  xlsx-to-csv/        split a workbook into per-sheet CSVs
  instagram-crawl/    crawl IG profiles via a logged-in Chrome (CDP)
  email-discovery/    find emails: IG → website → IG-from-website cascade
  apify-instagram/    fallback scrape via Apify (off your own account)
src/outreach/    # shared library imported by all skills (no duplication)
  text.py  emails.py  igclient.py  websites.py  sheet.py  browser.py
tests/           # unit tests for the pure helpers
```

## Quickstart

```bash
pip install -e .          # makes `import outreach` work; installs deps
# (no `playwright install` needed — the crawler attaches to your real Chrome)

# 1. Workbook -> CSVs
python3 skills/xlsx-to-csv/scripts/xlsx_to_csv.py \
    --input "input/北美 KOC 分潤計畫名單.xlsx" --outdir export/_sheets
cp "export/_sheets/Aying.csv" input/Aying.csv

# 2. Find which Chrome profile is logged into the IG account you want, then launch
python3 skills/instagram-crawl/scripts/seed_and_launch.py --list      # shows logged_in profiles
python3 skills/instagram-crawl/scripts/seed_and_launch.py --profile "<your profile>"
python3 skills/instagram-crawl/scripts/crawl.py \
    --input input/Aying.csv --output export/aying/01_ig_crawl.csv

# 3. Fill the email gaps (website-only is safest after crawling)
python3 skills/email-discovery/scripts/backfill.py \
    --crawl export/aying/01_ig_crawl.csv --input input/Aying.csv

# 4. (optional) Apify fallback for stubborn gaps, then backfill its websites
python3 skills/apify-instagram/scripts/apify_run.py --gaps-only \
    --crawl export/aying/01_ig_crawl.csv --dataset export/aying/apify_dataset.json
```

## Conventions

- **input/export split.** Never write results into `input/`. Each list gets
  `export/<list>/` with stage-numbered files (`01_…`, `02_…`).
- **Skills are thin.** All reusable logic lives in `src/outreach/`; skill
  scripts are CLIs that import it.
- **Email provenance.** Every discovered email carries `email_source` and
  `email_confidence` so results stay auditable.
- **Account safety.** Crawl under a brand/secondary IG account; prefer Apify
  when you don't want your own account in the loop.

See `CLAUDE.md` / `AGENTS.md` for agent-facing guidance and `skills/*/SKILL.md`
for per-skill detail.
