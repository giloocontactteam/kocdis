# AGENTS.md

Entry point for OpenAI Codex (and other agents). This repo is **skill-based**:
capabilities live under `skills/<name>/` with a `SKILL.md` describing when to use
them and the exact commands to run.

## Read order

0. **New owner / fresh machine?** `ONBOARDING.md` first (Chrome login, Apify, smoke test).
1. This file.
2. `skills/<name>/SKILL.md` for the skill you need.
3. `src/outreach/` for the shared library the skills call.

The guidance is identical to `CLAUDE.md` — read it for the full conventions.
Summary:

- **Goal:** a contact email per KOC. The IG handle is just one route.
- **Skills are thin CLIs;** all reusable logic is in `src/outreach/`
  (`text, emails, igclient, websites, sheet, browser`). Don't duplicate helpers.
- **input/ vs export/:** read from `input/`, write only to `export/<list>/`
  with stage-numbered files (`01_ig_crawl.csv`, `02_contacts.csv`).
- **Never commit data** (`input/`, `export/` are gitignored — they contain PII).
- **Account safety:** crawl under a brand/secondary IG account with delays;
  prefer Apify when you don't want your own account in the loop.
- **Keep** `email_source` + `email_confidence` on every discovered email, and
  keep the idempotent / incremental-write behavior.

## Skills

| Skill             | Purpose                                             |
| ----------------- | --------------------------------------------------- |
| `xlsx-to-csv`     | Split an Excel workbook into per-sheet CSVs         |
| `instagram-crawl` | Crawl IG profiles via a logged-in Chrome (CDP)      |
| `email-discovery` | Find emails: IG → website → IG-from-website cascade |
| `apify-instagram` | Fallback scrape via Apify, off your own account     |

## Setup

`pip install -e .`, then `playwright install chromium` if not reusing system
Chrome. Python ≥ 3.9.
