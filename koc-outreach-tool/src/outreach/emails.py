"""Email extraction, junk filtering and ranking."""
from __future__ import annotations

import re

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")

# Emails we never want to surface as a real contact (assets, placeholders, infra).
JUNK_EMAIL = re.compile(
    r"(\.(png|jpe?g|gif|svg|webp)$)|sentry|wixpress|example\.|@2x|"
    r"no-?reply|your@|name@|email@|domain\.com|user@|@sentry",
    re.IGNORECASE,
)

# Mailbox prefixes that indicate a deliberate contact address, best first.
CONTACT_PREFIXES = ("info@", "contact@", "hello@", "press@", "hi@", "team@")


def pick_email(*sources: str) -> str:
    """Return the first email found scanning each source string in order."""
    for src in sources:
        if not src:
            continue
        m = EMAIL_RE.search(src)
        if m:
            return m.group(0)
    return ""


def good_emails(text: str) -> list[str]:
    """De-duplicated, non-junk emails found in a blob of text/HTML."""
    seen: set[str] = set()
    out: list[str] = []
    for m in EMAIL_RE.findall(text or ""):
        e = m.strip().strip(".")
        if e.lower() in seen or JUNK_EMAIL.search(e):
            continue
        seen.add(e.lower())
        out.append(e)
    return out


def best_email(cands: list[str], prefer_domain: str = "") -> str:
    """Pick the most contact-worthy email, preferring one on ``prefer_domain``."""
    if not cands:
        return ""
    if prefer_domain:
        for e in cands:
            if e.split("@")[-1].lower() == prefer_domain:
                return e
    for kw in CONTACT_PREFIXES:
        for e in cands:
            if e.lower().startswith(kw):
                return e
    return cands[0]
