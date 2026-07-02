# CLAUDE.md

Agent guidance for this repo. (Codex: see `AGENTS.md`, which mirrors this.)

## What this is

A skill-based KOC outreach enrichment toolkit. **The goal is a contact email per
KOC.** The Instagram handle is a means to that end, not the end itself.

> **New owner / fresh machine?** Walk through `ONBOARDING.md` first (Chrome
> login, Apify, smoke test) before running anything at scale.

## How to work here

1. **Pick the skill, read its `SKILL.md` first.** Capabilities live under
   `skills/<name>/`; each `SKILL.md` has when-to-use + exact commands.
2. **Reuse the shared library.** All logic is in `src/outreach/` — `text`,
   `emails`, `igclient`, `websites`, `sheet`, `browser`. Add new logic there and
   keep skill scripts as thin CLIs. Do **not** copy helpers between skills.
3. **Respect the input/export split.** Read source data from `input/`, write
   results only to `export/<list>/` using stage-numbered names
   (`01_ig_crawl.csv`, `02_contacts.csv`).

## Pipeline

`xlsx-to-csv` → `instagram-crawl` (needs logged-in Chrome) → `email-discovery`
(fills gaps) → `apify-instagram` (optional fallback, off your own account).

## Hard rules

- **Account safety:** crawl under a brand/secondary IG account; use polite
  delays (defaults in the scripts). Prefer `--skip-ig` once profiles are crawled
  so you don't re-hit Instagram.
- **Never commit data.** `input/` and `export/` are gitignored — they hold PII
  (scraped emails). Don't `git add -f` them.
- **Email provenance is mandatory:** keep `email_source` + `email_confidence`.
- **Idempotency:** the crawl skips rows already done; backfill writes
  incrementally. Don't remove these safeguards.

## Browser auth model

`src/outreach/browser.py` seeds a throwaway debug profile from a logged-in
Chrome profile's cookies and launches headless Chrome on port 9222 — your main
Chrome is never disturbed. Find logged-in profiles with
`seed_and_launch.py --list`.

## Setup

`pip install -e .` then `playwright install chromium` (skippable if reusing
system Chrome over CDP). Python ≥ 3.9.
