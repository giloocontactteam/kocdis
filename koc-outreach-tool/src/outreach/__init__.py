"""outreach — shared library for the KOC outreach data-enrichment toolkit.

The skills under ``skills/`` are thin CLIs; all reusable logic lives here:

- :mod:`outreach.text`     — string cleaning, handle normalization, domains
- :mod:`outreach.emails`   — email regex, junk filtering, ranking
- :mod:`outreach.igclient` — logged-in Instagram profile fetch over CDP
- :mod:`outreach.websites` — scrape sites/contact pages for emails & IG links
- :mod:`outreach.sheet`    — read the KOC source sheet, dedup helpers
- :mod:`outreach.browser`  — seed & launch an authenticated debug Chrome
"""

__all__ = ["text", "emails", "igclient", "websites", "sheet", "browser"]
__version__ = "0.1.0"
