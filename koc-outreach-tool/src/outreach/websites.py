"""Scrape websites / link-aggregators for contact emails and IG handles."""
from __future__ import annotations

import re

from playwright.sync_api import TimeoutError as PWTimeout

from .emails import best_email, good_emails
from .text import domain_of

# Pages most likely to expose a contact email, tried in order.
CONTACT_PATHS = ["", "/contact", "/contact-us", "/about", "/about-us", "/press", "/team"]
IG_LINK_RE = re.compile(r"instagram\.com/([A-Za-z0-9._]+)")
IG_SKIP = {"p", "reel", "reels", "explore", "stories", "tv", "accounts", ""}
_MAILTO_RE = re.compile(r'mailto:([^"\'?\s>]+)')

# Link aggregators that hold no email themselves — follow their outbound links.
AGGREGATOR_HOSTS = ("linktr.ee", "beacons.ai", "linkin.bio", "bio.link",
                    "campsite.bio", "lnk.bio", "linkpop.com", "many.link")
# Social / store hosts we don't treat as the entity's own website.
_SKIP_HOSTS = ("instagram.com", "facebook.com", "twitter.com", "x.com",
               "tiktok.com", "youtube.com", "youtu.be", "spotify.com",
               "apple.com", "linkedin.com", "patreon.com", "threads.net",
               "discord.", "t.me", "amazon.", "/cdn-cgi/",
               # asset / infra hosts that show up in page markup
               "fonts.googleapis.com", "fonts.gstatic.com", "gstatic.com",
               "googleapis.com", "cloudflare", "cdn.", "jsdelivr", "schema.org",
               "w3.org", "googletagmanager", "google-analytics")
_HREF_RE = re.compile(r'href=["\'](https?://[^"\']+)["\']', re.IGNORECASE)


def _page_html(page) -> str:
    """Read page.content(), retrying through JS redirects (linktr.ee, substack)."""
    for _ in range(3):
        try:
            return page.content() or ""
        except Exception:
            try:
                page.wait_for_timeout(800)
            except Exception:
                break
    return ""


def email_from_website(page, website: str) -> tuple[str, str, str]:
    """Return (email, source_url, confidence) by scraping site + contact pages."""
    if not website:
        return "", "", ""
    base = website.rstrip("/")
    dom = domain_of(base)
    for path in CONTACT_PATHS:
        url = base + path
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=20000)
        except (PWTimeout, Exception):
            continue
        html = _page_html(page)
        cands = good_emails("\n".join(_MAILTO_RE.findall(html)) + "\n" + html)
        email = best_email(cands, prefer_domain=dom)
        if email:
            conf = "high" if (email.split("@")[-1].lower() == dom
                              or path in ("/contact", "/contact-us")) else "medium"
            return email, url, conf
    return "", "", ""


def is_aggregator(url: str) -> bool:
    return any(host in (url or "").lower() for host in AGGREGATOR_HOSTS)


def outbound_links(page, url: str) -> list[str]:
    """Real outbound websites from a link-aggregator page (socials/stores skipped)."""
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        page.wait_for_timeout(1200)  # let the SPA render its link buttons
    except (PWTimeout, Exception):
        return []
    html = _page_html(page)
    seen, out = set(), []
    for href in _HREF_RE.findall(html):
        low = href.lower()
        if is_aggregator(low) or any(h in low for h in _SKIP_HOSTS):
            continue
        base = href.split("?")[0].rstrip("/")
        if base.lower() not in seen:
            seen.add(base.lower())
            out.append(base)
    return out


def _alnum(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def _domain_core(url: str) -> str:
    """Registrable name of a domain, e.g. https://hettymckinnon.com/x -> hettymckinnon."""
    dom = domain_of(url)
    parts = dom.split(".")
    return parts[-2] if len(parts) >= 2 else (parts[0] if parts else "")


def owns_site(url: str, handle: str = "", name: str = "") -> bool:
    """True if a site is plausibly the entity's OWN (domain matches handle/name).

    Guards aggregator-following against grabbing a publisher's email (a writer's
    linktr.ee linking to a Forbes article must not yield feedback@forbes.com).
    """
    core = _alnum(_domain_core(url))
    if not core:
        return False
    h = _alnum(handle)
    n = _alnum(name)
    if h and (core == h or core in h or h in core):
        return True
    if n and len(core) >= 4 and (core in n or n in core):
        return True
    return False


def email_via_aggregator(page, url: str, handle: str = "", name: str = "") -> tuple[str, str, str]:
    """Follow an aggregator's outbound links; scrape only the entity's OWN site.

    Without an owning-site match we return nothing — a wrong email (e.g. a
    publisher's) is worse than a blank for outreach.
    """
    owned = [s for s in outbound_links(page, url) if owns_site(s, handle, name)]
    for site in owned[:3]:
        email, src, conf = email_from_website(page, site)
        if email:
            return email, src, conf
    return "", "", ""


def ig_handle_from_website(page, website: str) -> str:
    """Find the first real instagram.com/<handle> link on a website."""
    if not website:
        return ""
    try:
        page.goto(website, wait_until="domcontentloaded", timeout=20000)
    except (PWTimeout, Exception):
        return ""
    for cand in IG_LINK_RE.findall(_page_html(page)):
        if cand.lower() not in IG_SKIP:
            return cand
    return ""
